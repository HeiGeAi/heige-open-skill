# 协议选型指南

## 决策规则

- **MIT**：默认选项。纯工具、无商业顾虑的项目，口径是「随便用随便改随便分享」。
- **PolyForm Noncommercial 1.0.0**：商业化重、可货币化的旗舰 skill。它能挡未授权商用，MIT 挡不了。
- 拿不准就和负责人确认一句，一句话的事，别猜。

## MIT 生成

标准 MIT 文本，Copyright 行写：

```
Copyright (c) <年> HeiGeAi (Blake Xu)
```

## PolyForm NC 生成

官方文本从这里拉：

```bash
curl -sL https://raw.githubusercontent.com/polyformproject/polyform-licenses/1.0.0/PolyForm-Noncommercial-1.0.0.md -o LICENSE
```

然后在文件**开头插入一行**（PolyForm 要求的 Required Notice）：

```
Required Notice: Copyright <年> HeiGeAi (Blake Xu) (https://github.com/HeiGeAi)
```

两个注意点：

1. PolyForm NC 是 source-available，属于非 OSI 纯开源，GitHub 的协议识别会把它标成 Other，这是正常现象。
2. README 的许可证段落要按要点清单写（仿 guizang）：非商业免费 / 必须署名 / 禁止商用 / 商用先授权，附英文一句。

## README 许可证段落模板

**MIT 版：**

```markdown
## 许可证 | License

MIT。随便用，随便改，随便分享。

MIT License. Use it, fork it, share it.
```

**PolyForm NC 版：**

```markdown
## 许可证 | License

[PolyForm Noncommercial 1.0.0](LICENSE)

- ✅ 个人使用、学习、研究免费
- ✅ 修改、分发，保留署名即可
- ❌ 未经授权的商业使用
- 💼 商用请先联系授权：[@HeiGeAi](https://github.com/HeiGeAi)

Free for noncommercial use. For commercial licensing, contact [@HeiGeAi](https://github.com/HeiGeAi).
```

## 玄学 / 算命类项目的合规要求

定位必须是「传统文化数字化研究 + 自我认知工具」：

- 宣传语不宣扬封建迷信，无「改运」「消灾」「转运」承诺
- 无付费诱导
- 脚本和文档带「仅供研究参考」声明
- 断语克制：断语止于月不做每日吉凶、合婚只断相处模式不打分不下合不合判词
