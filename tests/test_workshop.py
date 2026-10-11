import unittest,tempfile,sys,json,zipfile,hashlib,urllib.error
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from workshop import Workshop,WorkshopError,OpenAIClient,TOPICS,QUESTIONS,validate_wiki
class FakeAI:
    def __init__(self):self.fail=False;self.calls=[]
    def __call__(self,instructions,text,max_tokens):
        self.calls.append(text)
        if self.fail:raise WorkshopError('테스트용 중단')
        import re
        ids=sorted(set(re.findall(r'\bD\d{2}\b',text)))
        return {'text':'# 테스트용 모의 응답\n'+' '.join('['+i+']' for i in ids), 'usage':{'input_tokens':10,'output_tokens':5},'model':'test-fake'}
class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.ai=FakeAI()
        self.sources={p.stem:p.read_text() for p in (ROOT/'materials/raw').glob('D*.md')}
        self.update=(ROOT/'materials/updates/D11.md').read_text()
        self.w=Workshop(self.sources,self.update,self.tmp.name,self.ai)
    def tearDown(self):self.tmp.cleanup()
    def test_rebuild_and_update_invalidation(self):
        count=self.w.build_rag();self.assertEqual(count,self.w.build_rag())
        self.assertEqual(count,len(set(x['id'] for x in self.w.rag)))
        self.w.add_update()
        with self.assertRaises(WorkshopError):self.w.answer_rag(QUESTIONS[7])
        self.w.build_rag();hits=self.w.rag_evidence(QUESTIONS[7],5)
        self.assertIn('D11',[x['source'] for x in hits])
    def test_retrieval_includes_actual_grounding(self):
        self.w.build_rag()
        for q,sid in [(QUESTIONS[0],'D04'),(QUESTIONS[2],'D07'),(QUESTIONS[3],'D05')]:
            self.assertIn(sid,[x['source'] for x in self.w.rag_evidence(q,3)],q)
        self.assertTrue({'D01','D02'}.issubset({x['source'] for x in self.w.rag_evidence(QUESTIONS[4],3)}))
    def test_wiki_selective_update_and_links(self):
        self.assertEqual(len(self.w.build_wiki()),4)
        self.assertEqual(self.w.build_wiki(),[])
        old=dict(self.w.pages);self.w.add_update()
        self.assertEqual(self.w.dirty_pages(),['schedule.md'])
        with self.assertRaises(WorkshopError):self.w.answer_wiki(QUESTIONS[7])
        self.assertEqual(self.w.build_wiki(),['schedule.md'])
        self.assertEqual(old['courses.md'],self.w.pages['courses.md'])
        self.assertIn('D11',self.w.pages['schedule.md'])
        self.assertTrue(list((self.w.root/'wiki/versions').glob('*.md')))
        self.assertIn('schedule.md',(self.w.root/'wiki/index.md').read_text())
    def test_failure_preserves_published_wiki(self):
        self.w.build_wiki();old=dict(self.w.pages)
        self.w.add_update();self.ai.fail=True
        with self.assertRaises(WorkshopError):self.w.build_wiki()
        self.assertEqual(old,self.w.pages)
        self.assertNotIn('D11',(self.w.root/'wiki/schedule.md').read_text())
    def test_rejects_untrusted_paths_and_citations(self):
        for text in ['# no citation','[D99]','[D01] [bad](../../secret)','[D01] [bad](https://example.com)']:
            with self.assertRaises(WorkshopError):validate_wiki(text,self.sources)
    def test_no_key_in_exports(self):
        self.w.build_rag();self.w.build_wiki();self.w.answer_rag(QUESTIONS[0])
        self.w.client=OpenAIClient('never-export-this-test-key')
        path=self.w.export(self.w.root/'out.zip')
        with zipfile.ZipFile(path) as z:
            self.assertIn('wiki/index.md',z.namelist());self.assertIn('results.json',z.namelist())
            self.assertFalse(any('..' in n for n in z.namelist()))
            self.assertNotIn(b'never-export-this-test-key',b''.join(z.read(n) for n in z.namelist()))
    def test_http_request_and_output_parsing(self):
        import io
        response={'status':'completed','output':[{'type':'reasoning'},{'type':'message','content':[{'type':'output_text','text':'ok'}]}],'usage':{}}
        seen=[]
        def fake(req,timeout):seen.append(req);return io.BytesIO(json.dumps(response).encode())
        with patch('urllib.request.urlopen',fake):r=OpenAIClient('test-key')('rules','question')
        self.assertEqual(r['text'],'ok')
        payload=json.loads(seen[0].data);self.assertFalse(payload['store'])
        self.assertEqual(payload['model'],'gpt-4.1-mini')
    def test_notebook_sources_match_repo_and_outputs_empty(self):
        n=json.loads((ROOT/'START_HERE.ipynb').read_text())
        datahash=hashlib.sha256(json.dumps(self.sources,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
        self.assertEqual(n['metadata']['workshop_source_sha256'],datahash)
        for c in n['cells']:
            if c['cell_type']=='code':
                self.assertEqual(c['outputs'],[]);self.assertIsNone(c['execution_count'])
                compile(''.join(c['source']),'cell','exec')
if __name__=='__main__':unittest.main()
