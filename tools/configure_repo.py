"""Instructor: add a real Colab link after selecting the GitHub repository."""
from pathlib import Path
import argparse,re
p=argparse.ArgumentParser();p.add_argument('repository');p.add_argument('--ref',default='main');a=p.parse_args()
if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',a.repository):p.error('Use OWNER/REPOSITORY')
if not re.fullmatch(r'[A-Za-z0-9_.-]+',a.ref):p.error('Use a simple branch or tag name')
r=Path(__file__).resolve().parents[1]/'README.md'
url=f'https://colab.research.google.com/github/{a.repository}/blob/{a.ref}/START_HERE.ipynb'
text=f'<!-- COLAB_LINK_START -->\n[![Colab에서 실습 시작](https://colab.research.google.com/assets/colab-badge.svg)]({url})\n\n공개 저장소는 위 버튼으로 엽니다. 비공개이거나 접근이 안 되면 노트북을 다운로드해 Colab에 업로드하세요.\n<!-- COLAB_LINK_END -->'
r.write_text(re.sub(r'<!-- COLAB_LINK_START -->.*?<!-- COLAB_LINK_END -->',lambda _:text,r.read_text(),flags=re.S),encoding='utf-8')
print('Updated README Colab link')
