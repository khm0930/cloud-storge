# Cloud Storage 웹 애플리케이션

## 프로젝트 소개
이 프로젝트는 사용자 친화적인 클라우드 스토리지 웹 애플리케이션입니다. 사용자들이 파일을 안전하게 저장하고 관리할 수 있는 개인 클라우드 스토리지 서비스를 제공합니다.

## 주요 기능
- **파일 관리**
  - 파일 업로드/다운로드
  - 폴더 생성 및 관리
  - 드래그 앤 드롭 파일 업로드
  - 파일 이동 및 삭제
  - 폴더 구조 지원

- **사용자 관리**
  - 이메일 기반 회원가입/로그인
  - 소셜 로그인 (Google, Apple)
  - 비밀번호 재설정
  - 사용자별 파일 관리

- **보안**
  - 사용자 인증 및 권한 관리
  - 파일 접근 제어
  - 안전한 파일 저장 및 관리

## 기술 스택
- **백엔드**
  - Django (Python 웹 프레임워크)
  - Django REST Framework
  - MySQL (데이터베이스)

- **프론트엔드**
  - HTML5/CSS3
  - JavaScript
  - Bootstrap 5
  - Font Awesome

- **인프라**
  - Docker
  - Nginx
  - Gunicorn
  - Prometheus (모니터링)
  - Logstash (로그 관리)

## 프로젝트 구조
```
cloud-storage/
├── cloudapp/              # 메인 애플리케이션
│   ├── templates/        # HTML 템플릿
│   ├── static/          # 정적 파일
│   └── models.py        # 데이터베이스 모델
├── cloudserver/         # 서버 설정
├── static/             # 전역 정적 파일
├── Dockerfile          # Docker 이미지 설정
├── docker-compose.yml  # Docker 컨테이너 구성
└── requirements.txt    # Python 패키지 의존성
```

## 설치 및 실행
1. 저장소 클론
```bash
git clone [repository-url]
cd cloud-storage
```

2. 환경 설정
```bash
cp .env.example .env
# .env 파일에 필요한 환경 변수 설정
```

3. Docker로 실행
```bash
docker-compose up -d
```

4. 로컬 개발 환경 설정
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 개발 환경 설정
- Python 3.8 이상
- Docker 및 Docker Compose
- Node.js 및 npm (프론트엔드 개발용)

## 기여 방법
1. 이슈 생성 또는 기존 이슈 확인
2. 새로운 브랜치 생성
3. 변경사항 커밋
4. Pull Request 생성

## 라이선스
이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 연락처
프로젝트에 대한 문의사항이 있으시면 이슈를 생성해 주시기 바랍니다.


