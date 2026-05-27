# 资料来源和当前工具判断

整理日期：2026-05-27。

这些资料不是用来崇拜工具，而是用来校准学习路线。

## 关键资料

- Bailey、Borwein、Lopez de Prado、Zhu 的 backtest overfitting 论文：说明尝试足够多策略配置后，漂亮回测很容易只是过拟合。
  - https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2308659
- VectorBT 官方文档：强调向量化、多参数扫描和 notebook 交互研究，适合研究加速，但也更容易让人暴力扫参数后自欺。
  - https://vectorbt.dev/
- QuantConnect/LEAN 官方文档：事件驱动、多资产、研究到回测到实盘的完整框架，适合理解接近实盘的算法生命周期。
  - https://www.quantconnect.com/docs/v2/
- Microsoft Research Qlib 页面：AI-oriented quantitative investment platform，适合后续研究机器学习、因子和模型流水线。
  - https://www.microsoft.com/en-us/research/project/ai-for-finance/tools/
- BacktestBench, 2026：LLM 自动回测方向的新 benchmark，提醒我们 AI 可以加速研究，但必须做 grounded verification 和标准化指标表示。
  - https://arxiv.org/abs/2605.17937

## 当前判断

学习阶段不要一上来依赖大框架。正确路线是：

1. 用标准库写清楚数据、信号、仓位、成本、权益曲线。
2. 用测试固定最容易犯错的时序规则。
3. 用 pandas/numpy 扩大研究规模。
4. 用 vectorbt 做参数网格和快速探索。
5. 用 Qlib 做因子/ML 研究流水线。
6. 用 LEAN 或事件驱动框架理解接近实盘的订单生命周期。

核心原则：工具越强，越要保留失败记录和样本外验证。否则只是更快地产生错觉。
