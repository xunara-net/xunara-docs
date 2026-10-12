# 简洁设备接入：单一复制与显式 Token

## 交付

「设备 → 添加设备」选择平台，勾选安装与可选 Token，再复制一个完整命令。
Linux 安装/加入两行合并，已安装则只给接入命令；MagicDNS、接收路由、名称、
子网/出口与有效期收进默认折叠的高级选项。显式选 Token 才直接带设备 Auth Key，
可粘贴已有密钥或生成默认 15 分钟一次性密钥，不自动签发/重试。

删除旧隐藏输入、Windows 临时密钥脚本、设备私有文件下载及独立 Token 复制
业务分支，不保留两套接入实现。已有 Token 隐藏生成按钮，清除与输入同行；
复制成功在原按钮反馈，不弹全局通知遮挡手机操作。关闭/切换浏览器或手机/
离页清除本页秘密，异步结果不能污染已关闭或新开的弹窗。

直接含 Token 的命令会进入剪贴板，执行时可能进入终端历史、进程参数或审计，
不能再宣称是无泄漏命令。页面在显式选择时提示风险，默认短期一次性密钥，
不把 Token 放 URL/query、应用日志或浏览器持久存储。私有中继安装不受此调整影响。
API、数据库、官方 wire、权限与配额都不改；仍沿用事务化签发/消费与设备审批。

当前契约以[服务端手册](https://github.com/xunara-net/xunara-server/blob/main/docs/device-enrollment.md)
和[实施前提案](https://github.com/xunara-net/xunara-server/blob/main/docs/proposals/2026-10-12-simplified-device-enrollment.md)
为准，[ADR-0038](../../adr/README.md)追加交互修订而保留后端事务决策。
任务为 [Web #3](https://github.com/xunara-net/xunara-web/issues/3)。

## 产物与测试

- 部署 Web [a35bc0e](https://github.com/xunara-net/xunara-web/commit/a35bc0eeaed835c622a0321ffa404fd859e6a2a9)，
  包含 [9c79aa0](https://github.com/xunara-net/xunara-web/commit/9c79aa0ee7c16d7d0b96183ba9567a24eb28b71f)；
  最终 [Web CI 通过](https://github.com/xunara-net/xunara-web/actions/runs/38269100133)。
- Server [405234b](https://github.com/xunara-net/xunara-server/commit/405234b7cdf1e9c1d5418301b4f8ea67ce23b3b7)
  仅改文档，不替换运行二进制；[其 CI](https://github.com/xunara-net/xunara-server/actions/runs/38267702067)
  的最终状态以运行页面为准。运行 Core 仍为上轮验收的 a9292d4，Admin/Relay/Deploy 不改代码。
- Web 402/Admin 51 单测、类型与构建通过；61 项针对性回归含 Linux mock 真实
  Bash 执行，下载/安装失败不继续接入，密钥/名称注入被拒绝，平台默认值核对 upstream。
- 最终共享 Chromium 96 阶段、真实 API 和真实剪贴板通过，JS 错误零；覆盖单一
  复制确实含设备密钥、无自动签发、手机主按钮可见/高级选项折叠、关闭/切换清理、
  权限未知/成员不能签发，以及已有网络/账号/设备过期等回归。
- 最终不可变 Git 归档重新 npm ci/类型/402 项测试/构建，全部 51 个产物与实际
  浏览器验收字节一致；不是拿修改前的构建充当最终验证。

## 只更新前端

[正式主域站点](https://fakeop4.onbed.cn:9090/login)已部署最终产物。先备份原 Web，
新增哈希资产，最后原子替换入口；旧哈希资产仅供已打开标签兼容，不进入新入口
依赖，源码中不混用旧接入实现。没有停止、reload 或重启服务，不触碰业务数据库。
最终私有备份为 `/root/xunara-rollback/20261012T151925Z-simple-enrollment-web`，
目录 0700、记录/快照 0600，不恢复开放业务后的旧数据库快照。

26 个受保护的 nginx/TLS/组织/环境/密钥与相关文件保持，Core/Relay/nginx 进程
保持。默认系统根从外部验证正式主域叶子不变、health/version、全部 51 个资产
与新匿名 API 拒绝；原租户 SNI/健康检查以及独立 OpenSSL 域名/信任验证通过。
一次公网旧租户握手瞬时错误经独立重试通过，没有降级 TLS 校验或修改生产配置。
没有操作员生产登录、改密、生成 Token、注册/过期设备或导出私人账户资料。
发布暂存清理，SSH 临时凭据验收后删除，未提交证书/Token/私钥。

## 边界

Linux 安装器与 CLI 执行为隔离 mock，不是实际软件包安装；Windows/macOS 和
安卓 APP 未现场执行，不伪造全 OS 或 WireGuard/DERP 数据面验收。原开发依赖
audit 六条告警仍待独立升级；主域正式证书的范围/到期/未自动续期情况仍按
[证书验收](2026-10-12-device-enrollment-production-tls.md)，不改变其他租户信任要求。
