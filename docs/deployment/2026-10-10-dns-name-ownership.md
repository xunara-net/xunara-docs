# DNS 名称归属开发验收（2026-10-10）

## 版本与状态

- Server：`88d19babd779ffefbb5b5fda7259dbeb63bb22b3`。
- 跟踪：[任务 #7](https://github.com/xunara-net/xunara-server/issues/7)；决策
  [ADR-0024](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0024-dns-name-ownership.md)。
- Server [CI 38058280838](https://github.com/xunara-net/xunara-server/actions/runs/38058280838)：
  已完成且结论为 success，build/vet/test/race 全部通过；head SHA 与上述 Server
  提交逐字一致，不使用旧提交的 CI 结果代替本次验收。
- 本轮只完成开发、隔离验收与 GitHub 提交，**没有登录或升级调试站**。
  线上仍是上一地址切片的 Server `bb32d65`、Web `726e8a5`、Admin `4ffca55`；
  本轮没有更改线上数据库、设备、网段、账号、套餐或公共中继。

## 完成内容

机器自报主机名与控制面分配的 DNS 名称分离；新同名设备和机器更名自动分配稳定
后缀，注册、轮换、MapRequest 和原生心跳走同一存储写入边界。设备、服务和自定义
记录双向检查同事务执行，查询失败不当作名称空闲，写入失败不发布候选事实。
共享投影读取来源的分配名，既有共享服务冲突检查统一尾点。

追加 state v24，identity v13 和 plans v4 不变。无冲突旧名称在绑定事务补录，旧 IP/
身份/记录不变；旧碰撞不静默更名。域名绑定后实例必须一致，在线换域名不在本次
实现。管理 API 字段、官方 wire、ACL、套餐、IPv4/IPv6 分配规则不变。

已清理重复的服务前置扫描和管理记录的独立设备名称判断；保留旧 UpdateNode 为
同一实现的薄委托，不把通用事实写入和名称更新分成两套竞争算法。

## 本地与隔离证据

- 最终 Go 全量 `build`、`vet`、普通测试及 `-race` 全部通过。最后竞态 control
  包为 582.337 秒，使用 `-timeout=20m`；不是跳过慢测试或只跑命中名称的子集。
- 新增 14 个顶层回归测试：两种 Store、同名注册、记录/服务双向保护、稳定重报、
  长名称、子域/ACME、跨 SQLite 连接竞争、真实 v23 只读预检/升级/重启、旧冲突与
  提交失败回滚、取消/读取故障、Noise/API/原生心跳和共享来源别名。
- 51 阶段真实后端 API Chromium 浏览器回归通过，包含 320/390/768px 手机/平板、
  权限矩阵、DNS CRUD/版本保护、中继、自定义网段与改 IP；0 JavaScript 错误。
  使用现有未改的 Web/Admin 产物，不把前端重构或新增手工别名 UI 当成已交付。
- 官方 Linux Tailscale 1.102.2 两个隔离 userspace 客户端，通过本地真实 TLS DERP/
  STUN 完成同名注册；预留管理 A 记录保留，机器在线更名得到新别名；官方
  `tailscale dns query --json` 内部 A/PTR 查询及按新名称的 WireGuard ICMP 通过。
  分配名的管理 API 覆盖请求被拒绝，控制面重启后名称与设备地址保持。
- 从上述干净 git 提交归档构建的二进制，版本字符串逐字匹配提交；其官方客户端
  脚本和 51 阶段浏览器再次通过。二进制 SHA256 为
  `f7764f6b73bf92cecdbbc4c5bb9dab8341de64de1961ad15af2a6d7aa2e23eae`。
  该文件是隔离验收产物，不是已签名/发布/上线的 Server Release。

复现命令、前置条件和实现入口以
[服务端操作文档](https://github.com/xunara-net/xunara-server/blob/main/docs/dns-name-ownership.md)
为准；本仓不复制接口或表结构。所有测试用临时状态和独立客户端 socket；凭据不
放参数/URL/日志，密钥文件 0600，不改宿主 DNS 或现有系统 tailscaled。

## 升级与未完成边界

上线前逐租户运行只读 `xunara dns check`，审查旧名称冲突，维护停写后做完整一致性
备份。启动迁移和域名绑定分属两个阶段，绑定失败时 schema 可能已经是 v24；旧
二进制不能直接打开。只能在未恢复业务、无新写入时成套恢复旧状态与旧产物，不能
在线恢复旧快照覆盖后续用户数据。本轮没有执行此升级，不复用历史上线证据。

测试用 `--accept-dns=false` 保持宿主 DNS 不变，验证的是官方内部 forwarder，
不是宿主解析器接管或全 OS DNS。用户手工别名、已绑定域名迁移、复杂共享投影的
持久全局名称预留、完整多实例实时下发、全 OS 实测及注册/审计整体原子性仍待完成。
本切片不等于 Viewer/Network Admin、2FA、找回、订阅支付等商业平台功能已完成。
