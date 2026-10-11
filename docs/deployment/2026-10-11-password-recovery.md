# 平台辅助密码恢复：开发与 HTTPS 调试站验收

## 交付范围

平台后台「用户管理」可以核实持有人、填写原因、核对版本并生成一次性密码
重置码。登录页新增「忘记密码」及独立恢复表单，由用户输入码和新密码。
生成不更改密码或退出登录；成功兑换才替换密码、消耗码、撤销该账号全部
原浏览器会话并提交必需审计，四项动作同事务。

码只哈希落库，短期、单次、单账号 / 网络；原码仅生成响应显示一次，不进入
URL、日志或浏览器持久存储。再次生成、普通改密、账号状态变更或删除使旧码
失效。版本冲突和结果未知保留草稿，需显式核对，不能自动重试。普通租户
owner/admin、服务 API Key 和匿名无生成权限；平台使用原 Bearer 边界。

这不是按未验证邮箱找回，不给第三方专用账号新增本地密码，不自动登录，
不冻结网络、不撤销机器 / 中继或 API Key、不移除第三方 / 通行密钥绑定。
人工核实归运营者负责，勾选不等于独立超管身份验证或 MFA。

使用见[用户手册](../user/password-recovery.md)与
[平台手册](../admin/password-recovery.md)。接口、身份迁移和安全边界以
[服务端说明](https://github.com/xunara-net/xunara-server/blob/main/docs/password-recovery.md)、
[ADR-0031](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0031-platform-password-recovery.md)
和 [Deploy](https://github.com/xunara-net/xunara-deploy) 为准，不在此复制字段定义。

## 源码与上线

| 仓库 | 本轮源码 |
|---|---|
| Server | [`f53fbbb`](https://github.com/xunara-net/xunara-server/commit/f53fbbbffd2f48cdf07698c5d67b7ac32e1ccc64) |
| Web | [`78c1033`](https://github.com/xunara-net/xunara-web/commit/78c1033ad5c96e99ec954c1fe6c92ae860b7f8b1) |
| Admin | [`fd2ed0b`](https://github.com/xunara-net/xunara-admin/commit/fd2ed0b2a04527f0ac636aea7c0a42d8b9232da2) |
| Deploy 升级说明 | [`fb628ae`](https://github.com/xunara-net/xunara-deploy/commit/fb628aeeb8bf4e3c99a595b8b54b3b62ade6773b) |

对应代码 CI 通过后，2026-10-11 15:41（Asia/Shanghai）完成原自签 HTTPS 调试站
维护升级与最终复核。服务端来自干净 Git archive，完整提交写入版本；Web / Admin
来自干净提交的生产构建，公网逐项匹配 45 个 Web / 22 个 Admin 产物。TLS / CA、
服务参数、平台令牌和独立中继保持，未配置假提供方。

- 平台入口：`https://fakeop4.onbed.cn:9090/admin/users`。
- 用户入口：`https://fakeop4.onbed.cn:9090/login` → 忘记密码；也可打开
  `https://fakeop4.onbed.cn:9090/reset-password`。
- 原测试 CA：`https://fakeop4.onbed.cn:9090/.well-known/xunara-test-ca.pem`；
  仍是自签测试证书，不当作已完成正式公网证书部署。

## 公网验证与原数据

真实浏览器确认恢复能力、匿名生成拒绝、平台原因与持有人确认、取消不写入、
再次打开清空草稿及用户离页清空输入。320 / 390 / 768px 页面无整体横向溢出，
管理弹窗不超屏，JavaScript 页面错误为零。只预览 / 取消，没有生成真实账号的
重置码、兑换密码、创建人类登录或设备，业务配置变更为零。

公网以 upstream `controlhttp` 验证可信 HTTPS 控制密钥、TS2021 / Noise upgrade、
early payload 与 HTTP/2 未知节点拒绝，零设备注册。这不扩展为全 OS 或双客户端
数据面验收；恢复的真实写入由隔离 HTTPS 夹具完成。

关闭公网写入、停旧控制面并排空旧代理 worker 后保存一致性快照，再交换产物。
两个活动租户 identity v16→17，state v24 / plans v4 保持。原表原列原数据逐项
比较，包括原账号状态、密码、绑定、设备、网段 / IP、套餐、DNS、ACL、认证
配置及历史库；不会为了通过验收强制重新启用此前已禁用的账号。

公网验证后再次复核 104 张原人类身份 / 认证表和 43 个原会话，没有新增或修改
人类身份 / 认证数据；新恢复凭证表为空。原环境 / 组织 / TLS / 密封密钥与中继
进程保持。保留现有认证配置，不将旧台账里的配置状态强套到本次部署。

备份：`/root/xunara-rollback/20261011T072247Z-password-reset`。目录 0700，
快照、原代理配置、清单与报告 0600，含数据库 / 私钥 / 服务环境，不可公开。
归档内的代理配置处于维护模式，回退要同时恢复单独保存的原 `nginx.conf`。
全部旧控制面需停止，不做混版本滚动；仅未开放写入时允许成套恢复。
尝试开放公网前就禁止自动旧快照回退，防止重载结果不明时覆盖已受理的新业务。
开放业务后不能用旧快照覆盖新数据。备份保留，远程本轮暂存目录已删除；
临时 SSH / 平台凭据不进入仓库，也不进入公开报告。

## 自动验证

- 最终全量 Go build / vet / test / race 通过，竞态使用 20 分钟预算。
- 身份层验证持久跨实例、单次消费、重新生成、失效 / 过期、跨租户、并发生成 / 兑换，
  与旧密码登录 / 普通改密竞争；错误或忽略写入的密码 / 会话 / 码 / 用户 / 审计
  回滚，以及旧身份 v16 升级保留数据。
- HTTP 验证平台权限、版本 / 核实 / 原因、未知能力、请求体 / Origin / query、
  持久限流、密码策略、其他账号 Cookie 与 Service Key 不受影响、兑换不发 Session。
- Web 199 / Admin 51 单测、类型检查与生产构建通过。
- 68 阶段隔离综合浏览器回归通过，零 JavaScript 页面错误。
- 15 阶段隔离真实 HTTPS 回归通过：真实生成 / 兑换、取消、CAS、显式刷新、
  原码不入存储 / URL、生成与兑换的真实数据库审计故障、两次守护进程重启、
  旧码 / 重放拒绝、原会话失效、其他人 / 网络不受影响、旧密码拒绝、新密码正常登录。
- 部署快照校验的隔离验证允许仅追加身份迁移，保留已禁用状态并能发现意外改写；
  不将它宣称为本轮实际生产故障回退演练。

运行目录、前置条件和浏览器命令见
[Admin 验收说明](https://github.com/xunara-net/xunara-admin#浏览器集成验收)。
业务代码 CI：
[Server](https://github.com/xunara-net/xunara-server/actions/runs/38120887626)、
[Web](https://github.com/xunara-net/xunara-web/actions/runs/38120887531)、
[Admin](https://github.com/xunara-net/xunara-admin/actions/runs/38120887265)、
[Deploy](https://github.com/xunara-net/xunara-deploy/actions/runs/38120887355) 均通过。
操作手册 CI [已通过](https://github.com/xunara-net/xunara-docs/actions/runs/38121471043)，
本上线记录发布后由本仓库 CI 再次检查。

## 未完成范围

没有修改官方客户端协议、Headscale 或套餐；没有更换既有机器 / 服务身份。
这是人工辅助的本地密码恢复，不是全部账户生命周期或接管处置完成。
邮箱验证 / 投递 / 自动邮件找回、可靠恢复通知、独立超管人身份 / MFA / Break Glass、
2FA、完整登录历史、全局账户 / 注销、订阅支付、公网第三方应用与全 OS 数据面
矩阵仍需独立交付和验收，不宣布全部功能完成。
