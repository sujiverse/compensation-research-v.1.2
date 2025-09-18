# -*- coding: utf-8 -*-
"""
보상작용 연구 자동화 시스템 - 5WHY 분석 엔진
Claude Development Rules 준수하여 개발

핵심 기능:
1. 논문 내용에서 5WHY 분석 수행
2. 보상작용 메커니즘 추출
3. 임상적 의미 도출
4. 치료 우선순위 결정
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

class CompensationType(Enum):
    WEAKNESS = "weakness"
    OVERACTIVITY = "overactivity"
    SUBSTITUTION = "substitution"
    ADAPTATION = "adaptation"

class CompensationStage(Enum):
    ACUTE = "acute"
    CHRONIC = "chronic"
    COMPENSATED = "compensated"

class Reversibility(Enum):
    REVERSIBLE = "reversible"
    PARTIALLY_REVERSIBLE = "partially_reversible"
    FIXED = "fixed"

@dataclass
class WhyLevel:
    level: int
    question: str
    findings: List[str]
    mechanisms: List[str]
    evidence_strength: float

@dataclass
class CompensationPattern:
    primary_dysfunction: str
    compensatory_muscles: List[str]
    affected_joints: List[str]
    compensation_type: CompensationType
    stage: CompensationStage
    reversibility: Reversibility
    clinical_tests: List[str]
    treatment_priority: List[str]

@dataclass
class FiveWhyAnalysis:
    paper_title: str
    why_levels: List[WhyLevel]
    compensation_pattern: CompensationPattern
    clinical_significance: str
    key_message: str
    treatment_keypoints: List[str]

class CompensationWhyAnalyzer:
    def __init__(self):
        # 5WHY 질문 템플릿
        self.why_questions = {
            1: "왜 이 통증/기능장애가 발생했는가?",
            2: "왜 특정 근육이 약화/과활성화되었는가?",
            3: "왜 근육 불균형이 생겼는가?",
            4: "왜 보상 패턴이 형성되었는가?",
            5: "왜 이 보상이 고착화되었는가?"
        }

        # 보상작용 키워드 패턴
        self.compensation_patterns = {
            "gluteus_medius_weakness": {
                "primary": ["gluteus medius weakness", "glut med weakness", "hip abductor weakness"],
                "compensatory": ["tensor fasciae latae", "tfl", "hip adductor", "quadratus lumborum"],
                "joints": ["hip", "knee", "si joint"],
                "tests": ["trendelenburg", "single leg squat", "step down test"]
            },
            "serratus_anterior_dysfunction": {
                "primary": ["serratus anterior dysfunction", "serratus weakness"],
                "compensatory": ["upper trapezius", "levator scapulae", "rhomboids"],
                "joints": ["scapulothoracic", "glenohumeral"],
                "tests": ["wall push-up", "scapular dyskinesis test"]
            },
            "tibialis_posterior_dysfunction": {
                "primary": ["tibialis posterior dysfunction", "tib post dysfunction"],
                "compensatory": ["peroneal", "gastrocnemius", "hip adductor"],
                "joints": ["ankle", "subtalar", "hip"],
                "tests": ["single heel raise", "too many toes sign"]
            }
        }

        # 임상적 의미 키워드
        self.clinical_keywords = {
            "diagnosis": ["differential diagnosis", "clinical presentation", "assessment"],
            "treatment": ["intervention", "therapy", "exercise", "strengthening", "stretching"],
            "prognosis": ["outcome", "recovery", "improvement", "success rate"],
            "prevention": ["risk factor", "prevention", "screening", "early detection"]
        }

    def analyze_paper(self, paper_data: Dict) -> FiveWhyAnalysis:
        """논문 데이터를 5WHY 분석"""
        title = paper_data.get("display_name", "")
        abstract = self._restore_abstract(paper_data.get("abstract_inverted_index", {}))

        # 추가 텍스트가 있다면 활용 (PDF 내용 등)
        full_text = paper_data.get("full_text", "")
        combined_text = f"{title}\n{abstract}\n{full_text}"

        # 5WHY 분석 수행
        why_levels = self._perform_five_why_analysis(combined_text)

        # 보상 패턴 식별
        compensation_pattern = self._identify_compensation_pattern(combined_text)

        # 임상적 의미 추출
        clinical_significance = self._extract_clinical_significance(combined_text)

        # 핵심 메시지 생성
        key_message = self._generate_key_message(why_levels, compensation_pattern)

        # 치료 키포인트 추출
        treatment_keypoints = self._extract_treatment_keypoints(combined_text, compensation_pattern)

        return FiveWhyAnalysis(
            paper_title=title,
            why_levels=why_levels,
            compensation_pattern=compensation_pattern,
            clinical_significance=clinical_significance,
            key_message=key_message,
            treatment_keypoints=treatment_keypoints
        )

    def _perform_five_why_analysis(self, text: str) -> List[WhyLevel]:
        """5단계 WHY 분석 수행"""
        why_levels = []
        text_lower = text.lower()

        # 1차 WHY: 왜 이 통증/기능장애가 발생했는가?
        level1_findings = self._extract_level1_findings(text_lower)
        level1_mechanisms = self._extract_level1_mechanisms(text_lower)
        why_levels.append(WhyLevel(
            level=1,
            question=self.why_questions[1],
            findings=level1_findings,
            mechanisms=level1_mechanisms,
            evidence_strength=self._calculate_evidence_strength(level1_findings, text_lower)
        ))

        # 2차 WHY: 왜 특정 근육이 약화/과활성화되었는가?
        level2_findings = self._extract_level2_findings(text_lower)
        level2_mechanisms = self._extract_level2_mechanisms(text_lower)
        why_levels.append(WhyLevel(
            level=2,
            question=self.why_questions[2],
            findings=level2_findings,
            mechanisms=level2_mechanisms,
            evidence_strength=self._calculate_evidence_strength(level2_findings, text_lower)
        ))

        # 3차 WHY: 왜 근육 불균형이 생겼는가?
        level3_findings = self._extract_level3_findings(text_lower)
        level3_mechanisms = self._extract_level3_mechanisms(text_lower)
        why_levels.append(WhyLevel(
            level=3,
            question=self.why_questions[3],
            findings=level3_findings,
            mechanisms=level3_mechanisms,
            evidence_strength=self._calculate_evidence_strength(level3_findings, text_lower)
        ))

        # 4차 WHY: 왜 보상 패턴이 형성되었는가?
        level4_findings = self._extract_level4_findings(text_lower)
        level4_mechanisms = self._extract_level4_mechanisms(text_lower)
        why_levels.append(WhyLevel(
            level=4,
            question=self.why_questions[4],
            findings=level4_findings,
            mechanisms=level4_mechanisms,
            evidence_strength=self._calculate_evidence_strength(level4_findings, text_lower)
        ))

        # 5차 WHY: 왜 이 보상이 고착화되었는가?
        level5_findings = self._extract_level5_findings(text_lower)
        level5_mechanisms = self._extract_level5_mechanisms(text_lower)
        why_levels.append(WhyLevel(
            level=5,
            question=self.why_questions[5],
            findings=level5_findings,
            mechanisms=level5_mechanisms,
            evidence_strength=self._calculate_evidence_strength(level5_findings, text_lower)
        ))

        return why_levels

    def _extract_level1_findings(self, text: str) -> List[str]:
        """1차 WHY: 관찰된 현상과 직접적 원인"""
        findings = []

        # 통증 패턴
        pain_patterns = [
            r"(\w+\s+pain)", r"pain in (\w+)", r"(\w+\s+discomfort)",
            r"(\w+\s+dysfunction)", r"dysfunction of (\w+)"
        ]

        for pattern in pain_patterns:
            matches = re.findall(pattern, text)
            findings.extend([f"Observed: {match}" for match in matches if match])

        # 기능 제한
        function_patterns = [
            r"reduced (\w+)", r"decreased (\w+)", r"impaired (\w+)",
            r"limited (\w+)", r"restricted (\w+)"
        ]

        for pattern in function_patterns:
            matches = re.findall(pattern, text)
            findings.extend([f"Functional limitation: {match}" for match in matches if match])

        return findings[:5]  # 상위 5개만

    def _extract_level2_findings(self, text: str) -> List[str]:
        """2차 WHY: 근육 불균형 패턴"""
        findings = []

        # 약화된 근육
        weakness_patterns = [
            r"(\w+\s+weakness)", r"weak (\w+)", r"(\w+\s+inhibition)",
            r"reduced (\w+\s+strength)", r"(\w+\s+atrophy)"
        ]

        for pattern in weakness_patterns:
            matches = re.findall(pattern, text)
            findings.extend([f"Weakness: {match}" for match in matches if match])

        # 과활성 근육
        overactivity_patterns = [
            r"(\w+\s+overactivity)", r"(\w+\s+dominance)", r"(\w+\s+tightness)",
            r"increased (\w+\s+activity)", r"(\w+\s+hyperactivity)"
        ]

        for pattern in overactivity_patterns:
            matches = re.findall(pattern, text)
            findings.extend([f"Overactivity: {match}" for match in matches if match])

        return findings[:5]

    def _extract_level3_findings(self, text: str) -> List[str]:
        """3차 WHY: 근육 불균형의 원인"""
        findings = []

        # 구조적 요인
        structural_patterns = [
            r"(\w+\s+injury)", r"previous (\w+)", r"(\w+\s+trauma)",
            r"anatomical (\w+)", r"structural (\w+)"
        ]

        for pattern in structural_patterns:
            matches = re.findall(pattern, text)
            findings.extend([f"Structural factor: {match}" for match in matches if match])

        # 기능적 요인
        functional_patterns = [
            r"(\w+\s+posture)", r"repetitive (\w+)", r"prolonged (\w+)",
            r"habitual (\w+)", r"occupational (\w+)"
        ]

        for pattern in functional_patterns:
            matches = re.findall(pattern, text)
            findings.extend([f"Functional factor: {match}" for match in matches if match])

        return findings[:5]

    def _extract_level4_findings(self, text: str) -> List[str]:
        """4차 WHY: 보상 패턴 형성 원인"""
        findings = []

        # 신경계 적응
        neural_patterns = [
            r"motor (\w+)", r"neural (\w+)", r"(\w+\s+adaptation)",
            r"central (\w+)", r"cortical (\w+)"
        ]

        for pattern in neural_patterns:
            matches = re.findall(pattern, text)
            findings.extend([f"Neural adaptation: {match}" for match in matches if match])

        # 역학적 적응
        mechanical_patterns = [
            r"mechanical (\w+)", r"biomechanical (\w+)", r"kinematic (\w+)",
            r"force (\w+)", r"load (\w+)"
        ]

        for pattern in mechanical_patterns:
            matches = re.findall(pattern, text)
            findings.extend([f"Mechanical adaptation: {match}" for match in matches if match])

        return findings[:5]

    def _extract_level5_findings(self, text: str) -> List[str]:
        """5차 WHY: 보상 고착화 원인"""
        findings = []

        # 학습된 패턴
        learning_patterns = [
            r"motor (\w+)", r"learned (\w+)", r"habitual (\w+)",
            r"automatic (\w+)", r"programmed (\w+)"
        ]

        for pattern in learning_patterns:
            matches = re.findall(pattern, text)
            findings.extend([f"Learned pattern: {match}" for match in matches if match])

        # 구조적 변화
        structural_change_patterns = [
            r"tissue (\w+)", r"fascial (\w+)", r"joint (\w+)",
            r"length (\w+)", r"stiffness (\w+)"
        ]

        for pattern in structural_change_patterns:
            matches = re.findall(pattern, text)
            findings.extend([f"Structural change: {match}" for match in matches if match])

        return findings[:5]

    def _extract_level1_mechanisms(self, text: str) -> List[str]:
        return self._extract_mechanisms(text, ["acute", "onset", "initial", "primary"])

    def _extract_level2_mechanisms(self, text: str) -> List[str]:
        return self._extract_mechanisms(text, ["inhibition", "facilitation", "imbalance", "asymmetry"])

    def _extract_level3_mechanisms(self, text: str) -> List[str]:
        return self._extract_mechanisms(text, ["predisposing", "risk factor", "etiology", "cause"])

    def _extract_level4_mechanisms(self, text: str) -> List[str]:
        return self._extract_mechanisms(text, ["compensation", "adaptation", "strategy", "substitution"])

    def _extract_level5_mechanisms(self, text: str) -> List[str]:
        return self._extract_mechanisms(text, ["plasticity", "chronic", "persistent", "maladaptive"])

    def _extract_mechanisms(self, text: str, keywords: List[str]) -> List[str]:
        """키워드 기반 메커니즘 추출"""
        mechanisms = []
        sentences = re.split(r'[.!?]+', text)

        for sentence in sentences:
            for keyword in keywords:
                if keyword in sentence.lower():
                    mechanisms.append(sentence.strip())
                    break

        return mechanisms[:3]  # 상위 3개만

    def _calculate_evidence_strength(self, findings: List[str], text: str) -> float:
        """증거 강도 계산"""
        if not findings:
            return 0.0

        evidence_indicators = ["significant", "p <", "correlation", "association", "effect"]
        evidence_count = sum(1 for indicator in evidence_indicators if indicator in text)

        return min(evidence_count / len(evidence_indicators), 1.0)

    def _identify_compensation_pattern(self, text: str) -> CompensationPattern:
        """보상 패턴 식별"""
        text_lower = text.lower()

        # 기본값
        primary_dysfunction = "Unknown dysfunction"
        compensatory_muscles = []
        affected_joints = []
        compensation_type = CompensationType.SUBSTITUTION
        stage = CompensationStage.CHRONIC
        reversibility = Reversibility.PARTIALLY_REVERSIBLE
        clinical_tests = []
        treatment_priority = []

        # 알려진 패턴과 매칭
        for pattern_name, pattern_data in self.compensation_patterns.items():
            for primary_keyword in pattern_data["primary"]:
                if primary_keyword in text_lower:
                    primary_dysfunction = primary_keyword.title()
                    compensatory_muscles = pattern_data["compensatory"]
                    affected_joints = pattern_data["joints"]
                    clinical_tests = pattern_data["tests"]
                    break

        # 보상 유형 결정
        if "weakness" in text_lower:
            compensation_type = CompensationType.WEAKNESS
        elif "overactivity" in text_lower or "dominance" in text_lower:
            compensation_type = CompensationType.OVERACTIVITY
        elif "substitution" in text_lower:
            compensation_type = CompensationType.SUBSTITUTION
        elif "adaptation" in text_lower:
            compensation_type = CompensationType.ADAPTATION

        # 단계 결정
        if "acute" in text_lower:
            stage = CompensationStage.ACUTE
        elif "chronic" in text_lower:
            stage = CompensationStage.CHRONIC
        else:
            stage = CompensationStage.COMPENSATED

        # 가역성 결정
        if "reversible" in text_lower or "recovery" in text_lower:
            reversibility = Reversibility.REVERSIBLE
        elif "fixed" in text_lower or "permanent" in text_lower:
            reversibility = Reversibility.FIXED

        # 치료 우선순위
        if "strengthening" in text_lower:
            treatment_priority.append("Strengthening weak muscles")
        if "stretching" in text_lower:
            treatment_priority.append("Stretching tight structures")
        if "motor control" in text_lower:
            treatment_priority.append("Motor control retraining")

        return CompensationPattern(
            primary_dysfunction=primary_dysfunction,
            compensatory_muscles=compensatory_muscles,
            affected_joints=affected_joints,
            compensation_type=compensation_type,
            stage=stage,
            reversibility=reversibility,
            clinical_tests=clinical_tests,
            treatment_priority=treatment_priority
        )

    def _extract_clinical_significance(self, text: str) -> str:
        """임상적 의미 추출"""
        significance_sentences = []
        sentences = re.split(r'[.!?]+', text)

        significance_keywords = [
            "clinical", "therapeutic", "treatment", "intervention",
            "rehabilitation", "management", "assessment", "diagnosis"
        ]

        for sentence in sentences:
            if any(keyword in sentence.lower() for keyword in significance_keywords):
                significance_sentences.append(sentence.strip())

        if significance_sentences:
            return ". ".join(significance_sentences[:2])  # 상위 2개 문장
        return "Clinical significance not clearly identified."

    def _generate_key_message(self, why_levels: List[WhyLevel], pattern: CompensationPattern) -> str:
        """핵심 메시지 생성"""
        if pattern.primary_dysfunction != "Unknown dysfunction":
            return f"{pattern.primary_dysfunction} leads to {pattern.compensation_type.value} " \
                   f"compensation pattern affecting {', '.join(pattern.affected_joints)} joints."

        # 기본 메시지
        strongest_level = max(why_levels, key=lambda x: x.evidence_strength) if why_levels else None
        if strongest_level and strongest_level.findings:
            return f"Primary finding: {strongest_level.findings[0]}"

        return "Compensation mechanism requires further analysis."

    def _extract_treatment_keypoints(self, text: str, pattern: CompensationPattern) -> List[str]:
        """치료 키포인트 추출"""
        keypoints = []

        # 패턴 기반 치료
        if pattern.treatment_priority:
            keypoints.extend(pattern.treatment_priority[:2])

        # 텍스트에서 치료법 추출
        treatment_patterns = [
            r"treatment (?:with|using|include[ds]?) ([^.]+)",
            r"intervention (?:with|using|include[ds]?) ([^.]+)",
            r"therapy (?:with|using|include[ds]?) ([^.]+)"
        ]

        for pattern in treatment_patterns:
            matches = re.findall(pattern, text.lower())
            keypoints.extend(matches[:2])

        return keypoints[:3]  # 상위 3개

    def _restore_abstract(self, inverted_index: Dict) -> str:
        """OpenAlex의 inverted index에서 초록 복원"""
        if not inverted_index:
            return ""

        word_positions = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_positions.append((pos, word))

        word_positions.sort()
        return " ".join(word for _, word in word_positions)

def test_why_analyzer():
    """5WHY 분석기 테스트"""
    print("TEST 2/5: 5WHY Analysis Engine Test")
    print("=" * 50)

    analyzer = CompensationWhyAnalyzer()

    # 테스트 논문 데이터 (가상)
    test_paper = {
        "display_name": "Gluteus Medius Weakness and TFL Compensation in Runners",
        "abstract_inverted_index": {
            "Gluteus": [0], "medius": [1], "weakness": [2], "is": [3], "a": [4],
            "common": [5], "cause": [6], "of": [7], "hip": [8], "dysfunction": [9],
            "leading": [10], "to": [11], "tensor": [12], "fasciae": [13], "latae": [14],
            "overactivity": [15], "and": [16], "compensation": [17], "patterns": [18],
            "Clinical": [19], "assessment": [20], "using": [21], "Trendelenburg": [22],
            "test": [23], "showed": [24], "significant": [25], "weakness": [26],
            "Treatment": [27], "with": [28], "strengthening": [29], "exercises": [30],
            "improved": [31], "function": [32]
        },
        "full_text": "This study examined the compensation patterns in runners with gluteus medius weakness. " \
                    "The primary dysfunction was identified as gluteus medius weakness due to " \
                    "motor inhibition following previous injury. This led to tensor fasciae latae " \
                    "overactivity as a compensatory mechanism. The biomechanical adaptation " \
                    "resulted in altered hip kinematics and increased knee valgus. " \
                    "Motor learning theory suggests this pattern becomes fixed through repetition. " \
                    "Clinical tests including Trendelenburg test and single leg squat revealed " \
                    "significant deficits. Treatment should prioritize gluteus medius strengthening " \
                    "followed by motor control retraining."
    }

    # 분석 실행
    analysis = analyzer.analyze_paper(test_paper)

    print(f"Paper Title: {analysis.paper_title}")
    print(f"\nKey Message: {analysis.key_message}")
    print(f"\nClinical Significance: {analysis.clinical_significance}")

    print(f"\n5WHY Analysis:")
    for why_level in analysis.why_levels:
        print(f"\n{why_level.level}. {why_level.question}")
        print(f"   Findings: {', '.join(why_level.findings[:2]) if why_level.findings else 'None'}")
        print(f"   Evidence Strength: {why_level.evidence_strength:.2f}")

    print(f"\nCompensation Pattern:")
    pattern = analysis.compensation_pattern
    print(f"   Primary Dysfunction: {pattern.primary_dysfunction}")
    print(f"   Compensatory Muscles: {', '.join(pattern.compensatory_muscles[:2])}")
    print(f"   Compensation Type: {pattern.compensation_type.value}")
    print(f"   Stage: {pattern.stage.value}")
    print(f"   Reversibility: {pattern.reversibility.value}")

    print(f"\nTreatment Keypoints:")
    for i, keypoint in enumerate(analysis.treatment_keypoints, 1):
        print(f"   {i}. {keypoint}")

    print("\n" + "=" * 50)
    print("TEST 2/5 COMPLETED")
    return True

if __name__ == "__main__":
    test_why_analyzer()