#!/usr/bin/env python3
"""
Test script to identify and fix current JSON processing errors
"""

import json
import traceback
import sys
from pathlib import Path

def load_json_file(filepath):
    """Load and validate JSON file"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        print(f"✅ Successfully loaded {filepath}")
        return data, None
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return None, str(e)

def test_json_files():
    """Test all JSON files for errors"""
    
    print("🔍 Testing JSON files for errors...\n")
    
    # Test the user's provided JSON data
    user_slides_json = '''{"slides": [{"template": "business_overview", "data": {"title": "Business Overview", "description": "Saudi Aramco is the world's largest integrated oil and gas producer, engaged in exploration, production, refining, chemicals, and global distribution. It is the most profitable energy company worldwide and a central pillar of Saudi Arabia's economy.", "timeline": {"start_year": 1933, "end_year": 2025}, "highlights": ["Largest proven oil reserves and production globally", "Industry-leading margins and financial strength", "Extensive global downstream and chemicals operations"], "services": ["Upstream oil and gas production", "Downstream refining and petrochemicals", "Energy trading and logistics"], "positioning_desc": "Aramco is positioned as the global leader in energy scale, operational efficiency, and profitability, with unmatched reserves and integrated infrastructure."}}]}'''
    
    try:
        user_data = json.loads(user_slides_json)
        print("✅ User provided JSON is valid")
    except json.JSONDecodeError as e:
        print(f"❌ User provided JSON is invalid: {e}")
        return False
    
    # Test existing files
    json_files = [
        'complete_content_ir.json',
        'complete_render_plan.json',
        'corrected_content_ir.json', 
        'corrected_render_plan.json',
        'fixed_render_plan.json'
    ]
    
    errors_found = []
    
    for filename in json_files:
        filepath = Path(filename)
        if filepath.exists():
            data, error = load_json_file(filepath)
            if error:
                errors_found.append((filename, error))
        else:
            print(f"⚠️ File {filename} does not exist")
    
    if errors_found:
        print(f"\n❌ Found {len(errors_found)} JSON errors:")
        for filename, error in errors_found:
            print(f"  - {filename}: {error}")
        return False
    else:
        print(f"\n✅ All existing JSON files are valid")
        return True

def test_vector_db_import():
    """Test vector database imports"""
    print("\n🔍 Testing vector database imports...\n")
    
    try:
        from vector_db import VectorDBManager, get_vector_db_manager
        print("✅ Vector DB imports successful")
        return True
    except Exception as e:
        print(f"❌ Vector DB import error: {e}")
        traceback.print_exc()
        return False

def test_app_imports():
    """Test main app imports"""
    print("\n🔍 Testing main app imports...\n")
    
    try:
        # Test individual components first
        print("Testing catalog_loader...")
        from catalog_loader import TemplateCatalog
        print("✅ TemplateCatalog import successful")
        
        print("Testing brand_extractor...")
        from brand_extractor import BrandExtractor  
        print("✅ BrandExtractor import successful")
        
        print("Testing executor...")
        from executor import execute_plan
        print("✅ execute_plan import successful")
        
        print("Testing validators...")
        import validators
        print("✅ validators import successful")
        
        return True
        
    except Exception as e:
        print(f"❌ App import error: {e}")
        traceback.print_exc()
        return False

def analyze_user_json_structure():
    """Analyze the structure of user-provided JSON for potential issues"""
    print("\n🔍 Analyzing user JSON structure...\n")
    
    user_slides_json = '''{"slides": [{"template": "business_overview", "data": {"title": "Business Overview", "description": "Saudi Aramco is the world's largest integrated oil and gas producer, engaged in exploration, production, refining, chemicals, and global distribution. It is the most profitable energy company worldwide and a central pillar of Saudi Arabia's economy.", "timeline": {"start_year": 1933, "end_year": 2025}, "highlights": ["Largest proven oil reserves and production globally", "Industry-leading margins and financial strength", "Extensive global downstream and chemicals operations"], "services": ["Upstream oil and gas production", "Downstream refining and petrochemicals", "Energy trading and logistics"], "positioning_desc": "Aramco is positioned as the global leader in energy scale, operational efficiency, and profitability, with unmatched reserves and integrated infrastructure."}}]}'''
    
    user_content_json = '''{"entities": {"company": {"name": "Saudi Aramco"}}, "facts": {"years": ["2020", "2021", "2022", "2023", "2024E"], "revenue_usd_m": [229000, 400000, 495100, 480570, 461560], "ebitda_usd_m": [100000, 180000, 239000, 223000, 215000], "ebitda_margins": [43.7, 45.0, 48.3, 46.4, 46.6]}}'''
    
    try:
        slides_data = json.loads(user_slides_json)
        content_data = json.loads(user_content_json)
        
        print("✅ User JSON structure is valid")
        print(f"📊 Slides count: {len(slides_data['slides'])}")
        print(f"📊 Content sections: {list(content_data.keys())}")
        
        # Check for common issues
        print("\n🔍 Checking for potential issues...")
        
        # Check slide structure
        for i, slide in enumerate(slides_data['slides']):
            if 'template' not in slide:
                print(f"❌ Slide {i}: Missing 'template' field")
            if 'data' not in slide:
                print(f"❌ Slide {i}: Missing 'data' field")
            elif 'title' not in slide['data']:
                print(f"❌ Slide {i}: Missing 'title' in data")
        
        return True
        
    except Exception as e:
        print(f"❌ Error analyzing user JSON: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting comprehensive error analysis...\n")
    
    success = True
    
    # Test JSON files
    if not test_json_files():
        success = False
    
    # Test imports
    if not test_vector_db_import():
        success = False
        
    if not test_app_imports():
        success = False
    
    # Analyze user JSON
    if not analyze_user_json_structure():
        success = False
    
    if success:
        print("\n🎉 All tests passed! No major errors found.")
        sys.exit(0)
    else:
        print("\n💥 Errors found. Check output above for details.")
        sys.exit(1)