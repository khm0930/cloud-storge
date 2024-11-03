#!/bin/bash

# 자동 푸시 스크립트

# 스크립트를 실행할 때 전달된 커밋 메시지를 변수에 저장
COMMIT_MESSAGE=${1:-"Auto-commit from script"}

# Git 상태 확인
echo "Checking Git status..."
git status

# Git 추가 (변경된 모든 파일 스테이징)
echo "Staging files..."
git add .

# 커밋
echo "Committing changes..."
git commit -m "$COMMIT_MESSAGE"

# 원격 저장소에 푸시
echo "Pushing to remote repository..."
git push origin main  # 필요에 따라 'main'을 다른 브랜치 이름으로 변경

# 완료 메시지
echo "Push completed successfully."
