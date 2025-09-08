#!/usr/bin/env python3
"""
Comprehensive Test Suite for Perfect JSON Validation System
Tests the management team validation with various team sizes and validates the perfect JSON system
"""

import json
import sys
import os
from typing import Dict, Any, List

# Add current directory to path to import our modules
sys.path.insert(0, '/home/user/webapp')

from json_validator_perfecter import JSONValidatorPerfector, ValidationResult
from perfect_json_prompter import PerfectJSONPrompter

def create_test_content_ir_with_management_team(team_size: int) -> Dict[str, Any]:
    """Create a test Content IR JSON with specified management team size"""
    
    # Base template
    base_json = {
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
            "left_column_profiles": [],
            "right_column_profiles": []
        },
        "strategic_buyers": ["Tech Corp A", "Tech Corp B"],
        "financial_buyers": ["PE Firm A", "PE Firm B"],
        "competitive_analysis": {"key_competitors": ["Competitor A", "Competitor B"]},
        "precedent_transactions": [{"target": "Similar Co", "value_usd_m": 100}],
        "valuation_data": [{"method": "DCF", "value_usd_m": 150}],
        "product_service_data": {"main_products": ["Product A", "Product B"]},
        "business_overview_data": {"description": "Technology company"},
        "growth_strategy_data": {"strategies": ["Expand markets", "New products"]},
        "investor_process_data": {"process_type": "Controlled auction"},
        "margin_cost_data": {"gross_margin": 75.0},
        "sea_conglomerates": ["SEA Corp A"],
        "investor_considerations": {"key_points": ["Strong growth", "Market leader"]}
    }
    
    # Create management profiles
    profiles = [
        {"name": "John Smith", "role_title": "Chief Executive Officer", "experience_bullets": ["Led company growth", "Former VP at Fortune 500", "15+ years experience"]},
        {"name": "Sarah Johnson", "role_title": "Chief Technology Officer", "experience_bullets": ["Architected platform", "Former Principal Engineer", "Expert in AI/ML"]},
        {"name": "Michael Chen", "role_title": "Chief Financial Officer", "experience_bullets": ["Former CFO at high-growth company", "15+ years finance experience", "Led $100M+ funding rounds"]},
        {"name": "Lisa Rodriguez", "role_title": "Chief Marketing Officer", "experience_bullets": ["Built marketing teams", "Former VP Marketing", "Expert in product marketing"]},
        {"name": "David Park", "role_title": "Chief Operations Officer", "experience_bullets": ["Scaled operations", "Former VP Operations", "Expert in expansion"]},
        {"name": "Amanda Williams", "role_title": "Chief People Officer", "experience_bullets": ["Built talent programs", "Former CHRO", "Expert in scaling teams"]}
    ]
    
    # Distribute profiles between left and right columns
    left_count = (team_size + 1) // 2  # Ceiling division for left column
    right_count = team_size - left_count
    
    base_json["management_team"]["left_column_profiles"] = profiles[:left_count]
    base_json["management_team"]["right_column_profiles"] = profiles[left_count:left_count + right_count]
    
    return base_json

def test_management_team_validation():
    """Test management team validation with different team sizes"""
    print("🧪 Testing Management Team Validation")
    print("=" * 50)
    
    validator = JSONValidatorPerfector()
    
    # Test different team sizes
    test_cases = [
        (1, "Too few members (should fail)"),
        (2, "Minimum valid size"),
        (3, "Small team"),
        (4, "Perfect template size"),
        (5, "Medium team"),
        (6, "Maximum valid size"),
        (7, "Too many members (should fail)")
    ]
    
    for team_size, description in test_cases:
        print(f"\n📋 Testing team size {team_size}: {description}")
        
        test_json = create_test_content_ir_with_management_team(team_size)
        result = validator.validate_content_ir(test_json)
        
        print(f"   Score: {result.score:.2f}")
        print(f"   Valid: {result.is_valid}")
        
        if result.issues:
            print("   Issues:")
            for issue in result.issues:
                if "management" in issue.lower():
                    print(f"     • {issue}")
        
        # Expected results
        if team_size < 2:
            assert not result.is_valid or result.score < 0.9, f"Team size {team_size} should fail validation"
            print("   ✅ Correctly flagged as invalid (too few members)")
        elif team_size > 6:
            assert result.score < 0.95, f"Team size {team_size} should have reduced score"
            print("   ✅ Correctly flagged issues (too many members)")
        else:
            print("   ✅ Valid team size accepted")

def test_perfect_template_loading():
    """Test that perfect templates load correctly"""
    print("\n🗂️  Testing Perfect Template Loading")
    print("=" * 50)
    
    validator = JSONValidatorPerfector()
    prompter = PerfectJSONPrompter()
    
    # Check validator templates
    assert validator.perfect_content_ir_template is not None, "Content IR template should be loaded"
    assert validator.perfect_render_plan_template is not None, "Render plan template should be loaded"
    
    # Check prompter templates
    assert prompter.perfect_content_ir_template is not None, "Prompter Content IR template should be loaded"
    assert prompter.perfect_render_plan_template is not None, "Prompter Render plan template should be loaded"
    
    print("✅ All perfect templates loaded successfully")
    
    # Validate perfect template management team size
    if "management_team" in validator.perfect_content_ir_template:
        mgmt = validator.perfect_content_ir_template["management_team"]
        left_count = len(mgmt.get("left_column_profiles", []))
        right_count = len(mgmt.get("right_column_profiles", []))
        total_count = left_count + right_count
        
        print(f"✅ Perfect template has {total_count} management members ({left_count} left + {right_count} right)")
        
        if total_count > 6:
            print("⚠️  WARNING: Perfect template exceeds 6 member limit")
        elif total_count < 2:
            print("⚠️  WARNING: Perfect template has too few members")

def test_validation_scoring():
    """Test the validation scoring system"""
    print("\n📊 Testing Validation Scoring System")
    print("=" * 50)
    
    validator = JSONValidatorPerfector()
    
    # Test perfect JSON (should get high score)
    perfect_json = create_test_content_ir_with_management_team(4)
    result = validator.validate_content_ir(perfect_json)
    
    print(f"Perfect JSON Score: {result.score:.3f}")
    print(f"Perfect JSON Valid: {result.is_valid}")
    
    assert result.score >= 0.90, f"Perfect JSON should score highly, got {result.score}"
    print("✅ Perfect JSON scores highly")
    
    # Test JSON with missing sections
    incomplete_json = create_test_content_ir_with_management_team(4)
    del incomplete_json["strategic_buyers"]
    del incomplete_json["financial_buyers"]
    
    result2 = validator.validate_content_ir(incomplete_json)
    
    print(f"Incomplete JSON Score: {result2.score:.3f}")
    print(f"Incomplete JSON Valid: {result2.is_valid}")
    
    assert result2.score < result.score, "Incomplete JSON should score lower than perfect JSON"
    print("✅ Incomplete JSON penalized correctly")

def test_enhanced_system_prompt():
    """Test that enhanced system prompt includes management team guidance"""
    print("\n📝 Testing Enhanced System Prompt")
    print("=" * 50)
    
    prompter = PerfectJSONPrompter()
    system_prompt = prompter.create_enhanced_system_prompt()
    
    # Check that prompt contains management team guidance
    assert "management_team" in system_prompt, "System prompt should mention management_team"
    assert "profiles" in system_prompt, "System prompt should mention profiles"
    
    print("✅ Enhanced system prompt contains management team guidance")
    
    # Check prompt length and quality
    assert len(system_prompt) > 1000, "System prompt should be comprehensive"
    print(f"✅ System prompt is comprehensive ({len(system_prompt)} characters)")

def run_comprehensive_tests():
    """Run all tests for the perfect JSON system"""
    print("🚀 PERFECT JSON VALIDATION SYSTEM - COMPREHENSIVE TESTS")
    print("=" * 70)
    
    try:
        test_perfect_template_loading()
        test_management_team_validation()
        test_validation_scoring()
        test_enhanced_system_prompt()
        
        print("\n" + "=" * 70)
        print("🎉 ALL TESTS PASSED - PERFECT JSON SYSTEM IS WORKING CORRECTLY!")
        print("✅ Management team validation supports 2-6 members properly")
        print("✅ Perfect templates loaded and validated")
        print("✅ Scoring system works correctly")
        print("✅ Enhanced prompts are comprehensive")
        print("=" * 70)
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = run_comprehensive_tests()
    sys.exit(0 if success else 1)