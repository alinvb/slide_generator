#!/usr/bin/env python3
"""
Test to verify company name propagation fix
"""

from bulletproof_json_generator_clean import generate_clean_bulletproof_json

def test_company_name_propagation():
    """Test that company name gets correctly propagated through the system"""
    
    # Mock messages about Rolex
    test_messages = [
        {"role": "user", "content": "Let's discuss Rolex"},
        {"role": "assistant", "content": "I'd be happy to help with Rolex analysis"},
        {"role": "user", "content": "Rolex is a luxury watch manufacturer based in Switzerland. They make high-end watches and have strong brand recognition globally."},
        {"role": "assistant", "content": "Great! Tell me more about Rolex's business model and financials."},
        {"role": "user", "content": "Rolex generates about $8 billion in revenue annually and has been growing steadily. They focus on luxury timepieces."}
    ]
    
    # Mock LLM API call function
    def mock_llm_call(messages):
        return """
        {
            "company_name": "Rolex",
            "business_description_detailed": "Swiss luxury watchmaker and manufacturer",
            "industry": "Luxury Goods",
            "annual_revenue_usd_m": [7000, 7500, 8000, 8200, 8500]
        }
        """
    
    required_slides = ["business_overview", "competitive_positioning"]
    
    print("🧪 Testing Company Name Propagation Fix...")
    print("📝 Company: Rolex")
    print("📊 Expected: All slides should reference 'Rolex', not 'TechCorp Solutions'")
    
    try:
        # Call the fixed generator with company name
        response, content_ir, render_plan = generate_clean_bulletproof_json(
            test_messages,
            required_slides, 
            mock_llm_call,
            company_name="Rolex"  # This should prevent TechCorp fallback
        )
        
        print(f"\n✅ Generation completed successfully!")
        
        # Check if the response contains Rolex instead of TechCorp
        if "TechCorp" in response:
            print(f"❌ STILL BROKEN: Response contains 'TechCorp'")
            print("TechCorp occurrences:")
            lines_with_techcorp = [line.strip() for line in response.split('\n') if 'TechCorp' in line]
            for line in lines_with_techcorp[:5]:  # Show first 5 occurrences
                print(f"  - {line}")
            return False
        elif "Rolex" in response:
            print(f"✅ FIXED: Response contains 'Rolex' correctly!")
            lines_with_rolex = [line.strip() for line in response.split('\n') if 'Rolex' in line]
            print("Rolex references found:")
            for line in lines_with_rolex[:5]:  # Show first 5 occurrences
                print(f"  - {line}")
            return True
        else:
            print(f"⚠️ UNCLEAR: Response doesn't contain 'TechCorp' or 'Rolex'")
            print("First 500 characters of response:")
            print(response[:500])
            return False
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔍 Company Name Propagation Test")
    print("=" * 50)
    
    success = test_company_name_propagation()
    
    if success:
        print("\n🎉 SUCCESS: Company name propagation is working!")
        print("✅ The app should now use 'Rolex' instead of 'TechCorp Solutions'")
    else:
        print("\n❌ FAILURE: Company name propagation still has issues")
        print("🔧 Additional fixes may be needed")