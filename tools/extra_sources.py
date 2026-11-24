from fetch_sources import fetch,ROOT
import concurrent.futures,json
urls={
'imf_page':'https://www.imf.org/en/Publications/imf-notes/Issues/2026/04/22/how-agentic-ai-will-reshape-payments-575560',
'imf_elibrary':'https://www.elibrary.imf.org/view/journals/068/2026/004/article-A001-en.xml',
'jensen_harvard':'https://www.hbs.edu/ris/Publication%20Files/76-024_0ab8dd2b-45e0-4c75-b4de-9b4c44b6d9de.pdf',
'jensen_metadata':'https://api.crossref.org/works/10.1016/0304-405X(76)90026-X',
'hart_metadata':'https://api.crossref.org/works/10.2307/1912698',
'safr_page':'https://www.mas.gov.sg/development/fintech/safeguards-for-agentic-finance-at-runtime',
'agentdojo_pmlr':'https://proceedings.neurips.cc/paper_files/paper/2024/hash/0339b18e93b4d1d9a8cbdf863920af5e-Abstract-Datasets_and_Benchmarks_Track.html',
}
with concurrent.futures.ThreadPoolExecutor(max_workers=5) as p:r=list(p.map(fetch,urls.items()))
(ROOT/'literature/extra_retrieval_log.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(r,indent=2))
