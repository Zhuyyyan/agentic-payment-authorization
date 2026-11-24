from .policies import decide
from .mandate import hard_check
from .audit import digest,complete
def execute(before,after,policy,**kwargs):
 r=decide(before,policy,**kwargs)
 # All mechanisms enforce immutable hard constraints again at execution.
 late=hard_check(after)
 if late:r.update(decision='DENY',reason='runtime_'+late)
 h1,h2=digest(before),digest(after)
 if policy in ['M3','M3_no_risk','M2_full'] and h1!=h2:r.update(decision='DENY',reason='integrity_mismatch')
 r.update(tx_id=before['tx_id'],mandate_id=before['mandate_id'],agent=before['agent'],before_hash=h1,after_hash=h2,policy=policy,timestamp=after['now'],executed=r['decision'] in ['AUTO_EXECUTE','OBSERVE'],amount=after['amount'],legitimate=after['legitimate'])
 r['audit_complete']=complete(r)
 return r
