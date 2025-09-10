#!/usr/bin/env python3
"""
Test the new question-based topic detection
"""
import sys
import os
sys.path.append('/home/user/webapp')

from topic_based_slide_generator import TopicBasedSlideGenerator

# Sample Netflix conversation messages
netflix_messages = [
    {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
    {"role": "user", "content": "Netflix"},
    {"role": "assistant", "content": "Netflix research info..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Now let's discuss your product/service footprint. What are your main offerings?"},
    {"role": "user", "content": "research this yourself"},
    {"role": "assistant", "content": "Netflix product research..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins..."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Financial performance research..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Now I need information about your management team. Can you provide names, titles, and brief backgrounds for 4-6 key executives including CEO, CFO, and other senior leaders?"},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Management team research..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Let's discuss your growth strategy and projections. What are your expansion plans, strategic initiatives, and financial projections for the next 3-5 years?"},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Growth strategy research..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "How is your company positioned competitively? I need information about key competitors, your competitive advantages, market positioning, and differentiation factors."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Competitive research..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Now let's examine precedent transactions. Focus ONLY on private market M&A transactions where one company acquired another company. I need recent corporate acquisitions in your industry."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Precedent transactions research..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "What valuation methodologies would be most appropriate for your business? I recommend DCF, Trading Multiples, and Precedent Transactions analysis."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Valuation methodologies research..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Based on your valuation range, let's identify strategic buyers who can afford this acquisition and would value your strategic assets."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Strategic buyers research..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Now let's identify private equity firms that can afford your valuation and have experience with companies in your sector."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "PE firms research..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Finally, let's identify large conglomerates that operate in your geographic region and could afford your valuation."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Conglomerates research..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Let's discuss margin and cost data. Can you provide your EBITDA margins for the last 2-3 years, key cost management initiatives, and main risk mitigation strategies?"},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Margin and cost research..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Now let's discuss investor considerations. What are the key RISKS and OPPORTUNITIES investors should know about your business?"},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Investor considerations research..."},
    {"role": "user", "content": "ok"},
    
    {"role": "assistant", "content": "Finally, what would the investment/acquisition process look like? I need diligence topics, synergy opportunities, risk factors and expected timeline."},
    {"role": "user", "content": "research this for me"},
    {"role": "assistant", "content": "Investment process research..."},
    {"role": "user", "content": "ok"}
]

def test_question_based_detection():
    """Test the new question-based detection logic"""
    print("🧪 TESTING QUESTION-BASED TOPIC DETECTION")
    print("=" * 60)
    
    generator = TopicBasedSlideGenerator()
    covered_topics, progress_info = generator.get_covered_topics_from_progress(netflix_messages)
    
    print(f"\n🎯 RESULTS:")
    print(f"📊 Topics detected: {len(covered_topics)}/14")
    print(f"📋 Coverage: {progress_info['completion_percentage']:.1%}")
    print(f"🔧 Method: {progress_info['method']}")
    print(f"\n📝 Covered topics:")
    for i, topic in enumerate(covered_topics, 1):
        print(f"  {i:>2}. {topic}")
    
    return covered_topics, progress_info

if __name__ == "__main__":
    covered_topics, progress_info = test_question_based_detection()
    print(f"\n🚀 Expected slides: {len(covered_topics)} (much better than 3!)")