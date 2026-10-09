# 开发者指南

## 仓库与依赖

见 [REPOSITORIES.md](../../REPOSITORIES.md)。核心约束：单向依赖、无循环依赖、
不共享代码只共享协议与生成的类型。

## 本地开发

```sh
# 控制面（xunara-server）
go build ./... && go vet ./... && go test ./... -count=1

# 前端（xunara-web / xunara-admin）
npm ci && npm run dev          # dev 代理默认指向 127.0.0.1:8080（可用 XUNARA_CONTROL_URL 覆盖）
npx vue-tsc --noEmit && npx vitest run && npx vite build

# 中继（xunara-relay）
go test ./... -count=1
```

## 协议修改

改 TS2021 / Noise / MapRequest / MapResponse / NodeKey / MachineKey / DiscoKey /
Register / Poll / DNS / DERP / Capabilities / FeatureQuery 之前：读 upstream 源码与测试，
确认数据流，然后补 compatibility/integration 测试，并在提交信息里写清兼容性影响。

## Headscale Adapter

- 只经 Adapter 访问网络控制状态，不直接依赖 Headscale 内部表结构。
- Adapter 层负责版本差异，Headscale 升级不得导致 Core 大规模重写。
- 迁移只允许追加。

## 数据库

- 用户、套餐、账单、审计属于 Xunara；网络控制状态属于 Headscale。
- 新增迁移必须可回滚（至少可前滚修复），已发布条目只能追加。
- 涉及 Migration 的改动需要 Architecture Change Proposal。

## 发布（补充规范 §52–§56）

| 项目 | 约定 |
|---|---|
| 版本 | 各仓库独立 SemVer |
| 镜像 | `ghcr.io/xunara-net/<repo>:<version>`，多架构 amd64/arm64 |
| 产物 | Release + SBOM + 变更摘要 + 升级/回滚说明 |
| 兼容 | server/relay 兼容矩阵写入 Release Notes |
| 依赖 | Dependabot / Renovate 跟踪升级 |

## 测试责任

协议兼容、租户隔离、Session/Identity、并发路径必须覆盖测试；只加功能不加测试的 PR
不予合入。

## 中文注释与旧实现清理

- 关键模块用中文解释身份/租户边界、事务原子性、挑战重放和兼容适配的原因，
  不逐行翻译显而易见的语句，不把已删除的实现整段注释后保留。
- 清理前搜索定义、生产调用与测试；功能对等后移除旧 UI 与重复业务逻辑。
  已公开地址按弃用、提示、迁移和最终删除推进；必要兼容入口只适配传输与字段形状，
  必须复用同一账户域逻辑，不能绕过权限或审计。实践见
  [ADR-0011](https://github.com/xunara-net/xunara-server/blob/main/docs/adr/ADR-0011-passkey-web-and-auth-consolidation.md)。
- 官方客户端的浏览器授权及尚未完成独立 Web 对等的模块不能为“清理”直接删除。
  修改已发布的数据库迁移、放宽协议或安全限制也不是合法的清理方式。
