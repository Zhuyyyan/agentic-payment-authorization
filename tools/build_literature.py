from pathlib import Path
import csv,json
R=Path(__file__).resolve().parents[1];D=R/'literature';D.mkdir(exist_ok=True)
# Metadata checked against source first pages, official publication page or Crossref.
entries=[
('Davidovic S; Tourpe H','2026','How Agentic AI Will Reshape Payments','IMF Notes 2026/004','R','https://www.imf.org/en/Publications/imf-notes/Issues/2026/04/22/how-agentic-ai-will-reshape-payments-575560','国际组织研究','意图、授权和结算分层；概率决策与确定性支付要求','概念与政策分析','未提供消费者交易级策略比较','1、2、5章','官方网页已读；PDF下载403；完整PDF未取得'),
('Monetary Authority of Singapore','2026','Safeguards for Agentic Finance at Runtime Version 1.1','MAS white paper, 9 October 2026','R','https://www.mas.gov.sg/-/media/mas-media-library/development/fintech/ai-safr/safr-v1-1.pdf','官方托管白皮书 非监管规则','身份、控制库、决策引擎、日志和四种运行时决策','参考架构与案例','通用架构不提供本文的仿真参数或消费者比较','2、5章','浏览工具取得29页PDF文本；直接下载实际为Maintenance HTML，不算PDF'),
('South T; Marro S; Hardjono T; Mahari R; Whitney C D; Chan A; Pentland A','2025','Position: AI Agents Need Authenticated Delegation','ICML, PMLR 267: 82211-82231','C','https://proceedings.mlr.press/v267/south25a.html','同行评审立场论文','身份认证、委托范围与可审计权限链','立场论证与协议扩展设计','不是消费者支付机制效果的实证检验','2、5章','元数据和完整开放PDF取得；重点读第2至4节'),
('Booth H; Fisher B; Galluzzo R; Roberts J','2026','Accelerating the Adoption of Software and AI Agent Identity and Authorization','NIST NCCoE, February 2026','R','https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf','征求意见概念草案','将身份、认证、授权与审计标准用于软件和AI Agent','项目概念与问题征询','初始企业场景不覆盖全部外部消费者Agent','2、7章','完整PDF取得；非最终标准'),
('Jensen M C; Meckling W H','1976','Theory of the Firm: Managerial Behavior, Agency Costs and Ownership Structure','Journal of Financial Economics, 3(4):305-360','J','https://doi.org/10.1016/0304-405X(76)90026-X','同行评审理论论文','代理成本与监督、约束和剩余损失','经济理论','原文企业主体与AI不同；只能分析类比','3章','Crossref与56页期刊版PDF核验；重点第1.4节、印刷页308—309；开放副本liuyanecon.com'),
('Hart O; Moore J','1988','Incomplete Contracts and Renegotiation','Econometrica, 56(4):755-785','J','https://doi.org/10.2307/1912698','同行评审理论论文','不完全契约与事后调整','契约理论模型','不是自然语言或AI授权的直接经验结论','3章','期刊元数据核验；1988版全文仍受限；阅读1985机构库工作论文，另列文献17，不冒充发表版'),
('Hu V C; Ferraiolo D; Kuhn R; et al.','2014','Guide to Attribute Based Access Control (ABAC) Definition and Considerations','NIST SP 800-162, updated 2019','R','https://doi.org/10.6028/NIST.SP.800-162','正式技术指南','主体、对象、操作、环境属性共同参与访问决策','定义与架构指南','未指定支付风险评分和阈值','3、5章','完整PDF核验'),
('Lodderstedt T; Richer J; Campbell B','2023','OAuth 2.0 Rich Authorization Requests','RFC 9396','S','https://www.rfc-editor.org/rfc/rfc9396','标准轨道RFC','JSON authorization_details支持金额和收款方等细粒度授权','协议规范','不是本项目风险模型的性能证明','2、5章','原文第1、2、6、12节'),
('Jones M; Nadalin A; Campbell B; et al.','2020','OAuth 2.0 Token Exchange','RFC 8693','S','https://www.rfc-editor.org/rfc/rfc8693','标准轨道RFC','区分委托和身份冒用语义及令牌交换','协议规范','不直接表达完整消费者任务语义','2章','原文介绍、令牌语义与安全讨论'),
('Rose S; Borchert O; Mitchell S; Connelly S','2020','Zero Trust Architecture','NIST SP 800-207','R','https://doi.org/10.6028/NIST.SP.800-207','正式技术指南','每次资源访问需动态认证授权决策','架构与部署模型','网络/企业访问场景需要支付适配','2、5章','完整PDF；第2节原则'),
('Fett D; Campbell B; Bradley J; et al.','2023','OAuth 2.0 Demonstrating Proof of Possession (DPoP)','RFC 9449','S','https://www.rfc-editor.org/rfc/rfc9449','标准轨道RFC','发送者约束与重放检测','密码协议规范','持有证明不能替代交易语义权限检查','2、7章','原文介绍、安全注意事项'),
('Lodderstedt T; Bradley J; Labunets A; Fett D','2025','Best Current Practice for OAuth 2.0 Security','RFC 9700, BCP 240','S','https://www.rfc-editor.org/rfc/rfc9700','最佳当前实践RFC','扩展OAuth威胁模型与安全实践','威胁分析与协议建议','本地仿真未实现OAuth协议栈','2、7章','原文摘要、令牌重放讨论'),
('Rundgren A; Jordan B; Erdtman S','2020','JSON Canonicalization Scheme (JCS)','RFC 8785','R','https://www.rfc-editor.org/rfc/rfc8785','信息类RFC 非标准轨道','确定性JSON序列化支持可重复摘要','序列化规范','本代码sort_keys是Python局部约定，不声称JCS兼容','5、7章','原文状态及设计说明'),
('Backman A; Richer J; Sporny M','2024','HTTP Message Signatures','RFC 9421','S','https://www.rfc-editor.org/rfc/rfc9421','标准轨道RFC','HTTP消息组件签名或MAC','协议与安全规范','未在本地SHA256演示中实现认证或密钥管理','5、7章','原文摘要和覆盖组件讨论'),
('National Institute of Standards and Technology','2023','Artificial Intelligence Risk Management Framework (AI RMF 1.0)','NIST AI 100-1','R','https://doi.org/10.6028/NIST.AI.100-1','官方自愿风险框架','治理、映射、测量和管理构成风险管理闭环','风险管理框架','非专门支付授权机制，无本文参数','7章','完整PDF核心四功能'),
('National Institute of Standards and Technology','2024','Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile','NIST AI 600-1','R','https://doi.org/10.6028/NIST.AI.600-1','官方风险指南','生成式AI风险及生命周期管理行动','跨领域风险画像','未对消费者支付策略作效果评估','7章','完整PDF风险和建议行动'),
('Hart O; Moore J','1985','Incomplete Contracts and Renegotiation','MIT Department of Economics Working Paper No. 367, January 1985','R','https://hdl.handle.net/1721.1/63746','机构库工作论文 非1988发表版','区分不完全性与信息不对称；研究事后修订机制','理论模型','不能把工作论文与期刊版视为逐页一致；不能由契约复杂性推出模型正式证明','3章','MIT公开API取得78页扫描PDF；核读引言、模型及修订机制讨论；SHA256见第四轮日志'),
]
fields=['id','authors','year','title','source','type_code','url','document_type','core_argument','method','limitations','used_in','verification']
with (D/'literature_matrix.csv').open('w',encoding='utf-8-sig',newline='') as f:
 w=csv.writer(f);w.writerow(fields)
 for i,e in enumerate(entries,1):w.writerow([i,*e])
(D/'references.json').write_text(json.dumps([dict(zip(fields,[i,*e])) for i,e in enumerate(entries,1)],ensure_ascii=False,indent=2),encoding='utf-8')
(D/'references.bib').write_text('\n\n'.join('@misc{ref%d,\n author={%s},\n year={%s},\n title={%s},\n howpublished={%s},\n url={%s},\n note={%s}\n}'%(i,e[0].replace(';',' and'),e[1],e[2],e[3],e[5],e[6]) for i,e in enumerate(entries,1)),encoding='utf-8')
(D/'literature_review_notes.md').write_text('''# 文献比较与核验说明

支付层次研究解决“授权处于何处”，认证委托研究解决“谁代表谁”，ABAC解决“依据哪些属性判定”，SAFR解决“动作发生时怎样治理”。这四类认识相互补充，不能将其中任何一类当作本项目首次发现。

RFC 9396已直接给出转账金额与收款方的细粒度授权例子，因而结构化授权书本身不构成新颖性主张。本文定位为场景操作化和可复现策略比较。固定规则可更保守，多因素评分也可能因稀释单项极端信号而失败；H2与H3均需保留反例。

文献以2020—2026年直接相关官方原始资料为主，保留必要奠基理论/指南及一个公开工作论文版本。17项中3项为同行评审学术论文，其中South为立场论文；另有1项1985工作论文，不当成1988发表版；其余资料明确标记。

第二轮改进：Jensen与Meckling的56页期刊版全文已取得，第1.4节明确代理成本包括监督支出、约束支出和剩余损失。Hart与Moore通过MIT公开API取得1985年工作论文78页扫描全文，单列文献17。其引言明确指出契约不完全与信息不对称可以区分；即使双方获得相同信息，也可能因描述与执行状态依存条款的成本而不完全。正文据此修正，不能把两者混为一谈。1988发表版依然只核对元数据，不将工作论文冒充发表版。

仍受限：IMF官方PDF和eLibrary全文入口403/405，MAS直接下载返回Maintenance HTML，JSTOR是挑战页；原始失败记录保留。IMF仅引用已读官方网页分层论断，不能称全文核读。浏览服务间歇连接失败。后续若取得全文，应补查具体版本与页码。
''',encoding='utf-8')
print('17 source records written')
