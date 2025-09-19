#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manual Test: Check if paper screening actually works
"""

import requests
import json
from datetime import datetime

def test_openalex_api():
    """Test if OpenAlex API actually returns papers"""
    print("🔍 Testing OpenAlex API...")

    api_base = "https://api.openalex.org/works"
    headers = {"User-Agent": "Compensation-Research-Bot/1.0 (+compensation@research.edu)"}

    query = "compensation AND (physical therapy OR physiotherapy)"

    params = {
        "search": query,
        "filter": [
            "type:article",
            "from_publication_date:2020-01-01",
            "cited_by_count:>0"
        ],
        "per_page": 3,
        "select": [
            "id", "doi", "title", "display_name",
            "publication_year", "cited_by_count",
            "abstract_inverted_index"
        ]
    }

    try:
        response = requests.get(api_base, params=params, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()

        papers = data.get("results", [])
        print(f"✅ API Success: Found {len(papers)} papers")

        for i, paper in enumerate(papers, 1):
            print(f"\nPaper {i}:")
            print(f"   Title: {paper.get('display_name', 'N/A')[:80]}...")
            print(f"   Year: {paper.get('publication_year', 'N/A')}")
            print(f"   Citations: {paper.get('cited_by_count', 0)}")

        return True, papers

    except Exception as e:
        print(f"❌ API Failed: {e}")
        return False, []

def create_real_content():
    """Create actual content from real data"""
    print("\n🔧 Creating real content...")

    success, papers = test_openalex_api()

    if success and papers:
        # Create HTML with real data
        timestamp = datetime.now().strftime("%Y년 %m월 %d일 %H:%M")

        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>보상작용 연구 - 실제 데이터</title>
    <meta charset="utf-8">
</head>
<body>
    <h1>🔬 실제 보상작용 연구 데이터</h1>
    <p><strong>마지막 업데이트:</strong> {timestamp}</p>
    <p><strong>실제 논문 수:</strong> {len(papers)}개</p>

    <h2>최신 논문들:</h2>
"""

        for i, paper in enumerate(papers, 1):
            title = paper.get('display_name', 'N/A')
            year = paper.get('publication_year', 'N/A')
            citations = paper.get('cited_by_count', 0)

            html_content += f"""
    <div style="border: 1px solid #ccc; padding: 10px; margin: 10px 0;">
        <h3>논문 {i}: {title[:100]}...</h3>
        <p>연도: {year} | 인용수: {citations}</p>
    </div>
"""

        html_content += """
</body>
</html>
"""

        # Save real content
        with open("docs/real-data.html", "w", encoding="utf-8") as f:
            f.write(html_content)

        print(f"✅ Real content saved to docs/real-data.html")
        print(f"📊 {len(papers)} actual papers processed")

        return True
    else:
        print("❌ Could not create real content - API failed")
        return False

if __name__ == "__main__":
    print("🚀 Manual Test Started")
    print("=" * 50)

    result = create_real_content()

    if result:
        print("\n✅ SUCCESS: Real data system working!")
        print("Visit: docs/real-data.html to see actual results")
    else:
        print("\n❌ FAILED: System not working properly")