# 코딩 없이 만드는 RAG와 LLM Wiki

코드를 작성하거나 수정하지 않습니다. **실습 노트북을 열고 버튼을 누르면** 같은 자료로 RAG와 LLM Wiki를 만들 수 있습니다.

<!-- COLAB_LINK_START -->
[![Colab에서 실습 시작](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/RichGom84/llm-wiki-rag-nocode/blob/main/START_HERE.ipynb)

공개 저장소는 위 버튼으로 엽니다. 비공개이거나 접근이 안 되면 노트북을 다운로드해 Colab에 업로드하세요.
<!-- COLAB_LINK_END -->

## 준비물

- Google 계정과 PC 브라우저
- 사용 가능한 OpenAI API 키와 API 사용 한도 (API 호출 비용 별도)
- 공개 GitHub 자료를 받기만 하는 수강생은 GitHub 계정이 없어도 됩니다. 개인 저장소에 결과를 커밋하려면 GitHub 계정이 필요합니다.
- Python 설치, VS Code, Git 명령어, GPU는 필요하지 않습니다.

## 수강생 시작 순서

1. 위의 **Colab에서 실습 시작** 버튼을 눌러 노트북을 엽니다.
2. Google 계정으로 로그인하고 런타임에 연결합니다. 버튼으로 열리지 않으면 `START_HERE.ipynb`를 다운로드한 뒤 [Google Colab](https://colab.research.google.com/)에서 **파일 → 노트북 업로드**로 여세요.
3. `1단계 실습 준비` 왼쪽 실행 버튼을 누릅니다.
4. `2단계 AI 연결`을 실행하고 **비밀번호 입력란**에 API 키를 입력합니다. 코드에는 쓰지 않습니다.
5. `3단계 실습 화면 열기`를 실행합니다. 아래에 실습 버튼들이 나옵니다.
6. **RAG 만들기 / 갱신 → 검색 근거만 보기 → RAG에 질문하기**를 차례로 누릅니다.
7. **Wiki 만들기 / 갱신 → Wiki 페이지 읽기 → Wiki에 질문하기**를 누릅니다.
8. 강사의 안내 후 **변경 공지 D11 추가**를 누릅니다. RAG와 Wiki의 갱신 버튼을 각각 누릅니다.
9. 같은 질문에 다시 답하게 하고 출처와 수정 내용을 확인합니다.
10. **결과 ZIP 다운로드**를 눌러 컴퓨터에 저장합니다. 실습 종료 전에 다운로드를 확인합니다.

Colab에서 실행 허용 안내가 나오면 이 수업에서 배포한 노트북인지 확인한 후 진행하세요. 메뉴 이름은 화면 언어에 따라 다를 수 있습니다.

## 무엇을 만드는가

| RAG | LLM Wiki |
|---|---|
| 질문과 관련된 원문 조각을 검색하고 AI가 답변 | AI가 여러 원문을 종합해 주제별 Markdown 페이지를 저장 |
| 검색 근거를 눈으로 확인 | 목차·출처·관련 페이지·변경 이력을 눈으로 확인 |
| 이번 수업은 BM25 키워드 검색 | 이번 수업은 생성한 페이지를 키워드로 찾아 답변 |

RAG는 벡터 검색만을 뜻하지 않습니다. 이 실습에는 임베딩 모델이나 Chroma 설치가 없습니다. Wiki도 질문할 때 검색을 사용하므로 두 방식은 배타적이지 않습니다. 이번 비교의 핵심은 **원문 조각을 검색하는가, 미리 종합한 지식 페이지를 검색하는가**입니다.

## 자료 안내

- [수강생 안내서](docs/STUDENT_GUIDE.md)
- [강사 운영 안내](teacher/TEACHER_GUIDE.md)
- [비교 질문 10개](materials/questions.md)
- [가상 원문 10개](materials/raw)
- [추가할 변경 공지](materials/updates/D11.md)
- [강사용 정답](teacher/ANSWER_KEY.md) — 검색 자료에 넣지 않습니다.
- [강사용 Word 강의안](docs/LLM_Wiki_RAG_노코딩_강의안.docx)

원문은 수업용 가상 데이터입니다. 학생 화면에는 기본 원문 10개만 들어 있고 D11은 버튼을 눌러야 추가됩니다. 노트북에는 원문과 실행 코드가 내장되어 있어 별도의 Git 복제 명령이 필요 없습니다. 원문을 수정한 강사는 노트북도 다시 만들어야 합니다.

## 결과 보관

Colab 런타임은 임시 환경입니다. 다운로드 ZIP에 `raw/`, `wiki/`, `rag_index.json`, `results.json`이 저장됩니다. API 키는 내보내지 않습니다. `wiki/versions/`에 갱신 전 페이지를 보관합니다. 결과 ZIP을 압축 해제해 Wiki 파일을 열거나 본인 GitHub 저장소에 업로드할 수 있습니다.

## 검증 범위

검색·중복 방지·갱신·Wiki 링크 검사·ZIP 내보내기·API 요청 형식은 로컬 자동 검사를 거쳤습니다. 자동 검사에서 AI 응답은 모의 응답을 사용했습니다. 실제 API와 Google Colab 로그인 환경의 최종 동작은 강사가 수업 전에 확인해야 합니다. 정답률이나 API 비용을 보장하지 않습니다.
