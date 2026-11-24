from pathlib import Path
import json,csv,time,hashlib,itertools
from collections import defaultdict
import pandas as pd
from .generator import generate,factorial
from .metrics import metrics,paired_ci
from .sensitivity import WEIGHTS,THRESHOLDS
from ..authorization.runtime import execute
from ..authorization.policies import CONFIG
ROOT=Path(__file__).resolve().parents[2]
def evaluate(batch,policy,**kw):return [execute(x,y,policy,**kw) for x,y in batch]
def run(n=None,seeds=None):
 start=time.time();n=n or CONFIG['n'];seeds=seeds or CONFIG['seeds']
 for p in ['data/generated','outputs/tables','outputs/figures','outputs/logs']: (ROOT/p).mkdir(parents=True,exist_ok=True)
 rows=[];sweep=[];sens=[];groups=[];manifest=[]
 for seed in range(seeds):
  batch=generate(seed,n)
  path=ROOT/f'data/generated/seed_{seed:02}.jsonl'
  with path.open('w',encoding='utf-8') as f:
   for x,y in batch:f.write(json.dumps({'before':x,'after':y},ensure_ascii=False)+'\n')
  manifest.append(dict(seed=seed,n=n,data_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),synthetic=True,config_sha256=hashlib.sha256((ROOT/'config.json').read_bytes()).hexdigest()))
  for m in ['M1','M2','M3','M3_no_risk','M3_no_integrity']:
   rs=evaluate(batch,m);rows.append(dict(seed=seed,policy=m,**metrics(rs)))
   with (ROOT/f'outputs/logs/{m}_{seed:02}.jsonl').open('w') as f:
    for r in rs:f.write(json.dumps(r)+'\n')
   for g in ['single','multiple']:
    selected=[r for r,(x,y) in zip(rs,batch) if sum(z>=.6 for z in [x['amount']/x['limit'],x['novelty'],1-x['consistency'],x['velocity'],x['environment']])==(1 if g=='single' else -1)] if g=='single' else [r for r,(x,y) in zip(rs,batch) if sum(z>=.6 for z in [x['amount']/x['limit'],x['novelty'],1-x['consistency'],x['velocity'],x['environment']])>=2]
    if selected:groups.append(dict(seed=seed,policy=m,group=g,**metrics(selected)))
  for t in THRESHOLDS:
   for m,kw in [('M3',dict(thresholds=[t/2,t,.95])),('M2',dict(fixed=[t,1,t]))]:
    sweep.append(dict(seed=seed,policy=m,threshold=t,**metrics(evaluate(batch,m,**kw))))
  for name,w in WEIGHTS.items():sens.append(dict(seed=seed,weights=name,**metrics(evaluate(batch,'M3',weights=w))))
  print(f'Completed seed {seed}',flush=True)
 df=pd.DataFrame(rows);df.to_csv(ROOT/'outputs/tables/per_seed.csv',index=False)
 pd.DataFrame(sweep).to_csv(ROOT/'outputs/tables/thresholds.csv',index=False);pd.DataFrame(sens).to_csv(ROOT/'outputs/tables/weights.csv',index=False);pd.DataFrame(groups).to_csv(ROOT/'outputs/tables/groups.csv',index=False)
 summary=[];contrasts=[]
 for m,g in df.groupby('policy'):
  for metric in ['UAER','LAER','FDR','ER','ELP','AC','OBS']:
   mean,lo,hi=paired_ci(g[metric],b=CONFIG['bootstrap']);summary.append(dict(policy=m,metric=metric,mean=mean,lo=lo,hi=hi))
 for ref in ['M1','M2','M3_no_risk','M3_no_integrity']:
  for metric in ['UAER','LAER','ER','ELP']:
   a=df[df.policy=='M3'].set_index('seed')[metric]-df[df.policy==ref].set_index('seed')[metric];mean,lo,hi=paired_ci(a,b=CONFIG['bootstrap']);contrasts.append(dict(contrast='M3 - '+ref,metric=metric,mean=mean,lo=lo,hi=hi))
 pd.DataFrame(summary).to_csv(ROOT/'outputs/tables/summary.csv',index=False);pd.DataFrame(contrasts).to_csv(ROOT/'outputs/tables/paired_contrasts.csv',index=False)
 probes=[]
 for i,(x,y) in enumerate(factorial()):
  for m in ['M1','M2','M3']:probes.append(dict(case=i,**execute(x,y,m)))
 pd.DataFrame(probes).to_csv(ROOT/'outputs/tables/factorial.csv',index=False)
 # Independent calibration seeds: choose highest-LAER point satisfying 5% UAER.
 cal=[]
 for t in THRESHOLDS:
  batch=generate(9000,10000)
  for m,kw in [('M3',dict(thresholds=[t/2,t,.95])),('M2',dict(fixed=[t,1,t]))]:cal.append(dict(policy=m,threshold=t,**metrics(evaluate(batch,m,**kw))))
 c=pd.DataFrame(cal);c.to_csv(ROOT/'outputs/tables/calibration.csv',index=False)
 chosen=[]
 for m,g in c.groupby('policy'):
  eligible=g[g.UAER<=.05]
  if len(eligible):
   t=eligible.sort_values('LAER').iloc[-1]['threshold'];test=pd.DataFrame(sweep);chosen.append(dict(policy=m,threshold=t,**test[(test.policy==m)&(test.threshold==t)].mean(numeric_only=True).drop(['seed','threshold']).to_dict()))
 pd.DataFrame(chosen).to_csv(ROOT/'outputs/tables/matched_safety.csv',index=False)
 if len(chosen)==2:
  sw=pd.DataFrame(sweep);sel={r['policy']:r['threshold'] for r in chosen};matched=[]
  for metric in ['UAER','LAER','ER']:
   a=sw[(sw.policy=='M3')&(sw.threshold==sel['M3'])].set_index('seed')[metric]-sw[(sw.policy=='M2')&(sw.threshold==sel['M2'])].set_index('seed')[metric]
   mean,lo,hi=paired_ci(a);matched.append(dict(metric=metric,mean=mean,lo=lo,hi=hi))
  pd.DataFrame(matched).to_csv(ROOT/'outputs/tables/h2_contrasts.csv',index=False)
 gr=pd.DataFrame(groups).pivot(index='seed',columns=['policy','group'],values='UAER')
 effect=(gr[('M3','multiple')]-gr[('M2','multiple')])-(gr[('M3','single')]-gr[('M2','single')])
 mean,lo,hi=paired_ci(effect)
 pd.DataFrame([dict(contrast='(M3-M2)_multiple - (M3-M2)_single',mean=mean,lo=lo,hi=hi)]).to_csv(ROOT/'outputs/tables/h3_contrast.csv',index=False)
 # DGP sensitivity changes noise and prevalence, never refits policy.
 dgp=[]
 for noise,prev in itertools.product([.12,.3],[.1,.35]):
  for seed in range(5):
   batch=generate(10000+seed,2000,noise,prev)
   for m in ['M1','M2','M3']:dgp.append(dict(noise=noise,prevalence=prev,seed=seed,policy=m,**metrics(evaluate(batch,m))))
 pd.DataFrame(dgp).to_csv(ROOT/'outputs/tables/dgp_sensitivity.csv',index=False)
 pd.DataFrame(manifest).assign(elapsed_seconds=time.time()-start).to_csv(ROOT/'experiment_manifest.csv',index=False)
 print(df.groupby('policy')[['UAER','LAER','ER','FDR','ELP']].mean().to_string())
