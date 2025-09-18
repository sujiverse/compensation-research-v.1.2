# -*- coding: utf-8 -*-
"""
Compensation Research Obsidian Vault Generator
Claude Development Rules compliant - creating structured knowledge vault

Core Features:
1. Create optimized Obsidian vault structure for compensation research
2. Generate paper analysis files using 5WHY methodology
3. Build node connection files with compensation relationships
4. Apply systematic naming and tagging conventions
"""

import os
import json
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

class CompensationObsidianGenerator:
    def __init__(self, vault_path: str = "Compensation-Research-Vault"):
        self.vault_path = Path(vault_path)
        self.structure = self._load_structure_config()

    def _load_structure_config(self) -> Dict:
        """Load vault structure configuration"""
        return {
            "folders": [
                "00-Templates",
                "01-Papers/Hip-Compensation",
                "01-Papers/Knee-Compensation",
                "01-Papers/Ankle-Compensation",
                "01-Papers/Spine-Compensation",
                "01-Papers/Multi-Joint",
                "02-Anatomy/Muscles",
                "02-Anatomy/Joints",
                "02-Anatomy/Fascial-Chains",
                "02-Anatomy/Neural-Control",
                "03-Compensation-Patterns/Primary-Patterns",
                "03-Compensation-Patterns/Secondary-Adaptations",
                "03-Compensation-Patterns/Complex-Chains",
                "04-Clinical-Tests/Movement-Screens",
                "04-Clinical-Tests/Muscle-Tests",
                "04-Clinical-Tests/Functional-Assessments",
                "05-Interventions/Exercise-Protocols",
                "05-Interventions/Manual-Therapy",
                "05-Interventions/Movement-Retraining",
                "06-Mechanisms/Neurological",
                "06-Mechanisms/Biomechanical",
                "06-Mechanisms/Physiological",
                "07-Graphs",
                "08-Meta"
            ],
            "templates": {
                "5WHY-Analysis-Template.md": self._get_5why_template(),
                "Paper-Review-Template.md": self._get_paper_template(),
                "Compensation-Pattern-Template.md": self._get_pattern_template()
            }
        }

    def create_vault_structure(self) -> bool:
        """Create complete Obsidian vault structure"""
        try:
            print("Creating Obsidian vault structure...")

            # Create main vault directory
            self.vault_path.mkdir(parents=True, exist_ok=True)

            # Create folder structure
            for folder in self.structure["folders"]:
                folder_path = self.vault_path / folder
                folder_path.mkdir(parents=True, exist_ok=True)
                print(f"   Created: {folder}")

            # Create templates
            templates_path = self.vault_path / "00-Templates"
            for template_name, content in self.structure["templates"].items():
                template_file = templates_path / template_name
                template_file.write_text(content, encoding='utf-8')
                print(f"   Created template: {template_name}")

            # Create vault configuration
            self._create_vault_config()

            # Create meta files
            self._create_meta_files()

            print(f"Vault structure created at: {self.vault_path.absolute()}")
            return True

        except Exception as e:
            print(f"Failed to create vault structure: {e}")
            return False

    def generate_paper_file(self, paper_data: Dict, analysis_data: Dict) -> str:
        """Generate individual paper analysis file"""

        # Extract key information
        title = paper_data.get("display_name", "Unknown Title")
        year = paper_data.get("publication_year", "Unknown")
        authors = self._extract_authors(paper_data)
        journal = self._get_journal_name(paper_data)

        # Create filename
        first_author = authors[0].split()[0] if authors else "Unknown"
        safe_title = self._create_safe_filename(title)[:30]
        body_region = self._detect_body_region(title + " " + str(analysis_data))

        filename = f"{first_author}-{year}-{safe_title}-{body_region}.md"

        # Determine folder based on body region
        folder_map = {
            "Hip": "01-Papers/Hip-Compensation",
            "Knee": "01-Papers/Knee-Compensation",
            "Ankle": "01-Papers/Ankle-Compensation",
            "Spine": "01-Papers/Spine-Compensation",
            "Multi": "01-Papers/Multi-Joint"
        }

        target_folder = folder_map.get(body_region, "01-Papers/Multi-Joint")
        file_path = self.vault_path / target_folder / filename

        # Generate content
        content = self._generate_paper_content(paper_data, analysis_data)

        # Write file
        file_path.write_text(content, encoding='utf-8')

        return str(file_path)

    def generate_compensation_pattern_file(self, pattern_data: Dict) -> str:
        """Generate compensation pattern analysis file"""

        primary = pattern_data.get("primary_dysfunction", "Unknown")
        compensation = pattern_data.get("main_compensation", "Unknown")

        # Create filename
        safe_primary = self._create_safe_filename(primary)
        safe_compensation = self._create_safe_filename(compensation)
        filename = f"{safe_primary}-to-{safe_compensation}.md"

        file_path = self.vault_path / "03-Compensation-Patterns/Primary-Patterns" / filename

        # Generate content
        content = self._generate_pattern_content(pattern_data)

        # Write file
        file_path.write_text(content, encoding='utf-8')

        return str(file_path)

    def generate_node_connection_file(self, connections: List[Dict]) -> str:
        """Generate node connection visualization file"""

        filename = f"Compensation-Network-{datetime.now().strftime('%Y%m%d')}.md"
        file_path = self.vault_path / "07-Graphs" / filename

        content = self._generate_connection_content(connections)

        # Write file
        file_path.write_text(content, encoding='utf-8')

        return str(file_path)

    def update_research_dashboard(self, stats: Dict) -> str:
        """Update research dashboard with current statistics"""

        dashboard_path = self.vault_path / "08-Meta" / "Research-Dashboard.md"

        content = f"""# Research Dashboard
Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## Current Statistics
- Total Papers Analyzed: {stats.get('total_papers', 0)}
- Compensation Patterns Identified: {stats.get('patterns', 0)}
- Node Connections: {stats.get('connections', 0)}
- High Quality Papers: {stats.get('high_quality', 0)}

## Recent Additions
{self._format_recent_additions(stats.get('recent', []))}

## Quality Metrics
- Average 5WHY Depth: {stats.get('avg_why_depth', 0):.1f}
- Pattern Coverage: {stats.get('pattern_coverage', 0):.1f}%
- Connection Density: {stats.get('connection_density', 0):.2f}

## Priority Areas
{self._format_priority_areas(stats.get('priorities', []))}

---
*Auto-generated by Compensation Research System*
"""

        dashboard_path.write_text(content, encoding='utf-8')
        return str(dashboard_path)

    def _get_5why_template(self) -> str:
        """Get 5WHY analysis template"""
        return """---
title: "논문 제목"
authors: []
journal: ""
year:
doi: ""
study_type: ""
body_region: []
compensation_type: []
quality_score:
obsidian_created: "{{date}}"
tags: [#5why-analysis, #compensation]
---

# {{title}}

## 📋 Paper Overview
**Authors:** {{authors}}
**Journal:** {{journal}} ({{year}})
**DOI:** {{doi}}
**Study Design:** {{study_type}}

## 🔍 5WHY Analysis

### 1차 WHY: 왜 이 통증/기능장애가 발생했는가?
**Answer:**
**Evidence:**
**Compensation Trigger:**

### 2차 WHY: 왜 이 근육/구조가 약화/과긴장되었는가?
**Answer:**
**Evidence:**
**Root Cause Factor:**

### 3차 WHY: 왜 이 운동패턴이 변화했는가?
**Answer:**
**Evidence:**
**Movement Dysfunction:**

### 4차 WHY: 왜 신경계가 이런 전략을 선택했는가?
**Answer:**
**Evidence:**
**Neural Adaptation:**

### 5차 WHY: 왜 이 보상이 고착화되었는가?
**Answer:**
**Evidence:**
**System Integration:**

## 🎯 Clinical Implications
**Primary Treatment Target:**
**Treatment Hierarchy:**
**Expected Timeline:**

## 🔗 Connected Patterns
- [[Pattern::]]
- [[Muscle::]]
- [[Assessment::]]
- [[Treatment::]]

## 📊 Evidence Quality
**Research Design:**
**Sample Size:**
**Clinical Relevance:**
"""

    def _get_paper_template(self) -> str:
        """Get paper review template"""
        return """---
title: "{{title}}"
authors: {{authors}}
journal: "{{journal}}"
year: {{year}}
doi: "{{doi}}"
study_type: "{{study_type}}"
sample_size: {{sample_size}}
quality_score: {{quality_score}}
body_region: {{body_region}}
compensation_type: {{compensation_type}}
assessment_methods: {{assessment_methods}}
interventions: {{interventions}}
key_findings: {{key_findings}}
clinical_significance: "{{clinical_significance}}"
obsidian_created: "{{date}}"
last_updated: "{{date}}"
tags: [#paper-review, #{{body_region}}, #{{compensation_type}}]
---

# {{title}}

## 📋 Study Information
- **Lead Author:** {{first_author}}
- **Publication:** {{journal}} ({{year}})
- **DOI:** {{doi}}
- **Study Design:** {{study_type}}
- **Sample Size:** N={{sample_size}}

## 🎯 Research Question
{{research_question}}

## 🔬 Methodology
{{methodology}}

## 📊 Key Findings
{{key_findings}}

## 🏥 Clinical Relevance
{{clinical_relevance}}

## 🔗 Compensation Connections
{{compensation_connections}}

## 📈 Quality Assessment
- **Design Quality:** {{design_quality}}/10
- **Clinical Applicability:** {{clinical_applicability}}/10
- **Evidence Strength:** {{evidence_strength}}/10

## 🔍 5WHY Integration
[[5WHY-Analysis-{{filename}}]]

---
*Analysis completed: {{date}}*
"""

    def _get_pattern_template(self) -> str:
        """Get compensation pattern template"""
        return """---
pattern_name: "{{pattern_name}}"
primary_dysfunction: "{{primary_dysfunction}}"
compensatory_muscles: {{compensatory_muscles}}
affected_joints: {{affected_joints}}
movement_affected: {{movement_affected}}
assessment_tests: {{assessment_tests}}
treatment_priority: {{treatment_priority}}
prognosis: "{{prognosis}}"
prevention_strategies: {{prevention_strategies}}
related_conditions: {{related_conditions}}
evidence_level: "{{evidence_level}}"
clinical_frequency: "{{clinical_frequency}}"
tags: [#compensation-pattern, #{{primary_body_region}}]
---

# {{pattern_name}}

## 🎯 Pattern Overview
**Primary Dysfunction:** {{primary_dysfunction}}
**Main Compensation:** {{main_compensation}}
**Clinical Frequency:** {{clinical_frequency}}

## 🔄 Compensation Chain
{{compensation_chain}}

## 🏥 Clinical Presentation
{{clinical_presentation}}

## 🔍 Assessment Protocol
{{assessment_protocol}}

## 💊 Treatment Approach
{{treatment_approach}}

## 📊 Evidence Base
{{evidence_base}}

## 🔗 Related Patterns
{{related_patterns}}

## 📚 Supporting Research
{{supporting_research}}

---
*Pattern documented: {{date}}*
"""

    def _create_vault_config(self):
        """Create Obsidian vault configuration"""
        obsidian_dir = self.vault_path / ".obsidian"
        obsidian_dir.mkdir(exist_ok=True)

        # Workspace config
        workspace_config = {
            "main": {
                "id": "compensation-research",
                "type": "split",
                "children": [
                    {
                        "id": "graph-view",
                        "type": "leaf",
                        "state": {
                            "type": "graph",
                            "state": {}
                        }
                    }
                ]
            },
            "left": {
                "id": "file-explorer",
                "type": "split",
                "children": [
                    {
                        "id": "file-tree",
                        "type": "leaf",
                        "state": {
                            "type": "file-explorer",
                            "state": {}
                        }
                    }
                ]
            }
        }

        workspace_file = obsidian_dir / "workspace.json"
        workspace_file.write_text(json.dumps(workspace_config, indent=2), encoding='utf-8')

    def _create_meta_files(self):
        """Create meta documentation files"""
        meta_path = self.vault_path / "08-Meta"

        # Quality metrics file
        quality_file = meta_path / "Quality-Metrics.md"
        quality_content = """# Quality Metrics Dashboard

## Paper Quality Standards
- **High Quality:** RCT, Systematic Review, Large Cohort (n>100)
- **Moderate Quality:** Cross-sectional, Case-control, Medium sample
- **Preliminary:** Case series, Small studies, Pilot research

## 5WHY Analysis Standards
- **Complete:** All 5 levels with evidence
- **Partial:** 3-4 levels with strong evidence
- **Basic:** 2-3 levels, needs expansion

## Connection Quality
- **Strong:** Direct causal relationship with evidence
- **Moderate:** Indirect relationship, plausible mechanism
- **Weak:** Theoretical connection, needs validation

---
*Standards updated: {{date}}*
"""
        quality_file.write_text(quality_content, encoding='utf-8')

        # Development log
        dev_log = meta_path / "Development-Log.md"
        dev_content = f"""# Development Log

## System Creation: {datetime.now().strftime('%Y-%m-%d')}
- Vault structure created
- Templates configured
- Quality standards established

## Automation Features
- 10-minute paper addition cycle
- Automatic 5WHY analysis
- Node connection generation
- Quality assessment

---
*Log started: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        dev_log.write_text(dev_content, encoding='utf-8')

    def _generate_paper_content(self, paper_data: Dict, analysis_data: Dict) -> str:
        """Generate complete paper analysis content"""

        title = paper_data.get("display_name", "Unknown Title")
        year = paper_data.get("publication_year", "Unknown")
        journal = self._get_journal_name(paper_data)
        doi = paper_data.get("doi", "")

        # Extract 5WHY analysis if available
        why_analysis = analysis_data.get("why_levels", [])

        content = f"""---
title: "{title}"
journal: "{journal}"
year: {year}
doi: "{doi}"
study_type: "{analysis_data.get('study_type', 'Unknown')}"
quality_score: {paper_data.get('quality_score', 0)}
compensation_pattern: "{analysis_data.get('compensation_pattern', {}).get('name', 'Unknown')}"
obsidian_created: "{datetime.now().strftime('%Y-%m-%d')}"
tags: [#compensation-research, #5why-analysis, #{self._detect_body_region(title).lower()}]
---

# {title}

## 📋 Study Overview
- **Journal:** {journal} ({year})
- **DOI:** {doi}
- **Quality Score:** {paper_data.get('quality_score', 0):.1f}/20
- **Citations:** {paper_data.get('cited_by_count', 0)}

## 🔍 5WHY Analysis

{self._format_5why_analysis(why_analysis)}

## 🎯 Compensation Pattern
**Pattern:** {analysis_data.get('compensation_pattern', {}).get('name', 'Not identified')}
**Primary Dysfunction:** {analysis_data.get('compensation_pattern', {}).get('primary_dysfunction', 'Unknown')}
**Compensatory Strategy:** {analysis_data.get('compensation_pattern', {}).get('compensatory_strategy', 'Unknown')}

## 🏥 Clinical Significance
{analysis_data.get('clinical_significance', 'Clinical relevance needs assessment')}

## 💡 Key Treatment Points
{self._format_treatment_points(analysis_data.get('treatment_keypoints', []))}

## 🔗 Related Concepts
{self._generate_related_links(analysis_data)}

---
*Analysis completed: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        return content

    def _generate_pattern_content(self, pattern_data: Dict) -> str:
        """Generate compensation pattern content"""

        name = pattern_data.get("name", "Unknown Pattern")
        primary = pattern_data.get("primary_dysfunction", "Unknown")
        compensation = pattern_data.get("main_compensation", "Unknown")

        content = f"""---
pattern_name: "{name}"
primary_dysfunction: "{primary}"
main_compensation: "{compensation}"
clinical_frequency: "{pattern_data.get('frequency', 'Unknown')}"
evidence_level: "{pattern_data.get('evidence_level', 'Preliminary')}"
tags: [#compensation-pattern, #clinical-assessment]
---

# {name}

## 🎯 Pattern Overview
**Primary Issue:** {primary}
**Compensatory Response:** {compensation}
**Clinical Frequency:** {pattern_data.get('frequency', 'Unknown')}

## 🔄 Compensation Mechanism
{pattern_data.get('mechanism', 'Mechanism needs detailed analysis')}

## 🏥 Clinical Assessment
{pattern_data.get('assessment', 'Assessment protocol needs development')}

## 💊 Treatment Strategy
{pattern_data.get('treatment', 'Treatment approach needs specification')}

## 📊 Evidence Quality
**Level:** {pattern_data.get('evidence_level', 'Preliminary')}
**Supporting Studies:** {len(pattern_data.get('supporting_papers', []))}

---
*Pattern documented: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        return content

    def _generate_connection_content(self, connections: List[Dict]) -> str:
        """Generate node connection visualization content"""

        content = f"""---
title: "Compensation Network Analysis"
generated: "{datetime.now().strftime('%Y-%m-%d %H:%M')}"
connection_count: {len(connections)}
tags: [#network-analysis, #compensation-connections]
---

# Compensation Network Analysis

## 🕸️ Network Overview
**Total Connections:** {len(connections)}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🔗 Connection Types

{self._format_connection_types(connections)}

## 📊 Network Statistics
{self._calculate_network_stats(connections)}

## 🎯 Key Relationships
{self._format_key_relationships(connections)}

---
*Network analysis: {datetime.now().strftime('%Y-%m-%d %H:%M')}*
"""
        return content

    def _extract_authors(self, paper_data: Dict) -> List[str]:
        """Extract author names from paper data"""
        authorships = paper_data.get("authorships", [])
        authors = []
        for authorship in authorships[:3]:  # First 3 authors
            author = authorship.get("author", {})
            name = author.get("display_name", "Unknown Author")
            authors.append(name)
        return authors

    def _get_journal_name(self, paper_data: Dict) -> str:
        """Extract journal name"""
        primary_location = paper_data.get("primary_location", {})
        source = primary_location.get("source", {})
        return source.get("display_name", "Unknown Journal")

    def _create_safe_filename(self, text: str) -> str:
        """Create safe filename from text"""
        safe = "".join(c for c in text if c.isalnum() or c in " -_")
        return safe.replace(" ", "-")[:50]

    def _detect_body_region(self, text: str) -> str:
        """Detect primary body region from text"""
        text_lower = text.lower()

        regions = {
            "Hip": ["hip", "gluteus", "tfl", "tensor fasciae latae", "acetabular"],
            "Knee": ["knee", "patella", "quadriceps", "hamstring", "meniscus"],
            "Ankle": ["ankle", "tibialis", "peroneal", "achilles", "plantar"],
            "Spine": ["spine", "vertebral", "lumbar", "cervical", "thoracic"],
        }

        for region, keywords in regions.items():
            if any(keyword in text_lower for keyword in keywords):
                return region

        return "Multi"

    def _format_5why_analysis(self, why_levels: List[Dict]) -> str:
        """Format 5WHY analysis for display"""
        if not why_levels:
            return "5WHY analysis not yet completed."

        formatted = ""
        for i, level in enumerate(why_levels, 1):
            formatted += f"### {i}차 WHY: {level.get('question', 'Question not available')}\n"
            formatted += f"**Answer:** {level.get('answer', 'Analysis needed')}\n"
            formatted += f"**Evidence:** {level.get('evidence', 'Evidence collection needed')}\n\n"

        return formatted

    def _format_treatment_points(self, treatment_points: List[str]) -> str:
        """Format treatment keypoints"""
        if not treatment_points:
            return "Treatment recommendations need development."

        formatted = ""
        for point in treatment_points:
            formatted += f"- {point}\n"

        return formatted

    def _generate_related_links(self, analysis_data: Dict) -> str:
        """Generate related concept links"""
        links = []

        # Add pattern link if available
        pattern = analysis_data.get('compensation_pattern', {})
        if pattern.get('name'):
            links.append(f"- [[Pattern::{pattern['name']}]]")

        # Add muscle links
        if pattern.get('primary_muscle'):
            links.append(f"- [[Muscle::{pattern['primary_muscle']}]]")
        if pattern.get('compensatory_muscle'):
            links.append(f"- [[Muscle::{pattern['compensatory_muscle']}]]")

        return "\n".join(links) if links else "Related links need development."

    def _format_connection_types(self, connections: List[Dict]) -> str:
        """Format connection types summary"""
        type_counts = {}
        for conn in connections:
            conn_type = conn.get('connection_type', 'Unknown')
            type_counts[conn_type] = type_counts.get(conn_type, 0) + 1

        formatted = ""
        for conn_type, count in type_counts.items():
            formatted += f"- **{conn_type}:** {count} connections\n"

        return formatted

    def _calculate_network_stats(self, connections: List[Dict]) -> str:
        """Calculate basic network statistics"""
        if not connections:
            return "No connections available for analysis."

        total_strength = sum(conn.get('strength', 0) for conn in connections)
        avg_strength = total_strength / len(connections) if connections else 0

        return f"""
- **Average Connection Strength:** {avg_strength:.2f}
- **Total Network Weight:** {total_strength:.1f}
- **Connection Density:** {len(connections) / 100:.2f} (normalized)
"""

    def _format_key_relationships(self, connections: List[Dict]) -> str:
        """Format top connection relationships"""
        if not connections:
            return "No key relationships identified yet."

        # Sort by strength and take top 5
        sorted_connections = sorted(connections,
                                  key=lambda x: x.get('strength', 0),
                                  reverse=True)[:5]

        formatted = ""
        for conn in sorted_connections:
            source = conn.get('source_title', 'Unknown')[:40]
            target = conn.get('target_title', 'Unknown')[:40]
            strength = conn.get('strength', 0)
            conn_type = conn.get('connection_type', 'Unknown')

            formatted += f"- **{source}** → **{target}** ({conn_type}, {strength:.1f})\n"

        return formatted

    def _format_recent_additions(self, recent: List[Dict]) -> str:
        """Format recent additions"""
        if not recent:
            return "No recent additions."

        formatted = ""
        for item in recent[-5:]:  # Last 5 items
            formatted += f"- {item.get('title', 'Unknown')} ({item.get('date', 'Unknown date')})\n"

        return formatted

    def _format_priority_areas(self, priorities: List[str]) -> str:
        """Format priority research areas"""
        if not priorities:
            return "Priority areas need identification."

        formatted = ""
        for priority in priorities:
            formatted += f"- {priority}\n"

        return formatted

def test_obsidian_generator():
    """Test Obsidian vault generator"""
    print("TEST 4/5: Obsidian Vault Generator Test")
    print("=" * 50)

    generator = CompensationObsidianGenerator("Test-Compensation-Vault")

    # Test 1: Create vault structure
    print("Step 1: Creating vault structure...")
    if generator.create_vault_structure():
        print("   SUCCESS: Vault structure created")
    else:
        print("   FAILED: Vault structure creation failed")
        return False

    # Test 2: Generate sample paper file
    print("Step 2: Generating sample paper file...")
    sample_paper = {
        "display_name": "Gluteus medius weakness and compensation patterns in hip pathology",
        "publication_year": 2020,
        "authorships": [{"author": {"display_name": "Neumann DA"}}],
        "primary_location": {"source": {"display_name": "Physical Therapy"}},
        "doi": "10.1093/ptj/example",
        "quality_score": 8.5,
        "cited_by_count": 45
    }

    sample_analysis = {
        "study_type": "Cross-sectional study",
        "why_levels": [
            {
                "question": "Why does hip pathology occur?",
                "answer": "Gluteus medius weakness leads to altered movement patterns",
                "evidence": "EMG analysis showed 40% reduction in gluteus medius activation"
            }
        ],
        "compensation_pattern": {
            "name": "Hip Abductor Weakness Pattern",
            "primary_dysfunction": "Gluteus medius weakness",
            "compensatory_strategy": "TFL overactivity and hip hiking"
        },
        "clinical_significance": "High clinical relevance for hip rehabilitation",
        "treatment_keypoints": ["Strengthen gluteus medius", "Address TFL tightness"]
    }

    try:
        paper_file = generator.generate_paper_file(sample_paper, sample_analysis)
        print(f"   SUCCESS: Paper file created at {paper_file}")
    except Exception as e:
        print(f"   FAILED: Paper file generation failed: {e}")
        return False

    # Test 3: Generate sample pattern file
    print("Step 3: Generating compensation pattern file...")
    sample_pattern = {
        "name": "Gluteus Medius Weakness Compensation",
        "primary_dysfunction": "Gluteus medius weakness",
        "main_compensation": "TFL overactivity",
        "frequency": "Very common",
        "evidence_level": "Strong",
        "mechanism": "Neural substitution due to weakness",
        "assessment": "Trendelenburg test, single leg squat assessment",
        "treatment": "Progressive strengthening protocol"
    }

    try:
        pattern_file = generator.generate_compensation_pattern_file(sample_pattern)
        print(f"   SUCCESS: Pattern file created at {pattern_file}")
    except Exception as e:
        print(f"   FAILED: Pattern file generation failed: {e}")
        return False

    # Test 4: Generate connection file
    print("Step 4: Generating node connection file...")
    sample_connections = [
        {
            "source_title": "Gluteus medius weakness study",
            "target_title": "TFL overactivity research",
            "connection_type": "CAUSAL",
            "strength": 8.5,
            "mechanism": "Weakness leads to compensation"
        }
    ]

    try:
        connection_file = generator.generate_node_connection_file(sample_connections)
        print(f"   SUCCESS: Connection file created at {connection_file}")
    except Exception as e:
        print(f"   FAILED: Connection file generation failed: {e}")
        return False

    # Test 5: Update dashboard
    print("Step 5: Updating research dashboard...")
    sample_stats = {
        "total_papers": 1,
        "patterns": 1,
        "connections": 1,
        "high_quality": 1,
        "recent": [{"title": "Sample paper", "date": "2024-01-01"}],
        "avg_why_depth": 3.0,
        "pattern_coverage": 85.0,
        "connection_density": 0.75,
        "priorities": ["Hip compensation mechanisms", "Treatment protocols"]
    }

    try:
        dashboard_file = generator.update_research_dashboard(sample_stats)
        print(f"   SUCCESS: Dashboard updated at {dashboard_file}")
    except Exception as e:
        print(f"   FAILED: Dashboard update failed: {e}")
        return False

    print("\n" + "=" * 50)
    print("TEST 4/5 COMPLETED - Obsidian vault generator functional")
    return True

if __name__ == "__main__":
    test_obsidian_generator()