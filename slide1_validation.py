#!/usr/bin/env python3
"""
Check Slide 1: Executive Summary/Overview - verify ALL fields populated
"""

import json
import sys
from bulletproof_json_generator_clean import CleanBulletproofJSONGenerator

def validate_slide1_executive_summary():
    """Validate Slide 1: Executive Summary - check ALL fields"""
    
    print("🔍 SLIDE 1 VALIDATION: EXECUTIVE SUMMARY")
    print("=" * 50)
    
    # Initialize generator 
    generator = CleanBulletproofJSONGenerator()
    
    # Test company
    company_name = "Netflix"
    print(f"Company: {company_name}")
    print()
    
    try:
        # First extract basic conversation data
        print("📡 Step 1: Extracting conversation data...")
        extracted_data = generator.extract_conversation_data(company_name)
        
        if not extracted_data:
            print("❌ FAIL: Could not extract conversation data")
            return False
            
        print(f"✅ Extracted conversation data successfully")
        print()
        
        # Required slides for executive summary
        required_slides = [
            'executive_summary',
            'business_overview', 
            'market_analysis',
            'competitive_positioning',
            'historical_financial_performance',
            'growth_investor',
            'buyer_profiles',
            'management_team',
            'precedent_transactions',
            'valuation_overview',
            'product_service_footprint',
            'investor_process_overview',
            'investor_considerations'
        ]
        
        # Build content_ir
        print("📡 Step 2: Building content_ir structure...")
        content_ir = generator.build_content_ir(extracted_data, required_slides)
        
        if not content_ir:
            print("❌ FAIL: Could not build content_ir")
            return False
            
        print(f"✅ Built content_ir successfully")
        print()
        
        # Extract slide 1 data 
        print("📊 Step 3: Extracting Slide 1 (Executive Summary) data...")
        
        # Check what's in content_ir
        print("Available content_ir keys:", list(content_ir.keys()) if content_ir else "None")
        
        # Look for executive summary data
        exec_summary_data = None
        
        # Try different possible keys
        possible_keys = ['executive_summary', 'entities', 'facts', 'summary']
        for key in possible_keys:
            if key in content_ir:
                print(f"Found data under key: {key}")
                if key == 'executive_summary':
                    exec_summary_data = content_ir[key]
                    break
                    
        # If no direct executive summary, build from available data
        if not exec_summary_data and 'entities' in content_ir:
            print("Building executive summary from entities and facts...")
            exec_summary_data = {
                'company_overview': content_ir.get('entities', {}).get('company', {}).get('name', company_name),
                'investment_highlights': content_ir.get('facts', {}).get('investment_highlights', []),
                'key_metrics': content_ir.get('facts', {}),
                'financial_snapshot': {
                    'revenue': content_ir.get('facts', {}).get('revenue_usd_m', []),
                    'ebitda': content_ir.get('facts', {}).get('ebitda_usd_m', []),
                    'years': content_ir.get('facts', {}).get('years', [])
                }
            }
        
        if not exec_summary_data:
            print("❌ FAIL: No executive summary data found")
            return False
            
        print(f"✅ Found executive summary data")
        print()
        
        # Validate all required fields for Executive Summary slide
        print("📋 FIELD-BY-FIELD VALIDATION:")
        print("-" * 30)
        
        validation_results = {}
        
        # Field 1: Company Overview
        print("1. Company Overview:")
        company_overview = exec_summary_data.get('company_overview')
        if company_overview and str(company_overview).strip():
            print("   ✅ PASS - Company overview present")
            validation_results['company_overview'] = True
        else:
            print("   ❌ FAIL - Company overview missing or empty")
            validation_results['company_overview'] = False
            
        # Field 2: Investment Highlights  
        print("2. Investment Highlights:")
        investment_highlights = exec_summary_data.get('investment_highlights', [])
        if isinstance(investment_highlights, list) and len(investment_highlights) > 0:
            print(f"   ✅ PASS - {len(investment_highlights)} investment highlights found")
            validation_results['investment_highlights'] = True
        else:
            print("   ❌ FAIL - Investment highlights missing or empty")
            validation_results['investment_highlights'] = False
            
        # Field 3: Key Metrics
        print("3. Key Metrics:")
        key_metrics = exec_summary_data.get('key_metrics', {})
        if isinstance(key_metrics, dict) and len(key_metrics) > 0:
            print(f"   ✅ PASS - Key metrics present: {list(key_metrics.keys())}")
            validation_results['key_metrics'] = True
        else:
            print("   ❌ FAIL - Key metrics missing or empty")
            validation_results['key_metrics'] = False
            
        # Field 4: Financial Snapshot
        print("4. Financial Snapshot:")
        financial_snapshot = exec_summary_data.get('financial_snapshot', {})
        if isinstance(financial_snapshot, dict):
            revenue = financial_snapshot.get('revenue', [])
            ebitda = financial_snapshot.get('ebitda', [])
            years = financial_snapshot.get('years', [])
            
            if revenue and ebitda and years:
                print(f"   ✅ PASS - Financial data: {len(years)} years, revenue & EBITDA present")
                validation_results['financial_snapshot'] = True
            else:
                print("   ❌ FAIL - Financial snapshot incomplete")
                validation_results['financial_snapshot'] = False
        else:
            print("   ❌ FAIL - Financial snapshot missing")
            validation_results['financial_snapshot'] = False
        
        print()
        print("📊 SLIDE 1 SUMMARY:")
        print("-" * 20)
        
        passed_fields = sum(validation_results.values())
        total_fields = len(validation_results)
        
        for field, passed in validation_results.items():
            status = "✅" if passed else "❌"
            print(f"{status} {field}")
            
        print()
        success = passed_fields == total_fields
        
        if success:
            print(f"🎉 SLIDE 1 COMPLETE: {passed_fields}/{total_fields} fields populated")
        else:
            print(f"⚠️  SLIDE 1 INCOMPLETE: {passed_fields}/{total_fields} fields populated")
            
        # Show actual data structure for debugging
        print()
        print("🔍 ACTUAL DATA STRUCTURE:")
        print(json.dumps(exec_summary_data, indent=2)[:500] + "..." if len(str(exec_summary_data)) > 500 else json.dumps(exec_summary_data, indent=2))
        
        return success
        
    except Exception as e:
        print(f"❌ Validation failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = validate_slide1_executive_summary()
    sys.exit(0 if success else 1)