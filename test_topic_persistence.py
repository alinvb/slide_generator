#!/usr/bin/env python3

"""
Test if the system properly stays within a topic until user says "next topic"
This is critical for the investment banking interview flow
"""

import sys
sys.path.append('/home/user/webapp')
from app import analyze_conversation_progress

def test_topic_persistence():
    """Test that system stays in topic with multiple follow-ups until 'next topic'"""
    
    print("🎯 TESTING TOPIC PERSISTENCE")
    print("=" * 50)
    print("REQUIREMENT: System should stay in current topic until user says 'next topic'")
    print("BEHAVIOR: All follow-up questions should be contextual to current topic")
    print()
    
    # Scenario: User has extended conversation about Topic 2 (product/service footprint)
    messages = [
        # Topic 1: Business Overview (completed quickly)
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        {
            "role": "user", 
            "content": "Nvidia - AI chip manufacturer"
        },
        
        # Topic 2: Product/Service Footprint (should stay here for multiple exchanges)
        {
            "role": "assistant",
            "content": "Now let's discuss your product/service footprint. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage?"
        },
        {
            "role": "user",
            "content": "We make GPUs for gaming, data centers, and AI workloads"
        },
        
        # Follow-up question 1 (should stay in Topic 2)
        {
            "role": "assistant",
            "content": "Can you provide more details about your data center products? What are the key models and their specifications?"
        },
        {
            "role": "user",
            "content": "H100, A100, and V100 series for enterprise AI training"
        },
        
        # Follow-up question 2 (should stay in Topic 2) 
        {
            "role": "assistant",
            "content": "What about geographic coverage? Which markets do you serve and what's your global footprint?"
        },
        {
            "role": "user",
            "content": "Global operations - US, Europe, Asia-Pacific, with manufacturing in Taiwan"
        },
        
        # Follow-up question 3 (should stay in Topic 2)
        {
            "role": "assistant", 
            "content": "How do you segment your product lines by customer type? Enterprise vs consumer?"
        },
        {
            "role": "user",
            "content": "Gaming GPUs for consumers, enterprise AI chips for hyperscalers, automotive chips for Tesla etc"
        },
        
        # User decides to move on (should complete Topic 2 and advance to Topic 3)
        {
            "role": "user",
            "content": "next topic"
        }
    ]
    
    print("📝 Testing extended conversation in Topic 2...")
    result = analyze_conversation_progress(messages)
    
    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"   Topics completed: {result['topics_completed']}")
    print(f"   Current topic: {result['current_topic']}")
    print(f"   Current position: {result['current_position']}")
    
    # Expected behavior:
    # - Topic 1 completed (business overview)  
    # - Topic 2 completed (after all the follow-ups and "next topic")
    # - Should now be at Topic 3 (historical_financial_performance)
    
    if result['topics_completed'] == 2 and result['current_topic'] == 'historical_financial_performance':
        print(f"\n✅ SUCCESS: Topic persistence working correctly!")
        print(f"   ✓ System stayed in Topic 2 throughout multiple follow-ups")
        print(f"   ✓ Only advanced to Topic 3 when user said 'next topic'") 
        print(f"   ✓ Follow-up questions didn't prematurely advance topics")
        return True
    else:
        print(f"\n❌ ISSUE: Topic persistence not working correctly")
        print(f"   Expected: 2 completed, at 'historical_financial_performance'")
        print(f"   Actual: {result['topics_completed']} completed, at '{result['current_topic']}'")
        return False

def test_research_within_topic():
    """Test multiple research requests within same topic"""
    
    print("\n🧪 TESTING MULTIPLE RESEARCH WITHIN TOPIC")
    print("=" * 40)
    
    messages = [
        # Topic 1: Business Overview  
        {
            "role": "assistant",
            "content": "What is your company name and give me a brief overview of what your business does?"
        },
        {
            "role": "user", 
            "content": "Tesla"
        },
        
        # Topic 2: Product/Service Footprint
        {
            "role": "assistant",
            "content": "Now let's discuss your product/service footprint. What are your main offerings?"
        },
        {
            "role": "user",
            "content": "research this for me"
        },
        {
            "role": "assistant",
            "content": "Tesla produces electric vehicles including Model S, Model 3, Model X, and Model Y. They also manufacture energy storage systems and solar panels. [200+ chars research content]"
        },
        {
            "role": "user",
            "content": "tell me more about their energy business"  # Still in Topic 2
        },
        {
            "role": "assistant", 
            "content": "Tesla's energy business includes Powerwall home batteries, Powerpack commercial storage, and Solar Roof tiles. [200+ chars research content]"
        },
        {
            "role": "user",
            "content": "research their geographic expansion"  # Still in Topic 2  
        },
        {
            "role": "assistant",
            "content": "Tesla operates globally with Gigafactories in Nevada, Shanghai, Berlin, and Texas. They sell in North America, Europe, China, and expanding to other markets. [200+ chars research]"
        },
        {
            "role": "user",
            "content": "sufficient. next topic"  # NOW should advance
        }
    ]
    
    result = analyze_conversation_progress(messages)
    
    print(f"📊 RESULTS:")
    print(f"   Topics completed: {result['topics_completed']}")
    print(f"   Current topic: {result['current_topic']}")
    
    if result['topics_completed'] == 2 and result['current_topic'] == 'historical_financial_performance':
        print("✅ SUCCESS: Multiple research requests within topic handled correctly")
        return True
    else:
        print("❌ ISSUE: Multiple research requests causing premature topic advancement")
        return False

def main():
    """Run all topic persistence tests"""
    
    test1 = test_topic_persistence()
    test2 = test_research_within_topic()
    
    print(f"\n🎯 OVERALL ASSESSMENT:")
    if test1 and test2:
        print("✅ TOPIC PERSISTENCE IS WORKING CORRECTLY!")
        print("   ✓ System stays in topic until user says 'next topic'")
        print("   ✓ Follow-up questions are contextual and don't advance topics")
        print("   ✓ Multiple research requests within topic work properly")
    else:
        print("❌ TOPIC PERSISTENCE NEEDS FIXES")
        print("   The system may be advancing topics too early")
        print("   Need to ensure follow-ups don't trigger topic completion")
    
    return test1 and test2

if __name__ == "__main__":
    main()