#!/usr/bin/env python3
"""
Test buyer slide fixes in fix/vector_db branch
Validates that the column header changes are properly implemented:
1. Strategic Buyer Profiles: "Concerns" → "Fit" 
2. SEA Conglomerate Strategic Buyers: "Moelis contact" → "Contact"
"""

import sys
import inspect

def test_buyer_slide_column_headers():
    """Test that buyer slide column headers are correctly fixed"""
    print("🧪 Testing buyer slide column header fixes...")
    
    try:
        from slide_templates import render_buyer_profiles_slide, render_sea_conglomerates_slide
        
        # Get function source code to verify fixes
        buyer_source = inspect.getsource(render_buyer_profiles_slide)
        sea_source = inspect.getsource(render_sea_conglomerates_slide)
        
        # Check buyer profiles fixes
        buyer_checks = {
            "Uses updated table headers": "['Buyer Name', 'Description', 'Strategic Rationale', 'Key Synergies', 'Fit']" in buyer_source,
            "Maps fit field correctly": "row_data.get('fit', row_data.get('concerns'" in buyer_source,
            "Includes description field": "row_data.get('description'" in buyer_source,
            "No longer defaults to Concerns": "'Concerns', 'Fit']" not in buyer_source
        }
        
        # Check SEA conglomerates fixes  
        sea_checks = {
            "Uses Contact header (not Moelis contact)": '"Contact"' in sea_source and '"Moelis contact"' not in sea_source,
            "Maps contact field correctly": "company.get('contact', company.get('moelis_contact'" in sea_source,
            "Updated default examples": '"contact": "Managing Director' in sea_source,
            "Maintains backward compatibility": "moelis_contact" in sea_source  # Should still have fallback
        }
        
        print("\n✅ Strategic Buyer Profiles fixes:")
        buyer_success = True
        for check_name, passed in buyer_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {passed}")
            if not passed:
                buyer_success = False
        
        print("\n✅ SEA Conglomerate fixes:")
        sea_success = True  
        for check_name, passed in sea_checks.items():
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}: {passed}")
            if not passed:
                sea_success = False
        
        return buyer_success and sea_success
        
    except Exception as e:
        print(f"❌ Error testing buyer slide fixes: {e}")
        return False

def test_ai_prompts_updated():
    """Test that AI prompts have been updated"""
    print("\n🧪 Testing AI prompt updates...")
    
    try:
        # Read app.py content to check for updated prompts
        with open('app.py', 'r') as f:
            app_content = f.read()
        
        prompt_checks = {
            "Updated buyer_profiles requirements": "strategic_rationale (5-10 words)" in app_content,
            "Uses Fit instead of concerns": "key_synergies, fit, financial_capacity" in app_content,
            "Updated sea_conglomerates contact field": "key_financials, contact)" in app_content,
            "Updated step instructions": "Moelis team contact for each" in app_content,
            "No references to old Concerns field in prompts": ", concerns," not in app_content.replace("get('concerns'", "").replace("row_data.get('concerns'", "")
        }
        
        print("\n✅ AI Prompt updates:")
        all_passed = True
        for check_name, passed in prompt_checks.items():
            status = "✅" if passed else "❌"  
            print(f"   {status} {check_name}: {passed}")
            if not passed:
                all_passed = False
        
        return all_passed
        
    except Exception as e:
        print(f"❌ Error testing AI prompt updates: {e}")
        return False

def main():
    """Run all tests for buyer slide fixes"""
    print("🚀 Testing buyer slide fixes in fix/vector_db branch...\n")
    
    success_count = 0
    total_tests = 2
    
    # Test 1: Column header fixes
    if test_buyer_slide_column_headers():
        success_count += 1
    
    # Test 2: AI prompt updates
    if test_ai_prompts_updated():
        success_count += 1
    
    print(f"\n📊 Test Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 All buyer slide fixes implemented successfully!")
        print("\n✅ Summary of fixes:")
        print("  • Strategic Buyer Profiles: 'Concerns' → 'Fit' column")
        print("  • SEA Conglomerates: 'Moelis contact' → 'Contact' column") 
        print("  • Added 5-10 word strategic rationale requirement")
        print("  • Updated AI prompts and validation functions")
        print("  • Maintained backward compatibility with fallback mappings")
        print("\nReady for commit and pull request! 🚀")
        return True
    else:
        print("❌ Some fixes still need work - check the errors above")
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)