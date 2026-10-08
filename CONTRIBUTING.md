# 贡献指南

## 分支与提交

- 默认分支 `main`，禁止直接 push（需要评审时用 PR；仓库保护见补充规范 §58–§59）。
- 分支命名：`feat/<scope>`、`fix/<scope>`、`docs/<scope>`、`chore/<scope>`。
- 一个 PR 只做一件事；跨仓库改动在描述里写清依赖顺序与合并顺序。

提交信息固定为中文五段式：

```text
<type>: <一句话标题>

What changed
- …

Why
- …

Compatibility impact
- 是否影响官方 Tailscale 客户端 / Headscale / 套餐 / API

Security impact
- 身份、Secret、Session、租户隔离、审计的影响

Tests
- 实际执行的命令与结果
```

## 代码要求

- Go：`gofmt`，`go build ./... && go vet ./... && go test ./... -count=1`；并发、
  Session、Identity、控制面改动必须 `go test -race ./...`。
- 前端：`npx vue-tsc --noEmit && npx vitest run && npx vite build`。
- 部署：`sh -n`、`shellcheck`、`nginx -t`、`docker compose config`。
- 修改协议相关代码（TS2021/Noise/MapRequest/MapResponse/NodeKey/MachineKey/DiscoKey/
  Register/Poll/DNS/DERP/Capabilities/FeatureQuery）必须先读 upstream，并补兼容性测试。

## 评审要求

- 安全 > 协议兼容 > 数据完整性 > 架构 > 功能完整 > 便利性。违反优先级顺序的 PR
  一律要求返工。
- 不允许引入 `if plan == "pro"` 形式的套餐判断，必须走 Entitlement。
- 不允许把 Secret 放进 URL query、命令行参数或日志。
- 不允许新增 server-local session map 作为 Session 存储。
- 数据库迁移只能追加，已发布条目不可修改。

## ADR 与 Proposal

- 涉及 Database / Authentication / Headscale Adapter / Network Allocation / Policy
  Engine / Official Client Compatibility / Billing / Tenant Model 的改动，先提
  Architecture Change Proposal。
- 决策落地后写 ADR 到对应仓库 `docs/adr/`，并在本仓库 [adr/README.md](adr/README.md)
  登记。

## 版本与发布（补充规范 §52–§56、§54）

- 各仓库独立 SemVer；`xunara-server` 与 `xunara-relay` 之间维护兼容矩阵
  （见 [docs/developer/README.md](docs/developer/README.md)）。
- Release 必须包含：变更摘要、兼容性说明、镜像 tag、升级/回滚步骤。
- 容器镜像发布到 GHCR：`ghcr.io/xunara-net/<repo>:<version>`，多架构 amd64/arm64。
- 产物需附 SBOM，依赖升级由 Dependabot / Renovate 跟踪。

## 安全

漏洞请按 [SECURITY.md](SECURITY.md) 私下报告，不要在公开 issue 里贴利用细节或 Secret。
