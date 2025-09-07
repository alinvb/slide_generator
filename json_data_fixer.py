#!/usr/bin/env python3
"""
Comprehensive JSON Data Fixer
Fixes data type mismatches and structure issues between user JSON and slide templates
"""

import json
from typing import Dict, Any, List, Union
import copy

def fix_business_overview_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix business overview slide data structure issues"""
    fixed_data = copy.deepcopy(data)
    
    # Fix timeline data types - convert integers to strings
    if 'timeline' in fixed_data and isinstance(fixed_data['timeline'], dict):
        timeline = fixed_data['timeline']
        
        if 'start_year' in timeline and isinstance(timeline['start_year'], int):
            timeline['start_year'] = str(timeline['start_year'])
            print(f"[FIX] Converted start_year from int to string: {timeline['start_year']}")
        
        if 'end_year' in timeline and isinstance(timeline['end_year'], int):
            timeline['end_year'] = str(timeline['end_year'])
            print(f"[FIX] Converted end_year from int to string: {timeline['end_year']}")
        
        # Add years_note if missing
        if 'years_note' not in timeline:
            start_year = int(timeline.get('start_year', '2020'))
            end_year = int(timeline.get('end_year', '2024'))
            years_count = end_year - start_year
            timeline['years_note'] = f"({years_count}+ years of operation)"
            print(f"[FIX] Added years_note: {timeline['years_note']}")
    
    return fixed_data

def fix_historical_financial_performance_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix historical financial performance slide data structure issues"""
    fixed_data = copy.deepcopy(data)
    
    # Fix key_metrics structure - should be {"metrics": [...]} with proper object structure
    if 'key_metrics' in fixed_data:
        if isinstance(fixed_data['key_metrics'], list):
            # Convert list of strings to proper metrics object structure
            metrics_objects = []
            for i, metric_str in enumerate(fixed_data['key_metrics']):
                if isinstance(metric_str, str):
                    # Convert string to proper metric object
                    metrics_objects.append({
                        'title': f'Key Metric {i+1}',
                        'value': metric_str,
                        'period': '(Historical)'
                    })
                else:
                    # Already proper structure
                    metrics_objects.append(metric_str)
            
            fixed_data['key_metrics'] = {"metrics": metrics_objects}
            print(f"[FIX] Converted key_metrics strings to object structure with {len(metrics_objects)} metrics")
        elif isinstance(fixed_data['key_metrics'], dict):
            # Check if metrics are properly structured
            metrics = fixed_data['key_metrics'].get('metrics', [])
            if metrics and isinstance(metrics[0], str):
                # Convert string metrics to objects
                metrics_objects = []
                for i, metric_str in enumerate(metrics):
                    metrics_objects.append({
                        'title': f'Key Metric {i+1}',
                        'value': metric_str,
                        'period': '(Historical)'
                    })
                fixed_data['key_metrics']['metrics'] = metrics_objects
                print(f"[FIX] Fixed nested key_metrics structure")
    
    return fixed_data

def fix_product_service_footprint_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix product service footprint slide data structure issues"""
    fixed_data = copy.deepcopy(data)
    
    # Fix coverage_table structure - convert dict array to 2D array
    if 'coverage_table' in fixed_data and isinstance(fixed_data['coverage_table'], list):
        if len(fixed_data['coverage_table']) > 0 and isinstance(fixed_data['coverage_table'][0], dict):
            # Convert object array to 2D array
            headers = list(fixed_data['coverage_table'][0].keys())
            table_data = [headers]
            for row in fixed_data['coverage_table']:
                table_data.append([str(row.get(key, '')) for key in headers])
            fixed_data['coverage_table'] = table_data
            print(f"[FIX] Converted coverage_table from dict array to 2D array")
    
    # Fix metrics structure - convert string values to proper object structure
    if 'metrics' in fixed_data and isinstance(fixed_data['metrics'], dict):
        fixed_metrics = {}
        for key, value in fixed_data['metrics'].items():
            if isinstance(value, str):
                # Convert string value to proper metric object structure
                fixed_metrics[key] = {
                    'label': key.replace('_', ' ').title(),
                    'value': value
                }
                print(f"[FIX] Converted metric '{key}' from string to object structure")
            else:
                # Already proper structure
                fixed_metrics[key] = value
        fixed_data['metrics'] = fixed_metrics
    
    return fixed_data

def fix_sea_conglomerates_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix sea conglomerates slide data structure issues"""
    fixed_data = copy.deepcopy(data)
    
    # Fix nested data structure
    if 'data' in fixed_data and 'data' not in fixed_data.get('data', {}):
        # Move nested data to top level
        if isinstance(fixed_data['data'], list):
            fixed_data['sea_conglomerates'] = fixed_data['data']
            del fixed_data['data']
            print(f"[FIX] Moved nested sea_conglomerates data to top level")
    
    return fixed_data

def fix_buyer_profiles_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix buyer profiles slide data structure issues"""
    fixed_data = copy.deepcopy(data)
    
    # Ensure proper table structure for buyer profiles
    if 'table_rows' in fixed_data and isinstance(fixed_data['table_rows'], list):
        for row in fixed_data['table_rows']:
            # Ensure all required fields exist
            required_fields = [
                'buyer_name', 'description', 'strategic_rationale', 
                'key_synergies', 'concerns', 'fit_score', 'financial_capacity'
            ]
            for field in required_fields:
                if field not in row:
                    row[field] = 'N/A'
                    print(f"[FIX] Added missing field '{field}' to buyer profile")
    
    return fixed_data

def fix_precedent_transactions_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix precedent transactions slide data structure issues"""
    fixed_data = copy.deepcopy(data)
    
    if 'transactions' in fixed_data and isinstance(fixed_data['transactions'], list):
        for transaction in fixed_data['transactions']:
            # Ensure enterprise_value and revenue exist and calculate multiple
            if 'enterprise_value' not in transaction or 'revenue' not in transaction:
                enterprise_value = transaction.get('enterprise_value', transaction.get('revenue', 100) * 3.0)
                revenue = transaction.get('revenue', transaction.get('enterprise_value', 300) / 3.0)
                
                transaction['enterprise_value'] = enterprise_value
                transaction['revenue'] = revenue
                print(f"[FIX] Added missing enterprise_value/revenue to transaction")
            
            # Calculate EV/Revenue multiple if missing
            if 'ev_revenue_multiple' not in transaction:
                if transaction['revenue'] != 0:
                    transaction['ev_revenue_multiple'] = round(transaction['enterprise_value'] / transaction['revenue'], 1)
                else:
                    transaction['ev_revenue_multiple'] = 0.0
                print(f"[FIX] Calculated EV/Revenue multiple: {transaction['ev_revenue_multiple']}")
    
    return fixed_data

def fix_margin_cost_resilience_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix margin cost resilience slide data structure issues"""
    fixed_data = copy.deepcopy(data)
    
    # Fix chart_data structure - handle alternative formats
    if 'chart' in fixed_data and 'chart_data' not in fixed_data:
        # Move chart to chart_data
        fixed_data['chart_data'] = fixed_data.pop('chart')
        print(f"[FIX] Moved chart to chart_data structure")
    
    # Ensure chart_data has proper structure
    if 'chart_data' in fixed_data:
        chart_data = fixed_data['chart_data']
        
        # Ensure categories and values exist
        if 'categories' not in chart_data or 'values' not in chart_data:
            if 'years' in chart_data and 'margins' in chart_data:
                # Alternative format conversion
                chart_data['categories'] = chart_data.pop('years')
                chart_data['values'] = chart_data.pop('margins')
                print(f"[FIX] Converted years/margins to categories/values")
            elif 'x_axis' in chart_data and 'y_axis' in chart_data:
                # Another alternative format
                chart_data['categories'] = chart_data.pop('x_axis')
                chart_data['values'] = chart_data.pop('y_axis')
                print(f"[FIX] Converted x_axis/y_axis to categories/values")
        
        # Validate data completeness
        categories = chart_data.get('categories', [])
        values = chart_data.get('values', [])
        if len(categories) != len(values):
            print(f"[FIX] WARNING: Chart data length mismatch - categories:{len(categories)}, values:{len(values)}")
    
    # Fix cost_management structure
    if 'cost_management' not in fixed_data:
        # Check for alternative formats
        if 'cost_initiatives' in fixed_data:
            fixed_data['cost_management'] = {'items': fixed_data.pop('cost_initiatives')}
            print(f"[FIX] Moved cost_initiatives to cost_management.items")
        elif 'efficiency_initiatives' in fixed_data:
            fixed_data['cost_management'] = {'items': fixed_data.pop('efficiency_initiatives')}
            print(f"[FIX] Moved efficiency_initiatives to cost_management.items")
    
    # Ensure cost_management.items is properly formatted
    if 'cost_management' in fixed_data:
        cost_mgmt = fixed_data['cost_management']
        if 'items' in cost_mgmt and isinstance(cost_mgmt['items'], list):
            # Ensure each item has title and description
            for i, item in enumerate(cost_mgmt['items']):
                if isinstance(item, str):
                    # Convert string to proper object
                    cost_mgmt['items'][i] = {
                        'title': f'Initiative {i+1}',
                        'description': item
                    }
                    print(f"[FIX] Converted cost management item {i+1} from string to object")
                elif isinstance(item, dict) and 'title' not in item:
                    # Add missing title
                    item['title'] = f'Cost Initiative {i+1}'
                    print(f"[FIX] Added missing title to cost management item {i+1}")
    
    # Fix risk_mitigation structure
    if 'risk_mitigation' not in fixed_data:
        # Check for alternative formats
        if 'risk_strategies' in fixed_data:
            fixed_data['risk_mitigation'] = fixed_data.pop('risk_strategies')
            print(f"[FIX] Moved risk_strategies to risk_mitigation")
        elif 'mitigation' in fixed_data:
            fixed_data['risk_mitigation'] = fixed_data.pop('mitigation')
            print(f"[FIX] Moved mitigation to risk_mitigation")
    
    # Ensure proper risk_mitigation structure
    if 'risk_mitigation' in fixed_data:
        risk_mitigation = fixed_data['risk_mitigation']
        
        # Ensure main_strategy is a dict with title and description
        if 'main_strategy' in risk_mitigation and isinstance(risk_mitigation['main_strategy'], str):
            risk_mitigation['main_strategy'] = {
                'title': 'Risk Mitigation Strategy',
                'description': risk_mitigation['main_strategy'],
                'benefits': ['Reduced risk exposure', 'Enhanced stability', 'Improved resilience']
            }
            print(f"[FIX] Converted main_strategy from string to object")
        
        # Ensure banker_view exists and is properly formatted
        if 'banker_view' not in risk_mitigation or not risk_mitigation['banker_view']:
            risk_mitigation['banker_view'] = {
                'title': "BANKER'S VIEW",
                'text': 'Strong cost discipline and risk management framework support sustainable profitability.'
            }
            print(f"[FIX] Added missing banker_view to risk_mitigation")
    
    return fixed_data

def fix_slide_data(template: str, data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix slide data based on template type"""
    
    print(f"[FIX] Fixing data for template: {template}")
    
    # Apply template-specific fixes
    if template == 'business_overview':
        return fix_business_overview_data(data)
    elif template == 'historical_financial_performance':
        return fix_historical_financial_performance_data(data)
    elif template == 'product_service_footprint':
        return fix_product_service_footprint_data(data)
    elif template == 'sea_conglomerates':
        return fix_sea_conglomerates_data(data)
    elif template == 'buyer_profiles':
        return fix_buyer_profiles_data(data)
    elif template == 'precedent_transactions':
        return fix_precedent_transactions_data(data)
    elif template == 'margin_cost_resilience':
        return fix_margin_cost_resilience_data(data)
    elif template == 'competitive_positioning':
        return fix_competitive_positioning_data(data)
    elif template == 'growth_strategy':
        return fix_growth_strategy_data(data)
    else:
        # For templates without specific fixes, return as-is
        return data

def fix_competitive_positioning_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix competitive positioning slide data structure issues"""
    fixed_data = copy.deepcopy(data)
    
    # The assessment data conversion is now handled in the slide template itself
    # No fixes needed here as the template can handle both object and 2D array formats
    print(f"[FIX] Competitive positioning data structure checked")
    
    return fixed_data

def fix_growth_strategy_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix growth strategy slide data structure issues"""
    fixed_data = copy.deepcopy(data)
    
    # Ensure growth_strategy structure exists
    if 'growth_strategy' not in fixed_data:
        # Check for alternative formats
        if 'strategies' in fixed_data:
            # Move strategies to proper nested structure
            fixed_data['growth_strategy'] = {
                'title': 'Multi-Pronged Growth Strategy',
                'strategies': fixed_data.pop('strategies')
            }
            print(f"[FIX] Moved strategies to growth_strategy.strategies structure")
        elif 'growth_strategies' in fixed_data:
            # Alternative naming
            fixed_data['growth_strategy'] = {
                'title': 'Multi-Pronged Growth Strategy', 
                'strategies': fixed_data.pop('growth_strategies')
            }
            print(f"[FIX] Moved growth_strategies to growth_strategy.strategies structure")
    
    # Ensure financial_projections structure exists  
    if 'financial_projections' not in fixed_data:
        # Check for chart data in alternative locations
        if 'chart' in fixed_data:
            fixed_data['financial_projections'] = fixed_data.pop('chart')
            print(f"[FIX] Moved chart data to financial_projections structure")
        elif 'projections' in fixed_data:
            fixed_data['financial_projections'] = fixed_data.pop('projections')
            print(f"[FIX] Moved projections to financial_projections structure")
    
    # Ensure key_assumptions structure exists
    if 'key_assumptions' not in fixed_data:
        if 'assumptions' in fixed_data:
            # Convert direct assumptions array to proper structure
            assumptions_list = fixed_data.pop('assumptions')
            fixed_data['key_assumptions'] = {
                'title': 'Key Planning Assumptions',
                'assumptions': assumptions_list
            }
            print(f"[FIX] Moved assumptions to key_assumptions.assumptions structure")
    
    # Validate chart data completeness
    projections = fixed_data.get('financial_projections', {})
    if projections:
        categories = projections.get('categories', [])
        revenue = projections.get('revenue', [])
        ebitda = projections.get('ebitda', [])
        
        # Ensure arrays have same length
        if len(categories) != len(revenue) or len(categories) != len(ebitda):
            print(f"[FIX] WARNING: Growth strategy chart data length mismatch - categories:{len(categories)}, revenue:{len(revenue)}, ebitda:{len(ebitda)}")
        
        # Add chart title if missing
        if 'chart_title' not in projections and 'title' not in projections:
            projections['chart_title'] = 'Revenue & EBITDA Projections'
            print(f"[FIX] Added missing chart_title to financial_projections")
    
    return fixed_data

def fix_render_plan(render_plan: Dict[str, Any]) -> Dict[str, Any]:
    """Fix entire render plan by fixing each slide's data"""
    
    print(f"[FIX] Fixing render plan with {len(render_plan.get('slides', []))} slides")
    
    fixed_plan = copy.deepcopy(render_plan)
    
    for i, slide in enumerate(fixed_plan.get('slides', [])):
        template = slide.get('template')
        data = slide.get('data', {})
        
        print(f"\n[FIX] Processing slide {i+1}: {template}")
        
        # Ensure title exists
        if 'title' not in data:
            data['title'] = template.replace('_', ' ').title()
            print(f"[FIX] Added missing title: {data['title']}")
        
        # Apply template-specific fixes
        fixed_data = fix_slide_data(template, data)
        slide['data'] = fixed_data
    
    return fixed_plan

def fix_content_ir(content_ir: Dict[str, Any]) -> Dict[str, Any]:
    """Fix content IR data structure issues"""
    
    print(f"[FIX] Fixing content IR with sections: {list(content_ir.keys())}")
    
    fixed_ir = copy.deepcopy(content_ir)
    
    # Add missing sections that are commonly required
    required_sections = [
        'entities', 'facts', 'charts', 'management_team', 'investor_considerations',
        'competitive_analysis', 'precedent_transactions', 'valuation_data', 'sea_conglomerates',
        'strategic_buyers', 'financial_buyers', 'product_service_data', 'business_overview_data',
        'growth_strategy_data', 'investor_process_data', 'margin_cost_data'
    ]
    
    for section in required_sections:
        if section not in fixed_ir:
            print(f"[FIX] Adding missing section: {section}")
            
            # Add appropriate default structure based on section
            if section == 'charts':
                fixed_ir[section] = [{
                    "id": "chart_hist_perf",
                    "type": "combo",
                    "title": "Revenue & EBITDA Growth",
                    "categories": fixed_ir.get('facts', {}).get('years', ['2020', '2021', '2022', '2023', '2024E']),
                    "revenue": fixed_ir.get('facts', {}).get('revenue_usd_m', [120, 145, 180, 210, 240]),
                    "ebitda": fixed_ir.get('facts', {}).get('ebitda_usd_m', [18, 24, 31, 40, 47]),
                    "unit": "US$m"
                }]
            elif section == 'investor_process_data':
                fixed_ir[section] = {
                    "diligence_topics": [
                        {"title": "Financial Review", "description": "Financial analysis and projections"},
                        {"title": "Market Analysis", "description": "Market size and competitive landscape"}
                    ],
                    "synergy_opportunities": [
                        {"title": "Revenue Synergies", "description": "Cross-selling opportunities"}
                    ],
                    "risk_factors": ["Market volatility", "Competitive pressure"],
                    "mitigants": ["Diversified portfolio", "Strong market position"],
                    "timeline": [
                        {"date": "Week 1-2", "description": "Initial due diligence"},
                        {"date": "Week 3-4", "description": "Management presentations"}
                    ]
                }
            else:
                # Default empty structure
                fixed_ir[section] = {}
    
    return fixed_ir

def comprehensive_json_fix(slides_json: Dict[str, Any], content_ir_json: Dict[str, Any]) -> tuple[Dict[str, Any], Dict[str, Any]]:
    """Apply comprehensive fixes to both slides and content IR"""
    
    print("=" * 60)
    print("COMPREHENSIVE JSON FIXING")
    print("=" * 60)
    
    # Fix content IR first
    fixed_content_ir = fix_content_ir(content_ir_json)
    
    # Fix render plan
    fixed_render_plan = fix_render_plan(slides_json)
    
    print("\n" + "=" * 60)
    print("FIXING COMPLETE")
    print("=" * 60)
    
    return fixed_render_plan, fixed_content_ir

if __name__ == "__main__":
    # Test with sample data
    print("Testing JSON data fixer...")
    
    sample_slides = {
        "slides": [{
            "template": "business_overview",
            "data": {
                "title": "Business Overview",
                "timeline": {"start_year": 1933, "end_year": 2025}
            }
        }]
    }
    
    sample_content_ir = {
        "entities": {"company": {"name": "Test Company"}},
        "facts": {"years": ["2020", "2021"], "revenue_usd_m": [100, 120]}
    }
    
    fixed_slides, fixed_content = comprehensive_json_fix(sample_slides, sample_content_ir)
    
    print("\nFixed slides:", json.dumps(fixed_slides, indent=2))
    print("\nFixed content IR keys:", list(fixed_content.keys()))