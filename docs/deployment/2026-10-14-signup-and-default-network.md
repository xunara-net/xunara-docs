# 2026-10-14：公开开户唯一与用户默认网段验收

## 范围

公开开户用户名唯一、旧同名账户保留、未完成开户补偿保护，以及用户默认 IPv4 池选择。
本地回归、最终源码 GitHub CI 和正式站实测通过，Server `/version` 为 `9a4e786`。
此结论仅覆盖本切片，不代表整个产品或独立原生客户端入口已经完成。

| 仓库 | 提交 |
|---|---|
| Server | `9a4e786`（前序用户名约束 `fb1b681`） |
| Web | `ced0f64` |
| Deploy | `b4f327b`（运维说明，无安装器 / nginx 代码修改） |

接口与决策以[服务端说明](https://github.com/xunara-net/xunara-server/blob/main/docs/signup-network-settings.md)、
[Proposal](https://github.com/xunara-net/xunara-server/blob/main/docs/proposals/2026-10-14-signup-uniqueness-and-default-network.md)
和 [ADR-0043](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0043-public-signup-uniqueness-and-default-network.md)为准。

## 已验证的本地边界

- 同名、大小写、空白及并发公开开户最多产生一个网络；用户名不是通过随机组织
  后缀变成新的账号。不同用户名的短名碰撞仍能开通不同网络。
- SQLite 两连接、重启、组织注册表 v1 升级、旧同名用户与密码保持、存储失败、
  未初始化回滚，以及已提交 owner 但确认丢失时仍能密码登录。
- 未完成名称同时保留组织 ID；另一连接不能在退出到套餐清理之间复用。
  构造失败只清理实际提交了组织的请求，冲突请求不释放别人的占用。
- 原默认池保留为附加池；保存后新设备分配使用新默认池，已有设备 IP 保持，
  标准 MapResponse 仍是单主机地址/路由。开启自定义网段不取消 Free 10 设备上限。
- Web 448 项单测、类型检查与生产构建通过；真实隔离 HTTPS 共享控制台 9 阶段
  回归通过，重复注册中文提示、取消不写入、手机预览确认与重载验证均通过，
  390px 无横向溢出或 JavaScript 错误。

并发复查发现失败冲突请求可能错误释放同 ID 的未完成占用，已补上所有权路径
和持久 ID 保护，并为最终源码重新执行 Go 全量 build/vet/test/race，不沿用前一
次较早提交的竞态结果冒充最终结果。
最终 Go build/vet/test 与全量 race 通过，Control 常规 87.658 秒、race 761.690 秒，
Identity race 141.917 秒；没有降低生产密码哈希强度。
最终 CI：[Server](https://github.com/xunara-net/xunara-server/actions/runs/38506929732)、
[Web](https://github.com/xunara-net/xunara-web/actions/runs/38505252067)、
[Deploy](https://github.com/xunara-net/xunara-deploy/actions/runs/38505253018)均通过。

## 发布约束

只追加组织注册表 v2；Identity、State、Plans 无新迁移。不更改原用户名 / 密码 /
活跃会话 / 独立网络 / Noise 与 TLS / 节点 IP；不自动删除旧同名账户。
调试站按运营者要求仅在 Free 持久套餐目录开启自定义网段，其他额度不变，
程序仍走原 Entitlement，内置套餐初始值不变。

升级先停止公共写入和全部旧控制面，私有备份完整状态、配置、程序与静态资源；
比较原身份 / 节点 / 预授权密钥 / 配置摘要后才恢复公共入口。
公共写入恢复后不能自动覆盖旧快照。测试仅允许自己的临时网络修改，结束后移除
活动测试网络；归档、名称墓碑与网段保留仍遵循产品规则。

## 正式站实测

2026-10-14 12:01（Asia/Shanghai）完成正式升级，Nginx / Control / Relay 均 active。
原 7 个托管网络与默认网络保留；升级前发现的 2 组旧同名账户未删除或合并。
组织注册表 v1 升级至 v2，补齐 6 个既有用户名占用；其它模块数据库版本不变。
原账户 / 密码哈希 / 人类会话 / 外部与 Passkey 绑定 / API 与预授权密钥 /
节点地址 / 配置 / Noise 与 TLS 摘要前后相同，平台令牌没有更换。
仅在 Free 持久目录开启自定义网段，10 设备及其它额度逐字段保持。
私有回退备份：`/root/xunara-rollback/signup-default-20261014T040113Z`；
公开写入恢复后不能覆盖旧快照。

通过正式站本机 HTTPS 入口、系统根证书与真实 Host/SNI，验证现有同名和大小写
变体返回 409，不改变原组织；只新建自己的临时网络完成注册 → 同源控制台
handoff → 实际密码登录 → Free 默认池预览 / 保存 / 切换 → 旧池保留和过期版本
409，根站不接受租户 Cookie。最后删除活动临时网络，不修改原用户网段。
测试网络的归档、名称墓碑及网段预留保留，不能称为完全无写入的生产检查。

公网 HTTPS `/health` 与 `/version` 通过；Chromium 390×844 正常校验证书，
只读检查新注册唯一提示，页面无横向溢出或 JavaScript 错误。
公网浏览器没有代用户登录或修改真实账户；默认池浏览器全流程由隔离 HTTPS
夹具验证，生产实写由自己的临时网络 API 验证，不以此冒充安卓客户端实测。

## 尚未解决

独立租户的旧 nip.io 原生客户端地址及 DNS/TLS 问题没有在本切片伪装为已修复。
主域名网页能访问不能证明该设备入口可用，也不能直接替换为默认网络的入口。
共享原生网关与正式租户域名 / 受信证书需要独立完成兼容性设计和实测。
这是三层地址管理，不是 VLAN，也不包含 Quad100 自动换址、邮箱身份验证或
全局账户跨租户成员模型。
