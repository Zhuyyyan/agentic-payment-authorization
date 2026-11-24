from pathlib import Path
import json
from .mandate import hard_check
from .risk import score,features
CONFIG=json.loads((Path(__file__).resolve().parents[2]/'config.json').read_text())
def decide(t,policy,weights=None,thresholds=None,fixed=None):
 if policy not in ['M1','M2','M3','M3_no_risk','M3_no_integrity','M2_full']:raise ValueError(policy)
 reason=hard_check(t)
 if reason:return dict(decision='DENY',reason=reason,risk=0.)
 if policy in ['M1','M3_no_risk']:return dict(decision='AUTO_EXECUTE',reason='mandate_ok',risk=0.)
 r=score(t,weights or CONFIG['weights'])
 if policy=='M2_full':
  cutoff=(fixed or [.7])[0]
  if not 0<cutoff<=1:raise ValueError('invalid fixed threshold')
  hit=max(features(t))>=cutoff
  return dict(decision='ESCALATE' if hit else 'AUTO_EXECUTE',reason='fixed5_trigger' if hit else 'fixed5_ok',risk=r)
 if policy=='M2':
  a,p,v=fixed or CONFIG['fixed'];hit=t['amount']/t['limit']>=a or t['novelty']>=p or t['velocity']>=v
  return dict(decision='ESCALATE' if hit else 'AUTO_EXECUTE',reason='fixed_trigger' if hit else 'fixed_ok',risk=r)
 lo,mid,hi=thresholds or CONFIG['thresholds']
 if not 0<=lo<mid<hi<=1:raise ValueError('unordered thresholds')
 d='AUTO_EXECUTE' if r<lo else 'OBSERVE' if r<mid else 'ESCALATE' if r<hi else 'DENY'
 return dict(decision=d,reason='risk_band',risk=r)
