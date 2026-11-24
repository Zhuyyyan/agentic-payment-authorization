"""Second retrieval pass: public original papers; validate actual PDF content."""
from pathlib import Path
import urllib.request,json,hashlib,concurrent.futures,re
from pypdf import PdfReader
from io import BytesIO
R=Path(__file__).resolve().parents[1];D=R/'literature/sources';D.mkdir(exist_ok=True)
URLS={
'jensen_retry':'https://www.liuyanecon.com/wp-content/uploads/JensenMeckling-1976.pdf',
'hart_author':'https://hart.scholars.harvard.edu/publications/incomplete-contracts-and-renegotiation',
'hart_mit':'https://dspace.mit.edu/entities/publication/f5d14137-5200-4cd3-b9e3-7681a96844e8',
'imf_full':'https://www.elibrary.imf.org/downloadpdf/view/journals/068/2026/004/article-A001-en.pdf',
'imf_xml':'https://www.elibrary.imf.org/view/journals/068/2026/004/article-A001-en.xml',
'imf_pdf':'https://www.imf.org/-/media/files/publications/imf-notes/2026/english/insea2026004.pdf',
'mas_retry':'https://www.mas.gov.sg/-/media/mas-media-library/development/fintech/ai-safr/safr-v1-1.pdf?download=1',
}
def get(kv):
 k,u=kv
 try:
  req=urllib.request.Request(u,headers={'User-Agent':'Mozilla/5.0','Accept':'application/pdf,text/html;q=0.9,*/*;q=0.8'})
  response=urllib.request.urlopen(req,timeout=35);b=response.read();pdf=b.startswith(b'%PDF');ext='.pdf' if pdf else '.html';(D/(k+ext)).write_bytes(b)
  t='\n'.join(p.extract_text() or '' for p in PdfReader(BytesIO(b)).pages) if pdf else b.decode('utf-8',errors='replace')
  (D/(k+'_extracted.txt')).write_text(t,encoding='utf-8')
  links=re.findall(r'(?:href|src)=[\"\x27]([^\"\x27]+)',t)
  return dict(id=k,url=u,final_url=response.url,status='pdf_verified' if pdf else 'html_requires_review',sha256=hashlib.sha256(b).hexdigest(),chars=len(t),pages=len(PdfReader(BytesIO(b)).pages) if pdf else None,title=t[:700] if pdf else re.findall(r'<title[^>]*>(.*?)</title>',t,re.S),links=[l for l in links if any(s in l.lower() for s in ['pdf','download','bitstream','file'])][:30])
 except Exception as e:return dict(id=k,url=u,status='failed',error=str(e))
if __name__=='__main__':
 with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:r=list(pool.map(get,URLS.items()))
 (R/'literature/fulltext_retry_log.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(r,ensure_ascii=False,indent=2))
