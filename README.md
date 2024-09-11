# 클라우드 스토리지 애플리케이션

이 저장소는 클라우드 스토리지 애플리케이션의 소스 코드를 포함하고 있습니다. 이 프로젝트는 Django로 구현된 백엔드 서비스, Docker를 사용한 컨테이너화된 배포, 그리고 Prometheus 및 Grafana를 통한 모니터링 서비스를 포함하고 있습니다.

## 프로젝트 구조

- `cloudapp/`: 클라우드 스토리지 관련 기능을 처리하는 Django 애플리케이션을 포함하고 있습니다.
- `cloudserver/`: 클라우드 스토리지 애플리케이션을 실행하는 서버 측 로직 및 설정 파일이 포함되어 있습니다.
- `static/admin/`: Django 관리자 인터페이스를 위한 정적 파일들이 포함되어 있습니다.
- `.env`: 프로젝트 환경 설정을 위한 환경 변수 파일(저장소에 포함되지 않음).
- `.gitattributes`: Git 파일 속성 관리 설정 파일.
- `.gitignore`: Git에서 버전 관리하지 않을 파일 및 디렉토리를 지정하는 파일.
- `Dockerfile`: 클라우드 스토리지 애플리케이션의 Docker 이미지를 빌드하기 위한 설정 파일.
- `alertmanager.yml`: Prometheus Alertmanager 설정 파일로, 사전에 정의된 규칙에 따라 알림을 보냅니다.
- `docker-compose.yml`: 여러 컨테이너(Django, Nginx, Prometheus, Grafana 등)를 관리하는 Docker Compose 설정 파일.
- `manage.py`: Django의 관리 작업을 위한 명령어 도구.
- `prometheus.yml`: Prometheus 설정 파일로, 모니터링 시스템을 구성하는 데 사용됩니다.
- `requirements.txt`: Django 애플리케이션에 필요한 Python 패키지 종속성 목록을 포함합니다.
- `runserver.sh`: Django 개발 서버를 실행하기 위한 셸 스크립트.

## 프로젝트 실행 방법

### 사전 준비 사항

- Docker 및 Docker Compose가 설치되어 있어야 합니다.
- Python 3.8 이상의 버전이 필요합니다.

### 실행 절차

1. 저장소를 클론합니다:
   ```bash
   git clone https://github.com/khm0930/cloud-storge.git

2. 프로젝트 디렉토리로 이동합니다:
   ```bash
   cd cloudserver_copy

3. Docker Compose를 사용해 컨테이너를 빌드하고 실행합니다:
    ```bash
   docker-compose up --build

4. 다음 경로에서 애플리케이션에 접근할 수 있습니다:

   - 클라우드 스토리지 애플리케이션: http://localhost:8001
   - Grafana 대시보드: http://localhost:3000
   - Prometheus: http://localhost:9090


