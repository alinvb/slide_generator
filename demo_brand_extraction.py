#!/usr/bin/env python3
"""
Demo script showing how to use the brand color extraction functionality
"""
import sys
import os
from pathlib import Path

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from brand_extractor import BrandExtractor

def demo_brand_extraction():
    """Demonstrate brand extraction with both rule-based and LLM methods"""
    print("🎨 Brand Color Extraction Demo\n")
    print("=" * 60)
    
    # Initialize extractor
    extractor = BrandExtractor()
    
    # Test file (use one that exists)
    test_file = "test_brand_deck.pptx"
    
    if not Path(test_file).exists():
        print(f"❌ Test file {test_file} not found!")
        return
    
    print(f"📁 Using test file: {test_file}\n")
    
    # 1. Rule-based extraction (no API key needed)
    print("🔧 1. RULE-BASED EXTRACTION")
    print("-" * 30)
    
    brand_config = extractor.extract_brand_from_pptx(test_file, use_llm=False)
    
    if brand_config:
        print("✅ Successfully extracted brand configuration!")
        
        # Show color scheme
        print("\n🎨 Color Scheme:")
        colors = brand_config['color_scheme']
        for color_name, color_obj in colors.items():
            if hasattr(color_obj, 'r') and hasattr(color_obj, 'g') and hasattr(color_obj, 'b'):
                hex_color = f"#{color_obj.r:02x}{color_obj.g:02x}{color_obj.b:02x}"
                print(f"  • {color_name:<12}: {hex_color} (RGB: {color_obj.r}, {color_obj.g}, {color_obj.b})")
            else:
                print(f"  • {color_name:<12}: {color_obj} (type: {type(color_obj).__name__})")
        
        # Show typography
        print("\n📝 Typography:")
        typography = brand_config['typography']
        print(f"  • Primary Font: {typography.get('primary_font', 'N/A')}")
        print(f"  • Title Size:   {typography.get('title_size', 'N/A')}pt")
        print(f"  • Body Size:    {typography.get('body_size', 'N/A')}pt")
        
        # Show layout config
        print("\n📐 Layout Configuration:")
        layout = brand_config['layout_config']
        print(f"  • Title Alignment: {layout.get('title_alignment', 'N/A')}")
        print(f"  • Header Type:     {layout.get('header_type', 'N/A')}")
        
    else:
        print("❌ Failed to extract brand configuration")
    
    print("\n" + "=" * 60)
    
    # 2. LLM-based extraction (requires API key)
    print("\n🤖 2. LLM-BASED EXTRACTION")
    print("-" * 30)
    print("NOTE: LLM extraction requires an API key and model configuration.")
    print("Example usage:")
    print()
    print("  # With Perplexity API")
    print("  brand_config = extractor.extract_brand_from_pptx(")
    print("      'your_file.pptx',")
    print("      use_llm=True,")
    print("      api_key='your-perplexity-api-key',")
    print("      model_name='llama-3.1-sonar-large-128k-online',")
    print("      api_service='perplexity'")
    print("  )")
    print()
    print("  # With Claude API")
    print("  brand_config = extractor.extract_brand_from_pptx(")
    print("      'your_file.pptx',")
    print("      use_llm=True,")
    print("      api_key='your-claude-api-key',")
    print("      model_name='claude-3-sonnet-20240229',")
    print("      api_service='claude'")
    print("  )")
    
    print("\n🎯 Key Benefits:")
    print("  • Rule-based: Fast, no API needed, works offline")
    print("  • LLM-based: More accurate, understands context and design patterns")
    
    print("\n💡 Integration Example:")
    print("  The brand extraction is already integrated into the main app.py")
    print("  Users can upload PowerPoint files and choose extraction method")
    print("  Extracted colors are then used for slide generation")

if __name__ == "__main__":
    demo_brand_extraction()