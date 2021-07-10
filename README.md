DB 오류 수정, Navigation Bar 추가 version:

처음 pull 하고 아래처럼 해주시면 DB 오류 해결됩니다

1. 'db.sqlite' 삭제
2. 'FLASK_FIRST_SHORTCUT.py' 실행

그리고 .gitignore 아래 포함하고 있는지 확인해주세요!


*.pyc
*~
/venv*
*/.idea
.DS_Store
*/__pycache__/
*/db.sqlite

.idea 폴더는 파이참 설정 충돌 날 가능성이 있고, 
__pycache__ 폴더와 .pyc 파일은 import 할 때 생긴 cache 파일이라 제외해주시면 좋아용
