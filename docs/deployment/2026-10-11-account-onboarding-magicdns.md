# MagicDNS 与 OIDC 账户入网验收（2026-10-11）

当前调试站 Server 为 `5fc7e6b6fbd793a9e774e87c4725fd9556ee8057`，包括文末的
旧默认配置兼容补丁；最初功能版本的证据仍单独保留，不混用两次验收。

## 首次发布与范围

- Server：`507b16a7d3a1baa83a7c0e5df3b9b77b32eb51d5`。
- Web：`a0effa3aacc667188e1389bafc216de351b17e10`。
- Admin：`944e60bd2eda5c1d2012b0f92973693b679e96dd`；只扩展浏览器回归，不修改后台产品代码。
- [任务 #10](https://github.com/xunara-net/xunara-server/issues/10)、
  [ADR-0027](https://github.com/xunara-net/xunara-server/blob/507b16a7d3a1baa83a7c0e5df3b9b77b32eb51d5/docs/adr/ADR-0027-account-onboarding-and-magicdns.md)。

此次交付显式首次 MagicDNS、账户级第三方绑定/解绑、OIDC 邀请加入原有网络。
不把全局账户、跨租户成员关系或第三方自动开通独立租户写成已完成。

## 修改、原因与安全

没有部署域名的网络原先无法启用设备名称解析。现在由网络管理员在 DNS 页面
确认分配内部域名；命名空间、配置、历史与必需审计同事务保存，设备名称、IP、
密钥和访问规则保留。现有 Noise 流收到真实 FQDN、DNSConfig 和 Domain，使用
上游已有字段语义；基础启用/开关不收费，高级 DNS 仍走实际 Entitlement。

第三方绑定从安全中心发起，要求同一浏览器、同一人类会话，回调和提交再复核。
外部身份唯一键仍是 `(provider_id, subject)`，邮箱不合并账户。绑定不创建新
成员、不改变角色、不信任机器；解绑撤销该来源控制台会话，保护最后一种当前
部署可用的密码、通行密钥或第三方登录。提供方未配置时明确提示，不显示假绑定。

所有者的邀请可用于密码或 OIDC 注册。邀请码只在正文传递，持久认证事务保存
哈希引用；兑换时重新检查撤销、有效期、单次使用、角色与成员额度。用户、身份
链接、邀请兑换、登录会话与必需审计只有一个提交点，失败/忽略写入不签发部分
凭据。普通 OIDC 登录遵守 invite/closed，已有绑定继续登录。

旧第三方分步创建用户/身份/会话的实现已删除，不与新原子流程并行运行。Human、
Machine、Service 身份边界与设备授权协议不变。实现与配置以
[固定版本服务端说明](https://github.com/xunara-net/xunara-server/blob/507b16a7d3a1baa83a7c0e5df3b9b77b32eb51d5/docs/account-onboarding-and-magicdns.md)
为准，不在本文复制会漂移的 API 字段。

## 迁移与隔离验证

只追加 identity v14，历史认证事务默认仍是普通登录用途；state v24、plans v4
不变。空部署域名恢复持久命名空间，显式冲突域名仍拒绝；新网络不会在升级时
自动启用 MagicDNS。旧二进制不能直接读取新身份库，回退必须恢复完整旧状态。

- Go build、vet、全量普通测试全部通过；control 为 93.242 秒、identity 为 31.060 秒。
- 最终完整 `go test -race ./... -count=1 -timeout=20m` 全部通过，control 为
  1012.793 秒、identity 为 102.016 秒；新链路定向 race 另重复三轮通过。
- 覆盖身份冲突、切换/撤销发起会话、回放、邀请过期/撤销/已用/超额、跨 SQLite
  连接并发、最后登录方式、提供方停用、v13 历史事务迁移、必需审计 ABORT/IGNORE
  回滚与 MagicDNS stale/CSRF/成员权限/现有 Noise 流更新。
- 干净 Git 归档构建的 Web 189 / Admin 37 项单测、类型检查、生产构建全部通过。
- 同一干净二进制通过 61 阶段 Chromium 真实 API 回归：RSA/JWKS/PKCE、邀请、
  绑定与解绑、MagicDNS、320/390/768px，零 JavaScript 错误；不用模拟 token
  或公网测试账户冒充实际提供方。
- 官方 Tailscale 1.102.2 Linux userspace 夹具通过 API 初始化域名、同名设备、
  A/PTR、在线更名、按名称 WireGuard ICMP 与重启保留。使用临时 Relay/STUN，
  不改宿主 DNS、不写生产状态；不等于所有 OS 或宿主解析器完成验收。
- 真正已发布的 `0ab02aac3a12c129a9eb69ce5dcbebf532fa75cf` 隔离状态从 identity
  v13 升级 v14，原身份、会话、邀请、DNS、设备和 IP 保留；新密码登录与审计经
  重启保持。旧二进制拒绝新库，配套完整旧快照隔离恢复后原会话仍有效。
- 部署门禁的隔离测试确认：仅允许 identity 13→14 标记归一化；新列不掩盖旧
  地址改变、未知迁移或表缺失；不可变资产冲突不发布新首页；私密权限保持。

对应 GitHub 独立复验：
[Server CI](https://github.com/xunara-net/xunara-server/actions/runs/38094779333)、
[Web CI](https://github.com/xunara-net/xunara-web/actions/runs/38094781332)、
[Admin CI](https://github.com/xunara-net/xunara-admin/actions/runs/38094782956)、
[Docs CI](https://github.com/xunara-net/xunara-docs/actions/runs/38094784750)。
四个仓库对应上述首次发布提交的 CI 均 completed/success；Server 的完整 race
也已通过。后续默认配置兼容补丁有独立提交与验收，不用此结果替代补丁复验。

## 实际调试部署

北京时间 2026-10-11 07:27 左右，调试站从 `0ab02aa` 升至上述完整提交。发布包
来自干净归档，只含二进制与前端，不包含数据库、生产环境或任何私密凭据。
Server SHA256：`584e796f257a032cff54ecf29785c20d28e7336118b974b72c0edb05a7f98804`；
发布包 SHA256：`e72e80b97fcd1af7a57a2cac1dc60412d693102c15495e2257f1a70cdd8224c2`。

部署前与停写后逐租户执行只读 DNS 预检；维护门禁排空旧 nginx worker，停止
控制面写入，完整备份状态、平台库、配置、二进制和两个前端后才升级。新进程
健康、版本、schema、原有表全部原字段及受保护文件核对通过后恢复访问。身份
迁移标记单独校验；不忽略任何既有用户、会话、IP 或配置变化。

完整维护备份：`/root/xunara-rollback/20261010T232706Z-account-onboarding`。
这是私有运维位置，不公开提供下载；重新开放业务后禁止自动恢复旧快照，以免
覆盖新数据。故障先停止新写入并评估新的数据边界。

实际上线后的只读结果：

- default/team 租户保留，均 state v24/identity v14，plans v4；既有用户与设备
  数量保持，实际网络仍与持久分配匹配。
- Free 自定义网段的管理员覆盖保持，不用源码默认套餐覆盖现有配置。
- 未改现有账号、密码、域名、网段、IP、设备、ACL 或中继；未创建生产测试用户，
  也没有替管理员自动确认 MagicDNS 首次域名。
- 静态公共 Relay 配置、二进制与进程事实保持，没有重启；本地固定证书 TLS
  probe 返回 200，不把它当作公网双客户端数据通路验收。
- 公网 Server 完整 SHA 匹配，Web 41 / Admin 19 个文件逐一与发布清单 SHA256
  匹配；用户/管理后台登录门禁与受保护 API（含 DNS/账户身份）401 通过。
- 公网 320/390/768px 无横向溢出、零 JavaScript 错误；验证不登录、不写业务数据。

## 用户入口与剩余边界

调试用户中心：`http://fakeop4.onbed.cn:9090/login`。DNS 页面由网络管理员点击
「启用 MagicDNS」；第三方绑定在「安全中心」；邀请由所有者在「成员」创建。
具体操作见[设备名称与账户入门](../user/account-onboarding.md)。

当前公网仍是 HTTP，实际 OIDC 发行方尚未配置，所以本轮没有宣称真实生产
第三方账号可用。需要实际 issuer/client ID、服务器私密保存的 client secret、
固定 HTTPS 回调后再验收；通行密钥的公网 HTTPS 条件也未因此消失。

邮件邀请投递、全局账户跨租户加入、邮箱验证/找回、完整 2FA、域名迁移和全 OS
DNS 接管不属于本轮完成范围，继续保留在实现台账。

## 旧默认配置兼容补丁

首次上线后继续复核既有部署域名场景，真实 HTTP 回归发现：没有配置分流表时
运行时为 `null`、GET 公开为 `{}`，Free 的基础开关被误判为高级 DNS 修改，
返回 403。补丁 `5fc7e6b6fbd793a9e774e87c4725fd9556ee8057` 规范默认运行时空对象，
不放宽 Entitlement、权限、CSRF 或版本保护；旧指纹页面需要重新读取当前基线。

- 修复前 nil 配置真实复现 403；修复后 nil/空 map 两种既有部署域名关闭、开启
  均通过，既有命名空间保持。DNS 定向测试、build、vet 与全量普通测试通过，
  control 为 106.370 秒、identity 为 48.330 秒。
- 此补丁最终完整 race 通过，control 为 902.800 秒、identity 为 106.916 秒；
  DNS/绑定/邀请的专项 race 另重复三轮通过，不用首次版本的竞态结果替代。
- 从此提交再次干净归档构建，Web 189/Admin 37 单测、类型检查与构建通过；
  同一二进制再次通过 61 阶段真实浏览器与官方 Linux DNS/ICMP/重启夹具。
- 从已发布的 `507b16a` 隔离状态升级并保留原会话与数据；schema 均保持
  state v24/identity v14/plans v4，旧二进制可读取未变 schema；隔离完整旧快照
  恢复通过。部署门禁不再归一化任何迁移标记，并核对布局完全一致。
- 北京时间 07:50 左右维护升级至此补丁，完整备份为
  `/root/xunara-rollback/20261010T235028Z-dns-defaults`；原表原字段、全部 schema、
  非数据库文件、配置、套餐、租户与公共 Relay 进程保持，没有自动初始化域名。
- 更新后的公网 SHA、Web 41/Admin 19 文件清单、受保护 API、320/390/768px 与
  零 JS 错误再次验证通过；平台实际分配、Free 覆盖及本地 Relay TLS probe 保持。
- 两次上传的临时目录已按原校验和核对后删除，临时 SSH 密码文件也已删除；
  私有维护备份保留，没有清除用户状态或回退材料。

最终二进制 SHA256：`220bfcea9d59ce6bfc98752bdf00dd2db843e7fb48db7846b5a71eb417783d5b`；
补丁发布包 SHA256：`1d6d894072c3ae1ffb9f180d0eb943a40a6f35a5c579fb74d76f5ee442c62678`。
最终服务端独立复验见
[CI 38095538496](https://github.com/xunara-net/xunara-server/actions/runs/38095538496)，
head SHA 与此补丁逐字匹配，build/vet/test/完整 race 均 completed/success。
真实公网 OIDC 仍未配置，不把功能代码和隔离
发行方测试当成已经开通的第三方账号。
