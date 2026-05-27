# 12 周学习计划

这个计划给小白用。不要追求快，追求每一步能讲清楚。

## 总规则

- 每次学习先读模块，再手算，再跑代码。
- 每周至少写一条“我之前误解了什么”。
- 每个策略想法先写反方观点。
- 没过阶段门禁，不升级工具。
- 学习阶段不做真钱交易。

## 第 1 周：正期望和小白地基

读：

- `docs/beginner_mental_model.md`
- `curriculum/modules/00_beginner_preflight.md`

跑：

```bash
make lesson00
```

手算：

- 设计一个胜率高但亏钱的游戏。
- 设计一个胜率低但赚钱的游戏。

输出：

- 用自己的话解释“为什么胜率不是核心”。
- 写一个交易想法，并写出最强反方观点。

## 第 2 周：价格、收益、权益

读：

- `curriculum/modules/01_market_basics.md`

跑：

```bash
make lesson01
```

手算：

- 用 `data/samples/ohlcv_demo.csv` 前 6 天收盘价计算逐日收益。
- 计算买入持有权益曲线。
- 找最大回撤。

输出：

- 解释为什么 +10% 后 -10% 不是回到原点。
- 比较最终收益和最大回撤哪个更影响真实执行。

## 第 3 周：数据契约

读：

- `curriculum/modules/02_data_contracts.md`
- `src/quant_learning/data.py`

跑：

```bash
python3 -m unittest tests.test_data
```

练习：

- 复制 sample CSV，制造负价格、重复日期、缺字段。
- 观察加载器如何失败。

输出：

- 写一份 OHLCV 数据契约。
- 用一句话解释前视偏差。

## 第 4-5 周：回测引擎

读：

- `curriculum/modules/03_backtesting.md`
- `src/quant_learning/backtest.py`
- `src/quant_learning/strategy.py`

跑：

```bash
make demo
python3 -m unittest tests.test_strategy_backtest
```

练习：

- 把 `--fee-bps` 从 5 改成 50。
- 比较交易次数、费用、最终权益。
- 手算一段 3 天价格的权益变化。

输出：

- 解释为什么当前回测使用上一根 K 线信号。
- 写出一个会作弊的错误回测规则。

## 第 6 周：风险和仓位

读：

- `curriculum/modules/04_risk_positioning.md`
- `src/quant_learning/risk.py`

跑：

```bash
python3 -m unittest tests.test_risk
```

练习：

- 用不同入场价、止损价、目标价计算仓位。
- 设计一个盈亏比高但不值得做的例子。

输出：

- 写一张交易审判卡，结论可以是 `kill`。

## 第 7-8 周：因子研究

读：

- `curriculum/modules/05_factor_research.md`
- `src/quant_learning/factors.py`

练习：

- 计算 5 日动量。
- 给多个假资产排序。
- 比较高分组和低分组未来收益。

输出：

- 解释为什么因子有效不等于策略可交易。
- 写出换手如何杀死一个因子。

## 第 9 周：组合构建

读：

- `curriculum/modules/06_portfolio.md`

练习：

- 手算三资产等权组合收益。
- 限制单资产最大权重。
- 比较日频和周频再平衡的换手。

输出：

- 解释为什么买 20 只同一行业股票不算真正分散。

## 第 10-11 周：机器学习

读：

- `curriculum/modules/07_machine_learning.md`
- `docs/qlib_deep_dive.md`
- `docs/aggressive_quant_models_2026.md`

练习：

- 画出特征窗口和标签窗口。
- 找出训练/测试边界附近的泄漏样本。
- 暂时只分析 Qlib 架构，不安装、不跑复杂模型。

输出：

- 解释为什么随机交叉验证在金融时间序列里危险。
- 写出模型输出如何变成仓位。

## 第 12 周：执行和复盘

读：

- `curriculum/modules/08_execution_review.md`
- `docs/trade_review_template.md`

练习：

- 选一个想法，写纸面交易规则。
- 写下线条件。
- 写亏损分类标准。

输出：

- 一份完整交易审判卡。
- 一个明确结论：`kill`、`observe`、`paper_trade` 或 `promote`。
