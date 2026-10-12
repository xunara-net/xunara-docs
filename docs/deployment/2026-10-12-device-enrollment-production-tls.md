# 设备过期、Token 接入与主域正式 HTTPS 验收

## 交付范围

用户设备列表和详情提供立即过期：显示当前身份和有效期，明确确认后只改变
设备 expiry，版本冲突必须刷新确认。设备需重新认证；不会把人类账号或中继
身份一起撤销。添加设备新增预授权 Token 模式，可签发短期一次性 Auth Key，
或使用已有设备密钥；不是平台管理令牌/API Key。

桌面命令通过隐藏输入和权限受限文件交给官方 `--auth-key=file:`，不把密钥放
URL/外部进程参数。Linux 显式确认后可下载含密钥的私有一键脚本；关闭窗口或
切换接入方式清除页面内存，不落浏览器持久存储。手机仍使用官方 APP 的浏览器
加入，不伪造 APP 的 CLI 参数支持。

使用与权限以[用户手册](../user/network-console.md#设备接入与中继诊断)、
[服务端契约](https://github.com/xunara-net/xunara-server/blob/main/docs/device-enrollment.md)
及 [ADR-0038](../../adr/README.md)为准；任务为
[Server #19](https://github.com/xunara-net/xunara-server/issues/19)。

## 源码与验证

| 仓库 | 实际部署提交 | CI |
|---|---|---|
| Server | [a9292d4](https://github.com/xunara-net/xunara-server/commit/a9292d4c88484c6516941841f2ca9a48e4a244d8) | [通过](https://github.com/xunara-net/xunara-server/actions/runs/38212659203) |
| Web | [9c5ddf9](https://github.com/xunara-net/xunara-web/commit/9c5ddf9c07a0cd77e4ae379f5f2f1f8986f9a41a) | [通过](https://github.com/xunara-net/xunara-web/actions/runs/38211357142) |
| Admin 共享验收 | [877e22a](https://github.com/xunara-net/xunara-admin/commit/877e22a841d618a4d85251331c84e91302ef5d11) | [通过](https://github.com/xunara-net/xunara-admin/actions/runs/38210531873) |

- Go 全量 build/vet/test/race 通过，最终 control race 967.810s；没有跳过旧用例。
  浏览器审批与 AuthKey 新建设备共享事务内额度计数，Free 第十一台不能并发越界。
- 真实 SQLite 覆盖持久身份/会话/角色复核、审计 ABORT/IGNORE、CAS、跨连接密钥
  消耗及额度竞争；已有机器满额时仍可合法重新认证并保持稳定身份和地址。
- 官方 SDK Noise：通过人类 API 签发密钥→真实机器注册→手动过期的 Map/注册
  反馈→重新认证；迟到客户端补充密钥或缩短有效期不能覆盖管理员过期事实。
- Web 396/Admin 51 单测、类型检查和构建通过；最终不可变产物的隔离 Chromium
  95 阶段通过，JS 错误零，覆盖真实 API、下载、失败关闭及四档宽度。
- Linux 私有脚本实际执行隐藏输入/文件权限/清理路径，但安装器与 CLI 为隔离
  mock，不是实装软件包。Windows 参数解析已修正，Windows/macOS 未现场执行。

没有新增迁移，state v24 / identity v18 / plans v4 与官方 wire、套餐规则保持。
旧 v1/HTML 是同一事务的适配；Cookie 下 v1 AuthKey 写新增 CSRF 要求。浏览器
审批的整个状态/审计链路并未因此全部事务化，不能扩大这一计数修复的结论。

## 功能上线与原数据

不可变 Git 归档重新构建并核对所有资产，按原 TLS 独立升级功能，再单独替换
证书。功能维护关闭公网写入、停止 Core、排空旧 nginx worker 后一致备份，
检查全部原数据库行/字段及非数据库密钥/配置后才重新开放。维护记录为
2026-10-12 14:04:48 UTC；私有备份为
`/root/xunara-rollback/20261012T062941Z-device-enrollment`（目录 0700、文件 0600）。

两个活动租户保持，最终复核 108 个人类/认证数据集合、46 个原会话凭据与生命周期、
27 条原成功登录记录；活动变化零。没有操作员人类登录、改密、生成恢复码、
导出私人账户数据、添加假提供方、注册或过期生产测试设备。原账号状态/登录配置/
设备/网络/套餐、控制密钥与默认 Relay 保持；发布暂存目录已移除。开放后不恢复
旧业务快照。公网先严格验证原测试 CA 下的版本、全部资产和新增匿名 API 拒绝。

## 正式证书替换

[主域入口](https://fakeop4.onbed.cn:9090/login)使用用户提供的完整证书链：SAN
`fakeop4.onbed.cn`，发行方 Let's Encrypt YR2，有效期至 **2027-01-10 02:27:57 UTC**。
系统信任链、域名、私钥匹配及未来七天有效性均通过，不使用跳过验证或信任叶子
证书的方式。ZIP/私钥未提交任何仓库，暂存文件私密保护并在验收后清理。

单域证书不覆盖已有 `nip.io` 租户或其他子域；只新增主域精确 SNI 的正式链，
其他 SNI 保留原测试链与转发行为。主域旧测试 CA 下载返回 410，其他测试域名
仍需原 CA 或各自正式证书；不能宣称所有自助租户已经获得受信任 HTTPS。

只有 nginx reload，Core 与 Relay 进程未重启、控制密钥不变；9091 的默认中继
证书和 pin 不换。最终 TLS 回滚备份为
`/root/xunara-rollback/20261012T141235Z-production-tls`，同样 root 私有。服务器
公网回环探测超时的尝试仅恢复 nginx，没有触碰业务数据；最终先用回环地址与
真实 SNI 校验，再从外部独立通过默认系统根验证。

外部验收使用系统根验证 TLS 1.2/1.3，确认提供的叶子证书实际生效、
health/version/所有前端资产一致、新增
匿名生命周期/Token API 均拒绝、旧安全 HTTP 页面 308 仍有效；原租户 SNI 与
健康保留。官方 upstream SDK 仅使用系统根，经 HTTPS 控制密钥、TS2021/Noise
early payload 和 HTTP/2 返回未知节点 404，没有创建生产设备或账户。

运维步骤以[正式证书轮换手册](https://github.com/xunara-net/xunara-deploy/blob/main/nginx/production-certificate.md)
为准。**尚未配置自动续期**，须在上述到期时间前轮换；可信根正常的现代客户端
访问主域不必再导入测试 CA，仍须直接配置 HTTPS 地址。
Deploy 原有 16 阶段真实 nginx/安装器隔离回归及脚本语法检查通过；此回归不改变
生产配置，systemd 调度 fixture 不等于完整生产演练。

## 未覆盖与风险

未现场执行所有 OS 安装、实际安卓 APP 登录、双客户端 WireGuard/DERP 数据面或
真实第三方应用回调；只读协议探测不能当成这些已完成。存量前端开发依赖 audit
仍有 6 条告警（3 moderate/1 high/2 critical），没有强制无关升级或公开开发服务。
付款、邮件、2FA、完整账号生命周期等仍见[实现台账](../developer/implementation-status.md)，
本轮不是全产品完成声明。
