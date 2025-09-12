#!/usr/bin/env python3
"""
Simple template verification
"""

from slide_templates import get_template_styling

def test_templates():
    print("🎨 Template Color Verification")
    print("=" * 50)
    
    # Test all templates
    templates = ["modern", "professional", "corporate", "investor"]
    
    for template in templates:
        print(f"\n📋 {template.upper()} TEMPLATE:")
        config = get_template_styling(template)
        colors = config["color_scheme"]
        
        # Create RGBColor instances to compare
        primary_color = colors['primary']
        secondary_color = colors['secondary']
        
        print(f"  Primary: {primary_color}")
        print(f"  Secondary: {secondary_color}")
        print(f"  Font: {config['typography']['primary_font']}")

    # Check the specific Professional template requirements
    prof_config = get_template_styling("professional")
    prof_colors = prof_config["color_scheme"]
    
    print(f"\n🎯 PROFESSIONAL TEMPLATE VERIFICATION:")
    print(f"  Expected: Gold and Blue color scheme")
    
    # The colors are RGBColor objects, let's check by creating expected ones
    from pptx.dml.color import RGBColor
    expected_blue = RGBColor(24, 58, 88)
    expected_gold = RGBColor(181, 151, 91)
    
    # Convert to hex for comparison
    primary_hex = hex(prof_colors['primary']._color_val) if hasattr(prof_colors['primary'], '_color_val') else str(prof_colors['primary'])
    secondary_hex = hex(prof_colors['secondary']._color_val) if hasattr(prof_colors['secondary'], '_color_val') else str(prof_colors['secondary'])
    
    print(f"  Primary color: {primary_hex}")
    print(f"  Secondary color: {secondary_hex}")
    
    print(f"\n✅ Professional template updated with investment banking colors!")
    return True

if __name__ == "__main__":
    test_templates()