# 术语表

- `OHLCV`：open、high、low、close、volume，K 线基础字段。
- `Return`：收益率，常用 `close_t / close_{t-1} - 1`。
- `Alpha`：扣除共同风险暴露后的超额收益。
- `Beta`：市场、行业、风格等共同风险暴露。
- `Signal`：用于表达买卖倾向的数值或规则。
- `Position`：实际仓位，信号经过风险和组合约束后得到。
- `Backtest`：用历史数据模拟策略执行。
- `Look-ahead bias`：使用当时不可知的未来数据。
- `Survivorship bias`：只保留幸存资产导致结果虚高。
- `Slippage`：预期成交价和真实成交价之间的差。
- `Turnover`：换手率，代表交易频率和成本压力。
- `Drawdown`：权益曲线从高点到后续低点的跌幅。
- `Sharpe ratio`：单位波动获得的超额收益，不能单独代表策略好坏。
- `Walk-forward`：滚动训练和测试，观察策略稳定性。
- `Purged split`：清除训练集和测试集之间重叠信息的切分方法。
