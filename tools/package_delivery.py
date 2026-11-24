from pathlib import Path
import zipfile,json,hashlib
R=Path(__file__).resolve().parents[1];out=R/'deliverables';out.mkdir(exist_ok=True)
paths=[p for p in R.rglob('*') if p.is_file() and not any(x in p.relative_to(R).parts for x in ['.git','tmp','__pycache__','deliverables','.venv']) and not p.is_relative_to(R/'literature/sources')]
manifest={str(p.relative_to(R)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
(out/'delivery_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
archive=out/'FinTech_Final_Research_delivery.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
 for p in paths:z.write(p,p.relative_to(R))
 z.write(out/'delivery_manifest.json','delivery_manifest.json')
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print(f'{archive}: {archive.stat().st_size/1024/1024:.1f} MB, {len(paths)} files')
