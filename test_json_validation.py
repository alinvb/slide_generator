#!/usr/bin/env python3

"""
Test JSON Validation
===================
Tests that the generated PRYPCO slides pass all validation requirements:
1. No empty/placeholder fields
2. All required fields present
3. Proper data structure
4. Ready for slide generation
"""

import sys
import os
import json
sys.path.append('/home/user/webapp')

from bulletproof_json_generator import BulletproofJSONGenerator

def validate_slide_data(slide_data, template_name):
    """Validate individual slide data"""
    
    issues = []
    warnings = []
    
    # Check basic structure
    if not slide_data.get("title"):
        issues.append("Missing title")
    
    # Template-specific validation
    if template_name == "business_overview":
        required_fields = ["company_name", "description"]
        for field in required_fields:
            if not slide_data.get(field):
                issues.append(f"Missing {field}")
        
        # Check for placeholder values
        company_name = slide_data.get("company_name", "")
        description = slide_data.get("description", "")
        
        if company_name in ["Company Name", "company name"]:
            issues.append("Placeholder company name")
        
        if "business description" in description.lower():
            warnings.append("Generic business description")
            
        if len(description) < 50:
            warnings.append("Very short description")
    
    elif template_name == "product_service_footprint":
        services = slide_data.get("services", [])
        if not services:
            issues.append("No services provided")
        elif isinstance(services, list):
            for i, service in enumerate(services):
                if isinstance(service, dict):
                    if not service.get("title") or service.get("title") in ["Service 1", "Service 2"]:
                        issues.append(f"Placeholder service title #{i+1}")
                    if not service.get("desc") or service.get("desc") == "Description":
                        issues.append(f"Placeholder service description #{i+1}")
        
        coverage_table = slide_data.get("coverage_table", [])
        if not coverage_table or len(coverage_table) < 2:
            warnings.append("Minimal coverage table data")
    
    elif template_name == "management_team":
        left_profiles = slide_data.get("left_column_profiles", [])
        right_profiles = slide_data.get("right_column_profiles", [])
        
        if not left_profiles and not right_profiles:
            issues.append("No team profiles provided")
        
        for profiles, side in [(left_profiles, "left"), (right_profiles, "right")]:
            for i, profile in enumerate(profiles):
                if isinstance(profile, dict):
                    name = profile.get("name", "")
                    if not name or name in ["CEO Name", "CTO Name", "Executive"]:
                        issues.append(f"Placeholder name in {side} column #{i+1}")
    
    elif template_name == "historical_financial_performance":
        chart = slide_data.get("chart", {})
        if not chart:
            issues.append("No chart data")
        else:
            categories = chart.get("categories", [])
            revenue = chart.get("revenue", [])
            if len(categories) != len(revenue):
                issues.append("Chart data mismatch (categories vs revenue)")
        
        key_metrics = slide_data.get("key_metrics", {}).get("metrics", [])
        if not key_metrics:
            warnings.append("No key metrics provided")
    
    return issues, warnings

def test_prypco_json_validation():
    """Test JSON validation with PRYPCO data"""
    
    print("🧪 Testing JSON Validation for PRYPCO...")
    
    # Generate PRYPCO slides
    prypco_messages = [
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "prypco"},
        {"role": "assistant", "content": "PRYPCO is a real estate technology platform based in Dubai..."},
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
        {"role": "user", "content": "research this yourself"},
        {"role": "assistant", "content": "PRYPCO offers: PRYPCO Blocks, PRYPCO Mint, PRYPCO One..."}
    ]
    
    def mock_llm_call(messages, model="test", api_key="test", service="test"):
        return json.dumps({
            "company_name": "PRYPCO",
            "description": "PRYPCO is a real estate technology platform based in Dubai that specializes in making property investment, mortgage acquisition, and visa facilitation accessible and streamlined for both residents and international investors",
            "founded": "2022",
            "headquarters": "Dubai, UAE",
            "key_milestones": [
                "Founded by Amira Sajwani in 2022",
                "Facilitated $2.73 billion in mortgages",
                "Helped 3,000+ individuals secure UAE Golden Visas"
            ],
            "team_members": [{
                "name": "Amira Sajwani",
                "title": "Founder & CEO", 
                "background": "Previously oversaw sales and development at DAMAC Properties"
            }],
            "products_services": [
                "PRYPCO Blocks - Fractional ownership platform enabling users to invest in real estate with low minimum capital",
                "PRYPCO Mint - Tokenized real estate investment platform allowing fractional property ownership via blockchain",
                "PRYPCO One - Platform for real estate agents with AI-driven market insights"
            ],
            "market_coverage": "UAE and MENA region"
        })
    
    try:
        # Generate slides
        generator = BulletproofJSONGenerator()
        all_slides = ["business_overview", "product_service_footprint", "management_team", "historical_financial_performance"]
        
        extracted_data = generator.extract_conversation_data(prypco_messages, mock_llm_call)
        covered_slides = generator.filter_slides_by_conversation_coverage(extracted_data, all_slides)
        response, content_ir, render_plan = generator.generate_perfect_jsons(extracted_data, {}, covered_slides)
        
        print(f"\n📊 Generated {len(render_plan['slides'])} slides for validation")
        
        # Validate each slide
        total_issues = 0
        total_warnings = 0
        
        for i, slide in enumerate(render_plan['slides']):
            template_name = slide['template']
            slide_data = slide['data']
            
            print(f"\n🔍 Slide {i+1}: {template_name}")
            
            issues, warnings = validate_slide_data(slide_data, template_name)
            
            if not issues and not warnings:
                print(f"   ✅ Perfect - No issues found")
            else:
                if issues:
                    print(f"   ❌ {len(issues)} critical issue(s):")
                    for issue in issues:
                        print(f"      • {issue}")
                    total_issues += len(issues)
                
                if warnings:
                    print(f"   ⚠️  {len(warnings)} warning(s):")
                    for warning in warnings:
                        print(f"      • {warning}")
                    total_warnings += len(warnings)
        
        # Overall validation result
        print(f"\n📋 OVERALL VALIDATION RESULTS:")
        print(f"   Total slides: {len(render_plan['slides'])}")
        print(f"   Critical issues: {total_issues}")
        print(f"   Warnings: {total_warnings}")
        
        if total_issues == 0:
            print(f"   ✅ VALIDATION PASSED - Ready for slide generation")
            return True
        else:
            print(f"   ❌ VALIDATION FAILED - {total_issues} critical issues must be fixed")
            return False
    
    except Exception as e:
        print(f"❌ Validation test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🎯 JSON VALIDATION TEST")
    print("=" * 60)
    print("Testing generated slides for validation compliance")
    print("Checking for placeholders, missing fields, and data quality")
    print("=" * 60)
    
    success = test_prypco_json_validation()
    
    print(f"\n" + "=" * 60)
    if success:
        print("🎉 VALIDATION SUCCESSFUL!")
        print("✅ All slides pass validation requirements")
        print("✅ No placeholders or empty fields detected") 
        print("✅ Ready for PowerPoint generation")
    else:
        print("⚠️  VALIDATION ISSUES DETECTED")
        print("❌ Some slides have validation problems")
        print("❌ Must fix issues before slide generation")
    print("=" * 60)