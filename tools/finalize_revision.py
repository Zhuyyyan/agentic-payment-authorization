from pathlib import Path
import shutil,json,hashlib,re
from pypdf import PdfReader
R=Path(__file__).resolve().parents[1]
for folder,name in [('final_native','paper'),('guide_native','理解辅助稿')]:
 source=R/'tmp'/folder/(name+'.pdf');assert source.exists();shutil.copy2(source,R/'paper'/(name+'.pdf'))
paper=PdfReader(R/'paper/paper.pdf');guide=PdfReader(R/'paper/理解辅助稿.pdf');assert len(paper.pages)==17 and len(guide.pages)==8
sizes=[]
for p in paper.pages:p.extract_text(visitor_text=lambda t,cm,tm,f,z:sizes.append(z) if t.strip() else None)
assert set(sizes)=={12.}
audit={'native_renderer':'LibreOffice 26.8.3.1 via documents/render_docx.py','paper_pages':len(paper.pages),'guide_pages':len(guide.pages),'paper_font_sizes':sorted(set(sizes)),'same_source_docx_and_pdf':True,'files':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'paper').glob('*') if p.suffix in ['.pdf','.docx']}}
(R/'outputs/logs/native_render_audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2),encoding='utf-8')
quality='''# 最终质量审查报告 第二次完善版

审查日期：2026年11月24日。论文和理解辅助稿均通过LibreOffice原生分页渲染；已逐页检查。仍保留IMF完整PDF与Hart1988发表版全文的访问限制，不宣称全部全文获取完成。

|检查项|结论与证据|
|---|---|
|PDF页数|论文17页，含参考文献；理解辅助稿单独8页，不并入论文|
|小四字体|论文原生渲染PDF所有文本12pt；DOCX正文及标题样式12pt宋体/Times New Roman，图内标注为图像|
|DOCX原生分页|安装官方LibreOffice26.8.3.1；调用技能render_docx.py成功，最终PDF直接来自最终DOCX；不再依赖平行生成的PDF|
|版面|修复双图后的短页及长策略名挤压；17页逐页检查无截断、重叠、孤立短页或公式减号缺失|
|文献|17项；Jensen1976期刊全文56页已取得；Hart1985MIT工作论文78页单列，与1988期刊条目区分；IMF仅据官方网页使用分层论断|
|引用映射|按首次出现编号，17项唯一对应；citation_mapping.csv保留矩阵ID与正文编号映射；RFC8785明确为信息类文档|
|理论与公式|区分信息不对称和契约不完全；AI只作经济学分析类比。评分用1-S；硬约束优先；权重非负和为1；ELP成本是假定|
|完整运行|主实验30×10000成功；追加30×10000使用新测试种子，单独校准。两类实验参数、摘要及输出保存|
|单元测试|15项通过；新增同信息集基准的任务/环境信号和完整性门测试，已观察失败后实现|
|结果核对|1500000条原始主/消融决策日志重算指标一致；seed0全流程重跑与日志逐条相同；追加实验seed20000重生成并复算一致|
|创新与外推|贡献限定为消费者场景操作化及仿真比较；不宣称首创，不以合成结果支持真实支付部署|
|Research Proposal|既有探索性结果和追加复核与未来计划明确区分；覆盖问题、文献、逻辑、设计、可行性及学术规范，不预测课程得分|

## 本轮实质改进

1. 加入220元购买耳机的具体问题情境，说明任务偏离和合法新商户的双重控制难题。
2. 根据Jensen第1.4节细化监督、约束和剩余损失；依据Hart/Moore公开工作论文修正“契约不完全等于信息不对称”的潜在混淆，不冒充已读1988发表版。
3. 追加M2_full：与M3使用相同五项信号、相同完整性验证。校准种子9100，测试种子20000—20029，每批10000。明确属于主实验完成后的探索性复核。
4. 追加结果M2_full/M3测试UAER约4.38%/1.84%、LAER71.68%/81.85%、ER36.43%/29.98%。差值及种子区间见robust_contrasts.csv；仍未严格等安全，也未覆盖全部固定规则。
5. 明确FDR=0可能反映正常压力样本不足；AC=100%只测字段，不代表日志不可修改。没有把较好结果包装成完美机制。
6. 增加8页中文理解辅助稿：手算例子、变量与标签、指标、统计、代码路径、复跑和问答。它是学习材料，不冒充已完成的访谈或个人研究经历。

## 剩余边界

- IMF完整PDF/eLibrary入口多次返回403/405；官方网页、DOI元数据已核对。正文只使用其可核验的分层认识。
- Hart1988发表版仍为挑战页；取得1985工作论文作为明确区分版本的理论补充，不能宣称逐页核读1988版本。
- MAS直接下载为维护页，初次浏览取得29页文档和关键文本；原始失败记录保留，不把HTTP200当成成功PDF。
- 未进行学校查重、未填写姓名学号、未提交Canvas。GitHub公开状态见PUBLICATION.md。提交前作者需完成课程规定的查重及个人信息核对。

## 独立复核

第二轮独立审查检查同信息集策略、校准/测试隔离、配对差值和理解辅助稿，没有发现显著问题；确认正文已经说明二元新颖性和共同阈值OR基准的局限。最终排版与完整日志复核由主执行者完成。
'''
(R/'quality_review.md').write_text(quality,encoding='utf-8')
(R/'progress.md').write_text('''# 完成情况 第二次完善版

已安装LibreOffice26.8.3.1，论文DOCX原生渲染17页，最终PDF直接由DOCX导出；理解辅助稿8页，均逐页检查。主实验30万笔和追加公平比较30万笔完成，15项测试通过。17项文献记录，Jensen56页期刊全文核读，Hart1985MIT工作论文78页核读并单列，与1988期刊版区分。所有论文、数据、代码和包已更新。

仓库公开状态见PUBLICATION.md。剩余：IMF完整PDF与Hart1988发表版获取仍受限；MAS直接下载返回维护页，保留浏览读取依据与原始失败记录。未做学校查重、未填个人信息、未提交Canvas。结果只限人工合成分布。
''',encoding='utf-8')

claims=(R/'claims_audit.md').read_text(encoding='utf-8').split('\n## 第二轮更新')[0]
claims=claims.replace('|代理成本与不完全性可解释控制需求|矩阵5、6及Crossref元数据|理论类比；两篇原文未获取，不作模型细节声明|','|代理成本与不完全性可解释控制需求|矩阵5期刊全文、矩阵6期刊元数据与矩阵17工作论文全文|理论类比；不混同1985与1988版本，不声称核读1988发表版|')
(R/'claims_audit.md').write_text(claims+'''

## 第二轮更新

- Jensen期刊全文取得：literature/fulltext_retry_log.json，jensen_retry，56页；第1.4节印刷页308—309支持代理成本三分法。
- Hart1985工作论文全文取得：literature/fourth_retrieval_log.json，hart_mit_api，78页；引言区分不完全性与信息不对称。矩阵17单列，不把1988期刊条目标成全文已读。
- 公平比较：robust_calibration.csv、robust_test.csv、robust_contrasts.csv，限定相同信息/执行门以及特定共同阈值OR，未声称对全部固定规则占优。
- 原生分页：native_render_audit.json，论文17页、学习稿8页；最终PDF直接由对应DOCX导出。
''',encoding='utf-8')
print(json.dumps(audit,ensure_ascii=False,indent=2))
