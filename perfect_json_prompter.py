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
    
    def create_enhanced_system_prompt(self) -> str:
        """Create the systematic interview prompt that conducts proper 14-topic interview"""
        
        # Get condensed examples of perfect structure for reference
        content_ir_example = self._get_condensed_content_ir_example()
        render_plan_example = self._get_condensed_render_plan_example()
        
        system_prompt = f"""
🎯 SYSTEMATIC INVESTMENT BANKING INTERVIEW PROTOCOL:

You are a professional investment banking copilot that conducts SYSTEMATIC INTERVIEWS covering ALL 14 required topics BEFORE generating any JSON files.

🚨 PRIMARY ROLE: CONDUCT COMPLETE INTERVIEW FIRST 🚨

**MANDATORY INTERVIEW SEQUENCE - ASK ONE TOPIC AT A TIME:**

1. **Company Overview**: "What is your company name and give me a brief overview of what your business does?"

2. **Product/Service Footprint**: "Now let's discuss your product/service footprint. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage?"

3. **Historical Financial Performance**: "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years?"

4. **Management Team**: "Now I need information about your management team. Can you provide names, titles, and brief backgrounds for 4-6 key executives including CEO, CFO, and other senior leaders?"

5. **Growth Strategy**: "Let's discuss your growth strategy and projections. What are your expansion plans, strategic initiatives, and financial projections for the next 3-5 years?"

6. **Competitive Positioning**: "How is your company positioned competitively? I need information about key competitors, your competitive advantages, market positioning, and differentiation factors."

7. **Precedent Transactions**: "Now let's examine precedent transactions. Focus ONLY on private market M&A transactions where one company acquired another company. I need recent corporate acquisitions in your industry."

8. **Valuation Overview**: "What valuation methodologies and overview would be most appropriate for your business?"

9. **Strategic Buyers**: "Now let's identify potential strategic buyers—companies that might acquire you for strategic reasons."

10. **Financial Buyers**: "Now let's identify financial buyers—private equity firms, VCs, and other financial investors."

11. **SEA Conglomerates**: "Let's identify potential global conglomerates and strategic acquirers relevant to your region."

12. **Margin/Cost Resilience**: "Let's discuss margin and cost data. Can you provide your EBITDA margins and cost management initiatives?"

13. **Investor Considerations**: "What are the key RISKS and OPPORTUNITIES investors should know about your business?"

14. **Investor Process**: "Finally, what would the investment/acquisition process look like?"

🚨 CRITICAL INTERVIEW RULES:
- ASK ONE TOPIC AT A TIME - Never ask multiple topics together
- COMPLETE each topic before moving to the next
- If user says "I don't know" - offer to research for them
- If user says "skip this slide" - mark as skipped and move to next topic
- ONLY generate JSON after ALL 14 topics are covered
- Follow the EXACT question format above for each topic

JSON GENERATION GUIDELINES (USE ONLY AFTER COMPLETE INTERVIEW):

🎯 JSON QUALITY STANDARDS (FOR FINAL GENERATION ONLY):
1. ZERO missing fields - every required section must be present
2. ZERO empty arrays or null values - all data must be populated
3. PERFECT structure matching - follow templates EXACTLY
4. PROFESSIONAL content - investment banking quality language
5. CONSISTENT data - arrays must have matching lengths
6. COMPLETE management profiles - names, titles, 3+ experience bullets

📊 PERFECT CONTENT IR STRUCTURE (REFERENCE):
```json
{json.dumps(content_ir_example, indent=2)}
```

📋 PERFECT RENDER PLAN STRUCTURE (REFERENCE):  
```json
{json.dumps(render_plan_example, indent=2)}
```

🚨 CRITICAL REQUIREMENTS - ZERO TOLERANCE FOR ERRORS:

CONTENT IR MANDATORY SECTIONS:
✅ entities: Company name and details
✅ facts: Financial data (years, revenue_usd_m, ebitda_usd_m, ebitda_margins) - MUST have matching array lengths
✅ management_team: left_column_profiles and right_column_profiles with complete profiles
✅ strategic_buyers: 3-5 buyers with ALL fields (buyer_name, description, strategic_rationale, key_synergies, fit, financial_capacity)
✅ financial_buyers: 3-5 buyers with ALL fields  
✅ competitive_analysis: competitors, assessment table, barriers, advantages
✅ precedent_transactions: 3-5 transactions with ALL fields
✅ valuation_data: Multiple methodologies with complete details
✅ product_service_data: services, coverage_table, metrics
✅ business_overview_data: description, timeline, highlights, services, positioning_desc
✅ growth_strategy_data: strategies, financial_projections, key_assumptions
✅ investor_process_data: All process details
✅ margin_cost_data: chart_data, cost_management, risk_mitigation
✅ sea_conglomerates: Global companies list
✅ investor_considerations: considerations and mitigants

RENDER PLAN MANDATORY STRUCTURE:
✅ slides: Array of slide objects
✅ Each slide MUST have: template, data
✅ Buyer profile slides MUST have: content_ir_key, table_headers, table_rows
✅ All slide data must be complete and structured correctly

MANAGEMENT TEAM PERFECTION:
- Each profile MUST have: name, role_title, experience_bullets
- experience_bullets MUST be an array of 3-5 detailed bullet points
- Names must be real, professional executive names
- Titles must be standard C-level or executive titles
- Experience bullets must be specific, professional, achievement-focused

BUYER PROFILES PERFECTION:
- Strategic buyers: Focus on tech giants, cloud providers, AI companies
- Financial buyers: Focus on top-tier VCs, PE firms, investment funds
- Each buyer MUST have ALL 6 required fields completely filled
- fit field must include numeric rating (e.g., "High (9/10) - Strategic alignment")
- Descriptions must be accurate and professional

FINANCIAL DATA PERFECTION:
- years, revenue_usd_m, ebitda_usd_m, ebitda_margins arrays MUST have identical lengths
- Use realistic growth trajectories for high-growth SaaS/AI companies
- EBITDA margins should show improvement over time
- Include 4-5 years of data minimum

VALIDATION CHECKPOINTS:
Before outputting JSON, verify:
1. All 16 required Content IR sections present ✓
2. All arrays have consistent lengths ✓  
3. Management team has 2-4 complete profiles ✓
4. Strategic and financial buyers have 3-5 entries each ✓
5. All buyer profiles have 6 complete fields ✓
6. Render plan has proper slide array ✓
7. Buyer slides have content_ir_key and table structure ✓
8. NO empty strings, null values, or missing data ✓

OUTPUT FORMAT REQUIREMENTS:
- Start with "CONTENT IR JSON:"
- Output complete Content IR JSON
- Then "RENDER PLAN JSON:"  
- Output complete Render Plan JSON
- Use proper JSON formatting with correct indentation
- Ensure ALL brackets and braces are properly closed


🚨 CURRENT WORKFLOW PRIORITY:
1. 🗣️ FIRST: Conduct systematic interview (ask one question at a time)
2. 🔍 SECOND: Research missing information when user says "I dont know"
3. 📊 THIRD: ONLY generate JSON when all 14 topics are covered
4. ✅ FOURTH: Apply perfect validation and auto-refinement

🎯 REMEMBER: You are conducting an INTERVIEW, not generating JSON. Start with the first systematic question about company overview.
QUALITY STANDARD: Your JSON must be so perfect that it requires ZERO fixes or validation errors. Every field must be populated with professional, accurate, investment-banking quality content."""

        return system_prompt
    
    def _get_condensed_content_ir_example(self) -> Dict[str, Any]:
        """Get a condensed but complete example of perfect Content IR structure"""
        if not self.perfect_content_ir_template:
            return {}
        
        # Create a condensed version showing all required sections with minimal data
        condensed = {
            "entities": {"company": {"name": "ExampleCorp"}},
            "facts": {
                "years": ["2022", "2023", "2024E"],
                "revenue_usd_m": [10.0, 25.0, 45.0],
                "ebitda_usd_m": [1.0, 3.0, 8.0],
                "ebitda_margins": [10.0, 12.0, 17.8]
            },
            "management_team": {
                "left_column_profiles": [
                    {
                        "name": "John Smith",
                        "role_title": "Chief Executive Officer",
                        "experience_bullets": [
                            "Led company growth from startup to $50M ARR",
                            "Former VP Engineering at Fortune 500 tech company",
                            "15+ years experience in SaaS and enterprise software"
                        ]
                    },
                    {
                        "name": "Michael Chen",
                        "role_title": "Chief Financial Officer",
                        "experience_bullets": [
                            "Former CFO at high-growth SaaS company with successful IPO",
                            "15+ years investment banking and corporate finance experience",
                            "Led $100M+ funding rounds and M&A transactions"
                        ]
                    },
                    {
                        "name": "Lisa Rodriguez",
                        "role_title": "Chief Marketing Officer",
                        "experience_bullets": [
                            "Built marketing teams at 3 unicorn startups",
                            "Former VP Marketing at Fortune 500 enterprise software company",
                            "Expert in product marketing and demand generation"
                        ]
                    }
                ],
                "right_column_profiles": [
                    {
                        "name": "Sarah Johnson", 
                        "role_title": "Chief Technology Officer",
                        "experience_bullets": [
                            "Architected scalable platform serving 1M+ users",
                            "Former Principal Engineer at leading cloud provider",
                            "Expert in AI/ML infrastructure and data platforms"
                        ]
                    },
                    {
                        "name": "David Park",
                        "role_title": "Chief Operations Officer", 
                        "experience_bullets": [
                            "Scaled operations from 10 to 1000+ employees",
                            "Former VP Operations at leading tech unicorn",
                            "Expert in international expansion and process optimization"
                        ]
                    },
                    {
                        "name": "Amanda Williams",
                        "role_title": "Chief People Officer",
                        "experience_bullets": [
                            "Built talent acquisition and retention programs",
                            "Former CHRO at high-growth technology companies", 
                            "Expert in scaling engineering and sales teams"
                        ]
                    }
                ]
            },
            "strategic_buyers": [
                {
                    "buyer_name": "Microsoft",
                    "description": "Leading cloud and enterprise software provider",
                    "strategic_rationale": "Expand Azure AI capabilities and enterprise reach",
                    "key_synergies": "Integration with Microsoft 365 and Azure ecosystem",
                    "fit": "High (9/10) - Strategic platform alignment",
                    "financial_capacity": "Very High"
                }
            ],
            "financial_buyers": [
                {
                    "buyer_name": "Sequoia Capital",
                    "description": "Top-tier venture capital firm with SaaS focus",
                    "strategic_rationale": "Invest in next-generation enterprise software leader",
                    "key_synergies": "Portfolio company cross-selling and growth acceleration",
                    "fit": "High (9/10) - Proven SaaS investor",
                    "financial_capacity": "Very High"
                }
            ],
            "competitive_analysis": {
                "competitors": [{"name": "Competitor1", "revenue": 50}],
                "assessment": [["Company", "Market Position"], ["ExampleCorp", "⭐⭐⭐⭐⭐"]],
                "barriers": [{"title": "Technology", "desc": "Advanced AI capabilities"}],
                "advantages": [{"title": "Market Leadership", "desc": "First-mover advantage"}]
            },
            "precedent_transactions": [
                {
                    "target": "SimilarCorp",
                    "acquirer": "BigTech Inc",
                    "date": "Q2 2024",
                    "country": "USA",
                    "enterprise_value": "$500M",
                    "revenue": "$25M",
                    "ev_revenue_multiple": "20x"
                }
            ],
            "valuation_data": [
                {
                    "methodology": "Trading Multiples",
                    "enterprise_value": "$400-600M",
                    "metric": "EV/Revenue",
                    "22a_multiple": "15x",
                    "23e_multiple": "12x", 
                    "commentary": "Based on high-growth SaaS comparables"
                }
            ],
            "product_service_data": {
                "services": [{"title": "AI Platform", "desc": "Enterprise AI solutions"}],
                "coverage_table": [["Region", "Segment"], ["North America", "Enterprise"]],
                "metrics": {"clients": 500, "arr_growth": 150}
            },
            "business_overview_data": {
                "description": "Leading AI platform for enterprise automation",
                "timeline": {"start_year": 2020, "end_year": 2024},
                "highlights": ["Rapid growth", "Enterprise adoption"],
                "services": ["AI Platform", "Professional Services"],
                "positioning_desc": "Market leader in enterprise AI automation"
            },
            "growth_strategy_data": {
                "growth_strategy": {"strategies": ["Expand enterprise sales"]},
                "financial_projections": {
                    "categories": ["2024E", "2025E"],
                    "revenue": [45.0, 75.0],
                    "ebitda": [8.0, 18.0]
                },
                "key_assumptions": {
                    "revenue_cagr": "80-120%",
                    "margin_improvement": "Positive unit economics"
                }
            },
            "investor_process_data": {
                "diligence_topics": ["Technology review", "Market validation"],
                "synergy_opportunities": ["Platform integration"],
                "risk_factors": ["Competition", "Technology changes"],
                "mitigants": ["Strong team", "IP protection"],
                "timeline": ["Week 1: Initial review"]
            },
            "margin_cost_data": {
                "chart_data": {"categories": ["2023", "2024E"], "values": [12.0, 17.8]},
                "cost_management": {
                    "items": [{"title": "Cloud Optimization", "description": "Reduce infrastructure costs"}]
                },
                "risk_mitigation": {"main_strategy": "Scalable architecture"}
            },
            "sea_conglomerates": [
                {
                    "name": "Global TechCorp",
                    "country": "USA",
                    "description": "Diversified technology conglomerate",
                    "key_shareholders": "Institutional investors",
                    "key_financials": "$100B revenue",
                    "contact": "BD Team"
                }
            ],
            "investor_considerations": {
                "considerations": ["Market competition", "Technology risks"],
                "mitigants": ["Strong differentiation", "IP portfolio"]
            }
        }
        
        return condensed
    
    def _get_condensed_render_plan_example(self) -> Dict[str, Any]:
        """Get a condensed but complete example of perfect Render Plan structure"""
        condensed = {
            "slides": [
                {
                    "template": "business_overview",
                    "data": {
                        "title": "Business Overview",
                        "description": "Leading AI platform for enterprise automation",
                        "timeline": {"start_year": 2020, "end_year": 2024},
                        "highlights": ["Rapid growth", "Enterprise adoption"],
                        "services": ["AI Platform", "Professional Services"],
                        "positioning_desc": "Market leader in enterprise AI"
                    }
                },
                {
                    "template": "buyer_profiles",
                    "content_ir_key": "strategic_buyers",
                    "data": {
                        "title": "Strategic Buyer Profiles",
                        "table_headers": ["Buyer Name", "Description", "Strategic Rationale", "Key Synergies", "Fit"],
                        "table_rows": [
                            {
                                "buyer_name": "Microsoft",
                                "description": "Leading cloud provider",
                                "strategic_rationale": "Expand Azure AI capabilities", 
                                "key_synergies": "Azure integration",
                                "fit": "High (9/10)"
                            }
                        ]
                    }
                }
            ]
        }
        
        return condensed
    
    def create_interview_completion_prompt(self, messages: List[Dict[str, Any]]) -> str:
        """Create enhanced prompt for when interview is complete"""
        
        # Extract key information from conversation
        conversation_text = " ".join([msg.get("content", "") for msg in messages if msg.get("role") != "system"])
        
        # Count available information
        info_indicators = {
            "company_name": any(word in conversation_text.lower() for word in ["company", "business", "firm", "startup"]),
            "financials": any(word in conversation_text.lower() for word in ["revenue", "million", "growth", "funding"]),
            "management": any(word in conversation_text.lower() for word in ["ceo", "founder", "team", "executive"]),
            "business_model": any(word in conversation_text.lower() for word in ["product", "service", "platform", "customers"]),
            "competitive": any(word in conversation_text.lower() for word in ["competitor", "market", "industry"])
        }
        
        available_info_count = sum(info_indicators.values())
        
        prompt = f"""Based on our comprehensive interview covering {available_info_count}/5 key business areas, I now need you to generate the complete JSON structures for this investment banking presentation.

CONVERSATION SUMMARY:
{conversation_text[-2000:]}  # Last 2000 characters

YOUR TASK: Generate TWO perfect JSON structures:

1. **CONTENT IR JSON**: Complete business intelligence and data
2. **RENDER PLAN JSON**: Slide-by-slide presentation structure

{self.create_enhanced_system_prompt()}

SPECIFIC INSTRUCTIONS FOR THIS COMPANY:
- Use the actual company information discussed in our conversation
- Fill any missing details with realistic, professional estimates
- Ensure all financial projections are growth-oriented and realistic
- Create compelling buyer profiles based on the company's industry
- Make management team profiles professional and achievement-focused

CRITICAL REMINDER: Your JSON must be FLAWLESS. Every field must be populated, every structure must be perfect, every piece of data must be professional and accurate. This goes directly into a $10M+ investment banking presentation.

Generate the perfect JSONs now:"""

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