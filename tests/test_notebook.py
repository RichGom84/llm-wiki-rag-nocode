"""Local widget wiring test. This is not a live Google Colab/API test."""
import unittest,sys,json,contextlib,io,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from test_workshop import FakeAI
@unittest.skipUnless(importlib.util.find_spec('ipywidgets'),'ipywidgets is only needed for the UI check')
class NotebookTests(unittest.TestCase):
    def test_buttons_complete_workflow_with_fake_ai(self):
        from unittest.mock import patch
        nb=json.loads((ROOT/'START_HERE.ipynb').read_text())
        ns={}
        with contextlib.redirect_stdout(io.StringIO()),patch('IPython.display.display',lambda *args,**kwargs:None):
            exec(''.join(nb['cells'][1]['source']),ns)
            ns['workshop'].client=FakeAI()
            exec(''.join(nb['cells'][3]['source']),ns)
            buttons={b.description:b for b in ns['buttons']}
            buttons['RAG 만들기 / 갱신'].click()
            buttons['검색 근거만 보기'].click()
            buttons['RAG에 질문하기'].click()
            buttons['Wiki 만들기 / 갱신'].click()
            buttons['Wiki에 질문하기'].click()
            self.assertEqual(len(ns['workshop'].pages),4)
            buttons['변경 공지 D11 추가'].click()
            self.assertEqual(ns['workshop'].dirty_pages(),['schedule.md'])
            buttons['RAG 만들기 / 갱신'].click()
            buttons['Wiki 만들기 / 갱신'].click()
            self.assertEqual(ns['workshop'].dirty_pages(),[])
            self.assertTrue(all(not b.disabled for b in ns['buttons']))
            self.assertEqual(len([r for r in ns['workshop'].history if r['mode'] in ['RAG','Wiki']]),2)
        import shutil
        shutil.rmtree(ns['workshop'].root)
