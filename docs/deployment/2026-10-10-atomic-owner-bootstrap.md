# 一次性初始化、owner 开通与登录配置恢复验收（2026-10-10）

状态：已完成本切片验收。最终本地验证、发布产物及对应 GitHub CI 全部通过后，
完成维护窗口升级；公网匿名浏览器与授权平台只读验收通过。

发布源码：服务端
[`65cba43`](https://github.com/xunara-net/xunara-server/commit/65cba43)、用户控制台
[`514467c`](https://github.com/xunara-net/xunara-web/commit/514467c)、超管验收脚本
[`5feaf54`](https://github.com/xunara-net/xunara-admin/commit/5feaf54)、部署说明
[`15c0536`](https://github.com/xunara-net/xunara-deploy/commit/15c0536)。
任务见[服务端 issue #3](https://github.com/xunara-net/xunara-server/issues/3)，前一部署见
[密码登录验收](2026-10-09-password-login-consolidation.md)。

## What changed

- 初始化与自助开独立租户共用一次性身份事务：认领内置 owner、写入资料/密码、
  会话、完成事实及必需成功审计；删除旧分步认领和重复的会话/审计业务。
- 启动、公开认证元数据、JSON/HTML 门禁和成员邀请使用同一带 context 的类型化
  初始化状态。状态、证明或限流读取/写入故障失败关闭，不假报尚未初始化。
- 初始化证明完整原子发布为 `0600`，并发启动采用同一证明；异常文件不静默替换。
  成功后文件只是清理，残留证明、删除密码或重启不会重新开放初始化。
- 自助开通失败在组织成功退出后释放套餐和网络分配，取消请求使用有界清理；
  补偿失败明确记录，不把多个平台数据库包装成一个全局事务。
- 用户登录页校验实际登录策略、提供方地址和自助端点。读取失败或畸形载荷时不
  启用入口，保留访问目标并提供重试；增加中文边界注释和浏览器恢复验收。

具体实现见
[身份事务](https://github.com/xunara-net/xunara-server/blob/65cba43/identity/sqlite_bootstrap.go)、
[初始化流程](https://github.com/xunara-net/xunara-server/blob/65cba43/control/setup.go)、
[登录页](https://github.com/xunara-net/xunara-web/blob/514467c/src/views/LoginView.vue)及
[ADR-0017](https://github.com/xunara-net/xunara-server/blob/65cba43/docs/adr/ADR-0017-atomic-owner-bootstrap.md)。

## Why

真实 SQLite 故障在修改前复现：初始化限流失败仍成功、状态读取故障被当作未
初始化、凭据/会话写入失败留下部分身份、审计失败仍完成。文件删除不能承担
数据库的唯一开通边界，分步写入也不能防止两个实例覆盖同一个 owner。

本轮按
[Proposal](https://github.com/xunara-net/xunara-server/blob/65cba43/docs/proposals/2026-10-09-atomic-owner-bootstrap.md)
延续已有认证失败关闭决策，不为页面便利降低安全规则，不改写已接受的历史 ADR。

## Compatibility impact

- **追加身份迁移 v13**，旧迁移 1–12 不变；根据已有本地凭据或明确的初始化/owner
  注册审计回填完成事实，不修改旧用户、密码、外部身份链接、会话或机器归属。
- 公开路径和成功载荷不变，正常注册模式、Cookie 和限流预算不变。故障改为明确
  不可用响应，调用方不能把 503 当成未初始化、错误令牌或无邀请权限。
- 不改官方 Tailscale wire 协议、机器身份、设备审批、Headscale、套餐额度；Free
  仍默认 10 台设备、一名成员，自动网段规则不变，不另建第二个 owner。
- 旧版本拒绝 v13 数据库；跨版本回退需要升级前的**完整一致性状态与旧产物**，
  必须在恢复公网写流量前完成。仅回退二进制无效，恢复公网后不覆盖旧快照。
- 初始占位用户播种仍是既有流程；旧 v1 迁移测试改用真实已发布 DDL，修复的是
  缺少审计表的简化测试模型，不修改已发布迁移或生产数据库以绕过问题。

## Security impact

- 事务先获取唯一开通名额，再复核/更新内置 owner；任何身份写点、最后审计或
  提交失败均不返回部分身份或新 Cookie，仍可恢复后重试。重复开通不改密码/资料。
- 保留 `(provider_id, subject)` 的既有链接，Email 仍只是属性，不把人类登录与
  机器信任、服务密钥或设备审批合并。数据库完成事实不等于完整账号恢复机制。
- 存储故障不撤销原会话、不清理 Cookie、不输出原始诊断或秘密；限流失败不能
  绕过开通预算，取消请求不开始身份写入。慢哈希不降成本，事务内不做慢哈希。
- 生产只读验收不注入故障、不重置密码或创建测试账号。平台令牌仅在远端内存中
  用于请求头，备份状态及节点密钥按机密保管，不进入公开报告或命令行。
- 成功密码登录审计、第三方首次建号、初始播种、跨库可靠补偿及响应丢失恢复仍
  未闭环；这次修复不是全部认证已原子化、已失败关闭或全项目完成的声明。

## Tests

下列 Go 命令在 `xunara-server` 仓库执行，前端测试与构建分别在 `xunara-web` 和
`xunara-admin` 执行；浏览器流程的准备命令以超管仓库 README 为准。

- 最终服务端 `go build ./...`、`go vet ./...`、`go test ./... -count=1` 和
  `go test -race ./... -count=1 -timeout=20m` 全部通过；owner/初始化、失败开通与
  迁移专项 race 重复 20 次通过，不跳过用例或降低真实 bcrypt 成本。
- 真实存储回归覆盖各身份写点/最终审计回滚、限流插入/更新失败、数据库扫描/关闭、
  取消请求、两个 SQLite 连接及两个 HTTP 实例竞争、密码删除后不重开、残留证明
  重放、重启、损坏/链接/权限错误证明、零部分身份及原 Cookie 保留和恢复成功。
- Web 106 项、Admin 25 项单元测试通过；两端类型检查与生产构建通过。登录配置
  校验拒绝未知策略和不安全地址，浏览器覆盖 503、畸形 200、恢复后正常登录。
- 最终发布二进制的
  [25 阶段 Chromium 回归](https://github.com/xunara-net/xunara-admin/blob/5feaf54/scripts/browser-smoke.cjs)
  通过、JS 错误为零，包含 owner 唯一认领、旧证明重放以及此前真实本地 RSA/JWKS/
  nonce/PKCE/OIDC、邀请、额度、中继和移动布局。全部在隔离临时状态执行。
- 真实上一版 `0be7330` 二进制初始化的隔离状态验证 v12 → v13：身份、密码及
  原会话保留；再同时恢复原二进制与一致性 v12 状态，原会话仍可登录。这是
  隔离回退演练，不是已经执行生产回退或完整灾备验收。
- 对应提交的 GitHub CI 全部通过：
  [服务端](https://github.com/xunara-net/xunara-server/actions/runs/37956978874)、
  [Web](https://github.com/xunara-net/xunara-web/actions/runs/37956979759)、
  [Admin](https://github.com/xunara-net/xunara-admin/actions/runs/37956981806)、
  [部署](https://github.com/xunara-net/xunara-deploy/actions/runs/37956983467)。服务端包含
  完整 race；部署 CI 覆盖 shellcheck、单/多租户 systemd 渲染、nginx 与 Compose。
  本机未安装 shellcheck，不将 CI 的验证写成本机执行结果。

## 调试部署与回退

最终 Linux/amd64 二进制 SHA-256：
`152302e4b0fff7b8c130f14689c72e5a2d038441afbe1f5fda3db22076288f23`。
产物从干净提交构建，前端逐文件校验；部署前核对线上旧二进制和静态入口。
临时维护拒绝只施加于 Xunara 公网入口，不停止中继或整台 nginx；确认旧 nginx
工作进程退出且控制面停止后，保存完整一致性状态，包含平台状态和归档租户。
备份为 `/root/xunara-rollback/20261009T162251Z-atomic-owner-bootstrap`，目录 `0700`、
状态归档 `0600`。路径时间使用 UTC，本文日期使用 Asia/Shanghai；快照按机密保管。

`default` 与 `team` 的身份 schema 均从 v12 升为 v13，完成事实回填符合原凭据/
审计；原用户、密码、外部身份链接、设备数量、域名、套餐和网段保持。组织配置、
环境文件、服务单元、nginx 原配置和公共中继 map 哈希未变，中继指纹未改变。
确认上述事实和本机匿名 API 门禁后恢复公网；控制面、中继、nginx 均 active。

失败回退仅在维护边界内启用：保留失败的新状态，再同时恢复原产物与完整旧状态。
恢复公网业务后不自动覆盖旧快照；本次升级成功，**未执行生产回退**。
不能将隔离恢复演练包装成生产回退或完整灾备已完成。

公网 HTTP `/version` 确认 `65cba43`。匿名 Chromium 确认用户/超管要求登录、
访问目标保留、390px 无整体横向溢出、零 JS 错误；账户会话、成员邀请和平台中继
三个受保护 API 均返回 401。授权平台只读探测核对新版、两租户、套餐及统计契约；
注册托管中继仍为零，静态公共 DERP 不属于此列表，不能据此判定没有可用中继。
没有修改生产密码、创建测试账号/中继或注入数据库故障，维护升级以外不改用户状态。
本轮上传的四个临时文件按精确路径删除，回滚快照保留并复核私有权限；完成后关闭
本地 SSH 复用连接。不清理用户状态或历史归档，也不保留持久的远程管理连接。

## 仍需完成

HTTP 调试不是正式 HTTPS；未配置公网 OIDC、生产 Passkey 或本次新的外部客户端
数据面验收。前一轮官方客户端实测不是本次新部署证据，本地 OIDC 夹具也不是公网
第三方配置。完整认证恢复、邮箱验证/找回/2FA、安全多实例、RBAC、DNS 写入、
Visual Policy、订阅/支付/账单、灾备与全 OS 兼容矩阵仍未全部交付。
按风险排序的后续与真实源码审查范围见[实现台账](../developer/implementation-status.md)。
