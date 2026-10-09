# API 概览

服务端 API 由 `xunara-server` 提供，前端与客户端都只经 API 访问控制面，不直连数据库。

## 分组

| 前缀 | 认证 | 用途 |
|---|---|---|
| `/api/v1/*` | 会话 Cookie / API Key（账户自助仅人类 Session） | 用户控制台：概览、账户、设备、路由、用户、DNS、策略、预认证密钥、API Key、Session、审计 |
| `/api/v2/*` | 会话 Cookie / API Key | 产品能力：meta、organization、TKA、DERP、policy、security、exit-nodes、relays、serve、devices、machines、services、flux、reach、audit、agent-tokens、webhooks、shares |
| `/api/platform/v1/*` | `XUNARA_PLATFORM_ADMIN_TOKEN`（Bearer） | 平台管理：organizations、plans、audit、跨租户用户管理 |
| `/api/agent/v1/*` | Agent Token | 原生客户端协议 |
| gRPC `xunara.v2.PlatformService` / `PlatformAdminService` | 前者为租户 Session/API Key 的 Bearer；后者为平台令牌 | 默认监听内网，身份与权限分别验证，fail closed |
| `/key`、`/ts2021`、`/machine/*`（Noise 内） | 无需会话（协议自证） | 官方 Tailscale 客户端接入 |

## 认证方式

```text
用户控制台   同源会话 Cookie（HttpOnly + SameSite=Lax）→ 必须由 nginx 同源部署
自动化/工具  Authorization: Bearer <API key>（scope 限定）
平台管理     Authorization: Bearer <XUNARA_PLATFORM_ADMIN_TOKEN>
中继注册     一次性 Relay Token（首次注册）→ Relay Identity（长期）
```

Secret 规则：不放 URL query、不放命令行、不进日志（规范 §8、§87）。

## 版本与兼容（规范 §96、§97、§110）

- URL 版本化：破坏性变更走新前缀（`/api/v3`），旧版本保留迁移窗口。
- `Capability API` 暴露服务端能力位，前端不得靠版本号猜功能。
- 官方客户端协议字段（MapRequest/MapResponse/NodeKey/…）不得为了产品需求改动。
- OpenAPI 生成类型与共享 Domain Layer 是目标；当前 web/admin 采用按端点手写适配与契约测试，尚未实现生成链路。

## 错误约定

- HTTP 状态码表达类别：`400` 参数、`401` 未认证、`403` 权限/套餐受限、`404`、`409` 冲突、`429` 限速、`5xx` 服务端。
- 套餐受限返回可识别的错误码（如 `DEVICE_LIMIT_REACHED`），前端据此展示升级引导。
- 错误响应不包含 Secret、密钥、内部路径与租户边界之外的信息。
- 身份存储不可用返回可重试错误，不伪装成未登录：HTTP 503、gRPC Unavailable；
  前端不因此清理有效凭据。详见 [ADR-0012](../../adr/README.md)。

## 契约位置

- 服务端路由与处理：`xunara-server/control/`（`api.go`、`api_v2.go`、`platform*.go`、`api_auth.go`、`api_account.go`）。
- gRPC/HTTP 定义：`xunara-server/api/proto/xunara/v2/platform.proto`（生成物在 `api/gen/`）。
- 中继注册协议：`xunara-relay/docs/relay-protocol.md`。
