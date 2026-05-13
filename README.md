# 6/45 Lotto Django Docker Project

## 제출자 정보

- 과목명: 오픈소스SW기초 3분반
- 과제명: Django와 Docker를 사용한 6/45 Lotto 웹 사이트 개발
- 학번: 32212817
- 이름: 유지웅

---

## 1. 프로젝트 개요

본 프로젝트는 오픈소스SW기초 과제로 개발한 Django 기반 6/45 Lotto 웹 사이트입니다.

일반 사용자는 수동 번호 또는 자동 번호로 복권을 구매하고, 추첨 결과에 따라 당첨 여부를 확인할 수 있습니다.  
관리자는 Django 관리자 페이지와 별도의 추첨 페이지를 통해 판매 내역 확인, 추첨 번호 생성, 당첨 내역 확인 기능을 사용할 수 있습니다.

---

## 2. 주요 기능

### 일반 사용자 기능

- 수동 번호 복권 구매
- 자동 번호 복권 구매
- 당첨 결과 확인

### 관리자 기능

- Django admin을 통한 판매 내역 확인
- 회차별 당첨 번호 추첨
- 당첨 내역 확인

---

## 3. 사용 기술

- Python
- Django
- Docker
- Docker Compose
- PostgreSQL

---

## 4. 프로젝트 구조

```text
lotto_project/
├─ Dockerfile
├─ compose.yaml
├─ requirements.txt
├─ manage.py
├─ README.md
├─ .gitignore
├─ .dockerignore
├─ lotto/
│  ├─ admin.py
│  ├─ apps.py
│  ├─ models.py
│  ├─ urls.py
│  ├─ views.py
│  ├─ migrations/
│  └─ templates/
│     └─ lotto/
│        ├─ index.html
│        ├─ buy_manual.html
│        ├─ buy_auto.html
│        ├─ draw.html
│        └─ check.html
└─ lotto_project/
   ├─ settings.py
   ├─ urls.py
   ├─ wsgi.py
   └─ asgi.py
```

---

## 5. Docker 구성

본 프로젝트는 Docker Compose를 사용하여 multi-container 환경으로 구성하였습니다.

```text
Docker Compose
├─ web: Django 웹 애플리케이션 컨테이너
└─ db: PostgreSQL 데이터베이스 컨테이너
```

### 서비스 구성

- `web`: Django Lotto 웹 애플리케이션 실행
- `db`: PostgreSQL 데이터베이스 실행
- `postgres_data`: PostgreSQL 데이터 유지를 위한 Docker volume

---

## 6. 실행 방법

### 1단계. Docker Compose 실행

프로젝트 루트 디렉토리에서 다음 명령어를 실행합니다.

```bash
docker compose up --build
```

또는 백그라운드에서 실행하려면 다음 명령어를 사용합니다.

```bash
docker compose up --build -d
```

---

### 2단계. DB 마이그레이션

처음 실행하는 경우 새 터미널에서 다음 명령어를 실행합니다.

```bash
docker compose exec web python manage.py migrate
```

---

### 3단계. 관리자 계정 생성

```bash
docker compose exec web python manage.py createsuperuser
```

---

### 4단계. 웹 사이트 접속

브라우저에서 다음 주소로 접속합니다.

```text
http://127.0.0.1:8000/lotto/
```

---

### 5단계. 관리자 페이지 접속

```text
http://127.0.0.1:8000/admin/
```

---

## 7. 주요 페이지

| 페이지 | 주소 | 설명 |
|---|---|---|
| 메인 페이지 | `/lotto/` | Lotto 웹 사이트 메인 화면 |
| 수동 구매 | `/lotto/buy/manual/` | 사용자가 직접 번호 6개 선택 |
| 자동 구매 | `/lotto/buy/auto/` | 서버가 번호 6개 자동 생성 |
| 추첨 기능 | `/lotto/admin/draw/` | 회차별 당첨 번호 생성 |
| 당첨 확인 | `/lotto/check/` | 구매 번호와 당첨 번호 비교 |
| 관리자 페이지 | `/admin/` | 판매 내역 및 추첨 내역 확인 |

---

## 8. 데이터베이스 관련 안내

본 프로젝트는 Docker Compose 환경에서 PostgreSQL을 사용합니다.

PostgreSQL 데이터는 Docker volume에 저장되므로, 같은 컴퓨터에서는 컨테이너를 종료한 뒤 다시 실행해도 데이터가 유지됩니다.

```bash
docker compose down
docker compose up -d
```

단, 아래 명령어는 volume까지 삭제할 수 있으므로 주의해야 합니다.

```bash
docker compose down -v
```

다른 컴퓨터에서 처음 실행할 경우 데이터베이스는 비어 있는 상태로 시작합니다.  
따라서 처음 실행 시 `migrate` 명령어와 `createsuperuser` 명령어를 다시 실행해야 합니다.

---

## 9. 테스트 내용

본 프로젝트에서는 다음 기능을 테스트하였습니다.

| 테스트 항목 | 확인 내용 |
|---|---|
| 메인 페이지 접속 | `/lotto/` 접속 시 메인 화면 출력 |
| 수동 구매 | 사용자가 선택한 번호 6개가 저장되는지 확인 |
| 자동 구매 | 1~45 사이의 중복 없는 번호 6개가 생성되는지 확인 |
| 추첨 기능 | 회차별 당첨 번호 6개가 생성되는지 확인 |
| 중복 추첨 방지 | 이미 추첨된 회차를 다시 추첨하지 못하도록 처리 |
| 당첨 확인 | 구매 번호와 당첨 번호의 일치 개수 출력 |
| 관리자 페이지 | 구매 내역과 추첨 내역 확인 |
| Docker 실행 | web, db 컨테이너가 함께 실행되는지 확인 |
| 데이터 유지 | Docker volume을 통해 DB 데이터가 유지되는지 확인 |

---

## 10. AI 도구 사용 내역

본 프로젝트에서는 ChatGPT를 학습 보조 도구로 사용하였습니다.

주요 사용 목적은 다음과 같습니다.

- Lotto 모델 설계 방향 검토
- 수동 구매, 자동 구매, 추첨, 당첨 확인 기능 구현 과정 설명
- Dockerfile 및 Docker Compose 구성 방향 검토
- 오류 원인 분석 및 해결 방법 확인
 
최종 구현, 실행, 테스트는 개발자가 직접 수행하였습니다.

---

## 11. 참고 사항

본 프로젝트는 학습 및 과제 제출 목적의 예제 프로젝트입니다.  
실제 6/45 로또 시스템과 달리 보너스 번호, 실제 결제, 회원 인증 등의 기능은 구현하지 않았습니다.  
수업에서 학습한 Django의 model, view, url, template, admin 기능과 Docker의 image, container, volume, compose 개념을 적용하는 데 중점을 두었습니다.