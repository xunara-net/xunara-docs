# 用户手册

面向 Tailnet 使用者（普通账号）。控制台与 API 同源部署，登录后所有操作都在
`/dashboard` 及其子页面完成。

## 入口

```text
/login       登录（密码 / Passkey / 身份提供方）
/register    注册（需要管理员邀请码，邀请链接形如 /register?invite=…）
/setup       首次初始化管理员（仅全新部署，使用一次性令牌）
```

## 导航（规范 §8、§93）

| 页面 | 路径 | 内容 |
|---|---|---|
| 概览 | `/dashboard` | 设备在线数、网络状态、套餐余量、安全提示 |
| 我的设备 | `/devices` | 列表、状态、审批、改名、路由、删除；`/devices/:id` 详情 |
| 网络中心 | `/network` | 网段、DNS、DERP、连接方式（直连/中继） |
| 拓扑 | `/topology` | 设备连接可视化 |
| 权限 | `/permissions` | 可视化授权：拓扑图、设备对设备、拖拽连线、按用户/设备组/服务、高级模式 |
| 成员 | `/members` | 组织成员与角色 |
| DNS | `/dns` | MagicDNS、split DNS、自定义解析 |
| 路由 | `/routes` | Subnet Router / Exit Node 审批与状态 |
| API | `/api` | API Key 与预认证密钥 |
| 安全 | `/security` | 改密、2FA、Passkey、登录记录、Session 管理 |
| 套餐 | `/plan` | 当前套餐、用量、升级 |
| 审计 | `/audit` | 关键操作记录 |
| 设置 | `/settings` | 个人资料与偏好 |

## 常见任务

- **加入设备**：`tailscale up --login-server https://<控制面地址>`，然后在「我的设备」
  批准；或创建预认证密钥（一次性凭据只显示一次）。
- **连接不上**：先在「网络中心」看是否有可用 DERP；没有中继时客户端会停在
  `Starting`。详见 [排障](../troubleshooting/README.md)。
- **权限**：默认走可视化配置，所有规则最终编译为 ACL/Grants，可在预览里看到影响面。
- **套餐限制**：Free 默认 10 台设备、网段不可改；达到上限时升级套餐（错误码
  `DEVICE_LIMIT_REACHED`）。

## 账号安全

登录方式、修改密码、2FA、Passkey、登录记录与 Session 管理都在 `/security`。
发现异常登录立即撤销 Session 并修改密码。
