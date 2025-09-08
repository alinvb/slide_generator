"""
JSON Validator & Perfecter System
Advanced JSON validation and automatic refinement system for ensuring LLM outputs match perfect structure
"""

import json
import copy
from typing import Dict, Any, List, Tuple, Optional, Union
from dataclasses import dataclass
import re
from datetime import datetime


@dataclass
class ValidationResult:
    """Result of JSON validation"""
    is_valid: bool
    score: float  # 0.0 to 1.0, where 1.0 is perfect
    issues: List[str]
    missing_fields: List[str]
    invalid_types: List[str]
    empty_fields: List[str]
    suggestions: List[str]


class JSONValidatorPerfector:
    """
    Advanced JSON validation and automatic refinement system
    Ensures LLM outputs match perfect JSON structure with automatic correction loops
    """
    
    def __init__(self):
        self.perfect_content_ir_template = None
        self.perfect_render_plan_template = None
        self.load_perfect_templates()
        
        # Validation thresholds
        self.perfect_score_threshold = 0.95
        self.acceptable_score_threshold = 0.80
        self.max_refinement_attempts = 5
    
    def load_perfect_templates(self):
        """Load perfect JSON templates for validation reference"""
        try:
            # Load perfect Content IR template
            with open('/home/user/webapp/test_user_json_content_ir.json', 'r', encoding='utf-8') as f:
                self.perfect_content_ir_template = json.load(f)
            
            # Load perfect Render Plan template  
            with open('/home/user/webapp/corrected_user_json_render_plan.json', 'r', encoding='utf-8') as f:
                self.perfect_render_plan_template = json.load(f)
                
            print("✅ [JSON VALIDATOR] Perfect templates loaded successfully")
            
        except Exception as e:
            print(f"❌ [JSON VALIDATOR] Failed to load templates: {str(e)}")
            # Fallback to basic templates if files not found
            self._create_fallback_templates()
    
    def _create_fallback_templates(self):
        """Create basic fallback templates if perfect ones can't be loaded"""
        self.perfect_content_ir_template = {
            "entities": {"company": {"name": ""}},
            "facts": {
                "years": [],
                "revenue_usd_m": [],
                "ebitda_usd_m": [],
                "ebitda_margins": []
            },
            "management_team": {
                "left_column_profiles": [],
                "right_column_profiles": []
            },
            "strategic_buyers": [],
            "financial_buyers": [],
            "competitive_analysis": {},
            "precedent_transactions": [],
            "valuation_data": [],
            "product_service_data": {},
            "business_overview_data": {},
            "growth_strategy_data": {},
            "investor_process_data": {},
            "margin_cost_data": {},
            "sea_conglomerates": [],
            "investor_considerations": {}
        }
        
        self.perfect_render_plan_template = {
            "slides": []
        }
    
    def validate_content_ir(self, json_data: Dict[str, Any]) -> ValidationResult:
        """
        Comprehensive validation of Content IR JSON against perfect template
        Returns detailed validation result with scoring and specific issues
        """
        issues = []
        missing_fields = []
        invalid_types = []
        empty_fields = []
        suggestions = []
        
        if not isinstance(json_data, dict):
            return ValidationResult(
                is_valid=False,
                score=0.0,
                issues=["Root must be a dictionary"],
                missing_fields=[],
                invalid_types=["root"],
                empty_fields=[],
                suggestions=["Ensure JSON root is an object/dictionary"]
            )
        
        # Check required top-level sections
        required_sections = [
            "entities", "facts", "management_team", "strategic_buyers", 
            "financial_buyers", "competitive_analysis", "precedent_transactions",
            "valuation_data", "product_service_data", "business_overview_data",
            "growth_strategy_data", "investor_process_data", "margin_cost_data",
            "sea_conglomerates", "investor_considerations"
        ]
        
        score = 1.0
        
        for section in required_sections:
            if section not in json_data:
                missing_fields.append(section)
                issues.append(f"Missing required section: {section}")
                score -= 0.05
            elif not json_data[section]:
                empty_fields.append(section)
                issues.append(f"Empty section: {section}")
                score -= 0.03
        
        # Validate entities section
        if "entities" in json_data:
            entities_score = self._validate_entities_section(json_data["entities"], issues, missing_fields, invalid_types)
            score *= entities_score
        
        # Validate facts section (financial data)
        if "facts" in json_data:
            facts_score = self._validate_facts_section(json_data["facts"], issues, missing_fields, invalid_types)
            score *= facts_score
        
        # Validate management team
        if "management_team" in json_data:
            mgmt_score = self._validate_management_team(json_data["management_team"], issues, missing_fields, invalid_types)
            score *= mgmt_score
        
        # Validate buyer sections
        if "strategic_buyers" in json_data:
            strategic_score = self._validate_buyers_section(json_data["strategic_buyers"], "strategic", issues, invalid_types)
            score *= strategic_score
            
        if "financial_buyers" in json_data:
            financial_score = self._validate_buyers_section(json_data["financial_buyers"], "financial", issues, invalid_types)
            score *= financial_score
        
        # Validate competitive analysis
        if "competitive_analysis" in json_data:
            comp_score = self._validate_competitive_analysis(json_data["competitive_analysis"], issues, invalid_types)
            score *= comp_score
        
        # Validate precedent transactions
        if "precedent_transactions" in json_data:
            prec_score = self._validate_precedent_transactions(json_data["precedent_transactions"], issues, invalid_types)
            score *= prec_score
        
        # Generate suggestions based on issues found
        suggestions = self._generate_content_ir_suggestions(issues, missing_fields, empty_fields)
        
        # Ensure score is between 0 and 1
        score = max(0.0, min(1.0, score))
        
        is_valid = score >= self.acceptable_score_threshold and len(missing_fields) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            score=score,
            issues=issues,
            missing_fields=missing_fields,
            invalid_types=invalid_types,
            empty_fields=empty_fields,
            suggestions=suggestions
        )
    
    def validate_render_plan(self, json_data: Dict[str, Any]) -> ValidationResult:
        """
        Comprehensive validation of Render Plan JSON against perfect template
        """
        issues = []
        missing_fields = []
        invalid_types = []
        empty_fields = []
        suggestions = []
        
        if not isinstance(json_data, dict):
            return ValidationResult(
                is_valid=False,
                score=0.0,
                issues=["Root must be a dictionary"],
                missing_fields=[],
                invalid_types=["root"],
                empty_fields=[],
                suggestions=["Ensure JSON root is an object with 'slides' array"]
            )
        
        score = 1.0
        
        # Check for slides array
        if "slides" not in json_data:
            missing_fields.append("slides")
            issues.append("Missing required 'slides' array")
            score -= 0.5
        elif not isinstance(json_data["slides"], list):
            invalid_types.append("slides")
            issues.append("'slides' must be an array")
            score -= 0.4
        elif len(json_data["slides"]) == 0:
            empty_fields.append("slides")
            issues.append("'slides' array is empty")
            score -= 0.3
        else:
            # Validate each slide
            slides_score = self._validate_slides_array(json_data["slides"], issues, invalid_types)
            score *= slides_score
        
        # Generate suggestions
        suggestions = self._generate_render_plan_suggestions(issues, missing_fields, empty_fields)
        
        score = max(0.0, min(1.0, score))
        is_valid = score >= self.acceptable_score_threshold and len(missing_fields) == 0
        
        return ValidationResult(
            is_valid=is_valid,
            score=score,
            issues=issues,
            missing_fields=missing_fields,
            invalid_types=invalid_types,
            empty_fields=empty_fields,
            suggestions=suggestions
        )
    
    def _validate_entities_section(self, entities: Any, issues: List[str], missing_fields: List[str], invalid_types: List[str]) -> float:
        """Validate entities section structure"""
        if not isinstance(entities, dict):
            invalid_types.append("entities")
            issues.append("entities must be an object")
            return 0.5
        
        score = 1.0
        
        if "company" not in entities:
            missing_fields.append("entities.company")
            issues.append("Missing company information in entities")
            score -= 0.2
        elif not isinstance(entities["company"], dict):
            invalid_types.append("entities.company")
            issues.append("entities.company must be an object")
            score -= 0.1
        elif "name" not in entities["company"]:
            missing_fields.append("entities.company.name")
            issues.append("Missing company name in entities")
            score -= 0.1
        elif not entities["company"]["name"]:
            issues.append("Company name is empty")
            score -= 0.05
        
        return score
    
    def _validate_facts_section(self, facts: Any, issues: List[str], missing_fields: List[str], invalid_types: List[str]) -> float:
        """Validate financial facts section"""
        if not isinstance(facts, dict):
            invalid_types.append("facts")
            issues.append("facts must be an object")
            return 0.3
        
        score = 1.0
        required_fact_fields = ["years", "revenue_usd_m", "ebitda_usd_m", "ebitda_margins"]
        
        for field in required_fact_fields:
            if field not in facts:
                missing_fields.append(f"facts.{field}")
                issues.append(f"Missing financial data: {field}")
                score -= 0.1
            elif not isinstance(facts[field], list):
                invalid_types.append(f"facts.{field}")
                issues.append(f"facts.{field} must be an array")
                score -= 0.08
            elif len(facts[field]) == 0:
                issues.append(f"facts.{field} is empty")
                score -= 0.05
        
        # Check data consistency
        if all(field in facts and isinstance(facts[field], list) for field in required_fact_fields):
            lengths = [len(facts[field]) for field in required_fact_fields]
            if len(set(lengths)) > 1:
                issues.append("Financial data arrays have inconsistent lengths")
                score -= 0.1
        
        return score
    
    def _validate_management_team(self, mgmt: Any, issues: List[str], missing_fields: List[str], invalid_types: List[str]) -> float:
        """Validate management team structure"""
        if not isinstance(mgmt, dict):
            invalid_types.append("management_team")
            issues.append("management_team must be an object")
            return 0.3
        
        score = 1.0
        required_columns = ["left_column_profiles", "right_column_profiles"]
        
        for column in required_columns:
            if column not in mgmt:
                missing_fields.append(f"management_team.{column}")
                issues.append(f"Missing management team column: {column}")
                score -= 0.15
            elif not isinstance(mgmt[column], list):
                invalid_types.append(f"management_team.{column}")
                issues.append(f"management_team.{column} must be an array")
                score -= 0.1
            else:
                # Validate individual profiles
                for i, profile in enumerate(mgmt[column]):
                    profile_score = self._validate_management_profile(profile, f"{column}[{i}]", issues, invalid_types)
                    score *= profile_score
        
        return score
    
    def _validate_management_profile(self, profile: Any, path: str, issues: List[str], invalid_types: List[str]) -> float:
        """Validate individual management profile"""
        if not isinstance(profile, dict):
            invalid_types.append(path)
            issues.append(f"{path} must be an object")
            return 0.5
        
        score = 1.0
        required_profile_fields = ["name", "role_title", "experience_bullets"]
        
        for field in required_profile_fields:
            if field not in profile:
                issues.append(f"Missing {field} in {path}")
                score -= 0.1
            elif field == "experience_bullets":
                if not isinstance(profile[field], list):
                    invalid_types.append(f"{path}.{field}")
                    issues.append(f"{path}.experience_bullets must be an array")
                    score -= 0.08
                elif len(profile[field]) < 3:
                    issues.append(f"{path}.experience_bullets should have at least 3 items")
                    score -= 0.05
            elif not profile[field]:
                issues.append(f"{path}.{field} is empty")
                score -= 0.05
        
        return score
    
    def _validate_buyers_section(self, buyers: Any, buyer_type: str, issues: List[str], invalid_types: List[str]) -> float:
        """Validate strategic or financial buyers section"""
        if not isinstance(buyers, list):
            invalid_types.append(f"{buyer_type}_buyers")
            issues.append(f"{buyer_type}_buyers must be an array")
            return 0.3
        
        if len(buyers) == 0:
            issues.append(f"{buyer_type}_buyers is empty")
            return 0.5
        
        score = 1.0
        required_buyer_fields = ["buyer_name", "description", "strategic_rationale", "key_synergies", "fit", "financial_capacity"]
        
        for i, buyer in enumerate(buyers):
            if not isinstance(buyer, dict):
                invalid_types.append(f"{buyer_type}_buyers[{i}]")
                issues.append(f"{buyer_type}_buyers[{i}] must be an object")
                score -= 0.1
                continue
            
            for field in required_buyer_fields:
                if field not in buyer:
                    issues.append(f"Missing {field} in {buyer_type}_buyers[{i}]")
                    score -= 0.05
                elif not buyer[field]:
                    issues.append(f"{buyer_type}_buyers[{i}].{field} is empty")
                    score -= 0.02
        
        return score
    
    def _validate_competitive_analysis(self, comp: Any, issues: List[str], invalid_types: List[str]) -> float:
        """Validate competitive analysis section"""
        if not isinstance(comp, dict):
            invalid_types.append("competitive_analysis")
            issues.append("competitive_analysis must be an object")
            return 0.3
        
        score = 1.0
        required_comp_fields = ["competitors", "assessment", "barriers", "advantages"]
        
        for field in required_comp_fields:
            if field not in comp:
                issues.append(f"Missing competitive_analysis.{field}")
                score -= 0.1
            elif field == "competitors" and not isinstance(comp[field], list):
                invalid_types.append(f"competitive_analysis.{field}")
                issues.append("competitive_analysis.competitors must be an array")
                score -= 0.08
            elif field == "assessment" and not isinstance(comp[field], list):
                invalid_types.append(f"competitive_analysis.{field}")
                issues.append("competitive_analysis.assessment must be an array")
                score -= 0.08
        
        return score
    
    def _validate_precedent_transactions(self, prec: Any, issues: List[str], invalid_types: List[str]) -> float:
        """Validate precedent transactions section"""
        if not isinstance(prec, list):
            invalid_types.append("precedent_transactions")
            issues.append("precedent_transactions must be an array")
            return 0.3
        
        if len(prec) == 0:
            issues.append("precedent_transactions is empty")
            return 0.5
        
        score = 1.0
        required_transaction_fields = ["target", "acquirer", "date", "country", "enterprise_value", "revenue", "ev_revenue_multiple"]
        
        for i, transaction in enumerate(prec):
            if not isinstance(transaction, dict):
                invalid_types.append(f"precedent_transactions[{i}]")
                issues.append(f"precedent_transactions[{i}] must be an object")
                score -= 0.08
                continue
            
            for field in required_transaction_fields:
                if field not in transaction:
                    issues.append(f"Missing {field} in precedent_transactions[{i}]")
                    score -= 0.02
        
        return score
    
    def _validate_slides_array(self, slides: List[Any], issues: List[str], invalid_types: List[str]) -> float:
        """Validate slides array in render plan"""
        score = 1.0
        
        for i, slide in enumerate(slides):
            if not isinstance(slide, dict):
                invalid_types.append(f"slides[{i}]")
                issues.append(f"slides[{i}] must be an object")
                score -= 0.05
                continue
            
            # Check required slide fields
            if "template" not in slide:
                issues.append(f"Missing template in slides[{i}]")
                score -= 0.03
            elif not slide["template"]:
                issues.append(f"slides[{i}].template is empty")
                score -= 0.02
            
            if "data" not in slide:
                issues.append(f"Missing data in slides[{i}]")
                score -= 0.03
            elif not isinstance(slide["data"], dict):
                invalid_types.append(f"slides[{i}].data")
                issues.append(f"slides[{i}].data must be an object")
                score -= 0.02
        
        return score
    
    def _generate_content_ir_suggestions(self, issues: List[str], missing_fields: List[str], empty_fields: List[str]) -> List[str]:
        """Generate helpful suggestions for Content IR improvements"""
        suggestions = []
        
        if missing_fields:
            suggestions.append("Add all missing required sections: " + ", ".join(missing_fields))
        
        if empty_fields:
            suggestions.append("Populate empty sections with relevant data: " + ", ".join(empty_fields))
        
        if any("management_team" in issue for issue in issues):
            suggestions.append("Ensure management team has 2-4 profiles with names, titles, and 3+ experience bullets each")
        
        if any("buyer" in issue for issue in issues):
            suggestions.append("Include 3-5 strategic and financial buyers with complete profiles (name, description, rationale, synergies, fit)")
        
        if any("financial" in issue or "facts" in issue for issue in issues):
            suggestions.append("Provide consistent financial data arrays (years, revenue, EBITDA, margins) with matching lengths")
        
        return suggestions
    
    def _generate_render_plan_suggestions(self, issues: List[str], missing_fields: List[str], empty_fields: List[str]) -> List[str]:
        """Generate helpful suggestions for Render Plan improvements"""
        suggestions = []
        
        if "slides" in missing_fields:
            suggestions.append("Add 'slides' array as the root container for all slide definitions")
        
        if any("template" in issue for issue in issues):
            suggestions.append("Ensure each slide has a valid 'template' field specifying the slide type")
        
        if any("data" in issue for issue in issues):
            suggestions.append("Each slide must have a 'data' object containing the slide content")
        
        if len(issues) > 5:
            suggestions.append("Consider using the perfect render plan template as a reference for proper structure")
        
        return suggestions
    
    def auto_refine_json(self, json_data: Dict[str, Any], json_type: str, interview_data: Optional[Dict] = None) -> Tuple[Dict[str, Any], ValidationResult, int]:
        """
        Automatically refine JSON using LLM until it meets perfection standards
        Returns: (refined_json, final_validation_result, attempts_made)
        """
        attempts = 0
        current_json = copy.deepcopy(json_data)
        
        print(f"🔄 [JSON REFINER] Starting auto-refinement for {json_type}")
        
        while attempts < self.max_refinement_attempts:
            attempts += 1
            
            # Validate current JSON
            if json_type == "content_ir":
                validation = self.validate_content_ir(current_json)
            elif json_type == "render_plan":
                validation = self.validate_render_plan(current_json)
            else:
                raise ValueError(f"Unknown JSON type: {json_type}")
            
            print(f"📊 [JSON REFINER] Attempt {attempts}: Score {validation.score:.2f}, Issues: {len(validation.issues)}")
            
            # Check if we've achieved perfection
            if validation.score >= self.perfect_score_threshold:
                print(f"✅ [JSON REFINER] Perfect JSON achieved in {attempts} attempts!")
                return current_json, validation, attempts
            
            # If not perfect, generate refinement prompt and call LLM
            if attempts < self.max_refinement_attempts:
                try:
                    current_json = self._llm_refine_json(current_json, validation, json_type, interview_data)
                except Exception as e:
                    print(f"❌ [JSON REFINER] LLM refinement failed: {str(e)}")
                    break
        
        print(f"⚠️ [JSON REFINER] Max attempts reached. Final score: {validation.score:.2f}")
        return current_json, validation, attempts
    
    def _llm_refine_json(self, json_data: Dict[str, Any], validation: ValidationResult, json_type: str, interview_data: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Use LLM to refine JSON based on validation results
        This integrates with the Streamlit app's LLM infrastructure
        """
        # Use the same LLM calling method as the main app
        
        # Get perfect template for reference
        if json_type == "content_ir":
            perfect_template = self.perfect_content_ir_template
            template_name = "Content IR"
        else:
            perfect_template = self.perfect_render_plan_template
            template_name = "Render Plan"
        
        # Create refinement prompt
        refinement_prompt = self._create_refinement_prompt(
            json_data, validation, perfect_template, template_name, interview_data
        )
        
        # Call LLM to refine JSON using Streamlit session state for API credentials
        try:
            import streamlit as st
            
            # Get API credentials from Streamlit session
            api_key = st.session_state.get('api_key')
            selected_model = st.session_state.get('model', 'llama-3.1-sonar-large-128k-online')
            api_service = st.session_state.get('api_service', 'perplexity')
            
            if not api_key:
                print("❌ [JSON REFINER] No API key available")
                return json_data
            
            # Import the LLM calling function from the main app
            import sys
            import os
            sys.path.append(os.path.dirname(os.path.abspath(__file__)))
            
            # Use direct API calls similar to brand_extractor.py
            if api_service == "perplexity":
                refined_json_str = self._call_perplexity_for_refinement(refinement_prompt, api_key, selected_model)
            else:
                print(f"❌ [JSON REFINER] Unsupported API service: {api_service}")
                return json_data
                
            if refined_json_str:
                refined_json = json.loads(refined_json_str)
                print(f"✅ [JSON REFINER] Successfully refined JSON with LLM")
                return refined_json
            else:
                print(f"❌ [JSON REFINER] Empty response from LLM")
                return json_data
                
        except Exception as e:
            print(f"❌ [JSON REFINER] LLM call failed: {str(e)}")
            return json_data  # Return original if refinement fails
    
    def _call_perplexity_for_refinement(self, prompt: str, api_key: str, model: str) -> str:
        """Call Perplexity API for JSON refinement"""
        import requests
        
        try:
            url = "https://api.perplexity.ai/chat/completions"
            
            messages = [
                {"role": "system", "content": "You are a JSON refinement specialist. Return ONLY valid JSON, no explanation or formatting."},
                {"role": "user", "content": prompt}
            ]
            
            payload = {
                "model": model,
                "messages": messages,
                "temperature": 0.1,  # Low temperature for consistency
                "max_tokens": 8000,
                "stream": False
            }
            
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json; charset=utf-8"
            }
            
            response = requests.post(url, json=payload, headers=headers, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
                
                # Extract JSON from response if it's wrapped in explanations
                start_idx = content.find('{')
                end_idx = content.rfind('}')
                if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                    json_content = content[start_idx:end_idx+1]
                    return json_content
                else:
                    return content
            else:
                print(f"❌ [JSON REFINER] Perplexity API Error: {response.status_code}")
                return ""
                
        except Exception as e:
            print(f"❌ [JSON REFINER] Perplexity call failed: {str(e)}")
            return ""
    
    def _create_refinement_prompt(self, json_data: Dict[str, Any], validation: ValidationResult, 
                                perfect_template: Dict[str, Any], template_name: str, 
                                interview_data: Optional[Dict] = None) -> str:
        """Create detailed refinement prompt for LLM"""
        
        prompt = f"""You are an expert JSON refinement specialist. Your task is to fix and perfect a {template_name} JSON.

CURRENT JSON VALIDATION SCORE: {validation.score:.2f}/1.0
TARGET SCORE: {self.perfect_score_threshold}/1.0

ISSUES FOUND:
{chr(10).join([f"• {issue}" for issue in validation.issues[:10]])}

MISSING FIELDS:
{chr(10).join([f"• {field}" for field in validation.missing_fields[:10]])}

EMPTY FIELDS:
{chr(10).join([f"• {field}" for field in validation.empty_fields[:10]])}

SUGGESTIONS:
{chr(10).join([f"• {suggestion}" for suggestion in validation.suggestions[:5]])}

PERFECT TEMPLATE REFERENCE:
```json
{json.dumps(perfect_template, indent=2)[:3000]}...
```

CURRENT JSON TO FIX:
```json
{json.dumps(json_data, indent=2)}
```
"""

        if interview_data:
            prompt += f"""
ADDITIONAL INTERVIEW DATA (use to fill missing information):
```json
{json.dumps(interview_data, indent=2)[:2000]}...
```
"""

        prompt += f"""
INSTRUCTIONS:
1. Fix ALL validation issues identified above
2. Ensure NO fields are missing or empty
3. Follow the EXACT structure of the perfect template
4. Use interview data to fill any missing information
5. Maintain high-quality, professional content
6. Return ONLY the corrected JSON, no explanation

CRITICAL REQUIREMENTS:
- Every required field must be present and populated
- Arrays must have appropriate number of items (3-5 for buyers, etc.)
- Management team profiles must have names, titles, and 3+ experience bullets
- Financial data arrays must have consistent lengths
- All text must be professional and detailed
- Follow the exact schema structure from the perfect template

Return the perfected JSON now:"""

        return prompt

    def integrate_interview_data(self, base_json: Dict[str, Any], interview_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Intelligently integrate interview data to fill missing fields in JSON
        """
        enhanced_json = copy.deepcopy(base_json)
        
        try:
            # Extract company name
            if "company_info" in interview_data:
                if "entities" not in enhanced_json:
                    enhanced_json["entities"] = {"company": {}}
                if "company" not in enhanced_json["entities"]:
                    enhanced_json["entities"]["company"] = {}
                
                enhanced_json["entities"]["company"]["name"] = interview_data["company_info"].get("name", "")
            
            # Enhance business description
            if "business_overview_data" in enhanced_json and "company_description" in interview_data:
                enhanced_json["business_overview_data"]["description"] = interview_data["company_description"]
            
            # Add financial data if available
            if "financials" in interview_data and "facts" in enhanced_json:
                financials = interview_data["financials"]
                if "revenue" in financials:
                    enhanced_json["facts"]["revenue_usd_m"] = financials["revenue"]
                if "years" in financials:
                    enhanced_json["facts"]["years"] = financials["years"]
            
            # Enhance management team with interview details
            if "management" in interview_data and "management_team" in enhanced_json:
                self._integrate_management_data(enhanced_json["management_team"], interview_data["management"])
            
            print("✅ [JSON INTEGRATOR] Interview data successfully integrated")
            
        except Exception as e:
            print(f"❌ [JSON INTEGRATOR] Integration failed: {str(e)}")
        
        return enhanced_json
    
    def _integrate_management_data(self, mgmt_section: Dict[str, Any], interview_mgmt: Dict[str, Any]):
        """Integrate interview management data"""
        # This would intelligently map interview data to management profiles
        # Implementation depends on your interview data structure
        pass

    def get_validation_report(self, json_data: Dict[str, Any], json_type: str) -> str:
        """Generate a beautiful validation report"""
        if json_type == "content_ir":
            validation = self.validate_content_ir(json_data)
        else:
            validation = self.validate_render_plan(json_data)
        
        score_emoji = "🟢" if validation.score >= 0.9 else "🟡" if validation.score >= 0.7 else "🔴"
        
        report = f"""
{score_emoji} JSON VALIDATION REPORT - {json_type.upper()}
{'='*50}
Overall Score: {validation.score:.2f}/1.0
Status: {'✅ PERFECT' if validation.is_valid and validation.score >= self.perfect_score_threshold else '⚠️ NEEDS IMPROVEMENT' if validation.is_valid else '❌ INVALID'}

📊 METRICS:
• Issues Found: {len(validation.issues)}
• Missing Fields: {len(validation.missing_fields)}
• Invalid Types: {len(validation.invalid_types)}
• Empty Fields: {len(validation.empty_fields)}

❗ TOP ISSUES:
{chr(10).join([f"  • {issue}" for issue in validation.issues[:5]])}

🔧 RECOMMENDATIONS:
{chr(10).join([f"  • {suggestion}" for suggestion in validation.suggestions[:3]])}
"""
        return report


# Integration function for your main application
def validate_and_perfect_json(json_data: Dict[str, Any], json_type: str, interview_data: Optional[Dict] = None) -> Tuple[Dict[str, Any], bool]:
    """
    Main function to validate and perfect JSON automatically
    Returns: (perfected_json, is_perfect)
    """
    validator = JSONValidatorPerfector()
    
    print(f"🚀 [JSON PERFECTER] Starting validation and refinement for {json_type}")
    
    # Get interview data from Streamlit session if not provided
    if interview_data is None:
        try:
            import streamlit as st
            # Extract interview data from conversation messages
            if hasattr(st.session_state, 'messages') and st.session_state.messages:
                interview_data = extract_interview_data_from_messages(st.session_state.messages)
        except:
            pass  # No Streamlit context or messages available
    
    # First, integrate any available interview data
    if interview_data:
        json_data = validator.integrate_interview_data(json_data, interview_data)
    
    # Auto-refine until perfect
    perfected_json, final_validation, attempts = validator.auto_refine_json(json_data, json_type, interview_data)
    
    # Generate final report
    report = validator.get_validation_report(perfected_json, json_type)
    print(report)
    
    is_perfect = final_validation.score >= validator.perfect_score_threshold
    
    return perfected_json, is_perfect

def extract_interview_data_from_messages(messages: List[Dict]) -> Dict[str, Any]:
    """Extract structured interview data from conversation messages"""
    interview_data = {}
    
    try:
        # Combine all message content for analysis
        conversation_text = " ".join([msg.get("content", "") for msg in messages if msg.get("role") != "system"])
        
        # Simple extraction patterns (can be enhanced)
        import re
        
        # Extract company name
        company_patterns = [
            r"company(?:\s+name)?\s+is\s+([^.!?]+)",
            r"(?:we|our company)\s+(?:is\s+)?([A-Z][A-Za-z\s]+?)(?:\s+(?:is|was|does|provides))",
            r"I work at\s+([A-Z][A-Za-z\s]+)",
        ]
        
        for pattern in company_patterns:
            match = re.search(pattern, conversation_text, re.IGNORECASE)
            if match:
                company_name = match.group(1).strip()
                if len(company_name) < 50:  # Reasonable company name length
                    interview_data["company_info"] = {"name": company_name}
                    break
        
        # Extract business description
        desc_patterns = [
            r"(?:company|business|we)\s+(?:does|provides|offers|specializes in)\s+([^.!?]+)",
            r"our business is\s+([^.!?]+)",
        ]
        
        for pattern in desc_patterns:
            match = re.search(pattern, conversation_text, re.IGNORECASE)
            if match:
                description = match.group(1).strip()
                if len(description) > 10:
                    interview_data["company_description"] = description
                    break
        
        # Extract financial information
        revenue_patterns = [
            r"revenue(?:\s+is)?\s+(?:about\s+)?\$?([0-9.]+)(?:\s*(?:million|m|billion|b))?",
            r"\$([0-9.]+)(?:\s*(?:million|m|billion|b))?\s+in\s+revenue",
        ]
        
        for pattern in revenue_patterns:
            matches = re.findall(pattern, conversation_text, re.IGNORECASE)
            if matches:
                try:
                    revenue_values = [float(match) for match in matches[:5]]  # Take first 5 values
                    interview_data["financials"] = {"revenue": revenue_values}
                    break
                except:
                    pass
        
        print(f"📊 [INTERVIEW EXTRACTOR] Extracted data keys: {list(interview_data.keys())}")
        
    except Exception as e:
        print(f"❌ [INTERVIEW EXTRACTOR] Failed to extract interview data: {str(e)}")
    
    return interview_data


if __name__ == "__main__":
    # Test the validator
    validator = JSONValidatorPerfector()
    
    # Test with a simple incomplete JSON
    test_json = {
        "entities": {"company": {"name": "TestCorp"}},
        "facts": {"years": [2023], "revenue_usd_m": [10]},
        "management_team": {"left_column_profiles": []}
    }
    
    result = validator.validate_content_ir(test_json)
    print(validator.get_validation_report(test_json, "content_ir"))