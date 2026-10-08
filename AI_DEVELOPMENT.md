# AI 开发规范（操作入口）

本文是《[Xunara AI 长期开发与架构规范](specs/ai-development-architecture.md)》与
《[GitHub 多仓库、中继平台与长期生态架构](specs/github-multi-repo-relay-ecosystem.md)》
的**可执行摘要**。冲突时以规格全文为准。

## 1. 项目身份

Xunara 是 Tailscale-compatible Control Plane，**不是 Headscale + UI**，也不是
MirageServer fork。第一目标是保持官方 Tailscale Client compatibility。

参考优先级：

```text
Protocol:  Tailscale upstream > Headscale upstream > Xunara > MirageServer
Product:   Xunara specification > MirageServer > Tailscale > Headscale
Identity:  MirageServer + Dex + go-oidc + oauth2 + WebAuthn > Xunara Identity
```

## 2. 工作流（禁止猜 API）

```text
定位模块 → 搜索定义 → 搜索调用链 → 查 upstream → 查测试
        → 建立数据流 → 设计最小修改 → 实现 → 测试 → 总结兼容性影响
```

修改 Tailscale/Headscale 行为前，必须先读 upstream 源码与测试，不允许凭印象写协议字段。

## 3. 每次输出必须说明（§108）

```text
修改了什么 / 为什么修改 / 涉及哪些文件 / 是否修改数据库 / 是否修改 API
是否影响官方客户端 / 是否影响套餐 / 是否影响 Headscale / 测试了什么 / 还有什么风险
```

提交信息使用中文五段式，顺序固定：

```text
type: 一句话标题

What changed
Why
Compatibility impact
Security impact
Tests
```

## 4. Definition of Done（§107）

数据模型 / API / 权限 / 套餐限制 / 审计 / 错误处理 / 测试 / Migration / 文档 /
官方客户端兼容测试 / 向后兼容检查 / 安全检查 —— 全部完成才算完成。

## 5. 架构变更必须先提 Proposal（§109）

涉及以下任一主题时，先写 Architecture Change Proposal（可放在对应仓库的
`docs/proposals/` 或 issue），不得直接改代码：

```text
Database | Authentication | Headscale Adapter | Network Allocation
Policy Engine | Official Client Compatibility | Billing | Tenant Model
```

重大决策记录为 ADR（§91）：`docs/adr/ADR-NNNN-*.md`，索引见 [adr/README.md](adr/README.md)。

## 6. 永久红线（§110）摘要

1. 产品层：UI 由 Xunara 自己提供；Xunara 是多租户 SaaS。
2. 身份：Xunara 用户身份与 Headscale 身份解耦；Human / Machine / Service 身份不互推。
3. 套餐：限制走 Entitlement，不写 `if plan == "pro"`；Free 默认 10 设备、CIDR 不可改，
   付费才可自定义 CIDR。
4. 协议：官方 Tailscale Client 必须始终可用；不为产品需求改 TS2021/Noise/MapRequest/
   MapResponse/NodeKey/MachineKey/DiscoKey/Register/Poll/DNS/DERP/Capabilities/FeatureQuery。
5. 权限：可视化配置与 Grants/ACL 共享 Policy AST，最终都经 Policy Compiler；
   Route 与 Permission 严格分离。
6. Headscale：不直接依赖其内部表结构，只经 Headscale Adapter；其升级不得导致 Core 重写。
7. 数据归属：用户/套餐/账单/审计属于 Xunara；网络控制状态属于 Headscale。
8. 可审计：所有关键操作必须可审计；所有重大架构变化必须记录 ADR。
9. 扩展：未来网络工具以独立模块接入；Client/Web/Admin 共享统一 API/Domain Layer。
10. 开发：AI 优先最小修改，禁止无必要的大规模重构。

第 11–25 条原文见规范 §110，不得删改。

## 7. 优先级（§111）

```text
Security > Protocol Compatibility > Data Integrity > Architecture
        > Feature Completeness > Convenience
```

## 8. 引用 MirageServer 的边界（§14）

允许参考：第三方登录、Dex/OIDC、OAuth、Aggregator、微信扫码、Device Authorization、
Organization/User、Machine、Funnel/Share。

禁止未经审查直接复制：`stateCodeCache`、`controlCodeCache`、`mirage-authstate2`、
`miragecontrol`、Email identity、server-local session cache、旧 Machine lookup。

## 9. 任务与分支

- 一个任务一个分支，命名 `feat/…`、`fix/…`、`docs/…`、`chore/…`，默认分支 `main`。
- PR 必须说明五段式内容；CI 全绿才可合并（§52–§70）。
- 跨仓库改动先提 issue 说明依赖顺序，避免循环依赖（§117–§118）。

## 10. 测试要求

```sh
# Go 仓库
go build ./... && go vet ./... && go test ./... -count=1
# 并发 / Session / Identity / Control Plane
go test -race ./...
# 前端仓库
npx vue-tsc --noEmit && npx vitest run && npx vite build
# 部署仓库
sh -n install.sh && shellcheck install.sh && nginx -t -c nginx/xunara.conf
```

协议相关修改必须补 compatibility / integration 测试（§68–§70）。
