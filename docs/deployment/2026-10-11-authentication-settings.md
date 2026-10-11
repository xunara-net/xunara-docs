# 登录与注册配置：开发和 HTTPS 测试站验收

## 交付范围

用户中心网络 owner 与平台后台均新增「登录与注册」：成员准入、OAuth2/OIDC
应用创建、启停、名称、密钥轮换、归档及固定回调。邀请历史保留，个人绑定仍在
安全中心；公开独立开户仅平台管理员可调整，不与共享网络邀请混淆。配置持久化、
版本 CAS、事务授权/审计及取消待完成授权，重启可恢复。

复核补了无密钥 OIDC 公共客户端：不调用要求非空的通用密封函数、不伪造密钥
已配置；非空凭据仍严格密封/解密，OAuth2 应用仍要求凭据。协议、API 和升级以
[服务端手册](https://github.com/xunara-net/xunara-server/blob/main/docs/authentication-settings.md)
及 [ADR-0029](../../adr/README.md) 为准，不复制接口结构。

## 实际部署产物

2026-10-11 已升级现有自签 HTTPS 测试站，未生成新 CA、未替换 TLS/pin 或中继进程：

| 仓库 | 实际产物源码 |
|---|---|
| Server | `acd19301a402b340d22a45b4f8060f8c08e5fb2e` |
| Web | `82919d15775b87a1bf4dcf651a8e6c8890d3985e` |
| Admin | `66d2d329a8095efb44a6d4709f8d40dff3494c2a` |
| Deploy 运维说明 | `fe87a2a`；未改服务参数 |

入口：`https://fakeop4.onbed.cn:9090/admin/authentication`；用户中心 owner 使用
`/authentication`。真实平台登录、网络 admin 的配置权限拒绝、绑定提示、租户
选择及固定回调预览通过。43 个 Web / 21 个 Admin 文件逐个匹配产物；手机
320 / 390 / 768px 无横向溢出、弹窗可取消，JavaScript 错误为零。

**没有擅自改变注册策略或创建假提供方**：入口租户原有公开独立开户保持开放，
共享网络成员加入仍关闭；managed 租户原邀请策略保持。用户可在新入口明确调整。
未配置真实公网应用，不把配置弹窗或隔离提供方当作生产 OAuth 已开通。

## 维护与数据保留

关闭公网写入、停控制面、保存一致性快照后升级。两活动租户 identity v14→15，
state v24 / plans v4 不变，迁移只追加。原表原列逐项核对，原账号、凭据、绑定、
设备、IP/网段、套餐、ACL、DNS、中继、环境和密钥保持；历史归档也核对。

首次替换遇到 `/srv` 与 `/root` 跨分区重命名，已在未开放写入时完整回退。
再次升级使用同分区原子目录交换，维护期间校验并清理临时旧目录，成功上线。
失败恢复旧源码与身份 v14 后健康检查通过，并非只换回二进制而留下新版库。

成功备份：`/root/xunara-rollback/20261011T040347Z-authentication-settings`。
私有目录保存 `snapshot.tar`、原 `nginx.conf`、清单和报告，含环境及私钥，不可公开。
快照内 nginx 是维护配置，恢复时须同时使用单独保存的原配置。仅仍关闭写入的
升级窗口可成套恢复；开放业务后禁止用过期快照覆盖新增数据。流程以服务端与
Deploy 升级说明为准。

上线只新增一个真实测试人类登录，已持久撤销；成功登录/撤销审计及两个限流桶
为预期元数据，不清除限流来伪造零变化。42 个快照中原会话（含归档）及撤销状态
保持，其余原行逐项保留。未写生产账户、角色、网络配置或假第三方应用。

## 验证和边界

- 最终全量 Go build / vet / test / race 通过，race 使用 20 分钟预算。
- Web 195 / Admin 42 项单测及类型检查、构建通过。
- 68 阶段综合浏览器与新增 6 阶段隔离真实 HTTPS 通过：邀请加入、独立开户、
  应用轮换/归档、跨后台 CAS、租户隔离、无密钥 OIDC 和手机弹窗。
- 运行时 OAuth2 绑定/回调、OIDC 签名/nonce/PKCE、重放及最后方法由隔离夹具
  验证；不连接公网 IdP，不代表运营方已申请真实应用。
- 公网请求校验自签 CA，浏览器只对指定证书公钥例外；不禁用全局 TLS 校验或
  安装系统 CA。安全上下文和 Secure/HttpOnly/Lax Cookie 通过。
- 上线使用 upstream `controlhttp` 完成 HTTPS TS2021/Noise、early payload、HTTP/2
  未知节点拒绝，未注册设备；不扩大为全 OS/双客户端数据面验收。

隔离命令及前置条件见 [Admin 验收](https://github.com/xunara-net/xunara-admin#浏览器集成验收)。
CI 以 [Server](https://github.com/xunara-net/xunara-server/actions/runs/38109665892)、
[Web](https://github.com/xunara-net/xunara-web/actions/runs/38108574441)、
[Admin](https://github.com/xunara-net/xunara-admin/actions/runs/38109666951) 为准。

真实第三方应用/可信证书、第三方自动独立开户、全局账户、独立超管人身份、找回/
邮箱验证、2FA、邮件投递仍有独立工作，不宣布全部商业化功能完成。
