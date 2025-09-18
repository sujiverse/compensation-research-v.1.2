# 📁 Obsidian 보상작용 연구 볼트 구조

> **최적화된 지식 네트워크 구축을 위한 체계적 파일 구조**
> **모든 파일은 이 구조를 따라 생성하고 관리합니다**

---

## 🏗️ **전체 폴더 구조**

```
📁 Compensation-Research-Vault/
├── 📁 00-Templates/
│   ├── 📄 5WHY-Analysis-Template.md
│   ├── 📄 Paper-Review-Template.md
│   └── 📄 Compensation-Pattern-Template.md
│
├── 📁 01-Papers/
│   ├── 📁 Hip-Compensation/
│   ├── 📁 Knee-Compensation/
│   ├── 📁 Ankle-Compensation/
│   ├── 📁 Spine-Compensation/
│   └── 📁 Multi-Joint/
│
├── 📁 02-Anatomy/
│   ├── 📁 Muscles/
│   ├── 📁 Joints/
│   ├── 📁 Fascial-Chains/
│   └── 📁 Neural-Control/
│
├── 📁 03-Compensation-Patterns/
│   ├── 📁 Primary-Patterns/
│   ├── 📁 Secondary-Adaptations/
│   └── 📁 Complex-Chains/
│
├── 📁 04-Clinical-Tests/
│   ├── 📁 Movement-Screens/
│   ├── 📁 Muscle-Tests/
│   └── 📁 Functional-Assessments/
│
├── 📁 05-Interventions/
│   ├── 📁 Exercise-Protocols/
│   ├── 📁 Manual-Therapy/
│   └── 📁 Movement-Retraining/
│
├── 📁 06-Mechanisms/
│   ├── 📁 Neurological/
│   ├── 📁 Biomechanical/
│   └── 📁 Physiological/
│
├── 📁 07-Graphs/
│   ├── 📄 Muscle-Network.md
│   ├── 📄 Pattern-Connections.md
│   └── 📄 Treatment-Pathways.md
│
└── 📁 08-Meta/
    ├── 📄 Research-Dashboard.md
    ├── 📄 Quality-Metrics.md
    └── 📄 Development-Log.md
```

---

## 📄 **파일 명명 규칙**

### **논문 파일**
```
Format: [First-Author-Year]-[Key-Finding]-[Body-Region].md
Examples:
- Neumann-2010-Gluteus-Medius-Weakness-Hip.md
- Page-2010-Hip-Knee-Compensation-Chain.md
- Fredericson-2000-ITB-Syndrome-TFL-Overactivity.md
```

### **해부학 파일**
```
Format: [Structure-Type]-[Specific-Name].md
Examples:
- Muscle-Gluteus-Medius.md
- Joint-Hip-Complex.md
- Chain-Posterior-Oblique.md
```

### **보상 패턴 파일**
```
Format: [Primary-Dysfunction]-to-[Compensation].md
Examples:
- Glut-Med-Weakness-to-TFL-Overactivity.md
- Tib-Post-Dysfunction-to-Peroneal-Compensation.md
```

---

## 🔗 **링크 연결 시스템**

### **기본 링크 문법**
```markdown
# 일반 링크
[[파일명]]

# 별칭 링크
[[파일명|표시할 제목]]

# 헤더 링크
[[파일명#헤더명]]

# 블록 링크
[[파일명^블록ID]]
```

### **보상작용 특화 링크 태그**
```markdown
# 근육 연결
[[Muscle::Gluteus-Medius]]

# 보상 패턴
[[Pattern::Hip-Hiking]]

# 치료법
[[Treatment::Hip-Strengthening]]

# 평가법
[[Assessment::Trendelenburg-Test]]

# 기전
[[Mechanism::Neural-Inhibition]]
```

---

## 🏷️ **태그 시스템**

### **주요 태그 카테고리**
```yaml
# 연구 유형
#systematic-review
#rct
#cohort-study
#cross-sectional
#case-series

# 신체 부위
#hip #knee #ankle #spine #shoulder

# 보상 유형
#weakness #overactivity #substitution #adaptation

# 치료 유형
#exercise #manual-therapy #movement-retraining
#strengthening #stretching #motor-control

# 평가 유형
#emg #motion-analysis #clinical-tests #imaging

# 품질 지표
#high-quality #moderate-quality #preliminary
#gold-standard #evidence-based
```

### **복합 태그 사용**
```markdown
#hip/compensation #glut-med/weakness #tfl/overactivity
#exercise/strengthening #assessment/functional
#mechanism/neural #outcome/positive
```

---

## 📊 **메타데이터 템플릿**

### **논문 메타데이터**
```yaml
---
title: "논문 제목"
authors: ["First Author", "Second Author"]
journal: "Journal Name"
year: 2023
doi: "10.xxxx/xxxx"
study_type: "RCT"
sample_size: 50
quality_score: 8
body_region: ["hip", "knee"]
compensation_type: ["weakness", "overactivity"]
assessment_methods: ["EMG", "3D motion"]
interventions: ["exercise", "manual therapy"]
key_findings: ["Gluteus medius weakness", "TFL compensation"]
clinical_significance: "High"
obsidian_created: "2024-01-01"
last_updated: "2024-01-01"
---
```

### **보상 패턴 메타데이터**
```yaml
---
pattern_name: "Gluteus Medius Weakness Pattern"
primary_dysfunction: "Gluteus Medius Weakness"
compensatory_muscles: ["TFL", "Hip Adductors", "QL"]
affected_joints: ["Hip", "Knee", "SI Joint"]
movement_affected: ["Walking", "Single leg stance", "Lateral movements"]
assessment_tests: ["Trendelenburg", "Single leg squat", "Step down"]
treatment_priority: ["Glut med strengthening", "TFL stretching", "Motor control"]
prognosis: "Good with appropriate intervention"
prevention_strategies: ["Hip strengthening", "Movement education"]
related_conditions: ["PFPS", "IT Band Syndrome", "Low back pain"]
evidence_level: "Strong"
clinical_frequency: "Very Common"
---
```

---

## 🎯 **템플릿 활용 가이드**

### **새 논문 분석 시**
1. `00-Templates/Paper-Review-Template.md` 복사
2. 적절한 폴더에 이름 변경하여 저장
3. 메타데이터 작성
4. 5WHY 분석 수행
5. 관련 노드들과 링크 연결

### **새 보상 패턴 발견 시**
1. `00-Templates/Compensation-Pattern-Template.md` 사용
2. 해당 카테고리 폴더에 저장
3. 관련 논문들과 양방향 링크 설정
4. 치료 프로토콜과 연결

### **정기 검토 시**
1. `08-Meta/Research-Dashboard.md`에서 전체 현황 확인
2. 연결이 부족한 노드 식별
3. 품질이 낮은 분석 개선
4. 새로운 패턴 발견 여부 검토

---

## 🔍 **검색 최적화**

### **효과적인 검색 쿼리**
```
# 특정 근육 관련 모든 내용
"Gluteus Medius" OR "Glut Med" tag:#hip

# 보상 패턴 검색
tag:#compensation tag:#overactivity

# 치료법 검색
tag:#exercise path:"05-Interventions"

# 고품질 연구만
tag:#high-quality tag:#rct

# 최근 분석 내용
created:2024-01-01..2024-12-31
```

### **유용한 쿼리 저장**
- Saved Searches 플러그인 활용
- 자주 사용하는 검색어 북마크
- 복잡한 쿼리는 별도 노트에 정리

---

## 📈 **그래프 뷰 최적화**

### **그래프 필터 설정**
```
# 핵심 노드만 표시
tag:#high-quality OR tag:#key-concept

# 특정 주제 네트워크
path:"03-Compensation-Patterns" OR path:"01-Papers"

# 치료 관련 연결
tag:#treatment OR tag:#intervention
```

### **색상 코딩**
- **빨간색**: 기본 기능장애 (Primary Dysfunction)
- **주황색**: 보상 패턴 (Compensation Patterns)
- **파란색**: 치료법 (Interventions)
- **초록색**: 평가법 (Assessments)
- **보라색**: 해부학적 구조 (Anatomy)

---

**💡 이 구조를 따라 체계적으로 지식을 축적하면, 보상작용에 대한 종합적이고 실용적인 임상 데이터베이스가 구축됩니다.**