# -*- coding: utf-8 -*-
"""
보상작용 연구 자동화 시스템 - 노드 연결 시스템
Claude Development Rules 준수하여 개발

핵심 기능:
1. 논문 간 해부학적 연결 생성
2. 보상 패턴 기반 기능적 연결
3. 치료법 기반 치료적 연결
4. 시간적 연결 (보상 발생 순서)
"""

import re
import math
from typing import Dict, List, Tuple, Set, Optional
from dataclasses import dataclass
from enum import Enum
from collections import defaultdict
import json

class ConnectionType(Enum):
    ANATOMICAL = "anatomical"
    FUNCTIONAL = "functional"
    THERAPEUTIC = "therapeutic"
    TEMPORAL = "temporal"
    CAUSAL = "causal"

class ConnectionStrength(Enum):
    WEAK = 1
    MODERATE = 2
    STRONG = 3
    VERY_STRONG = 4

@dataclass
class NodeConnection:
    source_id: str
    target_id: str
    connection_type: ConnectionType
    strength: ConnectionStrength
    evidence: List[str]
    confidence: float

@dataclass
class CompensationNode:
    node_id: str
    title: str
    node_type: str  # paper, muscle, joint, pattern, treatment
    keywords: List[str]
    concepts: List[str]
    body_region: List[str]
    compensation_elements: Dict[str, List[str]]
    clinical_significance: float

class CompensationNodeConnector:
    def __init__(self):
        # 해부학적 연결 데이터베이스
        self.anatomical_connections = {
            "hip": {
                "muscles": ["gluteus medius", "gluteus maximus", "gluteus minimus",
                          "tensor fasciae latae", "piriformis", "hip adductors"],
                "joints": ["hip joint", "si joint", "lumbar spine"],
                "related_regions": ["knee", "ankle", "pelvis"]
            },
            "knee": {
                "muscles": ["quadriceps", "hamstrings", "gastrocnemius", "popliteus"],
                "joints": ["knee joint", "patellofemoral joint"],
                "related_regions": ["hip", "ankle"]
            },
            "ankle": {
                "muscles": ["tibialis posterior", "peroneal", "gastrocnemius", "soleus"],
                "joints": ["ankle joint", "subtalar joint"],
                "related_regions": ["knee", "foot"]
            },
            "shoulder": {
                "muscles": ["serratus anterior", "upper trapezius", "lower trapezius",
                          "rhomboids", "rotator cuff"],
                "joints": ["glenohumeral", "scapulothoracic", "acromioclavicular"],
                "related_regions": ["neck", "thoracic spine"]
            }
        }

        # 보상 패턴 연결 데이터베이스
        self.compensation_patterns = {
            "gluteus_medius_weakness": {
                "primary_dysfunction": "gluteus medius weakness",
                "compensatory_muscles": ["tensor fasciae latae", "hip adductors", "quadratus lumborum"],
                "downstream_effects": ["knee valgus", "hip adduction", "lateral pelvic tilt"],
                "related_conditions": ["patellofemoral pain", "it band syndrome", "low back pain"]
            },
            "serratus_anterior_dysfunction": {
                "primary_dysfunction": "serratus anterior weakness",
                "compensatory_muscles": ["upper trapezius", "levator scapulae", "rhomboids"],
                "downstream_effects": ["scapular winging", "shoulder elevation", "forward head"],
                "related_conditions": ["shoulder impingement", "neck pain", "thoracic outlet"]
            },
            "core_instability": {
                "primary_dysfunction": "core weakness",
                "compensatory_muscles": ["hip flexors", "back extensors", "neck muscles"],
                "downstream_effects": ["anterior pelvic tilt", "lumbar hyperlordosis", "hip flexor tightness"],
                "related_conditions": ["low back pain", "hip impingement", "neck pain"]
            }
        }

        # 치료적 연결 데이터베이스
        self.therapeutic_connections = {
            "strengthening": {
                "gluteus medius": ["side-lying abduction", "clamshell", "single leg squat"],
                "serratus anterior": ["wall slides", "push-up plus", "bear crawl"],
                "core": ["dead bug", "bird dog", "plank variations"]
            },
            "stretching": {
                "tfl": ["standing tfl stretch", "side-lying tfl stretch"],
                "hip flexors": ["couch stretch", "kneeling hip flexor stretch"],
                "upper trapezius": ["upper trap stretch", "levator scapulae stretch"]
            },
            "motor_control": {
                "hip": ["single leg balance", "step down training", "gait retraining"],
                "shoulder": ["scapular stabilization", "reaching patterns", "overhead training"],
                "spine": ["spinal stabilization", "movement retraining", "postural correction"]
            }
        }

    def create_compensation_node(self, paper_data: Dict, analysis_data: Dict) -> CompensationNode:
        """논문 데이터에서 보상작용 노드 생성"""
        node_id = self._generate_node_id(paper_data)
        title = paper_data.get("display_name", "Unknown Paper")

        # 키워드 추출
        keywords = self._extract_keywords(paper_data, analysis_data)

        # 개념 추출
        concepts = self._extract_concepts(paper_data, analysis_data)

        # 신체 부위 식별
        body_region = self._identify_body_regions(paper_data, analysis_data)

        # 보상작용 요소 추출
        compensation_elements = self._extract_compensation_elements(analysis_data)

        # 임상적 중요도 계산
        clinical_significance = self._calculate_clinical_significance(paper_data, analysis_data)

        return CompensationNode(
            node_id=node_id,
            title=title,
            node_type="paper",
            keywords=keywords,
            concepts=concepts,
            body_region=body_region,
            compensation_elements=compensation_elements,
            clinical_significance=clinical_significance
        )

    def connect_nodes(self, nodes: List[CompensationNode]) -> List[NodeConnection]:
        """노드들 간의 연결 생성"""
        connections = []

        for i, source_node in enumerate(nodes):
            for target_node in nodes[i+1:]:
                # 각 연결 타입별로 연결 강도 계산
                anatomical_strength = self._calculate_anatomical_connection(source_node, target_node)
                functional_strength = self._calculate_functional_connection(source_node, target_node)
                therapeutic_strength = self._calculate_therapeutic_connection(source_node, target_node)
                causal_strength = self._calculate_causal_connection(source_node, target_node)

                # 가장 강한 연결 타입 선택
                connection_strengths = [
                    (ConnectionType.ANATOMICAL, anatomical_strength),
                    (ConnectionType.FUNCTIONAL, functional_strength),
                    (ConnectionType.THERAPEUTIC, therapeutic_strength),
                    (ConnectionType.CAUSAL, causal_strength)
                ]

                # 임계값 이상의 연결만 생성
                for conn_type, strength in connection_strengths:
                    if strength >= 0.3:  # 임계값
                        connection = NodeConnection(
                            source_id=source_node.node_id,
                            target_id=target_node.node_id,
                            connection_type=conn_type,
                            strength=self._strength_to_enum(strength),
                            evidence=self._generate_evidence(source_node, target_node, conn_type),
                            confidence=strength
                        )
                        connections.append(connection)

        return connections

    def _generate_node_id(self, paper_data: Dict) -> str:
        """노드 ID 생성"""
        title = paper_data.get("display_name", "unknown")
        year = paper_data.get("publication_year", "")

        # 제목에서 주요 단어 추출
        words = re.findall(r'\b[a-zA-Z]{4,}\b', title.lower())
        key_words = words[:3] if len(words) >= 3 else words

        node_id = "-".join(key_words) + f"-{year}" if year else "-".join(key_words)
        return re.sub(r'[^a-zA-Z0-9\-]', '', node_id)

    def _extract_keywords(self, paper_data: Dict, analysis_data: Dict) -> List[str]:
        """키워드 추출"""
        keywords = set()

        # 제목에서 키워드
        title = paper_data.get("display_name", "").lower()
        title_keywords = re.findall(r'\b[a-zA-Z]{4,}\b', title)
        keywords.update(title_keywords[:10])

        # 분석 데이터에서 키워드
        if "compensation_pattern" in analysis_data:
            pattern = analysis_data["compensation_pattern"]
            if hasattr(pattern, 'primary_dysfunction'):
                keywords.add(pattern.primary_dysfunction.lower())
            if hasattr(pattern, 'compensatory_muscles'):
                keywords.update(muscle.lower() for muscle in pattern.compensatory_muscles[:3])

        return list(keywords)[:15]

    def _extract_concepts(self, paper_data: Dict, analysis_data: Dict) -> List[str]:
        """개념 추출"""
        concepts = set()

        # 보상작용 핵심 개념
        compensation_concepts = [
            "muscle weakness", "overactivity", "compensation", "substitution",
            "biomechanics", "motor control", "rehabilitation", "strengthening"
        ]

        text = (paper_data.get("display_name", "") + " " +
                str(analysis_data.get("clinical_significance", ""))).lower()

        for concept in compensation_concepts:
            if concept in text:
                concepts.add(concept)

        return list(concepts)

    def _identify_body_regions(self, paper_data: Dict, analysis_data: Dict) -> List[str]:
        """신체 부위 식별"""
        regions = set()
        text = paper_data.get("display_name", "").lower()

        region_keywords = {
            "hip": ["hip", "pelvis", "gluteus", "gluteal"],
            "knee": ["knee", "patella", "patellar", "quadriceps"],
            "ankle": ["ankle", "foot", "tibialis", "peroneal"],
            "shoulder": ["shoulder", "scapula", "scapular", "serratus"],
            "spine": ["spine", "spinal", "back", "lumbar", "thoracic"]
        }

        for region, keywords in region_keywords.items():
            if any(keyword in text for keyword in keywords):
                regions.add(region)

        return list(regions)

    def _extract_compensation_elements(self, analysis_data: Dict) -> Dict[str, List[str]]:
        """보상작용 요소 추출"""
        elements = {
            "weak_muscles": [],
            "overactive_muscles": [],
            "affected_joints": [],
            "movement_patterns": [],
            "treatment_approaches": []
        }

        if "compensation_pattern" in analysis_data:
            pattern = analysis_data["compensation_pattern"]

            if hasattr(pattern, 'primary_dysfunction'):
                elements["weak_muscles"].append(pattern.primary_dysfunction)

            if hasattr(pattern, 'compensatory_muscles'):
                elements["overactive_muscles"].extend(pattern.compensatory_muscles[:3])

            if hasattr(pattern, 'affected_joints'):
                elements["affected_joints"].extend(pattern.affected_joints[:3])

            if hasattr(pattern, 'treatment_priority'):
                elements["treatment_approaches"].extend(pattern.treatment_priority[:3])

        return elements

    def _calculate_clinical_significance(self, paper_data: Dict, analysis_data: Dict) -> float:
        """임상적 중요도 계산"""
        significance = 0.0

        # 인용 수 기반 점수
        citations = paper_data.get("cited_by_count", 0)
        citation_score = min(citations / 100, 1.0)
        significance += citation_score * 0.3

        # 연도 기반 점수 (최신성)
        year = paper_data.get("publication_year", 2000)
        recency_score = max(0, (year - 2000) / 24)  # 2000년 기준으로 정규화
        significance += recency_score * 0.2

        # 분석 품질 점수
        if "why_levels" in analysis_data:
            why_levels = analysis_data["why_levels"]
            if why_levels:
                avg_evidence = sum(level.evidence_strength for level in why_levels) / len(why_levels)
                significance += avg_evidence * 0.5

        return min(significance, 1.0)

    def _calculate_anatomical_connection(self, node1: CompensationNode, node2: CompensationNode) -> float:
        """해부학적 연결 강도 계산"""
        strength = 0.0

        # 같은 신체 부위
        common_regions = set(node1.body_region) & set(node2.body_region)
        strength += len(common_regions) * 0.3

        # 인접한 신체 부위
        for region1 in node1.body_region:
            for region2 in node2.body_region:
                if region1 in self.anatomical_connections and region2 in self.anatomical_connections[region1].get("related_regions", []):
                    strength += 0.2

        # 공통 근육/관절
        elements1 = node1.compensation_elements
        elements2 = node2.compensation_elements

        common_muscles = (set(elements1.get("weak_muscles", [])) | set(elements1.get("overactive_muscles", []))) & \
                        (set(elements2.get("weak_muscles", [])) | set(elements2.get("overactive_muscles", [])))
        strength += len(common_muscles) * 0.2

        common_joints = set(elements1.get("affected_joints", [])) & set(elements2.get("affected_joints", []))
        strength += len(common_joints) * 0.2

        return min(strength, 1.0)

    def _calculate_functional_connection(self, node1: CompensationNode, node2: CompensationNode) -> float:
        """기능적 연결 강도 계산"""
        strength = 0.0

        # 보상 패턴 유사성
        for pattern_name, pattern_data in self.compensation_patterns.items():
            pattern_keywords = set(pattern_data["primary_dysfunction"].split() +
                                 [muscle for muscle in pattern_data["compensatory_muscles"]])

            node1_keywords = set(node1.keywords)
            node2_keywords = set(node2.keywords)

            node1_match = len(pattern_keywords & node1_keywords) / len(pattern_keywords) if pattern_keywords else 0
            node2_match = len(pattern_keywords & node2_keywords) / len(pattern_keywords) if pattern_keywords else 0

            if node1_match > 0.3 and node2_match > 0.3:
                strength += 0.4

        # 공통 개념
        common_concepts = set(node1.concepts) & set(node2.concepts)
        strength += len(common_concepts) * 0.1

        return min(strength, 1.0)

    def _calculate_therapeutic_connection(self, node1: CompensationNode, node2: CompensationNode) -> float:
        """치료적 연결 강도 계산"""
        strength = 0.0

        # 공통 치료 접근법
        treatments1 = set(node1.compensation_elements.get("treatment_approaches", []))
        treatments2 = set(node2.compensation_elements.get("treatment_approaches", []))
        common_treatments = treatments1 & treatments2
        strength += len(common_treatments) * 0.3

        # 치료 카테고리 매칭
        for category, treatments in self.therapeutic_connections.items():
            treatment_keywords = set()
            for treatment_list in treatments.values():
                treatment_keywords.update(treatment_list)

            node1_match = len(treatment_keywords & treatments1) > 0
            node2_match = len(treatment_keywords & treatments2) > 0

            if node1_match and node2_match:
                strength += 0.2

        return min(strength, 1.0)

    def _calculate_causal_connection(self, node1: CompensationNode, node2: CompensationNode) -> float:
        """인과관계 연결 강도 계산"""
        strength = 0.0

        # 한 노드의 약화된 근육이 다른 노드의 과활성 근육과 연관
        weak1 = set(node1.compensation_elements.get("weak_muscles", []))
        overactive1 = set(node1.compensation_elements.get("overactive_muscles", []))
        weak2 = set(node2.compensation_elements.get("weak_muscles", []))
        overactive2 = set(node2.compensation_elements.get("overactive_muscles", []))

        # 보상 관계 체크
        for pattern_data in self.compensation_patterns.values():
            primary = pattern_data["primary_dysfunction"]
            compensatory = set(pattern_data["compensatory_muscles"])

            # node1의 주요 문제가 node2의 보상과 연결
            if any(primary.lower() in keyword.lower() for keyword in node1.keywords):
                if compensatory & (overactive2 | weak2):
                    strength += 0.4

            # 반대 방향 체크
            if any(primary.lower() in keyword.lower() for keyword in node2.keywords):
                if compensatory & (overactive1 | weak1):
                    strength += 0.4

        return min(strength, 1.0)

    def _strength_to_enum(self, strength: float) -> ConnectionStrength:
        """연결 강도를 enum으로 변환"""
        if strength >= 0.8:
            return ConnectionStrength.VERY_STRONG
        elif strength >= 0.6:
            return ConnectionStrength.STRONG
        elif strength >= 0.4:
            return ConnectionStrength.MODERATE
        else:
            return ConnectionStrength.WEAK

    def _generate_evidence(self, node1: CompensationNode, node2: CompensationNode,
                          conn_type: ConnectionType) -> List[str]:
        """연결 근거 생성"""
        evidence = []

        if conn_type == ConnectionType.ANATOMICAL:
            common_regions = set(node1.body_region) & set(node2.body_region)
            if common_regions:
                evidence.append(f"Shared body regions: {', '.join(common_regions)}")

        elif conn_type == ConnectionType.FUNCTIONAL:
            common_concepts = set(node1.concepts) & set(node2.concepts)
            if common_concepts:
                evidence.append(f"Common concepts: {', '.join(list(common_concepts)[:3])}")

        elif conn_type == ConnectionType.THERAPEUTIC:
            treatments1 = set(node1.compensation_elements.get("treatment_approaches", []))
            treatments2 = set(node2.compensation_elements.get("treatment_approaches", []))
            common_treatments = treatments1 & treatments2
            if common_treatments:
                evidence.append(f"Shared treatments: {', '.join(list(common_treatments)[:2])}")

        elif conn_type == ConnectionType.CAUSAL:
            evidence.append("Identified compensation chain relationship")

        return evidence

    def generate_network_json(self, nodes: List[CompensationNode],
                            connections: List[NodeConnection]) -> str:
        """네트워크 JSON 생성"""
        network_data = {
            "nodes": [],
            "links": []
        }

        # 노드 데이터
        for node in nodes:
            node_data = {
                "id": node.node_id,
                "title": node.title,
                "type": node.node_type,
                "body_region": node.body_region,
                "significance": node.clinical_significance,
                "keywords": node.keywords[:5],  # 상위 5개만
                "concepts": node.concepts[:3]   # 상위 3개만
            }
            network_data["nodes"].append(node_data)

        # 연결 데이터
        for connection in connections:
            link_data = {
                "source": connection.source_id,
                "target": connection.target_id,
                "type": connection.connection_type.value,
                "strength": connection.strength.value,
                "confidence": connection.confidence,
                "evidence": connection.evidence
            }
            network_data["links"].append(link_data)

        return json.dumps(network_data, indent=2, ensure_ascii=False)

def test_node_connector():
    """노드 연결 시스템 테스트"""
    print("TEST 3/5: Node Connection System Test")
    print("=" * 50)

    connector = CompensationNodeConnector()

    # 테스트 논문 데이터들
    test_papers = [
        {
            "display_name": "Gluteus Medius Weakness and Hip Compensation",
            "publication_year": 2020,
            "cited_by_count": 45,
            "analysis": {
                "compensation_pattern": type('Pattern', (), {
                    'primary_dysfunction': 'gluteus medius weakness',
                    'compensatory_muscles': ['tensor fasciae latae', 'hip adductors'],
                    'affected_joints': ['hip', 'knee'],
                    'treatment_priority': ['strengthening', 'motor control']
                })(),
                "why_levels": [type('Level', (), {'evidence_strength': 0.8})()],
                "clinical_significance": "High clinical impact on runners"
            }
        },
        {
            "display_name": "TFL Overactivity in Patellofemoral Pain Syndrome",
            "publication_year": 2019,
            "cited_by_count": 32,
            "analysis": {
                "compensation_pattern": type('Pattern', (), {
                    'primary_dysfunction': 'patellofemoral dysfunction',
                    'compensatory_muscles': ['tensor fasciae latae', 'vastus lateralis'],
                    'affected_joints': ['knee', 'hip'],
                    'treatment_priority': ['stretching', 'strengthening']
                })(),
                "why_levels": [type('Level', (), {'evidence_strength': 0.7})()],
                "clinical_significance": "Moderate clinical relevance"
            }
        },
        {
            "display_name": "Serratus Anterior Dysfunction and Shoulder Impingement",
            "publication_year": 2021,
            "cited_by_count": 28,
            "analysis": {
                "compensation_pattern": type('Pattern', (), {
                    'primary_dysfunction': 'serratus anterior weakness',
                    'compensatory_muscles': ['upper trapezius', 'levator scapulae'],
                    'affected_joints': ['shoulder', 'scapulothoracic'],
                    'treatment_priority': ['strengthening', 'motor control']
                })(),
                "why_levels": [type('Level', (), {'evidence_strength': 0.6})()],
                "clinical_significance": "Important for shoulder rehabilitation"
            }
        }
    ]

    # 노드 생성
    nodes = []
    for paper_data in test_papers:
        node = connector.create_compensation_node(paper_data, paper_data["analysis"])
        nodes.append(node)

    print(f"Created {len(nodes)} compensation nodes:")
    for node in nodes:
        print(f"  - {node.title[:50]}...")
        print(f"    Body regions: {', '.join(node.body_region)}")
        print(f"    Significance: {node.clinical_significance:.2f}")

    # 연결 생성
    connections = connector.connect_nodes(nodes)

    print(f"\nGenerated {len(connections)} connections:")
    for conn in connections[:5]:  # 상위 5개만 표시
        print(f"  - {conn.source_id} -> {conn.target_id}")
        print(f"    Type: {conn.connection_type.value}")
        print(f"    Strength: {conn.strength.value}")
        print(f"    Confidence: {conn.confidence:.2f}")
        if conn.evidence:
            print(f"    Evidence: {conn.evidence[0]}")

    # 네트워크 JSON 생성
    network_json = connector.generate_network_json(nodes, connections)

    print(f"\nNetwork JSON generated ({len(network_json)} characters)")
    print("Sample JSON structure:")
    json_data = json.loads(network_json)
    print(f"  Nodes: {len(json_data['nodes'])}")
    print(f"  Links: {len(json_data['links'])}")

    print("\n" + "=" * 50)
    print("TEST 3/5 COMPLETED")
    return True

if __name__ == "__main__":
    test_node_connector()