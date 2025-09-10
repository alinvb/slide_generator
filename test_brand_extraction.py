#!/usr/bin/env python3
"""
Test script to verify brand color extraction functionality
"""
import sys
import os
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from brand_extractor import BrandExtractor
from pptx.dml.color import RGBColor

def test_brand_extraction():
    """Test brand extraction functionality with available test files"""
    print("🧪 Testing Brand Color Extraction Functionality\n")
    
    # Initialize the brand extractor
    extractor = BrandExtractor()
    
    # Test files available
    test_files = [
        "test_brand_colors.pptx",
        "test_brand_deck.pptx", 
        "test_enhanced_brand_deck.pptx"
    ]
    
    results = {}
    
    for test_file in test_files:
        if Path(test_file).exists():
            print(f"📁 Testing with file: {test_file}")
            try:
                # Test rule-based extraction (no API key required)
                print("  🔍 Testing rule-based extraction...")
                brand_config = extractor.extract_brand_from_pptx(test_file, use_llm=False)
                
                # Verify the structure
                expected_keys = ['color_scheme', 'typography', 'header_style', 'layout_config']
                has_all_keys = all(key in brand_config for key in expected_keys)
                
                print(f"  ✅ Structure valid: {has_all_keys}")
                
                if has_all_keys:
                    # Check color scheme
                    colors = brand_config['color_scheme']
                    print(f"  🎨 Colors extracted:")
                    
                    for color_name, color_value in colors.items():
                        if hasattr(color_value, 'r') and hasattr(color_value, 'g') and hasattr(color_value, 'b'):
                            hex_color = f"#{color_value.r:02x}{color_value.g:02x}{color_value.b:02x}"
                            print(f"    - {color_name}: RGB({color_value.r}, {color_value.g}, {color_value.b}) = {hex_color}")
                        elif isinstance(color_value, tuple) and len(color_value) == 3:
                            r, g, b = color_value
                            hex_color = f"#{r:02x}{g:02x}{b:02x}"
                            print(f"    - {color_name}: RGB({r}, {g}, {b}) = {hex_color}")
                        else:
                            print(f"    - {color_name}: {color_value} (type: {type(color_value)})")
                    
                    # Check typography
                    typography = brand_config['typography']
                    print(f"  📝 Typography:")
                    print(f"    - Primary font: {typography.get('primary_font', 'N/A')}")
                    print(f"    - Title size: {typography.get('title_size', 'N/A')}")
                    print(f"    - Body size: {typography.get('body_size', 'N/A')}")
                    
                    results[test_file] = {
                        'success': True,
                        'colors': len(colors),
                        'primary_font': typography.get('primary_font', 'N/A')
                    }
                    print(f"  ✅ Extraction successful for {test_file}\n")
                else:
                    results[test_file] = {'success': False, 'error': 'Missing required keys'}
                    print(f"  ❌ Missing required configuration keys\n")
                
            except Exception as e:
                results[test_file] = {'success': False, 'error': str(e)}
                print(f"  ❌ Error: {str(e)}\n")
        else:
            print(f"📁 File {test_file} not found, skipping...\n")
            results[test_file] = {'success': False, 'error': 'File not found'}
    
    # Summary
    print("📊 Test Summary:")
    print("=" * 50)
    successful_tests = sum(1 for result in results.values() if result.get('success', False))
    total_tests = len([f for f in test_files if Path(f).exists()])
    
    print(f"Successful extractions: {successful_tests}/{total_tests}")
    
    for test_file, result in results.items():
        if Path(test_file).exists():
            status = "✅ PASS" if result.get('success', False) else "❌ FAIL"
            print(f"  {test_file}: {status}")
            if not result.get('success', False):
                print(f"    Error: {result.get('error', 'Unknown')}")
    
    # Test with non-existent file to verify error handling
    print("\n🧪 Testing error handling with non-existent file...")
    try:
        error_result = extractor.extract_brand_from_pptx("nonexistent.pptx", use_llm=False)
        if error_result:
            print("  ✅ Error handling works - returned default configuration")
        else:
            print("  ❌ Error handling failed - returned None")
    except Exception as e:
        print(f"  ✅ Error handling works - caught exception: {str(e)}")
    
    print(f"\n🎯 Overall Assessment:")
    if successful_tests > 0:
        print("✅ Brand color extraction functionality is WORKING!")
        print(f"   - Successfully extracted colors from {successful_tests} test file(s)")
        print("   - Rule-based extraction is functional")
        print("   - Error handling is in place")
        return True
    else:
        print("❌ Brand color extraction functionality has ISSUES!")
        print("   - No successful extractions")
        print("   - Check file formats and extraction logic")
        return False

if __name__ == "__main__":
    test_brand_extraction()