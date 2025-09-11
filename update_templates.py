#!/usr/bin/env python3
"""Script to update slide template functions to support template_name parameter"""

import re

def update_slide_templates():
    # Read the file
    with open('slide_templates.py', 'r') as f:
        content = f.read()
    
    # Pattern to find render functions
    render_func_pattern = r'def (render_\w+_slide)\([^)]*brand_config=None([^)]*)\):'
    
    # Replace function signatures to add template_name parameter
    def replace_signature(match):
        func_name = match.group(1)
        remaining_params = match.group(2)
        # Add template_name parameter
        return f'def {func_name}({match.group(0)[4:-2]}, template_name="modern"{remaining_params}):'
    
    # Update function signatures
    content = re.sub(render_func_pattern, replace_signature, content)
    
    # Update get_brand_styling calls to include template_name
    content = re.sub(
        r'colors, fonts = get_brand_styling\(brand_config, color_scheme, typography\)',
        r'colors, fonts = get_brand_styling(brand_config, color_scheme, typography, template_name)',
        content
    )
    
    # Also update calls that only have brand_config
    content = re.sub(
        r'colors, fonts = get_brand_styling\(brand_config\)',
        r'colors, fonts = get_brand_styling(brand_config, template_name=template_name)',
        content
    )
    
    # Write back
    with open('slide_templates.py', 'w') as f:
        f.write(content)
    
    print("✅ Updated slide template functions")

if __name__ == "__main__":
    update_slide_templates()