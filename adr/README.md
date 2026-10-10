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
| [ADR-0006](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0006-relay-platform.md) | 中继平台的服务端实现（注册 / 心跳 / 配额） | xunara-server | Accepted | 2026-10-09 |
| [ADR-0007](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0007-self-service-tenancy.md) | 自助注册即开租户（托管部署的账户模型） | xunara-server | Accepted | 2026-10-09 |
| [ADR-0008](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0008-managed-relay-admission.md) | 托管租户的公共中继配置与准入 | xunara-server | Accepted | 2026-10-09 |
| [ADR-0009](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0009-account-self-service.md) | 账户自助资料、事务型改密与全部会话撤销 | xunara-server | Accepted | 2026-10-09 |
| [ADR-0010](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0010-account-session-revocation.md) | 用户自助会话管理与事务型批量退出 | xunara-server | Accepted | 2026-10-09 |
| [ADR-0011](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0011-passkey-web-and-auth-consolidation.md) | 通行密钥迁移到独立 Web 与账户认证收敛 | xunara-server | Accepted | 2026-10-09 |
| [ADR-0012](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0012-authentication-storage-failures.md) | 认证存储故障与无效身份分离 | xunara-server | Accepted | 2026-10-09 |
| [ADR-0013](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0013-atomic-relay-enrollment.md) | 中继注册的原子配额与凭据交换 | xunara-server | Accepted | 2026-10-09 |
| [ADR-0014](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0014-browser-auth-and-member-invitations.md) | 正式浏览器认证入口与原子成员邀请 | xunara-server | Accepted | 2026-10-09 |
| [ADR-0015](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0015-self-service-external-admission.md) | 自助入口禁止第三方隐式加入共享网络 | xunara-server | Accepted | 2026-10-09 |
| [ADR-0016](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0016-password-login-consolidation.md) | 密码登录共用业务路径与失败关闭 | xunara-server | Accepted | 2026-10-09 |
| [ADR-0017](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0017-atomic-owner-bootstrap.md) | 本地 owner 的一次性原子初始化 | xunara-server | Accepted | 2026-10-09 |
| [ADR-0018](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0018-network-console.md) | 持久网络配置与统一可视化策略 | xunara-server | Accepted | 2026-10-10 |
| [ADR-0019](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0019-managed-relay-map.md) | 租户私有中继地图与官方 TLS pin | xunara-server | Accepted | 2026-10-10 |
| [ADR-0020](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0020-relay-configuration-history.md) | 中继配置版本保护、事务历史与恢复 | xunara-server | Accepted | 2026-10-10 |
| [ADR-0021](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0021-relay-runtime-execution.md) | 中继运行时执行与服务身份回执 | xunara-server | Accepted | 2026-10-10 |
| [ADR-0022](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0022-address-management-and-external-relays.md) | 持久地址管理、非托管中继与预编译下载 | xunara-server | Accepted（强制 CGNAT 范围部分由 ADR-0023 替代） | 2026-10-10 |
| [ADR-0023](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0023-flexible-ipv4-allocation.md) | 合法 IPv4 自定义范围与官方兼容范围分离 | xunara-server | Accepted | 2026-10-10 |
| [ADR-0024](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0024-dns-name-ownership.md) | 设备、服务与记录的事务型 DNS 名称归属 | xunara-server | Accepted | 2026-10-10 |

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

- 前端 API 类型从 OpenAPI 生成（web/admin/client 共享 Domain Layer）。
- 内嵌 console 删除与服务端只提供 API 的最终形态（ADR-0003 的收尾）。
