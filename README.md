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

## 点击学习链路

按下面顺序点，不要跳。每一站都要做到“读完、手算、跑命令、过验收”。

### 0. 先建立脑子里的地图

| 顺序 | 学习入口 | 你要学会什么 |
| --- | --- | --- |
| 0.1 | [小白心智模型](docs/beginner_mental_model.md) | 先明白量化不是预测涨跌，而是检查一类下注是否长期划算 |
| 0.2 | [最小数学](docs/math_core.md) | 百分比、复利、期望值、回撤、相关性、夏普 |
| 0.3 | [学习路线总览](curriculum/README.md) | 四阶段路线、模块门禁、每阶段通过标准 |
| 0.4 | [12 周学习计划](docs/study_plan.md) | 每周读什么、跑什么、手算什么、输出什么 |
| 0.5 | [量化交易原理](docs/principles.md) | 想法、数据、规则、回测、反证、风控、复盘的完整链条 |
| 0.6 | [检查清单](docs/checklists.md) | 防止被漂亮回测和复杂模型骗 |

### 1. 课程模块和练习

| 模块 | 课程 | Lab | 建议命令 | 过关标准 |
| --- | --- | --- | --- | --- |
| 00 | [小白预备课](curriculum/modules/00_beginner_preflight.md) | [Lab 00](labs/00_beginner_preflight/README.md) | `make lesson00` | 能解释为什么高胜率也会亏钱 |
| 01 | [市场、收益和基准](curriculum/modules/01_market_basics.md) | [Lab 01](labs/01_returns_drawdown/README.md) | `make lesson01` | 能手算收益、权益曲线、最大回撤 |
| 02 | [数据契约和偏差](curriculum/modules/02_data_contracts.md) | [Lab 02](labs/02_data_bias_checks/README.md) | `python3 -m unittest tests.test_data` | 能指出前视、幸存者、复权和异常字段问题 |
| 03 | [回测引擎](curriculum/modules/03_backtesting.md) | [Lab 03](labs/03_backtest_delay_costs/README.md) | `make demo` | 能解释信号延迟、费用、权益曲线怎么来的 |
| 04 | [风险和仓位](curriculum/modules/04_risk_positioning.md) | [Lab 04](labs/04_position_sizing/README.md) | `python3 -m unittest tests.test_risk` | 能把买入信号翻译成仓位、止损、最大亏损 |
| 05 | [因子研究](curriculum/modules/05_factor_research.md) | [Lab 05](labs/05_factor_ic/README.md) | 先手算 | 能解释横截面排序、IC、分组收益、换手 |
| 06 | [组合构建](curriculum/modules/06_portfolio.md) | [Lab 06](labs/06_portfolio/README.md) | 先手算 | 能解释权重、相关性、集中度、再平衡 |
| 07 | [机器学习](curriculum/modules/07_machine_learning.md) | [Lab 07](labs/07_machine_learning/README.md) | 先画窗口 | 能画清特征窗口、标签窗口、泄漏边界 |
| 08 | [执行和复盘](curriculum/modules/08_execution_review.md) | [Lab 08](labs/08_execution_review/README.md) | 写审判卡 | 能写纸面交易规则、亏损分类、下线条件 |

### 2. 进阶专题

完成 00-08 后再读这些。没完成前读也可以，但不要急着照做。

| 顺序 | 专题 | 用途 |
| --- | --- | --- |
| A1 | [Qlib 深入分析](docs/qlib_deep_dive.md) | 理解 Qlib 为什么是 AI 量化研究流水线，不是小白第一课 |
| A2 | [进攻性量化模型 2026](docs/aggressive_quant_models_2026.md) | 理解 agentic alpha factory、Qlib/R&D-Agent、Mamba、LOB Transformer 等方向 |
| A3 | [研究协议](docs/research_protocol.md) | 每个策略研究如何留证据链 |
| A4 | [交易审判卡](docs/trade_review_template.md) | 把研究结果变成行动前的冷酷审查 |
| A5 | [资料来源](docs/source_notes.md) | 当前工具判断和参考来源 |
| A6 | [术语表](docs/glossary.md) | 查概念 |

### 3. 代码阅读顺序

课程读到对应模块时，再点代码，不要一开始就扎进实现。

| 顺序 | 代码 | 对应模块 |
| --- | --- | --- |
| C1 | [lessons.py](src/quant_learning/lessons.py) | 00-01 入门练习 |
| C2 | [data.py](src/quant_learning/data.py) | 02 数据契约 |
| C3 | [metrics.py](src/quant_learning/metrics.py) | 01 收益、波动、回撤 |
| C4 | [strategy.py](src/quant_learning/strategy.py) | 03 信号 |
| C5 | [backtest.py](src/quant_learning/backtest.py) | 03 回测 |
| C6 | [risk.py](src/quant_learning/risk.py) | 04 风险和仓位 |
| C7 | [factors.py](src/quant_learning/factors.py) | 05 因子 |
| C8 | [run_demo.py](src/quant_learning/run_demo.py) | 03 完整 demo |

### 4. 测试和验证

学习时随时跑：

```bash
make lesson00
make lesson01
make demo
make check
```

测试文件也可以点开看，它们代表这个仓库最小的“不要骗自己”规则：

- [test_lessons.py](tests/test_lessons.py)
- [test_data.py](tests/test_data.py)
- [test_metrics.py](tests/test_metrics.py)
- [test_strategy_backtest.py](tests/test_strategy_backtest.py)
- [test_risk.py](tests/test_risk.py)

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

不急着上复杂库。先把小样本手算、标准库脚本和测试跑明白。
