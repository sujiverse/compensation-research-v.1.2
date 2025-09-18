# 🔬 Compensation Research Automation System

> **5WHY 방법론 기반 보상작용 연구 자동화 시스템**
>
> 매 10분마다 고품질 논문을 수집하고 5WHY 분석을 통해 보상 메커니즘을 탐구하며 Obsidian 볼트로 구조화된 지식 네트워크를 구축합니다.

[![Research Automation](https://github.com/your-username/compensation-research/actions/workflows/compensation-research.yml/badge.svg)](https://github.com/your-username/compensation-research/actions/workflows/compensation-research.yml)

## 🎯 시스템 개요

이 시스템은 **Claude Development Rules**에 따라 설계된 완전 자동화된 연구 시스템입니다:

- **📚 논문 스크리닝**: OpenAlex API를 통한 보상작용 특화 논문 수집
- **🔍 5WHY 분석**: 보상 메커니즘의 근본 원인 추적
- **🕸️ 노드 연결**: 해부학적/기능적/치료적 관계 매핑
- **📝 Obsidian 볼트**: 구조화된 지식 베이스 자동 생성

## 🚀 GitHub 배포 방법

### 1. 저장소 생성 및 설정

```bash
# 1. 새 GitHub 저장소 생성
gh repo create compensation-research --public

# 2. 로컬 저장소 초기화
git init
git remote add origin https://github.com/your-username/compensation-research.git

# 3. 파일 추가 및 커밋
git add .
git commit -m "🎉 Initial compensation research system setup"

# 4. 메인 브랜치로 푸시
git branch -M main
git push -u origin main
```

### 2. GitHub Actions 권한 설정

Repository → Settings → Actions → General:
- **Workflow permissions**: "Read and write permissions" 선택
- **Allow GitHub Actions to create and approve pull requests** 체크

### 3. 자동화 실행 확인

- **Actions** 탭에서 워크플로우 상태 확인
- 5분마다 자동 실행 (GitHub의 최소 간격)
- 수동 실행: Actions → "Run workflow" 버튼

## 📁 시스템 구조

```
compensation-research/
├── .github/workflows/
│   └── compensation-research.yml    # GitHub Actions 워크플로우
├── paper_screener.py               # 논문 스크리닝 시스템
├── why_analyzer.py                 # 5WHY 분석 엔진
├── node_connector.py               # 노드 연결 시스템
├── obsidian_generator.py           # Obsidian 볼트 생성기
├── compensation_research_system.py # 통합 시스템
├── test_integration.py             # 통합 테스트
└── Compensation-Research-Vault/    # 생성된 Obsidian 볼트
    ├── 00-Templates/
    ├── 01-Papers/
    ├── 02-Anatomy/
    ├── 03-Compensation-Patterns/
    ├── 04-Clinical-Tests/
    ├── 05-Interventions/
    ├── 06-Mechanisms/
    ├── 07-Graphs/
    └── 08-Meta/
```

## 🔧 로컬 실행 방법

### 환경 설정
```bash
# Python 가상환경 생성
python -m venv research_env
source research_env/bin/activate  # Windows: research_env\Scripts\activate

# 의존성 설치
pip install requests unidecode schedule
```

### 실행 옵션
```bash
# 단일 사이클 실행
python compensation_research_system.py --single

# 자동화 모드 (10분마다)
python compensation_research_system.py

# 테스트 모드
python compensation_research_system.py --test
```

## 📊 시스템 모니터링

### GitHub Actions 상태
- **성공**: 🟢 새로운 논문 분석 및 볼트 업데이트
- **실패**: 🔴 API 제한 또는 분석 오류
- **스킵**: 🟡 새로운 고품질 논문 없음

### 생성된 콘텐츠
- **논문 분석 파일**: `01-Papers/[Body-Region]/[Author-Year].md`
- **보상 패턴**: `03-Compensation-Patterns/[Pattern-Name].md`
- **네트워크 연결**: `07-Graphs/Compensation-Network-[Date].md`
- **대시보드**: `08-Meta/Research-Dashboard.md`

## 🎛️ 설정 커스터마이징

### 논문 스크리닝 조정
```python
# paper_screener.py
self.quality_journals = {
    "Physical Therapy": 4.5,
    # 추가 저널 설정...
}
```

### 5WHY 분석 깊이 조정
```python
# why_analyzer.py
# WHY 레벨 수정 또는 질문 템플릿 변경
```

### 실행 간격 변경
```yaml
# .github/workflows/compensation-research.yml
on:
  schedule:
    - cron: '*/30 * * * *'  # 30분마다로 변경
```

## 📈 성능 메트릭

| 메트릭 | 목표 | 현재 상태 |
|--------|------|-----------|
| 논문 품질 점수 | >8.0/20 | ✅ 달성 |
| 5WHY 완성도 | 5단계 완료 | ✅ 달성 |
| 노드 연결 밀도 | >2.0 | 🔄 개선 중 |
| 볼트 구조 준수 | 100% | ✅ 달성 |

## 🔒 보안 및 API 제한

- **OpenAlex API**: 무료, 제한 없음 (예의 있는 사용)
- **GitHub Actions**: 2000분/월 무료 (퍼블릭 저장소)
- **데이터 저장**: GitHub 저장소 (1GB 제한)

## 🛠️ 문제 해결

### 일반적인 문제
1. **API 응답 없음**: 네트워크 연결 확인
2. **모듈 임포트 오류**: 의존성 재설치
3. **Git 커밋 실패**: 권한 설정 확인

### 디버깅 모드
```bash
python test_integration.py  # 전체 시스템 테스트
```

## 📚 추가 자료

- [5WHY 방법론](./5WHY-Template.md)
- [Obsidian 구조](./Obsidian-Structure.md)
- [개발 규칙](./CLAUDE_DEVELOPMENT_RULES.md)

---

**🤖 Claude Development Rules 준수하에 자동 생성됨**

*마지막 업데이트: 2025-09-18*