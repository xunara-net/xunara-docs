# 实现与审查台账

更新：2026-10-09。范围为 `xunara-net` 组织的六个现有仓库。

## 判断规则

以两份[权威规格](../../specs/)及主规范 §106–§107 为验收标准。历史 Roadmap 的
M1–M49 与新规范 Phase 0–6 不是同一套完成定义，不能从前者推导“所有功能已完成”。
本文记录本次代码/文档核对的事实，不替代规格、API 契约或安全评审。

- **已实现切片**：该边界有生产调用、错误处理和相应测试；不表示整个产品模块完成。
- **局部实现**：有底座或部分操作，仍缺完整 UI、规则或端到端验收。
- **待复核**：尚未完成详细数据流审查，不能按 README 宣传文字视为已验收。
- **未完成**：规格要求的能力尚未交付；占位页面不是功能。
- **未来阶段**：不是现阶段强制入口，不通过创建空仓库或修改客户端协议凑数。

每个功能应分别核对：数据模型、API、身份/租户权限、Entitlement、审计、错误处理、
测试、迁移、文档、官方客户端兼容、向后兼容与安全；没有修改数据库也应明确标为
“不涉及迁移”，不能省略判断。

## 当前阶段

| 阶段 | 判断 | 主要未闭环事项 |
|---|---|---|
| Phase 0 架构基础 | 局部实现 | Headscale Adapter 及数据归属与原生控制面实现存在待决策差异；统一 API 类型生成、异步任务与跨组件一致性仍需补齐 |
| Phase 1 MVP | 局部实现 | 核心注册/登录/设备/隔离/Free 配额已交付切片；完整账号生命周期与管理后台仍有缺口 |
| Phase 2 网络产品 | 局部实现 | DNS 配置写入、实时拓扑、权限矩阵、Visual Policy 与 Policy Explain 未完成 |
| Phase 3 商业化 | 未完成 | 套餐/配额不是支付系统；订阅、支付、账单及升降级工作流缺失 |
| Phase 4 高级网络 | 局部实现 | 已有底层策略/网络能力，不等于完整服务组、策略模拟与实时诊断产品 |
| Phase 5 自有客户端 | 未来阶段 | 官方 Tailscale 客户端继续是必需兼容目标，不强制自有客户端 |
| Phase 6 网络平台生态 | 未来阶段 | 独立模块/插件化推进，不混入协议或复制旧实现 |

## 功能核对

实现证据以对应仓库当前源码和测试为准，不在此复制可能漂移的接口字段。

| 模块 | 现状与证据 | 尚缺事项 |
|---|---|---|
| 组织与独立 tailnet | 已实现自助开通切片；[自助租户 ADR](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0007-self-service-tenancy.md)；各租户独立状态、网络分配与会话 | 注销/导出工作流、通知与账户生命周期 |
| 密码/邀请/注册模式 | 已实现切片，入口共享策略；本地成员注册将额度、账户、凭据、身份链接、邀请、会话和审计原子提交；[ADR-0014](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0014-browser-auth-and-member-invitations.md) | 独立租户 owner 认领、第三方/管理员其他创建点仍需复核；邮箱验证、找回、验证码及完整恢复策略未完成 |
| 账户资料与改密 | 已实现切片；[账户 ADR](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0009-account-self-service.md) | 联系邮箱仍是未验证属性，不能用来合并身份或找回密码 |
| Session | 持久会话、单个/批量撤销、事务审计；[撤销 ADR](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0010-account-session-revocation.md) | 多实例部署验收、完整设备/地点/最后活动登录记录；旧只读适配仍需逐步收敛 |
| 认证故障 | 本轮区分无效凭据与存储故障，HTTP/gRPC 失败关闭，Web 故障页保留地址与 Cookie；[ADR-0012](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0012-authentication-storage-failures.md) | 其他只读/历史登录入口的错误传播继续逐调用点复核，不能宣称全存储错误已收敛 |
| Passkey | 已实现 Web 注册/登录/删除切片；[迁移 ADR](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0011-passkey-web-and-auth-consolidation.md) | 正式 HTTPS 域名验收、凭据恢复与完整 2FA；Passkey 不等于已实现 2FA |
| OAuth/OIDC | 持久事务和提供方验证；正式 API 下浏览器入口与旧书签转接已消除 SPA 遮蔽，本地真实 RSA/JWKS/PKCE 同源浏览器验收通过；[登录代码](https://github.com/xunara-net/xunara-server/blob/main/control/login.go) | 公网提供方/固定 HTTPS 验收、第三方首次建号的配额/身份链接/审计原子性仍未闭环；夹具不等于生产第三方配置 |
| 设备与官方兼容 | 注册/审批/节点列表/路由底座与协议集成测试；[兼容 ADR](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0002-client-compatibility.md) | 全 OS/版本矩阵、持续外部双客户端验收及完整设备生命周期 |
| 套餐/Entitlement | 动态目录与资源闸门；[套餐 ADR](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0004-entitlements.md)；本轮后台补中继额度编辑 | 超额状态/提醒、所有并发创建点的原子性复核、账期/订阅事实与支付回调 |
| 网络分配 | 池分配、自定义 CIDR 校验与冲突检测；[网络 ADR](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0005-tenant-network.md) | 地址迁移对既有设备的完整工作流、保留网络运维与 Adapter 对接 |
| 成员/角色 | 成员列表、owner-only 角色编辑与邀请 Web 工作流；邀请写入事务复核会话/角色并绑定审计，旧表单共用实现；[成员页面](https://github.com/xunara-net/xunara-web/blob/main/src/views/MembersView.vue)不再提供后端未支持的 viewer 选项 | 服务端目前只有 owner/admin/member；Viewer/Network Admin、Resource Scope、角色变更的并发/审计原子性与邀请通知未完成，前端判断不代替后端授权 |
| DNS | 有客户端协议、读取与删除底座；[DNS 页面](https://github.com/xunara-net/xunara-web/blob/main/src/views/DNSView.vue) | 用户新增/编辑、解析器与 split DNS 的完整管理；不能因存在 DNS 页面认定可配置 |
| Route/Exit Node | 有通告/审批与能力闸门；本轮路由页分开记录四类读取故障并允许恢复，未知不显示为零，托管中继与 Peer Relay 数据来源已分离 | 其他页面读取故障仍需复核；路由不等于访问授权，静态中继不在托管注册列表里，心跳不代表真实数据路径 |
| 权限/ACL/Grants | 有底层解析、编译与测试；[策略引擎](https://github.com/xunara-net/xunara-server/tree/main/policy) | 统一 Visual Policy AST、七种编辑方式、矩阵、Diff/Explain/Simulator、策略版本回滚 |
| 拓扑与诊断 | 有节点视图及诊断底座 | 实时连接路径遥测与完整诊断未交付，不能把布局连线当作真实直连证据 |
| 托管中继管理 | 后端注册/心跳/期望配置/删除；本轮[超管页面](https://github.com/xunara-net/xunara-admin/blob/main/src/views/RelaysView.vue)替换路线图占位，支持筛选与一次性令牌 | 用户侧私有中继页面、分组/地图/成本、计费统计、灰度/签名自动升级与回滚 |
| 中继安全/一致性 | 准入与服务身份独立；本轮将令牌验证/配额检查/身份创建/令牌消费合并为同一事务，覆盖两个 SQLite 连接的竞争；[ADR-0013](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0013-atomic-relay-enrollment.md) | 注册审计仍在提交后执行，响应丢失的身份恢复及套餐修改竞争未闭环；心跳与其他历史读取的故障传播、租户/平台修改校验应继续对齐 |
| 超管用户管理 | 查看、会话撤销、删除与最后 owner 保护切片 | 禁用/解禁、重置密码、覆盖额度、完整账户注销、独立超管人身份与恢复/告警工作流 |
| 超管统计/套餐切换 | 本轮修复服务端字段到前端模型的映射，避免网段/额度/待审批统计丢失；修正套餐切换的请求字段，浏览器核对持久套餐结果 | 活跃用户/新增统计、真实健康/成本指标，不能填模拟数字 |
| 审计与事件 | 有账户/平台/中继操作审计与既有事件能力 | 逐操作原子性审查、统一来源、导出/筛选、可靠异步投递与告警 |
| 部署与运维 | 有同源 nginx、systemd/Compose、备份与回滚路径；[部署仓库](https://github.com/xunara-net/xunara-deploy) | 固定 HTTPS、安全多实例、可恢复演练、签名/SBOM/兼容 Release 自动化 |
| 旧扩展模块 | 服务、共享、Reach/Flux、TKA 等源码与测试仍在服务端 | 尚未本轮逐个完整复核；单测通过不替代新规格产品对等及安全验收 |

## 阅读与审查范围

本轮已建立六仓库文件清单，核对两份新规格、开发规则、各仓库 README、ADR 与手册。
重点阅读并跟踪认证存储 → 身份解析 → HTTP/gRPC 门禁 → Web 启动，以及平台中继 API
→ 注册事务/心跳契约 → 超管交互的实际数据流；核对用户设备、成员、DNS、路由、网络、
权限页面。中继写入复核包括内存实现、SQLite 即时事务、单次凭据和跨连接并发。

尚不能声称所有生产源码和历史测试都已逐行审查。旧扩展模块、存储全部写事务、设备
并发注册、权限编译器全部分支、部署全部安装路径、外部身份全回调分支仍需专项复核。
后续修改前必须继续搜索定义、调用方、测试和 upstream，不用一次清单扫描代替代码理解。

目标规格中的 Headscale Adapter 与当前原生控制面存在差异：本次不为“对齐文档”重写
协议或暗示已部署 Headscale。应单独提出架构变更 Proposal，明确兼容/迁移/数据归属后
再执行；权威规格和已接受 ADR 不因现状而改写。

## 上一轮验证：认证故障与中继管理

- 服务端：认证修复的 build、vet、test、race 已通过；后续全量竞态验证暴露旧 Webhook
  测试在发送端持久确认前断言的问题，已改为等待游标与重试状态，100 次定向 race 通过。
  认证事务过期测试改为显式持久化过期边界，100 次验证通过；CI 新增全量 race 步骤。
  中继原子注册定向 race 重复 20 次与跨连接回归通过；最新 build、vet、全量 test
  和全量 race 全部通过，不沿用旧结果冒充。
- 用户 Web：86 项单元测试通过，类型检查与生产构建通过。
- 超管：25 项测试覆盖接口契约、字段适配、套餐只读字段/完整额度、状态/筛选/限速、401/403 身份边界，类型检查和生产构建通过。
- 中继仓库：未改源码；baseline build、vet、test、race 通过。
- 浏览器管理面验收脚本保存在
  [xunara-admin/scripts/browser-smoke.cjs](https://github.com/xunara-net/xunara-admin/blob/main/scripts/browser-smoke.cjs)，
  十四阶段 Chromium 验收通过，使用隔离临时租户，页面 JS 错误为零；
  覆盖故障恢复、真实套餐切换/目录保存、中继接入/配置/配额/删除、令牌清理和移动布局，
  增加用户托管记录、四类网络读取故障及恢复、成员所有者边界、取消/失败保留原值，
  不替代真实数据面或生产多租户验收。成员角色取消/写入失败使用明确注入夹具，
  不据此宣称浏览器真实改变了后端用户角色。
- 部署 CI 修正已漂移的模板变量，单租户与多租户渲染、nginx 和 Compose 配置验证通过，
  最新 GitHub 部署 CI 通过；不改变安装器行为。认证与管理页面已在调试站升级，原有
  两租户、状态与配置保留，匿名浏览器和授权平台只读探测通过。
  最新版本、回滚快照和验证边界见[本轮验收](../deployment/2026-10-09-authentication-relay-admin.md)。
- 本轮未修改迁移或官方客户端 wire 协议；中继额度值不变，修改的是注册提交边界。
  套餐响应补充既有中继额度、编辑只提交可写字段。此前真实客户端实测见
  [上一轮记录](../deployment/2026-10-09-passkey-account-consolidation.md)，不能自动作为本轮生产部署证据。

## 本轮验证：正式认证与成员邀请

本地注册改为一个租户身份事务；通过逐个表写入故障注入、会话/审计失败回滚、
邀请重放、成员额度和两个 SQLite 连接竞争最后名额。移除旧 `createLocalAccount`、
单独 `RedeemRegistrationInvite` 和半注册成功分支；新旧邀请写操作共用 owner
会话复核与事务审计，新邀请不再生成含代码链接。普通成员管理并未变成完整 RBAC。

Web 92 项单测、类型检查与生产构建通过；超管 25 项单测与构建通过。
隔离 Chromium 脚本扩展到 23 阶段，页面 JS 错误为零，包括真实本地 OIDC 签名、
nonce、PKCE、浏览器绑定/state/事务重放、同源回跳与旧书签，以及邀请创建/兑换/
撤销/故障、Free 限制和秘密清除。没有使用虚构的 viewer 角色来声称后端支持它。
最终服务端 build、vet、全量 test 和全量 race 通过，对应 GitHub CI 全绿后部署。
运行版本为服务端 `35d291e`、用户控制台 `4f24b2e`、超管 `145806e`；原有两租户、
账户、设备、套餐、网段和受保护配置保留。公网匿名浏览器与授权平台只读探测通过，
没有修改生产密码或创建测试账号。本次协议与迁移均未修改，版本、回滚快照、
首轮测试夹具竞态的修复及验证边界见
[认证与成员邀请验收](../deployment/2026-10-09-browser-auth-member-invitations.md)，
不沿用上一轮部署证据。

补充检查发现第三方首次回调可能在自助入口建立共享成员；已按
[ADR-0015](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0015-self-service-external-admission.md)
拒绝入口未知外部身份，已有持久链接仍可登录，普通租户不变。第三方自动开独立租户
没有实现；不能把普通租户第三方登录或邮箱匹配包装成这项能力。

## 后续顺序

1. 安全/一致性：补注册审计与其他资源配额原子性，收敛历史身份查询错误传播与跨面授权校验。
2. 完整认证链路：补第三方首次建号事务、公网提供方/固定 HTTPS、多实例与恢复验收；
   先 Proposal 后实现邮箱验证、找回与 2FA，不把未验证邮箱作为身份键。
3. 前端对等：继续收敛其他页面加载错误，补 DNS 写接口/表单、用户私有中继管理及完整 RBAC。
4. 网络产品：按规格建立 Visual Policy AST/Compiler、矩阵、Explain/Diff/Simulator，
   配套权限、审计、套餐闸门和回滚；再清理已对等旧模板。
5. 商业化：订阅/账期/支付/账单/通知；不将套餐价格字段包装成已完成支付。
6. 运维交付：生产 HTTPS、数据面/多租户/全 OS 兼容矩阵、灾备、Release/SBOM/签名。
7. 自有客户端与未来生态按独立阶段推进，不把长期扩展全部塞入本次 MVP。

每项以小而可审查的提交记录实际验证结果，GitHub 使用真实组织 `xunara-net`，
保留必要兼容入口；不在根旧仓继续写新实现、不删除用户状态或历史迁移。
