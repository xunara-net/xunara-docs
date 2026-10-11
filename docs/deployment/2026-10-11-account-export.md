# 本人账户安全资料导出：开发与 HTTPS 调试站验收

## 交付范围

个人设置新增默认折叠的私人导出入口：本人账户安全资料 JSON、成功登录记录
CSV，支持可选日期范围、隐私确认和等待取消。手机日期字段纵向排列；取消、
离页、失败、不完整或异常响应不生成下载，不自动重试，临时 Blob URL 清理。

JSON 是已保存的资料、绑定展示属性、通行密钥名称 / 时间、活动会话和成功
记录；CSV 仅是成功登录记录。资料不受历史日期筛选，不把分页首屏当成全部
记录。只允许所属租户有效本人 Human Session 和 CSRF，平台令牌也不能代读。
不含密码、令牌 / 哈希、CSRF、外部 subject、通行密钥认证材料或他人资料。

服务端同事务复核会话与启用用户，读取有界白名单快照并提交必需准备审计；
存储、审计或被忽略的写入失败关闭。行数 / 读取文本 / 最终文件超限整份拒绝，
完整编码后才发私有附件，不静默截断、生成公开下载地址或伪装空数据。
准备审计不是浏览器保存证明；取消或失败可能仍消耗请求次数。

CSV 使用标准编码器、中文表头和 UTF-8 BOM，危险文本加可见「文本：」前缀。
原文本查看 JSON；不承诺任意表格软件、用户删除前缀或再保存后的安全。
这不是凭据、网络或完整个人数据备份，也不支持据此恢复账户。

使用见[个人导出手册](../user/account-export.md)。接口、具体限额和事务边界以
[服务端说明](https://github.com/xunara-net/xunara-server/blob/main/docs/account-security-export.md)、
[ADR-0033](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0033-account-security-export.md)
为准；跨仓库任务见 [Server #16](https://github.com/xunara-net/xunara-server/issues/16)。

## 源码与上线

| 仓库 | 本轮源码 |
|---|---|
| Server | [`0ad7c29`](https://github.com/xunara-net/xunara-server/commit/0ad7c29725ae706f309795e1a0987032d42e6f52) |
| Web | [`bab7996`](https://github.com/xunara-net/xunara-web/commit/bab79969e1b7086552d0afc7f7ea7f94e49f89dd) |
| Admin 共享验收脚本 | [`bc0056d`](https://github.com/xunara-net/xunara-admin/commit/bc0056dd5b4ba21be382d47f8f5ee678153a73d4) |
| Deploy 隐私与升级说明 | [`01d7d25`](https://github.com/xunara-net/xunara-deploy/commit/01d7d2531d0d1e5bbfd53a92f4005d12b315a31f) |

对应提交 CI 全绿后，2026-10-11 22:07:55–22:07:56（Asia/Shanghai）维护升级
原自签 HTTPS 调试站，22:09 完成公网与原数据复核。Server 从干净 Git archive
构建，完整提交写入版本；Web / Admin 同样来自干净提交的生产构建。逐项检查
线上 45 个 Web / 22 个 Admin 静态文件与发布校验和一致；Admin 只改共享验收
脚本，没有新增代读私人资料的业务入口。

- 用户入口：`https://fakeop4.onbed.cn:9090/settings`，本人登录后展开「个人数据导出」。
- 原测试 CA：`https://fakeop4.onbed.cn:9090/.well-known/xunara-test-ca.pem`。
- 仍是自签测试证书，不宣称正式公网 CA 与域名运维已经完成。

## 公网与原数据验证

先关闭公网写入、停止全部旧控制面并排空旧代理 worker，再成套私有备份
数据库、密封密钥、配置、TLS、环境、二进制和静态产物，原子交换发布产物。
本轮无新迁移：两个活动租户 identity v18、state v24，plans v4 保持。开放前
逐项比较全部原表原列原数据，包括已有登录记录；不再次回填、改变未知来源
或用历史台账中的网段值覆盖当前配置。

公网仅检查版本、健康、平台用户列表与静态文件。匿名和平台 Bearer 请求本人
导出均被拒绝且没有附件；没有登录原人类账号、读取其私人历史或导出其资料。
真实 Chromium 验证 320 / 390 / 768 / 1440px 登录页无整体横向溢出，匿名访问
个人设置 / 安全中心回到登录并保留目标，后台仍独立登录；页面 JS 错误为零。
两个被拒绝的导出 POST 不算成功业务写入，操作方业务写入及新会话为零。

使用 upstream `controlhttp` 验证可信 HTTPS 控制密钥、TS2021 / Noise upgrade、
early payload 和 HTTP/2 未知节点拒绝，设备注册为零。没有修改官方 wire；
只读探测不扩展成全 OS 或双设备数据面验收。

开放后检查 108 张原人类身份 / 认证表：43 个原会话的凭据、有效期和撤销事实
以及 24 条原登录记录保持。活动时间单独验证不倒退，本次观察到更新为零。
原密码、禁用状态、恢复码、绑定、认证配置、设备、地址、DNS、ACL 与套餐保持。
受保护配置 / 密封密钥 / TLS 未改变，独立 Relay 没有重启。

备份：`/root/xunara-rollback/20261011T135459Z-account-export`，目录 0700，
快照、原数据摘要和报告 0600；包含私人数据与密钥，不可公开。归档中代理配置
是维护模式，成套回退还须恢复单独保存的原代理配置。尝试开放公网前即禁止
自动恢复旧快照，避免重载结果未知时覆盖新业务写入。旧备份保留，本次远程
暂存已删除；临时 SSH / 平台凭据已清理，不进入 Git 或公开验收资料。

## 自动验证

- 最终全量 Go build / vet / test / race 通过；专项覆盖本人 / 跨用户 / 跨租户、
  服务身份拒绝、撤销 / 禁用 / 过期复核、同事务跨连接一致性及故障 / 忽略回滚。
- HTTP 覆盖 CSRF、时间 / 请求校验、持久准入失败关闭、上限整份拒绝、隐私字段
  排除、CSV 公式 / 分隔符和完整文件头；共用限流忽略写入不再错误放行。
- Web 263 / Admin 51 单测、类型检查与生产构建通过。前端覆盖旧版、异常 / 截断
  响应、解压后字节限制、取消 / 超时、本人白名单和保留旧文本，不持久存文件。
- 干净发布产物的 78 阶段跨模块浏览器回归与 26 阶段真实自签 HTTPS 通过，
  页面 JS 错误为零。实际私人 JSON / CSV 下载、日期、手机、取消、审计故障、
  超限与限流均在隔离临时租户执行，不导出原站资料。
- 原有 OAuth2 / OIDC、成员、ACL、DNS、地址、中继、登录记录与进程重启回归
  一起通过；隔离规模样本不是相同数量的真实认证，不接触公网第三方提供方。
- 真实已发布 identity v18 产物初始化临时状态，当前版本同 schema 保留 45 张
  原表事实；旧 v18 产物仍能读取原会话，成套恢复后原登录可用。四阶段通过。
- 已发布 v17→18、v17 拒绝新库且不改原表、成套旧状态 / 旧产物恢复仍通过，
  保留 44 张原表事实；不是将当前迁移倒退来冒充旧版本验证。
- 部署快照的隔离回归发现 schema、用户、凭据或旧历史误改；开放前全事实
  比较，开放后分开检查不可变凭据 / 历史与合法活动，不跳过整张私人数据表。

可复制命令与前置条件见
[服务端验证说明](https://github.com/xunara-net/xunara-server/blob/main/docs/account-security-export.md#验证与兼容)
与 [Admin 浏览器验收](https://github.com/xunara-net/xunara-admin#浏览器集成验收)。
源码 CI：
[Server](https://github.com/xunara-net/xunara-server/actions/runs/38144441325)、
[Web](https://github.com/xunara-net/xunara-web/actions/runs/38144442944)、
[Admin](https://github.com/xunara-net/xunara-admin/actions/runs/38144753573)、
[Deploy](https://github.com/xunara-net/xunara-deploy/actions/runs/38144756350) 全部通过。
手册与 ADR 索引 [CI 通过](https://github.com/xunara-net/xunara-docs/actions/runs/38144841378)，
本上线记录由本仓库 CI 再次检查。

## 未完成范围

这次仅交付本人账户安全资料与成功记录下载。设备 / 网络 / ACL / DNS / Routes
导出、异步大规模导出、自动保留 / 删除、完整注销、失败尝试、邮件验证 / 自动
找回、2FA、独立超管身份、订阅支付和全局跨租户账户仍需独立开发和验收。
不把私人文件保存、实际生产用户操作、公网第三方应用、多实例或全 OS 兼容
矩阵包装成已验证，也不宣布整个产品已完成。
