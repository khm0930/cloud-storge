# 베이스 이미지 선택 (Python 환경 설정)
FROM python:3.8-slim

# 필수 패키지 설치
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    gcc \
    pkg-config \
    libmariadb-dev-compat \
    libmariadb-dev \
    && rm -rf /var/lib/apt/lists/*


# 작업 디렉토리 설정
WORKDIR /app

# 현재 디렉토리의 모든 파일을 컨테이너로 복사
COPY . /app

# 패키지 설치 (requirements.txt에서 종속성 설치)
RUN pip install --no-cache-dir -r requirements.txt


# Nginx 설정 파일 복사 (필요한 경우)
COPY ./nginx.docker.conf /etc/nginx/nginx.conf

# 데이터베이스 마이그레이션 수행 및 정적 파일 수집
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput

# 기본 명령어 설정 (Django 서버 실행)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "cloudserver.wsgi:application"]

EXPOSE 8000
