# 学习进度表

用途：打开这份表，按顺序打勾。不要靠“看过了”判断学会，要靠能不能手算、跑命令、解释结果。

## 阶段 0：小白地基

- [ ] 读完 [小白心智模型](beginner_mental_model.md)。
- [ ] 读完 [最小数学](math_core.md)。
- [ ] 跑通 `make lesson00`。
- [ ] 能解释为什么 80% 胜率也可能亏钱。
- [ ] 能设计一个低胜率但正期望的例子。
- [ ] 能说明“我觉得会涨”为什么不是策略。

不满足以上条件，不进入阶段 1。

## 阶段 1：单资产闭环

- [ ] 读完 [01 市场、收益和基准](../curriculum/modules/01_market_basics.md)。
- [ ] 完成 [Lab 01](../labs/01_returns_drawdown/README.md)。
- [ ] 跑通 `make lesson01`。
- [ ] 能手算逐日收益和买入持有权益曲线。
- [ ] 能计算最大回撤。
- [ ] 读完 [02 数据契约和偏差](../curriculum/modules/02_data_contracts.md)。
- [ ] 完成 [Lab 02](../labs/02_data_bias_checks/README.md)。
- [ ] 能解释前视偏差、幸存者偏差、复权偏差。
- [ ] 读完 [03 回测引擎](../curriculum/modules/03_backtesting.md)。
- [ ] 完成 [Lab 03](../labs/03_backtest_delay_costs/README.md)。
- [ ] 跑通 `make demo`。
- [ ] 能解释为什么本仓库用上一根 K 线信号执行。
- [ ] 读完 [04 风险和仓位](../curriculum/modules/04_risk_positioning.md)。
- [ ] 完成 [Lab 04](../labs/04_position_sizing/README.md)。
- [ ] 能把入场价、止损价、账户风险翻译成仓位。

阶段 1 通过标准：给你一段价格序列和一个信号，你能手算收益、费用、权益曲线、回撤和最大亏损。

## 阶段 2：多资产研究

- [ ] 读完 [05 因子研究](../curriculum/modules/05_factor_research.md)。
- [ ] 完成 [Lab 05](../labs/05_factor_ic/README.md)。
- [ ] 能解释横截面排序和时间序列择时的区别。
- [ ] 能解释 IC、RankIC、分组收益、换手。
- [ ] 读完 [06 组合构建](../curriculum/modules/06_portfolio.md)。
- [ ] 完成 [Lab 06](../labs/06_portfolio/README.md)。
- [ ] 能手算等权和非等权组合收益。
- [ ] 能解释相关性和集中度为什么会毁掉表面分散。

阶段 2 通过标准：你能说明一个因子为什么可能只是行业、市值或流动性暴露。

## 阶段 3：模型和执行

- [ ] 读完 [07 机器学习](../curriculum/modules/07_machine_learning.md)。
- [ ] 完成 [Lab 07](../labs/07_machine_learning/README.md)。
- [ ] 能画出特征窗口、标签窗口和泄漏边界。
- [ ] 读完 [Qlib 深入分析](qlib_deep_dive.md)。
- [ ] 读完 [进攻性量化模型 2026](aggressive_quant_models_2026.md)。
- [ ] 能解释为什么 LLM 更适合当研究员，不适合直接当操盘手。
- [ ] 读完 [08 执行和复盘](../curriculum/modules/08_execution_review.md)。
- [ ] 完成 [Lab 08](../labs/08_execution_review/README.md)。
- [ ] 写一份 [交易审判卡](trade_review_template.md)。
- [ ] 明确策略结论：`kill`、`observe`、`paper_trade` 或 `promote`。

阶段 3 通过标准：你能把模型分数翻译成组合、成本、风控、纸面交易和下线条件。

## 每次学习后的记录

建议每次学习后记录 5 行：

```text
日期：
今天读了：
今天跑了：
我之前误解的是：
下一步：
```

不要写空泛总结。能被命令、手算或具体反例验证的内容才算学习记录。
