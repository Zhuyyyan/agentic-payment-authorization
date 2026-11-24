import unittest
from src.authorization.policies import decide
from src.authorization.risk import score
from src.simulation.generator import base
class PolicyTests(unittest.TestCase):
 def test_same_information_baseline_sees_task_and_environment(self):
  x=base();x['consistency']=.1
  self.assertEqual(decide(x,'M2_full',fixed=[.7])['decision'],'ESCALATE')
  x=base();x['environment']=.9
  self.assertEqual(decide(x,'M2_full',fixed=[.7])['decision'],'ESCALATE')
 def test_score_orientation(self):
  x=base();x.update(amount=100000,novelty=1,consistency=0,velocity=1,environment=1)
  self.assertAlmostEqual(score(x,[.2]*5),1)
 def test_hard_deny_all(self):
  for m in ['M1','M2','M3','M3_no_risk','M3_no_integrity']:
   x=base();x['revoked']=True;self.assertEqual(decide(x,m)['decision'],'DENY')
 def test_four_states(self):
  x=base();x['amount']=10000
  self.assertEqual(decide(x,'M3')['decision'],'AUTO_EXECUTE')
  for a,b in [(.3,'OBSERVE'),(.5,'ESCALATE'),(.8,'DENY')]:
   x.update(amount=int(a*100000),novelty=a,consistency=1-a,velocity=a,environment=a)
   self.assertEqual(decide(x,'M3')['decision'],b)
