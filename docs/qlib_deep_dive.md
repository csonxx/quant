# Qlib 深入分析

整理日期：2026-05-27。

## 一句话判断

Qlib 不是一个“均线回测库”，也不是一个“自动赚钱框架”。它更像一套 AI 量化研究生产线：

```text
数据 -> 特征/标签 -> 数据处理 -> 模型训练 -> 预测分数 -> 组合策略 -> 回测评估 -> 实验记录
```

它最适合的场景是：你已经理解数据偏差、标签、样本外、因子、组合和回测，然后想系统化地做机器学习选股/因子研究。

小白一开始不该直接上 Qlib。原因很简单：Qlib 会把大量细节封装起来。你如果不知道每一步在做什么，它跑出来的图和指标越漂亮，越容易骗你。

## 官方定位

Microsoft 对 Qlib 的定位是 AI-oriented quantitative investment platform，目标是覆盖从想法探索到 production 的量化研究链条。GitHub README 明确说它包含数据处理、模型训练和回测的完整 ML pipeline，也覆盖 alpha seeking、risk modeling、portfolio optimization 和 order execution。

这句话要拆开理解：

- `AI-oriented`：核心不是传统手写策略，而是让 ML/AI 进入量化研究。
- `pipeline`：它关心一整条研究链，不只是单个模型。
- `alpha seeking`：预测/排序未来收益。
- `portfolio optimization`：把预测分数变成组合。
- `order execution`：进一步考虑交易执行。

所以 Qlib 的野心很大。野心大是优点，也是小白学习时的危险点。

## Qlib 的核心结构

### 1. 数据层

Qlib 有自己的数据格式和数据访问层。它不是简单读一个 CSV，然后让你随便 pandas 操作。

核心概念：

- `provider_uri`：Qlib 数据目录。
- `calendar`：交易日历。
- `instrument`：股票池/标的池。
- `feature`：价格、成交量、衍生表达式等。
- `expression`：类似 `Mean($close, 5)` 这种特征表达式。
- `cache`：表达式和数据集缓存。

这套结构的意义是：多股票、多日期、多特征下，数据读取和特征计算要可复用、可缓存、可追踪。

毒辣提醒：数据层看起来很工程化，但它不能自动保证你的数据没有幸存者偏差、复权错误、字段发布时间错误。Qlib 给你工具，不替你负责。

### 2. DataHandler 和 Processor

Qlib 的 `DataHandlerLP` 很关键。它负责把原始数据变成模型可用的数据，并区分学习和推理流程。

你可以粗略理解成：

```text
DataLoader 负责加载
DataHandler 负责组织 raw/infer/learn 数据
Processor 负责 dropna、标准化、去噪等处理
Dataset 负责按 train/valid/test 切片喂给模型
```

这里最容易出错的是 Processor。比如标准化必须只用训练集 fit，然后应用到验证/测试。否则你就把未来分布偷进训练过程。

### 3. 模型层

Qlib 的模型层把模型抽象成：

```text
fit(dataset)
predict(dataset, segment="test")
```

官方示例里有 LightGBM、MLP、LSTM 等模型。它的主要用途不是让你发明模型接口，而是让不同模型能共享同一套数据、切分、评估和记录流程。

毒辣提醒：模型输出通常只是 `prediction score`。它不是买入结论。分数还要经过排序、组合、成本、风控和回测。

### 4. Workflow / qrun

Qlib 提供 `qrun`，可以用配置文件自动跑完整流程：

```text
加载数据 -> 处理数据 -> 切分数据 -> 训练模型 -> 预测 -> 信号分析 -> 回测 -> 记录结果
```

这对研究复现很有价值，因为配置文件能固定模型、数据、参数和记录项。

但对小白也很危险：一条命令跑完所有东西，你可能不知道每一步怎么来的。`qrun` 不是学习入口，应该是你理解各组件后的自动化工具。

### 5. Recorder / Experiment

Qlib 有实验管理能力，能追踪训练、预测、评估阶段产生的信息和 artifacts。

这点很重要，因为量化研究不能只保存成功截图。你需要保留：

- 数据版本。
- 特征配置。
- 模型参数。
- 切分方式。
- 预测分数。
- 回测报告。
- 失败实验。

没有实验记录，量化研究会变成“调参玄学”。

### 6. 策略和回测

Qlib 的回测不是简单地“模型预测上涨就买”。常见流程是：

```text
模型输出 score -> 策略按 score 选股/换仓 -> backtest_daily 或 backtest -> 风险分析
```

典型策略是 `TopkDropoutStrategy`：

- 持有预测分数最高的 `topk` 只股票。
- 每天卖出当前持仓里排名差的一部分。
- 买入未持仓里排名高的一部分。

这个策略很适合理解“模型分数如何转成组合”。但它也暴露一个核心问题：换手。

官方文档里说明，TopkDrop 大多数情况下每天买卖 `Drop` 只股票，换手近似和 `2 * Drop / K` 相关。换手越高，成本越容易吃掉模型优势。

## Qlib 强在哪里

### 1. 研究链完整

很多库只管回测，Qlib 管：

- 数据。
- 特征。
- 模型。
- 预测。
- 组合。
- 回测。
- 分析。
- 记录。

这对机器学习量化研究非常重要，因为 ML 策略最怕“每一步都散落在 notebook 里，最后没人知道结果怎么来的”。

### 2. 适合横截面 ML 选股

Qlib 的天然范式是：

```text
很多股票 + 很多日期 + 很多特征 -> 预测未来收益/排序 -> 构建组合
```

这比单资产择时更贴合它的设计。

### 3. 配置化和可复现

`qrun` 和 YAML workflow 让实验配置化。你可以把研究从“手点 notebook”变成“配置驱动”。

### 4. 有模型和策略基线

Qlib 自带一些模型和策略示例。对学习者来说，基线很重要，因为你可以先跑通官方 LightGBM，再逐步替换数据、特征、模型和策略。

### 5. 适合进一步学习 production-ish 流程

Qlib 文档还包含 online serving、task management、PIT database、reinforcement learning、order execution 等主题。这些不是小白第一阶段要学的，但说明它的设计不止是 notebook demo。

## Qlib 弱在哪里

### 1. 学习曲线陡

Qlib 抽象多：provider、handler、processor、dataset、model、record、strategy、executor、analysis。小白如果跳进去，会先被名词淹没。

### 2. 封装会隐藏账本

你可能一条 `qrun` 就拿到 annualized_return、information_ratio、max_drawdown。但你未必知道：

- 标签怎么定义。
- 标准化是否泄漏。
- 信号何时产生。
- 成交价格怎么假设。
- 成本怎么扣。
- 股票池是否幸存者偏差。

这就是为什么本仓库先手写最小回测。

### 3. 数据不是魔法

Qlib 提供数据准备脚本和格式，但真实研究要自己审数据：

- 中国市场复权。
- 停牌。
- 涨跌停。
- 指数成分历史。
- 财报 PIT。
- 交易成本。
- 股票池生灭。

Qlib 不能替你证明数据在交易时点可知。

### 4. 默认策略容易让人误判

TopkDropoutStrategy 很直观，但它容易让小白误解：

```text
模型分数高 -> 买入 -> 策略完成
```

实际上你还要审：

- topk 怎么选。
- n_drop 怎么选。
- 换手多高。
- 成本敏感性。
- 行业/市值暴露。
- 是否和 benchmark 比。
- 去掉少数贡献股票后是否还有效。

### 5. 它不是实盘保证

Qlib 的 production/online 组件不等于你可以直接拿去真钱交易。实盘还需要：

- 稳定数据源。
- 券商接口。
- 订单管理。
- 风控开关。
- 异常处理。
- 监控告警。
- 人工审批边界。

Qlib 更适合先做研究流水线和纸面/模拟链路。

## 和其他工具的区别

| 工具 | 更适合 | 不适合 |
| --- | --- | --- |
| 手写最小引擎 | 小白理解账本、时序、成本 | 大规模多资产研究 |
| pandas/vectorbt | 快速参数扫描、向量化研究 | 完整 ML workflow 和生产记录 |
| backtrader | 学事件驱动策略和订单对象 | 大规模横截面 ML |
| LEAN/QuantConnect | 接近实盘、多资产事件驱动 | 本地 ML 因子流水线自由度较低 |
| Qlib | AI/ML 横截面选股、因子研究、实验管理 | 小白第一课、简单手工策略、直接实盘 |

## Qlib 在本仓库学习路线里的位置

不要在 00-04 阶段用 Qlib。

推荐顺序：

1. `00`：理解正期望。
2. `01`：手算收益和回撤。
3. `02`：理解数据契约和前视偏差。
4. `03`：手写回测，理解信号延迟和成本。
5. `04`：仓位和风控。
6. `05`：因子排序和分组收益。
7. `06`：组合权重、相关性和换手。
8. `07`：标签、特征、时间切分、purged split。
9. 再进入 Qlib。

Qlib 最适合作为 `07 机器学习` 后半段和 `08 执行复盘` 前半段的工具：把你已经理解的 ML 因子研究流程配置化、批量化、可记录化。

## 小白进入 Qlib 的正确方式

### 第一步：只跑官方 LightGBM demo

目标不是相信结果，而是看懂链路：

```text
数据在哪里
特征是什么
标签是什么
模型是什么
预测分数长什么样
策略怎么用分数
回测怎么扣成本
输出指标是什么
```

### 第二步：冻结模型，只改成本

把交易成本调高，观察收益是否死亡。一个模型如果只在低成本假设下活着，优势很薄。

### 第三步：冻结成本，只改策略

比如 TopK 数量、Drop 数量、再平衡频率。观察换手和收益。

目标是理解：

```text
模型预测能力 != 组合收益
组合收益 != 执行后收益
```

### 第四步：冻结策略，只改特征

先别上复杂深度模型。用 LightGBM + 少量可解释特征，观察哪些特征真的贡献稳定。

### 第五步：做样本外和走步

一次 train/valid/test 不够。要做滚动验证，检查模型是否稳定。

## Qlib 的毒辣审查问题

每次看到 Qlib 结果，先问：

1. 标签是什么？预测未来几天？
2. 特征在预测时点是否已经可知？
3. Processor 是否把测试集信息泄漏进训练？
4. 股票池是否有幸存者偏差？
5. 成本是多少？加倍后还活着吗？
6. TopK 和 Drop 是怎么选的？是否调参过拟合？
7. 换手率多少？
8. 收益来自少数股票还是稳定分布？
9. 是否跑赢买入持有、指数、行业/风格基准？
10. 样本外和走步是否稳定？
11. 回测成交假设是否现实？
12. 是否保留了失败实验？

如果这些问题答不上来，Qlib 跑出来的 annualized_return 没有交易意义。

## 适合我们的落地计划

短期不安装 Qlib。先把本仓库 00-06 学完。

到 07 阶段时新增一个独立目录：

```text
experiments/qlib/
├── README.md
├── configs/
│   ├── lightgbm_alpha158.yaml
│   └── lightgbm_cost_sensitivity.yaml
├── notes/
│   ├── data_contract.md
│   ├── label_definition.md
│   └── leakage_audit.md
└── reports/
    └── first_lightgbm_review.md
```

第一批实验只做三件事：

1. 跑通官方 LightGBM。
2. 写清标签、特征、切分、成本。
3. 做成本敏感性和 TopK/Drop 敏感性。

禁止一开始就换深度模型。因为模型复杂度不是优势，验证纪律才是优势。

## 结论

Qlib 值得学，但不是入门工具。它是一个强大的 ML 量化研究流水线，适合你已经懂得“收益怎么来、数据哪里会骗、回测哪里会作弊、模型分数怎么变组合”之后使用。

最毒辣的判断是：

```text
Qlib 能让正确研究更高效，也能让错误研究更体面。
```

所以我们的学习路线是：先手写账本，再上 Qlib；先会杀假策略，再跑大框架。

## 资料来源

- Qlib GitHub README: https://github.com/microsoft/qlib
- Qlib latest docs: https://qlib.readthedocs.io/en/latest/
- Qlib Quick Start: https://qlib.readthedocs.io/en/latest/introduction/quick.html
- Qlib Workflow: https://qlib.readthedocs.io/en/latest/component/workflow.html
- Qlib Data Layer: https://qlib.readthedocs.io/en/latest/component/data.html
- Qlib Model: https://qlib.readthedocs.io/en/latest/component/model.html
- Qlib Strategy/Backtest: https://qlib.readthedocs.io/en/latest/component/strategy.html
- Qlib paper: https://arxiv.org/abs/2009.11189
