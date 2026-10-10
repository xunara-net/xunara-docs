# 地址、非托管中继与预编译下载验收（2026-10-10）

状态：源码与真实下载已发布，最终全量/竞态、干净产物浏览器及隔离升级/成套恢复
通过；等待服务端 GitHub CI 完成后进行调试站维护升级，不把本地功能当成已上线。
任务：[跨仓任务 #5](https://github.com/xunara-net/xunara-server/issues/5)。
架构与 API 边界以
[ADR-0022](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0022-address-management-and-external-relays.md)
与[服务端说明](https://github.com/xunara-net/xunara-server/blob/main/docs/network-console.md)为准。

## 本切片实现

- 用户网段读取、校验预览、带版本保存与单设备 IPv4 旧值基准修改；不静默改旧设备。
  实际分配状态持久化，旧心跳不能还原旧地址，自身/peer 更新沿用官方 MapResponse。
- 设备池仅 CGNAT 子集，排除官方/分享/部署保留与其他租户历史地址。Free 仍禁止
  自定义 CIDR，不按套餐名称特判；IPv6 系统分配，RFC1918 用于子网路由。
- 期望/实际跨库提交分开表达，失败显示待应用并重试收敛；旧网段/节点预留不自动
  回收。实际范围/IP、身份复核、审计及通知同事务，不声称跨库全局原子性。
- 默认中继首屏展示来源/端口；非托管地图支持手工配置、官方固定 HTTPS 导入草稿、
  确认发布与历史恢复。双方地区碰撞检查，包括离线托管记录；租户 DERP policy 不绕过。
- 外部节点不等于托管服务，无心跳/执行回执或远程控制，不虚构在线或公共服务接纳。
- 用户中心七种平台架构预编译直接下载、校验和与构建记录；新增发布工作流，不自动升级。

## 真实下载发布

Relay 提交 `1f0a7de`、tag `v0.1.0-preview.1` 已推实际组织 `xunara-net`。
[主线 CI](https://github.com/xunara-net/xunara-relay/actions/runs/38025104649)与
[Release CI](https://github.com/xunara-net/xunara-relay/actions/runs/38025600732)成功。
[发布资产](https://github.com/xunara-net/xunara-relay/releases/tag/v0.1.0-preview.1)为 Linux
AMD64/ARM64/ARMv7、macOS Intel/Apple Silicon、Windows AMD64/ARM64 七个真实可执行文件。

已重新下载七文件并逐项通过同版本 SHA256SUMS；Linux AMD64 版本输出与构建信息
确认对应干净提交，不发布 dirty 本地构建。BUILD.txt 可追溯源码。无 Apple 签名/公证、
Windows 服务安装器、独立签名更新或全 OS 现场运行保证；校验和仅用于完整性。

## 验证入口与恢复

以下在对应仓库执行；Go/Node 版本以模块与 CI 为准，浏览器需六仓同级、已构建前端、
Node 22 与可用 Chromium。浏览器运行命令以 xunara-admin README 为准，使用随机内存
凭据与 localhost 临时租户，不连接生产写 API。

```sh
# xunara-server
go build ./... && go vet ./... && go test ./... -count=1
go test -race ./... -count=1 -timeout=20m
# 分别在 xunara-web / xunara-admin
npm run test && npm run build
# xunara-docs
python3 .github/check_links.py
```

隔离 Chromium 已通过 46 阶段、零 JS 错误，包含默认首屏、七下载入口、320/390/768px
布局、外部配置持久化/CAS/删除、网段仅预览与旧 IP 保持、设备 IP 冲突保留草稿及
成员只读。设备为隔离数据库夹具，不冒充官方客户端注册或真实网络连接。

Server `499654b` build/vet/全量 test/全量 race 通过，Web `f7a38c3` 的 164 项单测与
Admin `8c5d732` 的 37 项单测、类型检查和生产构建通过。干净提交的实际发布二进制
及两个 dist 重新运行完整 46 阶段 Chromium 通过；不沿用 dirty 预览产物的结果。
对应 [Web CI](https://github.com/xunara-net/xunara-web/actions/runs/38028634899)、
[Admin CI](https://github.com/xunara-net/xunara-admin/actions/runs/38028635569)与
[Deploy CI](https://github.com/xunara-net/xunara-deploy/actions/runs/38028761936)成功；
[Server CI](https://github.com/xunara-net/xunara-server/actions/runs/38028761595)竞态阶段尚在执行。

真实已发布 `aa459c8` 旧二进制初始化的隔离租户，同时验证 state v22→v23 和 plans
v3→v4：原身份/会话/凭据/设备/旧 DNS/中继与历史/套餐不变，网段/单设备 IP/外部
地图写入及重启保持，旧二进制拒绝新 schema，成套完整旧状态恢复后可再次访问。
官方 live HTTPS 源通过新产品 API 成功导入预览且未保存；不证明公共中继接纳/转发。
初次回退脚本误用新版本断言，纠正后重新运行完整演练，不修改生产状态。

本切片只追加 state v23、plans v4，identity v13 不变。上线先核对真实旧产物与
各租户地址冲突，再关闭公网入口、排空请求、停止所有写任务、备份完整平台根/
活动/归档租户与匹配产物。旧服务端拒绝新 schema，回退须在恢复公网写流量前同时
恢复旧完整状态及旧产物；业务已恢复后禁止旧快照覆盖新写入。
静态公共中继不重启、不迁托管、不换 key/证书/pin；不在生产造测试节点或改密码。

## 尚待记录与限制

实际调试站维护升级及匿名/授权只读验收结果待确认。全 OS 外部设备实测、全生命周期网段回收/
迁移、IPv6 编辑、公共跨租户发布、计费/签名自动升级和生产 HTTPS 仍是独立缺口。
