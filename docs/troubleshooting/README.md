# 排障手册

先收集三件事实：**控制面进程状态**、**`/health` 返回**、**nginx/上游日志**。

## 常见问题

| 现象 | 排查 |
|---|---|
| 浏览器 502 / 空白页 | `systemctl status xunarad`；`curl -fsS http://127.0.0.1:9090/health`；确认 nginx 上游端口与单元一致 |
| 登录后立刻掉线 | 控制台必须与 API 同源（Cookie SameSite=Lax）；检查是否把 `xunara-web` 部署到了别的域名 |
| 登录报 OIDC 回调错误 | `-server-url` 与浏览器地址不一致；检查 OIDC 回调 allowlist 与 clock skew |
| `/admin/` 404 | 未安装 admin dist（`install-web.sh` 第二个参数），或 nginx 的 `/admin/` location 被覆盖 |
| 客户端一直「连接中」/ `Starting` | netmap 中没有可用 DERP：检查 `-derp-map`、9091 公网可达、`derp.json` 指纹是否最新 |
| 新建租户客户端没有中继 | 检查显式公共池配置与平台准入地址，见 [多租户部署](https://github.com/xunara-net/xunara-deploy/blob/main/README.md#多租户与自助注册)；静态组织仍需自身 map |
| 中继准入返回 404 | 多租户按 Host 路由，旧租户地址不能直接用回环 Host 调用；公共池改用平台准入地址并启用公共 map |
| 套餐、登录名、会话或审计字段空白 | 前端可能仍为旧构建，缺少按端点的响应转换；升级 web dist，保留服务端原有 API 契约 |
| 设备注册被拒 | 超出套餐设备上限（`DEVICE_LIMIT_REACHED`）；或注册审批未通过（控制台「我的设备」） |
| 平台 API 401/403 | 401 为令牌错误；403 也可能是平台未启用、权限或套餐限制，不必清理仍有效的令牌 |
| 控制台「暂时无法确认登录」 | 检查网络与认证存储；地址/Cookie 保留，恢复后重试，不用重复注册或清数据 |
| 登录页「暂时无法加载登录配置」 | 配置读取或响应校验失败时入口保持关闭；恢复服务后点击重试，不按默认值强行开放注册或第三方登录 |
| 初始化暂时不可用或启动拒绝初始化 | 核对认证数据库、持久限流和状态目录权限；不清状态、不替换异常证明文件，也不把删除密码当作重置初始化 |
| 中继列表为空 | 只统计平台注册的托管中继，静态公共 DERP map 不在列表中；不能据此认定没有可用中继 |
| 权限不生效 | 规则必须最终经 Policy Compiler；检查是否只改了可视化层未提交，或 Route/Permission 用错 |
| 升级后二进制没变 | 运行中的二进制被 systemd 占用：先 `systemctl stop xunarad` 再安装 |
| 回退旧版本提示 schema 过新 | 只替换二进制不能回退身份 v13；按[受控恢复](../operations/README.md)处理，禁止在线覆盖已接收新业务的数据库 |
| 中继启动即退出 | 中继 fail closed：控制面不可达或准入被拒；`journalctl -u xunara-relay -n 50` |

## 日志与诊断

```sh
journalctl -u xunarad -n 200 --no-pager
journalctl -u xunara-relay -n 200 --no-pager
curl -fsS http://127.0.0.1:9090/health
curl -fsS http://127.0.0.1:9090/version
nginx -t && tail -n 100 /var/log/nginx/error.log
```

## 取证注意

日志与工单里不要粘贴：节点密钥、预认证密钥、Session Cookie、Relay 身份文件、
`setup-token`、平台令牌。复制前先脱敏。
