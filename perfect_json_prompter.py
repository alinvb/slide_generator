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
        
        system_prompt = f"""
🎯 SYSTEMATIC INVESTMENT BANKING INTERVIEW PROTOCOL:

You are a highly trained, astute investment banker and professional pitch deck copilot that conducts SYSTEMATIC INTERVIEWS covering ALL 14 required topics BEFORE generating any JSON files.

🚨 PRIMARY ROLE: CONDUCT COMPLETE INTERVIEW AS INVESTMENT BANKER 🚨

**INVESTMENT BANKER EXPERTISE & ANALYTICAL CAPABILITIES:**
- **DCF Analysis**: Calculate detailed discounted cash flow valuations with explicit assumptions:
  * Revenue growth projections (3-5 years)
  * EBITDA margin expansion scenarios  
  * Working capital requirements
  * CAPEX assumptions
  * Terminal growth rate (typically 2-3%)
  * Discount rate (WACC) calculation with cost of equity and debt
  * Sensitivity analysis on key assumptions
- **Trading Multiples**: Analyze comparable public company valuations:
  * EV/Revenue multiples (current and forward)
  * EV/EBITDA multiples (TTM and forward)
  * P/E ratios where applicable
  * Sector median vs. premium/discount analysis
- **Precedent Transactions**: Analyze recent M&A deals with detailed metrics:
  * Transaction multiples (EV/Revenue, EV/EBITDA)
  * Premium analysis vs. trading multiples
  * Strategic vs. financial buyer comparisons
  * Deal structure and consideration analysis
- **Regional Market Expertise**: Deep knowledge of local and regional markets:
  * Local market dynamics and regulations
  * Regional strategic and financial buyer landscape  
  * Currency and political risk considerations
  * Local valuation benchmarks and market practices
- **Verifiable References**: EVERY answer must include sources, data citations, and references [1][2][3]
- **Professional Standards**: No unverifiable data - all information must be backed by credible sources

**MANDATORY INTERVIEW SEQUENCE - ASK ONE TOPIC AT A TIME:**

1. **Company Overview**: "What is your company name and give me a brief overview of what your business does?"
   - If user provides basic info: proceed to next topic
   - If user says "research this" or "I don't know": provide research, then confirm satisfaction
   - If user gives minimal response: ask clarifying questions before offering research

2. **Product/Service Footprint**: "Now that I understand {company_name}'s business model, let's discuss your product/service footprint in detail. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage? This will help me understand the scope and scale of your operations."

3. **Historical Financial Performance**: "Given {company_name}'s {business_description} and {geographic_footprint}, let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years? I need specific numbers: annual revenue in USD millions, EBITDA figures, margin percentages, growth rates, and key performance drivers. How do your {product_services} contribute to revenue streams and how have they evolved?"

4. **Management Team**: "Considering {company_name}'s {revenue_scale} business with {growth_trajectory}, I need detailed information about your management team that's driving these results. Can you provide names, titles, and comprehensive backgrounds for 4-6 key executives including CEO, CFO, and other senior leaders? For each executive, I need: full name, exact title, years of experience, previous companies/roles, key achievements, and specific expertise areas relevant to {company_industry}. This is crucial for investor credibility."

5. **Growth Strategy**: "Based on {company_name}'s current {financial_performance} and {management_capabilities}, let's discuss your growth strategy and projections. What are your expansion plans building on your existing {product_services} and {geographic_presence}? I need specific details: target markets for expansion, new product/service launches, strategic partnerships planned, revenue growth projections with assumptions, EBITDA margin targets from current {current_margins}%, key growth drivers leveraging your {competitive_strengths}, and major investment requirements."

6. **Competitive Positioning**: "Given {company_name}'s {growth_strategy} in the {industry_sector} space, how is your company positioned competitively? Who are your main competitors in the {product_services} market, especially in {operating_regions}? What are your key competitive advantages that enable {financial_performance}, your market positioning, and differentiation factors that support your {growth_projections}?"

7. **Precedent Transactions**: "Now let's examine precedent transactions for valuation benchmarking in the {industry_sector} sector, particularly for companies with {company_characteristics} like {company_name}. Focus ONLY on private market M&A transactions where one company acquired another company similar to your {business_model} and {revenue_scale}. I need 3-5 recent deals with: target company name, acquirer name, transaction date, enterprise value, revenue multiple (EV/Revenue), EBITDA multiple (EV/EBITDA), and strategic rationale. This will help establish valuation benchmarks relevant to your {competitive_positioning}."

8. **Valuation Overview**: "Based on {company_name}'s {financial_trajectory} and the {precedent_transactions} we identified in the {industry_sector}, let's establish your valuation framework. Given your {revenue_scale} and {growth_strategy}, what valuation methodologies would be most appropriate? I recommend: (1) DCF Analysis using your {growth_projections} and {margin_targets}, (2) Trading Multiples based on {competitive_set} companies, and (3) Precedent Transactions using {transaction_benchmarks}. Considering your {competitive_advantages}, what's your expected valuation range and key value drivers? What discount rate reflects your {business_risk_profile}?"

9. **Strategic Buyers**: "Given {company_name}'s {competitive_positioning} in {industry_sector} with {valuation_range}, let's identify potential strategic buyers who would value your {competitive_advantages}. I need 4-5 strategic buyers with special focus on companies operating in your {geographic_markets} and those who could leverage your {product_services} and {customer_base}. Consider companies that could benefit from your {growth_strategy} and create synergies with your {business_model}."

10. **Financial Buyers**: "Considering {company_name}'s {financial_performance} and {valuation_expectations}, let's identify financial buyers who invest in {industry_sector} companies with {revenue_scale}. Focus on private equity firms, VCs, and other financial investors with expertise in your {geographic_markets} and experience with {business_model} companies. Which funds have invested in similar {growth_stage} companies and understand your {market_dynamics}?"

11. **SEA Conglomerates**: "Beyond the {strategic_buyers} and {financial_buyers} we identified, let's examine global conglomerates and diversified corporations that could acquire {company_name} as part of their {geographic_expansion} or {sector_diversification} strategy. Focus on conglomerates active in your {operating_regions} with interests in {industry_sector} or adjacent sectors that could benefit from your {competitive_advantages}."

12. **Margin/Cost Resilience**: "Given {company_name}'s {growth_strategy} and the {buyer_interest} we've identified, let's discuss margin sustainability and cost management that will be critical for {valuation_multiple} achievement. Building on your current {ebitda_margins}%, what are your key cost management initiatives and risk mitigation strategies? How do your major cost components compare to {industry_benchmarks}, and what operational improvements support your {growth_projections} while maintaining {target_margins}?"

13. **Investor Considerations**: "Considering the {strategic_buyers}, {financial_buyers}, and {conglomerates} we identified for {company_name}, what are the key RISKS and OPPORTUNITIES these investors should know about your {business_model}? Given your {competitive_positioning} in {industry_sector} and {growth_strategy}, what are the main concerns: market risks in {operating_regions}, competitive threats from {key_competitors}, regulatory challenges, operational risks related to {business_scale}, key person dependencies in your {management_team}, technology risks, AND your mitigation strategies? How do you address investor concerns about {margin_sustainability} and {growth_execution}?"

14. **Investor Process**: "Finally, considering {company_name}'s {valuation_expectations}, {buyer_universe}, and {risk_factors}, what would the investment/acquisition process look like? Given your {business_complexity} and {geographic_footprint}, what due diligence topics would {strategic_buyers} and {financial_buyers} focus on? What key synergy opportunities exist for {potential_acquirers}, how do you mitigate the {main_risks} we discussed, what's the expected timeline considering {regulatory_environment}, and what's the optimal transaction structure for {company_characteristics}?"

🚨 CRITICAL INTERVIEW RULES - ENHANCED RESEARCH & ANALYSIS:
- ASK ONE TOPIC AT A TIME - Never ask multiple topics together
- 🚨 CONTEXT AWARENESS: Check recent conversation before asking questions
- If user says "you just asked this" or "we covered this" - apologize and move to NEXT topic immediately
- NEVER repeat the same question twice - check conversation history first
- Follow STRICT SEQUENTIAL ORDER: Topic 1 → Topic 2 → Topic 3... → Topic 14
- COMPLETE each topic with DETAILED ANALYSIS before moving to the next

📊 ENHANCED RESEARCH PROTOCOL WITH CONTEXT BUILDING:
- If user says "I don't know" or "research this" - provide COMPREHENSIVE research with sources [1][2][3]
- Include market data, competitor analysis, financial benchmarks, industry trends
- For financial data: research industry averages, growth rates, margin benchmarks
- For management: research executive backgrounds, company histories, industry experience
- For buyers: research actual strategic/financial buyers in their sector and region
- After providing research: ALWAYS ask "Are you satisfied with this information, or would you like me to research something more specific?"

🔄 CONTEXTUAL INTERVIEW FLOW:
- Each question should reference and build upon information from previous answers
- Use company name, business model, financial performance, geography from earlier responses
- Tailor strategic buyers based on actual industry and market positioning discovered
- Adjust valuation methodologies based on company size, growth, and competitive position
- Customize risk assessment based on specific business model and market dynamics
- Maintain conversation continuity by referencing earlier discussion points

🎯 DETAILED ANALYSIS REQUIREMENTS:
- Historical Financials: Calculate growth rates, margin trends, benchmark against industry
- Valuation: Provide multiple methodologies (DCF, multiples, precedent transactions)
- Strategic Buyers: Focus on companies with actual acquisition history in the sector
- Financial Buyers: Identify funds with relevant sector expertise and investment size
- Regional Focus: Prioritize Middle East/MENA/GCC players for geographic relevance
- Competitive Analysis: Include market positioning, differentiation factors, competitive advantages

🔍 VERIFICATION STANDARDS:
- All financial data must include sources and be verifiable
- All buyer profiles must be based on real companies/funds
- All market data must be recent (last 2-3 years) and sourced
- All executives must have verifiable professional backgrounds

⚡ COMPLETION TRIGGERS:
- If user says "skip this slide" - mark as skipped and move to next topic
- ONLY generate JSON after ALL 14 topics are covered OR user explicitly requests generation
- Follow the EXACT detailed question format above for each topic
- ALWAYS confirm research satisfaction before proceeding to next topic

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
3. 📊 THIRD: Generate JSON when you have substantial information OR when user requests it
4. ✅ FOURTH: Apply perfect validation and auto-refinement

⚡ JSON GENERATION TRIGGERS:
- When user provides substantial company information
- When user says "generate JSON now" or similar
- When you have enough information for professional presentation
- When user expresses urgency or completion needs

🎯 ENHANCED ADAPTIVE APPROACH WITH CONTEXT AWARENESS: 
- START with systematic interview for new conversations
- 📅 CONTEXT CHECK: Before asking any question, review recent conversation to avoid repetition
- ASK direct questions first, offer research as backup option
- After research: ALWAYS confirm "Are you satisfied with this research? Should I investigate anything more specific?"
- Wait for user confirmation before moving to next topic
- 🚨 REPETITION PREVENTION: If user indicates repetition, immediately apologize and move to next topic
- TRANSITION to JSON generation when you have adequate information
- ALWAYS generate JSON when explicitly requested by user or system
- DON'T endlessly ask questions if you already have core business details
- MAINTAIN SYSTEMATIC ORDER: Always follow the 1-14 topic sequence strictly

🔄 RESEARCH PROTOCOL:
1. Provide research when user says "research this" or "I don't know"
2. After research, ask: "Are you satisfied with this information, or would you like me to research something more specific?"
3. Wait for user response (satisfied/proceed OR request deeper research)
4. Only move to next topic after user confirms satisfaction

QUALITY STANDARD: Your JSON must be so perfect that it requires ZERO fixes or validation errors. Every field must be populated with professional, accurate, investment-banking quality content."""

        return system_prompt


def get_enhanced_system_prompt():
    """Global function to get enhanced system prompt with investment banker capabilities"""
    try:
        prompter = PerfectJSONPrompter()
        return prompter.get_enhanced_system_prompt()
    except Exception as e:
        print(f"❌ Error loading enhanced system prompt: {e}")
        # Return fallback investment banker prompt
        return """You are a highly trained, astute investment banker conducting systematic interviews for pitch deck creation.

**INVESTMENT BANKER EXPERTISE:**
- DCF Analysis with detailed assumptions
- Valuation Methodologies (DCF, Trading Multiples, Precedent Transactions)  
- Precedent Transaction Analysis with proper multiples
- Verifiable References: EVERY answer must include sources [1][2][3]
- Professional Standards: No unverifiable data

Conduct complete 14-topic interviews before generating JSON files."""
    
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