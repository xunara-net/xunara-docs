# 访问权限可视化、DNS 与私有中继验收（2026-10-10）

状态：最终本地回归、发布产物隔离验收与代码仓库 CI 通过，已完成维护升级；公网匿名
浏览器与授权平台只读验收通过。
本记录只覆盖网络控制台切片，不宣称全部规格或完整商业化平台已完成。

源码：服务端 [`5cbccd3`](https://github.com/xunara-net/xunara-server/commit/5cbccd3)、
用户中心 [`15c232c`](https://github.com/xunara-net/xunara-web/commit/15c232c)、
中继 [`e703d35`](https://github.com/xunara-net/xunara-relay/commit/e703d35)、
超管验收 [`9a10ca6`](https://github.com/xunara-net/xunara-admin/commit/9a10ca6)、
升级说明 [`98efec4`](https://github.com/xunara-net/xunara-deploy/commit/98efec4)。
跨仓库任务见 [Web issue #1](https://github.com/xunara-net/xunara-web/issues/1)。

## What changed

- 规则、策略图、矩阵、设备/成员组、高级策略、测试与历史使用同一 AST/Compiler，
  新增预览/自检/确认、CAS 发布、真实规则解释与版本恢复。
- 网络配置、不可变历史、成功审计、身份复查与客户端更新由持久事务和不可变快照
  承担；移除重复 DNS 删除业务，旧入口只保留同一保护和门禁的薄适配。
- MagicDNS、解析器、搜索域、split DNS 和 A/AAAA 增改删真实保存并下发，保护设备/
  服务/证书名称；域名仍由部署管理，不造未支持的 TXT/CNAME 编辑器。
- 租户私有中继页与路由分开，显示真实托管记录/额度、有效地图和一次性接入；
  服务端合并健康/近期心跳/启用/策略允许的私有地区，Relay 上报真实编号与 TLS pin。
- 桌面可收起侧栏，手机默认关闭的抽屉、焦点/滚动边界和单行功能标签；截图定位并
  修复通用按钮 CSS 覆盖响应式隐藏，避免桌面误显示手机按钮。

## Why

页面存在不等于可以安全完成操作。ACL 不能从图形状态另造授权，DNS 与地图不能
只改 UI；旧互通默认要明示，窄允许不能伪装成拒绝覆盖。草稿、发布、实际权限、
心跳与网络可达性必须分开，手机也不能把整套菜单堆在功能正文前。

## Compatibility impact

state 只追加 v20/v21，身份保持 v13；旧设备、DNS、会话和中继身份保留，旧迁移不改。
原配置首次发布前保持原语义，首次发布后数据库独占权威并保存版本 0；恢复历史
生成新版本。配置清空使用标准明确空 DNSConfig/DERPMap，不用 nil 留下旧配置。

不改官方 TS2021/Noise/Map/DERP wire 类型、Machine identity、Headscale 或套餐判定。
新产品 API 由独立 Web 使用；Free 仍默认 10 设备，写入按 Entitlement 而非套餐名称。
普通成员只读；应用 Grants/特殊端口规则通过高级编辑保留，不能称所有语法都可无损图形编辑。

## Security impact

策略/DNS 事务重查持久会话/API Scope 与角色、保存审计/历史、推进配置通知，策略
同时清旧 SSH check 批准；CAS、CSRF、严格字段/重复键与失败关闭防止部分或误发布。
服务身份不能覆盖令牌可见范围，私有地区不跨租户广播，TLS pin 由官方客户端验证。
一次性令牌只在内存显示、关闭/离开即清除；迟到响应不重新保留秘密，不入 URL、
argv、shell 历史、浏览器存储或日志。网络 API 超时不自动重复写入、不伪装提交失败。

## Tests

Go 命令分别在 server / relay 仓库执行，前端命令分别在 web / admin 仓库执行：

- 服务端发布提交 build/vet、全量 test/race 再次通过（控制面 race 548 秒）。覆盖严格解析、实际解释与
  Filter 一致性、跨连接 CAS/额度竞争、撤销/过期/降权/凭据混淆、各写点审计失败回滚、
  跨租户边界、读取错误不是空资源、重启/第二实例和历史恢复。
- 真实 TS2021/Noise 流收到 DNS 与 PacketFilters 更新；官方 derphttp 客户端用实际
  TLS 证书验证 pin，错误 pin 拒绝，不使用 InsecureForTests。Relay build/vet/test/race 通过。
- Web 146 项、Admin 25 项单测、类型检查和生产构建通过。最终 Linux/amd64 发布二进制
  下 34 阶段 Chromium 回归零 JS 错误，涵盖本地真实 OIDC/邀请及完整网络管理交互。
- 权限浏览器核对可视化编译、预览取消无生效、自检失败禁发布、CAS 草稿保留、
  矩阵跨目标页和真实原因、默认拒绝与历史恢复；DNS 检查增改删/名称保护/持久与冲突，
  中继检查秘密清除与成员只读。320/390/768px 无整体溢出，桌面/手机截图复核。
- 隔离设备由 Node 22 内置 SQLite 夹具构造，实际管理 API 和 Compiler 不打桩；
  这不代表浏览器完成了官方客户端注册或发包。生产不创建这些设备、账号或故障。
- 与线上同一 `65cba43` 已发布二进制初始化的隔离 state v19，保存完整停机快照后升级
  到 v21，身份 v13、原会话、DNS 与中继服务凭据保留，已用接入令牌不能重放。
  旧二进制拒绝新库；同时恢复旧产物和完整 v19 快照后原会话与中继心跳仍有效。
  这是隔离升级/恢复演练，不是生产回退或完整灾备验收。

对应代码提交的 GitHub CI 全部通过：
[服务端](https://github.com/xunara-net/xunara-server/actions/runs/38005904420)（完整 race）、
[Relay](https://github.com/xunara-net/xunara-relay/actions/runs/38005906391)、
[Web](https://github.com/xunara-net/xunara-web/actions/runs/38006149969)、
[Admin](https://github.com/xunara-net/xunara-admin/actions/runs/38005912389)、
[部署](https://github.com/xunara-net/xunara-deploy/actions/runs/38005914249)。部署 CI 包括
shellcheck、systemd/nginx/Compose；本机仅执行 shell 语法检查，不冒称本机已装 shellcheck。

发布二进制 SHA-256：`39e3495fddacc4f0c67259f8fc27e32e3ba92fd332f9b32fb5c7b72e8cffffab`。
从干净提交构建并逐文件校验前端；公网升级只替换 server/web/admin，中继代码已发布
但现有静态公共中继不重启、不重建证书或改准入配置。

## 维护升级

完整回归和对应 GitHub CI 通过后，仅关闭 Xunara 公网入口、排空旧 nginx 工作进程、
停止控制面并保存所有平台/活动/动态/归档状态、配置和旧产物，备份为
`/root/xunara-rollback/20261009T235908Z-network-console`（主机 UTC；本文日期为 Asia/Shanghai）。
目录 0700，状态及配置归档 0600；按机密保留。静态旧资产留作已打开页面/维护回退使用，
原子替换新入口，逐文件校验实际新产物，不让旧源码混入新构建。

`default` 与 `team` 的 state 从 v19 升至 v21，身份仍为 v13。迁移前后逐表摘要确认
原用户、密码、身份链接、Session、设备、DNS 和中继凭据保留，新配置/历史表为空，
没有隐式发布策略。租户集合、套餐、网段和域名不变；组织/环境/服务单元/原 nginx/
静态公共中继 map 不变，公共中继未重启、证书 pin 未变。确认后恢复公网，三服务 active。

公网 `/version` 为 `5cbccd3`；匿名 Chromium 验证所有新静态产物与发布 manifest 一致，
权限/DNS/中继及旧 console 均要求登录，超管使用独立登录，权限回跳保留；320/390/
768px 登录页面无整体溢出、零 JS 错误。策略、DNS、地址记录、私有中继、接入令牌
及平台中继受保护 GET 均为 401。授权平台只读核对两活动租户及实际统计/套餐契约；
托管注册数为零，静态公共中继不是注册记录，不能据此说没有中继。

本次不修改生产账号密码、不造测试账号/设备/中继或注入故障；公网测试只读，不替代
用户自己的真实连接验收。平台凭据只在远端内存经请求头使用，不进入报告或命令。
升级成功，未执行生产回退；保留一致性快照，不在公网恢复后覆盖状态。

失败只在维护窗口内同时恢复完整旧状态与产物；恢复公网写流量后绝不能覆盖旧快照，
不能仅回退二进制、手工降 user_version 或删表“兼容”。备份包含秘密，须私有权限保存。

## 后续边界

本站仍是 HTTP 调试，不是生产 HTTPS/Passkey/OIDC 配置验收；未重新执行外部双
官方客户端的真实数据面或全 OS 矩阵。模拟允许不代表服务、路由、防火墙或真实链路
已连通，心跳不代表延迟或可达。大规模虚拟化/分组、完整细粒度 RBAC、全语法
无损可视化、DNS 注册/更名反向冲突、中继配置 CAS/历史/全部审计原子性、计费、
灰度/签名升级与完整恢复仍需后续交付。具体见[实现台账](../developer/implementation-status.md)。
