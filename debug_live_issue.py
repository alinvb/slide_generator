#!/usr/bin/env python3
"""
Debug the live issue where the system is stuck asking the business overview question
"""

import sys
sys.path.append('/home/user/webapp')
from app import analyze_conversation_progress

def test_exact_scenario():
    """Test the exact scenario from the user report"""
    
    print("🔍 DEBUGGING EXACT USER SCENARIO")
    print("=" * 60)
    
    # Exact messages from the user report
    messages = [
        {"role": "assistant", "content": "Let's start: What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "databricks"},
        {"role": "assistant", "content": "Databricks is a San Francisco-based software company specializing in cloud-based data analytics and AI platforms, best known for pioneering the \"lakehouse\" architecture that unifies data warehousing and AI workloads. The company enables enterprises to process, analyze, and manage large-scale data using open-source technologies like Apache Spark, Delta Lake, and MLflow, and has become a leader in the data intelligence platform space. Business Model & Offerings: Databricks provides a unified analytics platform that allows organizations to build, deploy, and maintain enterprise-grade data, analytics, and AI solutions at scale. Its platform integrates with major cloud providers, automates infrastructure management, and leverages generative AI for advanced analytics and natural language data discovery. Core technologies include Delta Lake for data reliability, MLflow for machine learning lifecycle management, and Unity Catalog for governance. Market Position & Financials: As of September 2025, Databricks has reached a $100 billion valuation with $4 billion in annual recurring revenue (ARR), reflecting rapid growth and strong enterprise adoption. The company's customer base spans industries such as healthcare, financial services, retail, and manufacturing, with many Fortune 500 clients. Are you satisfied with this information, or would you like me to research something more specific about Databricks?"},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage?"},
        {"role": "user", "content": "research this yourself"},
        {"role": "assistant", "content": "Databricks provides a unified Data Intelligence Platform built on its proprietary \"Lakehouse\" architecture, combining data engineering, analytics, machine learning, and generative AI features for enterprises in 2025. Its platform is designed to solve the full spectrum of data management, AI, and business intelligence needs, and operates globally across AWS, Azure, and Google Cloud. Main Offerings (Products & Services): Delta Lake, Unity Catalog, MLflow, Spark Engine, Photon Engine, Delta Live Tables, Databricks SQL, AI/BI, Databricks Jobs, Databricks AI, Agent Bricks, Lakebase. Geographic Coverage & Market Reach: Cloud-agnostic: Databricks runs seamlessly on AWS, Azure, and Google Cloud—allowing global deployment and multi-cloud strategies for large enterprises. Are you satisfied with this information, or would you like more specific research on Databricks' market coverage, customer base, or technology stack?"},
        {"role": "user", "content": "ok"}
    ]
    
    print("📝 ANALYZING CONVERSATION...")
    result = analyze_conversation_progress(messages)
    
    print(f"\n📊 ANALYSIS RESULTS:")
    print(f"Next Topic: {result.get('next_topic', 'None')}")
    print(f"Next Question Preview: {result.get('next_question', 'None')[:150]}...")
    
    # Check what should happen
    expected = "historical_financial_performance"  # Should be Topic 3 after completing Topics 1 and 2
    actual = result.get('next_topic')
    
    print(f"\n✅ EXPECTED: {expected} (Topic 3 - Financial Performance)")
    print(f"🔍 ACTUAL: {actual}")
    
    if actual == "business_overview":
        print("❌ BUG CONFIRMED: System is stuck on business overview question!")
        print("   This means Topic 1 is not being marked as completed properly")
        return False
    elif actual == expected:
        print("✅ SUCCESS: System correctly progressed to next topic")
        return True
    else:
        print(f"⚠️  UNEXPECTED: Got {actual}, expected {expected}")
        return False

def test_simple_business_completion():
    """Test if business overview gets marked as complete with simple response"""
    print("\n🧪 TESTING SIMPLE BUSINESS OVERVIEW COMPLETION")
    print("=" * 60)
    
    simple_messages = [
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "Databricks. We provide a unified analytics platform for data engineering and machine learning."}
    ]
    
    result = analyze_conversation_progress(simple_messages)
    
    print(f"Simple Response Result - Next Topic: {result.get('next_topic')}")
    
    if result.get('next_topic') == 'product_service_footprint':
        print("✅ Simple response works - progresses to Topic 2")
        return True
    else:
        print("❌ Simple response also fails")
        return False

if __name__ == "__main__":
    print("🚨 DEBUGGING LIVE ISSUE: System stuck asking business overview")
    print("User Report: System keeps asking 'What is your company name...' in a loop")
    print("")
    
    success_1 = test_exact_scenario()
    success_2 = test_simple_business_completion()
    
    print("\n" + "=" * 60)
    if not success_1 and not success_2:
        print("❌ CRITICAL: The fix is not working. Topics are not being marked complete.")
        print("   Need to investigate the topic completion logic further.")
    elif success_2 and not success_1:
        print("⚠️  PARTIAL: Simple responses work but complex responses don't.")
        print("   The issue might be with how comprehensive AI responses are handled.")
    else:
        print("✅ Fix appears to be working in tests.")
        print("   The live issue might be a different problem (caching, session state, etc.)")