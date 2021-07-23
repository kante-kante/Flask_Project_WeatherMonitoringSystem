# 날씨정보 모니터링 시스템

### 실행

### Windows

```
set FLASK_APP=flaskr
set FLASK_ENV=development
flask run
```

### DB 초기화

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

## DB
### 사용자

| 구분 | 필드명 | 타입 | 비고 |
| ---- | ---- | ---- | ---- |
| 구분자 | id | integer | PRIMARY KEY |
| 이름 | username | text |  |
| 전화번호 | phone | TEXT |  |
| 이메일 | email | TEXT |  |
| 비밀번호 | password | TEXT | |
| 사용자 id | user_id | INT | 사용자 테이블의 아이디 |
| 생성일시 | created | TEXT | |
| 수정일시 | updated | TEXT | |

### 공지사항
| 구분 | 필드명 | 타입 | 비고 |
| ---- | ---- | ---- | ---- |
| 구분자 | id | INT | PRIMARY KEY |
| 사용자 id | user_id | INT | admin만 공지사항 게시 가능 |
| 제목 | title | TEXT |  |
| 내용 | content | TEXT |  |
| 생성일시 | created | TEXT |  |
| 수정일시 | updated | TEXT |  |

### 기기
| 구분 | 필드명 | 타입 | 비고 |
| ---- | ---- | ---- | ---- |
| 구분자 | id | INT | PRIMARY KEY |
| 사용자 id | user_id | INT | admin만 기기 등록 가능 |
| 지역명 | name | TEXT |  |
| API KEY | api | TEXT | 지역별 센서 구분 |
| 생성일시 | created | TEXT |  |
| 수정일시 | updated | TEXT |  |

### 모니터링 테이블
| 구분 | 필드명 | 타입 | 비고 |
| ---- | ---- | ---- | ---- |
| 구분자 | id | INT | PRIMARY KEY |
| 사용자 id | user_id | INT | 사용자 테이블 |
| 기기 id | device_id | INT | 기기 테이블 |
| 미세먼지 | Dust_ratio | TEXT | 각 센서 값  |
| 습도 | H_ratio | TEXT |  |
| 온도 | T_ratio | TEXT |  |
| 조도 | lux | TEXT |  |
| 우천여부 | weather | TEXT |  |
| 생성일시 | created | TEXT |  |
| 수정일시 | updated | TEXT |  |


## 설치해야 할 모듈

### 라즈베리파이
```
sudo apt-get install -y python3 python3-pip python-dev        # 파이썬 개발 킷
sudo pip3 install rpi.gpio                                    # gpio
git clone https://github.com/adafruit/Adafruit_Python_DHT.git # DHT 라이브러리
# 추가로 해당 경로에 setup.py 설치해주어야 한다(DHT 라이브러리 경로)

pip install requests
pip install smbus
```
