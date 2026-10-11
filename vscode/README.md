# VS Code + GPT로 만드는 RAG와 LLM Wiki

GPT 도구는 **OpenAI의 Codex IDE 확장**을 사용합니다. 수강생은 코드를 직접 작성하지 않고 [지시문 10개](PROMPTS.md)를 Codex 채팅에 복사합니다. Codex가 준비된 검색 도구를 실행하고 답변과 Wiki 문서를 파일로 작성합니다.

## 준비물

1. VS Code와 Python 3.10 이상을 수업 전에 설치합니다. Python 확장을 설치하는 것과 Python 실행기를 설치하는 것은 별개입니다.
2. VS Code 확장 보기에서 OpenAI가 제공하는 Codex 확장을 설치합니다. 공식 [설치 안내](https://learn.chatgpt.com/docs/codex/ide)를 이용하세요.
3. Codex에서 **Sign in with ChatGPT**로 로그인합니다. 계정의 Codex 사용 가능 여부와 한도를 사전에 확인합니다. 이 경로는 별도의 API 키를 입력하지 않으며, 무제한 사용을 뜻하지 않습니다.
4. 저장소의 **Code / Download ZIP**으로 자료를 받고 압축을 풉니다. VS Code의 **File / Open Folder**에서 README.md, materials, src, vscode 폴더가 함께 보이는 최상위 폴더를 엽니다.

Python 표준 라이브러리만 사용하므로 pip 패키지 설치, GPU, 벡터 DB는 필요하지 않습니다. GitHub 자료를 다운로드해서 실습할 때 Git 설치도 필수가 아닙니다.

## 만드는 방식

| 단계 | RAG | LLM Wiki |
|---|---|---|
| 자료 준비 | Python 도구가 원문 조각을 검색 준비 | Python 도구가 주제별 원문 묶음을 준비 |
| AI 작업 | Codex가 검색된 근거를 읽고 답변 작성 | Codex가 주제별 Markdown 페이지를 작성 |
| 질문 | 원문 조각을 BM25로 검색 | 저장한 Wiki 페이지를 BM25로 검색 |
| 변경 | 검색 색인 재생성 | 영향을 받는 페이지 수정 후 등록 |

이것은 **검색 도구와 Codex의 생성 단계를 수강생이 연결하는 교육용 RAG 워크플로**입니다. Python 도구 자체는 AI API를 호출하지 않습니다. 독립 실행형 자동 챗봇, 엄격히 격리한 성능 벤치마크는 아닙니다. 파일 형식과 출처 ID 검사는 사실의 정확성을 보장하지 않습니다.

## 진행 순서

| 순서 | 지시문 | 결과 확인 |
|---|---|---|
| 1 | 준비 점검 | output/raw에 D01~D10 |
| 2 | RAG 검색 | output/contexts/rag-q1-before.md |
| 3 | RAG 답변 | output/answers/rag-q1-before.md |
| 4 | 근거 수 비교 | 질문 5의 근거 수 1과 3 비교 |
| 5 | Wiki 작성 | output/wiki에 주제 페이지 4개 |
| 6 | Wiki 검토 | 출처와 필수 조건 확인 |
| 7 | Wiki 질문 | output/answers/wiki-q5-before.md |
| 8 | 변경 반영 | D11 추가, schedule.md 수정 |
| 9 | 변경 후 비교 | 같은 질문의 전후 결과 |
| 10 | 결과 저장 | exports/vscode-results.zip |

`vscode/output`과 `vscode/exports`는 작업 결과이며 Git 추적에서 제외했습니다. 수강생이 선택 활동으로 결과를 공개하려면 ZIP을 풀어 본인 저장소에 업로드합니다. raw와 wiki 폴더를 함께 올려 상대 링크를 유지합니다.

## 비교할 때의 규칙

- 답변 생성은 **새 Codex 채팅**에서 합니다. 관련 없는 편집기 탭을 닫고, 가능하면 자동 편집기 문맥 포함을 끕니다.
- 답변 지시문에는 읽을 근거 파일을 하나만 지정합니다. 원문 전체, 정답표, 다른 방식의 답변을 추가로 읽지 않도록 명시합니다.
- Codex의 파일 읽기 기록을 확인합니다. 지정하지 않은 자료를 읽었다면 그 응답은 비교에서 제외합니다.
- 이 방법은 문맥 혼입을 줄이지만 기술적으로 접근을 차단하지는 않습니다. 엄밀한 비교에는 별도의 격리 실행 환경이 필요합니다.
- 모델 이름은 계정에서 제공되는 선택지를 사용하고 두 방식에서 동일하게 맞춰 기록합니다. 고정된 최신 모델명이나 가격을 수업 자료에서 가정하지 않습니다.
- 생성 답변과 원문을 대조합니다. 정답표는 강사만 비교 후 사용합니다.

## 강사용 명령 안내

수강생은 아래 명령을 외울 필요가 없습니다. 지시문을 받은 Codex가 운영체제에 맞는 Python 실행 명령을 확인하여 실행합니다. Windows는 `py -3`, macOS/Linux는 `python3` 등이 될 수 있습니다.

```text
python vscode/lab.py prepare
python vscode/lab.py rag-index
python vscode/lab.py rag-context --question "질문" --k 3 --label rag-q1-before
python vscode/lab.py wiki-packets
python vscode/lab.py wiki-register
python vscode/lab.py wiki-status
python vscode/lab.py wiki-context --question "질문" --k 2 --label wiki-q1-before
python vscode/lab.py add-update
python vscode/lab.py export
```

`wiki-packets`는 작성할 원문 묶음을 만들고 기존 대상 페이지를 versions에 백업합니다. AI가 페이지를 쓴 후 `wiki-register`로 출처 ID·링크·파일 상태를 검사합니다. 원문이 바뀐 채 갱신하지 않으면 context 명령은 중단합니다.

## 공식 안내

- [Codex IDE](https://learn.chatgpt.com/docs/codex/ide)
- [ChatGPT 로그인과 API 키 인증](https://learn.chatgpt.com/docs/auth)
- [VS Code 확장 설치](https://code.visualstudio.com/docs/configure/extensions/extensions)
- [Python 실행기 설치](https://code.visualstudio.com/docs/languages/python)

확인일: 2026-10-12. 화면 이름과 이용 조건은 바뀔 수 있습니다.
