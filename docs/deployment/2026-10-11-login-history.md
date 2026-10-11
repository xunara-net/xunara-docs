# 本人登录记录与会话活动：开发与 HTTPS 调试站验收

## 交付范围

安全中心先展示活动会话卡片，手机无需横向滚动表格即可查看当前登录、首次来源
IP、浏览器 / 系统线索与最近活动，并沿用已有会话撤销入口。成功登录记录独立
折叠、按需加载，支持前后页、刷新和明确重试；读取故障保留上次确认的页面，
标明旧数据，不以空列表或退出登录掩盖存储故障。

记录与成功创建会话同事务，撤销、改密、平台恢复、禁用、解绑和轮换同步原有
生命周期。过期会话清理不删除登录记录，账号删除才在事务内清除这两类私人
数据。轮换继承首次来源，不冒充新的认证；旧记录来源未知，不补造 IP / 浏览器。
IP / UA 只是显示线索，不是机器身份、地理位置、设备信任或权限依据。

本人记录仅由所属租户的 Human Session 读取，平台 Bearer、服务 API Key、
MachineKey 和匿名不能读取。Free / 普通成员不另加套餐限制，不提供其他用户
查询参数或新超管历史入口。活动由数据库条件控制单调、分钟级持久更新，不
延长原会话有效期，不依赖单进程缓存；写入失败保持 Cookie 并明确报错。

使用见[用户手册](../user/login-history.md)。接口、来源规则、迁移与保留边界以
[服务端说明](https://github.com/xunara-net/xunara-server/blob/main/docs/account-login-history.md)、
[ADR-0032](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0032-account-login-history.md)
和 [Deploy](https://github.com/xunara-net/xunara-deploy) 为准，不在本仓库复制字段或 DDL。
跨仓库任务见 [Server #15](https://github.com/xunara-net/xunara-server/issues/15)。

## 源码与上线

| 仓库 | 本轮源码 |
|---|---|
| Server | [`01a075b`](https://github.com/xunara-net/xunara-server/commit/01a075bb7aed31c5a62a3a2aa0631b6f05e6744e) |
| Web | [`e187c77`](https://github.com/xunara-net/xunara-web/commit/e187c77fcc1ba0e3e8189a63e880fc7cafea983e) |
| Admin 共享验收脚本 | [`adc8204`](https://github.com/xunara-net/xunara-admin/commit/adc8204c6987200d1ee49ca57b5ea5a7ac18e9b7) |
| Deploy 升级与隐私说明 | [`33822e4`](https://github.com/xunara-net/xunara-deploy/commit/33822e44e44c1d545e257f32b37441296348a598) |

对应 CI 全绿后，2026-10-11 19:23（Asia/Shanghai）开始维护升级原自签 HTTPS
调试站，19:30 完成公网与原数据复核。Server 从干净 Git archive 构建，完整提交
写入版本；Web / Admin 来自干净提交的生产构建，逐项校验线上 45 个 Web / 22 个
Admin 静态产物。Admin 本轮只改验收脚本，业务页面没有新增登录记录读取权。

- 用户入口：`https://fakeop4.onbed.cn:9090/security`，必须登录后访问。
- 原测试 CA：`https://fakeop4.onbed.cn:9090/.well-known/xunara-test-ca.pem`。
- 仍是自签测试证书，不宣称已完成正式公网 CA / 域名运维。

## 公网验证与原数据

关闭公网写入、停止全部旧控制面并排空旧代理 worker 后，成套备份数据库、
配置、密封密钥、TLS、服务环境、二进制和静态产物，再原子交换发布产物。
两个活动租户 identity v17→18；state v24 / plans v4 不变。开放前逐项比较原表
原列原数据，账号状态、密码、绑定、设备、网段 / IP、套餐、DNS、ACL 与认证
配置保持，不将历史台账中的配置值强套到当前用户状态。

公网只读检查版本、健康、静态文件、平台用户列表和私人记录的拒绝边界。
真实 Chromium 验证 320 / 390 / 768 / 1440px 登录页无整体横向溢出，匿名安全
中心返回登录并保留目标，后台保持独立登录；页面 JavaScript 错误为零。
没有登录原站人类账号、读取其私人登录记录、创建会话或设备、重置密码、生成
恢复码、改变注册策略或配置假提供方，操作方业务写入为零。

公网使用 upstream `controlhttp` 验证可信 HTTPS 控制密钥、TS2021 / Noise
upgrade、early payload 和 HTTP/2 未知节点拒绝，设备注册为零。仅此探测不
扩展为本轮官方客户端全 OS 或双设备数据面验收。

开放后复核 106 张原人类身份 / 认证表，43 个原会话的凭据、有效期和撤销事实
保持，活动时间合法性单独检查，本次观察到活动更新为零。两个活动身份库新增
24 条仍有用户归属的 legacy 记录，首次来源全部未知；归档 / 已无用户归属的
旧会话不伪造登录记录，因此记录数不等于全部原会话数。现有恢复码、原账号
禁用状态及受保护配置保持，独立 Relay 没有重启。

备份：`/root/xunara-rollback/20261011T112317Z-login-history`，目录 0700，
快照与报告 0600，包含私人数据 / 密钥，不可公开。归档中的代理配置是维护
模式，成套回退还要恢复单独保存的原代理配置。旧实例不得与新身份库混版本
运行；尝试开放公网前就禁止自动恢复旧快照，避免重载结果未知时覆盖新业务。
公开业务受理后不得覆盖旧快照。备份保留，本轮远程发布暂存已清理；临时 SSH
与平台凭据文件已删除，不进入 Git 或公开验收报告。

## 自动验证

- 最终全量 Go build / vet / test / race 全部通过，race 使用 20 分钟预算。
- 身份层覆盖来源规范化、各认证入口、独立历史、清理 / 删除、撤销 / 轮换、
  跨连接分钟节流 / 单调更新、分页同时间边界、迁移 / 重启及忽略或失败写入回滚。
- HTTP 验证本人 / 其他成员 / 跨租户 / 平台与服务身份边界、受信代理最后一跳、
  非法 query、503 保留 Cookie 与读取故障不伪造空列表。
- Web 231 / Admin 51 单测、类型检查与生产构建通过；部署脚本本地语法检查
  通过，ShellCheck 由 Deploy CI 验证，未冒充本机已安装并执行。
- 干净发布产物的 73 阶段跨模块 Chromium 回归通过，涵盖现有 OAuth2 / OIDC、
  成员、ACL、DNS、地址与中继及新登录记录，JavaScript 页面错误为零。
- 21 阶段隔离真实自签 HTTPS 回归通过，包括来源 / 手机卡片、分页、故障重试、
  活动失败关闭、过期会话清理后的历史、生命周期镜像及实际守护进程重启；
  未接触公网第三方提供方，分页样本明确是隔离测试种子，不冒充同数量真实登录。
- 真实已发布 identity v17 二进制初始化隔离状态，v18 升级保留 44 张原表事实
  和原凭据；v17 拒绝新库且不改原表；成套恢复旧状态 / 旧产物后原登录仍可用。
  四阶段通过，不是在生产注入故障，也不是把当前迁移倒退当作旧版本验证。
- 部署快照校验的隔离回归允许仅追加迁移，保留原禁用状态，能发现误改用户 / 凭据；
  最终会话校验区分不可变凭据与合法活动，不为了忽略差异跳过整张会话表。

可复制命令和前置条件见
[服务端验证说明](https://github.com/xunara-net/xunara-server/blob/main/docs/account-login-history.md#验证与升级)
与 [Admin 浏览器验收](https://github.com/xunara-net/xunara-admin#浏览器集成验收)。
本轮源码 CI：
[Server](https://github.com/xunara-net/xunara-server/actions/runs/38134235621)、
[Web](https://github.com/xunara-net/xunara-web/actions/runs/38134735276)、
[Admin](https://github.com/xunara-net/xunara-admin/actions/runs/38134237729)、
[Deploy](https://github.com/xunara-net/xunara-deploy/actions/runs/38134238767) 全部通过。
手册与 ADR 索引 [CI 已通过](https://github.com/xunara-net/xunara-docs/actions/runs/38134240065)，
本上线记录由本仓库 CI 再次检查。

## 未完成范围

本次只补本人成功认证和会话生命周期，不包括失败尝试、城市定位、设备可信
认证或超管读取所有人历史。记录目前随账号保留，没有自动按年龄清理或个人
数据导出；旧版已清理的会话不能恢复，UA 可伪造，不保证最近活动等于在线。

官方 Tailscale wire 协议、机器 / 服务身份、Headscale 与套餐额度不变。
邮箱验证 / 邮件投递 / 自动邮件找回、2FA / 恢复码、独立超管人身份、完整账户
生命周期 / 全局跨租户账号、订阅支付、真实公网第三方应用、多实例生产验收与
全 OS 数据面矩阵仍需独立开发和验收，不宣布全部产品已完成。
