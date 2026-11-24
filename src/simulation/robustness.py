"""Post-pilot additional robustness, independently calibrated and held out."""
from pathlib import Path
import pandas as pd
import json,hashlib,time
from .generator import generate
from .experiments import evaluate
from .metrics import metrics,paired_ci
R=Path(__file__).resolve().parents[2]
GRID=[.15,.2,.25,.3,.35,.4,.45,.5,.55,.6,.65,.7,.75,.8,.85,.9,.95]
def kw(policy,t):return dict(fixed=[t]) if policy=='M2_full' else dict(thresholds=[t/2,t,.99])
def run():
 start=time.time();cal=[];batch=generate(9100,10000)
 for p in ['M2_full','M3']:
  for t in GRID:cal.append(dict(policy=p,threshold=t,**metrics(evaluate(batch,p,**kw(p,t)))))
 c=pd.DataFrame(cal);c.to_csv(R/'outputs/tables/robust_calibration.csv',index=False)
 selected={p:float(g[g.UAER<=.05].sort_values(['LAER','threshold']).iloc[-1].threshold) for p,g in c.groupby('policy')}
 rows=[];manifest=[]
 for seed in range(20000,20030):
  b=generate(seed,10000)
  manifest.append(dict(seed=seed,n=10000,synthetic=True,data_sha256=hashlib.sha256(json.dumps(b,sort_keys=True).encode()).hexdigest()))
  for p,t in selected.items():rows.append(dict(seed=seed,policy=p,threshold=t,**metrics(evaluate(b,p,**kw(p,t)))))
  print(f'Robustness seed {seed}',flush=True)
 df=pd.DataFrame(rows);df.to_csv(R/'outputs/tables/robust_test.csv',index=False)
 contrasts=[]
 for metric in ['UAER','LAER','ER','ELP']:
  a=df[df.policy=='M3'].set_index('seed')[metric]-df[df.policy=='M2_full'].set_index('seed')[metric];mean,lo,hi=paired_ci(a);contrasts.append(dict(metric=metric,mean=mean,lo=lo,hi=hi))
 pd.DataFrame(contrasts).to_csv(R/'outputs/tables/robust_contrasts.csv',index=False)
 pd.DataFrame(manifest).assign(calibration_seed=9100,elapsed_seconds=time.time()-start).to_csv(R/'outputs/tables/robust_manifest.csv',index=False)
 print(df.groupby('policy')[['threshold','UAER','LAER','ER','ELP']].mean().to_string())
if __name__=='__main__':run()
