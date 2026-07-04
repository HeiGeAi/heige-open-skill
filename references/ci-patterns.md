# CI 模式

加 CI 的前提：项目自带确定性校验脚本（validate / build / tests）。README 里挂了 CI 绿徽章却没实质校验，属于装样子，别加。

## 模式一：Python 项目（HeiGe-GEO-SEO 实例）

多版本矩阵 + 构建 + 自检 + 单测 + 冒烟门槛：

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  verify:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.9", "3.11", "3.12"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
      - name: 构建
        run: python3 build.py
      - name: 完整性自检
        run: python3 validate.py
      - name: 单元测试
        run: python3 -m unittest discover -s tests -p "test_*.py"
```

有可量化门槛的加冒烟步骤（如评分器 `--fail-under 70`），CI 直接当质量闸门。

## 模式二：Node 构建链（200-agent 实例）

校验 + 构建两步，步骤名用中文说清卡什么：

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:

jobs:
  validate-and-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: 校验(硬卡数量、slug 唯一、字段齐全)
        run: node build/validate.mjs
      - name: 构建产物
        run: node build/build.mjs
```

## 约定

- workflow 文件统一 `.github/workflows/ci.yml`，名字就叫 `CI`
- 步骤名允许中文，写清这步卡的是什么
- CI 绿了再在 README 上挂 tests 徽章，数字和实际对齐
