#!/usr/bin/env python3
"""
Test the corrected JSON structure with our fixed slide templates
"""

import json
from pptx import Presentation
from pptx.util import Inches
import slide_templates

def test_corrected_json():
    """Test slide generation with corrected JSON structure"""
    print("🧪 Testing Corrected JSON Structure...")
    print("=" * 60)
    
    try:
        # Load the corrected JSON
        with open('corrected_user_json_render_plan.json', 'r') as f:
            render_plan = json.load(f)
        
        # Load the content IR
        with open('test_user_json_content_ir.json', 'r') as f:
            content_ir = json.load(f)
        
        print(f"📊 Render plan slides: {len(render_plan['slides'])}")
        
        # Create presentation
        prs = Presentation()
        prs.slide_width = Inches(13.333)
        prs.slide_height = Inches(7.5)
        
        successful_slides = 0
        failed_slides = []
        
        for i, slide_config in enumerate(render_plan['slides']):
            template = slide_config['template']
            data = slide_config.get('data', {})
            
            print(f"\n🎯 Generating slide {i+1}: {template}")
            
            try:
                # Get the appropriate render function
                render_function = getattr(slide_templates, f'render_{template}_slide', None)
                
                if render_function:
                    # Generate slide - use existing presentation
                    prs = render_function(
                        data=data,
                        prs=prs,
                        content_ir=content_ir,
                        company_name="LlamaIndex"  # Set proper company name
                    )
                    successful_slides += 1
                    print(f"✅ Slide {i+1} ({template}) generated successfully")
                else:
                    print(f"❌ Slide {i+1} ({template}) - No render function found")
                    failed_slides.append(template)
                    
            except Exception as e:
                print(f"❌ Slide {i+1} ({template}) failed: {e}")
                failed_slides.append(template)
                import traceback
                traceback.print_exc()
        
        # Save complete presentation
        output_file = 'corrected_json_test_output.pptx'
        prs.save(output_file)
        
        total_slides = len(render_plan['slides'])
        print(f"\n📊 Generation Summary:")
        print(f"✅ Successful slides: {successful_slides}/{total_slides}")
        print(f"❌ Failed slides: {len(failed_slides)}")
        if failed_slides:
            print(f"Failed templates: {failed_slides}")
        
        print(f"💾 Complete presentation saved: {output_file}")
        
        return successful_slides > 0 and len(failed_slides) == 0
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_corrected_json()
    print(f"\n🏆 Test Result: {'✅ SUCCESS' if success else '❌ FAILED'}")
    exit(0 if success else 1)