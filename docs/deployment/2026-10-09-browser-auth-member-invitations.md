# 正式认证入口与成员邀请验收（2026-10-09）

已部署版本：服务端
[`35d291e`](https://github.com/xunara-net/xunara-server/commit/35d291e)，用户控制台
[`4f24b2e`](https://github.com/xunara-net/xunara-web/commit/4f24b2e)，超管
[`145806e`](https://github.com/xunara-net/xunara-admin/commit/145806e)。部署说明更新为
[`09a03f4`](https://github.com/xunara-net/xunara-deploy/commit/09a03f4)，未修改安装器或
正在运行的中继程序。跨仓库任务见
[服务端 issue #1](https://github.com/xunara-net/xunara-server/issues/1)。

## What changed

- 第三方登录改从 API 路径启动，避免正式 SPA 遮蔽旧浏览器起始请求。保留旧书签的
  薄转接，使用同一持久认证事务、浏览器绑定、回调和安全回跳校验。
- 本地成员注册在一个租户身份事务内核验邀请、角色和成员额度，并提交账户、密码、
  外部身份链接、邀请消费、会话及审计；任一步失败全部回滚。删除旧分步账户创建、
  独立兑换写接口和半注册成功分支，不保留两套业务实现。
- 成员页提供所有者专用邀请面板：创建、单次代码展示、记录读取、确认撤销、明确
  失败及重试。旧表单复用相同写服务，不再生成含邀请码的链接。移除前端后端并不
  支持的 viewer 选项，未借此宣称完整 RBAC 已实现。
- 自助开独立网络的入口拒绝未知第三方身份隐式加入共享网络；已有持久身份链接
  仍可登录。外部身份只按提供方和 subject 识别，不按相同邮箱认领所有者。
- 新的权限、事务、错误和安全边界增加中文注释。具体 API 与数据定义以
  [服务端说明](https://github.com/xunara-net/xunara-server/blob/main/README.md)和
  [用户控制台实现](https://github.com/xunara-net/xunara-web/tree/main/src)为准。

## Why

单有后端登录和邀请接口并不意味着正式控制台可用：SPA 路由曾遮蔽认证入口，分步
注册不能原子约束成员数量。修复围绕真实浏览器流程、并发一致性和租户边界展开，
避免用 UI 隐藏入口代替后端授权，也不为清理旧实现破坏已有登录或设备授权目标。

涉及认证和身份事务前先提出
[认证与邀请 Proposal](https://github.com/xunara-net/xunara-server/blob/main/docs/proposals/2026-10-09-browser-auth-and-member-invitations.md)，
并记录 [ADR-0014](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0014-browser-auth-and-member-invitations.md)。
入口租户门禁另有
[Proposal](https://github.com/xunara-net/xunara-server/blob/main/docs/proposals/2026-10-09-self-service-external-admission.md)
与 [ADR-0015](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0015-self-service-external-admission.md)，
不改写已有 Accepted ADR 的结论。

## Compatibility impact

- 不修改数据库结构或已发布迁移，不修改官方 Tailscale wire 协议、机器身份、设备
  审批、路由、DNS 或 DERP 数据面；未引入 Headscale 或迁移原有控制状态。
- 产品 API 新增正式浏览器认证起始入口和成员邀请管理；提供方响应引用新起始入口，
  旧登录书签仍复用同一流程。本地注册既有成功响应保持，失败不再留下孤立账户。
- 套餐数值不变，配额从 Entitlement 获取，Free 单成员限制仍在后端执行。普通
  invite 租户才允许新建邀请；自助入口不提供共享成员邀请，普通租户第三方策略未变。
- 人类登录不等于机器可信，成员邀请不批准设备，也不授予 owner。

## Security impact

- 创建和撤销邀请需要有效 owner 人类 Session、CSRF，并在写事务内复核会话和角色；
  API Key、普通成员和 admin 角色不能管理邀请。邀请与审计原子提交。
- 明文邀请码只在创建响应和弹窗中展示一次，关闭时清理，不写 URL、持久浏览器
  存储或日志。列表不返回明文或哈希，已消费和撤销记录保留。
- 新旧认证入口共享持久限流，存储故障失败关闭。提供方原始错误不写日志；严格
  校验本站回跳，拒绝外部地址、反斜杠及控制字符。
- 自助入口未知外部身份回调返回拒绝，不写账户、身份链接或会话；相同邮箱不会
  自动合并所有者。第三方自动开独立租户尚未实现，不能绕过本地自助开通流程。
- 普通租户的第三方首次建号、角色变更、其他资源注册审计及所有并发写入边界仍需
  专项闭环，本次没有把所有历史创建点包装为已原子化。

## Tests

- 在最终服务端版本执行 `go build ./...`、`go vet ./...`、`go test ./... -count=1`、
  `go test -race ./... -count=1 -timeout=20m`，全部通过；
  [对应 GitHub CI](https://github.com/xunara-net/xunara-server/actions/runs/37934213152)
  的构建、vet、普通测试及全量 race 均通过后才部署。
- 注册事务逐表写故障、会话和审计失败回滚、邀请到期/重放/撤销、最后成员名额、
  两个 SQLite 连接的竞争，以及入口旧/新 OIDC 回调和已链接身份回归均通过。
  身份事务、HTTP 门禁和入口专项 race 分别重复 20 次通过。
- 首轮 race 发现测试夹具在启动后台任务后直接替换存储指针造成竞争，已改为真实
  SQLite 故障注入，不修改生产同步语义、不跳过用例；修复后重跑最终全量验证。
- 用户控制台 92 项、超管 25 项单元测试、类型检查和生产构建通过。中继源码未改，
  不沿用旧中继验证冒充本轮改动证据。
- [可复现浏览器脚本](https://github.com/xunara-net/xunara-admin/blob/main/scripts/browser-smoke.cjs)
  在最终发布二进制与前端产物上完成 23 阶段隔离 Chromium 验收，页面 JavaScript
  错误为零：真实本地 OIDC RSA/JWKS/PKCE、签名和 nonce 拒绝、浏览器绑定与 state
  重放、产品及设备授权回跳、旧书签、同邮箱身份分离、邀请创建/兑换/撤销与错误恢复、
  Free 配额、跨角色门禁、一次性秘密清理和移动布局。
- 本地发行方夹具有固定回调与一次性授权码，不替代公网提供方配置、真实用户设备
  授权或全 OS 兼容矩阵；本轮未重新执行外部官方客户端的数据面测试。

## 调试部署与回滚

部署前核对现存运行版本、前端入口、归档路径及每个产物的校验和。停止控制面后
备份一致状态，原子替换二进制，先安装哈希静态资源再切换入口，启动后检查实际
HTTP 进程版本，而不是用另一个路径下的历史二进制代替运行版本。

快照保存在 `/root/xunara-rollback/20261009T131457Z-browser-auth-member-invitations`，
目录仅 root 可读，状态归档按机密保存；失败回滚恢复旧二进制与页面入口，不擅自
覆盖用户状态。升级保留 `default` 与 `team`、原有账户、设备、网段和套餐，组织
配置、环境文件、服务单元、nginx、公共中继 map 和证书指纹的哈希均未改变。

控制面、中继与 nginx 均为 active。公网匿名浏览器验证用户与超管页面要求登录、
保留用户原访问目标、移动端无整体横向溢出，三个受保护账户/平台 API 均返回 401，
JavaScript 错误为零。持部署凭据的平台只读探测确认两租户和统计契约正确，托管
注册中继仍为零；静态公共中继不属于该列表，不将零注册数解释为没有中继。
凭据只在远端内存用于请求头，未修改用户密码或创建生产测试账号/中继记录。

本次部署仍为 HTTP 调试站，尚未配置公网第三方提供方，未启用通行密钥。匿名
验收不替代真实生产用户点击；固定 HTTPS、公网 OIDC 与多实例仍须单独配置验收。

## 未完成事项

完整 DNS 写入、私有中继用户页面、Viewer/Network Admin 与 Resource Scope、
Visual Policy、邮箱验证/找回/2FA、订阅/支付/账单、独立超管人身份、HTTPS、灾备及
全 OS 官方客户端矩阵均未全部交付。Headscale Adapter 与现有原生控制面的差异
仍需要独立架构决策，不能因当前实现而修改权威规格或静默迁移用户设备。
后续顺序与审查范围见[实现与审查台账](../developer/implementation-status.md)。
