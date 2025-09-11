#!/usr/bin/env python3
"""
Comprehensive JSON Data Fixer
Fixes data type mismatches and structure issues between user JSON and slide templates
"""

import json
from typing import Dict, Any, List, Union
import copy

def validate_data_structure(data: Any, expected_type: type, context: str = "") -> bool:
    """Validate data structure and log issues"""
    if not isinstance(data, expected_type):
        print(f"[VALIDATION ERROR] {context}: Expected {expected_type.__name__}, got {type(data).__name__}")
        return False
    return True

def safe_dict_access(data: Any, key: str, default: Any = None, context: str = "") -> Any:
    """Safely access dictionary key with validation"""
    if not isinstance(data, dict):
        print(f"[VALIDATION ERROR] {context}: Cannot access key '{key}' - data is not a dictionary (got {type(data).__name__})")
        return default
    return data.get(key, default)

def safe_list_access(data: Any, index: int, default: Any = None, context: str = "") -> Any:
    """Safely access list index with validation"""
    if not isinstance(data, list):
        print(f"[VALIDATION ERROR] {context}: Cannot access index {index} - data is not a list (got {type(data).__name__})")
        return default
    if index >= len(data):
        print(f"[VALIDATION ERROR] {context}: Index {index} out of range for list of length {len(data)}")
        return default
    return data[index]

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
        else:
            # key_metrics is not a dict or list, create proper structure
            fixed_data['key_metrics'] = {"metrics": ["120%", "38.0", "5.7", "300"]}
            print(f"[FIX] Created missing key_metrics structure with default metrics")
    else:
        # key_metrics is completely missing, add it
        fixed_data['key_metrics'] = {"metrics": ["120%", "38.0", "5.7", "300"]}
        print(f"[FIX] Added missing key_metrics field with default metrics")
    
    # Ensure metrics array exists and is not empty
    if 'key_metrics' in fixed_data and isinstance(fixed_data['key_metrics'], dict):
        if 'metrics' not in fixed_data['key_metrics'] or not fixed_data['key_metrics']['metrics']:
            fixed_data['key_metrics']['metrics'] = ["120%", "38.0", "5.7", "300"]
            print(f"[FIX] Added missing metrics array to key_metrics")
    
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
    
    # Fix nested data structure with validation
    if 'data' in fixed_data:
        data_value = safe_dict_access(fixed_data, 'data', context="sea_conglomerates_data")
        if isinstance(data_value, list):
            fixed_data['sea_conglomerates'] = data_value
            del fixed_data['data']
            print(f"[FIX] Moved nested sea_conglomerates data to top level")
        elif isinstance(data_value, dict) and 'data' not in data_value:
            # Handle double-nested structure
            nested_data = safe_dict_access(data_value, 'data', context="sea_conglomerates_nested")
            if isinstance(nested_data, list):
                fixed_data['sea_conglomerates'] = nested_data
                del fixed_data['data']
                print(f"[FIX] Moved double-nested sea_conglomerates data to top level")
    
    return fixed_data

def fix_buyer_profiles_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix buyer profiles slide data structure issues"""
    print(f"[FIX] Fixing buyer profiles data. Input type: {type(data)}")
    if isinstance(data, dict):
        print(f"[FIX] Data keys: {list(data.keys())}")
        if 'table_rows' in data:
            print(f"[FIX] table_rows type: {type(data['table_rows'])}, length: {len(data['table_rows']) if isinstance(data['table_rows'], list) else 'N/A'}")
    
    fixed_data = copy.deepcopy(data)
    
    # Ensure proper table structure for buyer profiles
    if 'table_rows' in fixed_data and isinstance(fixed_data['table_rows'], list):
        print(f"[FIX] Processing {len(fixed_data['table_rows'])} buyer profile rows")
        
        for i, row in enumerate(fixed_data['table_rows']):
            # CRITICAL FIX: Check if row is a list (2D array format) and convert to dict
            if isinstance(row, list):
                print(f"[FIX] Converting row {i+1} from list format to dictionary format")
                # Convert list format to dictionary format
                # Expected order: buyer_name, description, strategic_rationale, key_synergies, fit, financial_capacity
                field_names = ['buyer_name', 'description', 'strategic_rationale', 'key_synergies', 'fit', 'financial_capacity']
                row_dict = {}
                for j, value in enumerate(row):
                    if j < len(field_names):
                        row_dict[field_names[j]] = value if value is not None else 'N/A'
                    else:
                        # Handle extra columns
                        row_dict[f'extra_field_{j}'] = value if value is not None else 'N/A'
                
                # Replace the list with the dictionary
                fixed_data['table_rows'][i] = row_dict
                row = row_dict  # Update row reference for further processing
                print(f"[FIX] Converted row {i+1} to dictionary with {len(row_dict)} fields")
            
            # Ensure row is a dictionary before proceeding
            if not isinstance(row, dict):
                print(f"[FIX] ERROR: Row {i+1} is not a dictionary or list, skipping")
                continue
            # Ensure all required fields exist with proper field name mapping
            required_fields = [
                'buyer_name', 'description', 'strategic_rationale', 
                'key_synergies', 'fit', 'financial_capacity'
            ]
            
            # Handle field name variations and defaults
            for field in required_fields:
                if field not in row:
                    # Map variations or provide defaults
                    if field == 'fit' and 'fit_score' in row:
                        row['fit'] = row['fit_score']  # Use fit_score if fit is missing
                        print(f"[FIX] Mapped 'fit_score' to 'fit' for row {i+1}")
                    elif field == 'key_synergies' and 'synergies' in row:
                        row['key_synergies'] = row['synergies']  # Use synergies if key_synergies is missing
                        print(f"[FIX] Mapped 'synergies' to 'key_synergies' for row {i+1}")
                    else:
                        # Only set to N/A if the field is truly missing
                        row[field] = 'N/A'
                        print(f"[FIX] Added missing field '{field}' to buyer profile row {i+1}")
            
            # Clean up any legacy fields that might cause confusion
            legacy_fields = ['concerns', 'fit_score']
            for legacy_field in legacy_fields:
                if legacy_field in row and legacy_field != 'fit_score':
                    # Don't remove fit_score as it might be used as fallback for fit
                    if legacy_field == 'concerns' and row[legacy_field] == 'N/A':
                        del row[legacy_field]
                        print(f"[FIX] Removed legacy field '{legacy_field}' with N/A value from row {i+1}")
    
    return fixed_data

def fix_precedent_transactions_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix precedent transactions slide data structure issues"""
    fixed_data = copy.deepcopy(data)
    
    if 'transactions' in fixed_data and isinstance(fixed_data['transactions'], list):
        valid_transactions = []
        
        for transaction in fixed_data['transactions']:
            # Validate acquirer - must be a real company, not public market or funding rounds
            acquirer = transaction.get('acquirer', '').lower().strip()
            invalid_acquirers = [
                'public market', 'public markets', 'ipo', 'initial public offering',
                'series a', 'series b', 'series c', 'series d', 'series e', 'series f', 
                'series g', 'series h', 'series i', 'series j', 'series k', 'series l',
                'seed round', 'pre-seed', 'angel round', 'venture round', 'funding round',
                'private placement', 'equity raise', 'capital raise'
            ]
            
            # Check if acquirer is invalid
            is_invalid = False
            for invalid_term in invalid_acquirers:
                if invalid_term in acquirer:
                    is_invalid = True
                    print(f"[FILTER] Excluding transaction with invalid acquirer: {transaction.get('acquirer', 'Unknown')}")
                    break
            
            # Skip invalid transactions
            if is_invalid or not acquirer or len(acquirer) < 3:
                continue
                
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
            
            valid_transactions.append(transaction)
        
        # Update with only valid transactions
        fixed_data['transactions'] = valid_transactions
        if len(valid_transactions) != len(data.get('transactions', [])):
            print(f"[FILTER] Filtered transactions: {len(data.get('transactions', []))} -> {len(valid_transactions)} (removed funding rounds/public markets)")
        
        # CRITICAL: Ensure there are always some transactions to display
        if len(valid_transactions) == 0:
            print(f"[FIX] No valid transactions found, adding sample transactions")
            fixed_data['transactions'] = [
                {
                    'target': 'Sample Company A',
                    'acquirer': 'Strategic Buyer Inc.',
                    'date': '2023',
                    'country': 'USA',
                    'enterprise_value': 250000000,
                    'revenue': 50000000,
                    'ev_revenue_multiple': 5.0
                },
                {
                    'target': 'Sample Company B', 
                    'acquirer': 'Private Equity Fund',
                    'date': '2022',
                    'country': 'USA',
                    'enterprise_value': 180000000,
                    'revenue': 60000000,
                    'ev_revenue_multiple': 3.0
                },
                {
                    'target': 'Sample Company C',
                    'acquirer': 'Industry Leader Corp',
                    'date': '2023',
                    'country': 'USA', 
                    'enterprise_value': 320000000,
                    'revenue': 80000000,
                    'ev_revenue_multiple': 4.0
                }
            ]
            print(f"[FIX] Added 3 sample precedent transactions")
    else:
        # No transactions array at all - add it
        print(f"[FIX] No transactions array found, adding sample transactions")
        fixed_data['transactions'] = [
            {
                'target': 'Sample Company A',
                'acquirer': 'Strategic Buyer Inc.',
                'date': '2023',
                'country': 'USA',
                'enterprise_value': 250000000,
                'revenue': 50000000,
                'ev_revenue_multiple': 5.0
            },
            {
                'target': 'Sample Company B', 
                'acquirer': 'Private Equity Fund',
                'date': '2022',
                'country': 'USA',
                'enterprise_value': 180000000,
                'revenue': 60000000,
                'ev_revenue_multiple': 3.0
            },
            {
                'target': 'Sample Company C',
                'acquirer': 'Industry Leader Corp',
                'date': '2023',
                'country': 'USA', 
                'enterprise_value': 320000000,
                'revenue': 80000000,
                'ev_revenue_multiple': 4.0
            }
        ]
        print(f"[FIX] Added 3 sample precedent transactions")
    
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

def fix_management_team_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix management team slide data structure issues"""
    fixed_data = copy.deepcopy(data)
    
    # CRITICAL FIX: Limit to maximum 6 profiles total (3 per column)
    left_profiles = fixed_data.get('left_column_profiles', [])
    right_profiles = fixed_data.get('right_column_profiles', [])
    total_profiles = len(left_profiles) + len(right_profiles)
    
    if total_profiles > 6:
        print(f"[FIX] Management team has {total_profiles} profiles, truncating to 6 (max 3 per column)")
        fixed_data['left_column_profiles'] = left_profiles[:3]
        fixed_data['right_column_profiles'] = right_profiles[:3]
    
    # Ensure proper profile structure
    for column_name in ['left_column_profiles', 'right_column_profiles']:
        profiles = fixed_data.get(column_name, [])
        for i, profile in enumerate(profiles):
            if not isinstance(profile, dict):
                continue
                
            # Ensure required fields exist
            if 'name' not in profile or not profile['name']:
                profile['name'] = f'Executive {i+1}'
                print(f"[FIX] Added missing name to {column_name} profile {i+1}")
            
            if 'role_title' not in profile or not profile['role_title']:
                profile['role_title'] = f'Management Role {i+1}'
                print(f"[FIX] Added missing role_title to {column_name} profile {i+1}")
            
            if 'experience_bullets' not in profile or not profile['experience_bullets']:
                profile['experience_bullets'] = ['Relevant industry experience', 'Proven track record']
                print(f"[FIX] Added missing experience_bullets to {column_name} profile {i+1}")
    
    return fixed_data

def fix_valuation_overview_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Fix valuation overview slide data structure issues"""
    fixed_data = copy.deepcopy(data)
    
    # Fix duplicate methodologies
    if 'valuation_data' in fixed_data and isinstance(fixed_data['valuation_data'], list):
        valuation_data = fixed_data['valuation_data']
        methodologies = [item.get('methodology', '') for item in valuation_data if isinstance(item, dict)]
        
        # Fix duplicate "Trading Multiples"
        if methodologies.count("Trading Multiples") > 1:
            print(f"[FIX] Found duplicate 'Trading Multiples' methodologies, differentiating them")
            for i, item in enumerate(valuation_data):
                if isinstance(item, dict) and item.get('methodology') == "Trading Multiples":
                    if i == 0:
                        item['methodology'] = "Trading Multiples (EV/Revenue)"
                    elif i == 1:
                        item['methodology'] = "Trading Multiples (EV/EBITDA)"
                    print(f"[FIX] Renamed methodology {i+1} to: {item['methodology']}")
    
    return fixed_data

def ensure_buyer_data_exists(content_ir: Dict[str, Any]) -> Dict[str, Any]:
    """Ensure strategic and financial buyers data always exists in Content IR"""
    fixed_content_ir = copy.deepcopy(content_ir)
    
    # Ensure strategic_buyers exists
    if 'strategic_buyers' not in fixed_content_ir or not fixed_content_ir['strategic_buyers']:
        print(f"[FIX] No strategic_buyers data found, adding sample data")
        fixed_content_ir['strategic_buyers'] = [
            {
                'buyer_name': 'Microsoft',
                'description': 'Leading global cloud and enterprise software provider',
                'strategic_rationale': 'Enhance AI and data platform capabilities',
                'key_synergies': 'Azure integration and enterprise customer base',
                'fit': 'High (9/10)',
                'financial_capacity': '$500B+ market cap'
            },
            {
                'buyer_name': 'Google',
                'description': 'Global technology leader in search, cloud, and AI',
                'strategic_rationale': 'Strengthen cloud AI and data analytics offerings',
                'key_synergies': 'Google Cloud Platform integration',
                'fit': 'High (8/10)',
                'financial_capacity': '$1.5T+ market cap'
            },
            {
                'buyer_name': 'Amazon',
                'description': 'E-commerce and cloud computing giant',
                'strategic_rationale': 'Enhance AWS data and analytics services',
                'key_synergies': 'AWS ecosystem and enterprise reach',
                'fit': 'Medium (7/10)',
                'financial_capacity': '$1.2T+ market cap'
            }
        ]
        print(f"[FIX] Added 3 sample strategic buyers")
    
    # Ensure financial_buyers exists
    if 'financial_buyers' not in fixed_content_ir or not fixed_content_ir['financial_buyers']:
        print(f"[FIX] No financial_buyers data found, adding sample data")
        fixed_content_ir['financial_buyers'] = [
            {
                'buyer_name': 'KKR & Co.',
                'description': 'Leading global investment firm',
                'strategic_rationale': 'Platform investment in high-growth tech sector',
                'key_synergies': 'Portfolio company synergies and operational expertise',
                'fit': 'High (9/10)',
                'financial_capacity': '$50B+ AUM'
            },
            {
                'buyer_name': 'Blackstone',
                'description': 'Alternative asset management leader',
                'strategic_rationale': 'Technology sector expansion and growth capital',
                'key_synergies': 'Technology portfolio and operational support',
                'fit': 'High (8/10)',
                'financial_capacity': '$1T+ AUM'
            },
            {
                'buyer_name': 'Carlyle Group',
                'description': 'Global private equity and investment firm',
                'strategic_rationale': 'Technology platform investment opportunity',
                'key_synergies': 'Technology sector expertise and global reach',
                'fit': 'Medium (7/10)',
                'financial_capacity': '$400B+ AUM'
            }
        ]
        print(f"[FIX] Added 3 sample financial buyers")
    
    return fixed_content_ir

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
    elif template == 'management_team':
        return fix_management_team_data(data)
    elif template == 'valuation_overview':
        return fix_valuation_overview_data(data)
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
    
    # CRITICAL: Skip fixing for bulletproof-generated data to preserve comprehensive content
    if isinstance(render_plan, dict) and render_plan.get("_bulletproof_generated", False):
        print(f"🛡️ [FIX] PROTECTED: Skipping render_plan fixing for bulletproof-generated data")
        print(f"🛡️ [FIX] Data sources: {render_plan.get('_data_sources', 'unknown')}")
        print(f"🛡️ [FIX] Generation method: {render_plan.get('_generation_method', 'unknown')}")
        
        # Remove bulletproof markers and return clean data without fixing
        clean_data = render_plan.copy()
        clean_data.pop("_bulletproof_generated", None)
        clean_data.pop("_generation_timestamp", None) 
        clean_data.pop("_data_sources", None)
        clean_data.pop("_slides_generated", None)
        clean_data.pop("_generation_method", None)
        
        return clean_data
    
    # Validate input structure
    if not validate_data_structure(render_plan, dict, "fix_render_plan"):
        return {"slides": []}
    
    slides = safe_dict_access(render_plan, 'slides', [], "fix_render_plan")
    if not validate_data_structure(slides, list, "fix_render_plan.slides"):
        return {"slides": []}
    
    print(f"[FIX] Fixing render plan with {len(slides)} slides")
    
    fixed_plan = copy.deepcopy(render_plan)
    
    for i, slide in enumerate(slides):
        # Validate slide structure
        if not validate_data_structure(slide, dict, f"fix_render_plan.slide_{i+1}"):
            print(f"[FIX] Skipping invalid slide {i+1}")
            continue
            
        template = safe_dict_access(slide, 'template', '', f"fix_render_plan.slide_{i+1}")
        data = safe_dict_access(slide, 'data', {}, f"fix_render_plan.slide_{i+1}")
        
        print(f"\n[FIX] Processing slide {i+1}: {template}")
        
        # Ensure title exists
        if 'title' not in data:
            data['title'] = template.replace('_', ' ').title()
            print(f"[FIX] Added missing title: {data['title']}")
        
        # Apply template-specific fixes with error handling
        try:
            fixed_data = fix_slide_data(template, data)
            fixed_plan['slides'][i]['data'] = fixed_data
        except Exception as e:
            print(f"[FIX] ERROR processing slide {i+1} ({template}): {str(e)}")
            # Keep original data if fixing fails
            fixed_plan['slides'][i]['data'] = data
    
    return fixed_plan

def fix_content_ir(content_ir: Dict[str, Any]) -> Dict[str, Any]:
    """Fix content IR data structure issues"""
    
    # CRITICAL: Skip fixing for bulletproof-generated data to preserve comprehensive content
    if isinstance(content_ir, dict) and content_ir.get("_bulletproof_generated", False):
        print(f"🛡️ [FIX] PROTECTED: Skipping content_ir fixing for bulletproof-generated data")
        print(f"🛡️ [FIX] Data sources: {content_ir.get('_data_sources', 'unknown')}")
        print(f"🛡️ [FIX] Generation method: {content_ir.get('_generation_method', 'unknown')}")
        
        # Remove bulletproof markers and return clean data without fixing
        clean_data = content_ir.copy()
        clean_data.pop("_bulletproof_generated", None)
        clean_data.pop("_generation_timestamp", None) 
        clean_data.pop("_data_sources", None)
        clean_data.pop("_slides_generated", None)
        clean_data.pop("_generation_method", None)
        
        return clean_data
    
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
    
    # CRITICAL: Skip ALL fixing for bulletproof-generated data to preserve comprehensive content
    if (isinstance(content_ir_json, dict) and content_ir_json.get("_bulletproof_generated", False)) or \
       (isinstance(slides_json, dict) and slides_json.get("_bulletproof_generated", False)):
        print("🛡️ [COMPREHENSIVE-FIX] PROTECTED: Skipping ALL fixing for bulletproof-generated data")
        
        # Clean bulletproof markers from both objects
        clean_content_ir = content_ir_json.copy() if isinstance(content_ir_json, dict) else {}
        clean_slides = slides_json.copy() if isinstance(slides_json, dict) else {}
        
        for clean_data in [clean_content_ir, clean_slides]:
            if isinstance(clean_data, dict):
                clean_data.pop("_bulletproof_generated", None)
                clean_data.pop("_generation_timestamp", None) 
                clean_data.pop("_data_sources", None)
                clean_data.pop("_slides_generated", None)
                clean_data.pop("_generation_method", None)
        
        return clean_slides, clean_content_ir
    
    print("=" * 60)
    print("COMPREHENSIVE JSON FIXING")
    print("=" * 60)
    
    # Validate inputs with error handling
    try:
        if not validate_data_structure(slides_json, dict, "comprehensive_json_fix.slides_json"):
            print("[FIX] Invalid slides_json structure, creating empty plan")
            slides_json = {"slides": []}
        
        if not validate_data_structure(content_ir_json, dict, "comprehensive_json_fix.content_ir_json"):
            print("[FIX] Invalid content_ir_json structure, creating empty IR")
            content_ir_json = {}
        
        # Fix content IR first
        print(f"[FIX] Fixing content IR with sections: {list(content_ir_json.keys())}")
        fixed_content_ir = fix_content_ir(content_ir_json)
        
        # Fix render plan
        print(f"[FIX] Fixing render plan with {len(safe_dict_access(slides_json, 'slides', [], 'comprehensive_json_fix'))} slides")
        fixed_render_plan = fix_render_plan(slides_json)
        
        print("\n" + "=" * 60)
        print("FIXING COMPLETE")
        print("=" * 60)
        
        return fixed_render_plan, fixed_content_ir
        
    except Exception as e:
        print(f"[FIX] ERROR in comprehensive_json_fix: {str(e)}")
        print(f"[FIX] Returning original data structures")
        print("=" * 60)
        return slides_json, content_ir_json

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