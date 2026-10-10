# 成员权限事务开发验收（2026-10-11）

## 版本与状态

- Server：`d9ca3c8a0d48217b37c9b0ed3c7ff1c76de958e3`；
  [任务 #8](https://github.com/xunara-net/xunara-server/issues/8)和
  [ADR-0025](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0025-atomic-member-updates.md)。
- Web：`02527c91ff3615ea2e7a37469ca80fddeb60d879`。
- Admin：`3a19ff4c3d58425f287918e7a5fb798012bd42e2`，只修改组合验收脚本，生产源码不变。
- Server [CI 38068652782](https://github.com/xunara-net/xunara-server/actions/runs/38068652782)：
  completed/success，build/vet/test/完整竞态测试全部通过，head SHA 匹配上述提交。
- Web [CI 38068653102](https://github.com/xunara-net/xunara-web/actions/runs/38068653102)和
  Admin [CI 38068654617](https://github.com/xunara-net/xunara-admin/actions/runs/38068654617)
  completed/success，head SHA 分别匹配上述提交。
- 本轮没有 SSH、部署或写入生产账号/会话/角色/套餐/网络/设备/中继。上次调试部署
  记录见 [合法 IPv4 验收](2026-10-10-flexible-ipv4.md)，本轮没有重新确认当前线上版本。

## 已交付切片

JSON 与兼容 HTML 成员修改共用 Identity 字段补丁事务；重新验证持久发起会话或
服务 key、当前 owner、目标版本与最后 owner，再提交更新和必需审计。审计/业务
写入零行也失败关闭，不把 SQL 无报错当作已提交。无变化请求仍检查凭据，不产生
假的变更审计。API 追加原始更新时间，Web/兼容表单传回原始版本，冲突暂停写入，
必须手动刷新、重新确认。旧服务端缺版本时不造默认基准，保留可读列表并禁写。

CLI 使用可信磁盘操作者的独立入口，共用补丁/不变量/审计；HTTP 不能选择这个
入口。旧完整 UpdateUser 保留为薄适配，已有版本时不能用旧资料恢复旧角色。
删除与降权在同一数据库写事务内复核 owner，不再各自检查外部旧列表。

仍使用 owner/admin/member，没有新增 Viewer/Network Admin 或 Resource Scope。
管理角色不替代 ACL，不改变 Human/Machine/Service 的信任边界。

## 验收证据

- 最终 Go build/vet/全量普通测试通过，control 为 78.722 秒；最终完整
  `go test -race ./... -count=1 -timeout=20m` 通过，control 为 598.962 秒，
  identity 为 61.778 秒。不是定向子集，也没有跳过慢测试。
- 新增 14 个顶层测试：字段保留、单次审计/无变化、会话与服务 key 的撤销/期限/
  异主/当前角色/范围、租户边界、版本 ABA/旧完整快照、查询错误、失败与忽略写入、
  跨连接 CAS、48 个 owner 移除竞争场景、真实 HTTP 门禁后的撤销与表单对等。
- Web 180 项、Admin 37 项单测及两仓库类型检查/生产构建、脚本语法检查通过。
- Chromium 56 阶段真实后端组合回归通过，320/390/768px、0 JavaScript 错误。
  新增五阶段：真实角色发布/会话权限更新、过期确认 409、手机手动刷新与重新确认、
  所有权交接及管理员不能自升、缺版本禁写；不将早期展示夹具的失败响应当作真实
  成功。临时夹具最终恢复原 owner/member；没有重置生产角色。
- 三个干净 Git 提交归档重新构建，独立产物再次通过全部 56 阶段浏览器。Server
  版本字符串与完整 SHA 逐字一致，二进制 SHA256 为
  `c0c7a8b2f8fbc89eadf4b19a8e6dbd34bf12d4113546441ddc1bc0753b5694cf`。
- 干净归档 CLI 在私有临时状态目录真实执行角色/资料修改与原子审计；最后 owner
  降权被拒绝，未提交字段/创建时间保留，忽略审计写入时角色回滚，未支持角色拒绝。
- 干净 Server 产物再次通过官方 Linux Tailscale 1.102.2：同名注册、在线更名、
  内部 A/PTR、按新名称的 WireGuard ICMP、记录保护和控制面重启保持。使用临时
  TLS DERP/STUN、独立 userspace 客户端/socket，关闭宿主 DNS 接管；不是全 OS 或
  系统解析器验收。该产物没有被签名、发布为正式 Release 或部署上线。

最初测试的文件权限场景因启动测试时使用 umask 077 未构造出预期的宽松文件而
失败；调整测试进程为正常 umask 022 后全量重新通过，未修改生产证明权限规则。
旧降权夹具先创建备用 owner，损坏场景显式模拟外部损坏，不放松正常删除保护。
浏览器交接场景修正了把普通提示当作 ARIA alert 的选择器后全量重新验证，不隐藏
真实失败；这些历史失败不计作最终通过。加强零行写入后停止早期竞态进程，并在
最终代码上重跑完整竞态，不能沿用早期结果。

复现入口、前置条件、字段和源码以
[服务端成员管理](https://github.com/xunara-net/xunara-server/blob/d9ca3c8a0d48217b37c9b0ed3c7ff1c76de958e3/docs/member-management.md)
及其链接为准，本仓不复制会漂移的接口或表结构。测试和日志只用隔离状态，凭据
不进入参数、URL 或错误栈。

## 兼容、升级与未完成边界

本切片无新迁移，state v24、identity v13、plans v4 保持；官方 wire、节点身份、
ACL、地址与套餐规则不变。HTTP 字段追加、旧无版本请求仍接受事务保护，但不
提供客户端 CAS 保证；Go Store 增加方法，第三方持久实现需要同步。

若从旧 state v23 升级，仍需前一 DNS 切片的逐租户只读名称预检与停写一致性备份，
不能以本切片无迁移跳过累计升级步骤。本轮未执行升级或恢复旧快照覆盖用户数据。

Viewer、Network Admin、Member 的设备 Resource Scope、其他资源写点的原子授权/
审计、平台删除/撤销整体事务、跨库账户注销/恢复生命周期、第三方首次建号、
多实例实时发布及 2FA/邮箱找回/订阅支付仍待完成。此验收不是所有角色或商业平台
功能已完成的声明，也没有改变前次 DNS 全 OS/复杂共享名称预留的未完成边界。
