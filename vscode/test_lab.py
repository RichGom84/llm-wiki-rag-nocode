import tempfile, unittest, zipfile, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lab import Lab, TOPICS

class Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.lab=Lab(Path(self.temp.name)/'output')
        self.lab.prepare()
    def tearDown(self):
        self.temp.cleanup()
    def pages(self, names):
        for name in names:
            raw=self.lab.topic_sources(name)
            text='# '+TOPICS[name][0]+'\n\n'+'\n'.join(f'내용 확인 [{s}]\n- [{s}](../raw/{s}.md)' for s in raw)
            self.lab.write('wiki/'+name,text)
    def test_rag_grounding_and_update_guard(self):
        self.lab.rag_index()
        p=self.lab.context('rag','Python 기초반 개강일은 언제인가요?',3,'q1')
        self.assertIn('D04',p.read_text())
        self.lab.add_update()
        with self.assertRaises(ValueError): self.lab.context('rag','일정',3,'q1-after')
        self.lab.rag_index()
        p=self.lab.context('rag','변경 공지 이후 RAG 실습반 최종 개강일은 언제인가요?',3,'q8-after')
        self.assertIn('D11',p.read_text())
    def test_wiki_selective_update_and_archive(self):
        self.assertEqual(len(self.lab.wiki_packets()),4)
        self.pages(TOPICS)
        self.lab.wiki_register()
        self.assertEqual(self.lab.dirty(),[])
        self.lab.add_update()
        self.assertEqual(self.lab.wiki_packets(),['schedule.md'])
        self.pages(['schedule.md'])
        self.assertEqual(self.lab.wiki_register(),['schedule.md'])
        self.assertEqual(len(list((self.lab.root/'wiki/versions').glob('*.md'))),1)
        self.lab.context('wiki','일정이 겹치나요?',2,'wiki-after')
    def test_prepare_preserves_work_and_export_allowlist(self):
        self.lab.write('answers/mine.md','보관할 답변')
        self.lab.write('.env','DO_NOT_EXPORT_TEST')
        self.lab.prepare()
        self.assertTrue((self.lab.root/'answers/mine.md').exists())
        p=self.lab.export(Path(self.temp.name)/'out.zip')
        with zipfile.ZipFile(p) as z:
            self.assertNotIn('.env',z.namelist())
            self.assertIn('answers/mine.md',z.namelist())
    def test_path_and_source_validation(self):
        self.lab.rag_index()
        with self.assertRaises(ValueError): self.lab.context('rag','일정',3,'../../escape')
        self.pages(TOPICS)
        self.lab.write('wiki/schedule.md','허구 [D99]')
        with self.assertRaises(Exception): self.lab.wiki_register()
        self.assertFalse((self.lab.root/'wiki_state.json').exists())

if __name__=='__main__': unittest.main()
