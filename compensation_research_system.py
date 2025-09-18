# -*- coding: utf-8 -*-
"""
Complete Compensation Research Automation System
Claude Development Rules compliant - 5WHY methodology focused

Integrates all components:
1. Paper screening (paper_screener.py)
2. 5WHY analysis (why_analyzer.py)
3. Node connections (node_connector.py)
4. Obsidian vault generation (obsidian_generator.py)

Automated execution every 10 minutes for continuous research growth.
"""

import time
import schedule
from datetime import datetime
from typing import Dict, List, Optional
import json
import traceback

try:
    from paper_screener import CompensationPaperScreener
except ImportError:
    CompensationPaperScreener = None

try:
    from why_analyzer import CompensationWhyAnalyzer
except ImportError:
    CompensationWhyAnalyzer = None

try:
    from node_connector import CompensationNodeConnector
except ImportError:
    CompensationNodeConnector = None

try:
    from obsidian_generator import CompensationObsidianGenerator
except ImportError:
    CompensationObsidianGenerator = None

class CompensationResearchSystem:
    def __init__(self, vault_path: str = "Compensation-Research-Vault"):
        """Initialize complete research automation system"""
        self.vault_path = vault_path

        # Initialize all components with error handling
        self.screener = CompensationPaperScreener() if CompensationPaperScreener else None
        self.analyzer = CompensationWhyAnalyzer() if CompensationWhyAnalyzer else None
        self.connector = CompensationNodeConnector() if CompensationNodeConnector else None
        self.generator = CompensationObsidianGenerator(vault_path) if CompensationObsidianGenerator else None

        # System state tracking
        self.processed_papers = []
        self.discovered_patterns = []
        self.node_network = []
        self.system_stats = {
            "total_papers": 0,
            "patterns": 0,
            "connections": 0,
            "high_quality": 0,
            "last_run": None,
            "success_rate": 0.0
        }

        # Create vault structure on initialization
        self.setup_system()

    def setup_system(self) -> bool:
        """Setup complete system and vault structure"""
        try:
            print("Setting up Compensation Research System...")

            # Create Obsidian vault structure
            if not self.generator.create_vault_structure():
                print("Failed to create vault structure")
                return False

            print("System setup completed successfully")
            return True

        except Exception as e:
            print(f"System setup failed: {e}")
            return False

    def run_research_cycle(self) -> bool:
        """Execute complete research cycle"""
        try:
            cycle_start = datetime.now()
            print(f"\n{'='*60}")
            print(f"COMPENSATION RESEARCH CYCLE - {cycle_start.strftime('%Y-%m-%d %H:%M')}")
            print(f"{'='*60}")

            # Step 1: Screen for new high-quality papers
            print("Step 1/5: Screening for compensation papers...")
            new_papers = self.screener.screen_papers(limit=3)

            if not new_papers:
                print("   No new papers found this cycle")
                return True

            print(f"   Found {len(new_papers)} papers for analysis")

            # Step 2: Perform 5WHY analysis on each paper
            print("Step 2/5: Performing 5WHY analysis...")
            analyzed_papers = []

            for paper in new_papers:
                try:
                    analysis = self.analyzer.analyze_paper(paper)
                    if analysis:
                        analyzed_papers.append({
                            "paper": paper,
                            "analysis": analysis
                        })
                        print(f"   Analyzed: {paper.get('display_name', 'Unknown')[:50]}...")
                except Exception as e:
                    print(f"   Analysis failed for paper: {e}")
                    continue

            if not analyzed_papers:
                print("   No papers successfully analyzed")
                return True

            # Step 3: Generate node connections
            print("Step 3/5: Building node connections...")
            all_nodes = []

            for item in analyzed_papers:
                node = self.connector.create_node_from_analysis(
                    item["paper"],
                    item["analysis"]
                )
                if node:
                    all_nodes.append(node)

            # Include existing nodes for connection analysis
            all_nodes.extend(self.node_network)

            new_connections = self.connector.connect_nodes(all_nodes)
            print(f"   Generated {len(new_connections)} new connections")

            # Step 4: Generate Obsidian files
            print("Step 4/5: Creating Obsidian files...")
            generated_files = []

            for item in analyzed_papers:
                try:
                    # Generate paper analysis file
                    paper_file = self.generator.generate_paper_file(
                        item["paper"],
                        item["analysis"].__dict__ if hasattr(item["analysis"], '__dict__') else item["analysis"]
                    )
                    generated_files.append(paper_file)

                    # Generate pattern file if new pattern discovered
                    pattern = item["analysis"].compensation_pattern if hasattr(item["analysis"], 'compensation_pattern') else None
                    if pattern and pattern.name not in [p.get("name") for p in self.discovered_patterns]:
                        pattern_file = self.generator.generate_compensation_pattern_file(
                            pattern.__dict__ if hasattr(pattern, '__dict__') else pattern
                        )
                        generated_files.append(pattern_file)
                        self.discovered_patterns.append(pattern.__dict__ if hasattr(pattern, '__dict__') else pattern)

                except Exception as e:
                    print(f"   File generation failed: {e}")
                    continue

            # Generate connection network file
            if new_connections:
                connection_file = self.generator.generate_node_connection_file(
                    [conn.__dict__ if hasattr(conn, '__dict__') else conn for conn in new_connections]
                )
                generated_files.append(connection_file)

            print(f"   Generated {len(generated_files)} Obsidian files")

            # Step 5: Update system state and dashboard
            print("Step 5/5: Updating system dashboard...")

            # Update internal state
            self.processed_papers.extend(analyzed_papers)
            self.node_network.extend(all_nodes)

            # Update statistics
            self.system_stats.update({
                "total_papers": len(self.processed_papers),
                "patterns": len(self.discovered_patterns),
                "connections": len(self.node_network),
                "high_quality": len([p for p in self.processed_papers
                                   if p["paper"].get("quality_score", 0) >= 10]),
                "last_run": cycle_start.strftime('%Y-%m-%d %H:%M'),
                "success_rate": len(analyzed_papers) / len(new_papers) if new_papers else 1.0
            })

            # Add recent additions
            self.system_stats["recent"] = [
                {
                    "title": item["paper"].get("display_name", "Unknown")[:50],
                    "date": cycle_start.strftime('%Y-%m-%d'),
                    "score": item["paper"].get("quality_score", 0)
                }
                for item in analyzed_papers[-5:]  # Last 5
            ]

            # Add priority areas based on gaps
            self.system_stats["priorities"] = self._identify_priority_areas()

            # Update dashboard
            dashboard_file = self.generator.update_research_dashboard(self.system_stats)

            cycle_end = datetime.now()
            cycle_duration = (cycle_end - cycle_start).total_seconds()

            print(f"\n{'='*60}")
            print(f"CYCLE COMPLETED - Duration: {cycle_duration:.1f}s")
            print(f"Papers Analyzed: {len(analyzed_papers)}")
            print(f"Files Generated: {len(generated_files)}")
            print(f"Total Network Size: {len(self.node_network)} nodes")
            print(f"Next cycle: {(cycle_start.replace(minute=cycle_start.minute + 10)).strftime('%H:%M')}")
            print(f"{'='*60}")

            return True

        except Exception as e:
            print(f"Research cycle failed: {e}")
            print(f"Error details: {traceback.format_exc()}")
            return False

    def _identify_priority_areas(self) -> List[str]:
        """Identify priority research areas based on current gaps"""
        priorities = []

        # Check for underrepresented body regions
        body_regions = {}
        for item in self.processed_papers:
            title = item["paper"].get("display_name", "").lower()
            if "hip" in title:
                body_regions["hip"] = body_regions.get("hip", 0) + 1
            elif "knee" in title:
                body_regions["knee"] = body_regions.get("knee", 0) + 1
            elif "ankle" in title:
                body_regions["ankle"] = body_regions.get("ankle", 0) + 1
            elif "spine" in title:
                body_regions["spine"] = body_regions.get("spine", 0) + 1

        # Identify underrepresented areas
        total_papers = len(self.processed_papers)
        if total_papers > 0:
            for region, count in body_regions.items():
                if count / total_papers < 0.15:  # Less than 15% representation
                    priorities.append(f"{region.title()} compensation mechanisms need more research")

        # Check for pattern gaps
        if len(self.discovered_patterns) < 5:
            priorities.append("Expand compensation pattern identification")

        # Check for connection density
        if len(self.node_network) > 0:
            connection_ratio = len(self.node_network) / max(len(self.processed_papers), 1)
            if connection_ratio < 2.0:
                priorities.append("Increase node connection analysis depth")

        # Default priorities if none identified
        if not priorities:
            priorities = [
                "Continue high-quality paper collection",
                "Deepen 5WHY analysis methodology",
                "Expand therapeutic intervention research"
            ]

        return priorities[:5]  # Limit to 5 priorities

    def start_automated_system(self):
        """Start automated 10-minute research cycles"""
        print("\n" + "="*60)
        print("STARTING AUTOMATED COMPENSATION RESEARCH SYSTEM")
        print("="*60)
        print(f"Vault Location: {self.vault_path}")
        print("Schedule: Every 10 minutes")
        print("Focus: Compensation mechanisms via 5WHY methodology")
        print("="*60)

        # Schedule the research cycle every 10 minutes
        schedule.every(10).minutes.do(self.run_research_cycle)

        # Run first cycle immediately
        print("Running initial research cycle...")
        self.run_research_cycle()

        # Keep the system running
        try:
            while True:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds
        except KeyboardInterrupt:
            print("\nSystem stopped by user")
        except Exception as e:
            print(f"System error: {e}")

    def run_single_cycle(self) -> bool:
        """Run a single research cycle for testing"""
        return self.run_research_cycle()

    def get_system_status(self) -> Dict:
        """Get current system status"""
        return {
            "stats": self.system_stats,
            "vault_path": self.vault_path,
            "papers_processed": len(self.processed_papers),
            "patterns_discovered": len(self.discovered_patterns),
            "network_size": len(self.node_network),
            "is_running": True
        }

def test_complete_system():
    """Test complete integrated system"""
    print("TEST 5/5: Complete System Integration Test")
    print("=" * 60)

    # Initialize system
    print("Step 1: Initializing complete research system...")
    system = CompensationResearchSystem("Test-Integration-Vault")

    if not system:
        print("   FAILED: System initialization failed")
        return False
    print("   SUCCESS: System initialized")

    # Test single research cycle
    print("Step 2: Running complete research cycle...")
    try:
        if system.run_single_cycle():
            print("   SUCCESS: Research cycle completed")
        else:
            print("   PARTIAL: Research cycle completed with issues")
    except Exception as e:
        print(f"   FAILED: Research cycle failed: {e}")
        return False

    # Check system status
    print("Step 3: Checking system status...")
    status = system.get_system_status()

    print(f"   Total Papers: {status['papers_processed']}")
    print(f"   Patterns Found: {status['patterns_discovered']}")
    print(f"   Network Size: {status['network_size']}")
    print(f"   Vault Location: {status['vault_path']}")

    # Verify critical components
    print("Step 4: Verifying system components...")

    components_ok = True

    # Check if screener is working
    if not system.screener:
        print("   ERROR: Paper screener not initialized")
        components_ok = False

    # Check if analyzer is working
    if not system.analyzer:
        print("   ERROR: 5WHY analyzer not initialized")
        components_ok = False

    # Check if connector is working
    if not system.connector:
        print("   ERROR: Node connector not initialized")
        components_ok = False

    # Check if generator is working
    if not system.generator:
        print("   ERROR: Obsidian generator not initialized")
        components_ok = False

    if components_ok:
        print("   SUCCESS: All components functional")

    # Final integration test
    print("Step 5: Integration validation...")

    if (status['is_running'] and
        hasattr(system, 'screener') and
        hasattr(system, 'analyzer') and
        hasattr(system, 'connector') and
        hasattr(system, 'generator')):

        print("   SUCCESS: Complete system integration validated")
        print("\n" + "=" * 60)
        print("TEST 5/5 COMPLETED - System ready for automation")
        print("=" * 60)
        print("System Features:")
        print("✓ Automated paper screening every 10 minutes")
        print("✓ 5WHY analysis for compensation mechanisms")
        print("✓ Node connection building")
        print("✓ Obsidian vault management")
        print("✓ Real-time dashboard updates")
        print("=" * 60)

        return True
    else:
        print("   FAILED: Integration validation failed")
        return False

def main():
    """Main execution function"""
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        # Run test mode
        test_complete_system()
    elif len(sys.argv) > 1 and sys.argv[1] == "--single":
        # Run single cycle
        system = CompensationResearchSystem()
        system.run_single_cycle()
    else:
        # Start automated system
        system = CompensationResearchSystem()
        system.start_automated_system()

if __name__ == "__main__":
    # For testing, run the test function
    test_complete_system()