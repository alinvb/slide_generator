#!/usr/bin/env python3
"""
Test script to debug brand styling and template application issues
"""
import sys
sys.path.append('.')

from slide_templates import get_brand_styling, get_template_styling
from pptx.dml.color import RGBColor

def test_template_styling():
    """Test if template styling is working correctly"""
    print("🧪 Testing template styling...")
    
    # Test each template
    templates = ["modern", "professional", "corporate", "investor"]
    
    for template in templates:
        print(f"\n📋 Testing template: {template}")
        try:
            config = get_template_styling(template)
            print(f"✅ Template config loaded: {len(config.get('color_scheme', {}))} colors, {len(config.get('typography', {}))} fonts")
            
            # Test color scheme
            color_scheme = config.get('color_scheme', {})
            for color_name, color_value in color_scheme.items():
                if hasattr(color_value, 'r'):
                    print(f"  🎨 {color_name}: RGB({color_value.r}, {color_value.g}, {color_value.b})")
                else:
                    print(f"  ❌ {color_name}: Invalid color format - {type(color_value)}")
            
        except Exception as e:
            print(f"❌ Template {template} failed: {e}")

def test_brand_styling():
    """Test brand styling function"""
    print("\n🎨 Testing brand styling function...")
    
    # Test with no brand config (should use template defaults)
    print("\n📋 Test 1: No brand config")
    try:
        colors, fonts = get_brand_styling(template_name="modern")
        print(f"✅ Default styling loaded: {len(colors)} colors, {len(fonts)} fonts")
        if 'primary' in colors:
            primary = colors['primary']
            print(f"  🎨 Primary color: RGB({primary.r}, {primary.g}, {primary.b})")
    except Exception as e:
        print(f"❌ Default styling failed: {e}")
    
    # Test with mock brand config
    print("\n📋 Test 2: Mock brand config")
    mock_brand_config = {
        'color_scheme': {
            'primary': '#FF0000',  # Red
            'secondary': '#00FF00'  # Green
        },
        'typography': {
            'primary_font': 'Calibri',
            'title_size': '28'
        }
    }
    
    try:
        colors, fonts = get_brand_styling(brand_config=mock_brand_config, template_name="modern")
        print(f"✅ Brand styling loaded: {len(colors)} colors, {len(fonts)} fonts")
        if 'primary' in colors:
            primary = colors['primary']
            print(f"  🎨 Primary color: RGB({primary.r}, {primary.g}, {primary.b}) - Should be red (255,0,0)")
        if 'primary_font' in fonts:
            print(f"  📝 Primary font: {fonts['primary_font']} - Should be Calibri")
    except Exception as e:
        print(f"❌ Brand styling failed: {e}")

if __name__ == "__main__":
    print("🔍 Brand Styling Debug Test")
    print("=" * 50)
    
    test_template_styling()
    test_brand_styling()
    
    print("\n" + "=" * 50)
    print("✅ Brand styling test completed")