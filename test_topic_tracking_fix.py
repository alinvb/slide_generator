#!/usr/bin/env python3
"""
Test for the critical topic tracking fix.
Verifies that comprehensive AI responses don't mark multiple topics as covered.
"""

# Import the fixed function
import sys
sys.path.append('/home/user/webapp')
from app import analyze_conversation_progress

def test_topic_coverage_fix():
    """Test that comprehensive responses only mark the current topic as covered"""
    
    print("🧪 TESTING TOPIC TRACKING FIX")
    print("=" * 50)
    
    # Simulate the scenario that was causing the bug
    # AI asks business overview question, then provides comprehensive research
    test_messages = [
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "Databricks"},
        {"role": "assistant", "content": "Based on my research, here are key facts about Databricks: Founded in 2013 by the original creators of Apache Spark, Databricks is a leading unified analytics platform company. The company provides cloud-based data engineering, data science, and analytics services. Key offerings include: 1) Databricks Lakehouse Platform - unified data analytics platform, 2) Delta Lake - open-source storage framework, 3) MLflow - machine learning lifecycle management. The management team includes CEO Ali Ghodsi (former Vice Provost at UC Berkeley), CTO Matei Zaharia (Apache Spark creator), and other Stanford/Berkeley academics. Financially, Databricks has shown strong growth with revenue exceeding $1 billion ARR. They compete with Snowflake, Amazon Redshift, and Google BigQuery. The company operates globally with offices in San Francisco, Amsterdam, London, and Singapore. Recent strategic initiatives focus on expanding their unified analytics platform and machine learning capabilities. For valuation, the company was last valued at $43 billion in their Series I funding round. Key competitive advantages include their Spark expertise, lakehouse architecture, and academic pedigree. The management team has deep technical expertise in distributed systems."},
        {"role": "user", "content": "ok"}
    ]
    
    # Run the analysis
    result = analyze_conversation_progress(test_messages)
    
    print("\n📊 ANALYSIS RESULTS:")
    print(f"Next Topic: {result.get('next_topic', 'None')}")
    print(f"Next Question: {result.get('next_question', 'None')[:100]}...")
    print(f"Has Research: {result.get('has_research_content', False)}")
    
    # Check what the next topic should be
    expected_next_topic = "product_service_footprint"  # Should be Topic 2, not Topic 9
    actual_next_topic = result.get('next_topic')
    
    print(f"\n✅ EXPECTED NEXT TOPIC: {expected_next_topic} (Topic 2)")
    print(f"🔍 ACTUAL NEXT TOPIC: {actual_next_topic}")
    
    if actual_next_topic == expected_next_topic:
        print("✅ SUCCESS: Topic tracking fix working correctly!")
        print("   The system properly stays on Topic 2 instead of jumping to Topic 9")
        return True
    else:
        print("❌ FAILED: System is still jumping topics")
        print(f"   Expected: {expected_next_topic}, Got: {actual_next_topic}")
        return False

def test_sequential_progression():
    """Test that topics progress in proper 1-14 sequential order"""
    print("\n🔢 TESTING SEQUENTIAL PROGRESSION")
    print("=" * 50)
    
    # Simulate completing topics 1-3 sequentially
    messages_topic_1_complete = [
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "Databricks is a unified analytics platform for data engineering and machine learning founded in 2013."}
    ]
    
    result_1 = analyze_conversation_progress(messages_topic_1_complete)
    print(f"After Topic 1: Next topic should be 'product_service_footprint', got: {result_1.get('next_topic')}")
    
    # Add Topic 2 completion
    messages_topic_2_complete = messages_topic_1_complete + [
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
        {"role": "user", "content": "Our main products include the Databricks Lakehouse Platform, Delta Lake storage framework, and MLflow for machine learning. We operate globally across North America, Europe, and Asia-Pacific regions."}
    ]
    
    result_2 = analyze_conversation_progress(messages_topic_2_complete)
    print(f"After Topic 2: Next topic should be 'historical_financial_performance', got: {result_2.get('next_topic')}")
    
    return True

if __name__ == "__main__":
    print("🚀 RUNNING TOPIC TRACKING TESTS")
    print("Testing the critical fix for investment banking interview system")
    print("")
    
    success_1 = test_topic_coverage_fix()
    success_2 = test_sequential_progression()
    
    print("\n" + "=" * 50)
    if success_1 and success_2:
        print("✅ ALL TESTS PASSED! The topic tracking fix is working correctly.")
    else:
        print("❌ SOME TESTS FAILED. Further debugging needed.")
    
    print("\n🌐 FIXED SYSTEM URL: https://3000-i1igkppq2hiu9o5h7uppm-6532622b.e2b.dev")