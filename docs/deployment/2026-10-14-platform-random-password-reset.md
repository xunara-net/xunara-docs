# 2026-10-14：超管随机临时密码恢复验收

## 状态与源码

本地验收、各源码仓库 GitHub CI 与正式站升级 / 自有隔离账号实测通过。
正式站 `/version` 为 `5e4caee`、`/health` 为 pass。此结论仅覆盖本切片，不代表整个产品开发完成。

| 仓库 | 提交 |
|---|---|
| Server | `5e4caee` |
| Web | `0656b28` |
| Admin | `e40152c` |
| Deploy | `321a8d9` |

设计和接口以[服务端手册](https://github.com/xunara-net/xunara-server/blob/main/docs/password-recovery.md)、
[Proposal](https://github.com/xunara-net/xunara-server/blob/main/docs/proposals/platform-random-password-reset.md)及
[ADR-0042](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0042-platform-random-password-reset.md)为准。

## 已验证

- Go build / vet / test 全量通过，最终 `go test -race ./... -count=1 -timeout=30m` 通过；
  Control 722.646 秒、Identity 147.527 秒。没有降低生产密码哈希强度。
- Web 445 / Admin 61 项单测与 vue-tsc / Vite 构建通过。
- 综合隔离浏览器 101 阶段、真实隔离 HTTPS 25 阶段、共享网络网页 7 阶段、
  独立平台多 Passkey 7 阶段通过，均无 JavaScript 错误。
- 真实 nginx / 安装器 18 阶段通过：根站和独立网络的改密 / 指导页可以导航，
  明文密码提交仍拒绝；本机 sh -n 通过，shellcheck 由 Deploy CI 验证。

覆盖管理员核实 / 取消 / CAS / 明确再重置、一次显示 / 复制 / 清除、旧会话即时失效、
真实审计故障全事务回滚、进程重启、首次本人改密、未知结果不自动重试以及
320 / 390 / 768px 页面。HTTP、gRPC、旧管理 / 设备审批与第三方 / Passkey 人类会话
不能绕过持久限制；跨租户同 ID、独立服务凭据和个人导出 schema v1 保持。

首次浏览器回归发现登录状态新增字段误扩散至个人导出；已将登录 / 账户 DTO
与原展示 / 导出 DTO 分开，重新执行最终全量、竞态与真实下载回归。

## 发布与数据边界

本轮发布只追加 identity v19；旧用户密码 / 原人类会话不因升级自动重置，
旧待用码作废，旧表结构保留给迁移和成套回退，不运行旧生成 / 兑换实现。
state / plans、官方 Tailscale 协议、原机器 / 服务凭据、设备 IP、TLS 和平台恢复令牌不变。

维护发布必须先停止公共入口及旧控制面、私有成套备份，比较原密码 / 活跃人类会话 /
节点身份地址 / 外部及 Passkey 绑定 / 密钥摘要，再恢复公共入口。
公共入口开始启动后不能自动覆盖旧快照；不擅自重置原生产用户。

已于 2026-10-14 09:49（Asia/Shanghai）完成正式站升级：Nginx / Control / Relay 均 active，
原有 6 个独立网络与默认网络可访问；8 个身份库（含独立平台身份）升级至 v19。
维护前后比较原账户、密码哈希、活跃人类会话、节点身份 / IP、外部 / Passkey 绑定、
服务凭据、TLS / Noise / 平台环境摘要一致。平台恢复令牌未更换，未自动重置原用户。
私有成套回退备份：`/root/xunara-rollback/random-password-20261014T014802Z`。
开放业务后不能直接恢复该旧快照覆盖新数据。

正式站仅新建自有一次性测试网络，验证随机重置 → 临时登录 → CSRF 改密 →
新密码正常登录；旧密码与原 / 临时会话确实失效，未完成本人改密时网络 API 403，
根站不接受该租户 Cookie、Free 10 设备额度保持，旧生成 / 兑换入口 410。
使用系统根验证正式 TLS，最后移除活动测试网络；归档 / 地址保留按既有产品行为执行。
没有对任何原生产账号执行密码重置。

真实公网 Chromium 390px、正常证书校验下可从「忘记密码」进入新版指导页，
无重置码输入、无横向溢出、无 JS 错误；HTTP 改密页面只返回 308 导航，不开放明文写入。

源码 CI：[Server](https://github.com/xunara-net/xunara-server/actions/runs/38496044569)、
[Web](https://github.com/xunara-net/xunara-web/actions/runs/38496044707)、
[Admin](https://github.com/xunara-net/xunara-admin/actions/runs/38496046543)、
[Deploy](https://github.com/xunara-net/xunara-deploy/actions/runs/38496047970)均通过。

## 未交付

人工核实与安全交付属于运营流程，不等同邮件通知、自动邮件恢复、完整 MFA
或全面账户接管恢复。此切片也不处理独立原生客户端的通配域名 / 证书问题。
用户操作见[忘记密码](../user/password-recovery.md)，管理员操作见
[重置手册](../admin/password-recovery.md)。
