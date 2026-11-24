"""Use installed LibreOffice, explicitly authorized by the user, via skill renderer."""
import os,sys,tempfile,runpy
from pathlib import Path
R=Path(__file__).resolve().parents[1]
office=Path('C:/Program Files/LibreOffice/program/soffice.exe')
assert office.exists(),'Install official LibreOffice first'
os.environ['PATH']=str(office.parent)+os.pathsep+os.environ['PATH']
tasktmp=R/'tmp/native_renderer';tasktmp.mkdir(parents=True,exist_ok=True)
tempfile.tempdir=str(tasktmp)
Original=tempfile.TemporaryDirectory
class QuietCleanup(Original):
 def __init__(self,*args,**kwargs):
  kwargs['ignore_cleanup_errors']=True
  super().__init__(*args,**kwargs)
tempfile.TemporaryDirectory=QuietCleanup
configured=os.environ.get('CODEX_DOCX_RENDERER')
candidates=list((Path.home()/'.codex/plugins/cache/openai-primary-runtime/documents').glob('*/skills/documents/render_docx.py'))
renderer=Path(configured) if configured else (sorted(candidates)[-1] if candidates else None)
if renderer is None or not renderer.is_file():
 raise SystemExit('Set CODEX_DOCX_RENDERER to the installed documents skill renderer, or export the DOCX using LibreOffice.')
sys.argv=[str(renderer),*sys.argv[1:]]
runpy.run_path(str(renderer),run_name='__main__')
