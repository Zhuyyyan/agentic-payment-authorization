import math
def features(t):
 return [min(t['amount']/t['limit'],1),t['novelty'],1-t['consistency'],t['velocity'],t['environment']]
def score(t,weights):
 if len(weights)!=5 or any(not math.isfinite(w) or w<0 for w in weights) or abs(sum(weights)-1)>1e-9:raise ValueError('Invalid weights')
 f=features(t)
 if any(not math.isfinite(x) or not 0<=x<=1 for x in f):raise ValueError('Invalid risk attributes')
 return sum(a*b for a,b in zip(f,weights))
