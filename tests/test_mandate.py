import unittest
from src.authorization.mandate import hard_check
from src.simulation.generator import base

class MandateTests(unittest.TestCase):
 def test_hard_constraints(self):
  for k,v in [('revoked',True),('expires',99),('operation','invest'),('amount',100001),('currency','USD'),('payee','blocked'),('amount',-1),('amount',float('nan')),('agent','other')]:
   x=base(); x[k]=v
   self.assertIsNotNone(hard_check(x),k)
 def test_exact_cap_allowed(self):
  x=base();x['amount']=x['limit'];self.assertIsNone(hard_check(x))
