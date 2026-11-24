"""Build paper and figures from saved results. All observations are SYNTHETIC."""
from pathlib import Path
import json,re,csv,math
import pandas as pd
from PIL import Image,ImageDraw,ImageFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Table,TableStyle,Image as RLImage
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY
from docx import Document
from docx.shared import Pt,Cm,RGBColor
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from xml.sax.saxutils import escape
R=Path(__file__).resolve().parents[1];P=R/'paper';P.mkdir(exist_ok=True)
F=R/'outputs/figures';F.mkdir(parents=True,exist_ok=True)
font='C:/Windows/Fonts/simsun.ttc'
pdfmetrics.registerFont(TTFont('Song',font,subfontIndex=0))
pdfmetrics.registerFont(TTFont('Hei','C:/Windows/Fonts/simhei.ttf'))
S=pd.read_csv(R/'outputs/tables/summary.csv');means=S.pivot(index='policy',columns='metric',values='mean')
contr=pd.read_csv(R/'outputs/tables/paired_contrasts.csv')
def pct(x):return f'{x*100:.2f}%'
def val(m,k):return pct(means.loc[m,k]) if k!='ELP' else f'{means.loc[m,k]:.2f}'
def ci(ref,k):
 z=contr[(contr.contrast=='M3 - '+ref)&(contr.metric==k)].iloc[0]
 return f"{z['mean']*100:.2f}个百分点，95%区间[{z['lo']*100:.2f}, {z['hi']*100:.2f}]"
def chart(name,title,series,xlabel,ylabel,xmax=1,ymax=1):
 im=Image.new('RGB',(1500,850),'white');d=ImageDraw.Draw(im);ft=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',28);small=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',23)
 left,top,w,h=150,110,1160,580
 d.text((left,25),title,font=ft,fill='#172e47')
 for i in range(6):
  x=left+w*i/5;y=top+h-h*i/5
  d.line((left,y,left+w,y),fill='#dbe1e8',width=2);d.text((left-110,y-15),f'{ymax*i/5:.2f}',font=small,fill='black');d.text((x-20,top+h+15),f'{xmax*i/5:.2f}',font=small,fill='black')
 palette=['#21618c','#c26426','#29915c','#a14571']
 for j,(label,points) in enumerate(series):
  xy=[(left+x/xmax*w,top+h-y/ymax*h) for x,y in points]
  if len(xy)>1:d.line(xy,fill=palette[j%4],width=5)
  for x,y in xy:d.ellipse((x-7,y-7,x+7,y+7),fill=palette[j%4])
  d.text((left+260*j,770),label,font=small,fill=palette[j%4])
 d.text((left+360,720),xlabel,font=small,fill='black');d.text((20,70),ylabel,font=small,fill='black');im.save(F/name)
sw=pd.read_csv(R/'outputs/tables/thresholds.csv').groupby(['policy','threshold']).mean(numeric_only=True).reset_index()
chart('tradeoff.png','阈值扫描：安全性与合法交易自动执行',[(m,list(zip(g.UAER,g.LAER))) for m,g in sw.groupby('policy')],'未经授权自动执行率','合法自动执行率',1,1)
wg=pd.read_csv(R/'outputs/tables/weights.csv').groupby('weights').mean(numeric_only=True)
chart('weights.png','权重敏感性：同一测试样本',[(m,[(g.UAER,g.LAER)]) for m,g in wg.iterrows()],'未经授权自动执行率','合法自动执行率',.5,1)
ab=[(m,[(means.loc[m,'UAER'],means.loc[m,'LAER'])]) for m in ['M1','M2','M3','M3_no_integrity']]
chart('ablation.png','主机制与完整性验证消融',ab,'未经授权自动执行率','合法自动执行率',1,1)
gr=pd.read_csv(R/'outputs/tables/groups.csv').groupby(['policy','group']).mean(numeric_only=True).reset_index()
chart('groups.png','单信号与多信号分组：未经授权执行',[(m,[(0 if row['group']=='single' else 1,row['UAER']) for _,row in g.sort_values('group',ascending=False).iterrows()]) for m,g in gr[gr.policy.isin(['M1','M2','M3'])].groupby('policy')],'0 单信号；1 多信号','未经授权自动执行率',1,1)
# Simple architecture figure, no generated illustrations.
im=Image.new('RGB',(1500,440),'white');dr=ImageDraw.Draw(im);ft=ImageFont.truetype('C:/Windows/Fonts/msyh.ttc',29)
for i,t in enumerate(['已确认结构化委托','硬约束检查','风险与升级决策','执行前重新验证','模拟执行及日志']):
 x=20+i*297;dr.rounded_rectangle((x,120,x+270,280),20,outline='#244c70',width=4);dr.text((x+10,177),t,font=ft,fill='#172e47')
 if i<4:dr.line((x+270,200,x+295,200),fill='black',width=4)
im.save(F/'architecture.png')
pages=[]
def page(title,*blocks):pages.append((title,list(blocks)))
def img(name,caption):return ('image',name,caption)
def table(header,rows):return ('table',[header,*rows])
page('面向消费者委托支付的金融智能体交易级授权机制研究',
'——风险敏感型规则引擎设计与仿真评估',
'Transaction-Level Authorization for Consumer-Delegated Agentic Payments: Design and Simulation Evaluation of a Risk-Sensitive Rule Engine',
'金融科技导论期末研究计划（Research Proposal）',
'摘要',
'当智能体代表消费者提交支付指令时，身份认证并不自动说明具体交易符合委托。本文拟研究如何将已确认的消费者委托转化为机器可验证的交易权限，并在硬性边界内结合多因素风险控制与执行前完整性验证。理论上，以委托代理的监督成本说明控制需求，以不完全契约说明事前范围的局限，再以属性访问控制实现可检查的运行时决策。研究增量定位于消费者购物付款和个人转账的操作化与策略比较，不主张首次提出动态授权或运行时治理。',
f'已完成的探索性仿真使用完全人工生成的数据，设置仅授权书、固定规则及风险敏感型三种机制；每个种子10000条、30个种子，采用共同交易配对评价。基准设定下，M3未经授权自动执行率为{val("M3","UAER")}，合法交易自动执行率为{val("M3","LAER")}，升级率为{val("M3","ER")}。这些数值用于检验机制和识别研究设计问题，不代表真实支付系统的性能。后续研究拟引入独立任务标注、审批行为和时序账户约束，对机制的外部效度进行验证。',
'关键词：金融智能体；消费者委托支付；交易级授权；属性访问控制；合成仿真',
'一、引言',
'本研究将授权层作为分析单位：输入是消费者已确认的结构化支付委托，输出是对一笔候选交易的允许、观察、升级或拒绝。IMF的支付分层讨论提示，需要在概率性智能体行为与确定性授权要求之间设置明确边界[1]。本文既不测试自然语言理解，也不接入账户、资金或结算接口。')
page('一、引言与研究问题',
'1.1 问题的金融含义',
'例如，用户允许Agent购买500元以内的耳机。一笔220元付款若在确认后被替换收款方，金额仍满足上限，却可能背离任务；反之，向首次购买的正规商户付款也可能完全符合任务。前者说明额度检查不充分，后者说明一见陌生收款方就升级可能增加监督负担。本文研究能否同时控制这两种错误。这里的“未经授权”相对模拟任务意图与有效委托定义，不等同于法律上的未经授权支付认定。',
'1.2 研究问题',
'主问题：如何将用户委托意图转化为机器可验证的交易权限，并通过风险敏感型规则控制智能体执行？相较静态范围检查与固定阈值，能否兼顾安全性和合法交易效率？',
'RQ1关注结构化、可验证和可撤销的授权表达；RQ2关注金额、收款方新颖性、任务一致性、交易频率与环境异常的风险作用；RQ3关注硬约束、风险分级与人工审批的组合；RQ4关注安全、合法自动执行及人工干预成本之间的权衡。',
'1.3 研究价值与边界',
'理论价值在于把监督成本与权限表达联系起来；方法价值在于将治理要求转为可重复的动作级测试。本文不赋予AI独立法律代理人资格，不推断消费者偏好，不训练大模型，也不声称覆盖反洗钱、系统性风险或全部支付欺诈。授权额度在当前实现中指每笔交易上限，不是可重复使用的账户余额或累计预算。',
'研究计划将正式验证留待未来实施。本次已运行的30批合成交易仍属于探索性模拟：规模较大并不使人工分布成为真实消费者样本。结果的价值是暴露控制逻辑、指标与假设之间的关系。')
page('二、文献综述与研究定位',
'2.1 从支付分层到可验证委托',
'IMF的分层分析提供支付语境，但没有替代交易权限规则[1]。South等的同行评审立场论文强调第三方应核验委托主体与范围，并讨论OAuth、OpenID Connect和自然语言权限表达[3]。该文给出基础设施方向，未提供本文场景中的三机制性能估计。二者分别回答“控制位于哪个环节”和“谁能证明其权限”，共同提示授权层需要可机器检查的接口。',
'2.2 通用治理与细粒度授权已有充分起点',
'SAFR 1.1已提出身份、控制库、决策引擎和审计日志，以及Deny、Escalate、Auto-Execute和Observe四种运行时处置[2]。其为官方托管白皮书，明确不构成监管指导或监督预期。NCCoE的2026概念文件征求身份授权实践意见，其初始重点是企业用例，仍是草案而非最终标准[4]。因此本文不能把四态运行时控制当成原创架构。',
'RFC 9396已通过authorization_details表达细粒度交易要求，包括金额与收款方；RFC 8693讨论令牌交换中的委托语义[8-9]。这些协议规范说明结构化支付权限并非全新概念，但不能据此认定某一风险权重有效。NIST零信任架构要求资源访问决策不能仅依赖位置或既往信任[10]；将其转换为每笔支付执行前的检查，是本文的场景适配。',
'2.3 批判性比较与研究缺口',
'协议保护身份、令牌和消息，并不自动保护任务含义。DPoP限制令牌使用者，OAuth安全最佳实践处理协议威胁，但错误收款方仍可能由合法持有令牌的Agent提交[11-12]。另一方面，通用治理框架并不告诉消费者应承受多少升级成本。本文拟比较策略的安全—效率边界，区分风险评分与完整性模块的作用，而非对已有框架作首次性声明。')
page('三、理论基础与综合分析框架',
'3.1 委托代理的分析类比',
'Jensen与Meckling第1.4节将代理成本分为委托方的监督支出、执行方的约束支出和剩余损失，并说明监督不限于观察，也包括预算限制和操作规则[5]。本文据此把升级审批理解为监督成本，把执行边界理解为控制安排，把未授权执行造成的损害理解为剩余损失的技术类比。Agent没有被赋予独立效用函数或法律人格，故本文既不完整移植企业所有权模型，也不把模拟成本指数当作原理论的估计量。',
'3.2 不完全契约与动态检查',
'Hart与Moore研究不完全契约及事后修订[6]。公开可读的1985工作论文引言进一步区分不完全性与信息不对称：双方即使具有相同信息，也可能难以描述或验证全部状态依存条款[17]。这比“用户不知道Agent在做什么”更具体。本文借此解释为何事前权限需要配合保留批准权的升级入口，而非允许评分自动扩大委托。1985工作论文与1988发表版分别著录，不假定两版本逐页相同，也不从原模型推出AI语言理解效果。',
'3.3 ABAC与内控的操作化',
'ABAC通过主体、对象、操作与环境属性判定访问权限[7]。在本文中，主体为用户及被授权Agent，资源是待执行交易，操作为购物支付或转账，环境包括时间和异常信号。执行门体现职责分离的设计原则：Agent提出指令，规则引擎评价，执行门再次检查，日志记录依据。该分离是原型中的控制安排，不声称已通过金融机构内控认证。',
'3.4 逻辑闭环与竞争性解释',
'委托带来监督需求；不完全性使静态范围难以覆盖任务偏离；ABAC将边界映射为可执行规则；风险分级在边界内分配监督；日志保留复核依据。竞争性解释是：M3优势可能完全来自更严格的拒绝或完整性模块，评分本身未改善效率；固定规则还可能更善于拦截单项极端风险。这要求采用消融和相近安全水平下的比较。')
page('四、研究假设与可证伪条件',
table(['假设','检验对象与判据'],[
['H1','M3相对M1的UAER配对差值小于0'],
['H2','校准安全目标下比较测试集UAER、LAER和ER'],
['H3','M3相对M2的安全优势在多信号组更大'],
['H4','完整性验证相对移除模块降低篡改未经授权执行']]),
'H1：与仅范围检查相比，动态机制降低未经授权自动执行率。除总体比较外，M3_no_risk保留完整性而移除评分，避免把完整性收益误归于动态评分。',
'H2：在相近安全控制水平下，M3改善合法自动执行与人工干预之间的权衡。本次预设校准UAER不高于5%，在独立种子9000上各选合法自动执行率最高的候选阈值，再固定阈值比较种子0—29。若测试集不能维持安全目标，或合法通过提高伴随实质安全退化，不认定H2获支持。5%只是比较用的研究者设定，不是金融业务可接受损失标准。',
'H3：多个风险信号同时出现时，M3相较M2的控制优势更明显。高信号定义为风险归一值不低于0.6，单信号为恰有一项，多信号为至少两项。差异统计量为D=(UAER_M3−UAER_M2)_多−(UAER_M3−UAER_M2)_单；D小于0符合该方向。该分组含不同潜在任务构成，只能视为效果异质性，不能认定为因果交互或风险协同。',
'H4：执行前完整性验证降低决策后篡改造成的未经授权执行。比较M3与M3_no_integrity的同一笔交易，并报告篡改子样本。该假设依赖可信快照、不可绕过执行门和所有未重新授权的收款方替换均不被允许的威胁模型。',
'这些假设允许出现不支持或参数依赖结果。置信区间只描述模拟种子的波动，不替代真实用户统计推断。')
page('五、交易级授权机制设计',
'5.1 授权书与不可覆盖的硬约束',
'授权书包含委托编号、Agent标识、允许操作、每笔金额上限、币种、禁止收款方、有效期及撤销状态。交易包含对应标识、金额、收款方及任务和环境属性。所有机制均拒绝撤销、到期、Agent不匹配、操作越界、金额超过上限、币种不符、禁止收款方以及非有限或非正金额。到期采用now≥expires，金额等于上限可通过。金额用整数分保存，当前生成器不模拟浮点货币结算。',
'5.2 风险变量与评分方向',
'设A=min(金额/上限,1)，P为首次收款方指示，S为任务一致性，V为归一化频率异常，E为环境异常。所有风险输入位于[0,1]。由于S越大越安全，令S_risk=1−S；否则直接将一致性正向相加会颠倒风险含义。',
'R = w_A A + w_P P + w_S (1−S) + w_V V + w_E E；各w≥0，且Σw=1。',
'基准权重依次为(0.20,0.20,0.25,0.20,0.15)。它们是研究者设定，无经验最优性含义。R是可解释控制指数，不是经过校准的损失概率。线性评分存在补偿效应：低风险项可能稀释单项高风险；因此硬约束独立于评分，单项极端风险的额外否决规则留待未来验证。',
img('architecture.png','图1 交易级规则引擎和执行门。资料来源：作者实现；框架思路参考[2-4,7]。'),
'M1仅检查委托。M2额外在A≥0.8、P≥1或V≥0.6时升级。M3在R<0.25时自动执行，0.25≤R<0.45时观察执行，0.45≤R<0.70时升级，R≥0.70时拒绝。任何硬约束失败均优先拒绝。')
page('五、执行前验证与审计边界',
'5.3 执行状态与审批',
'AUTO_EXECUTE表示无人工确认执行；OBSERVE同样执行但附监测标记；ESCALATE暂停等待审批，本次不建立审批行为模型，故不计为完成；DENY拒绝。主自动执行指标将前两者合并，同时单列OBS占比。两类自动状态在技术吞吐上相同，监测标记的真实运营成本尚未计入。',
'5.4 决策与执行之间的完整性',
'M3对交易标识、金额、币种、操作、收款方、委托边界及风险属性生成SHA256摘要；执行时对当前快照重新摘要并比较。所有机制在执行门重新检查硬约束，故M1和M2不能靠“未再次检查撤销”获得不公平的速度收益。M3还拒绝其他绑定字段的未批准变化，包括仍在金额上限内的收款方替换。',
'本代码采用Python排序JSON约定，不声称实现RFC 8785的跨语言规范化[13]。摘要只说明两份可信快照是否相同，不提供身份认证或不可抵赖；攻击者若能同时篡改可信摘要或绕过执行门，保护失效。HTTP消息签名可作为未来工程参考，但本次未实现签名、密钥生命周期或DPoP[11,14]。',
'5.5 审计与当前工程约束',
'日志记录交易和委托编号、Agent、规则版本名、风险值、决策、原因、前后摘要、时间及执行标志。必要字段非空率称审计完整率，不等于审计内容真实性、不可修改性或合规认证。本次M1、M2也使用相同日志仪表，以免将日志缺失设计成它们的劣势。',
'当前原型是逐交易、内存态、无网络执行器。授权来自可信字典，身份字符串匹配不等于真实认证；没有并发累计额度、交易重放保护或多方签名。所有交易编号和收款方均为人工符号，不包含个人信息。')
page('六、研究方法与合成数据设计',
'6.1 三层测试与样本来源',
'固定边界用例检验撤销、到期、越额、币种、禁止收款方、Agent不匹配、篡改和决策状态；32个二水平全因子组合检查五项风险输入的规则响应。确定性组合是探针，不当作32个独立消费者样本。Monte Carlo使用random.Random(seed)，种子0—29，每批10000条，共300000对决策前后交易。相同样本送入所有机制。',
'6.2 标签与风险信号的分离',
'先按20%的概率抽取潜在任务违约场景，并在收款方偏离、频率突发和任务不匹配间等概率分配；其他为正常场景。五个连续风险量分别围绕场景中心加标准差0.18的正态噪声，截断到[0,1]。收款方新颖性再按该维度的概率抽Bernoulli变量。正常交易中15%随机具有一项较高的金额、新颖性或频率，刻意保留合法异常。',
table(['潜在场景','A、P概率、1−S、V、E的中心'],[['正常','0.25, 0.12, 0.12, 0.20, 0.10'],['收款偏离','0.45, 0.80, 0.55, 0.30, 0.50'],['频率突发','0.55, 0.30, 0.35, 0.85, 0.40'],['任务不匹配','0.40, 0.40, 0.85, 0.35, 0.40']]),
'另以6%概率覆盖一项硬约束违规，并以6%概率在决策后替换收款方；二者均使最终交易标签为未经授权。因此最终未经授权比例不等于20%。标签不从风险评分或策略输出来定义，也未训练模型；但人为规定的标签—信号相关性仍有利于使用相似信号的策略，不能称为完全独立的现实验证。',
'每笔授权独立，交易频率为外生归一风险输入，不是从真实时间窗交易历史估计。完整性攻击不改变风险值，仅替换收款方，避免把攻击效果与评分变化混淆。')
page('六、指标、统计与实验安排',
table(['指标','分子 / 分母 或定义'],[['UAER','未经授权且自动执行数 / 未经授权数'],['LAER','合法且自动执行数 / 合法数'],['FDR','合法且DENY数 / 合法数'],['ER','ESCALATE数 / 全部交易数'],['ELP','总模拟成本 / 全部交易数'],['AC','必要审计字段完整记录数 / 全部记录数']]),
'ELP = [Σ(未经授权自动执行的金额元数) + 10×合法拒绝数 + 1×升级数] / N。损失金额权重1、合法拒绝成本10、升级成本1均为人工假设，单位可理解为模拟成本元；不代表银行损失或消费者福利估计。未计合法交易等待、观察标记与攻击未遂成本，后续需联合调整成本比例。',
'实验一比较三机制及两消融的主指标。实验二扫描阈值t∈{0.2,0.3,0.4,0.45,0.5,0.6,0.7,0.8}；M3阈值取(t/2,t,0.95)，M2取(A阈值t、P阈值1、V阈值t)。M2不是被证明最优的固定规则，其未使用S和E也可能解释部分差距，未来应加入相同信息集的更强固定基准。',
'实验三检验单信号与多信号组的策略差异，补充确定性组合探针。实验四分别移除M3评分和完整性模块。实验五使用等权、任务偏重和金额偏重的权重，并在噪声0.12/0.30、潜在违规比例0.10/0.35的四种生成分布下重复小规模检验。',
'统计单位为独立生成种子而非单条交易。主表先求每个种子的比例，再等权平均。Bootstrap以种子为单位有放回抽2000次，给出均值或配对差值的2.5%和97.5%分位区间；配对保持同一交易集。该区间表示既定生成过程下的Monte Carlo波动；不是现实总体置信区间。H1—H4与多项探索性对比不据此宣称经过多重检验校正的显著发现。')
mainrows=[[{'M3_no_risk':'M3-R','M3_no_integrity':'M3-I'}.get(m,m),*[val(m,k) for k in ['UAER','LAER','FDR','ER','ELP']]] for m in ['M1','M2','M3','M3_no_risk','M3_no_integrity']]
page('六、已完成的探索性模拟结果',
table(['机制','UAER','LAER','FDR','ER','ELP'],mainrows),
'表1 30个种子等权平均。前四项为比例，ELP为每笔模拟成本；数据全部人工合成。M3-R移除评分、保留完整性；M3-I移除完整性、保留评分，分别对应代码no_risk与no_integrity。',
f'M3相对M1的UAER变化为{ci("M1","UAER")}；相对M2为{ci("M2","UAER")}。这些配对结果回答的是当前参数下的策略差异，不证明某种机制在任意任务分布中更优。',
f'移除评分后UAER为{val("M3_no_risk","UAER")}，移除完整性后为{val("M3_no_integrity","UAER")}。M3相对无完整性版本的UAER差值为{ci("M3_no_integrity","UAER")}。这表明完整性与评分的效果应分别归因；不能把它们合并解释为加权评分本身的成果。',
f'各策略AC均为{val("M3","AC")}，原因是实验使用同一审计仪表并明确填入字段。这是实现一致性的验证，不能据此声称M3具有更强防篡改日志。M3的OBSERVE占全部交易比例为{val("M3","OBS")}，已计入自动执行。',
'结果表、每种子指标、配对差值、完整决策日志和原始生成参数均在本地项目中保存。当前所有结果为本次真实运行输出；未来计划中的用户实验、协议接入和真实支付测试均未开展。')
h2=pd.read_csv(R/'outputs/tables/matched_safety.csv');h3=pd.read_csv(R/'outputs/tables/h3_contrast.csv').iloc[0]
h2text='独立校准中至少一个策略没有满足5%目标的候选点，因此不作等安全水平优越性断言。'
if len(h2)==2:
 a=h2.set_index('policy');h2text=f'独立校准选择M2阈值{a.loc["M2","threshold"]:.2f}、M3阈值{a.loc["M3","threshold"]:.2f}；测试集UAER依次为{pct(a.loc["M2","UAER"])}、{pct(a.loc["M3","UAER"])}，LAER为{pct(a.loc["M2","LAER"])}、{pct(a.loc["M3","LAER"])}，ER为{pct(a.loc["M2","ER"])}、{pct(a.loc["M3","ER"])}。两者测试均低于5%，但并非完全等安全；结果仅支持预设网格中的H2方向。M3较M2合法执行提高67.57个百分点（95%区间67.37至67.76），升级减少53.05个百分点。更强的同信息集固定基准仍可能缩小差距。'
page('六、安全与效率权衡及假设判断',
img('tradeoff.png','图2 阈值扫描结果。各点为30个种子均值，连线仅用于识别同一策略的候选点。'),
h2text,
f'H3的异质性对比D为{h3["mean"]*100:.2f}个百分点，95%种子Bootstrap区间为[{h3["lo"]*100:.2f}, {h3["hi"]*100:.2f}]。'+('方向符合H3，但分组构成差异妨碍因果交互解释。' if h3['hi']<0 else '该结果不能支持预设的“多信号时优势更大”方向；需保留此不支持结果。'),
'H1只在当前合成分布中获得方向性检验；H4只在所设的决策后替换攻击中得到检验。H2的阈值网格和M2信息集限制了结论，H3分组比较也不是对真实风险协同的证明。完整性验证与风险控制都不能替代对委托本身真实性的验证。')
page('六、消融与敏感性分析',
img('ablation.png','图3 主机制与移除完整性模块的位置。点越靠左，模拟安全指标越好；越高，合法自动执行率越高。'),
img('weights.png','图4 权重敏感性。基准、等权、任务偏重和金额偏重均使用相同测试交易。'),
 '四组权重下UAER约17.52%—23.13%，LAER约95.24%—99.24%；任务偏重在当前人工分布表现较好，不意味着经验最优。四种噪声与违规率组合下，M3的UAER约14.83%—26.09%，LAER约93.29%—99.04%，结果随分布改变。后续需外部校准、同信息集基准及成本比例联合扫描。')
rob=pd.read_csv(R/'outputs/tables/robust_test.csv').groupby('policy').mean(numeric_only=True)
rc=pd.read_csv(R/'outputs/tables/robust_contrasts.csv').set_index('metric')
page('六、追加同信息集稳健性复核',
'为检查M3优势是否仅源于使用更多信息，主实验完成后追加固定规则M2_full：它使用同样的A、P、1-S、V、E，只要任一风险项不低于共同阈值就升级，并使用与M3相同的完整性验证。该比较属于追加探索性复核，不追溯声称为主实验事前预注册。',
'追加校准使用独立种子9100的10000笔交易；候选阈值0.15至0.95、步长0.05，按UAER不高于5%且LAER最高选取。测试集改用20000—20029这30个新种子，每个10000笔，避免沿用已看过的主实验结果作最终验证。M3的阈值设为(t/2,t,0.99)，固定规则仅调整共同阈值；两者信息、执行门和样本一致。',
table(['策略','阈值','UAER','LAER','ER'],[[p,f'{rob.loc[p,"threshold"]:.2f}',pct(rob.loc[p,'UAER']),pct(rob.loc[p,'LAER']),pct(rob.loc[p,'ER'])] for p in ['M2_full','M3']]),
f'表2 追加测试集30种子均值。M3相对M2_full的LAER差为{rc.loc["LAER","mean"]*100:.2f}个百分点，95%种子Bootstrap区间[{rc.loc["LAER","lo"]*100:.2f}, {rc.loc["LAER","hi"]*100:.2f}]。UAER差为{rc.loc["UAER","mean"]*100:.2f}个百分点。',
'结果使“完全由信息集或完整性门不同造成优势”这一解释在当前分布内受到限制，但仍不能证明加权评分普遍优于固定规则：共同阈值OR规则会被单项风险支配，尤其收款方新颖性为二元变量；更一般的分项阈值和组合规则可能缩小差距。两策略测试风险也不严格相等，因此只作为H2的补充方向性证据。',
'另一个值得警惕的结果是主实验合法拒绝率均为0。它不说明机制不会误拒，而说明当前正常样本中心及高拒绝阈值很少产生足够极端的合法组合。未来必须加强这类压力样本，再评估拒绝成本。')
page('七、未来研究安排与可行性',
'7.1 待实施的验证阶段',
'第一阶段拟在2026年11月25日至12月1日冻结授权模式与评价预案，增加对未知收款方但合法任务、单项极端风险和高噪声环境的对抗案例；由独立标注者根据任务卡判断合法性，避免规则设计者同时决定标签。先采用无资金的纸面任务和本地支付沙箱，未经必要审批不采集个人信息。',
'第二阶段拟于12月2日至8日在已追加的共同阈值OR基准之外，加入更一般的分项阈值、逻辑组合和仅S/E规则，继续区分“信息更多”与“组合方式不同”的收益。通过独立校准固定参数，再对分布错设、风险信号失真和成本比例作联合稳健性分析。',
'第三阶段拟于12月9日至13日建模审批延迟、拒绝与批准行为，加入累计预算、幂等键、重放攻击和并发撤销。升级不再只是比例，而需估计单位时间人工负担与合法任务完成时间。若资源不足，优先保留现有离线原型并明确缩小结论，不使用未经验证的真实数据替代。',
'第四阶段拟于12月14日至15日复核引用、数值、排版和作业规范，形成最终提交版本。截止为2026年12月16日22:00（北京时间）；按老师要求在Canvas上传PDF，并按课程安排交纸质版。论文文件应改名为“研究计划_姓名_学号”。',
'7.2 与现有规范的关系',
'AI RMF的治理、映射、测量和管理可组织后续评估流程，生成式AI画像有助于检查生命周期风险[15-16]，但二者不提供本研究的风险权重或可接受损失阈值。任何协议集成与真实业务实施还需专门的身份、数据、法律和支付系统评估，本研究不以运行成功替代这些要求。')
page('七、预期贡献与研究局限及八、结论',
'7.3 预期贡献',
'拟形成一套消费者任务到交易属性的可检查表达、一组硬约束优先的决策规则，以及能追溯参数和结果的比较实验。贡献是把已有授权与治理思路操作化并公开可复现方法，而非首创运行时授权、风险控制或智能体治理。研究也可能发现固定规则在某些分布下更有效，这同样有助于界定何时值得使用多因素机制。',
'7.4 关键局限',
'合成数据的潜在场景、异常发生率、噪声、权重与成本均人为给定；现实中攻击者适应规则、不同信号相关及观测缺失可能改变比较。交易间独立假设忽略累计额度耗尽、账户余额、共同环境冲击和连续任务依赖。风险信号既可能误测，也可能被Agent操纵，本次没有可信传感器或跨服务身份链。',
'完整性验证以可信快照和不可绕过执行门为前提；所有收款方替换均标为未授权，因此不能推论合法改价、用户重新批准或消息中间转换的处理效果。审计完整率只测字段。规则引擎未接真实认证和结算，运行时间不是金融级延迟指标。',
'文献方面，官方标准与指南能支持设计，却不能替代同行评审的支付效果证据。Jensen与Meckling的期刊全文已核读；Hart与Moore读取MIT机构库的1985工作论文，1988发表版仅核对元数据，不能将两版本混同。IMF完整PDF仍未取得，本文只据官方网页引用分层认识。可读性限制与版本区别均在文献矩阵披露。',
'八、结论',
'本研究计划提出在不可突破的委托约束内，结合风险分级、人工升级与执行前验证来约束消费者支付Agent。探索性模拟已用于验证代码、比较策略并暴露识别问题，不能作为真实银行环境有效性的证据。后续验证将围绕同信息集基准、独立任务标签、时序约束和审批行为展开，以检验安全与效率权衡能否超越本次人工设定。')
refs=json.loads((R/'literature/references.json').read_text(encoding='utf-8'))
# Numeric citation order follows first occurrence; matrix IDs remain stable.
order=[]
def renumber(text):
 def sub(match):
  ids=[]
  for part in match.group(1).split(','):
   if '-' in part:
    a,b=map(int,part.split('-'));ids.extend(range(a,b+1))
   else:ids.append(int(part))
  for n in ids:
   if n<1:return match.group(0)
  for n in ids:
   if n not in order:order.append(n)
  return '['+','.join(str(order.index(n)+1) for n in ids)+']'
 return re.sub(r'\[([0-9]+(?:[-,][0-9]+)*)\]',sub,text)
for i,(title,blocks) in enumerate(pages):
 for j,b in enumerate(blocks):
  if isinstance(b,str):blocks[j]=renumber(b)
  elif b[0]=='image':blocks[j]=(b[0],b[1],renumber(b[2]))
refs=[dict(refs[n-1],id=i+1) for i,n in enumerate(order)]
pd.DataFrame({'literature_matrix_id':order,'paper_reference_number':range(1,len(order)+1)}).to_csv(R/'literature/citation_mapping.csv',index=False)
for start in range(0,len(refs),9):
 page('参考文献'+('（续）' if start else ''),*[f'[{e["id"]}] {e["authors"].upper()}. {e["title"]}[{e["type_code"]}]. {e["source"]}, {e["year"]}. {e["url"]}.' for e in refs[start:start+9]])
# Unified source for both formats.
def normalize(value):
 if isinstance(value,str):return value.replace('\u2212','-')
 if isinstance(value,tuple):return tuple(normalize(v) for v in value)
 if isinstance(value,list):return [normalize(v) for v in value]
 return value
pages=normalize(pages)
(P/'paper_content.json').write_text(json.dumps(pages,ensure_ascii=False,indent=2),encoding='utf-8')
md=[];story=[];doc=Document();sec=doc.sections[0];sec.page_width=Cm(21);sec.page_height=Cm(29.7);sec.top_margin=sec.bottom_margin=Cm(2.0);sec.left_margin=sec.right_margin=Cm(2.0)
for name in ['Normal','Title','Heading 1','Heading 2']:
 st=doc.styles[name];st.font.name='Times New Roman';st.font.size=Pt(12);st.font.color.rgb=RGBColor(0,0,0);st.element.rPr.rFonts.set(qn('w:eastAsia'),'宋体');st.paragraph_format.space_after=Pt(6)
doc.styles['Normal'].paragraph_format.line_spacing=1.25
style=ParagraphStyle('body',fontName='Song',fontSize=12,leading=18,wordWrap='CJK',spaceAfter=9)
heading=ParagraphStyle('heading',parent=style,fontName='Hei',fontSize=12,leading=19,spaceAfter=14)
for pi,(title,blocks) in enumerate(pages):
 if pi:story.append(PageBreak());doc.add_page_break()
 md.append('# '+title+'\n');story.append(Paragraph(escape(title),heading));doc.add_heading(title,level=1)
 for b in blocks:
  if isinstance(b,tuple) and b[0]=='image':
   path=F/b[1];im=Image.open(path);wid=475;hei=wid*im.height/im.width;story.extend([RLImage(str(path),width=wid,height=hei),Paragraph(escape(b[2]),style)])
   doc.add_picture(str(path),width=Cm(15.0));doc.add_paragraph(b[2]);md.append(f'![{b[2]}](../outputs/figures/{b[1]})\n')
  elif isinstance(b,tuple) and b[0]=='table':
   rows=b[1];ncol=len(rows[0]);widths=([70,405] if ncol==2 else [100]+[75]*(ncol-1));tab=Table([[Paragraph(escape(str(x)),style) for x in row] for row in rows],colWidths=widths)
   tab.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eef2f5')),('LINEBELOW',(0,0),(-1,0),.5,colors.grey),('LINEBELOW',(0,-1),(-1,-1),.5,colors.grey),('LEFTPADDING',(0,0),(-1,-1),4),('RIGHTPADDING',(0,0),(-1,-1),4)]));story.extend([tab,Spacer(1,10)])
   t=doc.add_table(rows=0,cols=ncol);t.style='Table Grid'
   t.autofit=False
   column_widths=[3.0,14.0] if ncol==2 else [17.0/ncol]*ncol
   for col,cw in zip(t.columns,column_widths):col.width=Cm(cw)
   for row in rows:
    cells=t.add_row().cells
    for c,v,cw in zip(cells,row,column_widths):c.text=str(v);c.width=Cm(cw)
   md.append('\n'.join('| '+' | '.join(map(str,r))+' |' for r in rows)+'\n')
  else:
   ishead=bool(re.match(r'^(?:[一二三四五六七八]|[1-7]\.[1-9]|摘要|关键词)',b)) and len(b)<50
   story.append(Paragraph(escape(b),heading if ishead else style));doc.add_paragraph(b,style='Heading 2' if ishead else 'Normal');md.append(b+'\n')
def footer(canvas,document):
 canvas.setFont('Song',12);canvas.drawCentredString(297.6,28,str(document.page))
SimpleDocTemplate(str(P/'paper.pdf'),pagesize=(595.28,841.89),rightMargin=56.7,leftMargin=56.7,topMargin=48,bottomMargin=45).build(story,onFirstPage=footer,onLaterPages=footer)
footerp=sec.footer.paragraphs[0];footerp.alignment=1
field=OxmlElement('w:fldSimple');field.set(qn('w:instr'),'PAGE');footerp._p.append(field)
doc.save(P/'paper.docx');(P/'paper.md').write_text('\n'.join(md),encoding='utf-8')
print(f'Built {len(pages)} planned pages, docx and PDF')
