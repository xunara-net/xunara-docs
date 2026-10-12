# 路由与出口管理：开发及 HTTPS 调试站验收

## 范围

路由页直接搜索/筛选/分页、审批预览确认，设备详情复用同一弹窗；旧前端保存
实现移除，v1/HTML 服务端入口委托同一事务。支持版本冲突保留草稿、读取最新状态
后重放明确意图，以及单独的出口/子网门禁和降级清理。

出口展示最后一次自报选择及失效目标，提供本机平台选择/停止说明；独立快照的
身份、IP、批准、在线/过期事实不一致时不提示已确认可选。手机用 APP，命令
没有认证密钥、不重置登录或远程执行。重复成功提示不堆叠遮挡手机操作。

契约以[服务端手册](https://github.com/xunara-net/xunara-server/blob/main/docs/route-management.md)
及 [ADR-0037](../../adr/README.md)为准，任务为
[Server #18](https://github.com/xunara-net/xunara-server/issues/18)。

## 源码和 CI

| 仓库 | 部署提交 | CI |
|---|---|---|
| Server | [232b991](https://github.com/xunara-net/xunara-server/commit/232b991c525605c2f09d8f04a8b93dc610c9fa5e) | [通过](https://github.com/xunara-net/xunara-server/actions/runs/38198834549) |
| Web | [d10d646](https://github.com/xunara-net/xunara-web/commit/d10d646223227f21116ae2df451ed6ceff988fe8)（含 [c2ea28d](https://github.com/xunara-net/xunara-web/commit/c2ea28dbf0fc434d5bdd39917d8b5f0658178af2)） | [通过](https://github.com/xunara-net/xunara-web/actions/runs/38200170246) |
| Admin 共享验收 | [480f7c8](https://github.com/xunara-net/xunara-admin/commit/480f7c81c6262ef7b9c692d36f7901c08a73c9f7) | [通过](https://github.com/xunara-net/xunara-admin/actions/runs/38199280545) |

无迁移，state v24 / identity v18 / plans v4 保持。Relay、Deploy 本轮不改代码，
不新发 Relay 二进制。产物由干净提交的不可变源码归档构建，前端 npm ci/构建/
测试、服务端版本嵌入、各文件校验和及私有发布清单与实际安装内容一致。

## 验证

- Go 全量 build/vet/test/race 通过；不是只跑新用例，CI 延长竞态预算但不跳过测试。
- 真实 SQLite：审计 ABORT/IGNORE、计数更新被忽略、两连接 CAS/旧差量合并、
  持久撤销/降权、租户/Scope、新旧入口、套餐独立门禁、降级、有界提交及读故障。
- Map 遥测保留当前批准/身份管理事实，旧密钥不能恢复；断开活动只更新单字段，
  时间不倒退。官方 Noise 实际验证批准/撤销 AllowedIPs/PrimaryRoutes。
- Web 360 / Admin 51 单测、类型检查和构建通过；共享 Chromium 最终 90 阶段，
  320/390/768/1440 宽度、审批/预览焦点、409 草稿与并发新增保留、503 显式恢复、
  成员拒写、出口本机命令及全部旧链路通过，JS 错误为零。

浏览器使用 0700 隔离临时租户和真实 Core；故障注入不是生产连通成功证明。
执行目录/前置条件以各仓库 README 和服务端手册为准。

## 调试站升级

原 [HTTPS 入口](https://fakeop4.onbed.cn:9090/login)已升级。维护期间关闭公网写入，
停止 Core 后做一致私有备份；原全部数据库行/字段、非数据库密钥及配置核对后
才重新开放。备份 `/root/xunara-rollback/20261012T033949Z-routes` 为 0700，
快照和报告为 0600；维护时间以远端记录为准。未在重新开放后恢复旧业务快照。

公网严格验证原测试 CA：health/version、所有前端文件实际内容与清单一致；
匿名路由读写、出口/设备报告/私有健康 API 均拒绝。原 CA 下载字节保持；
上游 SDK 通过 HTTPS 控制密钥、TS2021/Noise early payload 与 HTTP/2，未知节点
拒绝，未注册任何生产测试设备。

最终三个服务活动，108 个人类/认证数据集合、45 个原会话凭据/生命周期及
26 条原成功登录记录保持，活动变化为 0。没有操作员人类登录、改密、恢复码、
私有导出或假提供方；原配置、密钥、账号状态和默认 Relay 进程保持。私有
暂存发布目录已移除。测试站仍是自签 CA，不改变手机/正式客户端的信任要求。

## 未覆盖

匹配、自报与控制连接在线不证明实时数据面；没有全 OS 出口现场验收、远程
切换客户端、自动故障转移或新的路由选举算法。路线审批不是 ACL/IP 转发/
防火墙授权。支付、邮件验证/自动找回、2FA 及其它缺口仍见
[实现台账](../developer/implementation-status.md)，不称为全产品完成。
