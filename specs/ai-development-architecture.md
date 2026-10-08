# Xunara AI 长期开发与架构规范

> 文档类型：长期维护型 AI 开发规范  
> 项目名称：Xunara  
> 项目定位：基于 Headscale Control Plane 的 Tailscale-like 网络服务平台  
> 核心目标：提供类似 Tailscale 官方产品的用户登录、Tailnet、设备管理、网络管理、权限管理、套餐体系和 Web Console，同时始终兼容官方 Tailscale 客户端，并为未来 Xunara 自有客户端及其他异地组网工具预留架构空间。
>
> **本文件是 AI 开发的最高级项目规范之一。**
>
> 任何 AI 在修改代码前，必须先阅读本文件，并遵守“架构不破坏、官方客户端兼容、数据隔离、向后兼容、可迁移、可测试”原则。

---

# 1. 项目总定位

Xunara 不是 Headscale Web UI。

Xunara 是一个完整的网络服务产品。

正确关系：

```text
                         Xunara Platform
                               │
          ┌────────────────────┼────────────────────┐
          │                    │                    │
     Identity Layer       Product Layer       Admin Layer
          │                    │                    │
     登录/注册/OAuth       Tailnet/Device       超级管理员
     用户中心             Network/Policy        套餐管理
     Session              Billing              系统管理
          │                    │                    │
          └────────────────────┼────────────────────┘
                               │
                        Xunara Core API
                               │
                    ┌──────────▼──────────┐
                    │ Headscale Adapter   │
                    │ Control Plane Layer │
                    └──────────┬──────────┘
                               │
                           Headscale
                               │
                    Tailscale Protocol
                               │
             ┌─────────────────┼─────────────────┐
             │                 │                 │
       Official Client    Official Client    Xunara Client
       Windows/macOS      Android/Linux      Future
             │                 │                 │
             └─────────────────┼─────────────────┘
                               │
                        WireGuard / DERP
```

必须牢记：

```text
Xunara ≠ Headscale
Xunara ≠ Headscale UI
Xunara ≠ Tailscale Client
```

Xunara 是产品层。

Headscale 是控制平面。

Tailscale Client 是现阶段主要客户端。

未来 Xunara Client 是客户端扩展层。

---

# 2. 核心设计原则

## 2.1 官方客户端兼容优先

这是项目最高级别的架构约束。

Xunara 必须始终保证：

```text
官方 Tailscale Client
        │
        ▼
Xunara / Headscale Control Server
        │
        ▼
正常加入 Tailnet
```

不得为了实现 Xunara 自定义功能而破坏：

- 官方 Tailscale Windows Client
- 官方 Tailscale macOS Client
- 官方 Tailscale Linux Client
- 官方 Tailscale Android Client
- 官方 Tailscale iOS Client
- 官方 Tailscale CLI
- 官方 Tailscale API/协议兼容行为

官方客户端使用自定义 Control Server 是 Xunara 的基础能力。

---

# 3. Xunara 三层产品模型

Xunara 从第一天就必须分成三层。

## Layer 1：Xunara SaaS

负责：

```text
用户
账户
登录
套餐
计费
Tailnet
设备
权限
网络
审计
通知
```

## Layer 2：Headscale Control Plane

负责：

```text
节点注册
节点状态
网络控制
密钥/身份
路由
策略
DERP
MagicDNS
Tailnet Control
```

## Layer 3：客户端

当前：

```text
官方 Tailscale Client
```

未来：

```text
Xunara Client
```

以后：

```text
Xunara Network Tools
```

---

# 4. 严格禁止的架构

AI 不得把以下东西直接混在一起：

```text
User
Plan
Billing
Payment
Device Limit
Subscription
```

不能直接写进 Headscale。

错误：

```text
Headscale Node
    ↓
判断用户是不是 Pro
```

正确：

```text
Xunara User
      ↓
Xunara Subscription
      ↓
Entitlement
      ↓
Policy Enforcement
      ↓
Headscale
```

---

# 5. 多租户模型

Xunara 必须从第一天支持 Multi-Tenant。

核心关系：

```text
Platform
 ├── User
 │
 ├── Organization
 │      │
 │      └── Membership
 │
 ├── Tailnet
 │      │
 │      ├── Devices
 │      ├── Routes
 │      ├── Policies
 │      ├── DNS
 │      └── Members
 │
 └── Subscription
```

最小模型：

```text
User
Organization
OrganizationMember
Tailnet
TailnetMember
Device
Network
Policy
Subscription
Plan
```

---

# 6. 用户体系

## 6.1 User

用户必须有稳定内部 ID。

推荐：

```text
UUID / ULID
```

禁止使用：

```text
email
username
phone
```

作为数据库主键。

用户信息：

```text
id
username
display_name
email
avatar
status
locale
timezone
created_at
updated_at
last_login_at
```

---

# 7. 登录体系

Xunara 必须自己拥有完整身份系统。

支持：

```text
Email + Password
Email Verification
Password Reset
OAuth/OIDC
Session
Refresh Token
2FA
Login History
Device Session
```

未来可以增加：

```text
Google
GitHub
Microsoft
Apple
微信
QQ
LinuxDo
企业 OIDC
LDAP
SAML
```

但所有第三方身份最终都必须映射到：

```text
Xunara User
```

不得让 OAuth Provider 成为业务主键。

---

# 8. 用户中心

用户中心是 Xunara 的核心产品之一。

推荐导航：

```text
我的账户
├── 总览
├── 个人资料
├── 安全中心
├── 登录与会话
├── 我的设备
├── 我的网络
├── 我的 Tailnet
├── 成员与共享
├── 权限管理
├── DNS
├── 路由
├── Exit Node
├── DERP / 连接
├── API
├── Auth Keys
├── 通知
├── 套餐
├── 账单
└── 设置
```

---

# 9. 用户中心：首页

Dashboard 必须让普通用户无需理解 Headscale。

首页显示：

```text
我的网络

Tailnet
Xunara Network

网络地址
100.x.x.x/24

设备
7 / 10

在线设备
5

离线设备
2

网络状态
正常

DERP
上海
直连率
92%
```

同时显示：

```text
最近设备
最近连接
最近事件
套餐使用情况
```

---

# 10. 个人资料

功能：

```text
头像
昵称
用户名
邮箱
语言
时区
个人简介
```

支持：

```text
修改头像
修改昵称
修改邮箱
验证邮箱
注销账户
导出个人数据
删除账户
```

删除账户必须有二次确认。

---

# 11. 安全中心

必须支持：

```text
修改密码
密码强度检查
2FA
恢复码
登录历史
活动 Session
设备登录记录
撤销 Session
撤销所有 Session
```

未来：

```text
Passkey
WebAuthn
硬件安全密钥
```

必须预留。

---

# 12. 登录与 Session

用户应该能够看到：

```text
当前登录设备

Chrome / Windows
东京
当前会话

Android
上海
2小时前

Firefox
广州
昨天
```

支持：

```text
退出当前设备
退出其他设备
退出所有设备
```

---

# 13. 我的设备

这是用户最常用页面之一。

显示：

```text
设备名称
操作系统
IP
Tailscale IP
在线状态
最后在线
客户端版本
DERP
直连状态
设备标签
设备角色
```

示例：

```text
MacBook-Pro
● 在线
100.100.1.2
Direct
macOS

NAS
● 在线
100.100.1.3
Shanghai DERP
Linux

Phone
○ 离线
100.100.1.4
Android
```

---

# 14. 设备详情页

必须提供完整设备信息：

```text
基本信息
网络信息
连接状态
客户端版本
操作系统
设备标签
路由
权限
最近活动
连接历史
```

操作：

```text
修改名称
添加标签
删除设备
撤销设备
重新授权
禁用设备
查看权限
查看网络连接
```

---

# 15. 设备状态

不要只显示：

```text
Online / Offline
```

应该至少显示：

```text
Online
Offline
Idle
Connecting
Relay
Direct
Expired
Needs Approval
Disabled
```

连接方式：

```text
Direct
DERP
Unknown
```

---

# 16. 网络中心

用户中心必须有一个独立：

```text
网络
```

页面。

显示：

```text
网络 CIDR
IP 分配
DNS
MagicDNS
Subnet Routes
Exit Nodes
DERP
Network Status
```

---

# 17. 免费套餐网络规则

Free 用户：

```text
最大设备：
10

网络：
系统自动分配

用户不能修改 CIDR
```

UI 必须明确告诉用户：

```text
当前套餐：
免费版

设备：
7 / 10

网络：
100.x.x.x/24

网络地址由 Xunara 自动分配。

升级套餐后可自定义网络地址。
```

---

# 18. 付费套餐网络规则

Pro / Business / Enterprise 可以开启：

```text
Custom Network
```

例如：

```text
192.168.50.0/24
```

提交后必须经过：

```text
CIDR Parser
      ↓
合法性检查
      ↓
保留网段检查
      ↓
平台网络冲突检查
      ↓
其他 Tailnet 冲突检查
      ↓
安全检查
      ↓
Network Allocation
      ↓
Headscale Adapter
```

---

# 19. Network Allocation Service

必须独立成模块。

```text
services/network-allocation/
```

负责：

```text
自动分配
自定义 CIDR
CIDR 冲突
保留地址
网络回收
网络迁移
网络扩容
网络审计
```

不能直接在 HTTP Controller 中处理。

---

# 20. 设备权限设计

这是 Xunara 的核心创新之一。

传统 ACL：

```text
src
dst
ports
action
```

对于普通中国用户不够直观。

Xunara 必须提供：

# 可视化权限中心

---

# 21. 权限方式一：拓扑图

页面：

```text
网络拓扑
```

例如：

```text
                 ┌─────────────┐
                 │  MacBook    │
                 │ 100.1.1.2   │
                 └──────┬──────┘
                        │
                     允许访问
                        │
              ┌─────────▼─────────┐
              │       NAS         │
              │    100.1.1.10     │
              └─────────┬─────────┘
                        │
                   TCP 443
                        │
              ┌─────────▼─────────┐
              │       Web         │
              │    HTTPS:443      │
              └───────────────────┘
```

节点颜色代表：

```text
绿色 = 可访问
灰色 = 无权限
黄色 = 部分权限
红色 = 禁止
蓝色 = 当前设备
```

点击两个设备：

```text
MacBook → NAS
```

弹出：

```text
访问权限

网络：
✓ 允许

端口：
☑ 22
☑ 80
☑ 443
☐ 445

方向：
MacBook → NAS

状态：
允许
```

---

# 22. 权限方式二：设备对设备

用户可以直接选择：

```text
来源设备：
[ 我的 MacBook ]

目标设备：
[ 家庭 NAS ]

权限：
● 完全访问
○ 仅指定端口
○ 仅指定服务
○ 禁止访问
```

如果选择：

```text
仅指定端口
```

显示：

```text
☑ SSH       22
☑ HTTPS     443
☐ SMB       445
☐ RDP       3389
```

---

# 23. 权限方式三：拖拽连线

拓扑图支持：

```text
拖动设备
    ↓
连接另一个设备
    ↓
创建访问规则
```

例如：

```text
[我的电脑] ─────────→ [家庭 NAS]
```

弹出：

```text
创建访问权限

允许：
我的电脑

访问：
家庭 NAS

服务：
☑ Web
☑ SSH

保存
```

AI 不得把拖拽 UI 直接转换成任意策略。

必须：

```text
Visual Rule
    ↓
Policy AST
    ↓
Validation
    ↓
Policy Compiler
    ↓
Headscale/Tailscale Policy
```

---

# 24. 权限方式四：按用户

例如：

```text
张三
```

允许：

```text
张三
 ├── NAS
 ├── Server
 └── Home PC
```

---

# 25. 权限方式五：按设备组

例如：

```text
家庭设备
├── NAS
├── TV
├── Home Assistant
└── Router

工作设备
├── MacBook
├── ThinkPad
└── Server
```

然后：

```text
工作设备
      ↓
允许访问
      ↓
服务器组
```

---

# 26. 权限方式六：按服务

对于中国普通用户，“设备 + 服务”比端口更容易理解。

提供：

```text
SSH
Web
HTTPS
RDP
SMB
FTP
数据库
自定义服务
```

用户选择：

```text
NAS
 ├── Web
 ├── SSH
 └── SMB
```

后台最终转换成：

```text
TCP/443
TCP/22
TCP/445
```

---

# 27. 权限方式七：高级模式

高级用户可以打开：

```text
高级策略编辑器
```

看到：

```text
Grants / ACL
```

但是默认不显示复杂 JSON。

普通用户：

```text
图形化
```

高级用户：

```text
Policy
```

两者必须使用同一个内部 Policy AST。

---

# 28. Policy Engine

必须独立：

```text
policy/
├── model
├── parser
├── validator
├── compiler
├── simulator
├── diff
└── adapters
```

架构：

```text
Visual UI
    │
    ▼
Policy AST
    │
    ├── Validation
    ├── Conflict Detection
    ├── Simulation
    ├── Diff
    │
    ▼
Policy Compiler
    │
    ├── Grants
    └── Legacy ACL
            │
            ▼
        Headscale
```

Tailscale 当前推荐 Grants，但 ACL 仍然保持支持，因此 Xunara 必须把 Grants 作为新策略的主要目标，同时保留 ACL Compatibility Layer。 

---

# 29. 权限模拟器

用户点击：

```text
测试权限
```

输入：

```text
来源：
MacBook

目标：
NAS

服务：
443
```

显示：

```text
✓ 允许

原因：

MacBook
  ↓
工作设备组
  ↓
允许访问
  ↓
家庭 NAS
  ↓
HTTPS / 443
```

如果拒绝：

```text
✕ 拒绝

原因：

没有匹配的访问策略
```

---

# 30. 权限变更预览

任何修改策略之前：

```text
保存
```

必须先显示：

```text
本次修改：

新增：
MacBook → NAS : HTTPS

删除：
无

影响设备：
2

可能受影响连接：
1

[确认修改]
[取消]
```

防止普通用户误操作导致整个网络断联。

---

# 31. Tailnet 页面

显示：

```text
Tailnet 名称
Tailnet ID
Network CIDR
DNS
设备
成员
策略
路由
Exit Node
DERP
```

---

# 32. 成员系统

未来必须支持多人 Tailnet。

角色：

```text
Owner
Admin
Network Admin
Member
Viewer
```

权限采用 RBAC + Resource Scope。

例如：

```text
Owner
 └── 全部权限

Network Admin
 ├── Devices
 ├── Routes
 ├── DNS
 └── Policies

Member
 └── 自己的设备

Viewer
 └── 只读
```

---

# 33. Subnet Router

用户可以看到：

```text
Subnet Router

设备：
Home Router

广告网络：
192.168.1.0/24

状态：
● 在线

路由：
✓ 已批准
```

必须明确区分：

```text
Route
```

与：

```text
Permission
```

Route 决定：

```text
哪个网络可以被路由到
```

Policy 决定：

```text
谁可以访问
```

两者不能混为一谈。

---

# 34. Exit Node

用户可以看到：

```text
Exit Nodes

Home
Japan
Online

Office
China
Online
```

可以：

```text
启用
禁用
设置允许用户
查看状态
```

---

# 35. DNS

用户中心：

```text
DNS
├── MagicDNS
├── DNS Servers
├── Search Domains
├── Split DNS
└── Hostnames
```

未来支持：

```text
自定义域名
内部 DNS
DoH
DoT
```

必须保持模块化。

---

# 36. DERP

普通用户不需要理解 DERP。

UI 应该显示：

```text
连接状态

MacBook → NAS

● Direct

延迟：
8 ms
```

或者：

```text
MacBook → NAS

● DERP 中继

中继：
上海

延迟：
42 ms
```

高级页面才显示：

```text
DERP Region
Latency
Connection
Relay
```

Headscale 当前支持嵌入式 DERP，因此 Xunara 的 DERP 管理必须与 Headscale Adapter 解耦。 

---

# 37. 设备连接可视化

提供：

```text
网络拓扑
```

显示：

```text
用户
  │
  ├── Device A
  │       │
  │       └──── Direct ─── Device B
  │
  └── Device C
          │
          └──── Shanghai DERP ─── Device D
```

点击连接：

```text
Connection Detail

Source:
MacBook

Destination:
NAS

Path:
Direct

Latency:
8ms

Packet Loss:
0%

Policy:
Allow HTTPS

Last Seen:
Now
```

---

# 38. 套餐系统

套餐必须数据驱动。

Plan：

```text
id
name
description
price
currency
billing_cycle
max_devices
max_members
max_routes
max_auth_keys
allow_custom_network
allow_custom_dns
allow_exit_node
allow_subnet_router
allow_api
allow_advanced_policy
allow_team
allow_audit
```

---

# 39. Entitlement

不要在代码里大量出现：

```text
if plan == "pro"
```

禁止。

正确：

```text
EntitlementService
```

例如：

```text
can("network.custom_cidr")
can("device.create")
can("policy.advanced")
can("route.create")
```

这样未来增加套餐不会修改业务代码。

---

# 40. 设备数量限制

例如 Free：

```text
max_devices = 10
```

流程：

```text
Device Create
      ↓
Entitlement Check
      ↓
Current Device Count
      ↓
< Max ?
      │
     YES
      ↓
Headscale Registration
```

超过：

```text
DEVICE_LIMIT_REACHED
```

---

# 41. 套餐升级

升级：

```text
Free
 ↓
Pro
```

立即：

```text
更新 Entitlement
```

但是不能自动破坏已有网络。

降级：

```text
Pro
 ↓
Free
```

如果当前：

```text
设备 30
Free 只能 10
```

不得立即删除设备。

应该进入：

```text
Over Limit
```

状态。

用户可以：

```text
删除设备
```

直到：

```text
<= 10
```

---

# 42. 计费架构

Billing 必须独立。

```text
billing/
├── plans
├── subscriptions
├── invoices
├── payments
├── entitlements
└── providers
```

支付渠道通过 Adapter：

```text
PaymentProvider
```

未来可以接：

```text
支付宝
微信支付
Stripe
PayPal
其他国内支付平台
```

业务层不能直接依赖某一个支付平台。

---

# 43. 超级管理员后台

域名建议：

```text
app.xunara.xxx
```

用户中心。

管理员：

```text
admin.xunara.xxx
```

完全独立。

---

# 44. Admin Dashboard

显示：

```text
用户总数
活跃用户
Tailnet 数量
设备数量
在线设备
套餐分布
收入
今日注册
今日新增设备
DERP 状态
Headscale 状态
API 状态
系统错误
```

---

# 45. Admin 用户管理

支持：

```text
查看用户
搜索用户
禁用用户
解禁用户
删除用户
修改套餐
查看 Tailnet
查看设备
强制退出
查看登录记录
查看审计
```

管理员不能默认知道用户密码。

---

# 46. Admin Tailnet 管理

支持：

```text
查看 Tailnet
搜索 Tailnet
查看 CIDR
查看设备
查看成员
查看策略
查看路由
查看 DERP
冻结 Tailnet
删除 Tailnet
```

---

# 47. Admin Device 管理

支持：

```text
查看所有设备
在线设备
离线设备
搜索设备
按用户过滤
按 Tailnet 过滤
按系统过滤
按版本过滤
强制删除
禁用
恢复
```

---

# 48. Admin Plan 管理

后台可视化创建：

```text
套餐名称
价格
周期
设备数量
成员数量
自定义网络
DNS
Routes
Exit Node
API
Advanced Policy
审计
```

---

# 49. Admin Network Pool

管理员可以配置：

```text
Free Network Pool
Paid Network Pool
Reserved Network
System Network
```

例如：

```text
Free Pool
100.64.0.0/10

Reserved
100.64.0.0/16

System
10.0.0.0/8
```

具体网段最终必须通过部署配置确定，不能在代码中硬编码。

---

# 50. Admin DERP 管理

显示：

```text
上海
广州
东京
香港
```

每个节点：

```text
Online
Latency
Connections
Traffic
Version
Region
IPv4
IPv6
```

---

# 51. 审计系统

所有关键操作必须记录：

```text
AuditLog
```

包括：

```text
登录
退出
创建设备
删除设备
修改权限
修改网络
修改套餐
邀请成员
删除成员
创建 API Key
删除 API Key
修改 DNS
修改 Route
修改 Exit Node
Admin 操作
```

记录：

```text
actor
action
resource
resource_id
ip
user_agent
before
after
created_at
```

敏感信息禁止进入日志。

---

# 52. Xunara Core API

所有前端都必须经过：

```text
Xunara API
```

不能：

```text
Frontend
   ↓
Headscale API
```

正确：

```text
Frontend
   ↓
Xunara API
   ↓
Domain Service
   ↓
Headscale Adapter
   ↓
Headscale
```

---

# 53. Headscale Adapter

这是整个项目最重要的隔离层之一。

```text
packages/headscale-adapter/
```

提供：

```text
createUser()
deleteUser()
listDevices()
deleteDevice()
createRoute()
approveRoute()
getPolicy()
setPolicy()
getStatus()
```

Xunara 业务层不能直接调用 Headscale SDK/API。

---

# 54. Headscale 版本兼容

必须建立：

```text
HeadscaleAdapterVxxx
```

例如：

```text
HeadscaleAdapter
├── v0_XX
├── v0_XX
└── ...
```

具体版本号根据实际部署确定。

升级 Headscale：

```text
Xunara Core
```

不应该被迫重写。

---

# 55. Headscale 数据库隔离

原则：

```text
Xunara Database
```

存：

```text
User
Plan
Subscription
Organization
Tailnet
Entitlement
Audit
Billing
VisualPolicy
```

Headscale Database：

```text
Headscale state
```

Xunara 不允许直接依赖 Headscale 数据库内部表结构。

必须通过：

```text
Headscale API
```

或者明确稳定的 Integration Layer。

---

# 56. Policy 数据双层存储

Xunara 保存：

```text
Visual Policy
```

例如：

```text
MacBook
 →
NAS
 →
HTTPS
```

同时编译成：

```text
Headscale/Tailscale Policy
```

所以：

```text
Visual Policy
        ↓
Policy AST
        ↓
Compiler
        ↓
Generated Policy
```

不能只保存生成后的 JSON。

否则以后无法可靠恢复可视化界面。

---

# 57. 官方客户端兼容层

Xunara 必须提供标准：

```text
Control Server
```

官方客户端：

```text
tailscale login --login-server=https://control.xunara.example
```

应该正常工作。

Xunara 不应要求用户安装 Xunara Client 才能加入网络。

这是产品核心原则。

---

# 58. 官方客户端登录体验

Web Console：

```text
添加设备
```

提供：

```text
Windows
macOS
Linux
Android
iOS
```

每个平台给出官方客户端安装方式。

然后：

```text
打开官方 Tailscale
        ↓
指定 Xunara Control Server
        ↓
认证
        ↓
设备进入 Xunara Tailnet
```

---

# 59. 不修改官方客户端协议

Xunara 不应该为了 Web UI 而修改 Tailscale WireGuard / coordination protocol。

原则：

```text
标准协议优先
官方客户端优先
自有功能通过控制层实现
```

---

# 60. Xunara 自有客户端预留

未来：

```text
Xunara Client
```

不能现在就把整个系统设计成“只有 Xunara Client 才能工作”。

正确：

```text
                 Xunara Control Plane
                         │
             ┌───────────┼───────────┐
             │           │           │
        Tailscale     Xunara       Future
        Client        Client       Client
             │           │           │
             └───────────┼───────────┘
                         │
                     Tailnet
```

---

# 61. Xunara Client 的定位

未来自有客户端不应该只是：

```text
重新包装 tailscale
```

而应该增加：

```text
个人用户中心
网络管理
设备管理
网络诊断
连接质量
权限可视化
节点发现
服务发现
快捷网络工具
```

例如：

```text
Xunara Client

我的账户
我的设备
我的网络
网络拓扑
附近设备
连接质量
路由
服务
诊断
设置
```

---

# 62. Client SDK Layer

为了以后开发自己的客户端，现在必须预留：

```text
Xunara Client API
```

而不是让客户端直接访问 Headscale。

架构：

```text
Xunara Client
      ↓
Xunara Client API
      ↓
Xunara Core
      ↓
Headscale Adapter
```

---

# 63. 未来异地组网工具平台

Xunara 最终不应该只是一套 Tailnet。

未来可以成为：

```text
Xunara Network Platform
```

功能模块：

```text
安全组网
远程访问
设备互联
内网穿透
文件传输
远程桌面
SSH
NAS
家庭网络
企业组网
IoT
远程运维
网络诊断
```

但：

**现在不要实现这些功能。**

现在只建立扩展接口。

---

# 64. Future Network Provider

定义统一接口：

```text
NetworkProvider
```

例如：

```text
HeadscaleProvider
XunaraProvider
FutureMeshProvider
```

未来可以：

```text
Xunara
 ├── Headscale
 ├── Xunara Mesh
 ├── Future Network
 └── Other Network Backend
```

---

# 65. Network Capability

不同网络后端提供：

```text
Capabilities
```

例如：

```text
supports_devices
supports_routes
supports_exit_nodes
supports_dns
supports_acl
supports_grants
supports_derp
supports_direct_p2p
supports_remote_access
```

前端根据 capability 显示功能。

不要写：

```text
if headscale
```

应该写：

```text
if capability.supports_routes
```

---

# 66. Xunara Tool Platform

未来：

```text
Tools
```

可以扩展：

```text
Network Scanner
Ping
Traceroute
DNS Test
Port Test
Route Test
DERP Test
Speed Test
Device Discovery
Remote SSH
Remote Desktop
File Transfer
```

这些必须作为独立模块：

```text
tools/
```

不能塞进：

```text
headscale/
```

---

# 67. Service Discovery

未来用户可以看到：

```text
NAS
Home Assistant
Web
SSH
RDP
Minecraft
```

而不是只有：

```text
100.100.x.x
```

服务模型：

```text
Service
├── device_id
├── name
├── protocol
├── port
├── category
└── visibility
```

---

# 68. 中国用户体验设计原则

Xunara 的 UI 必须面向普通中文用户。

不要要求用户理解：

```text
ACL
CIDR
DERP
Subnet Router
Exit Node
Policy
Tailnet
```

这些概念可以保留，但 UI 优先使用：

```text
我的网络
我的设备
允许谁访问谁
家庭设备
工作设备
共享设备
网络入口
网络出口
中继节点
```

高级用户再打开：

```text
高级设置
```

---

# 69. 权限 UI 的核心原则

默认：

```text
看图
点设备
选服务
保存
```

而不是：

```text
写 JSON
```

高级：

```text
可视化
↓
策略
↓
JSON
```

三者必须保持同步。

---

# 70. 权限模板

预置中国用户容易理解的模板：

```text
家庭网络
办公室网络
NAS 访问
远程办公
游戏设备
开发环境
服务器管理
仅浏览 Web
仅 SSH
完全互通
设备隔离
访客网络
儿童设备
IoT 隔离
```

例如：

```text
家庭 NAS
```

一键生成：

```text
手机 → NAS
电脑 → NAS
电视 → NAS

允许：
HTTPS
SMB
```

---

# 71. 网络拓扑视图

提供：

```text
拓扑
列表
矩阵
```

三种模式。

## 拓扑

```text
设备之间的连接关系
```

## 列表

```text
设备列表
```

## 权限矩阵

```text
             NAS   PC   手机   Server

NAS           -    ✓     ✓      ✓
PC            ✓    -     ✓      ✓
手机          ✓    ✓     -      ✕
Server        ✓    ✓     ✕      -
```

点击：

```text
✓
```

可以查看：

```text
为什么允许
允许哪些服务
由哪条策略决定
```

---

# 72. 权限矩阵必须支持大规模网络

设备超过：

```text
50
100
500
```

不能一次渲染所有节点。

必须支持：

```text
搜索
过滤
分组
折叠
虚拟滚动
按用户
按标签
按设备组
```

---

# 73. Policy Explain

任何权限结果都必须可以解释。

例如：

```text
为什么我的手机可以访问 NAS？

因为：

手机
 ↓
个人设备组
 ↓
家庭网络
 ↓
NAS
 ↓
HTTPS
```

或者：

```text
为什么不能访问？

因为：

手机
 ↓
没有匹配访问规则
 ↓
默认拒绝
```

---

# 74. Zero Trust

默认：

```text
Deny
```

用户明确允许：

```text
Allow
```

Xunara 新权限系统必须遵循最小权限原则。

---

# 75. ACL Compatibility

即使新系统使用 Grants，也必须兼容传统 ACL。

原因：

```text
旧配置
旧用户
旧 Headscale
旧客户端
已有策略
```

都不能因为 Xunara 升级突然失效。

---

# 76. API Key

Xunara API Key 与 Headscale API Key 必须完全分离。

用户看到：

```text
Xunara API Keys
```

而不是：

```text
Headscale API Keys
```

Xunara API：

```text
Bearer xunara_xxx
```

后端再通过内部身份访问 Headscale。

---

# 77. WebSocket / Event Bus

未来实时状态需要：

```text
Device Online
Device Offline
Route Changed
Policy Changed
DERP Changed
```

因此预留：

```text
Event Bus
```

例如：

```text
DeviceOnline
DeviceOffline
DeviceCreated
DeviceDeleted
PolicyChanged
RouteChanged
SubscriptionChanged
```

前端通过：

```text
WebSocket / SSE
```

获得实时更新。

---

# 78. 事件驱动架构

重要操作：

```text
Command
 ↓
Domain Service
 ↓
Database
 ↓
Event
 ↓
Async Handler
```

例如添加设备：

```text
DeviceCreateRequested
        ↓
Entitlement Check
        ↓
Create Device
        ↓
Headscale
        ↓
DeviceCreated
        ↓
Audit
        ↓
Notification
```

---

# 79. 后台任务

必须预留：

```text
Job Queue
```

处理：

```text
网络分配
设备同步
策略编译
Headscale 同步
账单
邮件
通知
统计
审计
健康检查
```

不能全部阻塞 HTTP 请求。

---

# 80. 数据一致性

Xunara 是业务事实来源：

```text
User
Plan
Subscription
Entitlement
VisualPolicy
```

Headscale 是网络控制事实来源：

```text
Node
Route
Network State
Control State
```

两者之间通过：

```text
Reconciliation
```

保持一致。

---

# 81. Reconciliation

定期：

```text
Xunara State
       ↕
Headscale State
```

发现：

```text
Xunara 有
Headscale 没有
```

或者：

```text
Headscale 有
Xunara 没有
```

必须报警/修复。

禁止静默忽略。

---

# 82. 删除策略

用户删除：

```text
Xunara User
```

不能直接：

```text
DELETE Headscale User
```

必须经过：

```text
Account Deletion Workflow
```

包括：

```text
停止登录
撤销 Session
撤销 API Key
处理设备
处理 Tailnet
处理订阅
处理审计
最后删除
```

---

# 83. 数据导出

用户应该能够导出：

```text
账户信息
设备列表
网络配置
策略
DNS
Routes
```

格式：

```text
JSON
CSV
```

---

# 84. 可观测性

必须从第一天加入：

```text
Metrics
Logs
Tracing
Health
Audit
```

至少：

```text
Prometheus
OpenTelemetry
structured logging
```

---

# 85. Health API

提供：

```text
/health
/ready
/version
```

内部：

```text
Xunara
Database
Redis
Queue
Headscale
DERP
Billing
```

分别检查。

---

# 86. 安全原则

禁止：

```text
Frontend → Headscale Admin API
```

禁止：

```text
Frontend 保存 Headscale API Key
```

禁止：

```text
浏览器拥有超级管理员 Headscale Credential
```

禁止：

```text
用户直接访问 Headscale Database
```

禁止：

```text
用户提交任意 Headscale Policy JSON
```

普通模式必须经过：

```text
Validation
```

---

# 87. Secret 管理

所有：

```text
Headscale Credential
JWT Secret
OAuth Secret
Database Password
Payment Secret
DERP Secret
```

必须通过：

```text
Environment
Secret Manager
```

不得提交 Git。

---

# 88. AI 开发规则

任何 AI 开始工作前：

```text
1. 阅读 AI_DEVELOPMENT.md
2. 阅读 ARCHITECTURE.md
3. 阅读当前模块 README
4. 检查现有代码
5. 检查测试
6. 确认 Headscale 版本
7. 确认数据库 Migration
8. 再修改
```

---

# 89. AI 禁止行为

AI 不得：

```text
擅自重构整个项目
擅自更换框架
擅自修改数据库
擅自删除 API
擅自改变数据模型
擅自改变认证流程
擅自改变 Headscale Adapter
擅自取消官方客户端兼容
擅自修改网络分配规则
擅自修改套餐限制
```

如果确实需要：

```text
先提出 Architecture Change
```

---

# 90. AI 修改代码的原则

优先：

```text
最小修改
```

而不是：

```text
重新实现
```

每次修改：

```text
分析
↓
修改
↓
测试
↓
验证
↓
记录
```

---

# 91. Architecture Decision Record

重大决定必须建立：

```text
docs/adr/
```

例如：

```text
ADR-0001 Headscale Adapter
ADR-0002 Multi-Tenant
ADR-0003 Network Allocation
ADR-0004 Policy AST
ADR-0005 Official Client Compatibility
ADR-0006 Xunara Client Architecture
ADR-0007 Billing
```

---

# 92. Repository 推荐结构

```text
xunara/
├── apps/
│   ├── web/
│   ├── admin/
│   └── api/
│
├── services/
│   ├── identity/
│   ├── tenant/
│   ├── tailnet/
│   ├── device/
│   ├── network/
│   ├── policy/
│   ├── billing/
│   ├── entitlement/
│   ├── audit/
│   ├── notification/
│   └── reconciliation/
│
├── adapters/
│   ├── headscale/
│   ├── oauth/
│   ├── payment/
│   └── notification/
│
├── packages/
│   ├── policy-ast/
│   ├── network-cidr/
│   ├── api-types/
│   ├── auth/
│   └── capabilities/
│
├── clients/
│   └── xunara/
│
├── tools/
│   ├── diagnostics/
│   ├── network/
│   └── remote/
│
├── migrations/
│
├── docs/
│   ├── architecture/
│   ├── api/
│   ├── security/
│   ├── adr/
│   └── operations/
│
└── AI_DEVELOPMENT.md
```

实际技术栈可以根据项目启动阶段再确定。

---

# 93. 前端路由

用户端：

```text
/login
/register
/forgot-password

/dashboard

/account
/account/profile
/account/security
/account/sessions

/tailnet
/tailnet/devices
/tailnet/devices/:id
/tailnet/network
/tailnet/topology
/tailnet/permissions
/tailnet/members
/tailnet/dns
/tailnet/routes
/tailnet/exit-nodes
/tailnet/derp
/tailnet/api

/billing
/billing/plan
/billing/invoices

/settings
```

---

# 94. Admin 路由

```text
/admin

/admin/dashboard
/admin/users
/admin/users/:id

/admin/tailnets
/admin/tailnets/:id

/admin/devices
/admin/plans
/admin/subscriptions

/admin/networks
/admin/network-pools

/admin/derp
/admin/headscale

/admin/audit
/admin/events
/admin/system

/admin/settings
```

---

# 95. Future Client API

预留：

```text
/api/client/v1
```

例如：

```text
GET /api/client/v1/me
GET /api/client/v1/devices
GET /api/client/v1/network
GET /api/client/v1/topology
GET /api/client/v1/services
GET /api/client/v1/permissions
GET /api/client/v1/connection
```

未来 Xunara Client 不允许直接依赖 Web 页面 API。

---

# 96. API Versioning

必须：

```text
/api/v1
/api/v2
```

不能：

```text
/api
```

长期稳定接口必须保证向后兼容。

---

# 97. Capability API

客户端先获取：

```text
GET /api/v1/capabilities
```

例如：

```text
network.custom_cidr
device.max
policy.visual
policy.grants
route
exit_node
dns
derp
remote_tools
```

未来客户端根据 Capability 决定显示什么。

---

# 98. Feature Flag

未来功能使用：

```text
Feature Flag
```

例如：

```text
xunara_client
visual_policy
network_tools
remote_desktop
file_transfer
```

禁止通过修改代码硬编码上线状态。

---

# 99. 中国用户体验

默认语言：

```text
简体中文
```

未来：

```text
繁体中文
English
Japanese
```

所有文案必须国际化。

不能直接把中文写死在组件里。

---

# 100. 错误提示

不要：

```text
HTTP 403
```

直接显示给普通用户。

应该：

```text
无法访问此设备

原因：
当前网络策略不允许访问 NAS。

你可以：
查看访问权限
联系网络管理员
```

高级用户可以展开：

```text
Technical Details
```

---

# 101. 网络诊断

未来加入：

```text
诊断网络
```

自动测试：

```text
DNS
Control Server
DERP
Direct Connection
Latency
Packet Loss
Route
Policy
```

最终显示：

```text
✓ 登录正常
✓ Control Server 正常
✓ DERP 正常
✓ DNS 正常
✓ 网络策略正常
✓ 设备在线

网络状态：正常
```

---

# 102. 未来自有客户端的个人中心

Xunara Client 最终可以做到：

```text
Xunara Client
│
├── 网络
├── 设备
├── 拓扑
├── 服务
├── 权限
├── 诊断
├── 文件
├── 远程
└── 我的账户
```

其中：

```text
我的账户
```

与 Web Xunara 使用统一 Identity。

---

# 103. 自有客户端不是强制入口

这是非常重要的产品原则。

即使未来：

```text
Xunara Client
```

非常成熟，也不能强制：

```text
必须安装 Xunara Client
```

才能使用 Xunara 网络。

必须保持：

```text
Official Tailscale Client
```

继续可用。

---

# 104. Xunara Client 可以提供额外能力

例如：

```text
网络拓扑
服务发现
网络诊断
远程工具
个人中心
通知
设备健康
```

这些能力可以是 Xunara Client 独有的，但核心网络连接仍然必须兼容标准 Tailscale/Headscale 体系。

---

# 105. 最终平台愿景

Xunara 最终不是：

```text
Headscale UI
```

而是：

```text
                     Xunara
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     Web Console   Official Client  Xunara Client
        │              │              │
        └──────────────┼──────────────┘
                       │
                  Xunara Core
                       │
          ┌────────────┼────────────┐
          │            │            │
      Identity      Network      Business
          │            │            │
          │        Headscale       Billing
          │            │            │
          └────────────┼────────────┘
                       │
                 Network Platform
                       │
       ┌───────────────┼────────────────┐
       │               │                │
    Tailnet       Network Tools     Future Tools
       │               │                │
    Devices        Diagnostics      Remote Desktop
    Routes         Discovery        File Transfer
    DNS            SSH              IoT
    Policy         Speed Test       Enterprise
```

---

# 106. 开发阶段

## Phase 0：架构基础

必须先完成：

```text
Repository
Database
Identity
Tenant
Tailnet
Headscale Adapter
API
Audit
```

---

## Phase 1：MVP

实现：

```text
注册
登录
用户中心
Tailnet
设备
10 台 Free 限制
固定 Free 网络
官方 Tailscale Client
设备管理
基础权限
Admin
```

---

## Phase 2：网络产品

实现：

```text
自定义 CIDR
Routes
Exit Node
DNS
DERP
网络拓扑
权限矩阵
Visual Policy
Policy Explain
```

---

## Phase 3：商业化

实现：

```text
套餐
订阅
支付
账单
Entitlement
升级
降级
配额
```

---

## Phase 4：高级网络

实现：

```text
高级 Grants
设备组
服务组
策略模拟
网络诊断
实时拓扑
实时状态
```

---

## Phase 5：Xunara Client

实现：

```text
个人中心
设备中心
网络拓扑
服务发现
诊断
通知
网络工具
```

---

## Phase 6：Xunara Network Platform

未来：

```text
远程桌面
SSH
文件传输
内网服务
家庭网络
IoT
企业网络
自动化
网络监控
```

这些功能必须通过插件/模块架构加入。

---

# 107. Definition of Done

任何功能完成必须满足：

```text
[ ] 数据模型完成
[ ] API 完成
[ ] 权限完成
[ ] 套餐限制完成
[ ] 审计完成
[ ] 错误处理完成
[ ] 测试完成
[ ] Migration 完成
[ ] 文档完成
[ ] 官方客户端兼容测试
[ ] 向后兼容检查
[ ] 安全检查
```

---

# 108. AI 每次开发后的输出要求

AI 完成任务后必须说明：

```text
修改了什么
为什么修改
涉及哪些文件
是否修改数据库
是否修改 API
是否影响官方客户端
是否影响套餐
是否影响 Headscale
测试了什么
还有什么风险
```

---

# 109. AI 架构变更规则

如果修改：

```text
Database
Authentication
Headscale Adapter
Network Allocation
Policy Engine
Official Client Compatibility
Billing
Tenant Model
```

必须先提出：

```text
Architecture Change Proposal
```

不得直接改。

---

# 110. 永久架构红线

以下内容属于 Xunara 的长期不可破坏约束：

```text
1. Headscale 没有 Web UI，Xunara 自己提供完整 Web 产品层。

2. Xunara 用户身份与 Headscale 身份必须解耦。

3. Xunara 是多租户 SaaS。

4. Free 默认最多 10 台设备。

5. Free 网络 CIDR 不允许用户修改。

6. 付费套餐可以拥有自定义 CIDR 能力。

7. 套餐限制必须通过 Entitlement，而不是大量 if plan == xxx。

8. 官方 Tailscale Client 必须始终可用。

9. Xunara Client 是未来扩展，不得成为现阶段强制依赖。

10. Visual Policy 与底层 Grants/ACL 必须共享 Policy AST。

11. 普通用户默认通过可视化方式配置权限。

12. 必须提供拓扑图、设备矩阵、设备组、服务选择等多种权限配置方式。

13. 所有权限最终必须经过 Policy Compiler。

14. Route 与 Permission 必须严格分离。

15. Xunara 不直接依赖 Headscale 数据库内部表结构。

16. Xunara 通过 Headscale Adapter 与 Headscale 对接。

17. Headscale 版本升级不得导致 Xunara Core 大规模重写。

18. 用户数据、套餐、账单、审计属于 Xunara。

19. 网络控制状态属于 Headscale。

20. 所有关键操作必须可审计。

21. 所有重大架构变化必须记录 ADR。

22. 未来网络工具必须以独立模块接入。

23. Xunara Client、Web、Admin 必须共享统一 API/Domain Layer。

24. 不允许为了快速开发破坏未来扩展点。

25. AI 修改代码必须优先最小修改，禁止无必要的大规模重构。
```

---

# 111. AI 开发的最终判断标准

当 AI 不确定如何实现一个功能时，按照以下优先级判断：

```text
① 官方 Tailscale/Headscale 兼容性
        ↓
② Xunara 数据模型正确性
        ↓
③ 多租户安全隔离
        ↓
④ 用户体验
        ↓
⑤ 套餐/商业规则
        ↓
⑥ 可维护性
        ↓
⑦ 可扩展性
        ↓
⑧ 性能优化
```

如果一个“方便实现”的方案违反前面的原则：

```text
不要采用。
```

---

# 112. 最终目标

Xunara 最终应该让一个普通中国用户做到：

```text
注册 Xunara
      ↓
登录
      ↓
自动获得自己的网络
      ↓
安装官方 Tailscale
      ↓
加入 Xunara
      ↓
设备出现
      ↓
看到网络拓扑
      ↓
点击设备
      ↓
选择允许访问
      ↓
选择 Web / SSH / SMB
      ↓
完成组网
```

用户不需要理解：

```text
Headscale
WireGuard
DERP
ACL
Grants
CIDR
Control Plane
```

高级用户仍然可以看到：

```text
CIDR
Policy
Grants
ACL
Routes
DERP
API
```

最终形成：

```text
简单模式
    ↓
中国普通用户

高级模式
    ↓
极客 / 开发者

Admin
    ↓
平台运营者

API / SDK
    ↓
开发者

Xunara Client
    ↓
未来生态

Network Tools
    ↓
未来平台
```

**这就是 Xunara 的长期产品架构。**

以后任何 AI 接手项目，都必须以本文件作为第一约束，而不是根据自己的理解重新发明一套 Xunara 架构。