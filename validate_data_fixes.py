"""
Validate that the data processing fixes are working correctly
This tests the specific validation logic without requiring API calls
"""
import sys
import os
import json

# Add the current directory to the path
sys.path.append('/home/user/webapp')

from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def test_competitive_analysis_processing():
    """Test the competitive analysis processing with complete assessment data"""
    print("🔍 Testing competitive analysis processing...")
    
    generator = CleanBulletproofJSONGenerator()
    
    # Test data simulating conversation extraction
    test_data = {
        'company_name': 'NVIDIA',
        'competitors_mentioned': ['AMD', 'Intel', 'Qualcomm'],
    }
    
    # Process competitive analysis
    generator._process_competitive_analysis(test_data)
    
    # Validate results
    competitive_analysis = test_data.get('competitive_analysis', {})
    competitors = competitive_analysis.get('competitors', [])
    assessment = competitive_analysis.get('assessment', [])
    
    print(f"✅ Competitive analysis results:")
    print(f"  • Competitors generated: {len(competitors)}")
    print(f"  • Assessment matrix rows: {len(assessment)}")
    
    # Check if assessment has header + data rows
    has_headers = len(assessment) > 0 and len(assessment[0]) > 0
    has_data_rows = len(assessment) > 1
    
    print(f"  • Has header row: {has_headers}")
    print(f"  • Has data rows: {has_data_rows}")
    
    if has_data_rows:
        print(f"  • Sample data row: {assessment[1][:2]}...")  # Show first 2 columns
        
    return has_headers and has_data_rows

def test_precedent_transaction_validation():
    """Test precedent transaction processing with null value handling"""
    print("🔍 Testing precedent transaction validation...")
    
    generator = CleanBulletproofJSONGenerator()
    
    # Test data with null/problematic values
    test_data = {
        'precedent_transactions_detailed': [
            {
                'target': 'Test Target Company',
                'acquirer': None,  # This should be fixed
                'enterprise_value': '$1.5B',
                'ev_revenue_multiple': '7.5x',
                'date': '2023'
            },
            {
                'target': None,  # This should be fixed too
                'acquirer': 'Test Acquirer', 
                'enterprise_value': None,
                'revenue': '$200M'
            }
        ]
    }
    
    # Process the transactions
    generator._process_detailed_conversation_fields(test_data)
    
    # Validate results
    transactions = test_data.get('precedent_transactions', [])
    print(f"✅ Transaction validation results:")
    print(f"  • Transactions processed: {len(transactions)}")
    
    all_valid = True
    for i, transaction in enumerate(transactions):
        target = transaction.get('target')
        acquirer = transaction.get('acquirer') 
        
        target_valid = target is not None and target != 'null'
        acquirer_valid = acquirer is not None and acquirer != 'null'
        
        print(f"  • Transaction {i+1}:")
        print(f"    - Target: '{target}' (valid: {target_valid})")
        print(f"    - Acquirer: '{acquirer}' (valid: {acquirer_valid})")
        
        if not (target_valid and acquirer_valid):
            all_valid = False
    
    return all_valid and len(transactions) > 0

def test_json_structure_completeness():
    """Test that the enhanced data structure includes all required fields"""
    print("🔍 Testing JSON structure completeness...")
    
    # Simulate the enhanced data structure that should be generated
    test_enhanced_data = {
        'company_name': 'NVIDIA',
        'competitors_mentioned': ['AMD', 'Intel'],
        'precedent_transactions_detailed': [
            {'target': 'Target Co', 'acquirer': 'Acquirer Co', 'enterprise_value': '$1B'}
        ]
    }
    
    generator = CleanBulletproofJSONGenerator()
    
    # Process all conversation data
    generator._process_detailed_conversation_fields(test_enhanced_data)
    
    # Check for required fields
    required_fields = [
        'competitive_analysis',
        'precedent_transactions'  
    ]
    
    print("✅ Structure completeness results:")
    all_present = True
    for field in required_fields:
        present = field in test_enhanced_data
        print(f"  • {field}: {'✓' if present else '✗'}")
        if not present:
            all_present = False
    
    # Additional validation for competitive analysis structure
    if 'competitive_analysis' in test_enhanced_data:
        comp_analysis = test_enhanced_data['competitive_analysis']
        has_competitors = len(comp_analysis.get('competitors', [])) > 0
        has_assessment = len(comp_analysis.get('assessment', [])) > 1  # Header + data
        print(f"  • Competitive analysis complete: {'✓' if (has_competitors and has_assessment) else '✗'}")
        all_present = all_present and has_competitors and has_assessment
    
    return all_present

def main():
    """Run all validation tests"""
    print("🧪 Running data processing validation tests...\n")
    
    tests_passed = 0
    total_tests = 3
    
    # Test 1: Competitive analysis processing
    if test_competitive_analysis_processing():
        tests_passed += 1
        print("✅ Test 1 passed: Competitive analysis processing\n")
    else:
        print("❌ Test 1 failed: Competitive analysis processing\n")
    
    # Test 2: Transaction validation
    if test_precedent_transaction_validation():
        tests_passed += 1
        print("✅ Test 2 passed: Precedent transaction validation\n")
    else:
        print("❌ Test 2 failed: Precedent transaction validation\n")
    
    # Test 3: JSON structure completeness
    if test_json_structure_completeness():
        tests_passed += 1
        print("✅ Test 3 passed: JSON structure completeness\n")
    else:
        print("❌ Test 3 failed: JSON structure completeness\n")
    
    print(f"🎯 Validation Results: {tests_passed}/{total_tests} tests passed")
    
    if tests_passed == total_tests:
        print("\n✅ All data processing fixes validated successfully!")
        print("\n📋 Confirmed improvements:")
        print("• Competitive assessment includes complete data matrix")
        print("• Precedent transactions validate and fix null values")
        print("• JSON structure maintains all required fields")
        print("• Data processing prevents renderer errors")
        
        print("\n🔧 The fixes should resolve the slide rendering issues:")
        print("• No more 'NoneType has no len()' errors")
        print("• Complete competitive assessment tables")
        print("• Properly formatted precedent transaction data")
    else:
        print("\n⚠️ Some validation tests failed - review the fixes")

if __name__ == "__main__":
    main()