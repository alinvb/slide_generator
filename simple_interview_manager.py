#!/usr/bin/env python3
"""
Simplified Interview Manager - Clean Sequential Approach
"""

class SimpleInterviewManager:
    """
    Simple interview manager that tracks progress through 14 topics sequentially
    Uses satisfaction checks as gates between topics
    """
    
    def __init__(self):
        self.topics = [
            {
                "id": "business_overview",
                "position": 1,
                "question": "What is your company name and give me a brief overview of what your business does?",
                "satisfaction_prompt": "Are you satisfied with the business overview information provided, or would you like me to research any specific aspects further?"
            },
            {
                "id": "product_service_footprint", 
                "position": 2,
                "question": "Now let's discuss your product/service footprint. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage?",
                "satisfaction_prompt": "Are you satisfied with the product/service information, or would you like me to investigate any specific areas further?"
            },
            {
                "id": "historical_financial_performance",
                "position": 3, 
                "question": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years? I need specific numbers: annual revenue in USD millions, EBITDA figures, margin percentages, growth rates, and key performance drivers. What are the main revenue streams and how have they evolved?",
                "satisfaction_prompt": "Are you satisfied with the financial performance analysis, or would you like me to investigate any specific financial areas further?"
            },
            {
                "id": "management_team",
                "position": 4,
                "question": "Now I need information about your management team. Can you provide names, titles, and brief backgrounds for 4-6 key executives including CEO, CFO, and other senior leaders?",
                "satisfaction_prompt": "Are you satisfied with the management team information, or would you like me to research any specific executives further?"
            },
            {
                "id": "growth_strategy_projections",
                "position": 5,
                "question": "Let's discuss your growth strategy and projections. What are your expansion plans, strategic initiatives, and financial projections for the next 3-5 years?",
                "satisfaction_prompt": "Are you satisfied with the growth strategy information, or would you like me to investigate any specific growth areas further?"
            },
            {
                "id": "competitive_positioning",
                "position": 6,
                "question": "How is your company positioned competitively? I need information about key competitors, your competitive advantages, market positioning, and differentiation factors.",
                "satisfaction_prompt": "Are you satisfied with the competitive analysis, or would you like me to research any specific competitors further?"
            },
            {
                "id": "precedent_transactions",
                "position": 7,
                "question": "Now let's examine precedent transactions. Focus ONLY on private market M&A transactions where one company acquired another company. I need recent corporate acquisitions in your industry with target company, acquirer, transaction date, enterprise value, and multiples.",
                "satisfaction_prompt": "Are you satisfied with the precedent transactions analysis, or would you like me to research additional transactions?"
            },
            {
                "id": "valuation_overview",
                "position": 8,
                "question": "What valuation methodologies would be most appropriate for your business? Based on your financial performance and growth projections, I recommend: (1) DCF Analysis with your specific cash flow projections and discount rate, (2) Trading Multiples from comparable public companies in your sector, and (3) Precedent Transactions from recent M&A deals. What's your expected enterprise value range?",
                "satisfaction_prompt": "Are you satisfied with the valuation analysis, or would you like me to investigate any specific valuation aspects further?"
            },
            {
                "id": "strategic_buyers",
                "position": 9,
                "question": "Now let's identify potential strategic buyers based on your valuation and geography. I need 4-5 strategic buyers (corporations) who: (1) Can afford your valuation range, (2) Operate in your geographic markets or want to expand there, (3) Would benefit from strategic synergies with your business. Focus on companies in your industry or adjacent sectors.",
                "satisfaction_prompt": "Are you satisfied with the strategic buyers analysis, or would you like me to research additional potential acquirers?"
            },
            {
                "id": "financial_buyers",
                "position": 10,
                "question": "Let's identify PRIVATE EQUITY FIRMS only (NOT venture capital firms, as VCs don't buy companies). I need 4-5 PE firms that: (1) Have the financial capacity for your valuation range, (2) Have experience acquiring companies in your sector/size, (3) Operate in or invest in your geographic regions.",
                "satisfaction_prompt": "Are you satisfied with the private equity analysis, or would you like me to research additional PE firms?"
            },
            {
                "id": "sea_conglomerates",
                "position": 11,
                "question": "Let's identify large conglomerates that could afford your valuation and are relevant to your geographic markets. Based on where your company operates, I need 4-5 conglomerates that: (1) Have the financial capacity for acquisitions in your valuation range, (2) Either operate in your regions OR want to expand into your markets.",
                "satisfaction_prompt": "Are you satisfied with the conglomerates analysis, or would you like me to research additional potential buyers?"
            },
            {
                "id": "margin_cost_resilience", 
                "position": 12,
                "question": "Let's discuss margin and cost data. Can you provide your EBITDA margins for the last 2-3 years, key cost management initiatives, and main risk mitigation strategies for cost control?",
                "satisfaction_prompt": "Are you satisfied with the margin and cost analysis, or would you like me to investigate any specific cost areas further?"
            },
            {
                "id": "investor_considerations",
                "position": 13,
                "question": "Now let's discuss investor considerations. What are the key RISKS and OPPORTUNITIES investors should know about your business? What concerns might they have and how do you mitigate these risks?",
                "satisfaction_prompt": "Are you satisfied with the risk and opportunity analysis, or would you like me to investigate any specific investor concerns further?"
            },
            {
                "id": "investor_process_overview",
                "position": 14,
                "question": "Finally, what would the investment/acquisition process look like? I need diligence topics investors would focus on, key synergy opportunities, main risk factors and mitigation strategies, and expected timeline for the transaction process.",
                "satisfaction_prompt": "Are you satisfied with the process overview, or would you like me to investigate any specific aspects of the transaction process further?"
            }
        ]
    
    def analyze_simple_progress(self, messages):
        """
        Simple progress analysis - just track current position and satisfaction state
        """
        result = {
            "current_position": 1,
            "total_topics": 14,
            "current_topic": self.topics[0],
            "next_question": self.topics[0]["question"],
            "is_complete": False,
            "awaiting_satisfaction": False,
            "satisfaction_question": None
        }
        
        # SIMPLIFIED: Count topic completions by looking at conversation flow
        completed_topics = 0
        satisfaction_responses = ["yes", "ok", "okay", "correct", "satisfied", "good", "right", "sure", "proceed", "continue", "next", "go ahead"]
        
        # Method: Look for AI questions followed by user responses (direct or research+satisfaction)
        topic_questions_asked = 0
        topic_completions = 0
        
        i = 0
        while i < len(messages):
            msg = messages[i]
            
            # Look for AI asking a topic question
            if msg["role"] == "assistant" and ("?" in msg["content"] or "let's" in msg["content"].lower()):
                topic_questions_asked += 1
                
                # Case 1: User provides direct answer
                if i + 1 < len(messages) and messages[i + 1]["role"] == "user":
                    user_response = messages[i + 1]["content"].lower()
                    
                    # Case 1a: Direct informational response (not research request)
                    if "research" not in user_response and len(user_response) > 10:
                        topic_completions += 1
                        i += 2
                        continue
                    
                    # Case 1b: Research request
                    elif "research" in user_response:
                        # Look for AI research response + user satisfaction
                        if (i + 2 < len(messages) and messages[i + 2]["role"] == "assistant" and
                            i + 3 < len(messages) and messages[i + 3]["role"] == "user"):
                            satisfaction_response = messages[i + 3]["content"].lower().strip()
                            if any(resp in satisfaction_response for resp in satisfaction_responses):
                                topic_completions += 1
                                i += 4
                                continue
            i += 1
        
        completed_topics = topic_completions
        
        # Current position = completed topics + 1 (next topic to ask)
        result["current_position"] = min(completed_topics + 1, 14)
        
        if result["current_position"] <= 14:
            result["current_topic"] = self.topics[result["current_position"] - 1]
            result["next_question"] = result["current_topic"]["question"]
        
        # Check if we're awaiting satisfaction confirmation
        if len(messages) >= 2:
            last_ai = None
            last_user = None
            
            # Find last AI and user messages
            for msg in reversed(messages):
                if msg["role"] == "assistant" and last_ai is None:
                    last_ai = msg
                elif msg["role"] == "user" and last_user is None:
                    last_user = msg
                if last_ai and last_user:
                    break
            
            if last_user and "research" in last_user["content"].lower():
                # User requested research, we should provide satisfaction check after research
                result["awaiting_satisfaction"] = True
                result["satisfaction_question"] = result["current_topic"]["satisfaction_prompt"]
            elif last_ai and "satisfied" in last_ai["content"].lower():
                # We already asked satisfaction question, waiting for response
                result["awaiting_satisfaction"] = True
        
        result["is_complete"] = result["current_position"] > 14
        
        # Debug info
        result["debug"] = {
            "questions_asked": topic_questions_asked,
            "completed_topics": completed_topics,
            "current_position": result["current_position"]
        }
        
        return result

# Test function
def test_simple_manager():
    manager = SimpleInterviewManager()
    
    # Test Netflix conversation - exact flow from user
    messages = [
        {"role": "system", "content": "System prompt"},
        {"role": "assistant", "content": "What is your company name and give me a brief overview of what your business does?"},
        {"role": "user", "content": "Netflix - streaming service"},
        {"role": "assistant", "content": "Now let's discuss your product/service footprint..."},
        {"role": "user", "content": "research this yourself"},
        {"role": "assistant", "content": "Netflix's ability to deliver timely, culturally relevant content... Are you satisfied with this research, or would you like me to investigate any specific areas further?"},
        {"role": "user", "content": "ok"},
        {"role": "assistant", "content": "Let's analyze your historical financial performance..."},
        {"role": "user", "content": "research this yourself"},  
        {"role": "assistant", "content": "Netflix's historical financial performance from 2021 to 2025... Are you satisfied with this research, or would you like me to investigate any specific areas further?"},
        {"role": "user", "content": "ok"}
    ]
    
    result = manager.analyze_simple_progress(messages)
    print(f"Current Position: {result['current_position']}")
    print(f"Current Topic: {result['current_topic']['id']}")
    print(f"Next Question: {result['next_question'][:100]}...")
    print(f"Debug: {result['debug']}")
    
    return result

if __name__ == "__main__":
    test_simple_manager()