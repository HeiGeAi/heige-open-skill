# README 模板

两种款式。写之前先拉现行标杆对齐（模板会演化，以线上最新为准）：

```bash
gh api repos/HeiGeAi/HeiGe-SuanMing/readme --jq .content | base64 -d | head -80
```

## 旗舰款（徽章版）

适用：多 Agent 兼容的旗舰 skill、有商业化定位的项目。结构骨架：

```markdown
<div align="center">
  <img src="assets/cover.png" alt="<名字> · <一句话定位>" width="100%">
</div>

# <仓库名>

<div align="center">

![Skill](https://img.shields.io/badge/skill-<版本>-7c3aed.svg)
![Agents](https://img.shields.io/badge/agents-universal-orange.svg)
![Recommended](https://img.shields.io/badge/recommended-Claude%20Opus%204.8-d97706.svg)
![License](https://img.shields.io/badge/license-<协议徽章>.svg)

**<中文名> · <中文一句话> | <English slogan>**

<一句副标题，说清它到底干什么>

[这是什么](#这是什么-what-is-this) • [为什么不一样](#为什么不一样-why-its-different) • [快速开始](#快速开始-quick-start) • [多 Agent 支持](#多-agent-支持-works-with-any-agent) • [许可证](#许可证-license)

</div>

---

## 这是什么 What is this

<两三段说清定位和分层设计>

### 它能做什么

- ✅ <功能点，每条以能力动词开头>
- ✅ ...

### 适合谁

- <画像一>
- <画像二>

## 为什么不一样 Why it's different

| 维度 | 普通做法 | 本项目 |
|---|---|---|
| ... | ... | ... |

## 快速开始 Quick Start

<从 clone 到跑通第一个结果的完整命令，陌生人视角可复制粘贴>

## 多 Agent 支持 Works with any agent

<Claude Code 主推，Codex / Cursor / Cline 各一个 <details> 折叠安装块>

## English

<核心段落的英文镜像，覆盖 What is this / Quick Start>

## 致谢 | Credits

由 [@blakexu](https://github.com/HeiGeAi) 打造。<一句灵感来源>

## 许可证 | License

<按 license-guide.md 的对应模板>
```

### 徽章配色规范

| 徽章 | 值 | 颜色 |
|---|---|---|
| skill 版本 | `skill-x.y.z` | `7c3aed`（紫） |
| engine 版本（有独立引擎才加） | `engine-x.y.z` | `0e7490`（青） |
| Agent 定位（多 Agent 款） | `agents-universal` | `orange` |
| Agent 定位（纯 CC 款） | `Claude-Skill` + `best%20model-...` | 蓝系 |
| 推荐模型 | `recommended-Claude%20Opus%204.8` | `d97706`（琥珀） |
| License（MIT） | `license-MIT` | `green` |
| License（PolyForm） | `license-PolyForm%20NC` | `64748b`（灰蓝） |

工具类项目（如 HeiGe-GEO-SEO）可用简化徽章行：Version / License / Agents / 特色标签（如 `Market-China%20First`、`Python-stdlib%20only`、`tests-N%20passing`），不居中也行。

## 轻量款

适用：单一功能小工具（easy-read、corpus-cleaner 这个量级）。省徽章：

```markdown
# <repo-name> | <中文名>

> <一句话标语>

中文 | [English](#english)

<直接进正文：是什么、怎么装、怎么用>
```

## 双语铁律

- 中文为主，English 做镜像段或 README.en.md，两边内容同步更新
- 中文句子里全角标点，代码、命令、URL 保持半角
- 禁破折号，禁「不是X而是Y」句式，短句直述
