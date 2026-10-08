# 客户端

## 官方 Tailscale 客户端（当前唯一必需入口）

Xunara 的控制面按官方协议实现，客户端**不需要**改配置模板：

```sh
tailscale up --login-server https://<控制面地址>
```

注册流程：客户端发起 TS2021（`/ts2021`）→ Noise 握手 → `Register` → 控制台批准设备 →
`MapRequest`/`MapResponse` 下发 netmap 与 DERP map。官方客户端始终可用是永久红线
（规范 §57–§59、ADR-0002）。

## 兼容性检查清单

- TS2021 升级路径与 HTTP/2（含 WASM 客户端的 WebSocket 升级）可用。
- Noise 会话内的 `Register`、`MapRequest`、`MapResponse`、`set-dns`、`feature/query`、
  `audit-log`、`update-health`、`whoami`、TKA 系列路径与 upstream 一致。
- DERP map 中的自签名中继通过 `CertName` 指纹固定，客户端可正常连接。
- 控制面 `MinSupportedCapabilityVersion` 拒绝过旧客户端时返回明确状态而不是静默失败。

## Xunara Client（未来扩展，现在不是依赖）

自有客户端是未来能力，不得成为现阶段强制入口（规范 §60–§62、§102–§104）。规划中的
位置：

```text
xunara-client  跨平台客户端（成熟后再按平台拆分仓库）
```

自有客户端可以提供的额外能力：更简单的登录、图形化网络诊断、权限编辑、服务发现入口。
它与 web/admin 共享同一 API/Domain Layer。

## Agent（原生设备）

`xunara-agent` 是控制面自带的最小原生客户端/联调工具：用预认证密钥注册，然后
`run` 维持连接。密钥放环境变量，不放命令行。
