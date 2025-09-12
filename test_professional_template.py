#!/usr/bin/env python3
"""
Test Professional template with gold and blue colors
"""

from slide_templates import get_template_styling
from pptx.dml.color import RGBColor

def test_professional_template():
    print("🎨 Testing Professional Template Gold & Blue Colors")
    print("=" * 60)
    
    # Test Professional template
    professional_config = get_template_styling("professional")
    
    print("📋 PROFESSIONAL TEMPLATE:")
    colors = professional_config["color_scheme"]
    typography = professional_config["typography"]
    
    print("🎨 Color Scheme:")
    primary_rgb = (colors['primary']._color_val >> 16 & 0xFF, colors['primary']._color_val >> 8 & 0xFF, colors['primary']._color_val & 0xFF)
    secondary_rgb = (colors['secondary']._color_val >> 16 & 0xFF, colors['secondary']._color_val >> 8 & 0xFF, colors['secondary']._color_val & 0xFF)
    accent_rgb = (colors['accent']._color_val >> 16 & 0xFF, colors['accent']._color_val >> 8 & 0xFF, colors['accent']._color_val & 0xFF)
    text_rgb = (colors['text']._color_val >> 16 & 0xFF, colors['text']._color_val >> 8 & 0xFF, colors['text']._color_val & 0xFF)
    
    print(f"  Primary (Blue): RGB{primary_rgb}")
    print(f"  Secondary (Gold): RGB{secondary_rgb}")
    print(f"  Accent: RGB{accent_rgb}")
    print(f"  Text: RGB{text_rgb}")
    
    print("🔤 Typography:")
    print(f"  Font: {typography['primary_font']}")
    print(f"  Title Size: {typography['title_size']}")
    print(f"  Body Size: {typography['body_size']}")
    
    # Verify it's the gold and blue we expect
    expected_blue = RGBColor(24, 58, 88)   # Professional blue
    expected_gold = RGBColor(181, 151, 91)  # Professional gold
    
    blue_match = (primary_rgb == (24, 58, 88))
    gold_match = (secondary_rgb == (181, 151, 91))
    
    print(f"\n✅ Validation:")
    print(f"  Blue Primary Color: {'✅ CORRECT' if blue_match else '❌ WRONG'} - RGB(24, 58, 88)")
    print(f"  Gold Secondary Color: {'✅ CORRECT' if gold_match else '❌ WRONG'} - RGB(181, 151, 91)")
    
    # Test Modern template for comparison
    print(f"\n📋 MODERN TEMPLATE (for comparison):")
    modern_config = get_template_styling("modern")
    modern_colors = modern_config["color_scheme"]
    
    print("🎨 Modern Color Scheme:")
    modern_primary = (modern_colors['primary']._color_val >> 16 & 0xFF, modern_colors['primary']._color_val >> 8 & 0xFF, modern_colors['primary']._color_val & 0xFF)
    modern_secondary = (modern_colors['secondary']._color_val >> 16 & 0xFF, modern_colors['secondary']._color_val >> 8 & 0xFF, modern_colors['secondary']._color_val & 0xFF)
    
    print(f"  Primary: RGB{modern_primary}")
    print(f"  Secondary: RGB{modern_secondary}")
    
    # Test Corporate template for comparison
    print(f"\n📋 CORPORATE TEMPLATE (for comparison):")
    corporate_config = get_template_styling("corporate")
    corporate_colors = corporate_config["color_scheme"]
    
    print("🎨 Corporate Color Scheme:")
    corporate_primary = (corporate_colors['primary']._color_val >> 16 & 0xFF, corporate_colors['primary']._color_val >> 8 & 0xFF, corporate_colors['primary']._color_val & 0xFF)
    corporate_secondary = (corporate_colors['secondary']._color_val >> 16 & 0xFF, corporate_colors['secondary']._color_val >> 8 & 0xFF, corporate_colors['secondary']._color_val & 0xFF)
    
    print(f"  Primary: RGB{corporate_primary}")
    print(f"  Secondary: RGB{corporate_secondary}")
    
    print(f"\n🏆 SUMMARY:")
    if blue_match and gold_match:
        print("✅ Professional template successfully updated with gold and blue colors!")
        print("🎯 Professional template now uses the classic investment banking color scheme")
        return True
    else:
        print("❌ Professional template colors not set correctly")
        return False

if __name__ == "__main__":
    test_professional_template()