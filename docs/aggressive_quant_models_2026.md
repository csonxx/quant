# 进攻性量化模型深度分析：2026 版

整理日期：2026-05-27。

## 先下结论

如果你问“有没有最新、最狠、最有效的进攻性量化模型”，答案不是某一个神经网络名字。

真正最狠的方向是：

```text
LLM/Agent 自动挖因子
-> 严格执行回测反馈
-> 去重和抗衰减筛选
-> 因子 + 模型联合优化
-> 市场状态/新闻语义决定因子开关
-> 组合层控制换手、成本、回撤
```

也就是“自动化 alpha 工厂”，不是“让 LLM 直接喊买卖”。

毒辣判断：

```text
2026 最值得押的进攻性研究路线，不是纯深度预测模型，而是 agentic alpha mining + 可解释因子 DSL + 严格回测闭环 + 轻量强基线模型 + regime-aware 组合。
```

原因很现实：金融数据噪声太大，单个深度模型很容易学到历史巧合；而进攻性 alpha 的核心在于持续生成、筛选、组合、淘汰信号。攻击力来自“搜索和迭代速度”，不是来自一个模型名字。

## 我怎么定义“进攻性”

这里的进攻性不是乱加杠杆、重仓梭哈。那是鲁莽，不是量化。

进攻性量化模型要满足：

- 能持续寻找新 alpha，而不是只吃一个老因子。
- 能适应 regime shift，知道什么时候因子失效。
- 能利用高维数据、非线性、横截面关系或微观结构。
- 能把预测翻译成仓位、换手和成本后的收益。
- 能快速证伪，杀掉假 alpha。
- 能在样本外仍有正收益或至少保留预测结构。

最狠的系统不是“预测最准”，而是“发现、验证、淘汰、再发现”的速度最快。

## 第一梯队：Agentic Alpha Factory

代表：

- R&D-Agent-Quant
- AlphaCrafter
- Hubble
- QuantaAlpha
- AlphaAgent / Alpha-R1 / MCTS alpha mining 系列

### 核心思想

这类系统把量化研究拆成闭环：

```text
生成假设 -> 写成可执行因子 -> 回测评估 -> 诊断失败 -> 变异/优化 -> 再评估
```

以前人手工想因子，现在 agent 批量生成；以前人手工看结果，现在系统用 IC、RankIC、ICIR、long-short、换手、回撤、成本敏感性筛。

### 为什么它最进攻

因为 alpha 会衰减。一个公开因子被人发现后，会被拥挤交易吃掉。

进攻性不是找到一个永远有效的因子，而是持续制造新候选，并有纪律地筛掉大多数垃圾。

这类系统的攻击力来自：

- 搜索空间大：能生成大量公式化因子。
- 反馈快：每个候选都能回测。
- 可解释：公式因子比端到端黑箱更容易审。
- 可复现：同一表达式能确定执行。
- 可组合：多个弱因子可以形成 ensemble。
- 可淘汰：衰减后能下线。

### R&D-Agent-Quant

R&D-Agent(Q) 是微软提出的多智能体量化研发框架，重点是因子和模型联合优化。它把流程拆成 Research、Development 和 feedback，使用代码生成 agent 实现任务，再通过真实市场回测反馈下一轮。论文摘要声称它用更少因子取得了高于经典因子库的年化收益，并超过一些深度时序模型。

它的强点：

- 因子和模型不是割裂优化，而是联动。
- 有多臂老虎机式调度，决定下一轮优先优化因子还是模型。
- 基于 Qlib，天然接实验记录和回测。
- 比“LLM 直接交易”更可复现。

它的弱点：

- 仍然依赖回测反馈，容易 reward hacking。
- 如果回测环境有偏差，agent 会放大偏差。
- 因子搜索越强，越需要严格去重和样本外。
- 论文结果不能直接等于个人可交易收益。

毒辣结论：这是目前最值得研究的“进攻性量化研发范式”，但它不是策略，是策略工厂。

### AlphaCrafter

AlphaCrafter 是 2026 年 5 月的新框架，定位更接近完整交易系统。它把 agent 分成：

- `Miner`：持续扩展因子池。
- `Screener`：判断市场状态，构造 regime-conditioned 因子组合。
- `Trader`：在风险约束下把因子组合变成策略。

它比单纯 alpha mining 更进一步：不是一次性挖因子，而是把市场状态纳入筛选。

进攻性在于：

```text
持续挖因子 + regime 条件筛选 + 交易执行闭环
```

最大坑：

- 多 agent 系统容易引入复杂度幻觉。
- 如果 Screener 判断 regime 不稳，组合会频繁切换。
- Trader 层如果风险约束不硬，可能把研究收益变成实盘回撤。

毒辣结论：概念很对，但越 full-stack，越要防“每层都有一点误差，最后全链路漂亮但不可交易”。

### Hubble

Hubble 的价值在“安全、可复现、多样性”。它没有把 LLM 当自由代码生成器，而是限制在 operator language 和 AST sandbox 里生成因子，并做 family-aware selection。

它解决的是 agentic alpha mining 的硬伤：

- 乱生成不可执行公式。
- 因子高度重复。
- 只会生成拥挤的 volume/momentum 变体。
- 回测结果难复现。
- 生成过程缺少诊断 artifacts。

毒辣结论：Hubble 可能没 AlphaCrafter 听起来猛，但它更像能落地的“安全因子工厂”。对我们学习最有价值。

### QuantaAlpha

QuantaAlpha 是 2026 年的 evolutionary alpha mining 框架。它把每次挖掘过程当成 trajectory，再做 mutation 和 crossover，复用高奖励片段。

它强在：

- 不是单轮生成，而是多轮进化。
- 对失败步骤做定位修复。
- 约束因子复杂度和冗余，降低 crowding。
- 论文声称在 CSI 300、CSI 500、S&P 500 有跨市场迁移效果。

毒辣提醒：任何“跨市场迁移有效”的结果都要高度警惕。要看数据切分、成本、行业暴露、汇率/交易规则差异、是否调参后才迁移。

## 第二梯队：LLM 因子筛选和推理模型

代表：

- Alpha-R1
- AlphaBench
- AlphaForgeBench
- AlphaAgent
- Chain-of-Alpha
- LLM + MCTS alpha mining

### 核心思想

LLM 不直接下单，而是参与：

- 因子生成。
- 因子解释。
- 因子筛选。
- 因子优化。
- 失败归因。
- 搜索树扩展。

这个方向比“LLM 直接交易”靠谱得多。

### Alpha-R1

Alpha-R1 的重点不是生成新因子，而是通过 reasoning 判断因子在当前市场和新闻语境下是否应该启用。它把因子的语义机制、实时新闻、市场状态结合起来，做 context-aware screening。

进攻性来自：

```text
不是固定持有因子，而是动态开关因子
```

这很关键。很多因子不是永远失效，而是在某些市场状态失效。一个能判断因子何时该停用的模型，比一个只会生成新因子的模型更接近实战。

最大坑：

- 新闻语义和市场状态之间容易过拟合。
- LLM 解释听起来合理，不代表统计上有效。
- 因子开关会增加模型自由度，必须做严格 walk-forward。

### AlphaBench / AlphaForgeBench 的警告

AlphaBench 系统性评估 LLM 在公式化 alpha mining 里的能力。一个很重要的发现方向是：LLM 可以生成和改写因子，但让 LLM 零回测判断因子质量仍然很弱。

AlphaForgeBench 更狠：它指出 LLM 作为实时交易 agent 会出现强烈不稳定，例如相邻时间动作翻转、确定性解码仍有行为不稳定等。它主张把 LLM 定位成“量化研究员”，生成可执行因子和策略，而不是直接输出交易动作。

毒辣结论：

```text
LLM 可以当研究员，不该当操盘手。
```

## 第三梯队：深度时序预测模型

代表：

- MASTER
- TRA
- MambaStock / Mamba 类模型
- HAELT
- LiT / LOB Transformer

这些是“预测模型”，不是完整策略。

### MASTER：市场引导的 Stock Transformer

MASTER 解决两个问题：

- 股票之间的关联不只是同一时点，可能跨时间发生。
- 不同特征在不同市场状态下有效性会变化。

它用 market-guided feature selection 和 intra-stock / inter-stock aggregation 来建模动态关联。

适合：

- 横截面股票预测。
- 多股票、多特征、多日期。
- 想捕捉行业/市场联动时。

不适合：

- 小样本。
- 没有严格切分的数据。
- 直接把预测当交易。

毒辣结论：MASTER 比普通 Transformer 更贴近股票横截面，但它仍然只是预测层。真正收益要看组合、换手、成本。

### TRA：多交易模式路由

TRA 的想法很漂亮：市场里存在多种交易模式，不应该用一个 predictor 吃所有样本。它用多个 predictor + router，把样本分派给不同模式。

这很符合市场现实：

- 趋势市场。
- 震荡市场。
- 高波动市场。
- 事件驱动市场。

攻击性来自 regime/pattern specialization。

最大坑：

- router 自己可能过拟合。
- 模式没有真实标签，训练难。
- 模式切换成本可能被忽略。

毒辣结论：TRA 的思想比单模型预测更高级，适合作为 regime-aware model 的学习材料。

### MambaStock / Mamba 类模型

Mamba 的优势是长序列建模效率高，理论上比 Transformer 更适合长时间序列。

MambaStock 把 Mamba 用于股票预测，强调不用大量手工特征也能挖历史序列。

攻击性来自：

- 长序列建模。
- 低计算复杂度。
- 对非线性时序模式敏感。

但金融里要冷静：

- 长序列不一定有稳定信号。
- 原始价格序列很容易非平稳。
- 单股票预测容易被噪声骗。
- 没有成本和交易层，预测准确不等于收益。

毒辣结论：Mamba 是值得关注的时序 backbone，但不是“最狠交易模型”。它更适合作为特征编码器或序列专家，放进因子/组合框架里。

### HAELT

HAELT 用 ResNet 降噪、self-attention、LSTM-Transformer 和自适应 ensemble 做高频股价预测。它在 2025 年论文里用 AAPL 小时级数据做方向预测。

这类模型适合学习高频预测结构，但实战风险很大：

- 单股票实验泛化弱。
- 小时级不等于真正 HFT。
- 方向 F1 高不等于扣成本后赚钱。
- 高频交易更依赖执行和滑点。

毒辣结论：HAELT 是结构参考，不是直接可用的赚钱机器。

### LiT / LOB Transformer

LiT 是 limit order book transformer，用 patch-based self-attention 替代卷积，面向 LOB forecasting，并在多个预测 horizon 上和传统/深度模型比较。

这是非常进攻的方向，因为订单簿微观结构是短周期预测里最接近“真实供需”的数据。

但门槛也最高：

- 要有高质量 L2/L3 order book 数据。
- 要处理纳秒/毫秒级时间戳、撮合、撤单。
- 要真实模拟排队位置和成交概率。
- 交易成本和延迟会杀死预测优势。
- 个人很难和专业 HFT 拼延迟。

毒辣结论：LOB Transformer 是技术上最进攻的模型之一，但对个人学习者最不友好。没有数据和执行基础，别碰真钱。

## 第四梯队：强化学习组合/执行

强化学习看起来很适合交易：状态、动作、奖励，天然像市场。

但它最大的问题是：金融环境非平稳，奖励噪声大，回测环境可被 agent exploit。

RL 最适合的位置不是“找 alpha”，而是：

- 因子权重动态分配。
- 组合再平衡。
- 执行算法。
- 做市库存管理。
- 多策略 allocator。

不建议一开始用 RL 直接决定买卖。

毒辣结论：

```text
RL 适合做 allocator 和 executor，不适合小白拿来当 alpha 生成器。
```

## 最不推荐：LLM 直接交易 agent

这类东西最容易火，也最容易骗人：

```text
把新闻、K 线、指标喂给 LLM，让它输出 BUY / SELL / HOLD
```

问题：

- 输出不稳定。
- 没有持久 action memory。
- 相邻时间可能逻辑翻转。
- 解释很顺，但统计弱。
- 很难复现。
- 难以做严格风险约束。

AlphaForgeBench 已经把这个问题点得很透：LLM 更适合作为量化研究员生成可执行策略，而不是直接作为交易执行 agent。

毒辣结论：这类 demo 可以看，不要当正路。

## 我的排序

| 排名 | 方向 | 攻击性 | 可落地性 | 对小白危险度 | 结论 |
| --- | --- | --- | --- | --- | --- |
| 1 | Agentic alpha factory | 极高 | 中高 | 高 | 最值得研究 |
| 2 | LLM 因子筛选/开关 | 高 | 中 | 高 | 很有前途 |
| 3 | MASTER/TRA 类横截面深度模型 | 中高 | 中 | 中高 | 适合作预测层 |
| 4 | Mamba 类长序列模型 | 中高 | 中 | 中高 | 可当 backbone |
| 5 | LOB Transformer/HFT 微结构 | 极高 | 低 | 极高 | 没数据和执行别碰 |
| 6 | RL 组合/执行 | 高 | 中低 | 极高 | 做 allocator 更合理 |
| 7 | LLM 直接 BUY/SELL | 表面高 | 低 | 极高 | 不推荐 |

## 最有效的实战型组合

如果我们要构建一个“进攻性但不乱来”的研究系统，我会这样设计：

```text
1. 数据层
   Qlib 格式数据 + PIT 审计 + 股票池生灭记录

2. 因子 DSL
   只允许白名单算子，AST sandbox，禁止任意代码执行

3. Alpha 生成
   LLM + RAG + evolutionary mutation/crossover + MCTS branch search

4. Alpha 评估
   IC / RankIC / ICIR / long-short / turnover / cost stress / regime slices

5. 去重和反拥挤
   因子相关性、family-aware selection、相似度惩罚

6. 模型层
   先 LightGBM，再 TRA/MASTER/Mamba 做对照

7. 因子开关
   Alpha-R1 风格：市场状态 + 新闻语义 + 因子机制一致性

8. 组合层
   TopK/Drop + 行业约束 + 波动率目标 + 成本约束

9. 风控层
   最大回撤、换手上限、因子衰减下线、异常数据停机

10. 纸面交易
    至少 3 个月 forward，不接真钱
```

这个系统的核心不是“预测明天涨跌”，而是“持续生产可解释 alpha，并用残酷评估筛掉 95%”。

## 最小可落地版本

不要一上来搞 full-stack multi-agent。

第一版只做：

```text
LLM 生成公式因子
-> 语法白名单
-> Qlib/本地回测评估
-> IC/RankIC/换手/成本筛选
-> 因子去重
-> LightGBM 排序模型
-> TopK/Drop 回测
```

验收标准：

- 至少 200 个候选因子。
- 至少 3 个不同 family。
- 每个因子有样本内、样本外、成本敏感性。
- 和 Alpha158/简单动量/反转基准比。
- 去掉最赚钱月份后仍不崩。
- 换手翻倍成本后仍可接受。
- 生成和评估过程可复现。

## 最狠的反证测试

任何“进攻性模型”都必须过这些刀：

1. 成本加倍。
2. 成交延迟一根 K 线。
3. 去掉最赚钱 5% 日期。
4. 换一个市场。
5. 换一个股票池。
6. 行业和市值中性化。
7. 因子相关性去重。
8. walk-forward。
9. regime slice。
10. 随机标签 sanity check。
11. 未来数据泄漏审计。
12. 纸面交易 forward。

过不了，不是“还需优化”，就是假。

## 现在最该学什么

你是小白，别直接开搞最复杂模型。正确顺序：

1. 学完当前仓库 00-04：正期望、收益、数据、回测、风控。
2. 学 05-06：因子和组合。
3. 再读 Qlib。
4. 然后做一个最小 alpha factory。
5. 最后才比较 MASTER、TRA、Mamba、LOB Transformer。

如果跳过前面，直接上 AlphaCrafter / R&D-Agent(Q)，它会很快生成一堆看起来很厉害的结果，但你分不清真 alpha 和漂亮垃圾。

## 最终判断

当前最狠的进攻性路线：

```text
Agentic alpha mining + regime-aware factor screening + factor-model joint optimization
```

当前最危险的伪进攻路线：

```text
LLM 直接交易 / 单个深度模型预测涨跌 / 高频模型无真实执行模拟
```

当前最适合我们下一步的路线：

```text
先建一个小型、可解释、可复现的 alpha factory。
```

它不需要一开始就很大，但必须从第一天就有：

- 因子白名单。
- 回测反馈。
- 去重。
- 成本。
- 样本外。
- 失败记录。

这才是进攻性量化里真正的刀。

## 资料来源

- R&D-Agent-Quant: https://arxiv.org/abs/2505.15155
- R&D-Agent GitHub: https://github.com/microsoft/RD-Agent
- Microsoft Research R&D-Agent-Quant article: https://www.microsoft.com/en-us/research/articles/rd-agent-quant/
- AlphaCrafter: https://arxiv.org/abs/2605.05580
- Hubble: https://arxiv.org/abs/2604.09601
- QuantaAlpha: https://arxiv.org/abs/2602.07085
- Alpha-R1: https://arxiv.org/abs/2512.23515
- AlphaForgeBench: https://arxiv.org/abs/2602.18481
- AlphaBench: https://alphabench.cc/
- MASTER: https://arxiv.org/abs/2312.15235
- TRA: https://arxiv.org/abs/2106.12950
- MambaStock: https://arxiv.org/abs/2402.18959
- HAELT: https://arxiv.org/abs/2506.13981
- LiT: https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1616485/full
