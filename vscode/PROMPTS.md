# 수강생용 복사 지시문 10개

각 코드 블록은 **Codex 채팅에 붙이는 한국어 지시문**입니다. 터미널에 붙이지 않습니다. 답변 생성 단계에서 새 채팅을 여세요. 지시문 전체 문서를 답변 채팅에 첨부하지 말고 필요한 블록만 복사하세요.

## 01. 준비 점검

```text
나는 코딩 초보자야. vscode/README.md만 먼저 읽고 이 실습 폴더가 맞는지 확인해줘. Python 3.10 이상을 실행할 수 있는 명령을 확인하고, 설치가 필요하면 내게 안내해줘. 가능하면 vscode/lab.py prepare를 실행해줘. pip 패키지는 설치하지 마. 원본과 기존 결과를 지우지 말고, vscode/output/raw에 원문이 몇 개인지 알려줘. Python 명령도 알려줘.
```

## 02. RAG 검색 자료 준비

```text
준비된 Python으로 vscode/lab.py rag-index를 실행해줘. 그다음 rag-context를 question="Python 기초반 개강일은 언제인가요?", k=3, label=rag-q1-before로 실행해줘. vscode/output/contexts/rag-q1-before.md를 열고 검색된 원문 ID만 알려줘. 아직 질문의 답은 쓰지 마. lab.py와 검색 알고리즘은 바꾸지 마.
```

## 03. RAG 답변 작성 — 새 채팅

```text
이번 채팅에서는 vscode/output/contexts/rag-q1-before.md만 읽고 그 안의 질문에 답해줘. 다른 원문, 정답표, 웹, 이전 답변을 찾지 마. 근거가 부족하면 제공된 자료로 확인할 수 없다고 말해줘. 주요 주장에 [D번호] 출처를 붙여줘. 답변과 사용한 원문 ID를 vscode/output/answers/rag-q1-before.md에 저장해줘. 이 파일이 이미 있으면 덮어쓰지 말고 새 이름을 사용해줘. 읽은 파일 목록도 알려줘.
```

## 04. 검색 근거 수 비교

```text
질문은 "Python 기초반과 RAG 실습반의 차이는 무엇인가요?"야. 준비된 Python으로 vscode/lab.py rag-context를 두 번 실행해줘. 첫 번째는 k=1, label=rag-q5-k1-before, 두 번째는 k=3, label=rag-q5-k3-before로 해줘. 두 근거 파일 경로만 알려주고 답변은 아직 쓰지 마. 검색 코드는 수정하지 마.
```

각 근거 파일에 대해 **새 채팅에서 03번**을 실행하되, 파일명 `rag-q1-before`를 각각 `rag-q5-k1-before`, `rag-q5-k3-before`로 바꿉니다. 두 답변을 생성할 때 서로의 근거 파일과 답변을 첨부하지 않습니다.

## 05. Wiki 작성

```text
준비된 Python으로 vscode/lab.py wiki-packets를 실행해줘. 반환된 페이지에 해당하는 vscode/output/contexts/wiki-build-*.md만 읽고 각 작성 지침에 따라 vscode/output/wiki의 같은 이름 페이지를 만들어줘. 원문에 없는 사실을 추가하지 말고 주요 주장마다 출처를 적어줘. 패킷에 제시된 원문 파일과 관련 페이지 링크를 모두 포함해줘. 원본 자료와 lab.py는 수정하지 마. 작성 후 wiki-register를 실행해 검사하고 목차를 만들어줘. 형식 검사를 사실 검증이라고 말하지 마.
```

## 06. Wiki 검토

```text
vscode/output/wiki/courses.md와 이 페이지가 출처로 삼은 vscode/output/raw/D01.md, D02.md, D03.md를 대조해줘. 교육 내용, 총 시간, 선수 지식, 보충 과제 조건이 정확한지 확인해줘. 근거와 다른 문장이 있으면 원문을 기준으로 이 페이지만 고쳐줘. 다른 페이지는 수정하지 마. 수정했다면 wiki-register를 다시 실행해줘. 내가 직접 확인할 원문 문장과 수정 내용을 알려줘.
```

## 07. Wiki 답변 — 새 채팅

```text
Python으로 vscode/lab.py wiki-context를 question="Python 기초반과 RAG 실습반의 차이는 무엇인가요?", k=2, label=wiki-q5-before로 실행해줘. 생성한 vscode/output/contexts/wiki-q5-before.md만 읽고 질문에 답해줘. 원문 전체, 정답표, 웹, 다른 답변을 읽지 마. 주요 주장에 원문 ID를 붙이고 근거가 없으면 확인할 수 없다고 말해줘. 답변을 vscode/output/answers/wiki-q5-before.md에 저장하고 읽은 파일 목록을 알려줘. 기존 답변 파일은 보존해줘.
```

## 08. 변경 공지 반영

이 단계 전 질문 7의 변경 전 답변을 남깁니다. 02·03·07 지시문의 질문과 label을 `rag-q7-before`, `wiki-q7-before`로 바꿔 각각 새 채팅에서 실행합니다. 질문 7: 두 과정을 연속으로 수강할 때 일정이 겹치나요?

```text
Python으로 vscode/lab.py add-update를 실행하고, rag-index를 다시 실행해줘. wiki-packets를 실행해 반환된 갱신 대상만 확인해줘. 해당 wiki-build 패킷과 기존 대상 페이지를 읽고 원문 기준으로 수정해줘. 대체 범위 밖의 내용과 다른 페이지는 그대로 보존해줘. wiki-register로 등록한 뒤 wiki-status가 빈 목록인지 확인해줘. 수정 전 파일은 wiki/versions에 보관됐는지 확인하고, 변경 이유를 설명해줘.
```

## 09. 변경 후 비교

```text
Python으로 vscode/lab.py의 context 명령을 실행해서 질문 "두 과정을 연속으로 수강할 때 일정이 겹치나요?"의 근거 파일 두 개를 만들어줘. rag-context는 k=3, label=rag-q7-after, wiki-context는 k=2, label=wiki-q7-after로 해줘. 파일 경로와 검색한 항목만 알려줘. 아직 답변은 작성하지 마.
```

각 파일에 대해 **새 채팅에서 03번**의 경로를 바꿔 답변을 만듭니다. 변경 전후 답변이 모두 나온 다음 강사와 함께 비교합니다. 질문 8~10도 질문과 label을 바꿔 같은 절차로 반복할 수 있습니다. 자료에 없는 질문에는 확인 불가를 기대합니다.

## 10. 결과 보관

```text
materials/comparison.csv 형식을 참고해 vscode/output/comparison.csv를 만들어줘. 이번에 실제로 생성된 answers와 contexts를 읽어 질문별 기록을 정리해줘. 실행하지 않은 문항과 사람이 아직 평가하지 않은 점수는 빈칸으로 두고 정답률이나 비용을 추정하지 마. Python으로 vscode/lab.py export를 실행해 결과 ZIP을 만들어줘. ZIP 경로와 포함된 폴더를 알려줘. 외부 업로드나 GitHub 공개는 하지 마.
```

완성 ZIP은 `vscode/exports/vscode-results.zip`입니다. 답변 기록과 비교 점수는 수강생이 원문으로 최종 확인합니다.
