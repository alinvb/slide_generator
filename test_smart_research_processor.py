#!/usr/bin/env python3
"""
Test the smart research processor that extracts entity info from research
"""

def test_extraction_logic():
    """Test the JSON extraction logic"""
    
    # Mock research text about Netflix
    research_text = """
Company Overview & Founding — Netflix, Inc. is an American media and entertainment company founded in 1997 by Reed Hastings and Marc Randolph. It began as a DVD rental service and evolved into the world's leading subscription-based streaming platform, offering a broad catalog of TV shows, movies, documentaries, and original content.

Business Model & Reach — Netflix is a pioneer of streaming media, operating an over-the-top (OTT) subscription service. As of 2024, it serves approximately 169 million paid users globally, excluding Mainland China, Syria, North Korea, and Crimea.
"""

    # Test extraction prompt
    entity = "Netflix"
    extraction_prompt = f"""
Extract key business information about {entity} from this research text and format as structured data:

RESEARCH TEXT:
{research_text}

Extract and format as JSON:
{{
    "company_name": "{entity}",
    "business_description": "Brief description of what the company does",
    "founding_year": "Year founded (if mentioned)",
    "legal_structure": "Legal entity type (if mentioned)", 
    "core_operations": "Primary business operations",
    "target_markets": "Key markets and geography (if mentioned)"
}}

Only include fields that are clearly mentioned in the research. Return just the JSON, no other text.
"""

    print("🧪 Testing Smart Research Processor")
    print("=" * 50)
    print("\n📄 Research Text:")
    print(research_text[:200] + "...")
    
    print(f"\n🎯 Target Entity: {entity}")
    
    print(f"\n📝 Extraction Prompt:")
    print(extraction_prompt[:300] + "...")
    
    # Expected extraction result
    expected_fields = [
        "company_name",
        "business_description", 
        "founding_year",
        "core_operations"
    ]
    
    print(f"\n✅ Expected to extract: {', '.join(expected_fields)}")
    
    # Test context-aware question generation
    mock_extracted_data = {
        "company_name": "Netflix",
        "business_description": "American media and entertainment company that operates a subscription-based streaming platform",
        "founding_year": "1997",
        "core_operations": "Streaming media service with TV shows, movies, documentaries, and original content"
    }
    
    # Generate context-aware question
    context_question = f"Based on the research about Netflix's business (American media and entertainment company that operates a subscription-based streaming platform...), let's dive into the financial performance metrics. What are the key revenue streams and recent financial highlights?"
    
    print(f"\n🎯 Context-Aware Next Question:")
    print(context_question)
    
    print(f"\n🔥 This should PREVENT asking 'What is your company name?' after research!")

if __name__ == "__main__":
    test_extraction_logic()