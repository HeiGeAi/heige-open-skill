# Changelog

## [1.0.2] - 2026-09-13

### Fixed

- git 历史身份闸门补扫 committer 邮箱, author 与 committer 统一校验 noreply。
- 历史检查改 fail-closed: 仅空仓库按空历史跳过, 其余 git 失败一律 ERROR。
- SKILL.md 带 UTF-8 BOM 时 frontmatter 不再误报缺失。
- 无 git 环境下给出明确 WARN 提示, 不再 traceback 崩溃。
- 域名与 GitHub 句柄清单超 20 条时标注省略条数。
- docstring 与 .gitignore 检查级别对齐。

## [1.0.1] - 2026-07-31

- 将发布前检查和单元测试接入 GitHub Actions。
- 新增私密安全报告入口。
- 保留现有零依赖 preflight 契约。
