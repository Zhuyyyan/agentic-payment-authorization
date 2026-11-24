# 消费者委托支付的交易级授权机制

**Transaction-Level Authorization for Consumer-Delegated Agentic Payments**

公开仓库：[Zhuyyyan/agentic-payment-authorization](https://github.com/Zhuyyyan/agentic-payment-authorization)。

金融科技导论研究计划及可复现Python仿真：当AI Agent代表消费者购物付款或转账时，如何逐笔检查其权限，并在安全性与人工确认成本之间取得平衡？

> 全部交易均为人工合成。项目不接入真实账户、不转移真实资金、不使用真实用户交易，也不训练大型语言模型。实验结论仅适用于所设模拟分布。

## 从这里开始

|材料|内容|
|---|---|
|[研究计划 PDF](paper/paper.pdf)|17页中文研究计划，含理论、机制、已完成模拟和未来研究|
|[可编辑论文](paper/paper.docx)|与最终PDF对应的DOCX|
|[理解辅助稿 PDF](paper/理解辅助稿.pdf)|8页中文讲解：220元交易手算、变量、指标、复跑与问答|
|[质量审查](quality_review.md)|验证证据、已修复问题及仍存在的文献获取限制|
|[运行验证记录](outputs/logs/verification.json) · [文档渲染记录](outputs/logs/native_render_audit.json)|源文件与论文摘要、复核规模、分页及字号等可检查证据|
|[文献矩阵](literature/literature_matrix.csv)|17项资料的类型、方法、局限和使用位置|
|[论文与仓库一致性核对](research/repository_consistency_review.md)|代码、结果表及论文文件的对应检查|

## 项目状态与验证

截至2026年11月24日，研究计划、Python仿真、探索性结果和理解辅助稿已整理并公开。论文属于 **Research Proposal（研究计划）**：已运行的合成仿真与未来拟开展的研究分别说明，假设的适用范围以论文分析为准。

|核对项目|记录与范围|
|---|---|
|论文排版|LibreOffice原生渲染，论文17页、辅助稿8页；论文文字字号12 pt（小四），PDF与DOCX同源，见[渲染记录](outputs/logs/native_render_audit.json)|
|程序验证|15项单元测试；[运行记录](outputs/logs/verification.json)另保存环境、源文件SHA256及150万条决策记录的复核规模，该数量包含同批交易在不同策略下的决策，不是150万笔独立交易|
|结果一致性|主实验、追加实验的结果表与论文展示值已核对；发布收尾仅修改说明和证据入口，实验参数、结果及论文数值保持不变|
|资料限制|部分文献全文仍有访问限制，详见[文献阅读说明](literature/literature_review_notes.md)和[质量审查](quality_review.md)；不据此宣称全部文献已完成全文核验|

这些记录对应已归档版本。修改代码、参数或文稿后，应重新运行相关验证，并同步结果表、图表、论文与README。公开范围和发布操作见[发布说明](PUBLICATION.md)。

首次阅读可先看[理解辅助稿](paper/理解辅助稿.md)中的交易手算与指标解释，再对照[实验设计](research/experimental_design.md)、下方结果表和源码；辅助稿也提供[可编辑DOCX](paper/理解辅助稿.docx)。

## 研究设计

用户意图被视为已经确认的结构化委托。所有策略共同遵守撤销、到期、操作、金额硬上限、币种及禁止收款方等约束；任何低风险评分都不能覆盖硬约束。

|策略|控制方式|
|---|---|
|M1|仅授权范围检查|
|M2|范围检查加金额、新收款方、频率固定规则|
|M3|五因素风险分级、人工升级和执行前完整性验证|
|M2_full（追加）|与M3共用五项信号和完整性门，采用共同阈值OR规则|

风险变量为金额占比A、收款方新颖性P、任务一致性S、频率风险V、环境异常E。因为一致性越高越安全，评分使用`1-S`。基准权重为`[0.20,0.20,0.25,0.20,0.15]`，属于人工设定，并非最优估计。

```text
结构化委托 → 硬约束检查 → 风险分级 → 执行前复查 → 模拟执行与审计
                                └→ 人工升级后暂停
```

![交易级授权流程](outputs/figures/architecture.png)

## 已完成的探索性结果

主实验：30个独立种子，每个10000笔，相同交易配对比较。AUTO_EXECUTE与OBSERVE均计为无人确认执行；ESCALATE暂停，不计为成功完成。

|策略|未经授权自动执行率 UAER ↓|合法自动执行率 LAER ↑|人工升级率 ER|
|---|---:|---:|---:|
|M1|79.50%|100.00%|0.00%|
|M2|28.05%|73.54%|33.84%|
|M3|21.87%|97.98%|12.12%|

基准残余风险较高，不能据此支持真实支付部署。阈值校准和追加实验用于检查权衡，而非把基准参数包装成可直接使用的风控方案。

![安全与效率权衡](outputs/figures/tradeoff.png)

追加公平比较另用30个新种子，共30万笔；校准与测试分离，共用五项风险信息和完整性门：

|策略|测试UAER|测试LAER|测试ER|
|---|---:|---:|---:|
|M2_full|4.38%|71.68%|36.43%|
|M3|1.84%|81.85%|29.98%|

这是主实验之后的探索性复核。共同阈值OR仍是受限基准，且测试安全水平不完全相等，不能推出M3优于所有固定规则。Bootstrap区间以模拟种子为单位，只衡量Monte Carlo波动。详见[逐种子结果](outputs/tables/per_seed.csv)、[配对差值](outputs/tables/paired_contrasts.csv)和[追加比较](outputs/tables/robust_contrasts.csv)。

### 实验与证据对应

|实验|主要输出|阅读重点|
|---|---|---|
|一：三种机制比较|[指标汇总](outputs/tables/summary.csv)、[逐种子结果](outputs/tables/per_seed.csv)|同时比较安全、合法执行、拒绝、人工升级、损失代理及审计完整性|
|二：阈值权衡|[阈值扫描](outputs/tables/thresholds.csv)、[校准记录](outputs/tables/calibration.csv)、[配对差值](outputs/tables/h2_contrasts.csv)|阈值由独立校准样本选择；测试安全水平是否接近仍需检查|
|三：风险信号组合|[分组结果](outputs/tables/groups.csv)、[组合效应差值](outputs/tables/h3_contrast.csv)|单信号与多信号组的相对控制效果；分组比较本身不构成真实因果推断|
|四：模块消融|[完整策略及消融汇总](outputs/tables/summary.csv)、[配对比较](outputs/tables/paired_contrasts.csv)、[篡改子集](outputs/tables/tamper_subset.csv)|分别检查移除风险评分或完整性验证后的变化|
|五：权重敏感性|[权重方案结果](outputs/tables/weights.csv)|比较人工设定方案，不将某一方案称为最优权重|
|追加复核|[公平基准测试](outputs/tables/robust_test.csv)、[配对比较](outputs/tables/robust_contrasts.csv)、[生成过程敏感性](outputs/tables/dgp_sensitivity.csv)|检查共用风险信号的固定规则基准，以及噪声和风险占比改变后的结果|

主实验的种子、样本量及数据摘要见[实验清单](experiment_manifest.csv)，追加实验见[追加清单](outputs/tables/robust_manifest.csv)。确定性边界与因子场景用于验证规则行为，不作为重复独立样本纳入置信区间。

## 安装与复现

Python 3.12.14已验证；实验依赖主要为NumPy和pandas。完整依赖及精确版本分别见[requirements.txt](requirements.txt)和[requirements-lock.txt](requirements-lock.txt)。

```bash
git clone https://github.com/Zhuyyyan/agentic-payment-authorization.git
cd agentic-payment-authorization
python -m venv .venv
# Windows: .venv/Scripts/Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m src.main
python -m src.simulation.robustness
```

15项单元测试覆盖硬约束、风险方向、四态、撤销、篡改、异常金额及追加固定规则。运行会生成原始合成交易、决策日志和结果表。快速练习请在项目副本运行`python -m src.main --n 1000 --seeds 3`，避免覆盖标准结果。

参数见[config.json](config.json)，数据生成过程见[generator.py](src/simulation/generator.py)，追加实验设置见[robustness.py](src/simulation/robustness.py)。[示例交易](data/examples/transactions.jsonl)仅含人工符号。完整大体积数据和日志不纳入Git历史，按固定种子可重建。

## 文档与工程结构

```text
src/authorization/   授权边界、评分、决策、执行门与审计
src/simulation/      数据生成、指标、配对比较及追加稳健性
tests/               单元测试
research/            研究问题、假设、理论与设计
literature/          元数据、BibTeX与文献比较
outputs/tables/      已运行的结果表
outputs/figures/     从结果生成的图
paper/               论文和理解辅助稿
```

论文生成使用python-docx、ReportLab及Windows宋体/微软雅黑；原生渲染另需LibreOffice和Poppler。`tools/render_native.py`可通过`CODEX_DOCX_RENDERER`指定本机文档技能渲染器，或在LibreOffice中直接导出DOCX。跨平台实验本身不依赖Office或Codex，文档重新生成需调整本机字体与渲染器路径。

## 研究边界与资料说明

- 贡献定位为消费者场景的机制操作化和可复现策略比较，不主张首次提出动态授权、运行时治理或Agent身份框架。
- 标签和信号关系为人工设定；未模拟真实认证、累计预算、重放防护、并发及审批行为。
- 完整性演示依赖可信快照和不可绕过的执行门；SHA256不等于签名或不可抵赖。
- Jensen1976期刊全文已取得；Hart1985工作论文与1988发表版分别著录。IMF完整PDF及Hart1988全文的访问限制保留在[文献说明](literature/literature_review_notes.md)。
- 研究与工程采用AI辅助整理和实现；提供代码、参数、引用边界和审查记录，供读者独立复核。

## 引用与使用

引用元数据见[CITATION.cff](CITATION.cff)。本仓库用于公开研究展示，尚未授予开源再分发许可证；原创材料的使用请联系仓库作者。第三方文献版权归原权利人，下载全文和课程原始作业文件不在公开仓库再分发。
