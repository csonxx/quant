# Notebooks

notebook 只用于探索和画图，不作为最终研究事实来源。

一旦 notebook 里有可复用逻辑，必须迁移到：

- `src/quant_learning/`：正式实现。
- `tests/`：防止未来改坏。
- `reports/`：研究结论和复盘。

原因很简单：notebook 很适合思考，也很适合偷偷藏状态。量化研究不能靠藏状态活着。

`make check` 会执行 notebook 边界检查：notebook 里不允许定义可复用 `def` / `class` 逻辑，也不允许通过 `sys.path` 或 `PYTHONPATH` 绕过包结构。需要复用的逻辑放进 `src/quant_learning/`，再补测试。
