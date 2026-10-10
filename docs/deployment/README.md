# 部署

部署产物与脚本在 [xunara-deploy](https://github.com/xunara-net/xunara-deploy)，本文只说明
拓扑与流程，具体命令以部署仓库 README 为准。

中继配置共享版本、历史恢复与事务审计的最新验收及维护升级状态见
[中继配置验收](2026-10-10-relay-configuration-history.md)。该切片无新迁移；期望配置
下发不等于节点已经执行，具体兼容性与未完成边界以该记录为准。

## 形态

```text
单机 systemd     install.sh + systemd 单元 + nginx 同源站点
Docker Compose   server + relay + web/nginx 三个容器 + 两个具名卷
```

## 端口

| 端口 | 归属 | 暴露范围 |
|---|---|---|
| 80 / 443（或任意单一公网端口，如 9090） | nginx：`/` 用户控制台、`/admin/` 超管后台、控制面 API 反代 | 公网 |
| 9190 | `xunarad` HTTP（nginx 的**上游**） | 仅本机/容器网络 |
| 9091 | `xunara-relay` DERP，客户端直连（不经过 nginx） | 公网 |
| 3478/udp | STUN（可选） | 公网 |
| 9191 | 平台 gRPC（Bearer，fail closed） | 仅本机/内网 |

公网只暴露 nginx 一个入口：控制台、超管后台、控制面 API 因此天然同源。控制面退到
回环地址，任何客户端协议（TS2021 / Noise / DERP 准入）都经 nginx 反代进来。

安装器默认不信任转发头。控制面仅通过同机 nginx 暴露时，显式设置
`XUNARA_TRUSTED_PROXY=true`：限流按代理追加的真实客户端地址计数。直接暴露公网的
控制面保持默认关闭，避免来源地址伪造。配置以部署仓库 README 为准。

## 单端口同源部署（实测路径）

主机只放行一个端口（例如 9090）时的完整流程，已在 systemd 主机上跑通：

在 `xunara-deploy` 仓库目录执行，先准备服务端二进制、前端 dist 与中继 map。

```sh
# 1) 控制面：退到 127.0.0.1:9190，把公网端口让给 nginx
sudo systemctl stop xunarad                      # 必须先停：运行中的二进制不可覆盖
sudo XUNARA_SERVER_URL=http://host:9090 \
     XUNARA_LISTEN=127.0.0.1:9190 \
     XUNARA_GRPC_LISTEN=127.0.0.1:9191 \
     XUNARA_TRUSTED_PROXY=true \
     XUNARA_EXTRA_ARGS="-derp-map /var/lib/xunara-relay/derp.json" \
     ./install.sh /tmp/xunarad

# 2) 前端：nginx 占公网端口，上游指向 9190
sudo XUNARA_HTTP_PORT=9090 XUNARA_UPSTREAM=127.0.0.1:9190 \
     ./install-web.sh /tmp/web-dist /tmp/admin-dist

# 3) 超管后台与平台 API 需要部署令牌（0600，不进命令行）
sudo sh -c 'printf "XUNARA_PLATFORM_ADMIN_TOKEN=%s\n" "$(openssl rand -hex 32)" \
     >> /etc/xunara/xunarad.env'
sudo systemctl restart xunarad
```

验收（全部应通过）：

```sh
curl -s http://127.0.0.1:9190/health                     # {"status":"pass"}
curl -sI http://127.0.0.1:9090/                          # 用户控制台 index.html
curl -sI http://127.0.0.1:9090/admin/                    # 超管后台 index.html
curl -s -o /dev/null -w '%{http_code}\n' http://127.0.0.1:9090/api/v1/overview   # 401
```

上线实测中踩过的坑，按出现顺序记在这里：

- **必须 `systemctl stop xunarad` 再覆盖二进制**，否则 `install` 报 `Text file busy`。
- 控制面搬家后，中继的 `-verify-url` 要跟着改（例如 9090 → 9190），否则 DERP 准入
  全部失败；托管模式（`-control-url`）同理。
- `/admin/` 曾因 nginx `location` 继承 server 级 `root`（`/srv/xunara/web`）导致
  `/admin/index.html` 内部重定向死循环（500）；模板里已显式 `root /srv/xunara;`。
- `/login` 的 GET 属于控制台 SPA，POST 才是控制面的旧版表单登录；两者都要留。
- 若开了套餐（`-plans builtin`），内置 Free 的 `max_users=1`：单租户部署里
  第二个账号注册会被 `USER_LIMIT_REACHED` 挡住。自托管不加 `-plans` 即无配额，
  联网售卖时用超管后台把租户调到 Pro/Business。
- `/console` 是控制面内嵌的旧版控制台，仍然可用；正式入口是 `/` 与 `/admin/`。

## 多租户与自助注册

注册策略由 `-registration` 决定：`closed`（只允许管理员建号）、`invite`（邀请码，
默认）、`open`（任何人可注册，spec §55）。单租户部署的开放注册得到的是本租户
`member`；托管部署要走「注册即开独立 tailnet」，需要三件套一起配：

```json
{
  "organizations": [
    {"id": "portal", "name": "Xunara Cloud", "domains": ["app.example.com"],
     "server_url": "https://app.example.com", "state_dir": "/var/lib/xunara/portal",
     "registration": "open"}
  ],
  "self_service": {
    "site": "portal",
    "domain_suffix": "tailnet.example.com",
    "scheme": "https",
    "port": "9090",
    "cookie_domain": "example.com",
    "plan": "free"
  }
}
```

```sh
sudo XUNARA_ORG_CONFIG=/etc/xunara/orgs.json \
     XUNARA_LISTEN=127.0.0.1:9190 XUNARA_TRUSTED_PROXY=true \
     XUNARA_MANAGED_DERP_MAP=/var/lib/xunara-relay/derp.json \
     XUNARA_EXTRA_ARGS="-plans builtin -network-pool 100.100.0.0/16" \
     ./install.sh /tmp/xunarad
```

在 `xunara-deploy` 仓库执行；组织配置和已有公共中继 map 必须已存在。安装器使用
`XUNARA_STATE` 作为平台状态根，自动选择多租户参数，不混入单租户启动选项。
不要通过 `XUNARA_EXTRA_ARGS` 追加 `-org-config`。中继准入 URL 与恢复规则见
[部署仓库的多租户章节](https://github.com/xunara-net/xunara-deploy/blob/main/README.md#多租户与自助注册)。

- 入口站必须 `registration=open`，否则启动报错（控制台与 API 不允许互相矛盾）。
- `*.domain_suffix` 需要泛解析到同一入口（nginx `server_name _` 已接受任意 Host）；
  新租户状态目录在 `-platform-state-dir/orgs/` 下自动创建，备份必须包含它。
- `cookie_domain` 让注册后的会话跨到租户域名；不配置则到新域名重新登录一次。
- 入口站限流 5 租户/小时/IP；删除租户走平台 API。
- 旧入口本地注册不会创建公共 tailnet 成员；控制台必须使用自助开通流程。
- 托管租户的公共中继只来自显式部署配置，不继承其他租户的私有 map 或身份数据。
- 只开放非标准端口（例如 nginx 独占 9090）时必须设置 `self_service.port`，
  否则租户 URL 指向 80/443。

`nip.io` 等绑定 IP 的临时域名仅适合调试。公网 IP 改变时，旧租户地址也会失效；
修改自助入口的域名后缀只影响新开通地址，不会自动改写已有客户端的控制服务器地址。
正式部署应使用可维护泛解析的稳定域名，并配置 HTTPS；不要把 HTTP 调试站作为生产站。

### 验收记录（2026-10-09）

已在本次调试部署验证：

- 浏览器自助注册后进入独立租户，owner、Free 额度与自动分配网段正确显示。
- 账号、套餐、活动会话与审计字段正常渲染；移动端无横向溢出或 JavaScript 页面错误。
- 官方 Linux 客户端 1.104.1 接入两个租户的三台设备，同租户发现对等节点，另一租户
  不可见；租户会话不能读取其他租户设备，也不能调用平台管理 API。
- 禁用测试客户端 UDP 直连后，经部署的 DERP 完成加密网络内的 HTTP 数据传输。
- 控制面重启保留组织、套餐、网段和设备；原客户端不需要新预授权密钥即可重连并继续
  通过中继传输。验收租户随后归档，原有组织及设备数据保留。

服务端构建、静态检查、全量与竞态测试，以及前端构建与响应契约测试通过。此次实测
覆盖 Linux 和浏览器，不代表 Windows、macOS、Android、iOS、直连与中继故障转移矩阵
已全部完成；完整兼容矩阵仍须单独验收。

### 账户自助验收（2026-10-09）

部署版本：服务端
[`ccb479f`](https://github.com/xunara-net/xunara-server/commit/ccb479f)，用户控制台
[`0d126f1`](https://github.com/xunara-net/xunara-web/commit/0d126f1)。

- 浏览器保存昵称及联系邮箱后即时更新展示，登录名、角色和所属组织不变。
  未携带 CSRF 的资料写请求拒绝；跨租户人类 Session 不能读取账户。
- 新密码确认不一致由页面阻止；当前密码错误不退出已有会话。正确改密后两个
  浏览器会话均失效，旧密码拒绝、新密码可登录，残留父域 Cookie 不遮蔽新登录。
- 改密前已经连接的两台官方 Linux 客户端 1.104.1 保留地址，改密后仍可通过
  强制 DERP 中继完成加密网络内的 HTTP 数据传输。
- 控制面重启后保留资料、新密码、新登录会话、套餐、网段及设备。两台原客户端
  无需新预授权密钥即可重连，中继数据传输继续成功。
- 桌面卡片对齐，390px 移动页面无横向溢出；浏览器无 JavaScript 页面错误。
  测试租户随后归档，原有 `default` 与 `team` 租户及其数据保留。

服务端 `go build`、`go vet`、全量测试与全量 `-race` 测试通过；前端 35 项测试、
类型检查及生产构建通过。原子提交、审计故障回滚和跨数据库连接的改密/登录/轮换
竞争由自动化测试覆盖。接口规则以
[服务端账户说明](https://github.com/xunara-net/xunara-server/blob/main/README.md#账户自助管理)
与 [ADR-0009](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0009-account-self-service.md)
为准。此次仍是 HTTP 调试环境，不代表 HTTPS、邮箱验证、密码找回或 2FA 已完成。

### 控制台登录管理验收（2026-10-09）

部署版本：服务端
[`e2068ac`](https://github.com/xunara-net/xunara-server/commit/e2068ac)，用户控制台
[`6edb417`](https://github.com/xunara-net/xunara-web/commit/6edb417)。升级前备份二进制、
静态入口和停止服务后的状态目录；升级不改组织配置、网段或中继证书指纹。

- 升级前创建的三个浏览器登录在升级后仍可使用；Free 账户可自助退出单个、
  其他及全部登录。“其他”实际退出两个并保留当前登录，“全部”实际退出三个，
  当前浏览器返回登录页；退出当前登录也显示明确结果。
- 缺失或错误 CSRF 被拒绝；跨租户令牌不能读取会话，其他租户的会话标识不能
  被撤销。另一个临时租户的登录不受单个、其他和全部退出影响。
- 取消确认不提交退出；页面注入列表读取和撤销失败时明确报错，刷新可恢复，
  不显示为零活动登录或操作成功。安全概览读取失败也单独显示，不伪造正常状态。
- 活动与失效记录分开，中文卡片替代原始 JSON；390px 页面无整体横向溢出，
  浏览器无 JavaScript 页面错误。重新登录时失效的父域 Cookie 不遮蔽新主机 Cookie。
- 两台官方 Linux 客户端 1.104.1 在退出登录后保留地址，并继续通过强制 DERP
  完成加密网络内的 HTTP 传输。首次冷启动数据探测曾超时，客户端重连后复测通过；
  之后的退出操作与重启回归传输均通过，未修改客户端协议。
- 控制面重启后，当前有效登录、失效状态与原因、另一个租户的登录均保持；
  原有设备、Free 配额和网段保持，两台客户端无需新预认证密钥即可重连并传输。
- 两个临时测试租户随后归档，临时密码、会话 Cookie、预认证密钥及客户端状态
  从测试端清理，原有 `default` 与 `team` 租户和数据保留。

服务端构建、vet、全量测试及全量 `-race` 通过；前端 46 项测试、类型检查与
生产构建通过。事务审计故障回滚、失效发起者拒绝及跨数据库连接的撤销/轮换竞争
由自动化测试覆盖。接口以
[服务端登录管理说明](https://github.com/xunara-net/xunara-server/blob/main/README.md#控制台登录管理)
与 [ADR-0010](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0010-account-session-revocation.md)
为准。本记录不代表完整登录审计、来源设备元数据、2FA、HTTPS 或全平台兼容矩阵
已经完成；当前仍是 HTTP 调试部署。

## 同源是硬要求

一次性初始化、独立租户 owner 开通与登录配置故障恢复的最新发布状态见
[一次性初始化验收](2026-10-10-atomic-owner-bootstrap.md)。本轮追加身份 v13；旧版本
不能直接读取新版数据库。回退须在恢复公网写流量前同时恢复旧产物和完整一致性
状态，不得仅替换旧二进制，也不得在线用旧快照覆盖已接收新业务的状态。

新旧密码入口的故障收敛、验证及发布状态见
[密码登录验收](2026-10-09-password-login-consolidation.md)。此切片不改前端静态产物、
套餐或客户端协议，仍需服务端提交的最终 CI 和可回滚升级验收。

正式第三方认证入口、成员邀请与自助入口租户门禁的最新版本和调试升级见
[认证与成员邀请验收](2026-10-09-browser-auth-member-invitations.md)。先升级服务端再
部署用户 Web；邀请码与注册页地址分开发送，自助入口不用于邀请共享成员。
本地 OIDC 夹具通过不代表本站已配置公网第三方提供方或正式 HTTPS。

认证故障、中继管理、注册原子性、成员/路由页面梳理和本轮调试升级见
[认证与中继审查验收](2026-10-09-authentication-relay-admin.md)。该记录明确自动化、
浏览器、只读公网探测与未完成事项的边界，不代表所有规格功能或 HTTPS 已交付。

通行密钥迁移、账户认证收敛与对应调试部署的最新版本、升级保护及实测边界见
[2026-10-09 验收记录](2026-10-09-passkey-account-consolidation.md)。公网 HTTP 不能
使用通行密钥；本地虚拟认证器验收不等于实体设备或生产 HTTPS 已完成。

用户控制台使用 HttpOnly + SameSite=Lax 的会话 Cookie，**必须**与控制面 API 同源。
`nginx/xunara.conf` 已经按同源写好；不要把 `xunara-web` 单独部署到另一个域名。

## 首次初始化

全新部署没有管理员密码：用服务写出的 `0600` 一次性证明（默认状态目录下的
`setup-token`）在 `/setup` 认领内置 owner。完成事实、资料、密码、会话及必需审计
同事务提交，成功后清理证明文件；限流或存储故障不留下半初始化，可在恢复后重试。
已完成的初始化不会因删除密码、遗留证明或重启而重新开放；`/setup` 不是密码重置。
启动无法确认初始化状态或安全发布证明时拒绝启动。不要打印证明或改权限绕过检查，
行为以 [ADR-0017](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0017-atomic-owner-bootstrap.md) 为准。

## 中继归属

中继是独立仓库（`xunara-relay`）的进程，和 nginx / 控制面**分开**：

- 独立模式（默认）：`-verify-url http://127.0.0.1:<控制面端口>/derp/admit`，准入问
  控制面，控制面不可达即 fail closed。多租户公共池使用平台准入地址，见
  [ADR-0008](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0008-managed-relay-admission.md)。
- 托管模式：`-control-url` + 一次性注册令牌，中继出现在超管后台的中继列表里，
  数量受套餐 `max_relays` 限制。

它的 9091 必须由中继自己终止 TLS：客户端按 `CertName`（`sha256-raw:<证书指纹>`）
固定证书，nginx 反代会破坏指纹。迁移中继时**复制证书与 `derp.key`**，指纹就能保持不变。

## 相关文档

- 安装/升级/回滚：[xunara-deploy README](https://github.com/xunara-net/xunara-deploy/blob/main/README.md)
- 运维（备份、灾备、灰度）：[docs/operations/README.md](../operations/README.md)
- 安全前提：[docs/security/README.md](../security/README.md)
- 排障：[docs/troubleshooting/README.md](../troubleshooting/README.md)
