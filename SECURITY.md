# 安全策略

## 支持范围

安全修复只针对最近一个发布版本的主要分支（`main`）与最新 Release。旧版本请先升级。

## 报告漏洞

请通过 GitHub Security Advisory（仓库 → Security → Report a vulnerability）私下报告，
或邮件联系组织管理员。**不要**在公开 issue 中提交：

- 可复现的利用步骤、PoC 与影响面细节
- 任何 Secret、Token、私钥、证书、真实账号
- 用户数据（节点密钥、登录记录、审计内容）

我们会在 72 小时内确认收到，并在评估后给出修复计划与致谢方式。

## 部署方须知

- 平台 API（`/api/platform`、gRPC `xunara.v2.Platform*`）默认 fail closed：未配
  `XUNARA_PLATFORM_ADMIN_TOKEN` 一律拒绝；配置后只允许内网/白名单访问。
- 控制面必须运行在非特权账号下（部署仓库的 systemd 单元已强制）。
- `-server-url` 必须是浏览器实际访问的地址，否则会话 Cookie 与 OIDC 回调会错位。
- 通行密钥（WebAuthn）只在 `https://` 或 `localhost` 下启用，不要用 IP 部署。

详见 [docs/security/README.md](docs/security/README.md)。
