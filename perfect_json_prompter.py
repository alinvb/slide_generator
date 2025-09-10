"""
Perfect JSON Prompter System
Creates enhanced prompts that teach LLMs to produce perfect JSON matching our templates
"""

import json
from typing import Dict, Any, List


class PerfectJSONPrompter:
    """
    Creates perfect prompts that teach LLMs to produce flawless JSON
    Uses our perfect templates as examples and provides detailed instructions
    """
    
    def __init__(self):
        self.perfect_content_ir_template = None
        self.perfect_render_plan_template = None
        self.load_perfect_templates()
    
    def load_perfect_templates(self):
        """Load perfect JSON templates"""
        try:
            with open('/home/user/webapp/test_user_json_content_ir.json', 'r', encoding='utf-8') as f:
                self.perfect_content_ir_template = json.load(f)
            
            with open('/home/user/webapp/corrected_user_json_render_plan.json', 'r', encoding='utf-8') as f:
                self.perfect_render_plan_template = json.load(f)
                
            print("✅ [PERFECT PROMPTER] Perfect templates loaded successfully")
            
        except Exception as e:
            print(f"❌ [PERFECT PROMPTER] Failed to load templates: {str(e)}")
    
    def get_enhanced_system_prompt(self) -> str:
        """Get the enhanced system prompt with investment banker identity and DCF capabilities"""
        return self.create_enhanced_system_prompt()
    
    def create_enhanced_system_prompt(self) -> str:
        """Create the systematic interview prompt that conducts proper 14-topic interview"""
        
        # Simple examples for reference
        content_ir_example = {"entities": {"company": {"name": "Example Corp"}}, "facts": {"years": ["2022", "2023"], "revenue_usd_m": [100, 120]}}
        render_plan_example = {"slides": [{"template": "business_overview", "data": {"title": "Business Overview"}}]}
        
        system_prompt = f"""🎯 SYSTEMATIC INVESTMENT BANKING INTERVIEW PROTOCOL:

You are a highly trained, astute investment banker and professional pitch deck copilot that conducts SYSTEMATIC INTERVIEWS covering ALL 14 required topics BEFORE generating any JSON files.

🚨 PRIMARY ROLE: CONDUCT COMPLETE INTERVIEW AS INVESTMENT BANKER 🚨

**INVESTMENT BANKER EXPERTISE & ANALYTICAL CAPABILITIES:**
- **DCF Analysis**: Calculate detailed discounted cash flow valuations with explicit assumptions
- **Trading Multiples**: Analyze comparable public company valuations with actual multiples
- **Precedent Transactions**: Analyze recent M&A deals with detailed metrics and calculations
- **Regional Market Expertise**: Deep knowledge of local and regional markets and buyers
- **Verifiable References**: EVERY answer must include sources, data citations, and references [1][2][3]

**NATURAL CONVERSATION FLOW:**
- Build context progressively through the interview
- Reference previous answers to create continuity  
- Use company-specific details discovered in earlier topics
- Maintain professional investment banker tone throughout
- Ask follow-up questions that demonstrate you're listening and building on responses

**ENHANCED RESEARCH PROTOCOL:**
- If user says "research this" or "I don't know": provide comprehensive research with sources
- After research: "Are you satisfied with this research, or would you like me to investigate any specific areas further?"
- Never repeat topics - check conversation history first
- Build each question on information from previous answers

**CRITICAL INTERVIEW RULES:**
- ASK ONE TOPIC AT A TIME - Never ask multiple topics together
- Follow STRICT SEQUENTIAL ORDER: Topic 1 → Topic 2 → ... → Topic 14
- CHECK conversation history before asking to prevent repetition
- If user says "you just asked this" - apologize and move to NEXT topic immediately
- Maintain conversational flow with contextual references"""

        return system_prompt
        
    def extract_context_from_conversation(self, messages: List[Dict[str, Any]]) -> Dict[str, str]:
        """Extract key context elements from the conversation for contextual prompting"""
        context = {
            "company_name": "[company_name]",
            "business_description": "[business_description]", 
            "geographic_footprint": "[geographic_footprint]",
            "product_services": "[product_services]",
            "revenue_scale": "[revenue_scale]",
            "growth_trajectory": "[growth_trajectory]",
            "company_industry": "[company_industry]",
            "financial_performance": "[financial_performance]",
            "management_capabilities": "[management_capabilities]",
            "current_margins": "[current_margins]",
            "competitive_strengths": "[competitive_strengths]",
            "industry_sector": "[industry_sector]",
            "operating_regions": "[operating_regions]",
            "growth_projections": "[growth_projections]",
            "company_characteristics": "[company_characteristics]",
            "business_model": "[business_model]",
            "competitive_positioning": "[competitive_positioning]",
            "valuation_range": "[valuation_range]",
            "competitive_advantages": "[competitive_advantages]",
            "geographic_markets": "[geographic_markets]",
            "customer_base": "[customer_base]",
            "growth_strategy": "[growth_strategy]",
            "valuation_expectations": "[valuation_expectations]",
            "market_dynamics": "[market_dynamics]",
            "growth_stage": "[growth_stage]",
            "strategic_buyers": "[strategic_buyers]",
            "financial_buyers": "[financial_buyers]",
            "conglomerates": "[conglomerates]",
            "ebitda_margins": "[ebitda_margins]",
            "buyer_interest": "[buyer_interest]",
            "valuation_multiple": "[valuation_multiple]",
            "industry_benchmarks": "[industry_benchmarks]",
            "target_margins": "[target_margins]",
            "key_competitors": "[key_competitors]",
            "business_scale": "[business_scale]",
            "margin_sustainability": "[margin_sustainability]",
            "growth_execution": "[growth_execution]",
            "buyer_universe": "[buyer_universe]",
            "risk_factors": "[risk_factors]",
            "business_complexity": "[business_complexity]",
            "potential_acquirers": "[potential_acquirers]",
            "main_risks": "[main_risks]",
            "regulatory_environment": "[regulatory_environment]"
        }
        
        # Extract actual values from conversation
        conversation_text = " ".join([msg["content"] for msg in messages if msg["role"] != "system"]).lower()
        
        # Simple pattern matching for key information
        # This could be enhanced with more sophisticated NLP
        
        return context
    
    def create_interview_completion_prompt(self, messages: List[Dict[str, Any]]) -> str:
        """Create simplified prompt for JSON generation"""
        
        # Extract key information from conversation
        conversation_text = " ".join([msg.get("content", "") for msg in messages if msg.get("role") != "system"])

        prompt = f"""Generate investment banking presentation JSONs based on our conversation.

CONVERSATION DATA:
{conversation_text[-1500:]}

🚨 REQUIRED OUTPUT FORMAT:

CONTENT IR JSON:
{{complete_business_data_json}}

RENDER PLAN JSON:
{{complete_slide_structure_json}}

REQUIREMENTS:
- Use conversation data to populate JSONs
- Professional estimates for missing data
- BOTH JSONs must be complete and valid
- Start immediately with "CONTENT IR JSON:" then "RENDER PLAN JSON:"

Generate both JSONs now:"""

        return prompt
    
    def create_refinement_prompt_with_perfect_examples(self, current_json: Dict[str, Any], 
                                                    issues: List[str], json_type: str) -> str:
        """Create refinement prompt using perfect examples"""
        
        if json_type == "content_ir":
            perfect_example = json.dumps(self.perfect_content_ir_template, indent=2)[:4000]
            json_description = "Content IR"
        else:
            perfect_example = json.dumps(self.perfect_render_plan_template, indent=2)[:4000]
            json_description = "Render Plan"
        
        prompt = f"""You are a JSON perfectionist. Your task is to fix this {json_description} JSON to achieve 100% perfection.

CURRENT ISSUES FOUND:
{chr(10).join([f"❌ {issue}" for issue in issues[:10]])}

PERFECT REFERENCE EXAMPLE:
```json
{perfect_example}
```

CURRENT JSON TO FIX:
```json
{json.dumps(current_json, indent=2)}
```

PERFECTION REQUIREMENTS:
1. Fix ALL issues listed above
2. Match the EXACT structure of the perfect example  
3. Ensure NO missing fields, empty arrays, or null values
4. Use professional, investment-banking quality language
5. Make all data consistent and realistic
6. Follow proper JSON formatting

Return ONLY the corrected JSON with zero issues:"""

        return prompt


# Global instance for easy access
perfect_prompter = PerfectJSONPrompter()


def get_enhanced_system_prompt() -> str:
    """Get the enhanced system prompt for perfect JSON generation"""
    return perfect_prompter.create_enhanced_system_prompt()


def get_interview_completion_prompt(messages: List[Dict[str, Any]]) -> str:
    """Get enhanced prompt for interview completion"""
    return perfect_prompter.create_interview_completion_prompt(messages)


if __name__ == "__main__":
    # Test the prompter
    prompter = PerfectJSONPrompter()
    system_prompt = prompter.create_enhanced_system_prompt()
    print("System prompt length:", len(system_prompt))
    print("First 500 chars:", system_prompt[:500])