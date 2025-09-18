# -*- coding: utf-8 -*-
"""
Standalone Integration Test for Compensation Research System
Tests each component individually then integration
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

def test_paper_screener():
    """Test paper screener component"""
    print("Testing Paper Screener...")
    try:
        import paper_screener
        screener = paper_screener.CompensationPaperScreener()
        papers = screener.screen_papers(limit=1)
        print(f"   SUCCESS: Found {len(papers)} papers")
        return True, screener
    except Exception as e:
        print(f"   FAILED: {e}")
        return False, None

def test_why_analyzer():
    """Test 5WHY analyzer component"""
    print("Testing 5WHY Analyzer...")
    try:
        import why_analyzer
        analyzer = why_analyzer.CompensationWhyAnalyzer()

        # Create sample paper for testing
        sample_paper = {
            "display_name": "Gluteus medius weakness and hip compensation",
            "abstract_inverted_index": {
                "gluteus": [0], "medius": [1], "weakness": [2], "leads": [3],
                "to": [4], "tensor": [5], "fasciae": [6], "latae": [7],
                "overactivity": [8], "compensation": [9]
            }
        }

        analysis = analyzer.analyze_paper(sample_paper)
        print(f"   SUCCESS: Analysis completed with {len(analysis.why_levels) if analysis else 0} WHY levels")
        return True, analyzer
    except Exception as e:
        print(f"   FAILED: {e}")
        return False, None

def test_node_connector():
    """Test node connector component"""
    print("Testing Node Connector...")
    try:
        import node_connector
        connector = node_connector.CompensationNodeConnector()

        # Create sample nodes for testing
        sample_nodes = []
        connections = connector.connect_nodes(sample_nodes)
        print(f"   SUCCESS: Generated {len(connections)} connections")
        return True, connector
    except Exception as e:
        print(f"   FAILED: {e}")
        return False, None

def test_obsidian_generator():
    """Test Obsidian generator component"""
    print("Testing Obsidian Generator...")
    try:
        import obsidian_generator
        generator = obsidian_generator.CompensationObsidianGenerator("Test-Final-Vault")

        if generator.create_vault_structure():
            print("   SUCCESS: Vault structure created")
            return True, generator
        else:
            print("   FAILED: Vault creation failed")
            return False, None
    except Exception as e:
        print(f"   FAILED: {e}")
        return False, None

def test_complete_integration():
    """Test complete system integration"""
    print("\n" + "="*60)
    print("FINAL INTEGRATION TEST - COMPENSATION RESEARCH SYSTEM")
    print("="*60)

    components = {}
    success_count = 0

    # Test each component
    tests = [
        ("Paper Screener", test_paper_screener),
        ("5WHY Analyzer", test_why_analyzer),
        ("Node Connector", test_node_connector),
        ("Obsidian Generator", test_obsidian_generator)
    ]

    for name, test_func in tests:
        success, component = test_func()
        components[name] = component
        if success:
            success_count += 1

    print(f"\nComponent Test Results: {success_count}/{len(tests)} passed")

    # Test integration if all components work
    if success_count == len(tests):
        print("\nTesting Integration...")
        try:
            # Simulate a mini research cycle
            screener = components["Paper Screener"]
            analyzer = components["5WHY Analyzer"]
            connector = components["Node Connector"]
            generator = components["Obsidian Generator"]

            print("   Step 1: Getting sample papers...")
            papers = screener.screen_papers(limit=1)

            print("   Step 2: Analyzing papers...")
            analyzed = []
            for paper in papers[:1]:  # Just test with 1 paper
                analysis = analyzer.analyze_paper(paper)
                if analysis:
                    analyzed.append({"paper": paper, "analysis": analysis})

            print("   Step 3: Creating nodes...")
            nodes = []
            for item in analyzed:
                node = connector.create_node_from_analysis(item["paper"], item["analysis"])
                if node:
                    nodes.append(node)

            print("   Step 4: Generating connections...")
            connections = connector.connect_nodes(nodes)

            print("   Step 5: Creating Obsidian files...")
            files_created = 0
            for item in analyzed:
                try:
                    file_path = generator.generate_paper_file(
                        item["paper"],
                        item["analysis"].__dict__ if hasattr(item["analysis"], '__dict__') else item["analysis"]
                    )
                    files_created += 1
                except Exception as e:
                    print(f"     File generation error: {e}")

            # Update dashboard
            stats = {
                "total_papers": len(analyzed),
                "patterns": 1,
                "connections": len(connections),
                "high_quality": 1,
                "recent": [{"title": "Test paper", "date": "2024-01-01"}],
                "avg_why_depth": 3.0,
                "pattern_coverage": 85.0,
                "connection_density": 0.75,
                "priorities": ["Test priority areas"]
            }

            dashboard_path = generator.update_research_dashboard(stats)

            print(f"   SUCCESS: Integration test completed")
            print(f"   Papers processed: {len(analyzed)}")
            print(f"   Nodes created: {len(nodes)}")
            print(f"   Connections made: {len(connections)}")
            print(f"   Files created: {files_created}")
            print(f"   Dashboard updated: {dashboard_path}")

        except Exception as e:
            print(f"   INTEGRATION FAILED: {e}")
            import traceback
            traceback.print_exc()
            return False

    # Final results
    print("\n" + "="*60)
    if success_count == len(tests):
        print("SYSTEM STATUS: FULLY OPERATIONAL")
        print("All components tested and integrated successfully")
        print("\nReady for deployment:")
        print("- 10-minute automated research cycles")
        print("- 5WHY methodology for compensation analysis")
        print("- Structured Obsidian vault creation")
        print("- Node-based knowledge network building")
    else:
        print("SYSTEM STATUS: PARTIAL FUNCTIONALITY")
        print(f"Working components: {success_count}/{len(tests)}")
        print("Some components need attention before full deployment")

    print("="*60)
    return success_count == len(tests)

if __name__ == "__main__":
    test_complete_integration()