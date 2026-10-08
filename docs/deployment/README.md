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
| 80 / 443 | nginx：`/` 用户控制台、`/admin/` 超管后台、控制面 API 反代 | 公网 |
| 9090 | `xunarad` HTTP（nginx 的上游） | 仅本机/容器网络 |
| 9091 | `xunara-relay` DERP，客户端直连（不经过 nginx） | 公网 |
| 3478/udp | STUN（可选） | 公网 |
| 9191 | 平台 gRPC（Bearer，fail closed） | 仅本机/内网 |

## 同源是硬要求

用户控制台使用 HttpOnly + SameSite=Lax 的会话 Cookie，**必须**与控制面 API 同源。
`nginx/xunara.conf` 已经按同源写好；不要把 `xunara-web` 单独部署到另一个域名。

## 首次初始化

全新部署没有管理员密码：用服务写出的一次性令牌（`/var/lib/xunara/setup-token`）在
`/setup` 创建 owner 账号，之后令牌文件立即删除，审计记录 `admin.bootstrap`。

## 相关文档

- 安装/升级/回滚：[xunara-deploy README](https://github.com/xunara-net/xunara-deploy/blob/main/README.md)
- 运维（备份、灾备、灰度）：[docs/operations/README.md](../operations/README.md)
- 安全前提：[docs/security/README.md](../security/README.md)
- 排障：[docs/troubleshooting/README.md](../troubleshooting/README.md)
