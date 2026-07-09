# heige-open-skill

![Skill](https://img.shields.io/badge/skill-1.0.0-7c3aed.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Agents](https://img.shields.io/badge/agents-Claude%20Code%20·%20Codex%20·%20Cursor-orange.svg)
![Python](https://img.shields.io/badge/python-stdlib%20only-yellow.svg)

> 一套把项目开源发布到 GitHub 的可执行流水线。协议选型、双语 README、CI、提交身份规范、发布前硬检查，一条龙走完，别再靠记。
>
> A repeatable pipeline for shipping a project to GitHub: license choice, bilingual README, CI, commit-identity rules, and a preflight hard-check. Stop relying on memory.

中文 | [English below](#english)

---

## 这是什么

`heige-open-skill` 是一个 AI Agent skill。把「我要开源这个项目」这句话，变成一条固定走完的发布流水线。

它解决的是一类真实的痛：开源发布看着简单，其实到处是坑。私人邮箱混进公开 git 历史、示例里写了真实存在的域名、skill 的目录名和 frontmatter 对不上、README 挂着打不开的外链。这些错误发出去就是公开事故，删库也洗不干净。

这套 skill 把发布拆成 8 步，其中确定性的检查交给 `preflight.py` 脚本自动跑，人祸类的检查列成清单人工过。规范以 HeiGeAi 组织的实际做法为范本，fork 后把组织名、提交身份换成你自己的即可。

## 能做什么

| 你的需求 | 流水线给你 |
|---|---|
| 该用什么协议 | MIT / PolyForm NC 决策表 + 官方文本拉取命令 |
| README 怎么写 | 旗舰款 / 轻量款两套骨架 + 徽章配色规范 |
| 要不要加 CI | 两个真实 CI 模式（Python 矩阵 / Node 构建链） |
| 提交身份怎么定 | 固定 noreply 身份，绝不泄私人邮箱 |
| 发布前查什么 | preflight 脚本查 6 类硬项 + 5 类人工清单 |

`preflight.py` 零依赖，检查：必备文件、LICENSE 合规、git 历史邮箱泄露、Co-Authored-By 残留、skill frontmatter 三一致、外部实体清单、外链存活。

## 为什么不一样

| 维度 | 普通发布 | 本流水线 |
|---|---|---|
| 检查方式 | 全靠人记，发完才发现漏 | 确定性项脚本硬卡，ERROR 清零才让 push |
| 身份泄露 | 私人邮箱经常混进历史 | 固定 noreply 身份 + 历史扫描 |
| 虚构实体 | 示例常引到真实第三方 | 脚本列清单，逐一 RDAP / MX 核查 |
| 一致性 | 目录名和 frontmatter 常打架 | 三一致检查内建 |

## 快速开始

装进 Claude Code 的 skills 目录：

```bash
git clone https://github.com/HeiGeAi/heige-open-skill.git
ln -s "$(pwd)/heige-open-skill" ~/.claude/skills/heige-open-skill
```

之后在会话里说「把这个项目开源」「发布前检查一下」，skill 会自动触发。也可以单独跑硬检查：

```bash
python3 ~/.claude/skills/heige-open-skill/scripts/preflight.py <你的仓库路径> --check-links
```

看到 `0 ERROR` 就过了硬闸门，再按 `references/checklist.md` 过一遍人工清单，就可以 push。

## 多 Agent 支持

主推 Claude Code。其他会读文件、能调 Python 的 agent 也能用。

<details>
<summary>Codex / Cursor / Cline</summary>

把仓库目录喂给 agent，让它读 `SKILL.md` 作为发布流程说明，`preflight.py` 直接命令行跑即可。脚本只依赖 Python 标准库，无需安装任何包。

</details>

## English

`heige-open-skill` is an AI-Agent skill that turns "let's open-source this" into a fixed 8-step release pipeline.

Open-source publishing looks trivial but is full of traps: a personal email leaking into public git history, example domains that point at real third parties, a skill whose directory name and frontmatter disagree, a README with dead links. Once pushed, these are public incidents that a force-push can barely clean up.

The skill splits publishing into 8 steps. Deterministic checks run through `preflight.py`; human-judgment checks go on a checklist. Conventions follow the HeiGeAi org as a template. Fork it and swap in your own org name and commit identity.

```bash
git clone https://github.com/HeiGeAi/heige-open-skill.git
ln -s "$(pwd)/heige-open-skill" ~/.claude/skills/heige-open-skill
python3 ~/.claude/skills/heige-open-skill/scripts/preflight.py <your-repo> --check-links
```

## 致谢 | Credits

由 [@blakexu](https://github.com/HeiGeAi) 打造，从十几个真实开源仓库的发布踩坑里反推固化。

Built by [@blakexu](https://github.com/HeiGeAi), distilled from the release mistakes of a dozen real repositories.

## 许可证 | License

MIT。随便用，随便改，随便分享。

MIT License. Use it, fork it, share it.

## 更多开源工具

本项目属于黑哥 AI 的开源武器库。全部开源项目的清单、用途和协议,见 [heigeai.com/opensource](https://www.heigeai.com/opensource/)。
