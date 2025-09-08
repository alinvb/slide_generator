#!/usr/bin/env python3
"""
Test competitive positioning slide rendering with user data
"""

from adapters import RENDERER_MAP
from pptx import Presentation

def test_competitive_data():
    """Test competitive positioning with actual user data"""
    
    print("🔍 Testing Competitive Positioning slide...\n")
    
    # User's actual competitive data
    user_data = {
        "title": "Competitive Positioning",
        "competitors": [
            {"name": "ExxonMobil", "revenue": 509000},
            {"name": "Chevron", "revenue": 288000},
            {"name": "Shell", "revenue": 225000},
            {"name": "BP", "revenue": 103000},
            {"name": "PetroChina", "revenue": 243000},
            {"name": "TotalEnergies", "revenue": 165000}
        ],
        "assessment": [
            {
                "category": "Market Cap (2024)",
                "our_company": "$1,570B", 
                "competitor_a": "$509B",
                "competitor_b": "$288B"
            },
            {
                "category": "Oil Production",
                "our_company": "Highest, concentrated",
                "competitor_a": "Top 3, diversified", 
                "competitor_b": "Top 5, diversified"
            },
            {
                "category": "Natural Gas",
                "our_company": "Large, growing",
                "competitor_a": "Very large, global",
                "competitor_b": "Very large, global"
            }
        ]
    }
    
    print("📊 User's competitor data:")
    for comp in user_data['competitors']:
        print(f"  - {comp['name']}: ${comp['revenue']:,}M revenue")
    
    print(f"\n📋 User's assessment data format:")
    for assessment in user_data['assessment']:
        print(f"  - {assessment['category']}: {assessment['our_company']} vs {assessment['competitor_a']}")
    
    # Test what the template would actually use
    print(f"\n🔧 Testing template data extraction...")
    
    # Simulate what the template does
    competitors_from_template = user_data.get('competitors', [
        {'name': 'Central Health', 'revenue': 450},  # Default fallback
        {'name': 'HK Sanatorium', 'revenue': 380},
    ])
    
    assessment_from_template = user_data.get('assessment', [
        ["Provider", "Services", "Digital"],  # Default fallback
        ["OT&P Healthcare", "●●●●●", "●●●●"],
    ])
    
    print(f"  ✅ Competitors extracted: {len(competitors_from_template)} companies")
    print(f"      Range: {min(c['revenue'] for c in competitors_from_template):,} - {max(c['revenue'] for c in competitors_from_template):,}")
    
    print(f"  ❌ Assessment format: {type(assessment_from_template)}")
    print(f"      Expected: 2D array like [['Header1', 'Header2'], ['Row1Col1', 'Row1Col2']]") 
    print("      Actual: Object array like [{'category': 'Market Cap', 'our_company': '$1,570B'}]")
    
    # Test renderer
    try:
        renderer = RENDERER_MAP['competitive_positioning']
        test_prs = Presentation()
        
        result = renderer(data=user_data, prs=test_prs)
        test_prs.save("test_competitive.pptx")
        
        print(f"\n  ✅ Slide rendered successfully")
        print(f"  💾 Saved to: test_competitive.pptx")
        
        return True
        
    except Exception as e:
        print(f"\n  ❌ Rendering failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_competitive_data()