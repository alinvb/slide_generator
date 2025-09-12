#!/usr/bin/env python3
"""
Test script to verify template switching is working correctly
"""

from pptx.dml.color import RGBColor
from slide_templates import get_brand_styling, get_template_styling, render_management_team_slide
from pptx import Presentation

def test_template_switching():
    """Test if different templates apply different styling"""
    
    print("🧪 Testing template switching...")
    
    templates = ["modern", "professional", "corporate", "investor"]
    
    for template_name in templates:
        print(f"\n🧪 Testing template: {template_name}")
        
        # Test 1: Test get_template_styling function
        template_config = get_template_styling(template_name)
        primary_color = template_config['color_scheme']['primary']
        primary_font = template_config['typography']['primary_font']
        
        if isinstance(primary_color, RGBColor):
            hex_str = str(primary_color)
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16) 
            b = int(hex_str[4:6], 16)
            print(f"  Template config - Color: RGB({r},{g},{b}), Font: {primary_font}")
        
        # Test 2: Test get_brand_styling with no brand config (should use template)
        colors, fonts = get_brand_styling(brand_config=None, template_name=template_name)
        styling_primary = colors.get('primary')
        styling_font = fonts.get('primary_font')
        
        if isinstance(styling_primary, RGBColor):
            hex_str = str(styling_primary)
            r = int(hex_str[0:2], 16)
            g = int(hex_str[2:4], 16) 
            b = int(hex_str[4:6], 16)
            print(f"  Brand styling - Color: RGB({r},{g},{b}), Font: {styling_font}")
        
        # Test 3: Render a slide with this template
        test_data = {
            'title': f'{template_name.title()} Template Test',
            'left_column_profiles': [
                {'name': f'Test {template_name.title()} CEO', 'role': 'Chief Executive Officer', 'experience': ['10+ years experience']}
            ],
            'right_column_profiles': []
        }
        
        prs = Presentation()
        
        # Render slide with template
        result_prs = render_management_team_slide(
            data=test_data,
            prs=prs,
            brand_config=None,  # No brand config to test pure template styling
            template_name=template_name,
            company_name="Template Test Company"
        )
        
        if result_prs and hasattr(result_prs, 'slides') and len(result_prs.slides) > 0:
            # Save test presentation to check visually
            test_output = f"/home/user/webapp/test_template_{template_name}.pptx"
            result_prs.save(test_output)
            print(f"  ✅ {template_name.title()} template saved to: {test_output}")
        else:
            print(f"  ❌ {template_name.title()} template rendering failed!")
    
    print("\n🧪 Template switching test completed!")
    
    # Expected colors for verification
    expected_colors = {
        "modern": (24, 58, 88),      # Current blue
        "professional": (30, 58, 138),  # Deep blue  
        "corporate": (88, 28, 135),     # Deep purple
        "investor": (56, 189, 248)      # Medium blue
    }
    
    print("\n🧪 Expected colors:")
    for template, (r, g, b) in expected_colors.items():
        print(f"  {template}: RGB({r},{g},{b})")

if __name__ == "__main__":
    test_template_switching()