# 关键论断证据审查

|论断|证据|边界|
|---|---|---|
|课程为研究计划，小四，至多20页|requirements/assignment_extracted.txt|老师允许不完成实证；本次模拟为探索性补充|
|支付可从意图、授权、结算分层讨论|文献矩阵1，IMF官方网页|完整PDF未获取，不声称核读全文|
|SAFR已含四态运行时决策|文献矩阵2，初次浏览取得29页PDF文本|白皮书明确非监管要求；直接HTTP返回维护页|
|Agent需要可验证委托范围|矩阵3，South开放PDF第2—4节|同行评审立场论文，非消费者效果评估|
|NCCoE资料是草案|矩阵4，PDF封面及第7—8页|企业用例概念征询，不是最终标准|
|代理成本与不完全性可解释控制需求|矩阵5期刊全文、矩阵6期刊元数据与矩阵17工作论文全文|理论类比；不混同1985与1988版本，不声称核读1988发表版|
|细粒度金额收款方授权已有标准起点|矩阵8，RFC9396第1—2节|不能宣称首创结构化支付权限|
|H1当前设定方向获支持|paired_contrasts.csv，M3−M1 UAER|合成分布及种子波动|
|H2仅支持预设候选网格内方向|matched_safety.csv、h2_contrasts.csv|相近但不完全等安全；M2信息集较少|
|H3只检验分组效果异质性|h3_contrast.csv、factorial.csv|不能宣称因果交互；确定性探针不是独立样本|
|H4在收款方替换威胁模型下有效|tamper_subset.csv、运行时测试、完整性消融|可信快照不可绕过门；无签名、无重放防护|
|字段完整率100%|per_seed.csv AC|共同日志仪表，不代表不可抵赖或防篡改|
|M3风险降低不代表可部署|summary.csv UAER21.87%|基准残余风险高；无真实环境效果结论|


## 第二轮更新

- Jensen期刊全文取得：literature/fulltext_retry_log.json，jensen_retry，56页；第1.4节印刷页308—309支持代理成本三分法。
- Hart1985工作论文全文取得：literature/fourth_retrieval_log.json，hart_mit_api，78页；引言区分不完全性与信息不对称。矩阵17单列，不把1988期刊条目标成全文已读。
- 公平比较：robust_calibration.csv、robust_test.csv、robust_contrasts.csv，限定相同信息/执行门以及特定共同阈值OR，未声称对全部固定规则占优。
- 原生分页：native_render_audit.json，论文17页、学习稿8页；最终PDF直接由对应DOCX导出。
