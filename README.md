# xunara-docs

超管改为直接重置随机临时密码，用户首次登录必须本人改密；旧码流程不再混用。
源码、最终回归、正式升级与自有隔离账号实测见
[随机密码恢复验收](docs/deployment/2026-10-14-platform-random-password-reset.md)。

免费开户网页改用可选的主域名独立网络路径；新增多 IPv4 地址池和 Linux 接入前
只读冲突保护。测试证据、非 VLAN / Quad100 自动换址 / 独立客户端 DNS/TLS 边界见
[注册与网络安全验收](docs/deployment/2026-10-13-shared-console-network-safety.md)。

设备「有效期设置」已上线：定时/指定时间、永不过期、立即过期和30分钟临时
续期，当前节点密钥与 Token TTL 分离。Go 全量 race、435 项 Web 单测与100阶段
最终隔离浏览器及安全发布见[最新有效期验收](docs/deployment/2026-10-13-device-expiry-settings.md)。

添加设备进一步简化为单一复制：显式选 Token 才直接带密钥，高级参数折叠，
删除旧隐藏输入与设备脚本分支。最终 402 项 Web / 96 阶段手机、剪贴板回归及
正式站只更新前端的证据见[简洁接入验收](docs/deployment/2026-10-12-simplified-device-enrollment.md)。

设备立即过期与 Token 接入已上线，主域改用正式受信任证书；原账户、会话、
设备与默认 Relay 保持。部署提交、最终 CI、95 阶段浏览器及系统根/官方 Noise
验证见[设备接入与证书验收](docs/deployment/2026-10-12-device-enrollment-production-tls.md)。
单域证书不覆盖其他租户，自动续期尚未配置。

同端口 HTTP 页面安全导航与 HTTPS 正式入口共用，未知 Host、明文 API/回调/凭据
明确拒绝；前端升级默认保留原 TLS。16 阶段隔离测试、原站 44 个 HTTP 探测、
四档匿名手机布局、上游 Noise 与全部原凭据保留见
[HTTP/HTTPS 共用入口验收](docs/deployment/2026-10-11-http-https-entry.md)。不新增明文登录。

Xunara 玄序的**文档中心**：规范、架构、ADR、API、运维、安全与用户手册。代码在各自的
仓库里，本仓库不承载业务代码，也**不复制**会在别处变化的接口细节——只做权威入口与
长期规格存放地。

## 仓库地图

| 仓库 | 职责 | 状态 |
|---|---|---|
| [xunara-server](https://github.com/xunara-net/xunara-server) | Tailscale 兼容控制面 + 产品 API（用户/组织/套餐/审计），不含 Web UI | v0.1 |
| [xunara-web](https://github.com/xunara-net/xunara-web) | 用户控制台（Vue 3 + TS） | v0.1 |
| [xunara-admin](https://github.com/xunara-net/xunara-admin) | 超级管理员后台（Vue 3 + TS） | v0.1 |
| [xunara-relay](https://github.com/xunara-net/xunara-relay) | DERP/STUN 中继与托管注册协议 | v0.1 |
| [xunara-deploy](https://github.com/xunara-net/xunara-deploy) | systemd / nginx / Docker Compose 部署 | v0.1 |
| [xunara-docs](https://github.com/xunara-net/xunara-docs) | 本仓库：规范与文档 | — |

完整规划（含未来 `xunara-client`、`xunara-cli`、`xunara-sdk`、`xunara-policy`、
`xunara-network-tools`、`xunara-infrastructure`）见 [REPOSITORIES.md](REPOSITORIES.md)。

## 先读什么

1. [AI_DEVELOPMENT.md](AI_DEVELOPMENT.md) — AI/人类开发者的操作入口：工作流、输出格式、
   Definition of Done、永久红线。**改代码前必读。**
2. [specs/ai-development-architecture.md](specs/ai-development-architecture.md) — 《Xunara AI
   长期开发与架构规范》全文（§1–§112）：产品模型、用户中心、套餐、权限、Admin、API。
3. [specs/github-multi-repo-relay-ecosystem.md](specs/github-multi-repo-relay-ecosystem.md) —
   《GitHub 多仓库、中继平台与长期生态架构》全文（§1–§125）：仓库边界、Relay 平台、
   CI/CD、发布与兼容矩阵。
4. [docs/architecture/README.md](docs/architecture/README.md) — 架构总览（三层模型、多租户、
   依赖方向、数据归属）。
5. [CONTRIBUTING.md](CONTRIBUTING.md) — 分支、提交信息、发布与版本兼容。

账户资料、改密、批量退出与通行密钥的已实现边界见 [用户手册](docs/user/README.md#账号安全)
和 [ADR 索引](adr/README.md)（ADR-0009、ADR-0010、ADR-0011）。
本人成功登录记录、首次来源 / 客户端线索、最近活动与手机卡片见
[登录记录手册](docs/user/login-history.md)和 ADR-0032；不包含失败尝试或地理定位。
现已随 identity v18 上线原自签 HTTPS 调试站；源码、真实旧版升级 / 成套回退、
公网只读验证与原会话保留见[登录记录验收](docs/deployment/2026-10-11-login-history.md)。
个人设置的本人安全资料 JSON / 成功登录记录 CSV 使用与隐私边界见
[个人导出手册](docs/user/account-export.md)，不代表整个网络或全部个人数据导出。
现已无新迁移升级原自签 HTTPS 调试站；源码、真实附件回归、原会话 / 历史保留
与公网只读证据见[个人导出验收](docs/deployment/2026-10-11-account-export.md)。
超管随机临时密码恢复与本人首次强制改密见[用户手册](docs/user/password-recovery.md)与
[管理员手册](docs/admin/password-recovery.md)。邮箱验证、自动邮件找回与 2FA 仍是
待开发功能，不以规格规划代替当前能力。
旧重置码流程已由 ADR-0042 替代，原 v17 发布记录留作历史证据：
[旧密码恢复验收](docs/deployment/2026-10-11-password-recovery.md)。
MagicDNS 首次启用、第三方绑定/解绑与 OIDC 邀请加入见
[账户与网络入门](docs/user/account-onboarding.md)；未配置真实提供方时不宣称生产第三方登录可用。
原生 OAuth2（GitHub/GitLab/Gitea/通用 S256）与 OIDC 共用的绑定、邀请和解绑见
[第三方登录](docs/user/third-party-login.md)；不代表公网应用已经配置。
成员邀请码与 OAuth2/OIDC 现在可在用户中心和超管后台管理，无需编辑部署文件；
入口、权限、公开开户与邀请的区别见[登录与注册设置](docs/user/authentication-settings.md)。
平台账号禁用 / 解禁及最后启用 owner 的保护见[账号禁用手册](docs/admin/account-suspension.md)；
解禁要求重新登录，在线设备和独立中继不因人类账号状态而被停用。
账号状态切片 identity v16、隔离真实写入与原站只读上线的事实见
[账号状态验收](docs/deployment/2026-10-11-account-suspension.md)。
实际 HTTPS 测试站升级、完整回退及数据保留见
[登录配置验收](docs/deployment/2026-10-11-authentication-settings.md)。
本轮清理、浏览器与官方 Linux 客户端的实测边界见
[通行密钥迁移与账户认证收敛验收](docs/deployment/2026-10-09-passkey-account-consolidation.md)。

[平台添加用户与多通行密钥手册](docs/admin/platform-administrator.md)记录成员创建与管理员安全入口，
不把单一运营者身份包装成多管理员 RBAC。

当前能力、真实缺口、源码审查范围与按风险排序的后续工作统一记录在
[实现与审查台账](docs/developer/implementation-status.md)。历史里程碑、页面路由或
接口存在不代表新规格的全部功能完成；手册中的目标模型应与台账一并阅读。
本轮代码梳理、认证故障、中继后台与原子注册的已实现边界、验证和调试部署见
[认证与中继审查验收](docs/deployment/2026-10-09-authentication-relay-admin.md)。
最新正式认证入口、原子成员邀请、自助入口租户门禁及可回滚调试部署见
[认证与成员邀请验收](docs/deployment/2026-10-09-browser-auth-member-invitations.md)。
密码登录失败关闭、旧业务收敛及本轮验证状态见
[密码登录验收](docs/deployment/2026-10-09-password-login-consolidation.md)。
最新初始化、独立租户 owner 原子开通、登录配置故障恢复与身份 v13 升级边界见
[一次性初始化验收](docs/deployment/2026-10-10-atomic-owner-bootstrap.md)。

访问权限优先：图形规则、策略关系图、权限矩阵、组、模拟解释、预览发布与版本恢复的
使用步骤见[网络控制台手册](docs/user/network-console.md)；DNS、私有中继和手机侧栏
与之一起交付，实施边界仍以台账和服务端测试为准，不表示全部商业化功能完成。
本轮验证、state v19→21 与维护回退边界见[网络控制台验收](docs/deployment/2026-10-10-network-console.md)。
中继的配置冲突保护、历史恢复与不可逆撤销见
[网络控制台手册](docs/user/network-console.md#配置与恢复)与 [ADR-0020](adr/README.md)。
本切片的提交、最终回归和维护升级状态见
[中继配置验收](docs/deployment/2026-10-10-relay-configuration-history.md)。
远程配置真实执行、持久服务回执及新进程失败关闭见
[ADR-0021](adr/README.md)与[中继运行时验收](docs/deployment/2026-10-10-relay-runtime-execution.md)。
执行报告不是端到端连接证明，也不代表方向/租户/用户限速已经实现。

地址管理、默认中继首屏、非托管/官方地图草稿导入与七平台预编译下载见
[网络控制台手册](docs/user/network-console.md)、[ADR-0022](adr/README.md)和
[本切片验收](docs/deployment/2026-10-10-addresses-and-external-relays.md)。
自定义合法 IPv4 已放开 CGNAT-only 和 /16～/28 人工限制；默认 CGNAT 与安全检查
保持，非标准范围不作为全平台官方客户端兼容承诺。范围策略变更见
[ADR-0023](adr/README.md)，规格只追加补充，不改写历史正文。
本轮官方 Linux 私网 ICMP/显式 IP 更新、51 阶段浏览器与调试站部署事实见
[合法 IPv4 范围验收](docs/deployment/2026-10-10-flexible-ipv4.md)。

DNS 注册/更名与自定义记录的事务型名称归属及升级前只读检查见
[服务端操作与隔离验收](https://github.com/xunara-net/xunara-server/blob/main/docs/dns-name-ownership.md)
和 [ADR-0024](adr/README.md)。两台同名新设备分配稳定别名，旧碰撞不静默更名；
Linux 内部 A/PTR 查询实测不代表全 OS 或宿主 DNS 接管；原开发验收当时未升级，见
[DNS 名称归属开发验收](docs/deployment/2026-10-10-dns-name-ownership.md)。

成员编辑现在使用版本确认和事务型权限/审计，过期页面不会自动覆盖；CLI 与
兼容表单共用不变量，最后 owner 的降权/删除竞争受保护。操作与边界见
[服务端成员管理](https://github.com/xunara-net/xunara-server/blob/main/docs/member-management.md)、
[ADR-0025](adr/README.md)和
[成员权限开发验收](docs/deployment/2026-10-11-atomic-member-updates.md)。仍只有三个
现有角色，不把 Viewer/Network Admin 占位当作实现；该记录保留原开发时未上线边界。

密码登录已补会话与两项成功审计的原子提交，删除控制层重复日志；原会话在故障
时保持。本次连同 DNS 名称归属与成员保护完成调试站维护升级。干净产物、只读
v23→24 预检、实际上线状态和剩余认证边界见
[密码审计与累计升级验收](docs/deployment/2026-10-11-password-login-audit.md)。

MagicDNS 首次启用、账户级 OIDC 绑定/解绑与第三方邀请入网已完成本轮切片和
调试站 identity v13→14 维护升级，原网段/账号/设备保持。61 阶段浏览器、官方
Linux 客户端、完整竞态与回退边界见
[账户入网与 MagicDNS 验收](docs/deployment/2026-10-11-account-onboarding-magicdns.md)。
真实公网 OIDC 仍需配置发行方与固定 HTTPS，不将隔离夹具当成生产开通。

## 目录

设备列表/详情有效期设置、短期设备 Token 与显式含 Token 的简短命令见
[用户手册](docs/user/network-console.md#设备接入与中继诊断)、
[服务端契约](https://github.com/xunara-net/xunara-server/blob/main/docs/device-enrollment.md)
及 [ADR-0038](adr/README.md)。原子额度/消费、真实 SDK Noise、95 阶段浏览器和
平台现场边界在[实施状态](docs/developer/implementation-status.md#2026-10-12设备过期与-token-接入切片)记录；
最终上线与证书范围见[设备接入验收](docs/deployment/2026-10-12-device-enrollment-production-tls.md)。

单设备「有效期设置」支持定时/指定时间、关闭过期、立即过期与已过期设备
30 分钟临时续期，见[用户手册](docs/user/network-console.md#设备接入与中继诊断)
及 [ADR-0039](adr/README.md)。不改变网络默认认证周期，接口/时间边界以
[服务端契约](https://github.com/xunara-net/xunara-server/blob/main/docs/device-enrollment.md)为准。
最新版本、事务/手机回归与安全上线见[有效期设置验收](docs/deployment/2026-10-13-device-expiry-settings.md)。

直接路由审批、冲突草稿、客户端本地出口说明和真实状态见
[用户手册](docs/user/network-console.md#路由与出口)及
[服务端契约](https://github.com/xunara-net/xunara-server/blob/main/docs/route-management.md)。
最终源码/CI、90 阶段隔离验证和原账号/会话/中继保留的正式调试升级见
[路由与出口验收](docs/deployment/2026-10-12-route-management.md)。

设备/私有中继参数化安装、分层健康与核心导航见
[用户手册](docs/user/network-console.md#设备接入与中继诊断)及 [ADR-0035/0036](adr/README.md)。
安装前置条件以 [relay 手册](https://github.com/xunara-net/xunara-relay/blob/main/docs/private-relay-install.md)为准。
源码、安装器产物、83 场景及调试站状态保持见
[2026-10-12 核心设备验收](docs/deployment/2026-10-12-device-core.md)。

```text
specs/          规格全文（长期规范、补充规范、PROJECT_SPEC、身份登录、Roadmap、参考来源）
adr/            架构决策索引（正文随各仓库 docs/adr/ 维护）
docs/user/      用户手册（控制台、设备、网络、权限）
docs/admin/     超管手册（用户、套餐、租户、中继、审计、Break Glass）
docs/developer/ 开发者指南（仓库边界、依赖方向、测试、Releases）
docs/api/       API 概览与版本策略
docs/deployment/部署（systemd / Docker / nginx 同源）
docs/relay/     中继平台规格与运维
docs/client/    客户端（官方客户端兼容 + 未来 Xunara Client）
docs/security/  安全红线（身份、Secret、Session、租户隔离、审计）
docs/architecture/ 架构总览
docs/operations/   运维（备份、灾备、灰度、监控、告警）
docs/troubleshooting/ 排障手册
```

## 规格文档的来源

`specs/` 下的文件是**权威规格**，只允许追加与勘误，不允许为了配合实现而改写：

| 文件 | 来源 |
|---|---|
| `ai-development-architecture.md` | 用户提供的《Xunara AI 长期开发与架构规范》 |
| `github-multi-repo-relay-ecosystem.md` | 用户提供的《Xunara AI 开发规范补充》 |
| `project-spec.md` | 原主仓库 `Xunara_AI_Development_Docs_2026-10-05/PROJECT_SPEC.md` |
| `identity-login.md` | 原主仓库 `IDENTITY_LOGIN.md` |
| `reference-sources.md` | 原主仓库 `REFERENCE_SOURCES.md` |
| `roadmap.md` | 原主仓库 `ROADMAP.md` |

实现与规格冲突时：**以规格为准**，并提 Architecture Change Proposal（见
[AI_DEVELOPMENT.md](AI_DEVELOPMENT.md)），而不是让代码悄悄定义标准。

## 相关仓库

- 控制面：[xunara-server](https://github.com/xunara-net/xunara-server)
- 前端：[xunara-web](https://github.com/xunara-net/xunara-web) · [xunara-admin](https://github.com/xunara-net/xunara-admin)
- 中继：[xunara-relay](https://github.com/xunara-net/xunara-relay)
- 部署：[xunara-deploy](https://github.com/xunara-net/xunara-deploy)
