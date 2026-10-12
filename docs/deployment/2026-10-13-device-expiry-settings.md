# 2026-10-13 单设备有效期设置验收

## 交付

设备列表与详情统一「有效期设置」：按 1/7/30/90/180 天、指定本地日期时间、
永不过期、立即过期；已过期设备只能显式临时续期 30 分钟，再在窗口内重新
认证或调整可信设备的有效期。相对天数从服务器事务计算，时间冲突/未知结果
需要重新读取确认，不自动续期或重试。紧凑弹窗保留手机可见页脚和键盘焦点。

只改变当前节点密钥，不改变 Token TTL、网页登录或全网络默认认证周期，
不删除设备、地址和路由，不释放设备额度。权限/CAS/必需审计通知共用原子
写路径，旧立即过期接口委托它。无迁移、官方 wire 或 Headscale 内部依赖改动。
契约以[Server 手册](https://github.com/xunara-net/xunara-server/blob/main/docs/device-enrollment.md)
和 [ADR-0039](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0039-device-expiry-settings.md)为准。

## 源码与验证

- Server `20b4577d99c946ca97e6d93fb545b55d858f47e6`，任务 [#20](https://github.com/xunara-net/xunara-server/issues/20)。
- Web `188ce2715544d71e1badddb06ff72f0a1a0a400e`，任务 [#4](https://github.com/xunara-net/xunara-web/issues/4)。
- Admin `877e22a841d618a4d85251331c84e91302ef5d11`，源码未改。
- 本地完整 Go build/vet/test/race；Web 435、Admin 51 单测与类型/构建通过。
- 时间边界/溢出、持久权限/CSRF、跨连接 CAS、IGNORE/ABORT 回滚、有限/零有效期
  持久读回、真实 TS2021 Map 与临时恢复、客户端不能延长管理员窗口有回归。
- 最终 100 阶段真实 API/剪贴板/手机隔离浏览器通过，JS 错误零；包含本地时区/
  DST、指定时间、永不过期、自然到期后的重新确认、过期恢复与不自动重试。
  发布版复跑曾在既有成员选择器出现一次等待超时，独立完整复跑通过，未为本
  任务修改该模块，不把首次失败隐藏成全程零失败。
- 干净 Git 导出构建，前端与浏览器验收产物逐文件一致，发布版 Core 再跑针对性
  回归及最终完整浏览器通过；版本嵌入 Server 提交。

Web CI [38282760548](https://github.com/xunara-net/xunara-web/actions/runs/38282760548)通过。
Server CI [38282919157](https://github.com/xunara-net/xunara-server/actions/runs/38282919157)
包含完整 build/vet/test/race，结果在最终交付前复核。

## 安全发布与现场

正式调试入口仍为 `https://fakeop4.onbed.cn:9090/login`。两个 TLS 虚拟主机均
临时关闭并实测 503、旧请求排空、控制面停止后取一致私有快照；不停止 Relay。
原表/列/全部行摘要、非数据库状态、配置与密钥验证后才重新开放。开放后禁止
用旧数据库快照覆盖新业务写入；旧哈希资源只为已打开标签保留，不进入新入口。

首次严格校验发现 `tenant_network_reservations` 增加一条，开放前自动回滚。
确认是原有启动流程补录已有设备 /32 的保护记录，不是设备/账号/IP 变化；旧版
回滚启动亦补录相同保护记录，核对全部已注册地址已受保护，无操作员改数据库。
再次发布保留原严格校验，所有原表/列/行摘要完全一致，不放宽未知变更的检查。

最终私有备份 `/root/xunara-rollback/20261012T172408Z-expiry-settings`，目录 0700、
快照/记录 0600。现场 state v24 / identity v18 / plans v4，两个租户保持。
27 个受保护文件、证书/组织/环境/账号状态不变，108 个身份相关表检查通过，
46 个原会话及 27 条登录记录保留，独立 Relay 未重启。

公网系统根验证正式叶子不变、health/version、74 个前端资产逐文件匹配、匿名
有效期/接入接口拒绝；其他租户原 SNI/健康保持。官方 SDK 完成 HTTPS /key、
TS2021 Noise/early payload/HTTP2 未知节点拒绝，只读无注册。没有操作员生产
人类登录、改密、生成 Token、设备注册/过期或私人账户导出。发布暂存清理，
SSH 临时凭据验证后删除，未提交任何证书包、私钥或真实令牌。

## 边界

跨连接持久读回不是整机灾备演练；Chromium 手机尺寸不是 Android/iOS APP
现场复测。不改变现有网络默认认证周期或合法重新认证策略，不冒充全产品
开发完成。正式证书的主域范围/到期/未自动续期情况保持，见[证书验收](2026-10-12-device-enrollment-production-tls.md)。
