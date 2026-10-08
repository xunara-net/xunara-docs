# 运维

## 备份

| 数据 | 位置 | 说明 |
|---|---|---|
| 控制面状态 | `/var/lib/xunara` | 节点、用户、Session、预认证密钥、审计、策略快照、Flux 密文 |
| 中继状态 | `/var/lib/xunara-relay` | DERP 节点密钥、证书、`derp.json`（指纹） |
| 平台 secret | `/etc/xunara/xunarad.env` | 0600，单独备份到密钥管理 |

备份前先 `systemctl stop xunarad` 保证一致；恢复后先 `-version` 校验再启动。

## 灾备（补充规范 §90、§91）

- 定期演练恢复：备份不可恢复等于没有备份。
- Headscale 密钥与控制面 Session 密钥必须随状态目录一起备份，否则会出现"数据在、
  登录态全失效 / 网络重建"。
- Relay 状态丢失需要重新下发指纹（`derp.json` 的 `CertName`）。

## 升级与灰度（补充规范 §97、§98）

- 先升级控制面，再升级中继；中继保持向后兼容的注册协议。
- 灰度按租户或按中继分批，观察错误率、DERP 延迟、登录成功率后再全量。
- 回滚：部署仓库保留 `xunarad.previous`；状态格式不兼容时同时回滚状态备份。
- 数据库迁移只能追加，已发布条目不可修改。

## 兼容矩阵（补充规范 §54）

`xunara-server` 与 `xunara-relay` 各自 SemVer；发布时标注两者兼容区间，并在
Release Notes 中给出最低/最高支持版本。官方客户端兼容性以补充规范 §68 的兼容测试
为准。

## 监控与告警（补充规范 §32–§34、§112–§113）

- 健康：`/health`（控制面）、中继心跳与健康评分。
- 指标：登录成功率、TS2021 握手失败率、MapRequest 延迟、DERP 流量与丢包、设备
  注册失败原因分布。
- 告警：控制面不可达、中继摘除、平台 API 401 激增、设备上限拒绝异常升高、
  审计写入失败。

## 观测面

- 日志：journald（`journalctl -u xunarad -f`、`-u xunara-relay -f`），不得输出 Secret。
- 审计：控制台「审计」页与 `/api/platform/v1/audit/actions`。
- Webhook/事件中心（补充规范 §111–§114）：关键事件推送与订阅。
