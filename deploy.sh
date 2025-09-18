#!/bin/bash

# 🚀 Compensation Research System - GitHub 배포 스크립트
# Claude Development Rules 준수하여 생성

echo "🔬 Starting Compensation Research System Deployment..."
echo "=================================================="

# 1. Git 저장소 초기화
echo "📁 Initializing Git repository..."
if [ ! -d ".git" ]; then
    git init
    echo "   ✅ Git repository initialized"
else
    echo "   ℹ️  Git repository already exists"
fi

# 2. 기본 설정
echo "⚙️  Configuring Git settings..."
git config --local user.name "Compensation Research Bot"
git config --local user.email "research@compensation.ai"

# 3. 첫 번째 커밋 생성
echo "📝 Creating initial commit..."
git add .
git commit -m "🎉 Initial compensation research system setup

- 5WHY methodology implementation
- Paper screening with OpenAlex integration
- Node connection system for compensation patterns
- Obsidian vault auto-generation
- GitHub Actions automation ready

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>" || echo "   ℹ️  No changes to commit"

# 4. GitHub 저장소 생성 (gh CLI 필요)
echo "🌐 Creating GitHub repository..."
read -p "Enter repository name (default: compensation-research): " REPO_NAME
REPO_NAME=${REPO_NAME:-compensation-research}

if command -v gh &> /dev/null; then
    gh repo create $REPO_NAME --public --description "Automated compensation research system with 5WHY methodology" --add-readme=false
    echo "   ✅ GitHub repository created: $REPO_NAME"

    # 원격 저장소 추가
    git remote add origin https://github.com/$(gh auth status 2>&1 | grep -o 'Logged in to github.com as [^[:space:]]*' | cut -d' ' -f6)/$REPO_NAME.git

else
    echo "   ⚠️  GitHub CLI not found. Please:"
    echo "      1. Install gh CLI: https://cli.github.com/"
    echo "      2. Create repository manually at github.com"
    echo "      3. Add remote: git remote add origin <your-repo-url>"
fi

# 5. 메인 브랜치로 푸시
echo "🚀 Pushing to GitHub..."
git branch -M main

if git remote get-url origin &> /dev/null; then
    git push -u origin main
    echo "   ✅ Code pushed to GitHub"
else
    echo "   ⚠️  Remote origin not set. Add it manually and push:"
    echo "      git remote add origin <your-repo-url>"
    echo "      git push -u origin main"
fi

# 6. GitHub Actions 설정 안내
echo ""
echo "⚙️  GitHub Actions Setup Instructions:"
echo "=================================================="
echo "1. Go to your repository on GitHub"
echo "2. Navigate to Settings → Actions → General"
echo "3. Under 'Workflow permissions':"
echo "   - Select 'Read and write permissions'"
echo "   - Check 'Allow GitHub Actions to create and approve pull requests'"
echo "4. Go to Actions tab and enable workflows"
echo ""

# 7. 배포 완료 메시지
echo "🎉 Deployment Setup Complete!"
echo "=================================================="
echo "Repository: https://github.com/$(git config user.name)/$REPO_NAME"
echo "Actions: Will run every 5 minutes automatically"
echo "Vault: Will be generated at 'Compensation-Research-Vault/'"
echo ""
echo "Next steps:"
echo "✅ 1. Enable GitHub Actions in repository settings"
echo "✅ 2. Check Actions tab for first workflow run"
echo "✅ 3. Monitor Research Dashboard updates"
echo "✅ 4. Download Obsidian vault artifacts"
echo ""

# 8. 테스트 실행 제안
echo "🧪 Test the system locally first?"
read -p "Run integration test now? (y/n): " RUN_TEST

if [[ $RUN_TEST =~ ^[Yy]$ ]]; then
    echo "🔬 Running integration test..."
    python test_integration.py
fi

echo ""
echo "🚀 System ready for automated compensation research!"
echo "   Focus: 5WHY methodology for compensation mechanisms"
echo "   Schedule: Every 5-10 minutes via GitHub Actions"
echo "   Output: Structured Obsidian knowledge vault"
echo "=================================================="