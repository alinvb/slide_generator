#!/usr/bin/env python3
"""
Debug validation issues to understand why perfect JSON gets low scores
"""

import json
import sys
import os

# Add current directory to path to import our modules
sys.path.insert(0, '/home/user/webapp')

from json_validator_perfecter import JSONValidatorPerfector, ValidationResult

def create_simple_test_json():
    """Create a simple test JSON"""
    return {
        "entities": {
            "company": {
                "name": "Test Company",
                "industry": "Technology",
                "location": "San Francisco, USA"
            }
        },
        "facts": {
            "years": [2022, 2023, 2024],
            "revenue_usd_m": [10.0, 25.0, 45.0],
            "ebitda_usd_m": [1.0, 3.0, 8.0],
            "ebitda_margins": [10.0, 12.0, 17.8]
        },
        "management_team": {
            "left_column_profiles": [
                {"name": "John Smith", "role_title": "CEO", "experience_bullets": ["Led growth", "Former VP", "15+ years exp"]}
            ],
            "right_column_profiles": [
                {"name": "Sarah Johnson", "role_title": "CTO", "experience_bullets": ["Architected platform", "Former Engineer", "Expert in AI"]}
            ]
        },
        "strategic_buyers": ["Tech Corp A"],
        "financial_buyers": ["PE Firm A"],
        "competitive_analysis": {"key_competitors": ["Competitor A"]},
        "precedent_transactions": [{"target": "Similar Co", "value_usd_m": 100}],
        "valuation_data": [{"method": "DCF", "value_usd_m": 150}],
        "product_service_data": {"main_products": ["Product A"]},
        "business_overview_data": {"description": "Technology company"},
        "growth_strategy_data": {"strategies": ["Expand markets"]},
        "investor_process_data": {"process_type": "Controlled auction"},
        "margin_cost_data": {"gross_margin": 75.0},
        "sea_conglomerates": ["SEA Corp A"],
        "investor_considerations": {"key_points": ["Strong growth"]}
    }

def debug_validation():
    """Debug what's causing low validation scores"""
    print("🐛 DEBUGGING VALIDATION ISSUES")
    print("=" * 50)
    
    validator = JSONValidatorPerfector()
    test_json = create_simple_test_json()
    
    result = validator.validate_content_ir(test_json)
    
    print(f"Overall Score: {result.score:.3f}")
    print(f"Valid: {result.is_valid}")
    print(f"Perfect Score Threshold: {validator.perfect_score_threshold}")
    
    print("\nDetailed Issues:")
    for issue in result.issues:
        print(f"  ❌ {issue}")
    
    print("\nMissing Fields:")
    for field in result.missing_fields:
        print(f"  📋 {field}")
    
    print("\nInvalid Types:")
    for field in result.invalid_types:
        print(f"  🔧 {field}")
    
    print("\nEmpty Fields:")
    for field in result.empty_fields:
        print(f"  📭 {field}")
    
    print("\nSuggestions:")
    for suggestion in result.suggestions:
        print(f"  💡 {suggestion}")

if __name__ == "__main__":
    debug_validation()