# 发布前人工自查清单

多轮发布审查固化，覆盖最常见的发布事故。preflight 脚本查确定性项，这五类必须人工过。每项过完在汇报里打勾。

## 1. 虚构实体核查

示例、文档里出现的每个外部实体，逐一确认它指向不了真实第三方：

| 实体类型 | 核查方法 | 安全写法 |
|---|---|---|
| 域名 | RDAP / DoH 查注册状态：`curl -s https://rdap.org/domain/<域名>` | 保留 TLD：`.example`、`example.com`、`.invalid`、`.test` |
| 邮箱域 | 查 MX：`dig MX <域名> +short` | `user@example.com` |
| GitHub 句柄 | `gh api users/<句柄>` 查存在 | 用 GitHub 非法格式（含下划线）：`your_username` |
| 公司 / 店铺名 | 全网搜索确认 0 命中 | 虚构商业案例带「纯属虚构」声明 |
| 虚构项目名 | 先搜全站 0 命中再用 | 命中了就换名 |

preflight 脚本会把发现的域名、邮箱、句柄列成清单，照单核查即可。

## 2. skill 三一致（skill 类仓库专属）

三个名字必须完全相等：

1. 安装落地目录名（`~/.claude/skills/<这里>`）
2. SKILL.md frontmatter 的 `name:`
3. 文档里教用户的 `/调用命令`

frontmatter 顶层只允许 `name` / `description` / `allowed-tools` / `compatibility` / `license` / `metadata` 六个键，`author`、`version` 之类的放 `metadata:` 下面。preflight 会查这条，这里是提醒来源。

## 3. 改示例必同步截图

示例 HTML / 模板改了内容，对应 previews 截图画面里还烤着旧内容，这就是不一致。修法：

- 同一个 commit 里重做截图
- playwright 同视口截图，`cwebp` 对齐旧图尺寸
- 检查方法：打开每张截图，逐一和当前示例内容比对文字

## 4. 修复收尾按概念 grep

修完一个问题，把它的**所有表述形式**都搜一遍，光搜字面会漏。例：修完 .skill 下载链接，还要搜「压缩包」「下载」「release」这些中文表述。做法：

1. 列出这个问题的 3 到 5 种说法（中文、英文、代码标识符）
2. 每种说法全仓 grep 一遍
3. 全部命中处确认改净

## 5. 黄金路径 + 链接 + 身份

- **黄金路径**：陌生人视角，从 README 第一行开始，clone、安装、跑通第一个结果，每条命令真实执行一遍
- **外链存活**：README 里每个外链 curl 一遍（preflight `--check-links` 可代跑）；注意 raw.githack 屏蔽 HEAD 请求会误报 403，改用 GET 复核
- **提交身份**：`git log --format='%an %ae' | sort -u`，只允许 `HeiGeAi` + noreply 地址；`git log --format='%B' | grep -i co-authored` 必须为空
