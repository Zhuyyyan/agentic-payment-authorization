"""SYNTHETIC ONLY. Labels derive from latent task violation, not engine score."""
import random,itertools
def base():
 return dict(tx_id='t0',mandate_id='m0',agent='a0',authorized_agent='a0',amount=20000,limit=100000,currency='CNY',allowed_currency='CNY',operation='purchase',allowed_operations=['purchase','transfer'],payee='known',blocked_payees=['blocked'],payee_type='merchant',novelty=0.,consistency=1.,velocity=0.,environment=0.,now=100,expires=200,revoked=False,changed=False,legitimate=True,latent='normal',synthetic=True)
def generate(seed,n,noise=0.18,prevalence=0.2):
 rng=random.Random(seed);out=[]
 for i in range(n):
  x=base();bad=rng.random()<prevalence;latent=rng.choice(['diversion','burst','mismatch']) if bad else 'normal'
  x.update(tx_id=f'{seed}-{i}',mandate_id=f'm-{seed}-{i}',latent=latent,legitimate=not bad)
  centers={'normal':[.25,.12,.12,.2,.1],'diversion':[.45,.8,.55,.3,.5],'burst':[.55,.3,.35,.85,.4],'mismatch':[.4,.4,.85,.35,.4]}[latent]
  f=[min(1,max(0,rng.gauss(c,noise))) for c in centers]
  # Legitimate purchases may also be novel/high-value: overlap is intentional.
  if not bad and rng.random()<.15:f[rng.choice([0,1,3])]=rng.uniform(.7,1)
  x.update(amount=max(1,int(f[0]*100000)),novelty=float(rng.random()<f[1]),consistency=1-f[2],velocity=f[3],environment=f[4],payee_type=rng.choice(['merchant','individual']),operation=rng.choice(['purchase','transfer']))
  if rng.random()<.06:
   k,v=rng.choice([('revoked',True),('expires',90),('amount',100001),('currency','USD'),('payee','blocked'),('operation','invest')]);x[k]=v;x['legitimate']=False
  y=dict(x)
  if rng.random()<.06:
   y.update(payee='replacement',changed=True,legitimate=False)
  out.append((x,y))
 return out
def factorial():
 out=[]
 for i,vals in enumerate(itertools.product([.15,.85],repeat=5)):
  x=base();a,p,s,v,e=vals;x.update(tx_id=f'factor-{i}',amount=int(a*100000),novelty=p,consistency=1-s,velocity=v,environment=e,legitimate=False,latent='designed_probe');out.append((x,dict(x)))
 return out
