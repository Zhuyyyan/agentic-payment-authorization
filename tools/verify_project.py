"""Validate artifacts, source retrieval classification and numerical lineage."""
from pathlib import Path
import json,hashlib,sys,platform,subprocess,re,zipfile
import pandas as pd
import numpy as np
from pypdf import PdfReader
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.simulation.metrics import metrics
from src.simulation.generator import generate,base
from src.authorization.runtime import execute
from src.simulation.robustness import kw
R=Path(__file__).resolve().parents[1]
for name in ['retrieval_log.json','extra_retrieval_log.json']:
 p=R/'literature'/name
 if not p.exists():continue  # Retrieval diagnostics are intentionally local-only.
 rs=json.loads(p.read_text(encoding='utf-8'))
 for r in rs:
  if r['id'] in ['safr','safr_page','hart']:
   r['transport_status']=r['status'];r['status']='content_verification_failed';r['note']='Maintenance HTML or client challenge, not the requested original'
 p.write_text(json.dumps(rs,ensure_ascii=False,indent=2),encoding='utf-8')
manifest=pd.read_csv(R/'experiment_manifest.csv');assert len(manifest)==30
per=pd.read_csv(R/'outputs/tables/per_seed.csv');checked=0;tamper=[]
for _,m in manifest.iterrows():
 seed=int(m.seed);path=R/f'data/generated/seed_{seed:02}.jsonl'
 assert hashlib.sha256(path.read_bytes()).hexdigest()==m.data_sha256
 dataset=[json.loads(line) for line in path.open(encoding='utf-8')];changed={r['after']['tx_id'] for r in dataset if r['after']['changed']}
 if seed==0:
  regenerated=generate(seed,10000);assert all(a==b['before'] and z==b['after'] for (a,z),b in zip(regenerated,dataset))
 for policy in ['M1','M2','M3','M3_no_risk','M3_no_integrity']:
  records=[json.loads(line) for line in (R/f'outputs/logs/{policy}_{seed:02}.jsonl').open()]
  calc=metrics(records);stored=per[(per.seed==seed)&(per.policy==policy)].iloc[0]
  for k,v in calc.items():assert abs(v-stored[k])<1e-9,(seed,policy,k)
  if seed==0:
   rerun=[execute(b['before'],b['after'],policy) for b in dataset];assert rerun==records
  sub=[r for r in records if r['tx_id'] in changed];tamper.append(dict(seed=seed,policy=policy,n=len(sub),executed=sum(r['executed'] for r in sub),rate=sum(r['executed'] for r in sub)/len(sub)))
  checked+=len(records)
pd.DataFrame(tamper).to_csv(R/'outputs/tables/tamper_subset.csv',index=False)
# Fixed edge cases saved as inspectable results, not independent inferential data.
cases=[]
for k,v in [('revoked',True),('expires',100),('amount',100001),('currency','USD'),('payee','blocked'),('operation','invest')]:
 for policy in ['M1','M2','M3']:
  x=base();x[k]=v;cases.append(dict(case=k,**execute(x,x,policy)));assert cases[-1]['decision']=='DENY'
pd.DataFrame(cases).to_csv(R/'outputs/tables/boundary_cases.csv',index=False)
pdf=PdfReader(R/'paper/paper.pdf');assert len(pdf.pages)<=20
sizes=[]
for page in pdf.pages:
 page.extract_text(visitor_text=lambda text,cm,tm,font,size:sizes.append(size) if text.strip() else None)
assert set(sizes)=={12.0},set(sizes)
mapping=pd.read_csv(R/'literature/citation_mapping.csv');assert len(mapping)==17 and len(set(mapping.literature_matrix_id))==17
text=(R/'paper/paper.md').read_text(encoding='utf-8');assert '\ufffd' not in text
with zipfile.ZipFile(R/'paper/paper.docx') as z:
 xml=z.read('word/styles.xml').decode();assert 'w:sz w:val="24"' in xml
rob=pd.read_csv(R/'outputs/tables/robust_test.csv');rman=pd.read_csv(R/'outputs/tables/robust_manifest.csv')
assert len(rman)==30 and len(rob)==60
first=generate(20000,10000)
assert hashlib.sha256(json.dumps(first,sort_keys=True).encode()).hexdigest()==rman.iloc[0].data_sha256
for _,row in rob[rob.seed==20000].iterrows():
 calc=metrics([execute(a,b,row.policy,**kw(row.policy,row.threshold)) for a,b in first])
 for k,v in calc.items():assert abs(v-row[k])<1e-9,(row.policy,k)
env={'python':sys.version,'platform':platform.platform(),'numpy':np.__version__,'pandas':pd.__version__,'checked_decision_records':checked,'pdf_pages':len(pdf.pages),'pdf_text_font_sizes':sorted(set(sizes))}
codehash={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in (R/'src').rglob('*.py')}
(R/'outputs/logs/verification.json').write_text(json.dumps(dict(environment=env,source_hashes=codehash),ensure_ascii=False,indent=2),encoding='utf-8')
(R/'requirements-lock.txt').write_text('\n'.join(f'{n}=={__import__(n).__version__}' for n in ['numpy','pandas','docx','PIL','pypdf','reportlab']).replace('docx==','python-docx==').replace('PIL==','Pillow==')+'\n',encoding='utf-8')
print(json.dumps(env,ensure_ascii=False,indent=2))
