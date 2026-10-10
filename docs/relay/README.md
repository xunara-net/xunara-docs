# 中继平台（Relay）

Xunara Relay 不是"简单的 derper 二进制"，而是 **Xunara Network Edge**（补充规范 §121）：
DERP、STUN、Peer Relay、流量控制、QoS、限速、指标、健康、远程管理、自动更新、故障转移
都属于它的长期范围，因此独立成仓。

## 中继类型（补充规范 §8–§13）

| 类型 | 说明 | 归属 |
|---|---|---|
| Global Relay | 平台自建，所有用户可用 | Xunara |
| Platform Relay | 平台为特定区域/套餐提供 | Xunara |
| Private Relay | 用户/组织自建，私有 Tailnet 使用 | 组织 |
| Community Relay | 社区贡献，按策略开放 | 第三方 |

## 生命周期（补充规范 §14–§17）

```text
未注册 → 提交一次性 Relay Token → 注册（Enroll）→ 获得 Relay Identity
      → 心跳 / 远程配置 / 流量上报 → 摘除 / 退役
```

- **Relay Identity**：注册后落盘（0600），长期凭证；丢失需重新注册。
- **Relay Token**：一次性，只在首次注册时使用，可限定归属与可见性。
- 控制面不可达时，公开中继 fail closed，不成为开放中继。

协议契约（服务端与中继共同的接口定义）在
[xunara-relay/docs/relay-protocol.md](https://github.com/xunara-net/xunara-relay/blob/main/docs/relay-protocol.md)：
`POST /api/relay/v1/enroll`、`POST /api/relay/v1/heartbeat`、状态机与错误码。

## 运行形态

```text
独立模式    -verify-url 指向控制面 /derp/admit：按节点准入，控制面不可达即拒
托管模式    -control-url + 一次性 enroll token：注册、心跳、拉取远程配置
```

部署、端口（9091 DERP、可选 3478/udp STUN）与升级见
[xunara-deploy](https://github.com/xunara-net/xunara-deploy/blob/main/README.md)。

## 限速、流量与隐私（补充规范 §26–§31）

- 限速必须区分方向（上传/下载分别计量），并支持按套餐与租户的策略。
- 流量统计只保留计费与运维所需的最小维度，不做 DPI、不解析用户负载。
- 健康评分与自动摘除基于心跳、延迟、错误率、带宽水位；摘除要可回滚并可审计。

## 配置与升级（补充规范 §35–§40、§93–§98）

- 远程配置带版本与历史恢复。新版托管中继持久化身份绑定的高水位/撤销缓存；
  新进程先确认控制面授权，不能凭缓存开放 DERP；运行中控制面故障保持当前配置和既有连接。
- 升级走 Release Channel（stable/beta），支持灰度与自动更新。
- Relay 软件需签名校验；镜像多架构（amd64/arm64）。

## 用户文档清单（补充规范 §101）

私有 Relay 必须提供：硬件要求、系统要求、网络要求、端口要求、安装（Binary / Docker /
Systemd）、注册、配置、升级、卸载、故障排查。

## 管理页面（补充规范 §18–§20）

用户控制台提供中继列表、拓扑与地图、自动选择；超管后台提供中继审批、限速、可见性、
区域/分组、成本与调度视图。

## 当前状态

`xunara-relay` v0.1 已实现 DERP/STUN 数据面、自签名证书与 DERP map 生成、准入
fail closed、限速、托管注册与心跳客户端；`xunara-server` 已实现 `/api/relay/v1/enroll`
与 `/api/relay/v1/heartbeat`、期望状态/限速/区域名下发、`plan.MaxRelays` 配额
（Free 1 / Pro 5 / Business 20）以及租户与平台两级中继管理 API（ADR-0006）。
两个后台已接入托管中继列表、一次性令牌、配置、删除、CAS/历史恢复与持久执行回执；
Relay 实际热更每连接双向限速、维护拒新、停用断连/恢复及终态撤销。使用上游真实
DERP 连接/字节计数，不伪造连接质量。旧 Relay 无报告则执行未知；服务自报不是
端到端证明。方向/全局/地区/租户/用户/设备额度、公共跨租户发布、成本账本、签名
自动升级/灰度与全 OS 实测仍未交付。最近心跳计数也不是可计费用量账本。详见
[超管手册](../admin/README.md)与[实现台账](../developer/implementation-status.md)。
