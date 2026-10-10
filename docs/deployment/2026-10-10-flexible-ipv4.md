# 放开合法 IPv4 范围：验收与调试部署

- 任务：[Server #6](https://github.com/xunara-net/xunara-server/issues/6)
- 决策：[ADR-0023](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0023-flexible-ipv4-allocation.md)
- 版本：Server `bb32d65` / Web `726e8a5` / Admin `4ffca55`

## 修改与边界

按用户「不要限制网段」要求，后端与两个管理入口移除 CGNAT-only 和 /16～/28
人工限制，允许经安全检查的私有/公网单播 IPv4。主机位规范化后保存；/31 与
/32 主机池分别使用 2 和 1 个地址，其余池排除网络/广播地址。自动与手动规则
一致，小池耗尽拒绝注册，不回退旧池或重复分配。自动租户块的搜索成本上限
保持，32 位计算已验证；它不限制手工 CIDR 长度。

非法、系统/客户端内部、分享、部署保留、其他租户及历史预留仍受保护。
Entitlement、角色、CSRF、CAS、审计和通知沿用原链路；旧 IP 不自动改变。
没有数据库迁移、API 字段更改、套餐定义更改或 Headscale 依赖变化。
state v23 / plans v4 / identity v13、默认 CGNAT、IPv6 与官方 wire 均不变。

非标准地址允许配置不等于全平台官方客户端兼容，也不表示获得公网 IP 所有权。
用户和超管入口提示 LAN / 子网 / 公网路由冲突及客户端功能风险。ADR-0023 只
替代 ADR-0022 的强制范围部分，不重写历史规格或旧验收记录。

## 验证

本地全量 Go build / vet / test / race 通过；race Control 包用时 574.872 秒。
新增私有/公网、大/小池、/31 /32 容量和耗尽、手动 IP、跨连接竞争、重启、
旧设备/历史预留保持、跨租户冲突及自身/peer 标准地址更新回归。
netspace 的 `GOARCH=386` 测试通过，没有改写已发布迁移。

Web 177、Admin 37 项单测、类型检查与生产构建通过。真实 API 的 51 阶段
隔离 Chromium 验收通过，包含私有 /8、/12、/29、/31、/32 预览和保存、旧 IP
保持、刷新持久、/32 显式修改 IPv4、超管私有网段保存及匿名/成员边界。
320 / 390 / 768px 无页面溢出，零 JavaScript 错误。干净提交重新安装依赖、运行
单测和构建，产物与被测工作区逐字节一致；最终发布二进制再次通过 51 阶段验收。

官方 Linux Tailscale **1.102.2** 实测采用两个隔离 userspace-networking 进程和
本机实际 TLS DERP / STUN，不碰系统现有 daemon 或生产租户。两个客户端分别
接受 `10.42.0.1`、`10.42.0.2`，通过 WireGuard 的 IPv4 ICMP ping 成功；显式把
第一台改为 `10.42.0.20` 后，客户端收到更新，第二台再次 ICMP ping 成功。
这不是只验证 disco 发现，也不是主机 OS 协议栈、应用 TCP、全部 DNS/路由功能
或全部平台验收；不能据此宣称 Windows/macOS/Android/iOS 的全部功能已支持。

持续验证：[Server CI](https://github.com/xunara-net/xunara-server/actions/runs/38050840130)、
[Web CI](https://github.com/xunara-net/xunara-web/actions/runs/38050840670)、
[Admin CI](https://github.com/xunara-net/xunara-admin/actions/runs/38050845412)。

复核 Go：在 `xunara-server` 仓库目录，使用 `go.mod` 对应 Go 版本执行：

```sh
go build ./... && go vet ./... && go test ./... -count=1
go test -race ./... -count=1 -timeout=20m
GOARCH=386 go test ./netspace -count=1
```

复核浏览器：先构建 Server、Web、Admin，在环境中提供测试二进制、Playwright
模块及 Chromium 的绝对路径；在 `xunara-admin` 仓库目录执行，夹具只操作临时租户：

```sh
: "${SMOKE_XUNARAD:?先设置测试二进制绝对路径}"
: "${PLAYWRIGHT_MODULE:?先设置 playwright-core 模块绝对路径}"
: "${CHROMIUM_BINARY:?先设置 Chromium 绝对路径}"
export SMOKE_XUNARAD PLAYWRIGHT_MODULE CHROMIUM_BINARY
node scripts/browser-smoke.cjs
```

## 上线事实

2026-10-10 北京时间 20:13 更新调试站的 Server、用户中心及超管前端。
先校验基线二进制/入口与发布包，维护门禁生效、旧 nginx worker 排空、控制面
停止后完整备份状态、配置和产物，再安装并恢复服务。默认公共 Relay 不重启。
备份：`/root/xunara-rollback/20261010T121349Z-flexible-ipv4`。
发布包 SHA-256：`eddff7d3f49007bf5522ba1f5e6d3af7c9b63b26ab8244cef50efc9dc24b862a`。

`default`、`team` 原有身份/会话/设备/DNS/中继/配置/历史/实际地址配置及平台
套餐表指纹保持；未更改生产网段、设备 IP、账户、凭据或套餐。两租户实际范围
与期望范围仍一致；公共 Relay 的进程、重启计数、证书 pin 与地图保持，并经
真实 TLS pin 校验后 `/derp/probe` 返回 200。该探测不等于数据转发验收。

公网匿名 Chromium 逐个核对 Web 40 / Admin 19 个资产哈希，确认用户/超管页面
均需登录、地址/平台 API 为 401、移动布局无溢出及零 JS 错误。生产仅作只读
验收；实际写入与非标准地址证明来自隔离真实服务与官方客户端，不在生产造节点。

## 恢复与未完成

旧版可以读取相同数据库，但编辑器会拒绝新开放范围。已有非标准地址后回退
须保留当前数据并审查，不在线恢复旧快照覆盖新写入。生产调试站仍是 HTTP；
HTTPS、全 OS/功能实测、IPv6 自定义、安全地址回收、批量迁移和自动修订关联
ACL / 外部 DNS / 应用配置仍需独立开发验收。
