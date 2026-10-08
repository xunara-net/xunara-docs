# 仓库规划（Repository 职责）

第一阶段真正需要的仓库（补充规范 §120）：

```text
xunara-server  xunara-web  xunara-admin  xunara-relay  xunara-deploy  xunara-docs
```

`xunara-relay` 从第一天就独立存在：即使第一版只有内置 DERP，也必须提前建立 Relay
abstraction。

## 当前仓库

| 仓库 | 语言 | 职责 | 不做什么 | 状态 |
|---|---|---|---|---|
| `xunara-server` | Go | 控制面：TS2021/Noise/DERP 准入、节点与路由、用户/组织/Session、套餐 Entitlement、网络分配、Policy Engine、审计、`/api/v1|v2`、`/api/platform/v1`、gRPC | 不含 Web UI（内嵌 console 迁移中，见 ADR-0003） | v0.1 可用 |
| `xunara-web` | Vue 3 + TS | 用户控制台：登录/注册、设备、网络、拓扑、权限、成员、DNS、路由、API Key、安全、套餐、审计、设置 | 不直连 Headscale；不做超管功能 | v0.1 |
| `xunara-admin` | Vue 3 + TS | 超管后台：平台令牌登录、租户、套餐、用户、审计、中继、系统 | 不复用用户会话；不放在用户控制台路由里 | v0.1 |
| `xunara-relay` | Go | DERP/STUN 数据面、Relay Identity/Token、托管注册与心跳、限速、健康、远程配置 | 不代理业务 API；不保存核心用户库 | v0.1 |
| `xunara-deploy` | Shell/YAML | systemd、nginx 同源站点、Docker Compose、安装与升级 | 不含业务逻辑 | v0.1 |
| `xunara-docs` | Markdown | 规格、架构、ADR 索引、API、运维、安全、手册 | 不复制会漂移的实现细节 | — |

## 依赖方向（§117–§118）

```text
web ─┐
     ├─→ server ─→ (Headscale Adapter / 官方客户端兼容层)
admin┘
relay ─→ server（注册 / 心跳 / 准入；数据面独立）
deploy ─→ server + web + admin + relay（编排，不反向依赖）
```

**不允许循环依赖**：server 不得依赖 web/admin/relay/deploy；Core 不依赖 WebUI 与
具体业务模块（依赖方向 `Platform → Core interfaces`）。

## 未来仓库（现在不建）

```text
xunara-client            自有客户端（跨平台，成熟后再拆 iOS/Android/Windows/macOS/Linux）
xunara-cli               命令行（现在由 server 仓库的 cmd/xunara 承担）
xunara-sdk               多语言 SDK
xunara-policy            Policy AST / Compiler / 模拟器（现在在 server 的 policy/ 包内）
xunara-network-tools     异地组网工具平台（§63–§66）
xunara-infrastructure    Terraform Provider / IaC（§104–§105）
xunara-community         社区
xunara-security          漏洞披露与安全公告
```

触发条件：只有当某模块**独立发布、独立版本、独立维护者**三者至少满足两条时才拆仓，
避免过早拆分成"空仓库"（补充规范 §119、§123）。

## 拆分规则

- 一个仓库 = 一个可独立构建、独立发布、独立 CI 的产物。
- 仓库之间只通过 **HTTP API / gRPC / DERP 协议** 通信，不共享代码（避免隐式耦合）。
- 前端共享的 API 类型从 OpenAPI 生成（§108–§109），不复制粘贴。
