# 第三方登录：OAuth2 与 OIDC

## 用户操作

正式登录页选择已启用的第三方按钮，完成授权后返回原页面。没有按钮时，网络所有者可进入「登录与注册」添加应用，平台管理员也可在后台选择租户配置；详见[管理设置](authentication-settings.md)。需要真实提供方应用，不会凭空生成可用的登录凭据。

已有密码账号，请先进入「安全中心 → 第三方账号绑定」添加登录方式，不要通过同邮箱重新建号。绑定须在同一发起浏览器会话完成；退出、切换账号或吊销原会话后重新开始。同邮箱不同账户、同 subject 不同提供方都不会自动合并。

受邀请加入：打开邀请者给出的网络注册页，输入一次性邀请码，选择第三方授权，不用另设密码。邀请码不要加入网址。授权成功提交时再次核验邀请与成员额度，第三方不能绕过套餐及 invite/closed 门禁。

解绑必须保留一种当前网络可用的登录方式。解绑撤销该第三方来源的控制台会话，不一并退出密码/其他来源会话，不删除设备、不更改 IP、角色或访问规则。登录只证明人类账户，设备仍需独立审批。

## 当前边界

- 已实现原生 OAuth2 的 GitHub.com、GitLab、自建 Gitea和严格 S256 通用适配器，与 OIDC 共用绑定、邀请、持久会话及审计。
- Google/Microsoft 等具有 OIDC 的服务沿用 ID Token 验证，不把 access token 当成 ID Token。
- 真实按钮只来自本租户已启用配置。支持页面管理应用、启停、密钥轮换与归档；应用登记和真实凭据仍由运营者/网络所有者准备，隔离测试不代表已启用公网提供方。
- LinuxDO S256 尚待核实，QQ/微信原生扫码未完成；不可关闭 PKCE 或秘密拼 URL 来换取“能登录”。可另行使用经过审核的 OIDC broker。
- 第三方直接自动创建独立租户、跨租户全局账号、邮箱验证/找回、2FA 与邮件自动投递未完成。

配置、安全约束、支持版本与验收命令以[服务端 OAuth2 手册](https://github.com/xunara-net/xunara-server/blob/main/docs/oauth2-login.md)为准，不复制接口 schema。决策见[ADR-0028](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0028-oauth2-human-login.md)，配合[账户与网络入门](account-onboarding.md)阅读。
