# 中继运行时与持久服务回执验收（2026-10-10）

状态：源码已提交，完整本地回归、干净发布产物浏览器与隔离升级/恢复通过。
Server/Relay/Web/Admin CI 全部通过，文档检查通过。调试站部署因 SSH 接入异常暂缓，
未执行维护切换、迁移或产物替换；公网页面仍运行旧版 `6809d4c`，不能写成新版已上线。
任务：[Relay issue #1](https://github.com/xunara-net/xunara-relay/issues/1)。
决策：[ADR-0021](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0021-relay-runtime-execution.md)。

源码：Server [`aa459c8`](https://github.com/xunara-net/xunara-server/commit/aa459c8)、
Relay [`9ab1afe`](https://github.com/xunara-net/xunara-relay/commit/9ab1afe)、
Web [`281f6ad`](https://github.com/xunara-net/xunara-web/commit/281f6ad)、
Admin [`473c058`](https://github.com/xunara-net/xunara-admin/commit/473c058)。

## 实现边界

- 远程配置不再是日志回调：在 Core 接口上执行限速热更、维护拒新、停用断连/恢复
  和不可逆撤销。保持官方 DERP Handler/准入；不更换节点 key、TLS pin 或地区 ID。
- 修复大包只预约一个 burst 却整包发送的漏计，读按实际字节计费；热更取消旧等待、
  完整分段计费并遵守读写 deadline。0 恢复启动本地基准，-1 不限速，正值覆盖。
- 新托管进程先拒绝 DERP；缓存绑定服务身份/控制面/凭据摘要/DERP 公钥，仅作高水位
  与撤销保护。重启必须重新授权并执行，不把缓存当作本进程成功。失败重试相同配置。
- 运行中短暂控制面故障保持已确认配置和既有连接；终态 401/403 停数据面、停止
  心跳并保存撤销。磁盘故障不能抵消停用指令；不记录服务端原始错误体。
- 遥测采用上游 DERP 计数，不伪造 TCP/HTTP 客户端、连接质量或计费账本。
- state 只追加 v22（报告/接收时间），identity v13 不变。心跳按 token hash 在事务
  里复核本租户身份与撤销，报告/遥测/变化审计一起提交；失败零部分状态。存储故障
  503，不伪装成凭据失效。旧 Relay 省略报告仍兼容，但清为执行未知。
- 用户与平台后台分开展示期望版本和服务报告，显示实际速率/状态、失败原因、
  上次成功版本、等待应用和过期回执。保存不显示为已执行；撤销没有停机 ACK。

协议字段以 [Relay 契约](https://github.com/xunara-net/xunara-relay/blob/main/docs/relay-protocol.md)
为准。未修改 Tailscale wire、套餐额度、Headscale 或静态公共 Relay 的配置/TLS pin。
当前每连接共用双向桶，不冒充规格要求的方向/全局/地区/租户/用户/设备额度。

## 验证入口

前置：Go/Node 版本以各仓库模块和 CI 为准；六仓库同级，前端已安装锁文件依赖。

```bash
# 在 xunara-server 与 xunara-relay 中分别执行
go build ./... && go vet ./... && go test ./... -count=1
go test -race ./... -count=1 -timeout=20m

# 在 xunara-web 与 xunara-admin 中分别执行
npm ci && npm run test && npm run build

# 在 xunara-docs 中执行
python3 .github/check_links.py
```

- Relay：大包完整读写计费、热更取消旧等待、deadline、基准恢复、并发关闭、缓存
  损坏/身份错配/重启、磁盘及执行失败重试、终态错误和敏感错误体脱敏。
- 官方客户端：严格自签 TLS pin 的 derphttp 真实转发；既有连接热更限速、维护保留/
  拒新、停用断连/恢复、撤销。另有真实心跳 + Manager + 缓存 + 数据面的组合测试，
  控制面故障时既有连接保留，真实计数与执行回执一致。
- 服务端：两种存储一致、v21→v22 旧身份保留/报告未知、重启持久化、必需字段/
  非法版本、取消、跨租户拒绝、两个 SQLite 连接撤销竞争、审计/通知故障全回滚。
- Web 156 / Admin 36 项测试和生产构建已通过；新增报告字段契约、失败、等待、
  旧回执与禁止虚构成功。浏览器脚本新增服务自报 UI 阶段，明确不当作真实数据面证据。

两仓库 build/vet/全量 test/全量 race 全部通过。干净提交构建的发布产物下，
40 阶段 Chromium 回归通过、零 JS 错误。首轮浏览器暴露旧验收文案断言未随
“配置→期望”更新，修正后重新跑完整脚本，不隐藏失败或复用上一轮结果。
运行时/限速及心跳/回执/跨连接撤销专项 race 各重复 20 次通过。

对应 CI：[Server](https://github.com/xunara-net/xunara-server/actions/runs/38019640718)、
[Relay](https://github.com/xunara-net/xunara-relay/actions/runs/38019643522)、
[Web](https://github.com/xunara-net/xunara-web/actions/runs/38019656328)、
[Admin](https://github.com/xunara-net/xunara-admin/actions/runs/38019657984)。

已发布 `6809d4c` 真实二进制初始化的隔离状态通过 v21→v22，原账户/会话/凭据/
DNS/中继/配置历史保留；旧客户端心跳继续可用，新增回执重启保留，旧二进制拒绝
v22。恢复配套旧产物及完整旧状态后 v21 可正常访问。不表示生产回退已执行。

## 发布与运维

先升级服务端，再升级两个后台与托管 Relay。旧服务端拒绝 v22；维护窗口中一致备份
平台根、所有活动/归档租户、受保护配置及匹配产物。回退需成套旧状态/旧二进制，
恢复业务写入后禁止覆盖旧快照。中继高水位若高于恢复的控制面版本，需一致性恢复
或经审查重新签发服务身份，不能删除缓存绕过撤销保护。

本轮不通过在生产创建测试账号、中继或修改密码来验收。线上静态公共 Relay 不迁入
托管、不重启，不变更端口/key/pin；没有托管服务就如实显示为空，不制造在线报告。
本轮 SSH 初始只读检查确认旧服务仍运行，随后接入返回验证成功/连接关闭或拒绝认证，
无法建立可靠发布会话，已请求确认接入规则。产物准备和隔离验收不等于线上已替换。
待恢复接入后，在上述 CI 全绿产物上重新复查旧版/哈希，执行完整维护备份、v22 迁移
和公网匿名浏览器/授权平台只读验收，再单独记录上线结果；不能直接跳过发布前置检查。

## 尚缺事项

方向/多维度带宽策略、公共跨租户发布、计费/成本、签名升级与灰度、全 OS 外部
实测、完整多实例与灾备仍未完成；本切片不是整个商业化平台“全部完成”。
