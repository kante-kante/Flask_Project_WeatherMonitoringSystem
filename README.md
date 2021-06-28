# 자원 모니터링 시스템

### 실행

### Windows

```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

##DB 초기화

```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask init-db
```

## URL 규칙

### 인증

| 기능 | method | url |
| --- | --- | --- |
| 로그인 화면 | GET | /auth/login |
| 로그인 처리 | POST | /auth/login |
| 가입 화면 | GET | /auth/register |
| 가입 처리 | POST | /auth/register |
| 로그아웃 처리 | GET | /auth/logout |

### 게시판 URL
| method | url |
| --- | --- |
| GET | /board/list |
| GET | /board/view/1 |
| GET | /board/add |
| POST | /board/add |
| GET | /board/update |
| POST | /board/update/1 |
| POST | /board/delete/1 |
"# Python Flask�� �̿��� �������� ����͸� �ý���" 
