# 架构总览

## 三层产品模型（规范 §3）

```text
Xunara SaaS            用户、组织、套餐、账单、审计、Admin
      │
      ▼
Control Plane          Tailscale 兼容控制面：TS2021、节点、路由、DNS、DERP 准入、Policy
      │
      ▼
客户端                 官方 Tailscale 客户端（兼容目标）；Xunara Client 为未来扩展
```

Xunara 不是 Headscale 的 Web UI：Headscale 只提供网络控制状态，产品层（身份、套餐、
权限可视化、审计、计费）全部属于 Xunara。

## 组件

```text
                    ┌────────────────────────────┐
  浏览器 ─────────▶ │ nginx（同源）               │
                    │  /        xunara-web       │
                    │  /admin/  xunara-admin     │
                    │  /api/…   ─┐               │
                    └────────────┼───────────────┘
                                 ▼
                    ┌────────────────────────────┐        ┌──────────────┐
   官方 Tailscale ─▶ │ xunara-server (9090)       │◀──────▶│ Headscale    │
   客户端 (TS2021)   │  TS2021/Noise/Map/DNS/TKA  │ Adapter│ Adapter/状态  │
                    │  产品 API /api/v1|v2       │        └──────────────┘
                    │  平台 API /api/platform/v1 │
                    │  gRPC 127.0.0.1:9191       │
                    └────────────────────────────┘
                          ▲                 ▲
     注册 / 心跳 / 准入   │                 │ 部署编排
                    ┌─────┴──────┐    ┌─────┴──────┐
                    │xunara-relay│    │xunara-deploy│
                    │DERP/STUN   │    │systemd/docker│
                    └────────────┘    └────────────┘
```

## 依赖方向（补充规范 §117–§118）

```text
web ─┐
     ├─→ server        admin ─→ server
     │                 relay ─→ server（只走注册/心跳/准入）
     └─→ 统一 API/Domain Layer（OpenAPI 生成类型）
deploy ─→ server + web + admin + relay
```

禁止反向依赖与循环依赖：`server` 不得引用任何前端或部署产物；`Core` 不依赖
`Platform` 与具体业务模块。

## 多租户与数据归属（规范 §5、§110）

| 数据 | 归属 | 说明 |
|---|---|---|
| 用户、组织、成员、邀请 | Xunara | 身份键 `(provider_id, subject)`，Email 只是属性 |
| 套餐、Entitlement、计费、审计 | Xunara | 商业规则只由 Xunara 判定 |
| 网段分配 | Xunara Network Allocation Service | 分配结果下发给控制面 |
| Tailnet / Node / Route / ACL / DERP 状态 | 控制面（Headscale Adapter） | 通过 Adapter 访问，不碰内部表结构 |
| Relay 身份、Token、流量统计 | Xunara + Relay | Relay 不保存核心用户数据库 |

映射关系：

```text
Xunara User → Xunara Tailnet → Headscale Namespace/User → Headscale Nodes
```

普通用户**不能直接操作 Headscale 全局对象**。

## 身份分离（规范 §5、AGENTS.md）

```text
Human Identity   登录、会话、2FA、Passkey、OAuth/OIDC
Machine Identity MachineKey + NodeKey + Tenant（设备注册与审批）
Service Identity API Key / Agent Token / Relay Token
```

禁止互推：`Google 登录 ≠ 设备可信`、`Email ≠ Machine Identity`、`NodeKey ≠ 人类用户`。

## 套餐与 Entitlement（规范 §38–§42）

套餐是**数据**不是代码：

```text
Plan { name, price, billing_cycle, max_devices, max_users,
       allow_custom_cidr, allow_exit_node, allow_subnet_router,
       allow_api, allow_acl, allow_grants, allow_custom_dns,
       max_routes, max_auth_keys, … }
```

判定一律走 Entitlement（ADR-0004），设备上限等商业规则在 Xunara 层强制执行
（例如 Free 第 11 台设备返回 `403 DEVICE_LIMIT_REACHED`），而不是交给 Headscale。

## 网络分配（规范 §17–§19、ADR-0005）

Free 用户网段由系统分配且不可修改；付费用户可自定义，但必须经过
CIDR Parser → Validator → Reserved Network Checker → Conflict Detector → Allocation
Manager → Headscale Adapter 流水线。

## 权限与 Policy（规范 §20–§30）

七种可视化配置方式（拓扑图、设备对设备、拖拽连线、按用户、按设备组、按服务、高级模式）
最终都产出同一个 **Policy AST**，经 Policy Compiler 编译为 Grants/ACL；Route 与
Permission 严格分离。

## 前端形态（规范 §93–§94）

- 用户控制台：`/login`、`/register`、`/dashboard`、`/devices`、`/network`、`/topology`、
  `/permissions`、`/members`、`/dns`、`/routes`、`/api`、`/security`、`/plan`、
  `/audit`、`/settings`。
- 超管后台：独立前端与独立入口（`/admin/`），不复用用户会话路由；平台令牌登录。

## 相关

- 仓库职责：[REPOSITORIES.md](../../REPOSITORIES.md)
- 安全红线：[docs/security/README.md](../security/README.md)
- 部署形态：[docs/deployment/README.md](../deployment/README.md)
