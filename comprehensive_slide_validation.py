#!/usr/bin/env python3
"""
Comprehensive slide data validation - checks ALL fields for ALL slides
"""

import json
import sys
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator
from slide_templates import *

def validate_all_slide_fields():
    """Validate all data fields for all 14 slides are populated"""
    
    # Initialize generator with API key from .env
    generator = CleanBulletproofJSONGenerator()
    
    # Test company for validation
    company_name = "Netflix"
    
    print("🔍 COMPREHENSIVE SLIDE VALIDATION REPORT")
    print("=" * 60)
    print(f"Company: {company_name}")
    print("Checking ALL fields for ALL 14 slides...")
    print()
    
    try:
        # Generate content_ir with real API data
        print("📡 Generating content_ir with Perplexity API...")
        content_ir = generator.generate_content_ir(company_name)
        
        if not content_ir:
            print("❌ CRITICAL: content_ir generation failed!")
            return False
            
        print(f"✅ content_ir generated successfully")
        print()
        
        # Validate each slide systematically
        validation_results = {}
        
        # SLIDE 1: Executive Summary
        print("📊 SLIDE 1: EXECUTIVE SUMMARY")
        print("-" * 40)
        slide1_data = generator.extract_slide_data('executive_summary', content_ir)
        slide1_results = validate_executive_summary(slide1_data)
        validation_results['executive_summary'] = slide1_results
        print()
        
        # SLIDE 2: Business Overview  
        print("📊 SLIDE 2: BUSINESS OVERVIEW")
        print("-" * 40)
        slide2_data = generator.extract_slide_data('business_overview', content_ir)
        slide2_results = validate_business_overview(slide2_data)
        validation_results['business_overview'] = slide2_results
        print()
        
        # SLIDE 3: Market Analysis
        print("📊 SLIDE 3: MARKET ANALYSIS")
        print("-" * 40)
        slide3_data = generator.extract_slide_data('market_analysis', content_ir)
        slide3_results = validate_market_analysis(slide3_data)
        validation_results['market_analysis'] = slide3_results
        print()
        
        # SLIDE 4: Competitive Landscape
        print("📊 SLIDE 4: COMPETITIVE LANDSCAPE")
        print("-" * 40)
        slide4_data = generator.extract_slide_data('competitive_positioning', content_ir)
        slide4_results = validate_competitive_landscape(slide4_data)
        validation_results['competitive_positioning'] = slide4_results
        print()
        
        # SLIDE 5: Financial Performance
        print("📊 SLIDE 5: FINANCIAL PERFORMANCE")
        print("-" * 40)
        slide5_data = generator.extract_slide_data('historical_financial_performance', content_ir)
        slide5_results = validate_financial_performance(slide5_data)
        validation_results['historical_financial_performance'] = slide5_results
        print()
        
        # SLIDE 6: Growth Strategy & Projections
        print("📊 SLIDE 6: GROWTH STRATEGY & PROJECTIONS")
        print("-" * 40)
        slide6_data = generator.extract_slide_data('growth_investor', content_ir)
        slide6_results = validate_growth_strategy(slide6_data)
        validation_results['growth_investor'] = slide6_results
        print()
        
        # SLIDE 7: Strategic Buyers
        print("📊 SLIDE 7: STRATEGIC BUYERS")
        print("-" * 40)
        slide7_data = generator.extract_slide_data('buyer_profiles', content_ir)
        slide7_results = validate_strategic_buyers(slide7_data, 'strategic')
        validation_results['strategic_buyers'] = slide7_results
        print()
        
        # SLIDE 8: Financial Buyers  
        print("📊 SLIDE 8: FINANCIAL BUYERS")
        print("-" * 40)
        slide8_data = generator.extract_slide_data('buyer_profiles', content_ir)
        slide8_results = validate_financial_buyers(slide8_data, 'financial')
        validation_results['financial_buyers'] = slide8_results
        print()
        
        # SLIDE 9: Management Team
        print("📊 SLIDE 9: MANAGEMENT TEAM")
        print("-" * 40)
        slide9_data = generator.extract_slide_data('management_team', content_ir)
        slide9_results = validate_management_team(slide9_data)
        validation_results['management_team'] = slide9_results
        print()
        
        # SLIDE 10: Precedent Transactions
        print("📊 SLIDE 10: PRECEDENT TRANSACTIONS")
        print("-" * 40)
        slide10_data = generator.extract_slide_data('precedent_transactions', content_ir)
        slide10_results = validate_precedent_transactions(slide10_data)
        validation_results['precedent_transactions'] = slide10_results
        print()
        
        # SLIDE 11: Valuation Overview
        print("📊 SLIDE 11: VALUATION OVERVIEW")
        print("-" * 40)
        slide11_data = generator.extract_slide_data('valuation_overview', content_ir)
        slide11_results = validate_valuation_overview(slide11_data)
        validation_results['valuation_overview'] = slide11_results
        print()
        
        # SLIDE 12: Product & Service Footprint
        print("📊 SLIDE 12: PRODUCT & SERVICE FOOTPRINT")
        print("-" * 40)
        slide12_data = generator.extract_slide_data('product_service_footprint', content_ir)
        slide12_results = validate_product_footprint(slide12_data)
        validation_results['product_service_footprint'] = slide12_results
        print()
        
        # SLIDE 13: Deal Structure & Timeline (Investor Process)
        print("📊 SLIDE 13: DEAL STRUCTURE & TIMELINE")
        print("-" * 40)
        slide13_data = generator.extract_slide_data('investor_process_overview', content_ir)
        slide13_results = validate_deal_structure(slide13_data)
        validation_results['investor_process_overview'] = slide13_results
        print()
        
        # SLIDE 14: Investment Considerations
        print("📊 SLIDE 14: INVESTMENT CONSIDERATIONS")
        print("-" * 40)
        slide14_data = generator.extract_slide_data('investor_considerations', content_ir)
        slide14_results = validate_investment_considerations(slide14_data)
        validation_results['investor_considerations'] = slide14_results
        print()
        
        # Summary Report
        print("🏆 VALIDATION SUMMARY")
        print("=" * 60)
        
        total_slides = len(validation_results)
        passed_slides = sum(1 for result in validation_results.values() if result['overall_pass'])
        
        for slide_name, result in validation_results.items():
            status = "✅ PASS" if result['overall_pass'] else "❌ FAIL" 
            print(f"{slide_name}: {status} ({result['passed_fields']}/{result['total_fields']} fields)")
            
        print()
        print(f"Overall: {passed_slides}/{total_slides} slides fully populated")
        
        if passed_slides == total_slides:
            print("🎉 ALL SLIDES FULLY POPULATED!")
            return True
        else:
            print("⚠️  Some slides have missing data")
            return False
            
    except Exception as e:
        print(f"❌ Validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_field(data, field_path, field_name):
    """Check if a field exists and has valid data"""
    try:
        # Navigate nested field path
        current = data
        for key in field_path:
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                print(f"  ❌ {field_name}: Missing field '{key}' in path")
                return False
                
        # Check if field has valid data
        if current is None:
            print(f"  ❌ {field_name}: Field is None")
            return False
        elif isinstance(current, (list, dict)) and len(current) == 0:
            print(f"  ❌ {field_name}: Field is empty")
            return False
        elif isinstance(current, str) and (not current.strip() or current.strip() in ['[]', '{}', 'null', 'undefined']):
            print(f"  ❌ {field_name}: Field is empty string or placeholder")
            return False
        else:
            print(f"  ✅ {field_name}: Valid data")
            return True
            
    except Exception as e:
        print(f"  ❌ {field_name}: Error checking field - {str(e)}")
        return False

def validate_executive_summary(data):
    """Validate Executive Summary slide fields"""
    fields_to_check = [
        (['company_overview'], 'Company Overview'),
        (['investment_highlights'], 'Investment Highlights'), 
        (['key_metrics'], 'Key Metrics'),
        (['financial_snapshot'], 'Financial Snapshot')
    ]
    
    passed = 0
    total = len(fields_to_check)
    
    for field_path, field_name in fields_to_check:
        if check_field(data, field_path, field_name):
            passed += 1
            
    return {'overall_pass': passed == total, 'passed_fields': passed, 'total_fields': total}

def validate_business_overview(data):
    """Validate Business Overview slide fields"""
    fields_to_check = [
        (['company_description'], 'Company Description'),
        (['services'], 'Services'),
        (['highlights'], 'Key Highlights'),
        (['market_position'], 'Market Position')
    ]
    
    passed = 0
    total = len(fields_to_check)
    
    for field_path, field_name in fields_to_check:
        if check_field(data, field_path, field_name):
            passed += 1
            
    return {'overall_pass': passed == total, 'passed_fields': passed, 'total_fields': total}

def validate_market_analysis(data):
    """Validate Market Analysis slide fields"""
    fields_to_check = [
        (['market_size'], 'Market Size'),
        (['growth_trends'], 'Growth Trends'),
        (['key_drivers'], 'Key Drivers'),
        (['market_dynamics'], 'Market Dynamics')
    ]
    
    passed = 0
    total = len(fields_to_check)
    
    for field_path, field_name in fields_to_check:
        if check_field(data, field_path, field_name):
            passed += 1
            
    return {'overall_pass': passed == total, 'passed_fields': passed, 'total_fields': total}

def validate_competitive_landscape(data):
    """Validate Competitive Landscape slide fields"""
    fields_to_check = [
        (['competitive_analysis', 'competitors'], 'Competitor List'),
        (['competitive_analysis', 'assessment'], 'Competitive Assessment'),
        (['positioning'], 'Market Positioning')
    ]
    
    passed = 0
    total = len(fields_to_check)
    
    for field_path, field_name in fields_to_check:
        if check_field(data, field_path, field_name):
            passed += 1
            
    return {'overall_pass': passed == total, 'passed_fields': passed, 'total_fields': total}

def validate_financial_performance(data):
    """Validate Financial Performance slide fields"""
    fields_to_check = [
        (['years'], 'Years'),
        (['revenue_usd_m'], 'Revenue'),
        (['ebitda_usd_m'], 'EBITDA'),
        (['ebitda_margins'], 'EBITDA Margins'),
        (['growth_rates'], 'Growth Rates')
    ]
    
    passed = 0
    total = len(fields_to_check)
    
    for field_path, field_name in fields_to_check:
        if check_field(data, field_path, field_name):
            passed += 1
            
    return {'overall_pass': passed == total, 'passed_fields': passed, 'total_fields': total}

def validate_growth_strategy(data):
    """Validate Growth Strategy & Projections slide fields"""
    fields_to_check = [
        (['growth_strategy_data', 'growth_strategy', 'strategies'], 'Growth Strategies'),
        (['growth_strategy_data', 'financial_projections', 'categories'], 'Projection Categories'),
        (['growth_strategy_data', 'financial_projections', 'revenue'], 'Revenue Projections'),
        (['growth_strategy_data', 'financial_projections', 'ebitda'], 'EBITDA Projections')
    ]
    
    passed = 0
    total = len(fields_to_check)
    
    for field_path, field_name in fields_to_check:
        if check_field(data, field_path, field_name):
            passed += 1
            
    return {'overall_pass': passed == total, 'passed_fields': passed, 'total_fields': total}

def validate_strategic_buyers(data, buyer_type):
    """Validate Strategic Buyers slide fields"""
    fields_to_check = [
        (['strategic_buyers'], 'Strategic Buyers List')
    ]
    
    passed = 0
    total = len(fields_to_check)
    
    for field_path, field_name in fields_to_check:
        if check_field(data, field_path, field_name):
            # Check individual buyer fields
            buyers = data.get('strategic_buyers', [])
            if buyers and len(buyers) > 0:
                buyer = buyers[0]  # Check first buyer structure
                buyer_fields = ['buyer_name', 'description', 'strategic_rationale', 'key_synergies', 'fit', 'financial_capacity']
                all_buyer_fields_present = all(field in buyer for field in buyer_fields)
                if all_buyer_fields_present:
                    print(f"    ✅ Strategic buyer fields complete")
                    passed += 1
                else:
                    print(f"    ❌ Strategic buyer missing fields")
            else:
                print(f"    ❌ No strategic buyers found")
        else:
            print(f"    ❌ Strategic buyers array missing")
            
    return {'overall_pass': passed == total, 'passed_fields': passed, 'total_fields': total}

def validate_financial_buyers(data, buyer_type):
    """Validate Financial Buyers slide fields"""
    fields_to_check = [
        (['financial_buyers'], 'Financial Buyers List')
    ]
    
    passed = 0
    total = len(fields_to_check)
    
    for field_path, field_name in fields_to_check:
        if check_field(data, field_path, field_name):
            # Check individual buyer fields
            buyers = data.get('financial_buyers', [])
            if buyers and len(buyers) > 0:
                buyer = buyers[0]  # Check first buyer structure
                buyer_fields = ['buyer_name', 'description', 'strategic_rationale', 'key_synergies', 'fit', 'financial_capacity']
                all_buyer_fields_present = all(field in buyer for field in buyer_fields)
                if all_buyer_fields_present:
                    print(f"    ✅ Financial buyer fields complete")
                    passed += 1
                else:
                    print(f"    ❌ Financial buyer missing fields")
            else:
                print(f"    ❌ No financial buyers found")
        else:
            print(f"    ❌ Financial buyers array missing")
            
    return {'overall_pass': passed == total, 'passed_fields': passed, 'total_fields': total}

def validate_management_team(data):
    """Validate Management Team slide fields"""
    fields_to_check = [
        (['left_column_profiles'], 'Left Column Profiles'),
        (['right_column_profiles'], 'Right Column Profiles')
    ]
    
    passed = 0
    total = len(fields_to_check)
    
    for field_path, field_name in fields_to_check:
        if check_field(data, field_path, field_name):
            passed += 1
            
    return {'overall_pass': passed == total, 'passed_fields': passed, 'total_fields': total}

def validate_precedent_transactions(data):
    """Validate Precedent Transactions slide fields"""
    fields_to_check = [
        (['precedent_transactions'], 'Precedent Transactions List')
    ]
    
    passed = 0
    total = len(fields_to_check)
    
    for field_path, field_name in fields_to_check:
        if check_field(data, field_path, field_name):
            # Check transaction structure
            transactions = data.get('precedent_transactions', [])
            if transactions and len(transactions) > 0:
                txn = transactions[0]  # Check first transaction structure
                txn_fields = ['target_company', 'acquirer', 'year', 'transaction_value', 'revenue_multiple', 'ebitda_multiple']
                all_txn_fields_present = all(field in txn for field in txn_fields)
                if all_txn_fields_present:
                    print(f"    ✅ Transaction fields complete")
                    passed += 1
                else:
                    print(f"    ❌ Transaction missing fields")
            else:
                print(f"    ❌ No transactions found")
        else:
            print(f"    ❌ Transactions array missing")
            
    return {'overall_pass': passed == total, 'passed_fields': passed, 'total_fields': total}

def validate_valuation_overview(data):
    """Validate Valuation Overview slide fields"""
    fields_to_check = [
        (['valuation_overview'], 'Valuation Overview Array')
    ]
    
    passed = 0
    total = len(fields_to_check)
    
    for field_path, field_name in fields_to_check:
        if check_field(data, field_path, field_name):
            # Check valuation method structure
            methods = data.get('valuation_overview', [])
            if methods and len(methods) > 0:
                method = methods[0]  # Check first method structure
                method_fields = ['methodology', 'commentary', 'enterprise_value', 'metric', '22a_multiple', '23e_multiple']
                all_method_fields_present = all(field in method for field in method_fields)
                if all_method_fields_present:
                    print(f"    ✅ Valuation method fields complete")
                    passed += 1
                else:
                    print(f"    ❌ Valuation method missing fields")
            else:
                print(f"    ❌ No valuation methods found")
        else:
            print(f"    ❌ Valuation methods array missing")
            
    return {'overall_pass': passed == total, 'passed_fields': passed, 'total_fields': total}

def validate_product_footprint(data):
    """Validate Product & Service Footprint slide fields"""
    fields_to_check = [
        (['products'], 'Products'),
        (['services'], 'Services'),
        (['geographic_footprint'], 'Geographic Footprint'),
        (['market_segments'], 'Market Segments')
    ]
    
    passed = 0
    total = len(fields_to_check)
    
    for field_path, field_name in fields_to_check:
        if check_field(data, field_path, field_name):
            passed += 1
            
    return {'overall_pass': passed == total, 'passed_fields': passed, 'total_fields': total}

def validate_deal_structure(data):
    """Validate Deal Structure & Timeline slide fields"""
    fields_to_check = [
        (['process_overview'], 'Process Overview'),
        (['timeline'], 'Timeline'),
        (['key_considerations'], 'Key Considerations')
    ]
    
    passed = 0
    total = len(fields_to_check)
    
    for field_path, field_name in fields_to_check:
        if check_field(data, field_path, field_name):
            passed += 1
            
    return {'overall_pass': passed == total, 'passed_fields': passed, 'total_fields': total}

def validate_investment_considerations(data):
    """Validate Investment Considerations slide fields"""
    fields_to_check = [
        (['investment_strengths'], 'Investment Strengths'),
        (['key_risks'], 'Key Risks'),
        (['mitigating_factors'], 'Mitigating Factors')
    ]
    
    passed = 0
    total = len(fields_to_check)
    
    for field_path, field_name in fields_to_check:
        if check_field(data, field_path, field_name):
            passed += 1
            
    return {'overall_pass': passed == total, 'passed_fields': passed, 'total_fields': total}

if __name__ == "__main__":
    success = validate_all_slide_fields()
    sys.exit(0 if success else 1)