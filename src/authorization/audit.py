import hashlib,json,math
FIELDS=['tx_id','mandate_id','agent','decision','reason','risk','before_hash','after_hash','policy','executed','timestamp']
def digest(t):
 # Bind complete transaction and mandate snapshot. Trusted record is assumed.
 keys=['tx_id','mandate_id','agent','authorized_agent','amount','limit','currency','allowed_currency','operation','allowed_operations','payee','blocked_payees','expires','revoked','novelty','consistency','velocity','environment']
 payload={k:('INVALID:'+repr(t[k]) if isinstance(t[k],float) and not math.isfinite(t[k]) else t[k]) for k in keys}
 return hashlib.sha256(json.dumps(payload,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()
def complete(record):return int(all(k in record and record[k] is not None for k in FIELDS))
