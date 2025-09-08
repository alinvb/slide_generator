"""
Test script to demonstrate automatic executive search functionality
Specifically testing with Arab Bank management team data
"""

from executive_search import auto_generate_management_data, ExecutiveSearchEngine

def test_arab_bank_executive_search():
    """
    Test automatic executive search with Arab Bank research data
    """
    print("🧪 TESTING EXECUTIVE SEARCH WITH ARAB BANK DATA")
    print("="*60)
    
    # Your provided Arab Bank research data
    arab_bank_research = """Based on the most recent and reliable public sources, here is a researched summary of Arab Bank's senior management and executive team for use in your pitch deck:

Management Team (2025)

Left Column Profiles:

Chief Executive Officer (Group) – Arab Bank (Amman HQ)

Oversees strategy and operations for the entire Arab Bank Group, including more than 600 branches in 27 countries.
25+ years of experience in international banking, digital transformation, and risk management.
Previously held senior roles at leading regional banks; recognized for driving innovation and profitable growth.
Led the Group through record net profit achievement in 2024 and 2025.
Holds advanced degrees in finance and international business.

Chief Financial Officer

Responsible for all financial planning, reporting, and investor relations for the Group.
Extensive background in global financial management and regulatory compliance.
Developed and implemented Group-wide cost and capital efficiency programs.
Previously served as CFO at a major MENA bank.
Certified Public Accountant (CPA) and MBA.

Chief Risk Officer

Leads enterprise-wide risk management, compliance, and anti-financial crime efforts.
20+ years' experience in credit, market, and operational risk.
Built the Group's best-in-class risk analytics and reporting systems.
Drives regulatory engagement in MENA and Europe.
Frequent speaker at regional risk and compliance forums.

Right Column Profiles:

Chief Operating Officer

Heads operations, IT, and digital banking transformation across Arab Bank's global network.
Previously COO at Emirates Islamic Bank and Board Member at Emirates NBD Egypt[1].
Led digital innovation and core banking upgrades in multiple institutions.
Expert in operational restructuring and process optimization.
Proven track record in large-scale technology deployment.

Head of Digital Banking & Innovation

Directs the group's digital banking platforms, fintech partnerships, and open banking (Omnify, Reflect, AB iHub).
15+ years in digital product development and financial technology.
Launched award-winning mobile banking and BaaS services.
Responsible for AB Ventures and ABX accelerator programs.
Holds degrees in computer science and business innovation.

Group General Counsel

Oversees all legal, regulatory, and governance matters for the Group.
Specialist in international banking law and cross-border transactions.
Advised on M&A, capital markets, and group restructuring deals.
Member of regional and international legal associations.
LLM in Corporate Law."""

    # Test the executive search engine
    search_engine = ExecutiveSearchEngine()
    
    # Test executive extraction
    print("\n🔍 EXTRACTING EXECUTIVES FROM RESEARCH...")
    executives = search_engine.extract_executive_names_from_text(arab_bank_research)
    
    print(f"✅ Found {len(executives)} executives")
    for i, exec_data in enumerate(executives, 1):
        print(f"\n{i}. {exec_data['title']}")
        print(f"   Role: {exec_data['role']}")
        print(f"   Experience: {exec_data['years_experience']}")
        print(f"   Bullets: {len(exec_data['experience_bullets'])}")
        for bullet in exec_data['experience_bullets'][:2]:  # Show first 2 bullets
            print(f"     • {bullet[:100]}...")
    
    # Test full auto-generation
    print(f"\n🚀 TESTING FULL AUTO-GENERATION...")
    management_data = auto_generate_management_data("Arab Bank", arab_bank_research)
    
    print(f"✅ Generated Management Team Data:")
    print(f"   Title: {management_data['title']}")
    print(f"   Left Column Profiles: {len(management_data['left_column_profiles'])}")
    print(f"   Right Column Profiles: {len(management_data['right_column_profiles'])}")
    print(f"   Total Executives: {management_data['total_executives']}")
    print(f"   Source: {management_data['source']}")
    
    # Show detailed profile structure
    print(f"\n📋 DETAILED PROFILE STRUCTURE:")
    if management_data['left_column_profiles']:
        sample_profile = management_data['left_column_profiles'][0]
        print(f"Sample Profile Keys: {list(sample_profile.keys())}")
        print(f"Sample Experience Bullets ({len(sample_profile.get('experience_bullets', []))}):")
        for bullet in sample_profile.get('experience_bullets', [])[:3]:
            print(f"  • {bullet}")
    
    return management_data

def test_template_generation():
    """
    Test template generation when no research data is provided
    """
    print("\n" + "="*60)
    print("🧪 TESTING TEMPLATE GENERATION (NO RESEARCH DATA)")
    print("="*60)
    
    # Test without research data
    template_data = auto_generate_management_data("Test Company Ltd")
    
    print(f"✅ Generated Template Management Team:")
    print(f"   Title: {template_data['title']}")
    print(f"   Left Column Profiles: {len(template_data['left_column_profiles'])}")
    print(f"   Right Column Profiles: {len(template_data['right_column_profiles'])}")
    print(f"   Total Executives: {template_data['total_executives']}")
    print(f"   Source: {template_data['source']}")
    
    return template_data

def test_slide_compatibility():
    """
    Test that generated data is compatible with slide templates
    """
    print("\n" + "="*60)
    print("🧪 TESTING SLIDE TEMPLATE COMPATIBILITY")
    print("="*60)
    
    # Generate data
    management_data = auto_generate_management_data("Arab Bank")
    
    # Test slide template compatibility
    from slide_templates import render_management_team_slide
    
    try:
        # Create a test presentation
        from pptx import Presentation
        prs = Presentation()
        
        # Test rendering with our generated data
        result_prs = render_management_team_slide(
            data=management_data,
            company_name="Arab Bank",
            prs=prs
        )
        
        print(f"✅ SLIDE RENDERING SUCCESSFUL!")
        print(f"   Generated {len(result_prs.slides)} slide(s)")
        print(f"   Data structure compatible with slide template")
        
        # Save test slide
        result_prs.save("test_executive_search_slide.pptx")
        print(f"   Test slide saved as: test_executive_search_slide.pptx")
        
        return True
        
    except Exception as e:
        print(f"❌ SLIDE RENDERING FAILED: {e}")
        return False

if __name__ == "__main__":
    print("🚀 EXECUTIVE SEARCH ENGINE TESTS")
    print("="*60)
    
    # Test 1: Arab Bank data extraction
    arab_bank_data = test_arab_bank_executive_search()
    
    # Test 2: Template generation
    template_data = test_template_generation()
    
    # Test 3: Slide compatibility
    slide_success = test_slide_compatibility()
    
    print("\n" + "="*60)
    print("📊 TEST SUMMARY")
    print("="*60)
    print(f"✅ Arab Bank Data Extraction: {len(arab_bank_data['left_column_profiles']) + len(arab_bank_data['right_column_profiles'])} executives")
    print(f"✅ Template Generation: {len(template_data['left_column_profiles']) + len(template_data['right_column_profiles'])} executives")
    print(f"{'✅' if slide_success else '❌'} Slide Template Compatibility: {'PASSED' if slide_success else 'FAILED'}")
    
    print(f"\n🎯 AUTOMATIC EXECUTIVE SEARCH IS {'WORKING' if slide_success else 'NEEDS FIXES'}")