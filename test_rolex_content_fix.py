#!/usr/bin/env python3
"""
Test to verify Rolex content is no longer contaminated with tech/AI infrastructure content
"""

from bulletproof_json_generator_clean import generate_clean_bulletproof_json
import json

def test_rolex_content_purity():
    """Test that Rolex content doesn't contain tech/AI infrastructure contamination"""
    
    # Mock messages about Rolex
    test_messages = [
        {"role": "user", "content": "Let's analyze Rolex"},
        {"role": "assistant", "content": "I'd be happy to help with Rolex analysis"},
        {"role": "user", "content": "Rolex is a Swiss luxury watch manufacturer founded in 1905. They make premium timepieces and are known for quality, precision, and luxury positioning."},
        {"role": "assistant", "content": "Great! Tell me more about Rolex's business operations and market position."},
        {"role": "user", "content": "Rolex generates billions in revenue from luxury watch sales globally. They have manufacturing in Switzerland and strong brand recognition in luxury markets."}
    ]
    
    # Mock LLM API call function
    def mock_llm_call(messages):
        return """
        {
            "company_name": "Rolex",
            "business_description_detailed": "Swiss luxury watchmaker known for precision timepieces",
            "industry": "Luxury Watches", 
            "headquarters_location": "Geneva, Switzerland",
            "annual_revenue_usd_m": [6000, 6500, 7000, 7500, 8000]
        }
        """
    
    required_slides = ["business_overview", "strategic_buyers", "competitive_positioning"]
    
    print("🧪 Testing Rolex Content Purity...")
    print("📝 Company: Rolex (Swiss luxury watches)")
    print("🚫 Should NOT contain: AI, infrastructure, enterprise software, cloud, technology")
    print("✅ Should contain: Rolex, luxury, watches, Swiss, precision")
    
    # Contamination keywords to check for
    contamination_keywords = [
        "enterprise software", "AI", "artificial intelligence", "cloud", "infrastructure",
        "SaaS", "technology", "Microsoft", "Azure", "Vista Equity", "enterprise",
        "software", "algorithms", "tech", "TechCorp", "innovation leader"
    ]
    
    # Expected Rolex-relevant keywords
    rolex_keywords = [
        "Rolex", "luxury", "watch", "timepiece", "Swiss", "precision", "quality"
    ]
    
    try:
        # Call the fixed generator
        response, content_ir, render_plan = generate_clean_bulletproof_json(
            test_messages,
            required_slides, 
            mock_llm_call,
            company_name="Rolex"
        )
        
        print(f"\n✅ Generation completed successfully!")
        
        # Check for contamination (use word boundaries to avoid false positives like "details" containing "ai")
        import re
        contamination_found = []
        for keyword in contamination_keywords:
            # Use word boundaries for precise matching
            if keyword.upper() == "AI":
                # Special case for AI - must be standalone word
                if re.search(r'\bAI\b', response, re.IGNORECASE):
                    contamination_found.append(keyword)
            else:
                # For other keywords, use simple case-insensitive search
                if keyword.lower() in response.lower():
                    contamination_found.append(keyword)
        
        # Check for Rolex-relevant content
        rolex_content_found = []
        for keyword in rolex_keywords:
            if keyword.lower() in response.lower():
                rolex_content_found.append(keyword)
        
        print(f"\n📊 CONTAMINATION CHECK:")
        if contamination_found:
            print(f"❌ CONTAMINATION DETECTED: {contamination_found}")
            print("Examples from response:")
            lines_with_contamination = [line.strip() for line in response.split('\n') 
                                       if any(kw.lower() in line.lower() for kw in contamination_found)]
            for line in lines_with_contamination[:3]:
                print(f"  - {line}")
            return False
        else:
            print(f"✅ NO CONTAMINATION: No tech/AI content found")
        
        print(f"\n📈 ROLEX CONTENT CHECK:")
        if rolex_content_found:
            print(f"✅ ROLEX CONTENT FOUND: {rolex_content_found}")
            lines_with_rolex = [line.strip() for line in response.split('\n') 
                               if any(kw.lower() in line.lower() for kw in rolex_content_found)]
            for line in lines_with_rolex[:3]:
                print(f"  - {line}")
        else:
            print(f"⚠️ LIMITED ROLEX CONTENT: May need more specific content")
        
        # Print sample of the content to verify
        print(f"\n📄 SAMPLE CONTENT (first 800 chars):")
        print(response[:800])
        
        return len(contamination_found) == 0
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Rolex Content Purity Test")
    print("=" * 60)
    
    success = test_rolex_content_purity()
    
    if success:
        print("\n🎉 SUCCESS: Rolex content is clean!")
        print("✅ No more AI/tech contamination in luxury watch company slides")
    else:
        print("\n❌ FAILURE: Still contains tech contamination")
        print("🔧 Additional hardcoded content needs to be eliminated")