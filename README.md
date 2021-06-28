# 날씨정보 모니터링 시스템

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
| 로그인 처리| POST | /auth/login |
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

## 참고사항 및 알림
해당 프로젝트의 README.md를 수정중에 있습니다.
빠르게 수정하겠습니다.

해당 프로젝트는 FLASK 파이썬 웹 프레임워크를 사용하였으며
라즈베리파이에서 센서 정보를 읽어 웹으로 보내주도록 전체적인 구성을 기획하였습니다.
참고 URL: https://www.youtube.com/watch?v=08ClT0fghRM
