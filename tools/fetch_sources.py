"""Download public primary sources only; retain failures without inventing evidence."""
from pathlib import Path
import urllib.request, json, hashlib, concurrent.futures
from pypdf import PdfReader
from io import BytesIO
ROOT=Path(__file__).resolve().parents[1]
SOURCES={
'imf':'https://www.imf.org/-/media/files/publications/imf-notes/2026/english/insea2026004.pdf',
'safr':'https://www.mas.gov.sg/-/media/mas-media-library/development/fintech/ai-safr/safr-v1-1.pdf',
'south':'https://raw.githubusercontent.com/mlresearch/v267/main/assets/south25a/south25a.pdf',
'nccoe':'https://www.nccoe.nist.gov/sites/default/files/2026-02/accelerating-the-adoption-of-software-and-ai-agent-identity-and-authorization-concept-paper.pdf',
'abac':'https://nvlpubs.nist.gov/nistpubs/specialpublications/NIST.sp.800-162.pdf',
'zero':'https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf',
'rmf':'https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf',
'genai':'https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf',
'jensen':'https://www.sfu.ca/~wainwrig/Econ400/jensen-meckling.pdf',
'hart':'https://doi.org/10.2307/1912698',
**{f'rfc{n}':f'https://www.rfc-editor.org/rfc/rfc{n}.txt' for n in [8693,9396,9449,9700,8785,9421]},
'agentdojo':'https://arxiv.org/pdf/2406.13352',
}
def fetch(kv):
 k,u=kv; folder=ROOT/'literature/sources';folder.mkdir(parents=True,exist_ok=True)
 try:
  b=urllib.request.urlopen(urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0'}),timeout=40).read()
  pdf=b.startswith(b'%PDF'); (folder/(k+('.pdf' if pdf else '.txt'))).write_bytes(b)
  t='\n'.join(p.extract_text() or '' for p in PdfReader(BytesIO(b)).pages) if pdf else b.decode('utf-8',errors='replace')
  (folder/(k+'_extracted.txt')).write_text(t,encoding='utf-8')
  return {'id':k,'url':u,'status':'retrieved','sha256':hashlib.sha256(b).hexdigest(),'chars':len(t)}
 except Exception as e:return {'id':k,'url':u,'status':'failed','error':str(e)}
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: results=list(pool.map(fetch,SOURCES.items()))
 (ROOT/'literature/retrieval_log.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(results,ensure_ascii=False,indent=2))
