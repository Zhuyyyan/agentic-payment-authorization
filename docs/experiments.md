# 实验怎么读、怎么复现

全部结果来自合成交易。合法性标签是数据生成过程的一部分，不是真实用户判断，也不是规则引擎的预测输出。信号与标签关系由研究者设定，改变这种关系可能改变策略排名。

## 两组比较

主实验默认使用种子0—29，每个种子10000笔。M1、M2、M3及两个消融版本在同批交易上比较。数据生成见 [generator.py](../src/simulation/generator.py)，默认参数见 [config.json](../config.json)。

追加实验使用M2_full和M3，两个机制共用五项风险信号和完整性门。用种子9100的10000笔校准，分别选择校准UAER不超过5%时合法自动执行率最高的阈值，再用种子20000—20029测试。阈值网格和筛选规则见 [robustness.py](../src/simulation/robustness.py)。这是主实验之后增加的探索性复核；校准目标不保证测试风险也恰好等于5%。

M2_full采用五项风险中任一达到共同阈值即暂停的规则。它比三信号M2更适合作为信息相同的比较，但仍没有覆盖所有可能的固定规则设计。

## 指标口径

AUTO_EXECUTE和OBSERVE都属于无人确认执行。ESCALATE只表示暂停，没有建立审批行为模型，不能计作成功完成。

|指标|计算方法|
|---|---|
|UAER|已自动执行的未经授权交易数/全部未经授权交易数|
|LAER|已自动执行的合法交易数/全部合法交易数|
|FDR|被DENY的合法交易数/全部合法交易数|
|ER|被ESCALATE的交易数/全部交易数|
|ELP|逐笔计算未经授权执行的金额损失代理、合法拒绝代价和升级代价，再取均值；系数在config.json中设定|
|AC|必要审计字段齐全的记录数/全部记录数|

ELP是人工设定的损失代理，不是真实货币损失。实现和分母处理见 [metrics.py](../src/simulation/metrics.py)。

## 结果文件

|要检查的问题|文件|
|---|---|
|默认策略整体表现|[summary.csv](../outputs/tables/summary.csv)、[per_seed.csv](../outputs/tables/per_seed.csv)|
|同批样本上策略差异及消融|[paired_contrasts.csv](../outputs/tables/paired_contrasts.csv)|
|阈值与安全/效率的关系|[thresholds.csv](../outputs/tables/thresholds.csv)、[calibration.csv](../outputs/tables/calibration.csv)、[h2_contrasts.csv](../outputs/tables/h2_contrasts.csv)|
|单信号与多信号的差异|[groups.csv](../outputs/tables/groups.csv)、[h3_contrast.csv](../outputs/tables/h3_contrast.csv)|
|权重改变后的结果|[weights.csv](../outputs/tables/weights.csv)|
|噪声与风险占比改变后的结果|[dgp_sensitivity.csv](../outputs/tables/dgp_sensitivity.csv)|
|追加公平比较|[robust_calibration.csv](../outputs/tables/robust_calibration.csv)、[robust_test.csv](../outputs/tables/robust_test.csv)、[robust_contrasts.csv](../outputs/tables/robust_contrasts.csv)|
|执行前篡改与硬约束边界|[tamper_subset.csv](../outputs/tables/tamper_subset.csv)、[boundary_cases.csv](../outputs/tables/boundary_cases.csv)|

区间用种子为重抽样单位的Bootstrap；比较先按种子配对求差，再计算区间。它描述Monte Carlo波动，不是从真实支付用户总体进行统计推断。确定性边界和全因子场景用于检查行为，不作为重复独立统计样本。

## 复现与归档

在仓库根目录运行README中的安装、单元测试和两个实验命令。主实验会重建交易、日志和主要结果表；追加命令重建M2_full/M3的校准、测试、差值和清单。

[主清单](../experiment_manifest.csv)及[追加清单](../outputs/tables/robust_manifest.csv)保存归档运行的种子、规模和数据摘要。运行时间受机器影响；同一种子在已记录环境下应生成相同交易。升级依赖后应重新核对，不能仅凭种子相同就保证跨版本逐字节一致。

[verification.json](../outputs/logs/verification.json)是此前归档检查的证据，含环境、源文件摘要和150万条决策记录的复核规模：30万笔交易分别经过五种策略，共150万条决策。它不表示150万笔独立交易，也不会在每次复跑后自动更新。

`tamper_subset.csv`、`boundary_cases.csv`和PNG图片是归档附加检查与展示文件，两个实验入口不会自动重新生成它们。复跑CSV会覆盖同名输出；建议在新克隆中复现，避免把小规模试跑结果和归档表混在一起。核心源码和实验参数本次未改变，原有论文的数值也保持不变。
