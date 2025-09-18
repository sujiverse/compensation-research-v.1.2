# 🚀 GitHub 배포 가이드

## 빠른 배포 (원클릭)

```bash
# 배포 스크립트 실행
./deploy.sh
```

## 수동 배포 단계

### 1️⃣ GitHub 저장소 생성

```bash
# GitHub CLI 사용
gh repo create compensation-research --public

# 또는 웹에서 생성: https://github.com/new
```

### 2️⃣ 로컬 Git 설정

```bash
# Git 초기화
git init
git remote add origin https://github.com/your-username/compensation-research.git

# 첫 커밋
git add .
git commit -m "🎉 Initial compensation research system"
git branch -M main
git push -u origin main
```

### 3️⃣ GitHub Actions 활성화

1. **저장소 Settings** → **Actions** → **General**
2. **Workflow permissions**:
   - ✅ "Read and write permissions"
   - ✅ "Allow GitHub Actions to create and approve pull requests"

### 4️⃣ 자동화 확인

- **Actions** 탭에서 워크플로우 실행 확인
- 5분마다 자동 실행
- 수동 실행: "Run workflow" 버튼

## 📊 배포 후 모니터링

### GitHub Actions 상태
```
🟢 성공: 새 논문 분석 완료
🟡 스킵: 신규 고품질 논문 없음
🔴 실패: API 오류 또는 분석 실패
```

### 생성된 아티팩트
- **Obsidian 볼트**: Actions → Artifacts
- **연구 대시보드**: `08-Meta/Research-Dashboard.md`
- **네트워크 그래프**: `07-Graphs/` 폴더

### 실시간 로그 확인
```bash
# GitHub CLI로 워크플로우 로그 확인
gh run list
gh run view <run-id> --log
```

## ⚙️ 고급 설정

### 실행 간격 변경
```yaml
# .github/workflows/compensation-research.yml
on:
  schedule:
    - cron: '*/30 * * * *'  # 30분마다
```

### 논문 필터링 조정
```python
# paper_screener.py에서 임계값 수정
if total_score >= 2.0:  # 더 관대한 필터링
```

### 알림 설정
```yaml
# Slack 알림 추가
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

## 🔒 보안 설정

### Secrets 관리
Repository → Settings → Secrets:
```
OPENAI_API_KEY: (선택사항)
SLACK_WEBHOOK: (알림용)
```

### API 제한 관리
- OpenAlex: 무료, 제한 없음
- GitHub Actions: 2000분/월 (퍼블릭)

## 📈 성능 최적화

### 1. 캐싱 활용
```yaml
- name: Cache dependencies
  uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
```

### 2. 병렬 처리
```python
# 여러 논문 동시 분석
import concurrent.futures
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
    futures = [executor.submit(analyze_paper, paper) for paper in papers]
```

### 3. 증분 처리
```python
# 이미 처리된 논문 스킵
processed_dois = load_processed_papers()
new_papers = [p for p in papers if p.get('doi') not in processed_dois]
```

## 🛠️ 문제 해결

### 일반적인 오류

**1. 워크플로우 권한 오류**
```
Error: Resource not accessible by integration
```
→ Settings → Actions → General → Workflow permissions 확인

**2. 모듈 임포트 오류**
```
ModuleNotFoundError: No module named 'requests'
```
→ `requirements.txt` 파일 생성:
```
requests>=2.31.0
unidecode>=1.3.7
schedule>=1.2.0
```

**3. Git 커밋 실패**
```
nothing to commit, working tree clean
```
→ 정상 동작 (변경사항 없음)

### 디버깅 모드
```bash
# 로컬에서 단일 사이클 테스트
python compensation_research_system.py --single

# 전체 통합 테스트
python test_integration.py
```

## 📊 운영 메트릭

### 성공 지표
- ✅ 논문 수집률: >5개/일
- ✅ 5WHY 완성도: 100%
- ✅ 볼트 구조 준수: 100%
- ✅ 업타임: >95%

### 모니터링 대시보드
```markdown
# 08-Meta/Research-Dashboard.md에서 확인
- 총 논문 수
- 패턴 발견 수
- 네트워크 밀도
- 품질 점수
```

## 🔄 업데이트 및 유지보수

### 시스템 업데이트
```bash
# 새로운 기능 추가 후
git add .
git commit -m "✨ Add new feature"
git push origin main
```

### 정기 점검 (월 1회)
1. API 응답률 확인
2. 논문 품질 검토
3. 볼트 구조 최적화
4. 필터링 임계값 조정

---

**🤖 이 가이드는 Claude Development Rules에 따라 생성되었습니다**

*자동화된 보상작용 연구를 위한 완전한 배포 솔루션*