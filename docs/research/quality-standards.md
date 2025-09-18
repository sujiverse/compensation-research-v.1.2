# 📏 Paper Quality Standards

> **Rigorous criteria for evaluating compensation research papers in our automated analysis system**

## 🎯 Overview

This document establishes the evidence-based quality standards used by our paper screening algorithm to identify high-quality compensation research. Each paper undergoes three-stage filtering to ensure clinical relevance and methodological rigor.

## 🔍 Three-Stage Filtering Process

### **Stage 1: Field Specialization Filter (0-18 points)**

**Journal Impact & Relevance (0-10 points)**
```yaml
High-Impact Journals (8-10 points):
  - Physical Therapy (Impact Factor 3.9)
  - Journal of Orthopaedic & Sports Physical Therapy (4.4)
  - Clinical Biomechanics (2.1)
  - Gait & Posture (2.4)
  - Journal of Biomechanics (2.4)

Medium-Impact Journals (5-7 points):
  - Manual Therapy (3.3)
  - Physiotherapy Theory and Practice (1.8)
  - Archives of Physical Medicine and Rehabilitation (3.1)
  - Journal of Electromyography and Kinesiology (2.4)

Lower-Impact but Relevant (2-4 points):
  - International Journal of Sports Physical Therapy
  - Physiotherapy Canada
  - Journal of Manual & Manipulative Therapy
```

**Compensation Keywords (0-5 points)**
```yaml
Primary Keywords (5 points):
  - "compensation pattern"
  - "compensatory movement"
  - "movement dysfunction"
  - "motor substitution"
  - "biomechanical adaptation"

Secondary Keywords (3 points):
  - "muscle substitution"
  - "altered movement pattern"
  - "functional compensation"
  - "postural adaptation"
  - "kinematic compensation"

Tertiary Keywords (1 point):
  - "movement analysis"
  - "motor control"
  - "neuromuscular adaptation"
```

**Anatomical Relevance (0-3 points)**
```yaml
High Relevance (3 points):
  - Hip abductor dysfunction
  - Gluteus medius weakness
  - Scapular dyskinesis
  - Core stability deficits

Medium Relevance (2 points):
  - Shoulder impingement
  - Low back pain
  - Knee valgus patterns
  - Ankle instability

General Relevance (1 point):
  - General musculoskeletal dysfunction
  - Movement screening
  - Exercise therapy
```

**Exclusion Penalties (-2 points each)**
```yaml
Automatic Exclusions:
  - "surgical intervention" (primary focus)
  - "pharmaceutical treatment"
  - "case report" (unless exceptional)
  - "editorial" or "commentary"
  - "animal study"
  - "cadaveric study"
```

### **Stage 2: Research Quality Filter (0-28 points)**

**Study Design Hierarchy (1-10 points)**
```yaml
Gold Standard (10 points):
  - Randomized Controlled Trial (RCT)
  - Systematic Review with Meta-analysis
  - Crossover Trial

High Quality (7-9 points):
  - Cohort Study (prospective)
  - Case-Control Study
  - Cross-sectional Study (large sample)

Moderate Quality (4-6 points):
  - Case Series (>20 participants)
  - Pilot Studies
  - Feasibility Studies

Lower Quality (1-3 points):
  - Case Series (<20 participants)
  - Case Reports (exceptional cases only)
  - Expert Opinions with data
```

**Sample Size Scoring (0-5 points)**
```yaml
Excellent (5 points): >100 participants
Very Good (4 points): 50-100 participants
Good (3 points): 30-49 participants
Adequate (2 points): 20-29 participants
Limited (1 point): 10-19 participants
Insufficient (0 points): <10 participants
```

**Citation Impact (0-10 points)**
```yaml
Formula: (Citations / Years since publication) * Age Factor

Age Factor:
  - 0-2 years: 1.0
  - 3-5 years: 0.8
  - 6-10 years: 0.6
  - >10 years: 0.4

Scoring Bands:
  - 9-10 points: >20 citations/year
  - 7-8 points: 10-20 citations/year
  - 5-6 points: 5-10 citations/year
  - 3-4 points: 2-5 citations/year
  - 1-2 points: 0.5-2 citations/year
  - 0 points: <0.5 citations/year
```

**Institution & Collaboration (0-3 points)**
```yaml
Multi-center International (3 points):
  - Multiple countries represented
  - >3 institutions involved

Multi-center National (2 points):
  - Multiple institutions, same country
  - University-hospital collaboration

Single Institution (1 point):
  - Established research institution
  - University or major medical center

Independent/Unknown (0 points):
  - Unknown affiliation
  - Non-research institution
```

### **Stage 3: Compensation Relevance Filter (0-30 points)**

**5WHY Analysis Potential (0-8 points)**
```yaml
Excellent (7-8 points):
  - Clear dysfunction-compensation chain described
  - Multiple causal layers identified
  - Mechanism of compensation explained
  - Treatment implications discussed

Good (5-6 points):
  - Basic compensation pattern identified
  - Some causal relationships described
  - Limited mechanistic explanation

Fair (3-4 points):
  - Compensation acknowledged
  - Minimal causal analysis
  - Descriptive rather than explanatory

Poor (0-2 points):
  - No clear compensation focus
  - Purely descriptive
  - No causal reasoning
```

**Assessment Methods Quality (0-6 points)**
```yaml
Gold Standard (6 points):
  - 3D Motion Analysis + EMG
  - Force plates + Kinematic analysis
  - Multiple outcome measures

High Quality (4-5 points):
  - 2D Motion Analysis + Clinical tests
  - EMG + Functional assessment
  - Validated movement screens

Moderate Quality (2-3 points):
  - Clinical assessment tools only
  - Single measurement method
  - Non-validated but reasonable measures

Low Quality (0-1 points):
  - Subjective measures only
  - Non-standardized assessment
  - Inadequate measurement methods
```

**Intervention Relevance (0-6 points)**
```yaml
Highly Relevant (6 points):
  - Compensation-specific interventions
  - Motor control/retraining focus
  - Movement pattern modification

Moderately Relevant (3-4 points):
  - General strengthening with movement focus
  - Manual therapy with movement assessment
  - Exercise therapy with biomechanical rationale

Limited Relevance (1-2 points):
  - General exercise prescription
  - Pain-focused interventions
  - Non-movement based treatments

Not Relevant (0 points):
  - Pharmaceutical interventions
  - Passive treatments only
  - No movement component
```

**Pattern Specificity (0-10 points)**
```yaml
Highly Specific (8-10 points):
  - Detailed compensation pattern description
  - Specific muscle substitution patterns
  - Clear biomechanical explanations
  - Quantitative movement analysis

Moderately Specific (5-7 points):
  - General compensation patterns identified
  - Some biomechanical details
  - Basic quantitative data

Limited Specificity (2-4 points):
  - Vague compensation description
  - Minimal biomechanical detail
  - Primarily qualitative observations

Non-Specific (0-1 points):
  - No specific pattern identification
  - General dysfunction focus
  - No compensation analysis
```

## 📊 Quality Scoring Matrix

### **Total Score Calculation**
```yaml
Maximum Possible Score: 76 points
  - Stage 1 (Field): 18 points
  - Stage 2 (Quality): 28 points
  - Stage 3 (Relevance): 30 points

Quality Tiers:
  - Exceptional (65-76 points): Auto-include, priority analysis
  - High Quality (50-64 points): Include, standard analysis
  - Moderate Quality (35-49 points): Include if resources allow
  - Low Quality (20-34 points): Exclude unless specific relevance
  - Inadequate (<20 points): Automatic exclusion
```

### **Minimum Thresholds**
```yaml
Stage Gate Requirements:
  - Stage 1: ≥8 points (excludes irrelevant papers)
  - Stage 2: ≥12 points (excludes poor quality research)
  - Stage 3: ≥15 points (excludes non-compensation focus)

Individual Minimums:
  - Study Design: ≥4 points (excludes case reports)
  - Sample Size: ≥2 points (excludes studies <20 participants)
  - Assessment Methods: ≥2 points (excludes purely subjective studies)
```

## 🔬 Special Considerations

### **Systematic Reviews & Meta-Analyses**
```yaml
Additional Scoring Criteria:
  - PRISMA compliance: +3 points
  - Risk of bias assessment: +2 points
  - Heterogeneity analysis: +2 points
  - Clinical recommendations: +2 points

Quality Requirements:
  - Must include ≥5 primary studies
  - Clear search strategy documented
  - Inclusion/exclusion criteria explicit
  - Data extraction methodology described
```

### **Pilot Studies & Feasibility Studies**
```yaml
Adjusted Scoring:
  - Sample size requirements relaxed (≥10 participants)
  - Emphasis on methodology description
  - Future study implications weighted higher
  - Preliminary results accepted

Inclusion Criteria:
  - Novel methodology
  - Innovative technology application
  - Unique population study
  - Methodological development focus
```

### **Clinical Practice Papers**
```yaml
Special Considerations:
  - Case series with ≥20 participants eligible
  - Clinical reasoning emphasis valued
  - Real-world applicability weighted
  - Treatment outcomes focus

Quality Indicators:
  - Standardized assessment protocols
  - Objective outcome measures
  - Follow-up data included
  - Clinical significance discussed
```

## 🎯 Output Quality Metrics

### **Analysis Confidence Levels**
```yaml
High Confidence (Score 65-76):
  - 5WHY analysis depth: 4-5 levels
  - Pattern recognition: Detailed
  - Clinical application: Comprehensive
  - Cross-references: Extensive

Medium Confidence (Score 50-64):
  - 5WHY analysis depth: 3-4 levels
  - Pattern recognition: Moderate
  - Clinical application: Standard
  - Cross-references: Good

Lower Confidence (Score 35-49):
  - 5WHY analysis depth: 2-3 levels
  - Pattern recognition: Basic
  - Clinical application: Limited
  - Cross-references: Minimal
```

### **Quality Assurance Checks**
```yaml
Automated Validation:
  - ✅ DOI verification
  - ✅ Author affiliation check
  - ✅ Journal indexing confirmation
  - ✅ Publication date validation

Manual Review Triggers:
  - 🔍 Score 65+ (exceptional quality verification)
  - 🔍 Controversial findings
  - 🔍 Novel methodology
  - 🔍 Contradictory conclusions
```

## 🔗 Integration with 5WHY Analysis

### **Quality Score Impact on Analysis Depth**
```yaml
High Quality Papers (65+):
  - Full 5-level WHY analysis
  - Detailed pattern extraction
  - Comprehensive cross-referencing
  - Clinical pearl identification

Medium Quality Papers (50-64):
  - Standard 4-level WHY analysis
  - Standard pattern extraction
  - Moderate cross-referencing
  - Key point identification

Lower Quality Papers (35-49):
  - Basic 3-level WHY analysis
  - Limited pattern extraction
  - Minimal cross-referencing
  - Summary point extraction
```

---

**📏 These quality standards ensure that our automated compensation research system focuses on the most valuable and clinically relevant scientific evidence for physical therapy and biomechanics practice.**