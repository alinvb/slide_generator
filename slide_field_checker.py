#!/usr/bin/env python3
"""
Simple slide field checker using existing test data
"""

import json
import sys

def load_test_content_ir():
    """Load test content_ir data"""
    try:
        with open('/home/user/webapp/working_content_ir_example.json', 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Could not load test data: {e}")
        return None

def check_slide_1_executive_summary(content_ir):
    """Check Slide 1: Executive Summary fields"""
    print("🔍 SLIDE 1: EXECUTIVE SUMMARY")
    print("=" * 40)
    
    # Expected fields for Executive Summary slide
    required_fields = {
        'company_overview': ['entities', 'company', 'name'],
        'investment_highlights': ['facts', 'investment_highlights'],  
        'key_financial_metrics': ['facts'],
        'revenue_data': ['facts', 'revenue_usd_m'],
        'ebitda_data': ['facts', 'ebitda_usd_m'],
        'years': ['facts', 'years'],
        'ebitda_margins': ['facts', 'ebitda_margins']
    }
    
    results = {}
    
    for field_name, path in required_fields.items():
        print(f"Checking {field_name}:")
        
        # Navigate to the field
        current = content_ir
        found = True
        
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                found = False
                break
                
        if found and current is not None:
            # Check if field has meaningful data
            if isinstance(current, list) and len(current) > 0:
                print(f"  ✅ {field_name}: List with {len(current)} items")
                results[field_name] = True
            elif isinstance(current, dict) and len(current) > 0:
                print(f"  ✅ {field_name}: Dict with {len(current)} keys")
                results[field_name] = True
            elif isinstance(current, str) and current.strip():
                print(f"  ✅ {field_name}: '{current}'")
                results[field_name] = True
            elif isinstance(current, (int, float)) and current != 0:
                print(f"  ✅ {field_name}: {current}")
                results[field_name] = True
            else:
                print(f"  ❌ {field_name}: Empty or invalid data")
                results[field_name] = False
        else:
            print(f"  ❌ {field_name}: Field not found")
            results[field_name] = False
    
    # Summary
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nSlide 1 Summary: {passed}/{total} fields populated")
    return results

def check_slide_2_business_overview(content_ir):
    """Check Slide 2: Business Overview fields"""
    print("\n🔍 SLIDE 2: BUSINESS OVERVIEW")
    print("=" * 40)
    
    required_fields = {
        'company_name': ['entities', 'company', 'name'],
        'business_description': ['entities', 'company', 'description'],
        'services_offered': ['services'],  # This may need to be extracted
        'key_highlights': ['highlights'],  # This may need to be extracted  
        'market_position': ['market_position']  # This may need to be extracted
    }
    
    results = {}
    
    for field_name, path in required_fields.items():
        print(f"Checking {field_name}:")
        
        # Navigate to the field
        current = content_ir
        found = True
        
        for key in path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                found = False
                break
                
        if found and current is not None:
            if isinstance(current, (list, dict)) and len(current) > 0:
                print(f"  ✅ {field_name}: Data present")
                results[field_name] = True
            elif isinstance(current, str) and current.strip():
                print(f"  ✅ {field_name}: '{current[:50]}...'")
                results[field_name] = True
            else:
                print(f"  ❌ {field_name}: Empty data")
                results[field_name] = False
        else:
            print(f"  ❌ {field_name}: Field not found")
            results[field_name] = False
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nSlide 2 Summary: {passed}/{total} fields populated")
    return results

def check_slide_7_strategic_buyers(content_ir):
    """Check Slide 7: Strategic Buyers fields"""
    print("\n🔍 SLIDE 7: STRATEGIC BUYERS")
    print("=" * 40)
    
    strategic_buyers = content_ir.get('strategic_buyers', [])
    
    if not strategic_buyers:
        print("❌ No strategic buyers found")
        return {'strategic_buyers': False}
    
    print(f"Found {len(strategic_buyers)} strategic buyers")
    
    # Check each buyer has required fields
    required_buyer_fields = ['buyer_name', 'description', 'strategic_rationale', 'key_synergies', 'fit', 'financial_capacity']
    
    all_buyers_complete = True
    
    for i, buyer in enumerate(strategic_buyers):
        print(f"\nBuyer {i+1}: {buyer.get('buyer_name', 'Unknown')}")
        
        for field in required_buyer_fields:
            if field in buyer and buyer[field] and str(buyer[field]).strip():
                print(f"  ✅ {field}: Present")
            else:
                print(f"  ❌ {field}: Missing or empty")
                all_buyers_complete = False
    
    results = {'strategic_buyers': all_buyers_complete}
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nSlide 7 Summary: {passed}/{total} sections populated")
    return results

def check_slide_8_financial_buyers(content_ir):
    """Check Slide 8: Financial Buyers fields"""
    print("\n🔍 SLIDE 8: FINANCIAL BUYERS")
    print("=" * 40)
    
    financial_buyers = content_ir.get('financial_buyers', [])
    
    if not financial_buyers:
        print("❌ No financial buyers found")
        return {'financial_buyers': False}
    
    print(f"Found {len(financial_buyers)} financial buyers")
    
    # Check each buyer has required fields
    required_buyer_fields = ['buyer_name', 'description', 'strategic_rationale', 'key_synergies', 'fit', 'financial_capacity']
    
    all_buyers_complete = True
    
    for i, buyer in enumerate(financial_buyers):
        print(f"\nBuyer {i+1}: {buyer.get('buyer_name', 'Unknown')}")
        
        for field in required_buyer_fields:
            if field in buyer and buyer[field] and str(buyer[field]).strip():
                print(f"  ✅ {field}: Present")
            else:
                print(f"  ❌ {field}: Missing or empty")
                all_buyers_complete = False
    
    results = {'financial_buyers': all_buyers_complete}
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nSlide 8 Summary: {passed}/{total} sections populated")
    return results

def check_slide_9_management_team(content_ir):
    """Check Slide 9: Management Team fields"""
    print("\n🔍 SLIDE 9: MANAGEMENT TEAM")
    print("=" * 40)
    
    mgmt_team = content_ir.get('management_team', {})
    
    if not mgmt_team:
        print("❌ No management team found")
        return {'management_team': False}
    
    # Check left and right column profiles
    left_profiles = mgmt_team.get('left_column_profiles', [])
    right_profiles = mgmt_team.get('right_column_profiles', [])
    
    print(f"Left column profiles: {len(left_profiles)}")
    print(f"Right column profiles: {len(right_profiles)}")
    
    results = {}
    
    # Check left column
    if left_profiles:
        print("\nLeft Column:")
        for i, profile in enumerate(left_profiles):
            name = profile.get('name', 'Unknown')
            role = profile.get('role_title', 'No role')
            bullets = profile.get('experience_bullets', [])
            
            print(f"  Profile {i+1}: {name} - {role}")
            print(f"    ✅ Experience bullets: {len(bullets)}")
        results['left_profiles'] = True
    else:
        print("  ❌ Left column profiles: Empty")
        results['left_profiles'] = False
    
    # Check right column  
    if right_profiles:
        print("\nRight Column:")
        for i, profile in enumerate(right_profiles):
            name = profile.get('name', 'Unknown')
            role = profile.get('role_title', 'No role')
            bullets = profile.get('experience_bullets', [])
            
            print(f"  Profile {i+1}: {name} - {role}")
            print(f"    ✅ Experience bullets: {len(bullets)}")
        results['right_profiles'] = True
    else:
        print("  ❌ Right column profiles: Empty")
        results['right_profiles'] = False
    
    passed = sum(results.values())
    total = len(results)
    
    print(f"\nSlide 9 Summary: {passed}/{total} sections populated")
    return results

def main():
    """Run comprehensive slide validation"""
    print("🔍 COMPREHENSIVE SLIDE FIELD VALIDATION")
    print("=" * 60)
    
    # Load test data
    content_ir = load_test_content_ir()
    
    if not content_ir:
        print("❌ Cannot proceed without test data")
        return False
    
    # Check critical slides that were previously failing
    all_results = {}
    
    # Slide 1: Executive Summary  
    all_results['slide_1'] = check_slide_1_executive_summary(content_ir)
    
    # Slide 2: Business Overview
    all_results['slide_2'] = check_slide_2_business_overview(content_ir)
    
    # Slide 7: Strategic Buyers (critical!)
    all_results['slide_7'] = check_slide_7_strategic_buyers(content_ir)
    
    # Slide 8: Financial Buyers (critical!)
    all_results['slide_8'] = check_slide_8_financial_buyers(content_ir)
    
    # Slide 9: Management Team (critical!)
    all_results['slide_9'] = check_slide_9_management_team(content_ir)
    
    # Overall summary
    print("\n🏆 OVERALL VALIDATION SUMMARY")
    print("=" * 60)
    
    total_slides = len(all_results)
    total_passed = 0
    
    for slide_name, slide_results in all_results.items():
        slide_passed = all(slide_results.values())
        status = "✅ PASS" if slide_passed else "❌ FAIL"
        
        if slide_passed:
            total_passed += 1
            
        field_count = len(slide_results)
        passed_fields = sum(slide_results.values())
        
        print(f"{status} {slide_name.upper()}: {passed_fields}/{field_count} fields")
    
    print(f"\nFinal Result: {total_passed}/{total_slides} slides fully populated")
    
    if total_passed == total_slides:
        print("🎉 ALL CRITICAL SLIDES HAVE COMPLETE DATA!")
        return True
    else:
        print("⚠️  Some slides are missing data")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)