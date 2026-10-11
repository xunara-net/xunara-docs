# 设备接入与私有中继：开发及 HTTPS 调试站验收

## 交付范围

- 设备页添加设备向导：官方 Linux curl 安装/仅登录，MagicDNS、接收路由、子网、出口和名称参数；手机用自定义控制面地址。
- 设备详情显示真实客户端持久报告、中继归属/来源/端口、UDP/IPv6/NAT、端点和探测延迟；不冒充实时流量路径。
- 核心菜单常显，其他管理折叠；手机抽屉、紧凑摘要、选中中继功能自动保持可见。
- 独立 Linux systemd 私有中继安装器：预编译校验、隐藏令牌、专用 CA、身份保留升级和失败恢复。
- 中继真实本地 TLS 健康；私有列表主动控制面 TLS/HTTP 检测，租户/Scope/CSRF/限流/审计和公网防 SSRF。

契约与局限以[核心手册](https://github.com/xunara-net/xunara-server/blob/main/docs/device-core.md)、
[relay 安装手册](https://github.com/xunara-net/xunara-relay/blob/main/docs/private-relay-install.md)、
[ADR-0035/0036](../../adr/README.md)为准。任务记录为
[Server #17](https://github.com/xunara-net/xunara-server/issues/17)及
[Relay #2](https://github.com/xunara-net/xunara-relay/issues/2)。

## 源码与产物

| 仓库 | 对应提交 |
|---|---|
| Server | [0202c7c](https://github.com/xunara-net/xunara-server/commit/0202c7ce2e87e19f2f493c004a76d3aae342ff99) |
| Web | [a601611](https://github.com/xunara-net/xunara-web/commit/a601611200a920098a525e6c2159683f9fe7a193) |
| Admin 共享验收 | [1e96417](https://github.com/xunara-net/xunara-admin/commit/1e96417e7c7780638063823e1e214a175b93878b) |
| Relay | [9d5559d](https://github.com/xunara-net/xunara-relay/commit/9d5559dc792a0f4898da805b35cb48d433d67905) |
| Deploy 安装边界 | [8d5dd22](https://github.com/xunara-net/xunara-deploy/commit/8d5dd22) / [16a7ec4](https://github.com/xunara-net/xunara-deploy/commit/16a7ec4) |

[Relay preview.2](https://github.com/xunara-net/xunara-relay/releases/tag/v0.1.0-preview.2)
真实发布七平台二进制、安装器、SHA256SUMS、BUILD.txt；全部资产实际下载核实，
Linux AMD64 版本/安装器语法/参数验证通过。checksum 不是独立签名认证。

## 验证

对应源码 [Server CI](https://github.com/xunara-net/xunara-server/actions/runs/38184728498)、
[Web CI](https://github.com/xunara-net/xunara-web/actions/runs/38184729754)、
[Admin CI](https://github.com/xunara-net/xunara-admin/actions/runs/38184730614)、
[Relay CI](https://github.com/xunara-net/xunara-relay/actions/runs/38183939746)与
[预编译发布](https://github.com/xunara-net/xunara-relay/actions/runs/38183940859)均通过。

Server 全量 build/vet/test 通过。默认十分钟竞态预算超时，没有发现竞态或业务
断言失败；增加测试预算后全量十八个包通过，control 包 668 秒、868 测试及子场景
通过。仓库 CI 原本已使用二十分钟竞态预算。没有跳过测试或修改密码算法。

从 server 仓库根目录复现，需 go.mod 指定工具链：

```bash
go build ./...
go vet ./...
go test ./... -count=1
go test -race ./... -count=1 -timeout=30m
```

Relay 全量 build/vet/test/race、官方数据面回归、ShellCheck 和隔离安装/升级/CA
恢复通过；真实二进制与 TLS 执行，CDN/systemd/control 响应为明确夹具。
Web 类型检查/构建/314 单测，Admin 构建/51 单测通过；工作区和提交归档重建产物
均完成 83 场景隔离 Chromium，JavaScript 异常为零。320/390/768/1440 手机/桌面
无横向页面溢出，命令 bash 语法、真实设备报告、健康 API 地址阻断、成员拒绝验证。

## 正式调试站核查

2026-10-12 07:49:53–07:49:54（上海）关闭公网写入、排空旧 worker、停止 Core、
一致备份后更新 Core/Web/Admin 静态产物，再核实原行/原列/配置/密钥后开放。
使用提交归档重建，版本与所有公网前端文件逐一匹配 manifest。

首次严格状态校验触发自动回滚，未开放新程序后恢复快照。比对后确认仅历史网段
预留表新增一条已有设备 /32 保护项：旧程序重启同样由 reserveLegacyAddresses
补录，不是新功能迁移、账号或 IP 变化。刷新原站基线后重试，全表原行/原列校验
通过，没有放宽校验、人工改数据库或强行跳过一致性保护。

- 两个活动租户，state 24 / identity 18 / plans 4，未新增迁移。
- 108 个人/认证相关表集合、45 原会话、26 原登录记录保持，活动更新为零。
- HTTPS/公有测试 CA/nginx/org 配置/环境/密钥保持；默认公共 Relay 未重启。
- 公网 health/version 与所有前端产物通过；新增报告与检测匿名请求 401。
- 官方上游 HTTPS key、TS2021/Noise/early payload/HTTP2 验证通过，未知节点拒绝，生产注册零。
- 未登录、重置或导出真实人类账号，未签发生产私有中继令牌，未安装/覆盖原公共中继。

本次备份为 `/root/xunara-rollback/20261011T234918Z-device-core`，目录 0700、文件
0600；原首次回滚备份仍保留。私有 staging 已清理，公开报告不含凭据。
重开公网之后不得直接恢复旧数据库快照覆盖新写入，须按运维恢复流程处理。

## 尚未验证/交付

Linux 安装器不是 Windows/macOS 服务安装器。未声称所有架构/发行版现场运行、
真实公网私有安装、STUN/准入/用户端到端连通、实时路径、自动升级/故障转移完成。
上线核查不代替用户用真实设备实测。自签测试 CA 仍需核实并在需要的设备信任，
Android 是否支持用户 CA 取决于实际客户端版本。支付、邮件、2FA 等外围模块未完成。
