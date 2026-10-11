import ipywidgets as W
from IPython.display import display, clear_output

status=W.HTML(value='<b>준비됨</b> · 원문 10개가 들어 있습니다. RAG 만들기부터 누르세요.')
question=W.Textarea(value=QUESTIONS[0],description='질문',layout=W.Layout(width='98%',height='75px'))
preset=W.Dropdown(options=[(str(i+1)+'. '+q,q) for i,q in enumerate(QUESTIONS)],description='연습 질문',layout=W.Layout(width='98%'))
preset.observe(lambda change:setattr(question,'value',change['new']),names='value')
rag_k=W.IntSlider(value=3,min=1,max=5,description='RAG 근거 수')
wiki_k=W.IntSlider(value=2,min=1,max=4,description='Wiki 페이지 수')
output=W.Output()
buttons=[]
def action(label,fn):
    b=W.Button(description=label,layout=W.Layout(width='220px',height='36px'))
    buttons.append(b)
    def clicked(_):
        for x in buttons:x.disabled=True
        with output:
            clear_output(wait=True)
            try:fn()
            except WorkshopError as e:print('안내:',str(e))
            except Exception:print('예상하지 못한 오류입니다. 화면을 강사에게 보여주세요. 키나 개인정보는 공유하지 마세요.')
            finally:
                for x in buttons:x.disabled=False
                status.value=f'<b>원문 {len(workshop.sources)}개 · 질문 기록 {sum(x["mode"] in ["RAG","Wiki"] for x in workshop.history)}개</b> · API 모델 {MODEL}'
    b.on_click(clicked);return b

def show_evidence(records):
    if not records:print('검색된 근거 없음')
    for x in records:
        print('\n근거:',x['id'],'| 검색 점수:',x['score']);print(x['text'])
def question_text():
    q=question.value.strip()
    if not q:raise WorkshopError('질문을 입력하세요.')
    if len(q)>1000:raise WorkshopError('질문을 1,000자 이내로 줄여주세요.')
    return q

def build_rag():print('RAG 준비 완료. 원문 조각',workshop.build_rag(),'개. 이 단계는 API를 호출하지 않습니다.')
def preview():show_evidence(workshop.rag_evidence(question_text(),rag_k.value))
def ask_rag():
    q=question_text();e=workshop.rag_evidence(q,rag_k.value);show_evidence(e)
    print('\nAI가 답변을 작성하고 있습니다...')
    r=workshop.answer_rag(q,rag_k.value);print('\nRAG 답변\n'+r['answer']);print('답변 처리:',r['seconds'],'초 | 토큰:',r['usage'])
def build_wiki():
    pages=workshop.build_wiki(lambda i,n,p:print(f'AI 작성 {i}/{n}: {p}'))
    print('저장 완료:',', '.join(pages) if pages else '변경이 없어 재생성하지 않았습니다.')
    print('페이지 선택에서 문서를 읽고, 원문 출처와 조건을 확인하세요.')
def ask_wiki():
    q=question_text();e=workshop.wiki_evidence(q,wiki_k.value);show_evidence(e)
    print('\nAI가 답변을 작성하고 있습니다...')
    r=workshop.answer_wiki(q,wiki_k.value);print('\nWiki 답변\n'+r['answer']);print('답변 처리:',r['seconds'],'초 | 토큰:',r['usage'])
def update():
    print('D11 추가 완료.' if workshop.add_update() else 'D11은 이미 추가되어 있습니다.')
    print('원문 추가만으로 색인과 Wiki가 갱신되지는 않습니다. RAG 만들기/갱신과 Wiki 만들기/갱신을 각각 누르세요.')
    print('Wiki 갱신 대상:',', '.join(workshop.dirty_pages()))
def download():
    import tempfile
    dest=str(Path(tempfile.gettempdir())/'my-workshop-results.zip')
    workshop.export(dest)
    try:
        from google.colab import files
        files.download(dest)
    except ImportError:
        from IPython.display import FileLink
        display(FileLink(dest))
    print('내보낸 항목: 원문, Wiki, 변경 이력, 검색 색인, 질문 결과. API 키는 내보내지 않습니다.')

source_pick=W.Dropdown(options=list(SAMPLE_SOURCES)+['D11'],description='원문')
page_pick=W.Dropdown(options=['index.md',*TOPICS,'log.md'],description='Wiki 페이지')
def read_source():
    sid=source_pick.value
    print(workshop.sources.get(sid,'아직 추가되지 않은 변경 공지입니다. 강사의 안내 후 추가하세요.'))
def read_page():
    path=workshop.root/'wiki'/page_pick.value
    print(path.read_text(encoding='utf-8') if path.exists() else '먼저 Wiki를 만들어 주세요.')
def read_diff():print(workshop.diffs.get(page_pick.value,'이 페이지의 변경 비교 기록이 없습니다.'))
def show_usage():
    sums={}
    for row in workshop.history:
        phase=row['mode']; d=sums.setdefault(phase,{'calls':0,'input_tokens':0,'output_tokens':0})
        d['calls']+=1
        for key in ['input_tokens','output_tokens']:d[key]+=row.get('usage',{}).get(key,0)
    print(json.dumps(sums,ensure_ascii=False,indent=2))
    print('초기 Wiki 작성과 갱신 호출도 포함됩니다. 가격은 강사가 수업일의 API 요율로 계산합니다.')

controls=W.VBox([
 status,
 W.HTML('<h3>1 원문 확인</h3>'),W.HBox([source_pick,action('선택한 원문 읽기',read_source)]),
 W.HTML('<h3>2 질문 선택</h3>'),preset,question,
 W.HTML('<h3>3 RAG 실습</h3>'),rag_k,
 W.HBox([action('RAG 만들기 / 갱신',build_rag),action('검색 근거만 보기',preview),action('RAG에 질문하기',ask_rag)]),
 W.HTML('<h3>4 Wiki 실습</h3>'),wiki_k,
 W.HBox([action('Wiki 만들기 / 갱신',build_wiki),action('Wiki에 질문하기',ask_wiki)]),
 W.HBox([page_pick,action('Wiki 페이지 읽기',read_page),action('수정 전후 보기',read_diff)]),
 W.HTML('<h3>5 변경 실험과 제출</h3>'),
 W.HBox([action('변경 공지 D11 추가',update),action('사용량 확인',show_usage),action('결과 ZIP 다운로드',download)]),
 W.HTML('<p>아래에 마지막 실행 결과가 표시됩니다. AI 답변은 출처와 대조하세요.</p>'),output])
display(controls)
