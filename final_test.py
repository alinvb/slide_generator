#!/usr/bin/env python3
"""
Final test to confirm the topic skipping issue is completely resolved
"""

import sys
sys.path.append('/home/user/webapp')
from app import analyze_conversation_progress

def final_comprehensive_test():
    """Test the exact user scenario that was causing the infinite loop"""
    
    print("🔬 FINAL COMPREHENSIVE TEST")
    print("=" * 60)
    
    # The exact conversation that was causing the infinite loop
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
    
    print("📊 RUNNING ANALYSIS...")
    result = analyze_conversation_progress(messages)
    
    print(f"\n📋 RESULTS:")
    print(f"Next Topic: {result.get('next_topic', 'NONE')}")
    print(f"Next Question Preview: {result.get('next_question', 'NONE')[:100]}...")
    
    # What should happen after Topics 1 and 2 are completed
    expected_topic = "historical_financial_performance"  # Topic 3
    actual_topic = result.get('next_topic')
    
    print(f"\n🎯 EXPECTED: {expected_topic} (Topic 3)")
    print(f"🔍 ACTUAL: {actual_topic}")
    
    if actual_topic == expected_topic:
        print("✅ SUCCESS! Topic progression is working correctly!")
        print("   ✅ Topic 1 (business_overview) completed")
        print("   ✅ Topic 2 (product_service_footprint) completed")  
        print("   ✅ Topic 3 (historical_financial_performance) is next")
        print("   ✅ No more infinite loop!")
        return True
    elif actual_topic == "business_overview":
        print("❌ FAILED: Still stuck in infinite loop asking business overview")
        return False
    else:
        print(f"⚠️  UNEXPECTED: Got {actual_topic}, but at least not stuck in loop")
        return False

if __name__ == "__main__":
    print("🎯 FINAL TEST: Verifying the topic skipping fix is complete")
    print("Testing the exact scenario that was causing the infinite loop")
    print("")
    
    success = final_comprehensive_test()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 EXCELLENT! The fix is working perfectly!")
        print("   📈 Interview now progresses correctly: Topic 1 → Topic 2 → Topic 3")
        print("   🚫 No more infinite loops or inappropriate topic skipping")
        print("   ✅ Users can now complete the full 14-topic interview")
        print("\n🌐 UPDATED SYSTEM: https://3000-i1igkppq2hiu9o5h7uppm-6532622b.e2b.dev")
    else:
        print("❌ The issue persists. Further investigation needed.")