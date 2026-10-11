# 账号禁用与解禁：开发和 HTTPS 测试站验收

## 交付范围

平台后台「用户管理」新增状态筛选、禁用 / 解禁、管理原因、版本确认与冲突后
显式刷新。用户中心成员页只读显示禁用状态，不泄露平台原因，也不获得平台权限。
取消和预览不写入；超时、读取失败或版本变化保留草稿，不能盲目重复提交。

禁用状态、浏览器会话撤销与必需审计在同一事务提交。密码、OAuth2/OIDC、通行
密钥的新会话及 HTTP / gRPC 认证受持久状态约束；解禁需要重新登录，不恢复旧
会话。删除 / 降权也保护最后一位启用的 owner，已禁用 owner 不算恢复入口。

这是人类账号控制，**不是网络冻结**：设备、设备接入 Key、DNS、ACL、套餐与
独立中继身份不改。委托 API 权限暂停，但独立 API Key 不自动撤销；解禁后未
撤销、未过期的 key 可再使用。禁用账号仍占成员额度。未知账户仍不能绕过原有
注册策略；外部身份继续以提供方与 subject 区分，不按邮箱合并。

接口、数据库及升级 / 回滚以
[服务端手册](https://github.com/xunara-net/xunara-server/blob/main/docs/account-suspension.md)、
[ADR-0030](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0030-account-suspension.md)
与 [Deploy](https://github.com/xunara-net/xunara-deploy) 为准，不在本文复制字段定义。
普通操作说明见[管理员手册](../admin/account-suspension.md)。

## 源码和部署

| 仓库 | 本轮源码 |
|---|---|
| Server | [`76a5568`](https://github.com/xunara-net/xunara-server/commit/76a556883dc667b4819fa6c4649a882042d343c7) |
| Web | [`cc01307`](https://github.com/xunara-net/xunara-web/commit/cc01307483a57e5b546af188852e2e6fb42223b0) |
| Admin | [`0b82d4d`](https://github.com/xunara-net/xunara-admin/commit/0b82d4d8367ea290a8d09abae6003b23d0a1ef6a) |
| Deploy 升级说明 | [`062d203`](https://github.com/xunara-net/xunara-deploy/commit/062d20368585f574d5267f3a24f4c1c2d9d14ec4) |

2026-10-11 13:48（Asia/Shanghai）已升级原自签 HTTPS 测试站。服务端与前端均
由上述干净提交构建；线上 43 个 Web / 22 个 Admin 文件逐个匹配发布清单，
控制面版本与提交一致。未重启公共中继、替换 CA / TLS pin 或改动服务参数。

入口：`https://fakeop4.onbed.cn:9090/admin/users`。真实平台后台显示账号状态与
版本；禁用弹窗要求原因，明确提示不是网络冻结。320 / 390 / 768px 页面无整体
横向溢出、弹窗不超出屏幕；取消不提交，再打开不残留原因，状态筛选结果与
真实接口一致。匿名读取和状态变更被拒绝，JavaScript 页面错误为零。

公网验证**只读及预览取消**，未实际禁用既有账号，未创建人类会话、假提供方
或设备。禁用 / 解禁的真实写入、审计故障与重启恢复由下述隔离 HTTPS 夹具验证，
不在生产库注入故障。公网使用 upstream `controlhttp` 验证 HTTPS TS2021/Noise、
early payload、HTTP/2 未知节点拒绝；未注册设备，不扩大为全 OS 数据面验收。

## 维护与原数据保留

关闭公网写入、停止全部旧控制面实例、排空旧代理 worker 并保存一致性快照后
升级；前端目录在 `/srv` 同分区交换，不复用此前跨分区失败的实现。维护中先
验证数据，再恢复原代理配置和公网入口。两活动租户 identity v15→16，state
v24 / plans v4 不变，迁移只追加；旧账号均默认启用。

原数据库原表原列逐项核对，账号、凭据、绑定、设备、网段 / IP、套餐、DNS、
ACL、认证配置及历史归档保留。公网探测后再核对 32 张人类身份 / 认证表和
43 个原会话，未新增或修改人类身份 / 认证数据、未禁用任何既有账号。环境、
组织配置、TLS / 密封密钥及中继进程保持；注册策略不变，未创建假第三方应用。

备份：`/root/xunara-rollback/20261011T053129Z-account-status`。目录 0700，
快照 / 原代理配置 / 清单 / 校验报告 0600，含私钥和服务环境，不可公开。
恢复快照时须同时恢复独立保存的原 `nginx.conf`，因为归档内是维护配置。
仅仍关闭写入的窗口可成套恢复；开放业务后禁止覆盖新增数据。备份保留，
本轮远程上传暂存目录已清理，本地临时 SSH / 平台凭据不进入仓库。

## 本地验证

- 最终全量 Go build / vet / test / race 通过；竞态测试使用 20 分钟预算。
- 专项竞态重复三轮：禁用、密码发会话、删除 / 降权、最后启用 owner 与跨连接竞争。
- 旧身份库升级保留数据；禁用 / 解禁、幂等、缺失版本与 CAS 冲突、故障和忽略
  写入的回滚、重新启用后新登录、已撤销会话不恢复均有自动化验证。
- Web 196 / Admin 47 项单测、类型检查及生产构建通过。
- 68 阶段隔离综合浏览器回归通过，零 JavaScript 页面错误。
- 10 阶段隔离真实 HTTPS 回归通过：版本冲突保留原因、显式刷新核对、取消不
  写入、禁用登录 / Cookie、租户与平台边界、最后 owner、真实数据库审计故障
  回滚、守护进程重启恢复与解禁重新登录；320 / 390 / 768px 弹窗通过。
- OAuth2/OIDC 与通行密钥发行路径由本地提供方 / 身份测试覆盖，不连接公网
  IdP，不把同邮箱属性当身份，也不宣称已申请真实第三方应用。

隔离浏览器命令、运行目录和前置条件见
[Admin 验收说明](https://github.com/xunara-net/xunara-admin#浏览器集成验收)。

对应提交的 CI 已通过：
[Server](https://github.com/xunara-net/xunara-server/actions/runs/38114843098)、
[Web](https://github.com/xunara-net/xunara-web/actions/runs/38114730546)、
[Admin](https://github.com/xunara-net/xunara-admin/actions/runs/38114729263)、
[Deploy](https://github.com/xunara-net/xunara-deploy/actions/runs/38114731583)。

## 兼容和未完成边界

身份迁移追加新版本，历史用户默认启用；老版本不理解禁用状态。部署前必须停止
全部旧控制面实例，不可混版本滚动上线。完整备份应包含数据库、密封密钥、
服务环境及产物；失败回退必须成套恢复，不能只换旧二进制。开放业务写入后，
不能用旧快照覆盖新用户数据。

没有修改官方客户端协议或套餐规则，不与机器 / 中继凭据混用。已受理的请求不
被强制终止，不能把本切片宣称为所有历史业务写入均已原子授权。仍使用原平台
Bearer 权限边界，尚无独立超管人身份、强 MFA 或 Break Glass。

完整登录历史、邮件通知、邮箱验证 / 找回、2FA、全局账号与完整注销、订阅支付、
网络冻结、真实公网第三方应用及全 OS / 双客户端数据面矩阵仍是独立工作；不宣布
全部产品功能完成。
