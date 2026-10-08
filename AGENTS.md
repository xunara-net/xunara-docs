# AGENTS.md — xunara-docs 仓库

本仓库是 Xunara 的文档中心，只放规格、架构、ADR 索引、手册与运维文档。

## 规则

1. 改文档前先读 [AI_DEVELOPMENT.md](AI_DEVELOPMENT.md) 与
   [specs/](specs/) 下的两份权威规范。
2. `specs/` 下的规格全文**只允许追加与勘误**；不得为了配合当前实现改写结论。
   发现规格与实现冲突时，先提 Architecture Change Proposal，再改代码或规格。
3. 文档中的命令必须可直接复制执行，并标注执行目录与前置条件。
4. 不要在本仓库复制会漂移的实现细节（接口字段、表结构、端口清单）——引用对应仓库的
   文件链接，或明确写明"以 <仓库> 为准"。
5. 新增文档后更新 [README.md](README.md) 的目录与索引。
6. 提交信息使用中文五段式（见 [CONTRIBUTING.md](CONTRIBUTING.md)）。

## 禁止

- 不写未经验证的能力（例如把规划中的功能写成已实现）。
- 不在文档中放置任何 Secret、Token、证书指纹私钥或真实账号口令。
