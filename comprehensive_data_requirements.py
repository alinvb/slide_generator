#!/usr/bin/env python3
"""
Comprehensive Data Requirements Mapping
Maps all required fields for complete investment banking analysis
"""

# Complete field requirements based on slide templates and working examples
REQUIRED_FIELDS_MAPPING = {
    # CORE COMPANY DATA
    "entities": {
        "company": {
            "name": "REQUIRED - Company name from conversation or user input"
        }
    },
    
    # FINANCIAL DATA  
    "facts": {
        "years": "REQUIRED - Financial years array [2020, 2021, 2022, 2023, 2024E]",
        "revenue_usd_m": "REQUIRED - Revenue figures in USD millions",
        "ebitda_usd_m": "REQUIRED - EBITDA figures in USD millions", 
        "ebitda_margins": "REQUIRED - EBITDA margin percentages"
    },
    
    # MANAGEMENT TEAM (for slide 4)
    "management_team": {
        "left_column_profiles": "REQUIRED - 2-3 executive profiles",
        "right_column_profiles": "REQUIRED - 2-3 executive profiles"
    },
    
    # BUSINESS OVERVIEW (for slide 1)
    "business_overview_data": {
        "description": "REQUIRED - Company business description",
        "timeline": "REQUIRED - Start year and end year",
        "highlights": "REQUIRED - 3-5 key business highlights",
        "services": "REQUIRED - Core services/products list",
        "positioning_desc": "REQUIRED - Market positioning description"
    },
    
    # PRODUCT & SERVICE FOOTPRINT (for slide 2)
    "product_service_data": {
        "services": "REQUIRED - Detailed service descriptions",
        "coverage_table": "REQUIRED - Geographic/market coverage matrix",
        "metrics": "REQUIRED - Key business metrics"
    },
    
    # GROWTH STRATEGY (for slide 5)  
    "growth_strategy_data": {
        "growth_strategy": {
            "strategies": "REQUIRED - Growth strategy initiatives"
        },
        "financial_projections": {
            "categories": "REQUIRED - Future years",
            "revenue": "REQUIRED - Projected revenue",
            "ebitda": "REQUIRED - Projected EBITDA"
        }
    },
    
    # COMPETITIVE POSITIONING (for slide 6)
    "competitive_analysis": {
        "competitors": "REQUIRED - Competitor list with revenue",
        "assessment": "REQUIRED - Competitive assessment matrix",
        "barriers": "REQUIRED - Competitive barriers/moats",
        "advantages": "REQUIRED - Competitive advantages"
    },
    
    # PRECEDENT TRANSACTIONS (for slide 7)
    "precedent_transactions": "REQUIRED - List of comparable transactions",
    
    # VALUATION OVERVIEW (for slide 8)
    "valuation_data": "REQUIRED - Valuation methodologies and ranges",
    
    # STRATEGIC BUYERS (for slide 9)
    "strategic_buyers": "REQUIRED - Strategic buyer profiles with rationale",
    
    # FINANCIAL BUYERS (for slide 10) 
    "financial_buyers": "REQUIRED - Financial buyer profiles with rationale",
    
    # SEA CONGLOMERATES (for slide 11)
    "sea_conglomerates": "REQUIRED - Regional conglomerate profiles",
    
    # MARGIN & COST RESILIENCE (for slide 12)
    "margin_cost_data": {
        "chart_data": "REQUIRED - Margin trend data",
        "cost_management": "REQUIRED - Cost management initiatives", 
        "risk_mitigation": "REQUIRED - Risk mitigation strategies"
    },
    
    # INVESTOR CONSIDERATIONS (for slide 13)
    "investor_considerations": {
        "considerations": "REQUIRED - Investment considerations",
        "mitigants": "REQUIRED - Risk mitigants"
    },
    
    # INVESTOR PROCESS OVERVIEW (for slide 14)
    "investor_process_data": {
        "diligence_topics": "REQUIRED - Due diligence topics",
        "synergy_opportunities": "REQUIRED - Synergy opportunities",
        "risk_factors": "REQUIRED - Risk factors",
        "mitigants": "REQUIRED - Risk mitigants",
        "timeline": "REQUIRED - Deal process timeline"
    }
}

# Field priority levels for gap-filling
FIELD_PRIORITY_LEVELS = {
    "CRITICAL": [
        "entities.company.name",
        "facts.revenue_usd_m", 
        "facts.ebitda_usd_m",
        "facts.years",
        "business_overview_data.description"
    ],
    
    "HIGH": [
        "management_team.left_column_profiles",
        "management_team.right_column_profiles", 
        "strategic_buyers",
        "financial_buyers",
        "competitive_analysis.competitors",
        "precedent_transactions",
        "valuation_data"
    ],
    
    "MEDIUM": [
        "product_service_data.services",
        "growth_strategy_data.growth_strategy.strategies",
        "competitive_analysis.assessment",
        "margin_cost_data.chart_data",
        "investor_considerations.considerations"
    ],
    
    "LOW": [
        "sea_conglomerates",
        "investor_process_data.timeline",
        "business_overview_data.highlights",
        "product_service_data.metrics"
    ]
}

# Minimum data quality thresholds
QUALITY_THRESHOLDS = {
    "management_team_profiles": {"min_count": 4, "min_bullets_per_profile": 3},
    "strategic_buyers": {"min_count": 3, "required_fields": ["buyer_name", "description", "strategic_rationale"]},
    "financial_buyers": {"min_count": 3, "required_fields": ["buyer_name", "description", "strategic_rationale"]},
    "precedent_transactions": {"min_count": 3, "required_fields": ["target", "acquirer", "enterprise_value"]},
    "valuation_data": {"min_count": 3, "required_fields": ["methodology", "enterprise_value"]},
    "competitive_analysis.competitors": {"min_count": 3, "required_fields": ["name", "revenue"]},
    "revenue_data_points": {"min_count": 5, "required_years": ["2020", "2021", "2022", "2023", "2024E"]}
}

def get_missing_critical_fields(data: dict) -> list:
    """Identify missing critical fields that must be filled"""
    missing = []
    
    for field_path in FIELD_PRIORITY_LEVELS["CRITICAL"]:
        if not _get_nested_field(data, field_path):
            missing.append(field_path)
    
    return missing

def get_missing_high_priority_fields(data: dict) -> list:
    """Identify missing high priority fields"""
    missing = []
    
    for field_path in FIELD_PRIORITY_LEVELS["HIGH"]:
        if not _get_nested_field(data, field_path):
            missing.append(field_path)
    
    return missing

def validate_data_quality(data: dict) -> dict:
    """Validate data quality against thresholds"""
    validation_results = {
        "passed": [],
        "failed": [],
        "warnings": []
    }
    
    for field, thresholds in QUALITY_THRESHOLDS.items():
        field_data = _get_nested_field(data, field)
        
        if not field_data:
            validation_results["failed"].append(f"{field}: Missing entirely")
            continue
            
        if "min_count" in thresholds:
            if isinstance(field_data, list) and len(field_data) < thresholds["min_count"]:
                validation_results["failed"].append(f"{field}: Only {len(field_data)} items, need {thresholds['min_count']}")
            else:
                validation_results["passed"].append(f"{field}: Count OK ({len(field_data)} items)")
                
        if "required_fields" in thresholds and isinstance(field_data, list):
            for item in field_data:
                if isinstance(item, dict):
                    missing_fields = [f for f in thresholds["required_fields"] if not item.get(f)]
                    if missing_fields:
                        validation_results["warnings"].append(f"{field} item missing: {missing_fields}")
    
    return validation_results

def _get_nested_field(data: dict, field_path: str):
    """Get nested field value using dot notation"""
    keys = field_path.split('.')
    current = data
    
    try:
        for key in keys:
            current = current[key]
        return current
    except (KeyError, TypeError):
        return None

def get_comprehensive_field_template() -> dict:
    """Return complete field template for gap-filling"""
    return {
        "entities": {"company": {"name": "[COMPANY_NAME]"}},
        "facts": {
            "years": ["2020", "2021", "2022", "2023", "2024E"],
            "revenue_usd_m": "[REVENUE_DATA]",
            "ebitda_usd_m": "[EBITDA_DATA]", 
            "ebitda_margins": "[MARGIN_DATA]"
        },
        "management_team": {
            "left_column_profiles": "[MANAGEMENT_PROFILES_LEFT]",
            "right_column_profiles": "[MANAGEMENT_PROFILES_RIGHT]"
        },
        "business_overview_data": {
            "description": "[BUSINESS_DESCRIPTION]",
            "timeline": {"start_year": "[START_YEAR]", "end_year": "[END_YEAR]"},
            "highlights": "[BUSINESS_HIGHLIGHTS]",
            "services": "[CORE_SERVICES]",
            "positioning_desc": "[MARKET_POSITIONING]"
        },
        "product_service_data": {
            "services": "[SERVICE_DETAILS]",
            "coverage_table": "[COVERAGE_MATRIX]",
            "metrics": "[KEY_METRICS]"
        },
        "growth_strategy_data": {
            "growth_strategy": {"strategies": "[GROWTH_STRATEGIES]"},
            "financial_projections": {
                "categories": "[FUTURE_YEARS]",
                "revenue": "[REVENUE_PROJECTIONS]", 
                "ebitda": "[EBITDA_PROJECTIONS]"
            }
        },
        "competitive_analysis": {
            "competitors": "[COMPETITOR_LIST]",
            "assessment": "[COMPETITIVE_ASSESSMENT]",
            "barriers": "[COMPETITIVE_BARRIERS]",
            "advantages": "[COMPETITIVE_ADVANTAGES]"
        },
        "precedent_transactions": "[PRECEDENT_TRANSACTIONS]",
        "valuation_data": "[VALUATION_METHODS]",
        "strategic_buyers": "[STRATEGIC_BUYER_PROFILES]",
        "financial_buyers": "[FINANCIAL_BUYER_PROFILES]", 
        "sea_conglomerates": "[REGIONAL_CONGLOMERATES]",
        "margin_cost_data": {
            "chart_data": "[MARGIN_TRENDS]",
            "cost_management": "[COST_INITIATIVES]",
            "risk_mitigation": "[RISK_STRATEGIES]"
        },
        "investor_considerations": {
            "considerations": "[INVESTMENT_CONSIDERATIONS]",
            "mitigants": "[RISK_MITIGANTS]" 
        },
        "investor_process_data": {
            "diligence_topics": "[DD_TOPICS]",
            "synergy_opportunities": "[SYNERGIES]",
            "risk_factors": "[RISK_FACTORS]",
            "mitigants": "[MITIGANTS]",
            "timeline": "[DEAL_TIMELINE]"
        }
    }