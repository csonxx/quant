# quant

这是一个独立的量化交易学习仓库，不绑定任何已有项目。目标不是堆指标、调参数、做漂亮回测，而是训练一套能把交易想法拆成数据、假设、回测、风险、执行和复盘的研究框架。

一句狠话：量化学习的第一课不是“怎么找到赚钱策略”，而是“怎么尽快证明大多数策略不能赚钱”。活下来的少数想法，才值得继续深化。

## 快速开始

```bash
cd /Users/tt/goworkspace/src/csonxx/quant
make lesson00
make lesson01
make demo
make test
```

当前代码骨架只依赖 Python 标准库，先保证学习闭环可跑。等每个原理吃透后，再按需引入 `pandas`、`numpy`、`vectorbt`、`Qlib`、`LEAN` 等更重的工具。

## 仓库结构

```text
.
├── README.md
├── Makefile
├── pyproject.toml
├── curriculum/          # 学习路线，每个模块都有交付物和验收门槛
├── docs/                # 原理、研究协议、交易审判卡、资料来源
├── labs/                # 练习入口，后续每个模块加 notebook 或脚本
├── notebooks/           # 只放探索；正式逻辑要回写到 src/ 和 tests/
├── data/                # sample/raw/interim/processed 分层
├── src/quant_learning/  # 最小量化研究代码骨架
├── tests/               # 用测试防止自己骗自己
├── artifacts/           # 模型、回测中间产物，不默认入库
└── reports/             # 研究报告、复盘、交易审判输出
```

## 学习主线

这套学习路线分四阶段走，不建议跳级。

1. 小白地基：先理解交易是在做不确定下注，补齐 Python、表格数据、概率和期望值的最低常识。
2. 单资产闭环：只研究一个标的，把价格、收益、数据偏差、信号、回测、成本、风控彻底讲清楚。
3. 多资产研究：再进入因子、组合、相关性、换手、容量，学习为什么“选对股票”不等于“组合赚钱”。
4. 模型和执行：最后才碰机器学习、纸面交易、监控、复盘和下线机制。

每一阶段都有门禁。门禁没过，不升级工具；能用手算和小样本讲清楚，才允许扩大数据和框架。

## 硬规则

- 回测好看，默认先判假，直到它通过样本外、成本、换手、容量和反例审查。
- 指标不是策略。策略必须能回答：买什么、买多少、何时买、何时卖、错了怎么办。
- 模型分数不是交易结论。分数必须被翻译成仓位、风险预算和执行规则。
- 任何研究都要有可复现输入、代码、参数、输出和失败记录。
- 不做裸奔优化：没有基准、没有成本、没有样本外，就没有结论。

## 当前可运行骨架

- `src/quant_learning/data.py`：OHLCV CSV 数据契约和加载。
- `src/quant_learning/strategy.py`：移动均线交叉信号，演示信号如何产生。
- `src/quant_learning/backtest.py`：长仓信号回测，刻意使用上一根 K 线信号，避免同日偷看。
- `src/quant_learning/metrics.py`：收益、波动、夏普、最大回撤。
- `src/quant_learning/risk.py`：单笔风险、盈亏比、交易计划审查。
- `data/samples/ohlcv_demo.csv`：最小样例数据。

下一步深化时，优先按这个顺序读：

1. `docs/beginner_mental_model.md`
2. `docs/math_core.md`
3. `curriculum/README.md`
4. `docs/study_plan.md`
5. `docs/principles.md`
6. `docs/qlib_deep_dive.md`
7. `docs/aggressive_quant_models_2026.md`

不急着上复杂库。先把小样本手算、标准库脚本和测试跑明白。
