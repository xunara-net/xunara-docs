# Xunara AI 开发规范补充

> 本文件是 `AI_DEVELOPMENT.md` 的补充章节。
>
> 本章重点解决：
>
> - GitHub Organization 多仓库管理
> - 服务端 / Web / Admin / Client 分仓
> - Xunara Relay 中继平台
> - 官方 DERP 兼容
> - Xunara 自营中继
> - 用户私有中继
> - 超级管理员全局中继
> - 中继限速
> - 中继流量统计
> - 中继套餐
> - 中继健康检查
> - 中继自动注册
> - 中继远程管理
> - 中继程序自动升级
> - 中继故障转移
> - 未来网络节点生态
> - GitHub CI/CD
> - 版本管理
> - 安全供应链
> - 灾备与数据恢复
> - 运营、计费、审计和合规
>
> 所有 AI 在涉及这些模块时，必须同时阅读本文件与主 `AI_DEVELOPMENT.md`。

---

# 1. GitHub Organization

Xunara 必须使用 GitHub Organization 作为整个项目的代码与协作中心。

推荐：

```text
github.com/Xuanra
```

如果实际组织名称已经确定，则统一使用实际 Organization 名称。

原则：

```text
一个 Organization
多个职责明确的 Repository
```

禁止：

```text
一个超级大仓库
所有代码全部塞在 monorepo
```

也禁止：

```text
每个小功能一个仓库
```

仓库数量必须围绕产品边界划分。

---

# 2. GitHub Repository 总体规划

推荐：

```text
xunara/
```

Organization 下：

```text
xunara-server
xunara-web
xunara-admin
xunara-api
xunara-client
xunara-relay
xunara-relay-installer
xunara-cli
xunara-sdk
xunara-docs
xunara-deploy
xunara-infrastructure
xunara-policy
xunara-network-tools
xunara-community
```

但第一阶段不要全部创建。

MVP 推荐首先建立：

```text
xunara-server
xunara-web
xunara-admin
xunara-relay
xunara-deploy
xunara-docs
```

以后逐步增加。

---

# 3. Repository 职责

## 3.1 xunara-server

核心后端。

负责：

```text
Identity
User
Organization
Tailnet
Device
Network
Policy
Entitlement
Billing
Audit
API
Headscale Adapter
Relay Manager
```

不负责：

```text
Web UI
Admin UI
Xunara Client UI
```

---

# 4. xunara-web

普通用户 Web Console。

负责：

```text
登录
注册
用户中心
Tailnet
设备
网络
拓扑
权限
套餐
账单
API
设置
```

不允许直接访问：

```text
Headscale
Database
Relay Node
```

全部通过：

```text
Xunara API
```

---

# 5. xunara-admin

超级管理员后台。

负责：

```text
用户
Tailnet
设备
套餐
订阅
中继
网络池
DERP
系统
审计
运维
```

Admin 与普通 Web Console 必须分离。

---

# 6. xunara-relay

这是非常重要的新仓库。

定位：

```text
Xunara Relay Agent / Relay Server
```

负责：

```text
DERP
STUN
Relay
Traffic Control
Bandwidth Limit
Metrics
Health
Registration
Remote Configuration
```

必须同时考虑两种运行模式：

```text
Xunara Managed Relay
Private Relay
```

---

# 7. xunara-relay 的设计目标

用户下载：

```text
xunara-relay
```

然后在自己的服务器执行安装。

例如：

```text
curl ...
```

或者：

```text
wget ...
```

安装完成：

```text
xunara-relay install
```

输入：

```text
Xunara Relay Token
```

完成：

```text
服务器
   ↓
Xunara Relay Agent
   ↓
Xunara Control
   ↓
注册
```

---

# 8. 中继类型

Xunara 必须区分至少四种 Relay。

```text
1. Global Relay
2. Platform Relay
3. Private Relay
4. Community Relay
```

---

# 9. Global Relay

由超级管理员部署。

例如：

```text
日本东京
中国香港
中国上海
中国广州
新加坡
美国
德国
```

这些中继属于：

```text
Xunara Platform
```

可以：

```text
全局启用
全局禁用
限制区域
限制套餐
限制带宽
查看流量
查看用户
```

---

# 10. Platform Relay

属于 Xunara 自己，但可能：

```text
某个地区
某个机房
某个线路
某个运营商
```

例如：

```text
Xunara JP-01
Xunara JP-02
Xunara HK-01
Xunara SG-01
```

支持：

```text
Region
ISP
ASN
IPv4
IPv6
线路标签
成本
带宽
```

---

# 11. Private Relay

用户自己部署。

例如：

```text
用户购买 VPS
        ↓
安装 Xunara Relay
        ↓
绑定自己的 Xunara Tailnet
        ↓
成为私有中继
```

私有中继默认：

```text
仅服务该用户/组织
```

不能被其他用户使用。

---

# 12. Private Relay 权限

用户可以设置：

```text
私有
共享给组织
共享给指定用户
共享给指定 Tailnet
```

例如：

```text
家庭 Relay
```

只服务：

```text
我的 Tailnet
```

企业 Relay：

```text
公司 Tailnet
```

---

# 13. Relay Ownership

数据库必须记录：

```text
Relay
├── owner_type
├── owner_id
├── organization_id
├── tailnet_id
└── visibility
```

例如：

```text
owner_type:
platform

owner_id:
xunara
```

或者：

```text
owner_type:
user

owner_id:
USER-123
```

或者：

```text
owner_type:
organization

owner_id:
ORG-123
```

---

# 14. Relay 生命周期

每一个 Relay 都必须有状态。

```text
Pending
Registering
Online
Degraded
Offline
Disabled
Revoked
Updating
Maintenance
```

不能只使用：

```text
Online / Offline
```

---

# 15. Relay 注册流程

推荐：

```text
管理员/用户创建 Relay
        ↓
Xunara 生成一次性 Enrollment Token
        ↓
用户下载 Relay
        ↓
安装
        ↓
relay register
        ↓
Relay 验证 Token
        ↓
生成长期身份
        ↓
向 Xunara 注册
        ↓
Token 失效
        ↓
Relay Online
```

---

# 16. Relay Identity

Relay 必须拥有自己的：

```text
Relay ID
Relay Key
Certificate
Credential
```

不要每次连接都使用普通用户 Token。

推荐：

```text
Enrollment Token
        ↓
短期注册凭证

Relay Identity
        ↓
长期运行凭证
```

---

# 17. Relay Token

Token 必须支持：

```text
一次性
过期时间
绑定 Relay
绑定用户
绑定组织
绑定区域
```

例如：

```text
xrl_enroll_xxxxxxxxx
```

---

# 18. Relay 管理页面

普通用户：

```text
我的网络
 └── 我的中继
```

显示：

```text
Relay 名称
地区
公网 IP
IPv4
IPv6
在线状态
延迟
带宽
当前连接
流量
版本
最后心跳
```

---

# 19. 超级管理员 Relay 页面

Admin：

```text
Relay Center
```

显示所有：

```text
Global Relay
Platform Relay
Private Relay
Community Relay
```

支持：

```text
搜索
地区
国家
运营商
ASN
IPv4
IPv6
在线状态
版本
流量
带宽
Owner
Tailnet
```

---

# 20. Relay 拓扑

管理员可以看到：

```text
                   Xunara Control
                         │
       ┌─────────────────┼─────────────────┐
       │                 │                 │
   Tokyo Relay       Shanghai Relay     HK Relay
       │                 │                 │
    Users              Users             Users
```

点击 Relay：

```text
连接数量
流量
用户
Tailnet
地区
健康状态
```

---

# 21. Relay 地图

Admin 提供：

```text
Global Relay Map
```

显示：

```text
东京      ● 1,240 users
上海      ● 3,421 users
广州      ● 1,823 users
香港      ● 2,132 users
新加坡    ● 834 users
```

节点状态：

```text
绿色 = 正常
黄色 = 高负载
红色 = 故障
灰色 = 离线
```

---

# 22. Relay 自动选择

Xunara 不应该简单：

```text
固定 Relay
```

而应该给客户端下发：

```text
Relay Map
```

然后客户端根据：

```text
Latency
Region
Availability
Load
Network
```

选择最合适的 Relay。

Tailscale 客户端本身会根据 Control Server 提供的 DERP Map 测量并选择较合适的中继区域，因此 Xunara 应该尽量利用这个既有机制，而不是设计一套破坏官方客户端兼容性的专有选择协议。

---

# 23. Relay Region

Relay 不应该只有：

```text
relay_id
```

还必须有：

```text
region_id
region_code
region_name
country
province
city
latitude
longitude
isp
asn
```

例如：

```text
JP-TYO-01
```

---

# 24. Relay Group

多个 Relay 可以组成 Region：

```text
Tokyo
├── Relay 01
├── Relay 02
└── Relay 03
```

Region 出现故障：

```text
Tokyo
 ↓
Unavailable
 ↓
Singapore
```

---

# 25. Relay 高可用

一个 Region 最好支持：

```text
Relay A
Relay B
Relay C
```

而不是：

```text
一个 Region = 一个服务器
```

否则一个 VPS 挂掉整个区域就不可用。

---

# 26. Relay 限速

这是 Xunara 与普通 Headscale 部署非常重要的差异化功能。

支持：

```text
Global Limit
Region Limit
Relay Limit
Tailnet Limit
User Limit
Device Limit
```

例如：

```text
Relay：
1 Gbps

Tailnet：
200 Mbps

User：
50 Mbps

Device：
20 Mbps
```

---

# 27. Relay 限速模型

建立：

```text
BandwidthPolicy
```

字段：

```text
max_ingress
max_egress
max_total
burst
priority
```

例如：

```text
Free:
10 Mbps

Pro:
100 Mbps

Enterprise:
1 Gbps
```

---

# 28. 限速必须区分方向

不能只设计：

```text
bandwidth = 100Mbps
```

必须支持：

```text
Ingress
Egress
Bidirectional
```

例如：

```text
上传：
100 Mbps

下载：
500 Mbps
```

---

# 29. Relay 流量统计

必须统计：

```text
bytes_in
bytes_out
packets_in
packets_out
active_connections
peak_connections
peak_bandwidth
```

按：

```text
Relay
Region
Tailnet
User
Device
```

聚合。

---

# 30. 流量统计的隐私原则

Relay 可以统计：

```text
流量大小
连接数量
时间
来源设备
目标设备
Relay
```

但是不能记录：

```text
业务数据内容
```

因为 DERP 本身转发的是已经加密的 WireGuard 流量；官方文档也明确说明 DERP 无法解密设备之间的流量。

---

# 31. Relay 不做 DPI

禁止：

```text
Deep Packet Inspection
内容解析
明文抓包
业务内容记录
```

Xunara Relay 的职责：

```text
转发
统计
限速
健康检查
```

---

# 32. Relay 监控

每个 Relay 必须发送：

```text
Heartbeat
CPU
Memory
Disk
Network
Connections
Bandwidth
Version
Uptime
```

---

# 33. Relay 健康评分

后台计算：

```text
Health Score
```

例如：

```text
CPU      32%
Memory   41%
Bandwidth 63%
Latency  18ms
Packet Loss 0.1%

Health:
98
```

---

# 34. Relay 自动摘除

如果：

```text
连续 N 次 heartbeat 失败
```

自动：

```text
Relay
 ↓
Degraded
 ↓
Offline
 ↓
从新下发的 Relay Map 中降低优先级/移除
```

但必须注意：

**不能直接假定现有官方 Tailscale 客户端会瞬间重新获取最新 Map。**

客户端本地会缓存 DERP Map，因此 Control Plane 恢复后仍然需要通过标准机制让客户端最终获得新状态。

---

# 35. Relay 配置中心

Admin 可以设置：

```text
监听地址
监听端口
IPv4
IPv6
Region
Relay Name
STUN
Bandwidth
Maximum Connections
```

---

# 36. Relay 远程配置

Xunara 不应该要求管理员：

```text
SSH
 ↓
修改配置文件
 ↓
systemctl restart
```

而应该：

```text
Admin
 ↓
Relay
 ↓
配置
 ↓
下发
 ↓
Relay Agent
 ↓
Apply
```

---

# 37. Relay Agent

建议：

```text
xunara-relay
```

不仅是一个 DERP Server。

它应该是：

```text
Relay Engine
+
Control Agent
+
Metrics Agent
+
Update Agent
+
Config Agent
```

结构：

```text
xunara-relay
├── relay
├── agent
├── metrics
├── updater
├── config
└── health
```

---

# 38. Relay 自动更新

Admin：

```text
Relay
 ↓
Upgrade
```

支持：

```text
Current:
1.2.3

Available:
1.2.4

[升级]
```

但必须：

```text
下载
 ↓
验证签名
 ↓
备份
 ↓
安装
 ↓
健康检查
 ↓
成功
```

失败：

```text
Rollback
```

---

# 39. Relay 软件签名

这是必须提前设计的。

Relay 更新包必须：

```text
SHA256
+
Digital Signature
```

Relay 不允许执行：

```text
未签名软件
```

---

# 40. Relay Release Channel

支持：

```text
stable
beta
nightly
```

默认：

```text
stable
```

Admin 可以选择：

```text
Relay Group
 ↓
stable
```

---

# 41. 私有 Relay 下载

用户界面：

```text
我的中继
 ↓
创建私有中继
```

选择：

```text
Linux AMD64
Linux ARM64
Linux ARMv7
Linux LoongArch64
```

未来：

```text
Windows Server
```

---

# 42. 安装方式

推荐提供：

```text
Install Script
Docker
Binary
Systemd
Package
```

例如：

```text
Binary
Docker
Debian/Ubuntu
RHEL
Arch
```

但安装脚本必须公开、可审计。

---

# 43. Docker Relay

提供：

```text
ghcr.io/xunara/xunara-relay
```

支持：

```text
amd64
arm64
arm/v7
```

未来：

```text
loong64
```

---

# 44. Relay Docker 模式

例如：

```text
docker run \
  --network host \
  ...
```

具体参数不要硬编码到产品设计中，最终根据 Relay 实现确定。

---

# 45. 私有 Relay 的安全边界

私有 Relay 注册后：

```text
只能服务授权 Tailnet
```

不能因为拿到：

```text
Relay IP
```

就允许任何用户使用。

必须：

```text
Headscale / Control Verification
```

验证客户端。

Headscale 当前的 DERP 文档也支持让独立 DERP 通过 `/verify` 向 Headscale 查询连接客户端是否属于允许的 Tailnet。

---

# 46. Relay ACL

Relay 本身也需要权限：

```text
Relay
 ├── allowed_tailnets
 ├── allowed_users
 └── allowed_devices
```

但优先级：

```text
Xunara Ownership
        ↓
Tailnet Permission
        ↓
Relay Permission
```

---

# 47. 全局 Relay 与 Private Relay 的关系

用户可以选择：

```text
默认：
Xunara Global Relay

高级：
我的 Private Relay

混合：
Global + Private
```

---

# 48. Relay Policy

例如：

```text
我的设备
 ↓
优先 Private Relay
 ↓
Private Relay 不可用
 ↓
Xunara Tokyo Relay
 ↓
Tokyo 不可用
 ↓
Singapore Relay
```

这样可以兼顾：

```text
性能
成本
可靠性
```

---

# 49. Relay 套餐关联

套餐可以决定：

```text
Free:
使用 Xunara Global Relay

Pro:
Global Relay
+
Private Relay

Business:
Private Relay
+
多个 Relay

Enterprise:
自建 Relay Region
+
专属 Relay
```

但这属于 Entitlement，不应该硬编码。

---

# 50. Relay 流量计费

未来可以支持：

```text
免费额度
Relay Traffic
超额流量
按量计费
```

例如：

```text
Pro：
500 GB / 月

Enterprise：
5 TB / 月
```

因此数据库现在就应该预留：

```text
RelayUsage
```

---

# 51. Relay Usage 数据

例如：

```text
relay_usage
----------------
id
relay_id
tailnet_id
user_id
bytes_in
bytes_out
period
created_at
```

统计系统可以异步聚合。

---

# 52. GitHub CI/CD

所有仓库统一：

```text
GitHub Actions
```

流程：

```text
Push
 ↓
Lint
 ↓
Unit Test
 ↓
Integration Test
 ↓
Security Scan
 ↓
Build
 ↓
Artifact
 ↓
Release
```

---

# 53. Release 管理

所有组件统一 SemVer：

```text
MAJOR.MINOR.PATCH
```

例如：

```text
Xunara Server:
1.0.0

Web:
1.0.0

Relay:
1.0.0

Client:
1.0.0
```

---

# 54. Server / Relay 版本兼容矩阵

必须维护：

```text
Compatibility Matrix
```

例如：

```text
Xunara Server | Relay | Client

1.0            1.x      Official Tailscale
1.1            1.x      Official Tailscale
2.0            2.x      Xunara Client 1.x
```

禁止升级 Server 后才发现旧 Relay 全部不可用。

---

# 55. GitHub Release

每个重要组件都必须有：

```text
Release
Changelog
Checksums
SBOM
Signature
Docker Image
Documentation
```

---

# 56. Container Registry

推荐：

```text
GHCR
```

例如：

```text
ghcr.io/xunara/xunara-server
ghcr.io/xunara/xunara-relay
ghcr.io/xunara/xunara-web
```

未来可以同步：

```text
Docker Hub
国内镜像仓库
```

---

# 57. Docker 镜像多架构

至少：

```text
linux/amd64
linux/arm64
```

以后：

```text
linux/arm/v7
linux/loong64
```

---

# 58. GitHub Environment

至少：

```text
development
staging
production
```

Production：

```text
Required Review
Protected Branch
Signed Release
```

---

# 59. GitHub Branch

推荐：

```text
main
develop
feature/*
fix/*
release/*
```

生产：

```text
main
```

必须经过：

```text
PR
CI
Review
```

---

# 60. CODEOWNERS

不同模块由不同维护者负责：

```text
/server
/web
/admin
/relay
/docs
```

未来可以：

```text
@xunara/backend
@xunara/frontend
@xunara/network
@xunara/security
```

---

# 61. GitHub Issue

Issue 类型：

```text
Bug
Feature
Security
Performance
Architecture
Documentation
Relay
Client
Server
```

---

# 62. GitHub Projects

建议至少：

```text
Xunara Core
Xunara Relay
Xunara Client
Xunara Platform
```

而不是所有东西堆在一个 Project。

---

# 63. Security Repository

建议未来独立：

```text
xunara-security
```

保存：

```text
Threat Model
Security Policy
CVE
Incident Response
Security Architecture
```

---

# 64. SECURITY.md

每个公开仓库都必须有：

```text
SECURITY.md
```

包括：

```text
漏洞报告
支持版本
响应时间
安全邮箱
```

---

# 65. SBOM

每次 Release 生成：

```text
SBOM
```

用于：

```text
依赖追踪
供应链安全
漏洞排查
```

---

# 66. Dependabot / Renovate

自动检测：

```text
Go
Node
Docker
GitHub Actions
```

依赖升级。

但：

**Headscale 版本升级必须经过兼容性测试。**

---

# 67. Headscale Upgrade Test

每次 Xunara Server CI：

```text
启动 Headscale
 ↓
启动 Xunara
 ↓
启动 Tailscale Client Test
 ↓
注册
 ↓
连接
 ↓
Policy
 ↓
Route
 ↓
DERP
```

验证官方客户端兼容。

---

# 68. 官方客户端 Compatibility Test

必须建立专门测试矩阵：

```text
Linux
Windows
macOS
Android
iOS
```

至少验证：

```text
登录
注册
设备出现
设备删除
策略更新
DNS
Route
DERP
Direct
Reconnect
```

---

# 69. Relay Compatibility Test

测试：

```text
Official Tailscale Client
        ↓
Xunara Control
        ↓
Xunara Relay
        ↓
Device
```

必须测试：

```text
Direct
DERP
Relay Failover
Relay Disable
Relay Recovery
```

---

# 70. Network Failure Test

CI/测试环境模拟：

```text
Relay Down
Control Down
Database Down
DNS Down
Network Packet Loss
High Latency
NAT
IPv4 Only
IPv6 Only
```

验证客户端是否可以恢复。

---

# 71. IPv4 / IPv6

Xunara 必须从架构层支持：

```text
IPv4
IPv6
Dual Stack
```

Relay 尤其要考虑：

```text
IPv4 → IPv6
IPv6 → IPv4
```

官方 DERP 本身也是双栈设计。

---

# 72. STUN

Relay 必须区分：

```text
DERP
STUN
```

STUN 用于：

```text
NAT Discovery
```

DERP 用于：

```text
Relay
```

Headscale Embedded DERP 当前也需要 STUN UDP/3478；生产部署必须明确开放这些网络要求。

---

# 73. Relay 端口规划

不能简单认为：

```text
443 = 全部
```

必须在部署文档明确：

```text
TCP/443
UDP/3478
```

以及未来可能的：

```text
IPv6
HTTP captive portal check
Metrics
Management
```

---

# 74. Relay 管理面与数据面分离

非常重要。

```text
Management Plane
        │
        │ HTTPS
        ▼
Xunara Control

Data Plane
        │
        ▼
DERP Traffic
```

Relay 数据流量不能经过 Xunara API。

否则：

```text
Xunara API
```

会成为：

```text
带宽瓶颈
```

---

# 75. Relay 不代理业务 API

正确：

```text
Device A
   │
   │ encrypted traffic
   ▼
Relay
   │
   ▼
Device B
```

错误：

```text
Device A
 ↓
Xunara API
 ↓
Relay
 ↓
Device B
```

---

# 76. Control Plane / Data Plane

Xunara 必须明确：

```text
Control Plane
```

负责：

```text
身份
配置
策略
Relay Map
设备
网络
权限
```

Data Plane：

```text
WireGuard
DERP
STUN
Peer Relay
```

---

# 77. Peer Relay 预留

除了 DERP，未来还应该预留：

```text
Peer Relay
```

因为 Tailscale 现在也支持 Peer Relay：当直连失败时，可以优先使用 Tailnet 内高吞吐节点作为中继，再回退到 DERP。

因此 Xunara：

```text
RelayType
├── DERP
├── PeerRelay
└── FutureRelay
```

---

# 78. 网络路径优先级

未来可以抽象：

```text
Direct
 ↓
Peer Relay
 ↓
Private DERP
 ↓
Xunara Regional DERP
 ↓
Xunara Global DERP
```

具体优先级不能写死，应该由：

```text
NetworkPolicy
```

决定。

---

# 79. Relay 成本管理

超级管理员需要看到：

```text
服务器成本
带宽成本
流量成本
在线时间
用户数量
每 GB 成本
```

例如：

```text
Tokyo Relay

月成本：
¥300

流量：
8.2 TB

成本：
¥36.5 / TB
```

这样以后才能做真正的商业化。

---

# 80. Relay 调度

未来可以根据：

```text
Latency
Load
Cost
Region
ISP
User Plan
Private Relay
```

选择：

```text
Relay Candidate
```

例如：

```text
User in Japan

Tokyo:
12ms / 30% Load

Hong Kong:
52ms / 10% Load

Singapore:
72ms / 20% Load

→ Tokyo
```

---

# 81. Relay 限制策略

支持：

```text
Hard Limit
Soft Limit
Burst
Priority
```

例如：

```text
Pro:
100 Mbps

Burst:
200 Mbps

持续超过：
降回 100 Mbps
```

---

# 82. Relay 优先级

支持：

```text
Priority
```

例如：

```text
Private Relay:
100

Xunara Paid Relay:
80

Xunara Free Relay:
50
```

---

# 83. Admin 可以控制 Relay 是否向用户公开

例如：

```text
Tokyo Relay

Visibility:
☑ Global
☐ Private
☐ Enterprise Only
```

---

# 84. Enterprise 专属 Relay

未来：

```text
Enterprise
 ↓
专属 Relay
```

例如：

```text
Company A
 ├── Relay CN-Shanghai-01
 ├── Relay CN-Guangzhou-01
 └── Relay HK-01
```

其他用户无法使用。

---

# 85. Relay 资源隔离

一个 Relay 如果服务多个 Tailnet：

```text
Tailnet A
Tailnet B
Tailnet C
```

必须逻辑隔离。

不能：

```text
Tailnet A
看到
Tailnet B
```

任何 Relay Metadata 都不能跨租户泄露。

---

# 86. Tenant Isolation

这是平台最高安全等级之一。

任何 API：

```text
GET /relays
```

都必须经过：

```text
Tenant Scope
```

普通用户只能看到：

```text
Global Relay
+
自己拥有的 Relay
+
明确共享给自己的 Relay
```

---

# 87. Admin 与 Super Admin

未来管理员也应该分级：

```text
Super Admin
Platform Admin
Network Admin
Support Admin
Billing Admin
Operations Admin
Security Admin
```

例如：

```text
Support Admin
```

不能：

```text
修改套餐
```

Billing Admin：

```text
可以管理账单
```

但：

```text
不能查看用户网络流量详细信息
```

---

# 88. Break Glass Account

超级管理员必须预留：

```text
Emergency Admin
```

用于：

```text
SSO 故障
OAuth 故障
数据库故障
身份系统故障
```

必须：

```text
强 MFA
独立凭据
审计
报警
```

---

# 89. 管理员操作审计

Admin 操作必须记录：

```text
谁
什么时候
IP
操作什么
修改前
修改后
原因
```

高风险操作：

```text
删除用户
删除 Tailnet
修改全局 Relay
修改网络池
修改管理员
修改认证
```

必须：

```text
二次确认
```

---

# 90. 数据库灾备

至少：

```text
Daily Backup
Hourly Backup
```

根据部署规模调整。

需要：

```text
Backup
Restore
Point-in-Time Recovery
```

---

# 91. Headscale 密钥备份

这是非常容易漏掉的一项。

必须保护：

```text
Headscale private key
Machine identity
Database
Policy
Xunara secrets
```

因为仅仅备份：

```text
PostgreSQL
```

是不够的。

---

# 92. Relay 不保存核心用户数据库

Relay 只保存：

```text
Relay Identity
Local Config
Cache
Metrics
```

不要把：

```text
User Database
Subscription Database
```

同步到 Relay。

---

# 93. Relay 离线行为

如果：

```text
Xunara Control Server
```

暂时不可用：

Relay 应该根据安全策略继续：

```text
已有连接
```

但新连接是否允许必须有明确策略。

推荐：

```text
Existing Sessions:
Continue

New Unknown Clients:
Deny
```

---

# 94. Relay 配置缓存

Relay 应缓存：

```text
Relay Policy
Allowed Tailnets
Region
Bandwidth
Configuration
```

用于短时 Control Plane 故障。

---

# 95. Relay 配置版本

每次配置：

```text
Config Revision
```

例如：

```text
revision: 1024
```

Relay：

```text
local revision: 1023
```

收到：

```text
1024
```

才更新。

---

# 96. Relay Configuration Rollback

每次配置修改：

```text
Config History
```

支持：

```text
查看
比较
回滚
```

---

# 97. Relay 灰度发布

未来：

```text
10% Relay
 ↓
观察
 ↓
30%
 ↓
100%
```

不能：

```text
一次性升级全部 Relay
```

---

# 98. Server 灰度升级

同样：

```text
Staging
 ↓
Canary
 ↓
Production
```

---

# 99. Feature Flag

未来：

```text
relay.bandwidth_limit
relay.private
relay.billing
relay.peer
client.network_tools
```

全部通过 Feature Flag 控制。

---

# 100. 文档仓库

`xunara-docs` 必须包含：

```text
docs/
├── user/
├── admin/
├── developer/
├── api/
├── deployment/
├── relay/
├── client/
├── security/
├── architecture/
├── operations/
└── troubleshooting/
```

---

# 101. Relay 文档必须提供

用户安装私有 Relay 时：

```text
硬件要求
系统要求
网络要求
端口要求
安装
Docker
Binary
Systemd
注册
配置
升级
卸载
故障排查
```

---

# 102. 自托管 Xunara

未来应该预留：

```text
Xunara Self-Hosted
```

企业可以：

```text
自己部署
Xunara Server
Xunara Web
Xunara Relay
```

但：

```text
SaaS
```

和：

```text
Self-Hosted
```

共享：

```text
Core API
Domain Model
Relay
Client
```

---

# 103. 部署仓库

`xunara-deploy`：

```text
docker-compose
helm
kubernetes
systemd
ansible
terraform
```

未来支持：

```text
1-click deployment
```

---

# 104. Infrastructure Repository

`xunara-infrastructure`：

```text
Terraform
Ansible
Monitoring
Prometheus
Grafana
Alertmanager
Cloud
DNS
CDN
```

与业务代码分离。

---

# 105. Terraform Provider

未来可以提供：

```text
terraform-provider-xunara
```

例如：

```text
xunara_tailnet
xunara_device
xunara_policy
xunara_relay
xunara_dns
```

这也是企业用户非常需要的能力。

---

# 106. CLI

未来：

```text
xunara-cli
```

例如：

```text
xunara login
xunara device list
xunara device remove
xunara network list
xunara relay list
xunara relay create
xunara policy test
```

CLI 使用：

```text
Xunara API
```

而不是直接访问数据库。

---

# 107. SDK

未来：

```text
xunara-sdk-go
xunara-sdk-js
xunara-sdk-python
```

至少先定义：

```text
OpenAPI
```

自动生成 SDK。

---

# 108. OpenAPI

所有公开 API：

```text
OpenAPI 3.x
```

自动生成：

```text
API Docs
SDK
Client Types
```

避免：

```text
前端自己猜 API
```

---

# 109. Web / Admin / Client 共用 API Types

统一：

```text
api-types
```

例如：

```text
Device
Relay
Network
Policy
User
Plan
Subscription
```

避免：

```text
Web Device
Admin Device
Client Device
```

出现三个不同定义。

---

# 110. API Compatibility

任何 API 删除必须：

```text
Deprecation
 ↓
Warning
 ↓
Migration
 ↓
New API
 ↓
最终删除
```

不能直接删除。

---

# 111. Webhook

未来必须支持：

```text
Webhook
```

例如：

```text
device.created
device.deleted
relay.offline
relay.online
subscription.created
subscription.expired
policy.changed
```

企业可以接入自己的系统。

---

# 112. Notification

通知中心：

```text
站内消息
Email
Webhook
未来短信
未来微信
```

例如：

```text
Relay 离线
套餐即将到期
设备超过限制
新设备加入
安全登录
```

---

# 113. Alerting

管理员可以配置：

```text
Relay CPU > 90%
Relay bandwidth > 90%
Relay offline
DERP unavailable
Database failure
```

通知：

```text
Email
Webhook
```

---

# 114. 事件中心

平台统一：

```text
Event Bus
```

例如：

```text
UserCreated
DeviceCreated
DeviceOnline
DeviceOffline
RelayOnline
RelayOffline
PolicyChanged
SubscriptionChanged
```

未来所有模块都订阅这个 Event Bus。

---

# 115. 最重要的新增架构

最终 Xunara 应该形成：

```text
                         XUNARA
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
     Identity          Business           Network
        │                  │                  │
     User/Auth        Billing/Plan       Tailnet
     OAuth             Entitlement       Device
     Session           Subscription      Policy
        │                  │              Route
        │                  │              DNS
        │                  │
        └──────────────────┼──────────────────┘
                           │
                       Control API
                           │
             ┌─────────────┼─────────────┐
             │             │             │
         Headscale       Relay        Future
         Adapter        Manager       Network
             │             │
             │       ┌─────┼─────┐
             │       │     │     │
             │     Global Private Enterprise
             │     Relay  Relay    Relay
             │
             ▼
       Tailscale Protocol
             │
      ┌──────┼─────────┐
      │      │         │
 Official  Xunara    Future
 Client    Client    Clients
```

---

# 116. 最终 GitHub Organization

长期最终可以形成：

```text
Xunara/
│
├── xunara-server
├── xunara-web
├── xunara-admin
├── xunara-relay
├── xunara-client
├── xunara-cli
├── xunara-sdk
│
├── xunara-policy
├── xunara-network-tools
│
├── xunara-deploy
├── xunara-infrastructure
│
├── xunara-docs
├── xunara-community
└── xunara-security
```

---

# 117. Repository 依赖关系

```text
                    xunara-sdk
                       ▲
                       │
                  xunara-server
                   ▲    ▲    ▲
                   │    │    │
             xunara-web │ xunara-admin
                        │
                 xunara-client
                        │
                  xunara-policy
                        │
                 xunara-network-tools


xunara-relay
      │
      ▼
xunara-server


xunara-deploy
      │
      ├── server
      ├── web
      ├── admin
      └── relay
```

---

# 118. 不允许形成循环依赖

例如：

```text
xunara-server
    ↓
xunara-web
    ↓
xunara-server
```

禁止。

正确：

```text
xunara-server
      ↑
      │
api-types
      │
      ├── web
      ├── admin
      └── client
```

---

# 119. 目前不应该创建的仓库

虽然最终可能需要：

```text
xunara-ios
xunara-android
xunara-windows
xunara-macos
xunara-linux
```

但是早期不要拆这么细。

第一阶段：

```text
xunara-client
```

即可。

等客户端成熟以后，再根据平台实际情况拆分。

---

# 120. 当前第一阶段真正需要的仓库

建议实际马上创建：

```text
xunara-server
xunara-web
xunara-admin
xunara-relay
xunara-deploy
xunara-docs
```

其中：

```text
xunara-relay
```

从第一天就建立。

即使第一版只有：

```text
Embedded DERP
```

也必须提前建立 Relay abstraction。

---

# 121. Relay 的最终定位

Xunara Relay 不是：

```text
简单 derper 二进制
```

而是：

```text
Xunara Network Edge
```

未来它可以拥有：

```text
DERP
STUN
Peer Relay
Traffic Control
QoS
Bandwidth Limit
Metrics
Health
Remote Management
Auto Update
Failover
```

因此必须独立仓库。

---

# 122. 还需要补充的产品模块

经过这次架构审查，目前上一版还缺少以下模块：

```text
① Relay Platform
② Network Monitoring
③ Notification
④ Webhook
⑤ API / SDK
⑥ CLI
⑦ Terraform
⑧ Backup / Restore
⑨ Disaster Recovery
⑩ Security / Threat Model
⑪ Supply Chain Security
⑫ Feature Flags
⑬ Compatibility Matrix
⑭ IPv6
⑮ Peer Relay
⑯ Service Discovery
⑰ Network Diagnostics
⑱ Admin RBAC
⑲ Usage Metering
⑳ Cost Accounting
```

---

# 123. 未来还应该考虑但暂时不要实现

这些必须留接口，但不要现在开发：

```text
远程桌面
SSH
文件传输
Taildrive
NAS 服务发现
设备远程控制
IoT
智能家居
网络测速
公网服务发布
Funnel 类功能
企业 SSO
SAML
LDAP
设备合规检查
MDM
设备姿态检查
```

Headscale/Tailscale 生态本身也在继续增加 Grants、Node Attributes、Peer Relay 等能力，因此 Xunara 的 Policy / Capability 模型必须保持足够抽象，不能只围绕今天的 ACL 写死。

---

# 124. Xunara 的长期产品边界

最终必须形成三个产品层：

## Xunara Cloud

```text
用户
套餐
Tailnet
网络
设备
权限
Relay
计费
```

## Xunara Network

```text
Headscale
DERP
STUN
Peer Relay
Network Control
```

## Xunara Ecosystem

```text
Client
CLI
SDK
Terraform
Network Tools
Remote Tools
第三方集成
```

---

# 125. 最终原则

Xunara 不应该变成：

```text
一个漂亮的 Headscale Admin UI
```

而应该成为：

```text
                    Xunara Network Platform

       ┌─────────────────────────────────────────┐
       │                User Cloud               │
       │                                         │
       │ Account / Plan / Billing / Tailnet      │
       └────────────────────┬────────────────────┘
                            │
                   ┌────────▼────────┐
                   │ Xunara Control  │
                   └────────┬────────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
          Headscale       Relay        Network
          Control         Platform      Tools
              │             │             │
              │        ┌────┼────┐        │
              │        │    │    │        │
              │      Global Private  Enterprise
              │      Relay  Relay      Relay
              │
        ┌─────┴──────────────┐
        │                    │
 Official Tailscale      Xunara Client
 Client                       │
        │                     │
        └──────────┬──────────┘
                   │
                Tailnet
```

**官方 Tailscale 客户端永远是兼容入口之一；Xunara Client 是增强入口，而不是替代入口。**

**Relay 永远属于独立的数据平面，不允许成为 Xunara API 的流量代理瓶颈。**

**GitHub 多仓库是项目长期治理基础。**

**所有未来功能通过 Capability / Provider / Adapter / Plugin 接入，而不是不断修改核心 Headscale 逻辑。**