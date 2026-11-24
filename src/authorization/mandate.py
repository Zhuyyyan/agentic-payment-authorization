"""Amounts are integer cents; limits are per-transaction, not aggregate budgets."""
import math
def hard_check(t):
 for k in ['amount','limit','now','expires']:
  if not isinstance(t.get(k),(int,float)) or not math.isfinite(t[k]):return 'invalid_numeric'
 if t['amount']<=0 or t['limit']<=0:return 'invalid_amount'
 if t['agent']!=t['authorized_agent']:return 'agent_mismatch'
 if t['revoked']:return 'revoked'
 if t['now']>=t['expires']:return 'expired'
 if t['operation'] not in t['allowed_operations']:return 'operation'
 if t['amount']>t['limit']:return 'amount_cap'
 if t['currency']!=t['allowed_currency']:return 'currency'
 if t['payee'] in t['blocked_payees']:return 'blocked_payee'
 return None
