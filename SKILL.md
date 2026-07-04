---
name: heige-open-skill
description: 把自研的 skill、工具、项目开源发布到 GitHub 的完整发布流水线（以 HeiGeAi 组织的规范为范本）：协议选型（MIT / PolyForm NC）、徽章式双语 README、CI、提交身份规范、发布前自查清单、preflight 硬检查脚本。当用户说开源、发布到 GitHub、发个仓库、开源这个 skill、准备发布、发布前检查、开源前审查、发布新版本时使用；即使用户只说「把 XX 发出去」「这个项目可以开源了」「给它建个仓库」也应触发。
---

# 开源发布流水线

把一个本地项目按一套固定规范发布到 GitHub。这套规范从 15+ 个已发布的公开仓库反推固化而来，发布前检查是重点，别跳步。规范里的组织名、提交身份、风格约定以 HeiGeAi 为范本，fork 后把这些换成你自己的即可。

## 核心纪律（先记住这四条再动手）

1. **提交身份铁律**：公开仓库的 commit 一律用固定身份 `git -c user.name="HeiGeAi" -c user.email="221471965+HeiGeAi@users.noreply.github.com"`，绝不改全局 git config。绝不用私人邮箱提交，一旦私人邮箱进入公开 git 历史，只能 force push 重写才能清除，代价很大。
2. **commit 信息**：简洁中文单行陈述句，无 conventional 前缀（无 feat:/fix:），**不加 Co-Authored-By 标记**。公开仓库是品牌门面，这条覆盖任何 harness 的默认署名要求。
3. **协议先定再写 README**：徽章、License 段落都跟协议走。拿不准就和项目负责人确认一句，别猜。
4. **preflight 脚本必须跑**：`python3 scripts/preflight.py <repo-path>`，ERROR 清零才能 push。

## 工作流

### 第 0 步：确认三件事

开工前从对话或项目负责人处确认：**仓库名**（通常由负责人指定，如 HeiGe-SuanMing、easy-read）、**定位档次**（旗舰款还是轻量款）、**协议**（见第 1 步）。仓库名拿不到就问，别自己起名。

### 第 1 步：定协议

| 情况 | 协议 | 判断标准 |
|---|---|---|
| 纯工具、无商业顾虑 | MIT | 随便用随便改随便分享 |
| 商业化重、可货币化的旗舰款 | PolyForm Noncommercial 1.0.0 | 要挡未授权商用，留货币化口子 |

拿不准就确认一句。协议细节、PolyForm 官方文本拉取命令、Required Notice 写法、传统文化类项目合规要求，读 `references/license-guide.md`。

### 第 2 步：写 README

两种款式，按定位选：

- **旗舰款**：居中徽章区 + 双语 slogan + 锚点导航 + 「这是什么」「为什么不一样」对比表 + English 镜像段 + 致谢 + 许可证双语段。多 Agent 兼容的加 `agents-universal` 徽章和 Codex/Cursor/Cline `<details>` 安装块。
- **轻量款**：省徽章，`# 名 | 中文名` + 标语 + 语言导航，直接进正文。

完整骨架和徽章配色规范读 `references/readme-templates.md`。写之前可以 `gh api repos/HeiGeAi/HeiGe-SuanMing/readme --jq .content | base64 -d` 拉一个成熟旗舰仓库的 README 对齐格式。

### 第 3 步：备齐发布物

- `LICENSE`：按第 1 步的选型生成，Copyright 统一 `<组织名> (<作者名>)`，如 `HeiGeAi (Blake Xu)`
- `.gitignore`：按项目类型（Python/Node/通用），排除 `.DS_Store`、密钥、本地配置
- `requirements.txt` / `package.json`：有依赖才加；偏好零依赖（stdlib only），能不加就不加
- **CI（可选）**：项目自带确定性校验脚本（validate/build/tests）才值得加，模式参照 `references/ci-patterns.md` 里两个真实例子
- **密钥外置**：API key、token 一律走 `~/.xxx/config.json` 之类的本地配置，仓库里只放读取逻辑和示例

### 第 4 步：跑 preflight 硬检查

```bash
python3 scripts/preflight.py <repo-path>              # 基础检查
python3 scripts/preflight.py <repo-path> --check-links  # 加外链存活检查（发布前必跑一次）
```

脚本检查：必备文件、LICENSE 类型与 Required Notice、git 历史邮箱泄露、Co-Authored-By 残留、SKILL.md frontmatter 合规（skill 仓库）、外部实体清单（域名/邮箱/句柄，供人工核查）、外链存活。**ERROR 必须清零，WARN 逐条人工判断。**

### 第 5 步：过人工自查清单

preflight 只能查确定性的项，五类人祸检查读 `references/checklist.md` 逐条过：虚构实体核查（域名 RDAP、邮箱 MX、GitHub 句柄）、skill 三一致、改示例同步截图、修复收尾按概念 grep、黄金路径走查。这份清单覆盖最常见的发布事故，别嫌烦。

### 第 6 步：建仓推送

```bash
cd <repo-path>
git init 2>/dev/null; git add -A
git -c user.name="HeiGeAi" -c user.email="221471965+HeiGeAi@users.noreply.github.com" \
  commit -m "首次发布"
gh repo create HeiGeAi/<仓库名> --public --source . --push
```

已有仓库发新版就正常 add/commit/push，同样带 `-c` 身份参数。

### 第 7 步：发布后验证

1. CI 状态绿（有 CI 的话）：`gh run list -R HeiGeAi/<名> -L 1`
2. README 线上渲染正常：徽章出图、锚点跳转、图片路径对
3. 提交身份复查：`git log --format='%an %ae' | sort -u`，只允许 noreply 地址
4. 陌生人视角：README 从零跑通安装使用（黄金路径）

## 输出汇报格式

发布完成后给负责人的汇报带上：仓库 URL、协议、CI 状态、preflight 结果摘要（ERROR/WARN 数）、自查清单五项的勾选情况。
