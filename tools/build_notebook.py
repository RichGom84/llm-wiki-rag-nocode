"""Instructor-only build: regenerate the self-contained notebook after source edits."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def cell(kind,text,**metadata):
    c={'cell_type':kind,'metadata':metadata,'source':text.splitlines(keepends=True)}
    if kind=='code':c.update(execution_count=None,outputs=[])
    return c
sources={p.stem:p.read_text(encoding='utf-8') for p in sorted((ROOT/'materials/raw').glob('D*.md'))}
update=(ROOT/'materials/updates/D11.md').read_text(encoding='utf-8')
fingerprint=hashlib.sha256(json.dumps(sources,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
core=(ROOT/'src/workshop.py').read_text(encoding='utf-8')
ui=(ROOT/'src/notebook_ui.py').read_text(encoding='utf-8')
intro='''# 코딩 없이 만드는 RAG와 LLM Wiki
수강생은 코드를 수정하지 않습니다. 아래 실행 버튼 세 개를 위에서부터 누른 뒤, 실습 화면의 버튼을 사용하세요.

- Google 계정과 사용 가능한 OpenAI API 키가 필요합니다. API 사용에는 별도 비용이 발생할 수 있습니다.
- API 키는 2단계의 비밀번호 입력란에만 넣습니다. 코드·질문·GitHub에는 적지 않습니다.
- RAG는 키워드 기반 BM25 검색을 사용합니다. Wiki는 AI가 주제별 Markdown 문서를 작성하고 저장합니다.
- 개인 실습 런타임을 사용하며 웹 서버나 외부 공개 링크를 생성하지 않습니다.
- 결과는 종료 전에 ZIP으로 다운로드하세요. Colab 연결이 끊기면 작업 파일이 사라질 수 있습니다.
- 이 노트북은 함께 배포된 원문을 내장합니다. GitHub 원문 파일을 수정해도 자동으로 바뀌지 않습니다.
'''
setup='#@title 1단계 실습 준비  왼쪽 실행 버튼을 누르세요\n'+core+'\nSAMPLE_SOURCES = '+repr(sources)+'\nSAMPLE_UPDATE = '+repr(update)+'''
import tempfile
workshop=Workshop(SAMPLE_SOURCES,SAMPLE_UPDATE,Path(tempfile.mkdtemp(prefix='wiki-rag-')))
print('준비 완료: 기본 원문 10개. 다음 2단계를 실행하세요.')
'''
connect='''#@title 2단계 AI 연결  키는 비밀번호 입력란에만 넣으세요
from getpass import getpass
_api_key=getpass('OpenAI API 키 입력 (코드에 붙여넣지 마세요): ')
workshop.client=OpenAIClient(_api_key,MODEL)
del _api_key
print('키를 메모리에 연결했습니다. 아직 API 호출은 하지 않았습니다. 다음 3단계를 실행하세요.')
'''
notebook={'nbformat':4,'nbformat_minor':5,'metadata':{'colab':{'name':'START_HERE.ipynb','provenance':[]},'kernelspec':{'display_name':'Python 3','name':'python3'},'language_info':{'name':'python'},'workshop_source_sha256':fingerprint},'cells':[
 cell('markdown',intro),cell('code',setup,cellView='form'),cell('code',connect,cellView='form'),
 cell('code','#@title 3단계 실습 화면 열기\n'+ui,cellView='form'),
 cell('markdown','''## 종료 전 확인
1. 질문 기록과 Wiki 문서를 확인합니다.
2. **결과 ZIP 다운로드**를 누르고 컴퓨터에 저장됐는지 확인합니다.
3. 제출할 때 노트북 대신 결과 ZIP을 사용합니다.
4. 다시 시작하려면 런타임을 종료하고 1단계부터 실행합니다. API 키는 다시 입력해야 합니다.
''')]}
for i,c in enumerate(notebook['cells']):c['id']=f'workshop-{i+1}'
(ROOT/'START_HERE.ipynb').write_text(json.dumps(notebook,ensure_ascii=False,indent=1),encoding='utf-8')
print('Built START_HERE.ipynb')
