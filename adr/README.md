# ADR 索引（Architecture Decision Record）

规则（规范 §91、§110）：

- 每个重大架构变化必须记录 ADR；只做决策记录，不写成教程。
- ADR 一旦 Accepted 不再改写结论；推翻时新增一条 ADR 并标注 `Supersedes`。
- 正文放在**做出决策的仓库**的 `docs/adr/` 下，本文件只做索引与状态。

## 状态定义

```text
Proposed → Accepted → （Deprecated | Superseded by ADR-NNNN）
```

## 索引

| ADR | 标题 | 仓库 | 状态 | 日期 |
|---|---|---|---|---|
| [ADR-0001](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0001-multi-repo.md) | 采用 GitHub Organization 多仓库治理 | xunara-server | Accepted | 2026-10-09 |
| [ADR-0002](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0002-client-compatibility.md) | 官方 Tailscale 客户端兼容是不可修改的红线 | xunara-server | Accepted | 2026-10-09 |
| [ADR-0003](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0003-server-web-split.md) | 服务端与 Web UI 分离（内嵌 console 迁移中） | xunara-server | Accepted（迁移中） | 2026-10-09 |
| [ADR-0004](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0004-entitlements.md) | 套餐能力通过 Entitlement 强制，而不是散落的 if | xunara-server | Accepted | 2026-10-09 |
| [ADR-0005](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0005-tenant-network.md) | 租户网段由 Network Allocation Service 分配 | xunara-server | Accepted | 2026-10-09 |

## 模板

```markdown
# ADR-NNNN：<决策标题>

- 状态：Proposed | Accepted | Deprecated | Superseded by ADR-NNNN
- 日期：YYYY-MM-DD
- 决策者：

## 背景
（问题、约束、现状）

## 决策
（选择了什么，边界在哪里）

## 备选方案
（被否决的方案与原因）

## 影响
（兼容性 / 安全 / 数据 / 运维 / 迁移）

## 后续
（需要跟进的工作）
```

## 待补 ADR（候选）

- Relay 托管注册与心跳的服务端契约落地（`/api/relay/v1/*`）。
- 前端 API 类型从 OpenAPI 生成（web/admin/client 共享 Domain Layer）。
- 内嵌 console 删除与服务端只提供 API 的最终形态（ADR-0003 的收尾）。
