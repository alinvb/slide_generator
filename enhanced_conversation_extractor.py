#!/usr/bin/env python3
"""
Enhanced Conversation Data Extractor
Ensures comprehensive extraction of all required fields from conversation
"""

import json
import re
from typing import Dict, List, Any, Optional
from comprehensive_data_requirements import (
    REQUIRED_FIELDS_MAPPING, 
    FIELD_PRIORITY_LEVELS, 
    QUALITY_THRESHOLDS,
    get_missing_critical_fields,
    get_missing_high_priority_fields,
    validate_data_quality
)

class EnhancedConversationExtractor:
    """Enhanced extractor ensuring comprehensive field coverage"""
    
    def __init__(self):
        self.extraction_coverage = {
            "critical_fields_extracted": [],
            "high_priority_extracted": [], 
            "medium_priority_extracted": [],
            "low_priority_extracted": [],
            "missing_critical": [],
            "missing_high_priority": []
        }
    
    def extract_comprehensive_data(self, messages: List[Dict], llm_api_call, company_name: str = None) -> Dict:
        """Extract all possible data from conversation with comprehensive coverage"""
        print("🔍 [ENHANCED] Starting comprehensive conversation data extraction...")
        
        if not messages or len(messages) == 0:
            print("❌ [ENHANCED] No conversation messages provided")
            raise ValueError("Conversation messages required for data extraction - no fallback data allowed")
        
        # Extract company context
        company_context = self._extract_company_context(messages, company_name)
        print(f"🏢 [ENHANCED] Company context: {company_context.get('name', 'Unknown')}")
        
        # Multi-pass extraction for comprehensive coverage
        extracted_data = {}
        
        # Pass 1: Extract critical fields first
        critical_data = self._extract_critical_fields(messages, company_context, llm_api_call)
        extracted_data.update(critical_data)
        
        # Pass 2: Extract high-priority business data
        business_data = self._extract_business_data(messages, company_context, llm_api_call)
        extracted_data.update(business_data)
        
        # Pass 3: Extract financial and valuation data
        financial_data = self._extract_financial_data(messages, company_context, llm_api_call)
        extracted_data.update(financial_data)
        
        # Pass 4: Extract buyer and transaction data
        buyer_data = self._extract_buyer_transaction_data(messages, company_context, llm_api_call)
        extracted_data.update(buyer_data)
        
        # Pass 5: Extract competitive and strategic data
        competitive_data = self._extract_competitive_data(messages, company_context, llm_api_call)
        extracted_data.update(competitive_data)
        
        # Validate extraction coverage
        self._validate_extraction_coverage(extracted_data)
        
        print(f"✅ [ENHANCED] Comprehensive extraction completed: {len(extracted_data)} top-level fields")
        return extracted_data
    
    def _extract_company_context(self, messages: List[Dict], company_name: str = None) -> Dict:
        """Extract basic company context and identify the target company"""
        context = {"name": company_name or "Unknown Company"}
        
        # Look for company mentions in conversation
        conversation_text = self._get_conversation_text(messages)
        
        # Extract company name if not provided
        if not company_name:
            company_patterns = [
                r"(?:analyzing|researching|about)\s+([A-Z][A-Za-z\s&,.-]+?)(?:\s+(?:is|was|has|stock|company|inc|corp|ltd))",
                r"([A-Z][A-Za-z\s&,.-]+?)(?:\s+(?:Inc|Corp|Ltd|LLC|Company))",
                r"(?:^|\s)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*?)(?:\s+(?:business|revenue|EBITDA))"
            ]
            
            for pattern in company_patterns:
                matches = re.findall(pattern, conversation_text, re.MULTILINE | re.IGNORECASE)
                if matches:
                    # Take the most frequently mentioned company name
                    company_candidates = [m.strip() for m in matches if len(m.strip()) > 2]
                    if company_candidates:
                        context["name"] = max(set(company_candidates), key=company_candidates.count)
                        break
        
        # Extract industry context
        industry_keywords = {
            "technology": ["software", "saas", "platform", "ai", "ml", "data", "analytics", "cloud"],
            "healthcare": ["medical", "pharmaceutical", "biotech", "health", "clinical", "drug"],
            "financial": ["fintech", "banking", "payment", "lending", "insurance", "investment"],
            "media": ["streaming", "content", "entertainment", "video", "music", "gaming"],
            "retail": ["ecommerce", "marketplace", "consumer", "retail", "shopping", "brand"],
            "manufacturing": ["manufacturing", "industrial", "automotive", "aerospace", "materials"]
        }
        
        for industry, keywords in industry_keywords.items():
            if any(keyword in conversation_text.lower() for keyword in keywords):
                context["industry"] = industry
                break
        
        return context
    
    def _extract_critical_fields(self, messages: List[Dict], company_context: Dict, llm_api_call) -> Dict:
        """Extract critical fields required for basic functionality"""
        print("🎯 [ENHANCED] Extracting critical fields...")
        
        conversation_text = self._get_conversation_text(messages)
        company_name = company_context.get("name", "Unknown Company")
        
        critical_prompt = f"""
        Extract CRITICAL business information for {company_name} from this conversation:
        
        CONVERSATION:
        {conversation_text[-3000:]}  # Last 3000 chars for context
        
        Return ONLY a JSON object with these CRITICAL fields:
        {{
            "entities": {{"company": {{"name": "{company_name}"}}}},
            "facts": {{
                "years": ["2020", "2021", "2022", "2023", "2024E"],
                "revenue_usd_m": [extract actual revenue figures in USD millions, or empty array if not mentioned],
                "ebitda_usd_m": [extract actual EBITDA figures in USD millions, or empty array if not mentioned],
                "ebitda_margins": [extract actual EBITDA margins in percentages, or empty array if not mentioned]
            }},
            "business_overview_data": {{
                "description": "Comprehensive description of what {company_name} does based on conversation",
                "timeline": {{"start_year": "founding year if mentioned or estimate", "end_year": 2025}},
                "highlights": ["3-5 key business highlights extracted from conversation"],
                "services": ["core services/products mentioned in conversation"],
                "positioning_desc": "market positioning description based on conversation"
            }}
        }}
        
        CRITICAL: Use ONLY information directly mentioned or clearly implied in the conversation.
        If financial data is not mentioned, use empty arrays [].
        Focus on extracting real conversation content, not generic descriptions.
        """
        
        try:
            response = llm_api_call([{"role": "user", "content": critical_prompt}])
            return self._parse_json_response(response, "critical_fields")
        except Exception as e:
            print(f"❌ [ENHANCED] Critical field extraction failed: {e}")
            raise ValueError(f"Critical field extraction failed: {e} - no fallback data allowed")
    
    def _extract_business_data(self, messages: List[Dict], company_context: Dict, llm_api_call) -> Dict:
        """Extract comprehensive business and operational data"""
        print("🏢 [ENHANCED] Extracting business data...")
        
        conversation_text = self._get_conversation_text(messages)
        company_name = company_context.get("name", "Unknown Company")
        
        business_prompt = f"""
        Extract BUSINESS and OPERATIONAL information for {company_name} from conversation:
        
        CONVERSATION:
        {conversation_text[-4000:]}
        
        Return JSON with these fields:
        {{
            "product_service_data": {{
                "services": [
                    {{"title": "Service Name", "desc": "Detailed service description from conversation"}},
                    // Extract 3-5 services mentioned
                ],
                "coverage_table": [
                    ["Geographic Region", "Market Segment", "Product Focus", "Status"],
                    ["Region 1", "Market info from conversation", "Products mentioned", "Status"]
                    // Add rows based on geographic/market info from conversation
                ],
                "metrics": {{
                    "key_metric_1": "value if mentioned",
                    "key_metric_2": "value if mentioned"
                    // Extract any business metrics mentioned (users, customers, etc.)
                }}
            }},
            "management_team": {{
                "left_column_profiles": [
                    {{
                        "name": "Executive Name from conversation",
                        "role_title": "Exact title mentioned",
                        "experience_bullets": [
                            "Background point 1 from conversation",
                            "Background point 2 from conversation", 
                            "Background point 3 from conversation",
                            "Background point 4 from conversation",
                            "Background point 5 from conversation"
                        ]
                    }}
                    // Extract 2-3 executives mentioned in conversation
                ],
                "right_column_profiles": [
                    // Additional executives if mentioned
                ]
            }}
        }}
        
        Extract ONLY information mentioned in conversation. If executives aren't mentioned, return empty arrays.
        """
        
        try:
            response = llm_api_call([{"role": "user", "content": business_prompt}])
            return self._parse_json_response(response, "business_data")
        except Exception as e:
            print(f"⚠️ [ENHANCED] Business data extraction failed: {e}")
            return {}  # Not critical, can be filled by gap-filling
    
    def _extract_financial_data(self, messages: List[Dict], company_context: Dict, llm_api_call) -> Dict:
        """Extract financial performance and valuation data"""
        print("💰 [ENHANCED] Extracting financial data...")
        
        conversation_text = self._get_conversation_text(messages)
        company_name = company_context.get("name", "Unknown Company")
        
        financial_prompt = f"""
        Extract FINANCIAL and VALUATION information for {company_name}:
        
        CONVERSATION:
        {conversation_text[-4000:]}
        
        Return JSON:
        {{
            "growth_strategy_data": {{
                "growth_strategy": {{
                    "strategies": [
                        "Growth strategy 1 mentioned in conversation",
                        "Growth strategy 2 mentioned in conversation"
                        // Extract growth initiatives discussed
                    ]
                }},
                "financial_projections": {{
                    "categories": ["2024E", "2025E", "2026E", "2027E"],
                    "revenue": [projected revenue if mentioned],
                    "ebitda": [projected ebitda if mentioned]
                }}
            }},
            "valuation_data": [
                {{
                    "methodology": "Valuation method mentioned (DCF, Trading Multiples, etc.)",
                    "enterprise_value": "Valuation range mentioned",
                    "metric": "Key metric used",
                    "22a_multiple": "Multiple if mentioned",
                    "23e_multiple": "Multiple if mentioned", 
                    "commentary": "Valuation explanation from conversation"
                }}
                // Extract all valuation discussions
            ],
            "margin_cost_data": {{
                "chart_data": {{
                    "categories": ["2021", "2022", "2023", "2024E", "2025E"],
                    "values": [margin values if mentioned in conversation]
                }},
                "cost_management": {{
                    "items": [
                        {{"title": "Cost initiative", "description": "Description from conversation"}}
                    ]
                }},
                "risk_mitigation": {{
                    "main_strategy": "Risk mitigation strategy mentioned"
                }}
            }}
        }}
        
        Extract only financial information specifically mentioned in conversation.
        """
        
        try:
            response = llm_api_call([{"role": "user", "content": financial_prompt}])
            return self._parse_json_response(response, "financial_data")
        except Exception as e:
            print(f"⚠️ [ENHANCED] Financial data extraction failed: {e}")
            return {}
    
    def _extract_buyer_transaction_data(self, messages: List[Dict], company_context: Dict, llm_api_call) -> Dict:
        """Extract buyer profiles and transaction comparables"""
        print("🤝 [ENHANCED] Extracting buyer and transaction data...")
        
        conversation_text = self._get_conversation_text(messages)
        company_name = company_context.get("name", "Unknown Company")
        
        buyer_prompt = f"""
        Extract BUYER and TRANSACTION information for {company_name}:
        
        CONVERSATION:
        {conversation_text[-4000:]}
        
        Return JSON:
        {{
            "strategic_buyers": [
                {{
                    "buyer_name": "Strategic buyer name mentioned in conversation",
                    "description": "Buyer description from conversation", 
                    "strategic_rationale": "Why they would acquire - from conversation",
                    "key_synergies": "Synergies mentioned",
                    "fit": "Strategic fit assessment if mentioned",
                    "financial_capacity": "Financial capacity if discussed"
                }}
                // Extract all strategic buyers mentioned
            ],
            "financial_buyers": [
                {{
                    "buyer_name": "PE/VC firm name mentioned",
                    "description": "Firm description from conversation",
                    "strategic_rationale": "Investment thesis from conversation", 
                    "key_synergies": "Value-add mentioned",
                    "fit": "Investment fit if discussed",
                    "financial_capacity": "Capital availability if mentioned"
                }}
                // Extract all financial buyers mentioned
            ],
            "precedent_transactions": [
                {{
                    "target": "Target company mentioned",
                    "acquirer": "Acquirer mentioned",
                    "date": "Transaction date if mentioned",
                    "country": "Country if mentioned",
                    "enterprise_value": "Deal value if mentioned", 
                    "revenue": "Target revenue if mentioned",
                    "ev_revenue_multiple": "Multiple if calculated/mentioned"
                }}
                // Extract all transactions mentioned as comparables
            ],
            "sea_conglomerates": [
                {{
                    "name": "Conglomerate name mentioned",
                    "country": "Country from conversation",
                    "description": "Description from conversation",
                    "key_shareholders": "Shareholders if mentioned", 
                    "key_financials": "Financial info if mentioned",
                    "contact": "Contact info if available"
                }}
                // Extract regional conglomerates mentioned
            ]
        }}
        
        Focus on buyers and transactions specifically mentioned in the conversation.
        """
        
        try:
            response = llm_api_call([{"role": "user", "content": buyer_prompt}])
            return self._parse_json_response(response, "buyer_transaction_data")
        except Exception as e:
            print(f"⚠️ [ENHANCED] Buyer/transaction data extraction failed: {e}")
            return {}
    
    def _extract_competitive_data(self, messages: List[Dict], company_context: Dict, llm_api_call) -> Dict:
        """Extract competitive analysis and strategic considerations"""
        print("⚔️ [ENHANCED] Extracting competitive data...")
        
        conversation_text = self._get_conversation_text(messages)
        company_name = company_context.get("name", "Unknown Company")
        
        competitive_prompt = f"""
        Extract COMPETITIVE and STRATEGIC information for {company_name}:
        
        CONVERSATION:
        {conversation_text[-4000:]}
        
        Return JSON:
        {{
            "competitive_analysis": {{
                "competitors": [
                    {{"name": "Competitor name mentioned", "revenue": "revenue figure if mentioned or null"}},
                    // Extract all competitors mentioned
                ],
                "assessment": [
                    ["Company", "Market Focus", "Product Quality", "Market Share", "Innovation"],
                    ["{company_name}", "Assessment from conversation", "Quality from conversation", "Share from conversation", "Innovation from conversation"],
                    ["Competitor 1", "Assessment", "Quality", "Share", "Innovation"]
                    // Build assessment table based on conversation
                ],
                "barriers": [
                    {{"title": "Barrier mentioned", "desc": "Description from conversation"}}
                ],
                "advantages": [
                    {{"title": "Advantage mentioned", "desc": "Description from conversation"}}
                ]
            }},
            "investor_considerations": {{
                "considerations": [
                    "Investment consideration 1 from conversation",
                    "Investment consideration 2 from conversation"
                    // Extract investment thesis points
                ],
                "mitigants": [
                    "Risk mitigant 1 from conversation", 
                    "Risk mitigant 2 from conversation"
                    // Extract risk mitigation factors
                ]
            }},
            "investor_process_data": {{
                "diligence_topics": [
                    "Due diligence topic mentioned",
                    // Extract DD topics if discussed
                ],
                "synergy_opportunities": [
                    "Synergy opportunity mentioned"
                    // Extract synergies discussed
                ],
                "risk_factors": [
                    "Risk factor mentioned"
                    // Extract risks discussed
                ],
                "mitigants": [
                    "Risk mitigant mentioned"
                    // Extract mitigants
                ],
                "timeline": [
                    "Process step mentioned"
                    // Extract process timeline if discussed
                ]
            }}
        }}
        
        Extract competitive and strategic information mentioned in conversation.
        """
        
        try:
            response = llm_api_call([{"role": "user", "content": competitive_prompt}])
            return self._parse_json_response(response, "competitive_data")
        except Exception as e:
            print(f"⚠️ [ENHANCED] Competitive data extraction failed: {e}")
            return {}
    
    def _get_conversation_text(self, messages: List[Dict], max_messages: int = 15) -> str:
        """Extract conversation text for analysis"""
        conversation_text = ""
        
        # Get recent messages for context
        recent_messages = messages[-max_messages:] if len(messages) > max_messages else messages
        
        for msg in recent_messages:
            if isinstance(msg, dict) and 'content' in msg:
                role = msg.get('role', 'unknown')
                content = str(msg['content'])
                conversation_text += f"[{role.upper()}]: {content}\n\n"
        
        return conversation_text
    
    def _parse_json_response(self, response: str, data_type: str) -> Dict:
        """Parse JSON response with error handling"""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if not json_match:
                print(f"⚠️ [ENHANCED] No JSON found in {data_type} response")
                return {}
            
            json_str = json_match.group()
            
            # Clean common issues
            json_str = (json_str.replace('–', '-')
                               .replace('—', '-')  
                               .replace('"', '"')
                               .replace('"', '"')
                               .replace(''', "'")
                               .replace(''', "'")
                               .replace(',}', '}')
                               .replace(',]', ']'))
            
            parsed = json.loads(json_str)
            print(f"✅ [ENHANCED] Successfully parsed {data_type}: {len(parsed)} fields")
            return parsed
            
        except json.JSONDecodeError as e:
            print(f"❌ [ENHANCED] JSON parsing failed for {data_type}: {e}")
            return {}
        except Exception as e:
            print(f"❌ [ENHANCED] Unexpected error parsing {data_type}: {e}")
            return {}
    
    def _validate_extraction_coverage(self, extracted_data: Dict) -> None:
        """Validate extraction coverage and update tracking"""
        missing_critical = get_missing_critical_fields(extracted_data)
        missing_high = get_missing_high_priority_fields(extracted_data)
        
        self.extraction_coverage["missing_critical"] = missing_critical
        self.extraction_coverage["missing_high_priority"] = missing_high
        
        # Log coverage results
        if missing_critical:
            print(f"🚨 [ENHANCED] Missing CRITICAL fields: {missing_critical}")
        else:
            print(f"✅ [ENHANCED] All CRITICAL fields extracted")
            
        if missing_high:
            print(f"⚠️ [ENHANCED] Missing HIGH priority fields: {missing_high}")
        
        # Validate data quality
        quality_results = validate_data_quality(extracted_data)
        if quality_results["failed"]:
            print(f"📊 [ENHANCED] Quality issues: {quality_results['failed']}")
    
    def get_extraction_summary(self) -> Dict:
        """Get summary of extraction coverage"""
        return self.extraction_coverage