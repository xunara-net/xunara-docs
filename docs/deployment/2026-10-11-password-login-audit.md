# 密码登录原子审计与累计升级验收（2026-10-11）

## 版本与当前状态

- Server：`0ab02aac3a12c129a9eb69ce5dcbebf532fa75cf`；
  [任务 #9](https://github.com/xunara-net/xunara-server/issues/9)、
  [ADR-0026](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0026-atomic-password-login-audit.md)。
- Web：`02527c91ff3615ea2e7a37469ca80fddeb60d879`；本轮未再改前端源码。
- Admin：`3a19ff4c3d58425f287918e7a5fb798012bd42e2`；生产源码不变。
- Server [CI 38090680394](https://github.com/xunara-net/xunara-server/actions/runs/38090680394)
  completed/success，build/vet/test/完整竞态全部通过，head SHA 匹配上述提交。
  Web [CI 38068653102](https://github.com/xunara-net/xunara-web/actions/runs/38068653102)和
  Admin [CI 38068654617](https://github.com/xunara-net/xunara-admin/actions/runs/38068654617)
  对应同一上述前端提交也全部通过。
- 北京时间 2026-10-11 06:33 完成调试站维护升级，Server 从 `bb32d65` 更新为上述
  完整提交；两活动租户 state v23→24，identity v13/plans v4 不变。公网验收已通过。

## 修改、原因与安全边界

真实 SQLite 故障先复现：忽略会话插入或拒绝登录成功审计时，旧实现仍返回 200。
现在密码会话、登录成功与会话创建两项必需事件共享原身份事务；两项审计或会话
插入的 SQL 错误/零行写入都失败关闭，提交后才签发 Cookie。控制层两份成功日志
调用已删除，没有将旧分步实现和新事务并行使用；新边界增加中文注释。

日志只绑定人类 user ID、local 提供方与 session ID，不保存登录名、密码、密码
hash、token 或 token hash。旧 Cookie/会话不因失败而被清除或撤销。失败登录尽力
日志及持久限流预算仍是原边界，不将事务回滚包装成撤销尝试预算。

本切片不新增角色，不改变 Human/Machine/Service 的关系，也不是完整登录历史、
失败事件可靠投递、OIDC/Passkey 整体事务、2FA 或邮箱恢复。

## 干净产物与验证

三个仓库各自从上述 Git 提交归档，重新安装前端依赖、运行单测/类型检查/生产
构建，Server/CLI 使用归档 Go 源码编译，无数据库或生产配置打包。

- 最终 Go build/vet/全量普通测试通过，control 为 102.063 秒，identity 为 40.230 秒。
- 最终完整 `go test -race ./... -count=1 -timeout=20m` 通过，control 为 959.544 秒、
  identity 为 90.287 秒；不是只跑定向子集。密码审计专项 race 重复三次通过。
- 新增五个 Identity 顶层测试和一个真实 HTTP 入口顶层测试；既有存储失败回归
  增加会话 IGNORE、两项审计各自 ABORT/IGNORE。覆盖原会话保持、零部分成功、
  存储恢复、取消、旧密码、12 次跨连接登录及每次恰好两项必需事件。
- 账户夹具改用通用 CreateSession 预置状态，不假装发生密码认证；真实密码会话
  仍使用 CreateLocalSession 并检查成功审计，不删除日志以满足旧计数。
- Web 180/Admin 37 项单测、类型检查与构建通过。干净产物的 Chromium 56 阶段
  真实 API 组合回归通过，320/390/768px、零 JS 错误；包含前次角色交接与冲突。
- 干净 Server 再次通过官方 Linux Tailscale 1.102.2：同名设备、在线更名、内部
  A/PTR、按新名称的 WireGuard ICMP 及重启保持。使用临时 TLS DERP/STUN 和
  userspace 客户端；不改宿主 DNS，不是全 OS/宿主系统解析器或公网数据面验收。
- 真正已发布 `bb32d65` 二进制初始化的隔离 v23 状态升级到 v24，原身份、旧
  会话、DNS 记录、设备及 IP 保持；升级后的密码登录恰好两项成功审计并经重启
  保持。旧产物拒绝 v24，配套旧完整快照隔离恢复到 v23 后原会话仍有效。
  该演练不使用生产状态，也不是上线后恢复旧快照的许可。
- 隔离验证部署校验助手：新增迁移列不会掩盖旧 IP 改变，原表缺失失败关闭，
  不覆盖冲突的不可变资产，失败不发布新首页；原子文件写入保持私有权限。
- 发布二进制版本逐字匹配完整 SHA；SHA256 为
  `9535086c92960837f92d0a6d49c86c0d9b22115a354263cf12dae7b40639586d`。
  发布包 SHA256 为 `25be23a5a7c74928795edb17a7bd1e3937db09bfa1fc956bd55a0680780ec363`。

实现字段与可复制的开发复核入口以
[服务端密码登录审计](https://github.com/xunara-net/xunara-server/blob/0ab02aac3a12c129a9eb69ce5dcbebf532fa75cf/docs/password-login-audit.md)
为准；原子成员与 DNS 的既有证据分别见
[成员权限](2026-10-11-atomic-member-updates.md)和
[DNS 名称归属](2026-10-10-dns-name-ownership.md)。

## 上线门禁与只读预检

SSH 只读确认当前二进制/页面哈希、两租户 schema、原账号/设备数量、受保护配置
与公共 Relay。保留实际 Free 自定义网段的目录覆盖，不恢复源码默认目录来覆盖
管理员配置；MagicDNS 部署域名保持实际值，不凭页面或推荐域名猜测。

新 CLI 逐租户只读名称检查通过，预检阶段仍为 v23；没有因预检改变账号/会话/
设备/网段/套餐。最终本地与对应 GitHub 竞态全部通过后，维护门禁排空旧 worker、
停控制面写入，再次复检并完整备份状态、平台库、配置、二进制和两个前端，随后升级。

完整维护备份：`/root/xunara-rollback/20261010T223344Z-password-login-audit`。
此路径为私有服务端目录，不包含在公开发布包中。

启动后的校验比较所有旧数据库表的原列内容，不能因 v24 给 nodes 增加 dns_name
就误报全部节点变了，也不能跳过旧列。核对 schema、文件哈希、租户集与公共 Relay
进程/重启计数；全部通过才恢复访问。恢复业务前失败可成套还原同一维护快照；
一旦可能恢复业务则禁止自动用旧状态覆盖，保留新状态并人工审查/前滚。

实际启动校验通过：default/team 所有原数据库表的原列内容、Noise 等状态文件、
受保护配置、账号/旧会话/设备/IP/网段/套餐与中继保持。新增 DNS 列是已验收的
迁移，不能用“原列保持”暗示新 schema 与旧完全相同。两租户各保有一名 owner，
原用户数量分别为 2/1，设备数量为 2/0；没有创建测试账号或生产设备。
实际/期望网段一致，Free 自定义网段管理员覆盖保持；MagicDNS 部署域名没有修改。

公网匿名 Chromium 逐项核对 Web 40/Admin 19 个资产哈希与干净发布包相同；
成员页与超管页分别进入正式登录入口，成员/地址/平台 API 均返回 401，匿名会话
不误判为已认证。320/390/768px 无溢出、零 JS 错误。授权平台只读契约与两个
租户 schema/分配状态再次核对通过。公共 Relay 进程、重启计数、地图和证书 pin
保持，服务器本机 TLS pin 校验后 probe 为 200；不是公网转发或双客户端数据面
实测。写入场景及官方客户端证据来自前述隔离夹具，不在生产注入故障或改角色。

## 兼容与剩余事项

本密码审计切片无新迁移、HTTP 字段或 AccountStore 签名变化；持久方法新增
成功事件的强制提交要求，故障 503 是预期收敛。官方 wire、ACL、网段、套餐和
Headscale 依赖不变。此次实际部署包含此前未上线的 DNS state v24 与成员
事务，identity v13/plans v4 不变；不是只替换一个无迁移修复。

正式 HTTPS、公网提供方、多实例/全 OS、细分角色和设备 Resource Scope、完整
注销/恢复、第三方首次建号、2FA、订阅支付和统一可靠审计仍未完成，不声称全部
产品完成。默认静态 Relay 不升级或重启，非托管公共接纳仍需独立实测。
