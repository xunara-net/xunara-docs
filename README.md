# xunara-docs

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
邮箱验证、密码找回与 2FA 仍是待开发功能，不以规格规划代替当前能力。
本轮清理、浏览器与官方 Linux 客户端的实测边界见
[通行密钥迁移与账户认证收敛验收](docs/deployment/2026-10-09-passkey-account-consolidation.md)。

## 目录

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
