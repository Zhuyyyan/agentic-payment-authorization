import unittest
from src.simulation.generator import generate
from src.authorization.runtime import execute
from src.simulation.metrics import metrics
class Invariants(unittest.TestCase):
 def test_reproducibility_and_pairing(self):
  self.assertEqual(generate(4,10),generate(4,10))
 def test_escalation_never_execution(self):
  for x,y in generate(5,200):
   r=execute(x,y,'M3')
   if r['decision'] in ['DENY','ESCALATE']:self.assertFalse(r['executed'])
 def test_denominators(self):
  r=[dict(legitimate=False,executed=True,decision='AUTO_EXECUTE',amount=100,audit_complete=1),dict(legitimate=True,executed=False,decision='ESCALATE',amount=100,audit_complete=1)]
  z=metrics(r);self.assertEqual(z['UAER'],1);self.assertEqual(z['LAER'],0);self.assertEqual(z['ER'],.5)
