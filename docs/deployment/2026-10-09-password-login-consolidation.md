# 密码登录故障与旧业务收敛验收（2026-10-09）

状态：已完成本切片验收。最终本地验证、发布产物浏览器回归和对应 GitHub CI
通过后完成可回滚升级，公网匿名浏览器与授权平台只读探测均通过。

已部署版本：服务端
[`0be7330`](https://github.com/xunara-net/xunara-server/commit/0be7330)。用户控制台
[`4f24b2e`](https://github.com/xunara-net/xunara-web/commit/4f24b2e)、超管
[`145806e`](https://github.com/xunara-net/xunara-admin/commit/145806e)源码和静态产物未改，
部署说明仍为 [`09a03f4`](https://github.com/xunara-net/xunara-deploy/commit/09a03f4)。
前一轮认证与邀请的实际升级见[上一轮记录](2026-10-09-browser-auth-member-invitations.md)。
任务记录见[服务端 issue #2](https://github.com/xunara-net/xunara-server/issues/2)。

## What changed

- 正式 JSON 与兼容 HTML 密码入口共用持久限流、身份/凭据读取、bcrypt、事务型
  本地会话签发及既有审计调用，不再保留两份独立密码业务代码。
- 增加带 context、保留错误结果的登录名、凭据和本地凭据数量读取。旧布尔/数量
  方法仅薄适配同一 SQL，未删除尚有调用方的兼容接口。
- 限流、密码登录的初始化状态、身份或会话存储故障统一中止认证，返回脱敏的
  不可用响应与重试提示，不签发或清理 Cookie，不引导用户重新初始化。
- 身份缺失与错误密码仍统一拒绝，保留 HTML 表单 CSRF、成功回跳与 API 会话载荷；
  慢哈希后仍在事务内复核密码，防止并发改密后的旧密码签发新登录。
- 增加中文边界注释与真实数据库回归，先复现故障再修复。实现以
  [共用密码服务](https://github.com/xunara-net/xunara-server/blob/main/control/password_login.go)和
  [ADR-0016](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0016-password-login-consolidation.md)为准。

## Why

继续逐调用点审查发现：两种密码入口在限流数据库错误后继续验证；身份布尔查询
把存储故障解释为错误密码；初始化计数可能将故障伪装成未初始化。正式 SPA 不再
使用旧表单并不能消除旧入口旁路，需要收敛业务而不是只隐藏页面。

真实 SQLite 故障回归在修改前分别复现错误的成功 200、未认证 401、未初始化 409
和会话写失败 500。按
[Proposal](https://github.com/xunara-net/xunara-server/blob/main/docs/proposals/2026-10-09-password-login-failure-consolidation.md)
延续 ADR-0012 的失败关闭决策，并新增 ADR-0016；不改写已接受的历史结论。

## Compatibility impact

- 不修改表结构、已发布迁移、套餐额度、机器身份、Headscale 或官方 Tailscale wire
  协议；没有新增公开 API 路径或成功载荷字段，内部 Store 追加类型化读取。
- 原 Cookie、IP/登录名预算、大小写处理及实际 bcrypt 成本不变。已确认错误凭据
  仍返回相同拒绝；存储故障改为 503，调用方不能再据此判定错误密码或需要初始化。
- 旧入口保留为兼容薄适配，只有重复的密码业务被删除。其他尚未对等的旧功能
  和客户端授权页面不为清理而删除，机器审批仍独立于人类登录。

## Security impact

- 限流插入/更新、账户/凭据读取或会话写入失败都不能获得新登录，响应不暴露密码、
  会话令牌或数据库诊断，旧 Cookie 不被删除或替换。
- 两种入口共享原预算，切换 JSON/HTML 或登录名大小写不能获得新预算。进入共用
  路径前已取消的请求不写限流或会话；查询取消仍保留底层 context 错误链。
- 未知用户和无本地密码继续完成原 dummy bcrypt 工作量；不降低哈希成本、不用
  内存限流或会话表、不在后台任务启动后替换存储指针来制造测试故障。
- 成功登录审计仍在会话提交后执行，尚未与会话原子绑定。启动初始化、其他旧
  元数据读取/写入、第三方首次建号和完整账号恢复仍须继续复核，不将本切片视为
  全部认证路径已原子化或已失败关闭。

## Tests

- 最终代码 `go build ./...`、`go vet ./...`、`go test ./... -count=1` 和
  `go test -race ./... -count=1 -timeout=20m` 全部通过。
- 身份查询与密码故障/恢复专项 race 重复 20 次，共享预算 race 重复 5 次通过。
  覆盖无记录、扫描失败、关闭数据库、取消 context、限流插入/更新失败、身份与
  会话故障、零新会话/原会话不撤销、秘密脱敏和故障恢复后的真实成功登录。
- Web 92 项、Admin 25 项单元测试、类型检查及生产构建重新通过，前端静态入口
  校验和与上一轮一致，不因服务端修复虚构前端版本升级。
- 最终发布二进制上的
  [23 阶段 Chromium 脚本](https://github.com/xunara-net/xunara-admin/blob/main/scripts/browser-smoke.cjs)
  回归通过，页面 JavaScript 错误为零，包括本地 OIDC、邀请和原有控制台管理工作流。
  密码数据库故障由上述真实 Go/SQLite 用例验证，不把浏览器代理故障当成数据库证据。
- [对应 GitHub CI](https://github.com/xunara-net/xunara-server/actions/runs/37939090420)
  的 build、vet、普通测试及全量 race 全部通过后才升级。没有沿用前一服务端
  提交的全绿结果；托管竞态运行时间较长，但在既有硬预算内完成，未跳过用例。

## 调试部署与回滚

部署前核对已运行的前一版本、前端入口、归档路径及所有产物校验和，停止控制面后
备份一致状态。快照为 `/root/xunara-rollback/20261009T140033Z-password-login-consolidation`，
目录仅 root 可读，状态归档按机密保存；失败回滚仅恢复二进制和静态入口，不擅自
覆盖用户状态。真实 HTTP 进程和服务路径下二进制均确认新版，不使用历史别名判断。

原有 `default` 与 `team`、账户、设备、网段和套餐保留；组织配置、环境文件、服务
单元、nginx、公共中继 map 及证书指纹哈希不变，控制面、中继和 nginx 均 active。
没有在生产注入故障、重置用户密码或创建测试账号/中继记录。

公网匿名 Chromium 确认用户/超管页面要求登录、原访问目标保留、390px 无整体
横向溢出和零 JavaScript 错误，三个受保护账户/平台 API 均返回 401。
授权平台只读探测确认新版、两租户、统计和套餐契约，托管注册中继仍为零；
静态公共中继不属于此列表，不能将零注册数解释为没有中继。凭据仅在远端内存中
用于请求头，上传的本轮临时发布文件随后按精确路径清理，用户状态和回滚快照保留。

仍为 HTTP 调试部署，未配置公网提供方或启用通行密钥；没有重复执行外部客户端
数据面。本地真实 OIDC 夹具、Go 兼容回归、匿名探测不等于生产 HTTPS、公网 OIDC、
真实生产用户操作或完整全 OS 验收，上一轮客户端实测也不作为本次新部署证据。

## 仍需完成

HTTP 调试不是正式 HTTPS。公网 OIDC、邮箱验证/找回/2FA、多实例、完整 RBAC、
DNS 写入、Visual Policy、订阅/支付/账单、灾备和全 OS 官方客户端兼容矩阵仍未
全部交付。后续顺序及源码审查范围见[实现台账](../developer/implementation-status.md)。
