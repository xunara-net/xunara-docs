# HTTP / HTTPS 共用入口验收

日期：2026-10-11。范围：systemd 测试站的 nginx 边缘入口和前端安装器。
这不是整个产品完成声明，也不是新数据库、身份或官方客户端协议实现。

## 交付

HTTP 与 HTTPS 共用一个 Web / Admin / Core 和数据源，正式业务仅 HTTPS 受理。
同端口 HTTP 安全页面导航跳同租户同路径；未知 Host、API / 回调 / 协议路径、
写方法、query、认证头、Cookie、CSRF、Upgrade 与请求体明确拒绝。不运行两套
登录，不把 HTTP 和 HTTPS 浏览器源视为同源或共享明文 Cookie。

部署仓库增加单一 renderer，安装器已有站点默认保留 TLS / 定制配置；显式渲染
严格校验，私有备份、同文件系统原子替换、先校验后复制静态、重载失败返回错误
并恢复原配置。不再维护复制的 HTTPS locations，不以忽略 reload 失败伪装成功。
操作、环境变量及失败边界以
[Deploy README](https://github.com/xunara-net/xunara-deploy/blob/main/README.md)、
[nginx 手册](https://github.com/xunara-net/xunara-deploy/blob/main/nginx/README.md)和
[ADR-0034](https://github.com/xunara-net/xunara-deploy/blob/main/docs/adr/ADR-0034-http-https-entry.md)为准。
提案先于实现，跟踪为 [Deploy issue #1](https://github.com/xunara-net/xunara-deploy/issues/1)。

## 产物与兼容

入口实现来源：Deploy `92264a06e60e988e096c02c49e082e2ebbaea524`，干净 git archive
的生产 renderer 生成两个片段，并校验 payload SHA-256 后执行。其
[CI](https://github.com/xunara-net/xunara-deploy/actions/runs/38152048378) 全绿才更新原站。

原站应用未替换：Server `0ad7c29725ae706f309795e1a0987032d42e6f52`、
Web `bab79969e1b7086552d0afc7f7ea7f94e49f89dd`、
Admin `bc0056dd5b4ba21be382d47f8f5ee678153a73d4`。
没有 Go / 前端业务源码改动，不把上一轮全量 Go / race / 前端测试冒充本轮重跑。

identity v18 / state v24 / plans v4 保持，无数据库迁移、Core API、套餐、身份
映射或 Headscale Adapter 改动。HTTPS TS2021 / Noise / Upgrade 保持，DERP
直连、证书与 pin 独立。HTTP API 原先会跳转，现在固定拒绝；客户端必须直接
使用 HTTPS 并正确信任测试 CA，不承诺旧 HTTP 客户端无感切换。

## 隔离验证

- 真实生产 renderer、默认 HTTP / HTTPS、443 标准 Host、IPv6 upstream，24 类
  非法输入失败且无输出；不复制测试专用渲染逻辑。
- 真实 nginx 同端口 TLS 校验、显式租户/IPv4/IPv6/大小写导航、未知 Host 和
  转发头伪造拒绝；API/回调/query/方法/认证头/Cookie/CSRF/Upgrade/非零长度/
  分块传输拒绝。明文后端请求为零，无 Location / 会话下发。
- HTTPS 用户/管理员 SPA、后端 Host/scheme/方法/请求体转发保持。
- 安装器原 TLS 字节/权限保留、旧静态清理、非法输入不修改、真实 `nginx -t`
  错误和 reload 失败恢复、私有备份、symlink 保护及新站引导，共 16 阶段通过。
  只有 systemd 调度用隔离 fixture，不混称为生产 systemd 验收。
- `sh -n`、真实 ShellCheck、HTTP / Docker 模板 `nginx -t`、Compose config 与
  `git diff --check` 通过；没有修改原 Docker 模板。

## 原站只读验收与数据保留

原自签 HTTPS 测试站只更新 HTTP guard：删除旧 unknown Host fallback / 子域
通配跳转 map，登记六个已存在的精确 origin；保留证书、CA 下载、全部原代理
locations / 前端 / 上游配置。nginx 校验成功后真实 reload，Core、Relay 与 nginx
master 不重启。没有执行安装器静态复制，没有登录真实人类账户或提交业务写入。

私有 nginx 回退目录为 `/root/xunara-rollback/20261011T154241Z-http-https-entry`，
目录 0700、原配置 / 清单 / 不可变摘要 / 日志 0600。备份只服务这次边缘配置回退，
不是数据库灾备快照；失败仅恢复 nginx，绝不覆盖正在使用的旧数据库快照。

- 公网 44 个 HTTP 探测、六个已登记 origin：安全导航 308；未知/错误端口/
  未登记子域、明文 API/回调/协议/query/写方法/凭据/body/分块请求 400，
  不跟随失败跳转，不发送真实密码/令牌。
- 正常验证 CA、域名及 TLS 1.2/1.3，健康/version 正确；team Host 的提供方只读
  API 可达，本人私人 API 匿名 401。原 Web 45、Admin 22 个当前发布文件 SHA-256
  逐项核对通过，无静态资源替换。
- Chromium 新匿名上下文验证 HTTP→HTTPS 登录、私人页面门禁和管理员入口，
  320/390/768/1440 宽度没有横向溢出或页面异常，无浏览器 API 写入。证书信任
  限定原服务 SPKI；另外独立 HTTPS 请求完整验证 CA 与域名，不全局禁用校验。
- 官方上游 `controlhttp` 的 HTTPS key、TS2021 / Noise Upgrade、early payload、
  HTTP/2 未知节点拒绝通过；注册设备数为零，不等于 WireGuard 数据面实测。
- 初次及最终复核：132 个受保护文件字节/归属/权限、108 张人类/认证表不可变
  事实、43 个原会话凭据/生命周期和 24 条原登录历史保持。分钟活动单独允许合法
  单调更新，本轮观测为零；Core、Relay 与 nginx master 进程事实保持，schema 不变。

入口仍为 `https://fakeop4.onbed.cn:9090/login`，管理员为 `/admin/login`。
测试 CA 不是公网受信任证书；浏览器/客户端应通过可信渠道核对并安装公有 CA。
HTTP 地址仅用于安全导航，不能拿来提交登录、初始化令牌或 API 凭据。

## 剩余边界

本轮未实现公网 CA / 自动续期、HSTS、完整 Compose TLS、多实例或整套静态/
数据库自动回退；新租户 HTTP 导航仍需显式登记 origin，HTTPS 自助开通保持。
邮箱验证 / 邮件恢复、完整 2FA、订阅/支付/账单等产品缺口继续以
[实现台账](../developer/implementation-status.md)为准，不能从本切片推导全部完成。
