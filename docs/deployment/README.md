# 部署

部署产物与脚本在 [xunara-deploy](https://github.com/xunara-net/xunara-deploy)，本文只说明
拓扑与流程，具体命令以部署仓库 README 为准。

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

控制面单元带 `-trusted-proxy`：限流按 `X-Forwarded-For` 的最后一跳（nginx 追加的
真实客户端地址）计数，否则所有请求都会记在 127.0.0.1 上共享同一个桶。若把控制面
直接暴露到公网，必须去掉该开关。

## 单端口同源部署（实测路径）

主机只放行一个端口（例如 9090）时的完整流程，已在 systemd 主机上跑通：

```sh
# 1) 控制面：退到 127.0.0.1:9190，把公网端口让给 nginx
sudo systemctl stop xunarad                      # 必须先停：运行中的二进制不可覆盖
sudo XUNARA_SERVER_URL=http://host:9090 \
     XUNARA_LISTEN=127.0.0.1:9190 \
     XUNARA_GRPC_LISTEN=127.0.0.1:9191 \
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
XUNARA_EXTRA_ARGS="-org-config /etc/xunara/orgs.json \
  -platform-state-dir /var/lib/xunara/platform -plans builtin"
```

- 入口站必须 `registration=open`，否则启动报错（控制台与 API 不允许互相矛盾）。
- `*.domain_suffix` 需要泛解析到同一入口（nginx `server_name _` 已接受任意 Host）；
  新租户状态目录在 `-platform-state-dir/orgs/` 下自动创建，备份必须包含它。
- `cookie_domain` 让注册后的会话跨到租户域名；不配置则到新域名重新登录一次。
- 入口站限流 5 租户/小时/IP；删除租户走平台 API。
- 只开放非标准端口（例如 nginx 独占 9090）时必须设置 `self_service.port`，
  否则租户 URL 指向 80/443。

## 同源是硬要求

用户控制台使用 HttpOnly + SameSite=Lax 的会话 Cookie，**必须**与控制面 API 同源。
`nginx/xunara.conf` 已经按同源写好；不要把 `xunara-web` 单独部署到另一个域名。

## 首次初始化

全新部署没有管理员密码：用服务写出的一次性令牌（`/var/lib/xunara/setup-token`）在
`/setup` 创建 owner 账号，之后令牌文件立即删除，审计记录 `admin.bootstrap`。

## 中继归属

中继是独立仓库（`xunara-relay`）的进程，和 nginx / 控制面**分开**：

- 独立模式（默认）：`-verify-url http://127.0.0.1:<控制面端口>/derp/admit`，准入问
  控制面，控制面不可达即 fail closed。
- 托管模式：`-control-url` + 一次性注册令牌，中继出现在超管后台的中继列表里，
  数量受套餐 `max_relays` 限制。

它的 9091 必须由中继自己终止 TLS：客户端按 `CertName`（`sha256-raw:<证书指纹>`）
固定证书，nginx 反代会破坏指纹。迁移中继时**复制证书与 `derp.key`**，指纹就能保持不变。

## 相关文档

- 安装/升级/回滚：[xunara-deploy README](https://github.com/xunara-net/xunara-deploy/blob/main/README.md)
- 运维（备份、灾备、灰度）：[docs/operations/README.md](../operations/README.md)
- 安全前提：[docs/security/README.md](../security/README.md)
- 排障：[docs/troubleshooting/README.md](../troubleshooting/README.md)
