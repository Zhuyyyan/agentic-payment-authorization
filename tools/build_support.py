from pathlib import Path
import json,hashlib,datetime
import pandas as pd
R=Path(__file__).resolve().parents[1]
pages=json.loads((R/'paper/paper_content.json').read_text(encoding='utf-8'))
for file,indices in {'research_questions.md':[1],'hypotheses.md':[4],'theoretical_framework.md':[3],'experimental_design.md':[7,8,12]}.items():
 text=[]
 for i in indices:
  title,blocks=pages[i];text.append('# '+title)
  for b in blocks:
   if isinstance(b,str):text.append(b)
 (R/'research'/file).write_text('\n\n'.join(text),encoding='utf-8')
man=pd.read_csv(R/'experiment_manifest.csv')
man['run_date_beijing']='2026-11-24';man['data_generator']='src/simulation/generator.py';man['weights']='0.20|0.20|0.25|0.20|0.15';man['thresholds']='0.25|0.45|0.70';man['dgp_noise']=.18;man['dgp_latent_violation']=.2
sourcehash=hashlib.sha256(''.join(hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted((R/'src').rglob('*.py'))).encode()).hexdigest();man['source_tree_sha256']=sourcehash;man.to_csv(R/'experiment_manifest.csv',index=False)
