import unittest
from src.simulation.generator import base
from src.authorization.runtime import execute
class RuntimeTests(unittest.TestCase):
 def test_matched_baseline_has_same_integrity(self):
  x=base();self.assertFalse(execute(x,dict(x,payee='replacement'),'M2_full',fixed=[.7])['executed'])
 def test_nan_auditable_denial(self):
  x=base();x['amount']=float('nan');self.assertEqual(execute(x,x,'M3')['decision'],'DENY')
 def test_context_change_denial(self):
  x=base();self.assertFalse(execute(x,dict(x,environment=1),'M3')['executed'])
 def test_payee_substitution(self):
  x=base();y=dict(x,payee='replacement')
  self.assertFalse(execute(x,y,'M3')['executed'])
  self.assertTrue(execute(x,y,'M3_no_integrity')['executed'])
 def test_late_revocation_all(self):
  for m in ['M1','M2','M3']:
   x=base();self.assertFalse(execute(x,dict(x,revoked=True),m)['executed'])
 def test_audit_fields(self):
  r=execute(base(),base(),'M3');self.assertTrue(all(r[k] is not None for k in ['tx_id','mandate_id','agent','decision','reason','risk','before_hash','after_hash','policy','executed','timestamp']))
