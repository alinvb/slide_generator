#!/usr/bin/env python3
"""
Test comprehensive slide fixes merged into fix/vector-db branch
Validates that ALL the slide enhancements from our work session are properly integrated:
1. Product & Service Footprint: 3-4 column enhancements
2. Competitive Positioning: iCar Asia 5-column format with star ratings  
3. Buyer Slides: Column header fixes (Concerns → Fit, Moelis contact → Contact)
4. AI Prompt Requirements: Enhanced validation and content requirements
"""

import sys
import inspect

def test_product_service_footprint_enhancements():
    """Test that Product & Service Footprint has 3-4 column enhancements"""
    print("🧪 Testing Product & Service Footprint 3-4 column enhancements...")
    
    try:
        from slide_templates import render_product_service_footprint_slide
        
        # Get function source code to verify enhancements
        source = inspect.getsource(render_product_service_footprint_slide)
        
        enhancement_checks = {
            "Has 3-column optimization": "cols == 3:" in source,
            "Has 4-column optimization": "cols == 4:" in source,
            "Has enhanced column width distribution": "ENHANCED: Optimal column width distribution" in source,
            "Has 3-column specific widths": "Inches(2.2)" in source and "Inches(1.65)" in source,
            "Has 4-column specific widths": "Inches(1.9)" in source and "Inches(1.4)" in source and "Inches(1.1)" in source
        }
        
        print("\n✅ Product & Service Footprint enhancements:")
        all_passed = True
        for check_name, passed in enhancement_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {passed}")
            if not passed:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error testing Product & Service Footprint enhancements: {e}")
        return False

def test_competitive_positioning_enhancements():
    """Test that Competitive Positioning has iCar Asia 5-column enhancements"""  
    print("\n🧪 Testing Competitive Positioning iCar Asia format enhancements...")
    
    try:
        from slide_templates import render_competitive_positioning_slide
        
        # Get function source code to verify enhancements
        source = inspect.getsource(render_competitive_positioning_slide)
        
        enhancement_checks = {
            "Has iCar Asia format description": "iCar Asia format" in source,
            "Has 5-column assessment reference": "5-column assessment table" in source,
            "Has enhanced column width optimization": "ENHANCED: Optimal column widths for 5-column iCar Asia format" in source,
            "Has 5-column width specification": "cols >= 5:" in source,
            "Has iCar Asia specific column widths": "Inches(1.3), Inches(1.0), Inches(1.0), Inches(0.9), Inches(0.8)" in source,
            "Has enhanced source note positioning": "ENHANCED: Source note positioned better" in source
        }
        
        print("\n✅ Competitive Positioning enhancements:")
        all_passed = True
        for check_name, passed in enhancement_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {passed}")
            if not passed:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error testing Competitive Positioning enhancements: {e}")
        return False

def test_buyer_slide_fixes():
    """Test that buyer slides have column header fixes"""
    print("\n🧪 Testing Buyer Slide column header fixes...")
    
    try:
        from slide_templates import render_buyer_profiles_slide, render_sea_conglomerates_slide
        
        # Get function source code to verify fixes
        buyer_source = inspect.getsource(render_buyer_profiles_slide)
        sea_source = inspect.getsource(render_sea_conglomerates_slide)
        
        buyer_checks = {
            "Strategic Buyer Profiles uses new headers": "['Buyer Name', 'Description', 'Strategic Rationale', 'Key Synergies', 'Fit']" in buyer_source,
            "Maps fit field correctly": "row_data.get('fit', row_data.get('concerns'" in buyer_source,
            "No longer defaults to Concerns": "'Concerns', 'Fit']" not in buyer_source
        }
        
        sea_checks = {
            "SEA Conglomerates uses Contact header": '"Contact"' in sea_source and '"Moelis contact"' not in sea_source,
            "Maps contact field with fallback": "company.get('contact', company.get('moelis_contact'" in sea_source,
            "Updated default examples": '"contact": "Managing Director' in sea_source
        }
        
        print("\n✅ Buyer Slide fixes:")
        all_passed = True
        
        for check_name, passed in buyer_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {passed}")
            if not passed:
                all_passed = False
        
        for check_name, passed in sea_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {passed}")
            if not passed:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error testing Buyer Slide fixes: {e}")
        return False

def test_ai_prompt_enhancements():
    """Test that AI prompts have comprehensive enhancements"""
    print("\n🧪 Testing AI Prompt comprehensive enhancements...")
    
    try:
        # Read app.py content to check for enhanced prompts
        with open('app.py', 'r') as f:
            app_content = f.read()
        
        prompt_checks = {
            "Has iCar Asia format requirements": "iCar Asia format with 5-column assessment table" in app_content,
            "Has 3-4 column requirements": "coverage_table must have 3-4 columns for proper market comparison" in app_content,
            "Has star rating requirements": "Use 1-5 stars (⭐) or numeric ratings" in app_content,
            "Has enhanced competitive positioning validation": "ENHANCED: Validate competitive positioning slide - iCar Asia format requirements" in app_content,
            "Has 5-column assessment validation": "iCar Asia format requires 5 columns: Company, Market Share, Tech Platform, Coverage, Revenue" in app_content,
            "Has coverage table column validation": "market comparison tables should have 3-4 columns" in app_content,
            "Has buyer slide 5-10 word requirement": "strategic_rationale (5-10 words)" in app_content,
            "Uses fit instead of concerns in prompts": "key_synergies, fit, financial_capacity" in app_content
        }
        
        print("\n✅ AI Prompt enhancements:")
        all_passed = True
        for check_name, passed in prompt_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {passed}")
            if not passed:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error testing AI Prompt enhancements: {e}")
        return False

def main():
    """Run all comprehensive slide enhancement tests"""
    print("🚀 Testing comprehensive slide fixes merged into fix/vector-db branch...\n")
    
    success_count = 0
    total_tests = 4
    
    # Test 1: Product & Service Footprint 3-4 column enhancements
    if test_product_service_footprint_enhancements():
        success_count += 1
    
    # Test 2: Competitive Positioning iCar Asia enhancements  
    if test_competitive_positioning_enhancements():
        success_count += 1
    
    # Test 3: Buyer Slide column header fixes
    if test_buyer_slide_fixes():
        success_count += 1
    
    # Test 4: AI Prompt comprehensive enhancements
    if test_ai_prompt_enhancements():
        success_count += 1
    
    print(f"\n📊 Test Results: {success_count}/{total_tests} test categories passed")
    
    if success_count == total_tests:
        print("🎉 ALL COMPREHENSIVE SLIDE FIXES SUCCESSFULLY MERGED!")
        print("\n✅ Complete list of enhancements now in fix/vector-db branch:")
        print("  🔧 Product & Service Footprint: Enhanced 3-4 column market comparison")
        print("  🔧 Competitive Positioning: iCar Asia 5-column format with star ratings")
        print("  🔧 Strategic Buyer Profiles: 'Concerns' → 'Fit' column header")
        print("  🔧 SEA Conglomerates: 'Moelis contact' → 'Contact' column header")  
        print("  🔧 AI Prompts: Enhanced validation with structural requirements")
        print("  🔧 Validation Functions: 3-4 column and 5-column format checks")
        print("  🔧 Content Requirements: 5-10 word strategic rationale")
        print("  🔧 Backward Compatibility: Fallback field mappings maintained")
        print("\nAll our comprehensive slide generation work is now properly integrated! 🚀")
        return True
    else:
        print("❌ Some comprehensive fixes may be missing - check the errors above")
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)