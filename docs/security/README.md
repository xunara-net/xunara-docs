# 安全红线

安全高于一切（规范 §111：Security > Protocol Compatibility > Data Integrity >
Architecture > Feature Completeness > Convenience）。

## 身份（规范 §5、§6）

```text
Human Identity    人类用户：会话、2FA、Passkey、OAuth/OIDC
Machine Identity  设备：MachineKey + NodeKey + Tenant
Service Identity  服务：API Key / Agent Token / Relay Token
```

- 唯一外部身份键是 `(provider_id, subject)`；Email 只是属性，不作为身份。
- 禁止 `machine_key = ? OR node_key = ?` 形式的跨租户身份混淆查询。
- 机器注册审批必须同时校验 MachineKey、NodeKey、Tenant。

## OAuth / OIDC（规范 §7）

必须校验 `state`、`nonce`、PKCE、`issuer`、`audience`、签名、`exp`/`iat`、
`redirect_uri`、JWKS 轮换、时钟偏移、code replay、state replay；Redirect URI 必须
allowlist，禁止开放重定向。

## Secret 处理（规范 §8、§87）

- 禁止把 `client_secret`、`appkey`、`access_token`、`refresh_token`、API secret 放进 URL query。
- 优先 `Authorization` 头、POST body 或安全存储；日志中不得出现 Secret。
- 部署侧统一使用 `/etc/xunara/xunarad.env`（0600）+ `*-env` 标志，避免 `ps` 泄漏。
- Relay 的一次性注册令牌只在首次注册时读取，不写入身份文件、不进日志。

## Session（规范 §9、§12）

Session 必须考虑多实例、撤销、过期、审计、轮换；**禁止**使用进程内 map 作为核心
Session 存储。控制面 Session 落状态目录，重启不掉登录，是水平扩展的前提。

用户自助退出使用仅允许人类 Session 的账户接口，写请求校验 CSRF。
单个目标必须属于本人；批量退出前在事务内重新确认发起会话仍有效，
撤销与审计同事务。失败回滚，轮换不得复活已撤销登录。“其他”保留当前登录，
“全部”包含当前登录，只影响操作时仍活动的会话，不修改机器身份或服务密钥。
接口细节与并发边界以
[服务端说明](https://github.com/xunara-net/xunara-server/blob/main/README.md#控制台登录管理)
及 [ADR-0010](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0010-account-session-revocation.md) 为准。

## 租户隔离（规范 §12、§86）

租户边界覆盖：User、Machine、Node、Device、Route、ACL、Grant、Auth Key、API Key、
DERP Policy、Service、Share、Audit。跨租户读取一律视为漏洞。

## 设备授权（规范 §10）

```text
AuthTransaction ≠ Session ≠ DeviceAuthorization
```

不得把 OAuth State、用户身份、MachineKey、Organization、设备审批塞进同一个 cache struct。

## 中继边界（补充规范 §45、§74、§75、§92）

- Relay 管理面与数据面分离；Relay 不代理业务 API，不保存核心用户数据库。
- 私有 Relay 的准入必须 fail closed（控制面不可达即拒绝放行）。
- Relay 流量统计遵循隐私最小化原则，不做 DPI（补充规范 §30、§31）。

## 审计与 Break Glass（补充规范 §87–§89）

- 所有关键操作可审计：登录、改密、2FA、设备审批/删除、路由、ACL、套餐变更、
  平台操作、Relay 变更。
- 管理员操作单独审计并标注 actor 与来源。
- Break Glass 账号用于灾难恢复，使用必须高优先级告警并事后复核。

## 部署安全

- 控制面以非特权账号运行（部署仓库 systemd 单元已强制 sandbox）。
- 平台 API/ gRPC 只监听本机或内网白名单，默认 fail closed。
- 通行密钥只在 `https://` 或 `localhost` 启用。
- 状态目录备份文件包含节点密钥与会话，按机密数据保管。

## 漏洞报告

见 [SECURITY.md](../../SECURITY.md)。
