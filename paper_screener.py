# -*- coding: utf-8 -*-
"""
보상작용 연구 자동화 시스템 - 논문 스크리닝 모듈
Claude Development Rules 준수하여 개발

핵심 기능:
1. OpenAlex API에서 보상작용 관련 논문 검색
2. 3단계 품질 필터링 (분야 특화 → 연구 품질 → 보상작용 관련성)
3. 고품질 논문만 선별하여 반환
"""

import requests
import re
from typing import Dict, List, Optional, Tuple
from datetime import datetime
import time

class CompensationPaperScreener:
    def __init__(self):
        self.api_base = "https://api.openalex.org/works"
        self.headers = {"User-Agent": "Compensation-Research-Bot/1.0 (+compensation@research.edu)"}

        # 보상작용 핵심 키워드 (Claude Rules 기반)
        self.compensation_keywords = [
            "compensation", "compensatory", "overactivity", "substitution",
            "muscle imbalance", "altered kinematics", "movement dysfunction",
            "gait deviation", "postural compensation", "pain adaptation",
            "force redistribution", "load transfer", "kinetic chain"
        ]

        # 해부학적 키워드
        self.anatomy_keywords = [
            "gluteus medius", "tensor fasciae latae", "tfl", "glut med",
            "serratus anterior", "upper trapezius", "tibialis posterior",
            "peroneal", "hip abductor", "scapular dyskinesis"
        ]

        # 고품질 저널 목록
        self.quality_journals = {
            "Physical Therapy": 4.5,
            "Journal of Orthopaedic & Sports Physical Therapy": 3.8,
            "Clinical Biomechanics": 2.8,
            "Gait & Posture": 2.5,
            "Journal of Biomechanics": 2.4,
            "Archives of Physical Medicine and Rehabilitation": 3.2,
            "Manual Therapy": 2.9,
            "Physiotherapy": 2.3,
            "Journal of Electromyography and Kinesiology": 2.1,
            "Human Movement Science": 2.0
        }

    def search_papers(self, limit: int = 50) -> List[Dict]:
        """OpenAlex에서 보상작용 관련 논문 검색"""

        # 검색 쿼리 구성 (보상작용 + 물리치료 + 인체역학)
        query_terms = [
            "compensation AND (physical therapy OR physiotherapy OR rehabilitation)",
            "compensatory AND (biomechanics OR kinesiology)",
            "muscle imbalance AND (movement OR gait)",
            "overactivity AND (weakness OR dysfunction)"
        ]

        search_query = " OR ".join(f"({term})" for term in query_terms)

        params = {
            "search": search_query,
            "filter": [
                "type:article",
                "from_publication_date:2010-01-01",  # 2010년 이후
                "to_publication_date:2024-12-31",
                "cited_by_count:>1"  # 최소 인용 1회 이상으로 완화
            ],
            "sort": "cited_by_count:desc",
            "per_page": min(limit, 200),  # API 제한
            "select": [
                "id", "doi", "title", "display_name",
                "publication_year", "publication_date",
                "primary_location", "open_access",
                "authorships", "institutions_distinct_count",
                "cited_by_count", "counts_by_year",
                "concepts", "keywords",
                "abstract_inverted_index",
                "mesh", "sustainable_development_goals"
            ]
        }

        try:
            response = requests.get(
                self.api_base,
                params=params,
                headers=self.headers,
                timeout=30
            )
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])

        except Exception as e:
            print(f"OpenAlex API 검색 실패: {e}")
            return []

    def filter_by_field_specialization(self, papers: List[Dict]) -> List[Dict]:
        """1차 필터: 분야 특화 필터링"""
        filtered = []

        for paper in papers:
            journal_name = self._get_journal_name(paper)
            abstract = self._restore_abstract(paper.get("abstract_inverted_index", {}))
            title = paper.get("display_name", "").lower()

            # 고품질 저널 체크
            journal_score = 0
            for quality_journal, score in self.quality_journals.items():
                if quality_journal.lower() in journal_name.lower():
                    journal_score = score
                    break

            # 키워드 매칭 체크
            text_to_check = f"{title} {abstract}".lower()

            # 보상작용 키워드 점수
            compensation_score = sum(1 for kw in self.compensation_keywords
                                   if kw.lower() in text_to_check)

            # 해부학적 키워드 점수
            anatomy_score = sum(1 for kw in self.anatomy_keywords
                              if kw.lower() in text_to_check)

            # 제외 키워드 체크 (수술, 약물 위주)
            exclude_keywords = [
                "surgery", "surgical", "operation", "medication",
                "drug", "pharmaceutical", "injection", "arthroscopy"
            ]
            exclude_score = sum(1 for kw in exclude_keywords
                              if kw.lower() in text_to_check)

            # 점수 계산
            total_score = journal_score + compensation_score + anatomy_score - exclude_score

            if total_score >= 1.0 and exclude_score <= 2:  # 임계값 완화
                paper["screening_score"] = total_score
                paper["journal_score"] = journal_score
                paper["compensation_score"] = compensation_score
                paper["anatomy_score"] = anatomy_score
                filtered.append(paper)

        return sorted(filtered, key=lambda x: x["screening_score"], reverse=True)

    def filter_by_research_quality(self, papers: List[Dict]) -> List[Dict]:
        """2차 필터: 연구 품질 필터링"""
        filtered = []

        for paper in papers:
            # 연구 설계 점수
            abstract = self._restore_abstract(paper.get("abstract_inverted_index", {})).lower()
            title = paper.get("display_name", "").lower()
            text = f"{title} {abstract}"

            design_scores = {
                "randomized controlled trial": 10,
                "rct": 10,
                "systematic review": 9,
                "meta-analysis": 9,
                "cohort study": 7,
                "prospective": 6,
                "cross-sectional": 5,
                "case-control": 4,
                "case series": 2,
                "case report": 1
            }

            design_score = 0
            for design, score in design_scores.items():
                if design in text:
                    design_score = max(design_score, score)

            # 샘플 크기 추정
            sample_size = self._estimate_sample_size(text)
            sample_score = min(sample_size / 20, 5) if sample_size else 0

            # 인용 점수
            citation_count = paper.get("cited_by_count", 0)
            year = paper.get("publication_year", 2024)
            years_since_pub = 2024 - year
            citation_score = min(citation_count / max(years_since_pub, 1), 10)

            # 기관 점수 (다기관 연구 가산점)
            institution_count = paper.get("institutions_distinct_count", 1)
            institution_score = min(institution_count, 3)

            quality_score = design_score + sample_score + citation_score + institution_score

            # 품질 기준 통과 (20점 만점에 6점 이상으로 완화)
            if quality_score >= 6 and design_score >= 2:
                paper["quality_score"] = quality_score
                paper["design_score"] = design_score
                paper["sample_score"] = sample_score
                paper["citation_score"] = citation_score
                filtered.append(paper)

        return sorted(filtered, key=lambda x: x["quality_score"], reverse=True)

    def filter_by_compensation_relevance(self, papers: List[Dict]) -> List[Dict]:
        """3차 필터: 보상작용 관련성 필터링"""
        filtered = []

        for paper in papers:
            abstract = self._restore_abstract(paper.get("abstract_inverted_index", {}))
            title = paper.get("display_name", "")
            text = f"{title} {abstract}".lower()

            # 5WHY 분석 가능성 체크
            why_indicators = {
                "cause": 2, "etiology": 2, "mechanism": 3, "pathophysiology": 3,
                "due to": 1, "because": 1, "result": 1, "lead to": 1,
                "primary": 2, "secondary": 2, "compensatory": 3,
                "adaptation": 2, "strategy": 2
            }

            why_score = sum(score for indicator, score in why_indicators.items()
                           if indicator in text)

            # 평가 방법 점수
            assessment_methods = {
                "electromyography": 3, "emg": 3, "motion analysis": 3,
                "3d motion": 3, "kinematics": 2, "kinetics": 2,
                "force plate": 2, "pressure": 1, "clinical test": 2,
                "functional": 2, "performance": 1
            }

            assessment_score = sum(score for method, score in assessment_methods.items()
                                 if method in text)

            # 중재법 점수
            intervention_methods = {
                "exercise": 3, "strengthening": 3, "stretching": 2,
                "training": 2, "rehabilitation": 2, "therapy": 1,
                "manual": 2, "mobilization": 2, "education": 1
            }

            intervention_score = sum(score for method, score in intervention_methods.items()
                                   if method in text)

            # 보상작용 특이성 점수
            compensation_specificity = 0
            specific_patterns = [
                "gluteus medius weakness", "tfl overactivity", "hip hiking",
                "serratus anterior dysfunction", "upper trap dominance",
                "tibialis posterior dysfunction", "peroneal compensation",
                "scapular dyskinesis", "anterior head posture"
            ]

            for pattern in specific_patterns:
                if pattern in text:
                    compensation_specificity += 2

            total_relevance = why_score + assessment_score + intervention_score + compensation_specificity

            # 관련성 기준 통과 (최소 4점으로 완화)
            if total_relevance >= 4:
                paper["relevance_score"] = total_relevance
                paper["why_score"] = why_score
                paper["assessment_score"] = assessment_score
                paper["intervention_score"] = intervention_score
                paper["compensation_specificity"] = compensation_specificity
                filtered.append(paper)

        return sorted(filtered, key=lambda x: x["relevance_score"], reverse=True)

    def screen_papers(self, limit: int = 20) -> List[Dict]:
        """전체 3단계 스크리닝 프로세스 실행"""
        print("Compensation paper screening started...")

        # 1. 논문 검색
        print("Step 1: Searching papers from OpenAlex...")
        raw_papers = self.search_papers(limit * 5)  # 여유분 확보
        print(f"   Found papers: {len(raw_papers)}")

        if not raw_papers:
            print("No papers found.")
            return []

        # 2. 1차 필터: 분야 특화
        print("Step 2: Field specialization filtering...")
        field_filtered = self.filter_by_field_specialization(raw_papers)
        print(f"   Passed papers: {len(field_filtered)}")

        # 3. 2차 필터: 연구 품질
        print("Step 3: Research quality filtering...")
        quality_filtered = self.filter_by_research_quality(field_filtered)
        print(f"   Passed papers: {len(quality_filtered)}")

        # 4. 3차 필터: 보상작용 관련성
        print("Step 4: Compensation relevance filtering...")
        final_filtered = self.filter_by_compensation_relevance(quality_filtered)
        print(f"   Final filtered papers: {len(final_filtered)}")

        # 5. 상위 논문만 반환
        result = final_filtered[:limit]
        print(f"Final result: {len(result)} papers")

        return result

    def _get_journal_name(self, paper: Dict) -> str:
        """논문의 저널명 추출"""
        primary_location = paper.get("primary_location", {})
        source = primary_location.get("source", {})
        return source.get("display_name", "") if source else ""

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

    def _estimate_sample_size(self, text: str) -> Optional[int]:
        """텍스트에서 샘플 크기 추정"""
        patterns = [
            r'n\s*=\s*(\d+)',
            r'N\s*=\s*(\d+)',
            r'(\d+)\s+participants?',
            r'(\d+)\s+subjects?',
            r'(\d+)\s+patients?'
        ]

        for pattern in patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                try:
                    return int(matches[0])
                except ValueError:
                    continue
        return None

def test_paper_screener():
    """논문 스크리너 테스트"""
    print("TEST 1/5: Paper Screening System Test")
    print("=" * 50)

    screener = CompensationPaperScreener()

    # 테스트 실행
    papers = screener.screen_papers(limit=5)

    if papers:
        print(f"\nSUCCESS: {len(papers)} high-quality papers selected")

        for i, paper in enumerate(papers, 1):
            print(f"\nPaper {i}:")
            print(f"   Title: {paper.get('display_name', 'N/A')[:80]}...")
            print(f"   Year: {paper.get('publication_year', 'N/A')}")
            print(f"   Citations: {paper.get('cited_by_count', 0)}")
            print(f"   Journal: {screener._get_journal_name(paper)}")
            print(f"   Screening score: {paper.get('screening_score', 0):.1f}")
            print(f"   Quality score: {paper.get('quality_score', 0):.1f}")
            print(f"   Relevance score: {paper.get('relevance_score', 0):.1f}")
    else:
        print("FAILED: No papers selected.")
        return False

    print("\n" + "=" * 50)
    print("TEST 1/5 COMPLETED")
    return True

if __name__ == "__main__":
    test_paper_screener()