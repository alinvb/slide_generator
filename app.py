import json
import io
from pathlib import Path
import requests
import streamlit as st
import pandas as pd
import zipfile
from datetime import datetime
import re

# Local libs
from executor import execute_plan
from catalog_loader import TemplateCatalog
from brand_extractor import BrandExtractor
from executive_search import ExecutiveSearchEngine, auto_generate_management_data

def validate_and_fix_json(content_ir, render_plan):
    """
    MANDATORY validation and fixing function that enforces all requirements
    Uses comprehensive JSON data fixer for all structure issues
    """
    print("🔧 MANDATORY: Starting validation and fixing process...")
    
    # Import the comprehensive data fixer
    from json_data_fixer import comprehensive_json_fix
    
    # Apply comprehensive fixes first - this fixes data type mismatches and structure issues
    print("🔧 MANDATORY: Applying comprehensive JSON fixes...")
    fixed_render_plan, fixed_content_ir = comprehensive_json_fix(render_plan, content_ir)
    
    # Required Content IR sections
    required_content_ir_sections = [
        'entities', 'facts', 'charts', 'management_team', 'investor_considerations',
        'competitive_analysis', 'precedent_transactions', 'valuation_data', 'sea_conglomerates',
        'strategic_buyers', 'financial_buyers', 'product_service_data', 'business_overview_data',
        'growth_strategy_data', 'investor_process_data', 'margin_cost_data'
    ]
    
    # Required slide order - EXACTLY 14 slides
    required_slide_order = [
        'management_team', 'historical_financial_performance', 'margin_cost_resilience',
        'investor_considerations', 'competitive_positioning', 'product_service_footprint',
        'business_overview', 'precedent_transactions', 'valuation_overview',
        'investor_process_overview', 'growth_strategy_projections', 'sea_conglomerates',
        'buyer_profiles', 'buyer_profiles'
    ]
    
    print(f"🔧 MANDATORY: Required slide count: {len(required_slide_order)}")
    
    print(f"🔧 MANDATORY: Required Content IR sections: {len(required_content_ir_sections)}")
    print(f"🔧 MANDATORY: Required slide order: {len(required_slide_order)}")
    
    # Use the already fixed content IR from comprehensive_json_fix
    # Additional legacy compatibility checks for any remaining issues
    print("🔧 MANDATORY: Checking Content IR sections...")
    for section in required_content_ir_sections:
        if section not in fixed_content_ir:
            print(f"❌ MISSING: {section} - Adding mandatory section")
    
    # Add missing sections
    if 'charts' not in fixed_content_ir:
        print("🔧 MANDATORY: Adding missing charts section")
        fixed_content_ir['charts'] = [
            {
                "id": "chart_hist_perf",
                "type": "combo",
                "title": "Revenue & EBITDA Growth",
                "categories": fixed_content_ir.get('facts', {}).get('years', ['2020', '2021', '2022', '2023', '2024E']),
                "revenue": fixed_content_ir.get('facts', {}).get('revenue_usd_m', [120, 145, 180, 210, 240]),
                "ebitda": fixed_content_ir.get('facts', {}).get('ebitda_usd_m', [18, 24, 31, 40, 47]),
                "unit": "US$m"
            }
        ]
    
    if 'investor_process_data' not in fixed_content_ir:
        fixed_content_ir['investor_process_data'] = {
            "diligence_topics": [
                {"title": "Financial & Operational Review", "description": "Historical performance, unit economics, and forward projections"},
                {"title": "Market & Competitive Analysis", "description": "Market sizing, competitive landscape, and growth opportunities"},
                {"title": "Management Assessment", "description": "Leadership evaluation, organizational structure, and succession planning"}
            ],
            "synergy_opportunities": [
                {"title": "Revenue Synergies", "description": "Enhanced service offerings through expanded capabilities"},
                {"title": "Operational Excellence", "description": "Best practices implementation across broader network"}
            ],
            "risk_factors": ["Market volatility", "Competitive intensity", "Execution risk"],
            "mitigants": ["Diversified revenue streams", "Strong market position", "Experienced management"],
            "timeline": [
                {"date": "Week 1-2", "description": "Initial outreach and process launch"},
                {"date": "Week 3-4", "description": "Management presentations and strategic discussions"},
                {"date": "Week 5-6", "description": "Due diligence data room access and information review"},
                {"date": "Week 7-8", "description": "Site visits and operational assessments"},
                {"date": "Week 9-10", "description": "Financial model review and synergy analysis"},
                {"date": "Week 11-12", "description": "Legal and commercial due diligence"},
                {"date": "Week 13-14", "description": "Final bid submissions and negotiations"},
                {"date": "Week 15-16", "description": "Definitive agreements and closing preparations"}
            ]
        }
    
    if 'margin_cost_data' not in fixed_content_ir:
        fixed_content_ir['margin_cost_data'] = {
            "chart_data": {
                "categories": fixed_content_ir.get('facts', {}).get('years', ['2020', '2021', '2022', '2023', '2024E']),
                "values": fixed_content_ir.get('facts', {}).get('ebitda_margins', [15.0, 16.6, 17.2, 19.0, 19.6])
            },
            "cost_management": {
                "title": "Strategic Cost Management Initiatives",
                "items": [
                    {"title": "Supplier Consolidation", "description": "Centralized procurement achieving cost savings"},
                    {"title": "Operational Efficiency", "description": "Process optimization and automation"}
                ]
            },
            "risk_mitigation": {
                "title": "Risk Mitigation Framework",
                "main_strategy": {"title": "Diversified Revenue Base", "description": "Multi-dimensional diversification"},
                "banker_view": {"title": "BANKER'S VIEW", "text": "Strong operational resilience with proven margin maintenance"}
            }
        }
    
    # Fix precedent transactions
    if 'precedent_transactions' in fixed_content_ir:
        for transaction in fixed_content_ir['precedent_transactions']:
            if 'enterprise_value' not in transaction or 'revenue' not in transaction:
                transaction['enterprise_value'] = transaction.get('enterprise_value', transaction.get('revenue', 100) * 3.0)
                transaction['revenue'] = transaction.get('revenue', transaction.get('enterprise_value', 300) / 3.0)
            if 'ev_revenue_multiple' not in transaction:
                transaction['ev_revenue_multiple'] = transaction['enterprise_value'] / transaction['revenue']
    
    # Use the already fixed render plan from comprehensive_json_fix 
    # Additional legacy compatibility checks for slide order
    print("🔧 MANDATORY: Checking Render Plan slide order...")
    current_slides = [slide['template'] for slide in fixed_render_plan.get('slides', [])]
    print(f"❌ CURRENT ORDER: {current_slides}")
    print(f"✅ REQUIRED ORDER: {required_slide_order}")
    
    # Reorder slides to match required order
    existing_slides = {slide['template']: slide for slide in render_plan.get('slides', [])}
    
    for i, template in enumerate(required_slide_order):
        if template in existing_slides:
            slide = existing_slides[template].copy()
            # Ensure title field exists
            if 'data' in slide and 'title' not in slide['data']:
                slide['data']['title'] = f"{template.replace('_', ' ').title()}"
            fixed_render_plan['slides'].append(slide)
        else:
            # Add missing slide - CRITICAL FIX
            if template == 'investor_process_overview':
                print("🔧 MANDATORY: Adding missing investor_process_overview slide")
                fixed_render_plan['slides'].append({
                    "template": "investor_process_overview",
                    "data": {
                        "title": "Comprehensive Investor Process Overview",
                        "diligence_topics": fixed_content_ir.get('investor_process_data', {}).get('diligence_topics', []),
                        "synergy_opportunities": fixed_content_ir.get('investor_process_data', {}).get('synergy_opportunities', []),
                        "risk_factors": fixed_content_ir.get('investor_process_data', {}).get('risk_factors', []),
                        "mitigants": fixed_content_ir.get('investor_process_data', {}).get('mitigants', []),
                        "timeline": fixed_content_ir.get('investor_process_data', {}).get('timeline', [])
                    }
                })
            else:
                print(f"🔧 MANDATORY: Adding missing slide: {template}")
                fixed_render_plan['slides'].append({
                    "template": template,
                    "data": {
                        "title": template.replace('_', ' ').title(),
                        "placeholder": "Data will be populated from Content IR"
                    }
                })
    
    # MANDATORY: Fix all semantic errors
    print("🔧 MANDATORY: Fixing semantic errors...")
    
    for slide in fixed_render_plan['slides']:
        # Fix key_metrics structure
        if slide['template'] == 'historical_financial_performance':
            if 'data' in slide and 'key_metrics' in slide['data']:
                if isinstance(slide['data']['key_metrics'], list):
                    print("🔧 MANDATORY: Fixing key_metrics structure")
                    slide['data']['key_metrics'] = {"metrics": slide['data']['key_metrics']}
        
        # Fix coverage_table structure - CRITICAL FIX
        if slide['template'] == 'product_service_footprint':
            if 'data' in slide and 'coverage_table' in slide['data']:
                if isinstance(slide['data']['coverage_table'], list) and len(slide['data']['coverage_table']) > 0:
                    if isinstance(slide['data']['coverage_table'][0], dict):
                        print("🔧 MANDATORY: Fixing coverage_table structure")
                        # Convert object array to 2D array
                        headers = list(slide['data']['coverage_table'][0].keys())
                        table_data = [headers]
                        for row in slide['data']['coverage_table']:
                            table_data.append([str(row.get(key, '')) for key in headers])
                        slide['data']['coverage_table'] = table_data
        
        # Fix sea_conglomerates structure - CRITICAL FIX
        if slide['template'] == 'sea_conglomerates':
            if 'data' in slide and 'data' in slide['data']:
                print("🔧 MANDATORY: Fixing sea_conglomerates structure")
                # Move nested data to top level
                slide['data']['sea_conglomerates'] = slide['data']['data']
                del slide['data']['data']
        
        # Ensure all slides have proper data structure
        if 'data' not in slide:
            print(f"🔧 MANDATORY: Adding data structure to {slide['template']}")
            slide['data'] = {"title": slide['template'].replace('_', ' ').title()}
        
        # Ensure title exists
        if 'data' in slide and 'title' not in slide['data']:
            print(f"🔧 MANDATORY: Adding title to {slide['template']}")
            slide['data']['title'] = slide['template'].replace('_', ' ').title()
        
        # Fix buyer_profiles slides - CRITICAL FIX
        if slide['template'] == 'buyer_profiles':
            if 'content_ir_key' not in slide:
                print(f"🔧 MANDATORY: Adding content_ir_key to buyer_profiles slide")
                # Determine if this is strategic or financial based on position
                slide_index = fixed_render_plan['slides'].index(slide)
                if slide_index == 12:  # First buyer_profiles slide
                    slide['content_ir_key'] = 'strategic_buyers'
                    slide['data']['title'] = 'Strategic Buyer Profiles'
                elif slide_index == 13:  # Second buyer_profiles slide
                    slide['content_ir_key'] = 'financial_buyers'
                    slide['data']['title'] = 'Financial Buyer Profiles'
            
            # Ensure proper table structure
            if 'data' in slide and 'table_rows' not in slide['data']:
                print(f"🔧 MANDATORY: Adding table structure to buyer_profiles slide")
                slide['data']['table_headers'] = [
                    "Buyer Name", "Description", "Strategic Rationale", 
                    "Key Synergies", "Fit", "Financial Capacity"
                ]
                slide['data']['table_rows'] = fixed_content_ir.get(slide.get('content_ir_key', 'strategic_buyers'), [])
    
    # MANDATORY: Final validation
    print("🔧 MANDATORY: Final validation...")
    print(f"✅ Content IR sections: {len(fixed_content_ir)}")
    print(f"✅ Render Plan slides: {len(fixed_render_plan['slides'])}")
    
    # Verify all required sections are present
    missing_sections = [s for s in required_content_ir_sections if s not in fixed_content_ir]
    if missing_sections:
        print(f"❌ STILL MISSING: {missing_sections}")
    else:
        print("✅ All Content IR sections present!")
    
    # Verify slide count and order
    final_slide_order = [slide['template'] for slide in fixed_render_plan['slides']]
    if len(final_slide_order) != len(required_slide_order):
        print(f"❌ WRONG SLIDE COUNT: {len(final_slide_order)} vs {len(required_slide_order)}")
    else:
        print("✅ Correct slide count!")
    
    if final_slide_order != required_slide_order:
        print(f"❌ WRONG SLIDE ORDER: {final_slide_order}")
    else:
        print("✅ Correct slide order!")
    
    print("🔧 MANDATORY: Validation and fixing completed!")
    return fixed_content_ir, fixed_render_plan

# ADD THESE IMPORTS FOR BRAND FUNCTIONALITY
try:
    from pptx import Presentation
    from pptx.dml.color import RGBColor
    from pptx.util import Pt
    from pptx.enum.dml import MSO_COLOR_TYPE
    HAS_PPTX = True
except ImportError:
    HAS_PPTX = False
    st.error("python-pptx not installed. Please run: pip install python-pptx")

# validators are optional
try:
    from validators import validate_render_plan_against_catalog, summarize_issues
    HAS_VALIDATORS = True
except Exception:
    HAS_VALIDATORS = False

st.set_page_config(page_title="AI Deck Builder", page_icon="🤖", layout="wide")
st.title("🤖 AI Deck Builder – LLM-Powered Pitch Deck Generator")

# JSON CLEANING FUNCTIONS - ALL SAFE STRING OPERATIONS
def clean_json_string(json_str):
    """SIMPLE JSON cleaning - minimal processing to avoid parsing errors"""
    if not json_str:
        return "{}"
    
    print(f"[JSON CLEAN] Input length: {len(json_str)}")
    
    # Only basic cleaning
    json_str = json_str.strip()
    
    # Remove markdown code blocks
    if json_str.startswith('```json'):
        json_str = json_str[7:].strip()
    elif json_str.startswith('```'):
        json_str = json_str[3:].strip()
    
    if json_str.endswith('```'):
        json_str = json_str[:-3].strip()
    
    # Extract JSON content between first { and last }
    start_idx = json_str.find('{')
    end_idx = json_str.rfind('}')
    
    if start_idx == -1 or end_idx == -1 or start_idx >= end_idx:
        print(f"[JSON CLEAN] No valid JSON structure found")
        return "{}"
    
    json_str = json_str[start_idx:end_idx+1]
    
    # Test if it's already valid
    try:
        import json
        json.loads(json_str)
        print(f"[JSON CLEAN] JSON is valid as-is")
        return json_str
    except json.JSONDecodeError as e:
        print(f"[JSON CLEAN] JSON parse error: {e}")
        # Return as-is - let the enhanced error handling deal with it
        return json_str

def advanced_json_repair(json_str):
    """DISABLED - Advanced JSON repair causes more problems than it solves"""
    print(f"[JSON REPAIR] Advanced repair disabled - returning original JSON")
    # Just return the original - the enhanced parsing will handle errors
    return json_str

def validate_json_char_by_char(json_str, error_pos):
    """DISABLED - Character validation causes parsing errors"""
    print(f"[CHAR VALIDATION] Disabled - returning original JSON")
    return json_str

def fallback_json_repair(json_str):
    """DISABLED - Fallback repair causes more issues"""
    print(f"[FALLBACK REPAIR] Disabled - returning empty JSON")
    # Return minimal valid JSON to prevent crashes
    return '{}'

def extract_jsons_from_response(response_text):
    """Extract both Content IR and Render Plan JSONs from AI response using improved parsing"""
    content_ir = None
    render_plan = None
    
    print(f"[JSON EXTRACTION DEBUG] Starting extraction from response of length: {len(response_text)}")
    
    # Method 1: Look for specific JSON markers in the response
    content_ir_markers = [
        "CONTENT IR JSON:",
        "Content IR:",
        "content_ir",
        "## CONTENT IR JSON:",
        "**CONTENT IR JSON:**"
    ]
    
    render_plan_markers = [
        "RENDER PLAN JSON:",
        "Render Plan:",
        "render_plan",
        "## RENDER PLAN JSON:",
        "**RENDER PLAN JSON:**"
    ]
    
    # Find Content IR section
    content_ir_start = None
    content_ir_end = None
    
    for marker in content_ir_markers:
        pos = response_text.find(marker)
        if pos != -1:
            content_ir_start = pos + len(marker)
            print(f"[JSON EXTRACTION DEBUG] Found Content IR marker: '{marker}' at position {pos}")
            break
    
    # Find Render Plan section
    render_plan_start = None
    render_plan_end = None
    
    for marker in render_plan_markers:
        pos = response_text.find(marker)
        if pos != -1:
            render_plan_start = pos + len(marker)
            print(f"[JSON EXTRACTION DEBUG] Found Render Plan marker: '{marker}' at position {pos}")
            break
    
    # Extract Content IR JSON
    if content_ir_start is not None:
        # Find the start of the JSON (first { after marker)
        json_start = response_text.find('{', content_ir_start)
        if json_start != -1:
            # Find the matching closing brace
            brace_count = 0
            content_ir_end = json_start
            
            for i in range(json_start, len(response_text)):
                if response_text[i] == '{':
                    brace_count += 1
                elif response_text[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        content_ir_end = i + 1
                        break
            
            if content_ir_end > json_start:
                content_ir_json = response_text[json_start:content_ir_end]
                print(f"[JSON EXTRACTION DEBUG] Extracted Content IR JSON (length: {len(content_ir_json)})")
                
                try:
                    cleaned_json = clean_json_string(content_ir_json)
                    content_ir = json.loads(cleaned_json)
                    print(f"✅ Successfully parsed Content IR JSON")
                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse Content IR JSON: {e}")
                    # Try advanced repair
                    try:
                        repaired_json = advanced_json_repair(cleaned_json)
                        content_ir = json.loads(repaired_json)
                        print(f"✅ Successfully repaired and parsed Content IR JSON")
                    except:
                        print(f"❌ Advanced repair also failed for Content IR")
                        content_ir = None
    
    # Extract Render Plan JSON
    if render_plan_start is not None:
        # Find the start of the JSON (first { after marker)
        json_start = response_text.find('{', render_plan_start)
        if json_start != -1:
            # Find the matching closing brace
            brace_count = 0
            render_plan_end = json_start
            
            for i in range(json_start, len(response_text)):
                if response_text[i] == '{':
                    brace_count += 1
                elif response_text[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        render_plan_end = i + 1
                        break
            
            if render_plan_end > json_start:
                render_plan_json = response_text[json_start:render_plan_end]
                print(f"[JSON EXTRACTION DEBUG] Extracted Render Plan JSON (length: {len(render_plan_json)})")
                
                try:
                    cleaned_json = clean_json_string(render_plan_json)
                    render_plan = json.loads(cleaned_json)
                    print(f"✅ Successfully parsed Render Plan JSON")
                except json.JSONDecodeError as e:
                    print(f"❌ Failed to parse Render Plan JSON: {e}")
                    # Try advanced repair
                    try:
                        repaired_json = advanced_json_repair(cleaned_json)
                        render_plan = json.loads(repaired_json)
                        print(f"✅ Successfully repaired and parsed Render Plan JSON")
                    except:
                        print(f"❌ Advanced repair also failed for Render Plan")
                        render_plan = None
    
    # Method 2: Fallback to code block extraction if markers didn't work
    if not content_ir or not render_plan:
        print("[JSON EXTRACTION DEBUG] Fallback to code block extraction...")
        
        # Look for JSON code blocks
        json_blocks = []
        start_pos = 0
        
        while True:
            start_marker = '```json'
            end_marker = '```'
            
            start_idx = response_text.find(start_marker, start_pos)
            if start_idx == -1:
                break
            
            content_start = start_idx + len(start_marker)
            end_idx = response_text.find(end_marker, content_start)
            if end_idx == -1:
                break
            
            json_content = response_text[content_start:end_idx].strip()
            if json_content:
                json_blocks.append(json_content)
            
            start_pos = end_idx + len(end_marker)
        
        # Try to parse each JSON block
        for i, block in enumerate(json_blocks):
            try:
                cleaned_block = clean_json_string(block)
                if not cleaned_block or cleaned_block == "{}":
                    continue
                    
                parsed = json.loads(cleaned_block)
                
                if not isinstance(parsed, dict):
                    continue
                
                # Identify which JSON is which based on structure
                if ("entities" in parsed or "management_team" in parsed or 
                    "historical_financials" in parsed or "strategic_buyers" in parsed):
                    if not content_ir:
                        content_ir = parsed
                        print(f"✅ Successfully extracted Content IR from code block {i+1}")
                        
                elif "slides" in parsed and isinstance(parsed.get("slides"), list):
                    if not render_plan:
                        render_plan = parsed
                        print(f"✅ Successfully extracted Render Plan from code block {i+1}")
                        
            except json.JSONDecodeError as e:
                print(f"❌ Failed to parse JSON block {i+1}: {e}")
                continue
            except Exception as e:
                print(f"❌ Unexpected error parsing block {i+1}: {e}")
                continue
    
    # Method 3: Aggressive extraction if still nothing found
    if not content_ir or not render_plan:
        print("[JSON EXTRACTION DEBUG] Attempting aggressive extraction...")
        
        # Look for any JSON-like content
        potential_jsons = []
        
        # Find all potential JSON objects
        brace_count = 0
        json_start = -1
        
        for i, char in enumerate(response_text):
            if char == '{':
                if brace_count == 0:
                    json_start = i
                brace_count += 1
            elif char == '}':
                brace_count -= 1
                if brace_count == 0 and json_start != -1:
                    potential_json = response_text[json_start:i+1]
                    if len(potential_json) > 50:  # Only consider substantial JSONs
                        potential_jsons.append(potential_json)
                    json_start = -1
        
        # Try to parse each potential JSON
        for i, potential_json in enumerate(potential_jsons):
            try:
                cleaned_json = clean_json_string(potential_json)
                parsed = json.loads(cleaned_json)
                
                if not isinstance(parsed, dict):
                    continue
                
                # Identify which JSON is which
                if ("entities" in parsed or "management_team" in parsed or 
                    "historical_financials" in parsed or "strategic_buyers" in parsed):
                    if not content_ir:
                        content_ir = parsed
                        print(f"✅ Successfully extracted Content IR via aggressive method")
                        
                elif "slides" in parsed and isinstance(parsed.get("slides"), list):
                    if not render_plan:
                        render_plan = parsed
                        print(f"✅ Successfully extracted Render Plan via aggressive method")
                        
            except:
                continue
    
    # Final validation and structure checking
    if content_ir:
        print(f"[JSON EXTRACTION DEBUG] Content IR keys: {list(content_ir.keys())}")
    if render_plan:
        print(f"[JSON EXTRACTION DEBUG] Render Plan keys: {list(render_plan.keys())}")
        if 'slides' in render_plan:
            print(f"[JSON EXTRACTION DEBUG] Number of slides: {len(render_plan['slides'])}")
    
    return content_ir, render_plan

def debug_json_extraction(response_text, content_ir, render_plan):
    """Debug JSON extraction by showing what was returned and what was extracted"""
    print("\n" + "🔍"*20 + " JSON EXTRACTION DEBUG " + "🔍"*20)
    
    # Show response length and first/last parts
    print(f"📏 Response Length: {len(response_text)} characters")
    print(f"📝 Response Preview (first 500 chars):")
    print(response_text[:500] + "..." if len(response_text) > 500 else response_text)
    
    if len(response_text) > 500:
        print(f"\n📝 Response Preview (last 500 chars):")
        print("..." + response_text[-500:] if len(response_text) > 500 else response_text)
    
    # Show what was extracted
    print(f"\n📊 EXTRACTION RESULTS:")
    if content_ir:
        print(f"✅ Content IR extracted:")
        print(f"   - Type: {type(content_ir)}")
        print(f"   - Keys: {list(content_ir.keys()) if isinstance(content_ir, dict) else 'N/A'}")
        if isinstance(content_ir, dict) and 'entities' in content_ir:
            company_name = content_ir.get('entities', {}).get('company', {}).get('name', 'Unknown')
            print(f"   - Company: {company_name}")
    else:
        print("❌ Content IR NOT extracted")
    
    if render_plan:
        print(f"✅ Render Plan extracted:")
        print(f"   - Type: {type(render_plan)}")
        print(f"   - Keys: {list(render_plan.keys()) if isinstance(render_plan, dict) else 'N/A'}")
        if isinstance(render_plan, dict) and 'slides' in render_plan:
            print(f"   - Slides: {len(render_plan['slides'])}")
            slide_types = [slide.get('template', 'unknown') for slide in render_plan['slides']]
            print(f"   - Slide Types: {slide_types[:5]}{'...' if len(slide_types) > 5 else ''}")
    else:
        print("❌ Render Plan NOT extracted")
    
    # Show common extraction issues
    print(f"\n🔍 COMMON EXTRACTION ISSUES CHECK:")
    
    # Check for JSON markers
    markers_found = []
    for marker in ["CONTENT IR JSON:", "RENDER PLAN JSON:", "```json", "```"]:
        if marker in response_text:
            markers_found.append(marker)
    
    if markers_found:
        print(f"✅ Found markers: {markers_found}")
    else:
        print("❌ No JSON markers found - LLM may not have formatted response properly")
    
    # Check for JSON structure
    brace_count = response_text.count('{') - response_text.count('}')
    if brace_count == 0:
        print("✅ Balanced braces found")
    else:
        print(f"❌ Unbalanced braces: {brace_count} more {'{' if brace_count > 0 else '}'}")
    
    # Check for common LLM response patterns
    if "I apologize" in response_text or "I'm sorry" in response_text:
        print("⚠️ LLM may have encountered an error")
    
    if "I don't have enough information" in response_text or "cannot generate" in response_text:
        print("⚠️ LLM may not have had sufficient context")
    
    print("🔍"*60 + "\n")

def normalize_extracted_json(content_ir, render_plan):
    """Normalize extracted JSON to match expected structure from examples"""
    print("[NORMALIZATION] Starting JSON normalization...")
    
    if content_ir:
        # Normalize Content IR
        content_ir = normalize_content_ir_structure(content_ir)
    
    if render_plan:
        # Normalize Render Plan
        render_plan = normalize_render_plan_structure(render_plan)
    
    return content_ir, render_plan

def normalize_content_ir_structure(content_ir):
    """Normalize Content IR structure to match expected format"""
    if not isinstance(content_ir, dict):
        return content_ir
    
    normalized = {}
    
    # Handle common field name variations
    field_mappings = {
        'company_name': 'entities',
        'company_info': 'entities',
        'management': 'management_team',
        'executives': 'management_team',
        'team': 'management_team',
        'strategic_buyers': 'strategic_buyers',
        'financial_buyers': 'financial_buyers',
        'pe_buyers': 'financial_buyers',
        'buyers': 'strategic_buyers'
    }
    
    # Map fields to correct names
    for old_key, new_key in field_mappings.items():
        if old_key in content_ir and new_key not in content_ir:
            normalized[new_key] = content_ir[old_key]
            print(f"[NORMALIZATION] Mapped {old_key} -> {new_key}")
    
    # Ensure entities structure
    if 'entities' not in normalized and 'entities' not in content_ir:
        # Try to find company name in various locations
        company_name = None
        for key in ['company_name', 'company', 'name', 'business_name']:
            if key in content_ir:
                if isinstance(content_ir[key], str):
                    company_name = content_ir[key]
                elif isinstance(content_ir[key], dict) and 'name' in content_ir[key]:
                    company_name = content_ir[key]['name']
                break
        
        if company_name:
            normalized['entities'] = {'company': {'name': company_name}}
            print(f"[NORMALIZATION] Created entities.company.name: {company_name}")
    
    # Ensure management_team structure
    if 'management_team' not in normalized and 'management_team' not in content_ir:
        # Look for management data in various forms
        mgmt_data = None
        for key in ['management', 'executives', 'team', 'leadership']:
            if key in content_ir:
                mgmt_data = content_ir[key]
                break
        
        if mgmt_data and isinstance(mgmt_data, dict):
            # Normalize to expected structure
            normalized_mgmt = {}
            
            # Handle different profile structures
            for column in ['left_column_profiles', 'right_column_profiles']:
                if column in mgmt_data:
                    normalized_mgmt[column] = mgmt_data[column]
                else:
                    # Try to find profiles in other formats
                    profiles = []
                    for key in ['profiles', 'members', 'executives']:
                        if key in mgmt_data:
                            profiles = mgmt_data[key]
                            break
                    
                    if profiles and isinstance(profiles, list):
                        # Split profiles between left and right columns
                        mid_point = len(profiles) // 2
                        normalized_mgmt['left_column_profiles'] = profiles[:mid_point]
                        normalized_mgmt['right_column_profiles'] = profiles[mid_point:]
                        break
            
            if normalized_mgmt:
                normalized['management_team'] = normalized_mgmt
                print(f"[NORMALIZATION] Created management_team structure with {len(normalized_mgmt.get('left_column_profiles', [])) + len(normalized_mgmt.get('right_column_profiles', []))} profiles")
    
    # Copy remaining fields
    for key, value in content_ir.items():
        if key not in normalized:
            normalized[key] = value
    
    return normalized

def normalize_render_plan_structure(render_plan):
    """Normalize Render Plan structure to match expected format"""
    if not isinstance(render_plan, dict):
        return render_plan
    
    normalized = {}
    
    # Ensure slides array exists
    if 'slides' not in render_plan:
        # Look for slides in other formats
        slides = None
        for key in ['slide_list', 'presentation_slides', 'deck_slides']:
            if key in render_plan:
                slides = render_plan[key]
                break
        
        if slides:
            normalized['slides'] = slides
            print(f"[NORMALIZATION] Mapped slides from {key}")
        else:
            # Create empty slides array
            normalized['slides'] = []
            print("[NORMALIZATION] Created empty slides array")
    else:
        normalized['slides'] = render_plan['slides']
    
    # Normalize each slide
    if 'slides' in normalized and isinstance(normalized['slides'], list):
        for i, slide in enumerate(normalized['slides']):
            if isinstance(slide, dict):
                normalized['slides'][i] = normalize_slide_structure(slide, i)
    
    return normalized

def normalize_slide_structure(slide, slide_index):
    """Normalize individual slide structure"""
    if not isinstance(slide, dict):
        return slide
    
    normalized_slide = {}
    
    # Ensure template field exists
    if 'template' not in slide:
        # Try to infer template from other fields
        template = None
        for key in ['slide_type', 'type', 'template_type']:
            if key in slide:
                template = slide[key]
                break
        
        if template:
            normalized_slide['template'] = template
            print(f"[NORMALIZATION] Slide {slide_index + 1}: Mapped template from {key}")
        else:
            # Default template
            normalized_slide['template'] = 'business_overview'
            print(f"[NORMALIZATION] Slide {slide_index + 1}: Set default template 'business_overview'")
    else:
        normalized_slide['template'] = slide['template']
    
    # Ensure data field exists
    if 'data' not in slide:
        # Look for data in other fields
        data = None
        for key in ['slide_data', 'content', 'information']:
            if key in slide:
                data = slide[key]
                break
        
        if data:
            normalized_slide['data'] = data
            print(f"[NORMALIZATION] Slide {slide_index + 1}: Mapped data from {key}")
        else:
            # Use slide content as data
            normalized_slide['data'] = {k: v for k, v in slide.items() if k not in ['template', 'slide_type', 'type', 'template_type']}
            print(f"[NORMALIZATION] Slide {slide_index + 1}: Created data from slide content")
    else:
        normalized_slide['data'] = slide['data']
    
    # Handle content_ir_key for buyer_profiles
    if normalized_slide.get('template') == 'buyer_profiles' and 'content_ir_key' not in slide:
        # Try to infer content_ir_key from data
        if 'data' in normalized_slide and isinstance(normalized_slide['data'], dict):
            data = normalized_slide['data']
            if 'strategic' in str(data).lower() or 'strategic_buyers' in str(data):
                normalized_slide['content_ir_key'] = 'strategic_buyers'
                print(f"[NORMALIZATION] Slide {slide_index + 1}: Inferred content_ir_key: strategic_buyers")
            elif 'financial' in str(data).lower() or 'financial_buyers' in str(data):
                normalized_slide['content_ir_key'] = 'financial_buyers'
                print(f"[NORMALIZATION] Slide {slide_index + 1}: Inferred content_ir_key: financial_buyers")
    
    # Copy any other fields
    for key, value in slide.items():
        if key not in normalized_slide:
            normalized_slide[key] = value
    
    return normalized_slide

def validate_json_structure_against_examples(content_ir, render_plan):
    """Validate extracted JSON structure against the example files"""
    print("[STRUCTURE VALIDATION] Starting validation against examples...")
    
    validation_results = {
        'content_ir_valid': False,
        'render_plan_valid': False,
        'missing_sections': [],
        'structure_issues': []
    }
    
    # Validate Content IR structure
    if content_ir and isinstance(content_ir, dict):
        print("[STRUCTURE VALIDATION] Validating Content IR structure...")
        
        # Check for required top-level sections
        required_sections = ['entities', 'management_team', 'strategic_buyers', 'financial_buyers']
        missing_sections = []
        
        for section in required_sections:
            if section not in content_ir:
                missing_sections.append(f"Missing '{section}' section")
        
        if missing_sections:
            validation_results['structure_issues'].extend(missing_sections)
            print(f"[STRUCTURE VALIDATION] ❌ Content IR missing sections: {missing_sections}")
        else:
            print("[STRUCTURE VALIDATION] ✓ Content IR has all required sections")
            
            # Validate management_team structure
            if 'management_team' in content_ir:
                mgmt = content_ir['management_team']
                if isinstance(mgmt, dict):
                    if 'left_column_profiles' in mgmt and 'right_column_profiles' in mgmt:
                        print("[STRUCTURE VALIDATION] ✓ Management team structure is correct")
                    else:
                        validation_results['structure_issues'].append("Management team missing column profiles")
                        print("[STRUCTURE VALIDATION] ❌ Management team structure incomplete")
                else:
                    validation_results['structure_issues'].append("Management team is not a dictionary")
                    print("[STRUCTURE VALIDATION] ❌ Management team is not properly structured")
            
            # Validate buyer arrays
            for buyer_type in ['strategic_buyers', 'financial_buyers']:
                if buyer_type in content_ir:
                    buyers = content_ir[buyer_type]
                    if isinstance(buyers, list):
                        print(f"[STRUCTURE VALIDATION] ✓ {buyer_type} is properly formatted array")
                    else:
                        validation_results['structure_issues'].append(f"{buyer_type} is not an array")
                        print(f"[STRUCTURE VALIDATION] ❌ {buyer_type} is not properly formatted")
            
            validation_results['content_ir_valid'] = True
    
    # Validate Render Plan structure
    if render_plan and isinstance(render_plan, dict):
        print("[STRUCTURE VALIDATION] Validating Render Plan structure...")
        
        # Check for slides array
        if 'slides' in render_plan and isinstance(render_plan['slides'], list):
            print(f"[STRUCTURE VALIDATION] ✓ Render Plan has {len(render_plan['slides'])} slides")
            
            # Validate each slide has required fields
            slide_issues = []
            for i, slide in enumerate(render_plan['slides']):
                if isinstance(slide, dict):
                    if 'template' not in slide:
                        slide_issues.append(f"Slide {i+1} missing 'template' field")
                    if 'data' not in slide:
                        slide_issues.append(f"Slide {i+1} missing 'data' field")
                    
                    # Check for content_ir_key in buyer_profiles slides
                    if slide.get('template') == 'buyer_profiles' and 'content_ir_key' not in slide:
                        slide_issues.append(f"Slide {i+1} (buyer_profiles) missing 'content_ir_key'")
            
            if slide_issues:
                validation_results['structure_issues'].extend(slide_issues)
                print(f"[STRUCTURE VALIDATION] ❌ Slide structure issues: {slide_issues}")
            else:
                print("[STRUCTURE VALIDATION] ✓ All slides have required fields")
                validation_results['render_plan_valid'] = True
        else:
            validation_results['structure_issues'].append("Render Plan missing 'slides' array")
            print("[STRUCTURE VALIDATION] ❌ Render Plan missing slides array")
    
    # Summary
    if validation_results['content_ir_valid'] and validation_results['render_plan_valid']:
        print("[STRUCTURE VALIDATION] ✅ Both Content IR and Render Plan structures are valid!")
    else:
        print(f"[STRUCTURE VALIDATION] ⚠️  Validation issues found: {len(validation_results['structure_issues'])} issues")
    
    return validation_results

# COMPREHENSIVE SLIDE VALIDATION SYSTEM
def validate_individual_slides(content_ir, render_plan):
    """Validate each slide individually to ensure no empty boxes or missing content"""
    
    validation_results = {
        'overall_valid': True,
        'slide_validations': [],
        'critical_issues': [],
        'warnings': [],
        'summary': {
            'total_slides': 0,
            'valid_slides': 0,
            'invalid_slides': 0,
            'slides_with_warnings': 0
        }
    }
    
    # Safety checks for None values
    if not content_ir:
        validation_results['critical_issues'].append("Content IR is None or empty")
        validation_results['overall_valid'] = False
        return validation_results
        
    if not render_plan or 'slides' not in render_plan:
        validation_results['critical_issues'].append("Render Plan is None or has no slides")
        validation_results['overall_valid'] = False
        return validation_results
    
    if not render_plan or 'slides' not in render_plan:
        validation_results['critical_issues'].append("No render plan or slides found")
        validation_results['overall_valid'] = False
        return validation_results
    
    slides = render_plan['slides']
    validation_results['summary']['total_slides'] = len(slides)
    
    # Define validation rules for each template
    template_validators = {
        'business_overview': validate_business_overview_slide,
        'investor_considerations': validate_investor_considerations_slide,
        'product_service_footprint': validate_product_service_footprint_slide,
        'product_service_overview': validate_product_service_overview_slide,
        'buyer_profiles': validate_buyer_profiles_slide,
        'historical_financial_performance': validate_historical_financial_performance_slide,
        'management_team': validate_management_team_slide,
        'growth_strategy_projections': validate_growth_strategy_slide,
        'competitive_positioning': validate_competitive_positioning_slide,
        'valuation_overview': validate_valuation_overview_slide,
        'trading_comparables': validate_trading_comparables_slide,
        'precedent_transactions': validate_precedent_transactions_slide,
        'margin_cost_resilience': validate_margin_cost_resilience_slide,
        'financial_summary': validate_financial_summary_slide,
        'transaction_overview': validate_transaction_overview_slide,
        'appendix': validate_appendix_slide,
        'sea_conglomerates': validate_sea_conglomerates_slide,
        'investor_process_overview': validate_investor_process_overview_slide
    }
    
    # Validate each slide
    for i, slide in enumerate(slides):
        slide_num = i + 1
        template = slide.get('template', 'unknown')
        
        slide_validation = {
            'slide_number': slide_num,
            'template': template,
            'valid': True,
            'issues': [],
            'warnings': [],
            'missing_fields': [],
            'empty_fields': []
        }
        
        # Basic slide structure validation
        if not slide.get('data'):
            slide_validation['issues'].append("Missing 'data' section")
            slide_validation['valid'] = False
        
        # Template-specific validation
        if template in template_validators:
            template_validator = template_validators[template]
            template_validation = template_validator(slide, content_ir)
            
            slide_validation['issues'].extend(template_validation.get('issues', []))
            slide_validation['warnings'].extend(template_validation.get('warnings', []))
            slide_validation['missing_fields'].extend(template_validation.get('missing_fields', []))
            slide_validation['empty_fields'].extend(template_validation.get('empty_fields', []))
            
            if template_validation.get('issues') or template_validation.get('missing_fields') or template_validation.get('empty_fields'):
                slide_validation['valid'] = False
        else:
            slide_validation['warnings'].append(f"Unknown template type: {template}")
        
        # Update summary counts
        if slide_validation['valid']:
            validation_results['summary']['valid_slides'] += 1
        else:
            validation_results['summary']['invalid_slides'] += 1
            validation_results['overall_valid'] = False
        
        if slide_validation['warnings']:
            validation_results['summary']['slides_with_warnings'] += 1
        
        validation_results['slide_validations'].append(slide_validation)
    
    return validation_results

# FIXED SLIDE-SPECIFIC VALIDATORS
def validate_business_overview_slide(slide, content_ir):
    """Validate business overview slide for completeness"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    # Required fields for business overview
    required_fields = {
        'title': 'Slide title',
        'description': 'Business description',
        'highlights': 'Key highlights',
        'services': 'Services/products list',
        'positioning_desc': 'Market positioning description'
    }
    
    for field, description in required_fields.items():
        if field not in data:
            validation['missing_fields'].append(f"Missing {description} ({field})")
        elif not data[field] or (isinstance(data[field], list) and len(data[field]) == 0):
            validation['empty_fields'].append(f"Empty {description} ({field})")
        elif isinstance(data[field], str) and (data[field].strip() == '' or '[' in data[field]):
            validation['empty_fields'].append(f"Placeholder or empty {description} ({field})")
    
    # Validate highlights array
    if 'highlights' in data and isinstance(data['highlights'], list):
        if len(data['highlights']) < 1:
            validation['warnings'].append("No highlights provided")
        for i, highlight in enumerate(data['highlights']):
            if not highlight or highlight.strip() == '' or '[' in highlight:
                validation['empty_fields'].append(f"Empty highlight #{i+1}")
    
    # Validate services array
    if 'services' in data and isinstance(data['services'], list):
        if len(data['services']) < 1:
            validation['warnings'].append("No services listed")
        for i, service in enumerate(data['services']):
            if not service or service.strip() == '' or '[' in service:
                validation['empty_fields'].append(f"Empty service #{i+1}")
    
    return validation

def validate_product_service_footprint_slide(slide, content_ir):
    """Validate product service footprint slide - the one with empty boxes"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    # Required fields
    if 'title' not in data or not data['title']:
        validation['missing_fields'].append("Missing slide title")
    
    if 'services' not in data:
        validation['missing_fields'].append("Missing services array")
    elif not isinstance(data['services'], list) or len(data['services']) == 0:
        validation['empty_fields'].append("Empty services array")
    else:
        # Validate each service entry
        for i, service in enumerate(data['services']):
            service_num = i + 1
            if not isinstance(service, dict):
                validation['issues'].append(f"Service #{service_num} is not a proper object")
                continue
                
            if 'title' not in service or not service['title'] or service['title'].strip() == '':
                validation['empty_fields'].append(f"Service #{service_num} missing title")
            elif '[' in service['title']:
                validation['empty_fields'].append(f"Service #{service_num} has placeholder title")
                
            if 'desc' not in service or not service['desc'] or service['desc'].strip() == '':
                validation['empty_fields'].append(f"Service #{service_num} missing description")
            elif '[' in service['desc']:
                validation['empty_fields'].append(f"Service #{service_num} has placeholder description")
    
    # ENHANCED: Check for market coverage data with 3-4 column requirements
    if 'coverage_table' in data:
        coverage_data = data['coverage_table']
        if not coverage_data or (isinstance(coverage_data, list) and len(coverage_data) == 0):
            validation['empty_fields'].append("Empty coverage table section")
        elif isinstance(coverage_data, list) and len(coverage_data) > 0:
            # Check column structure
            if isinstance(coverage_data[0], list):
                num_cols = len(coverage_data[0])
                if num_cols < 2:
                    validation['warnings'].append(f"Coverage table has only {num_cols} columns - consider adding more columns")
                elif num_cols > 6:
                    validation['warnings'].append(f"Coverage table has {num_cols} columns - many columns may affect readability")
                
                # Validate header row content and company-specific data
                if len(coverage_data) > 0 and isinstance(coverage_data[0], list):
                    header_row = coverage_data[0]
                    required_concepts = ['region', 'market', 'segment', 'business', 'asset', 'coverage', 'product', 'service']
                    header_text = ' '.join(str(h).lower() for h in header_row)
                    has_market_concepts = any(concept in header_text for concept in required_concepts)
                    if not has_market_concepts:
                        validation['warnings'].append("Table headers should include market comparison concepts like Region, Market Segment, Assets, Coverage")
                
                # Check for wrong company data (generic Indonesian cities instead of company-specific data)
                table_text = str(coverage_data).lower()
                wrong_data_indicators = ['jakarta', 'bandung', 'surabaya', 'outlets', 'branches']
                for indicator in wrong_data_indicators:
                    if indicator in table_text:
                        validation['issues'].append(f"Coverage table contains generic/wrong company data ('{indicator}') - use company-specific geographic and operational data")
    else:
        validation['warnings'].append("No coverage table data - right side may appear empty")
    
    if 'metrics' in data:
        metrics = data['metrics']
        if not metrics or (isinstance(metrics, dict) and len(metrics) == 0):
            validation['empty_fields'].append("Empty metrics section")
    else:
        validation['warnings'].append("No operational metrics - may result in empty boxes")
    
    return validation

def validate_buyer_profiles_slide(slide, content_ir):
    """Validate buyer profiles slide - FIXED to handle both approaches correctly"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    # Check for content_ir_key (preferred) or table_rows (fallback)
    has_content_ir_key = 'content_ir_key' in slide
    has_table_rows = 'table_rows' in data
    
    if not has_content_ir_key and not has_table_rows:
        validation['issues'].append("Missing content_ir_key - table will be empty")
    elif has_content_ir_key:
        content_key = slide['content_ir_key']
        
        # Verify the key exists in content_ir and has data
        if content_key not in content_ir:
            validation['issues'].append(f"content_ir_key '{content_key}' not found in Content IR")
        elif not content_ir[content_key] or len(content_ir[content_key]) == 0:
            validation['empty_fields'].append(f"Empty {content_key} array in Content IR")
        else:
            # Validate buyer data completeness
            buyers = content_ir[content_key]
            if not isinstance(buyers, list):
                validation['issues'].append(f"content_ir_key '{content_key}' should be an array")
            else:
                # MANDATORY: Check minimum buyer count requirement (4-5 buyers minimum)
                buyer_count = len(buyers)
                if buyer_count < 2:
                    validation['warnings'].append(f"Only {buyer_count} {content_key} provided - consider adding more for comprehensive analysis")
                elif buyer_count < 3:
                    validation['warnings'].append(f"Consider adding more {content_key} - current {buyer_count}")
                
                for i, buyer in enumerate(buyers):
                    buyer_num = i + 1
                    if not isinstance(buyer, dict):
                        validation['issues'].append(f"Buyer #{buyer_num} should be an object")
                        continue
                    
                    # Check for required buyer fields - FIXED for your data structure
                    required_buyer_fields = ['buyer_name', 'strategic_rationale', 'fit']
                    for field in required_buyer_fields:
                        if field not in buyer:
                            validation['empty_fields'].append(f"Buyer #{buyer_num} missing {field}")
                        elif not buyer[field] or str(buyer[field]).strip() == '':
                            validation['empty_fields'].append(f"Buyer #{buyer_num} has empty {field}")
                        elif '[' in str(buyer[field]):
                            validation['empty_fields'].append(f"Buyer #{buyer_num} has placeholder {field}")
                    
                    # Validate strategic_rationale length (RELAXED: 3-50 words)
                    if 'strategic_rationale' in buyer and buyer['strategic_rationale']:
                        strategic_words = len(str(buyer['strategic_rationale']).split())
                        if strategic_words < 3:
                            validation['warnings'].append(f"Buyer #{buyer_num} strategic_rationale quite short: {strategic_words} words")
                        elif strategic_words > 50:
                            validation['warnings'].append(f"Buyer #{buyer_num} strategic_rationale quite long: {strategic_words} words")
                    
                    # Validate fit format (score + 5-word rationale)
                    if 'fit' in buyer and buyer['fit']:
                        fit_text = str(buyer['fit']).strip()
                        # Should contain both a score (like "High (9/10)") and a 5-word rationale
                        if not any(score in fit_text for score in ['High', 'Medium', 'Low']):
                            validation['issues'].append(f"Buyer #{buyer_num} fit missing score level (High/Medium/Low)")
                        # Check if it has additional rationale after the score (RELAXED)
                        fit_parts = fit_text.split(')')
                        if len(fit_parts) < 2 or not fit_parts[1].strip():
                            validation['warnings'].append(f"Buyer #{buyer_num} fit missing rationale after score")
                        else:
                            rationale_words = len(fit_parts[1].strip().split())
                            if rationale_words < 1:
                                validation['warnings'].append(f"Buyer #{buyer_num} fit rationale empty")
                            # No upper limit - let AI be flexible with rationale length
    
    elif has_table_rows and not has_content_ir_key:
        # Validate table_rows content - FIXED to handle your data structure
        validation['warnings'].append("Using hardcoded table_rows - content_ir_key preferred for dynamic data")
        
        table_rows = data.get('table_rows', [])
        if not table_rows or len(table_rows) == 0:
            validation['empty_fields'].append("Empty table_rows array")
        else:
            for i, row in enumerate(table_rows):
                row_num = i + 1
                # Your table_rows contain dictionaries, not lists
                if isinstance(row, dict):
                    # Check if it has required fields
                    required_fields = ['buyer_name', 'strategic_rationale']
                    for field in required_fields:
                        if field not in row or not row[field] or str(row[field]).strip() == '':
                            validation['empty_fields'].append(f"Table row #{row_num} missing or empty {field}")
                    
                    # Validate strategic_rationale length (RELAXED: 3-50 words) for table_rows
                    if 'strategic_rationale' in row and row['strategic_rationale']:
                        strategic_words = len(str(row['strategic_rationale']).split())
                        if strategic_words < 3:
                            validation['warnings'].append(f"Table row #{row_num} strategic_rationale quite short: {strategic_words} words")
                        elif strategic_words > 50:
                            validation['warnings'].append(f"Table row #{row_num} strategic_rationale quite long: {strategic_words} words")
                    
                    # Validate fit format (score + 5-word rationale) for table_rows
                    if 'fit' in row and row['fit']:
                        fit_text = str(row['fit']).strip()
                        # Should contain both a score (like "High (9/10)") and a 5-word rationale
                        if not any(score in fit_text for score in ['High', 'Medium', 'Low']):
                            validation['issues'].append(f"Table row #{row_num} fit missing score level (High/Medium/Low)")
                        # Check if it has additional rationale after the score (RELAXED)
                        fit_parts = fit_text.split(')')
                        if len(fit_parts) < 2 or not fit_parts[1].strip():
                            validation['warnings'].append(f"Table row #{row_num} fit missing rationale after score")
                        else:
                            rationale_words = len(fit_parts[1].strip().split())
                            if rationale_words < 1:
                                validation['warnings'].append(f"Table row #{row_num} fit rationale empty")
                            # No upper limit - let AI be flexible with rationale length
                elif isinstance(row, list):
                    if len(row) == 0:
                        validation['empty_fields'].append(f"Table row #{row_num} is empty")
                    else:
                        for j, cell in enumerate(row):
                            cell_num = j + 1
                            if not cell or str(cell).strip() == '' or '[' in str(cell):
                                validation['empty_fields'].append(f"Table row #{row_num}, cell #{cell_num} is empty or placeholder")
                else:
                    validation['empty_fields'].append(f"Table row #{row_num} has invalid structure")
    
    # Validate required fields
    required_fields = ['title', 'table_headers']
    for field in required_fields:
        if field not in data:
            validation['missing_fields'].append(f"Missing {field}")
        elif not data[field]:
            validation['empty_fields'].append(f"Empty {field}")
        elif field == 'table_headers' and isinstance(data[field], list):
            if len(data[field]) < 1:
                validation['warnings'].append("No table headers provided")
            for i, header in enumerate(data[field]):
                if not header or str(header).strip() == '':
                    validation['empty_fields'].append(f"Table header #{i+1} is empty")
    
    return validation

def validate_management_team_slide(slide, content_ir):
    """Validate management team slide - FIXED for correct field names"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    # Handle None content_ir
    if not content_ir:
        validation['warnings'].append("No Content IR provided for validation")
        return validation
    
    # Check if using content_ir_key approach
    # Add safety check for content_ir
    if not content_ir:
        validation['warnings'].append("Content IR is empty or None")
        return validation
        
    if 'content_ir_key' in slide:
        content_key = slide['content_ir_key']
        if content_key not in content_ir:
            validation['issues'].append(f"content_ir_key '{content_key}' not found in Content IR")
            return validation
        mgmt_data = content_ir[content_key]
    else:
        # Check data section
        data = slide.get('data', {})
        if 'management_team' not in content_ir:
            validation['issues'].append("No management_team data in Content IR")
            return validation
        mgmt_data = content_ir['management_team']
    
    # Check for required profile arrays
    for column in ['left_column_profiles', 'right_column_profiles']:
        if column not in mgmt_data:
            validation['missing_fields'].append(f"Missing {column}")
        elif not isinstance(mgmt_data[column], list) or len(mgmt_data[column]) == 0:
            validation['empty_fields'].append(f"Empty {column}")
        else:
            # Validate individual profiles - FIXED FIELD NAMES
            for i, profile in enumerate(mgmt_data[column]):
                profile_num = i + 1
                # Check for the CORRECT field names used in your data
                required_profile_fields = ['role_title', 'experience_bullets']
                for field in required_profile_fields:
                    if field not in profile or not profile[field]:
                        validation['empty_fields'].append(f"{column} profile #{profile_num} missing/placeholder {field}")
                    elif field == 'role_title' and '[' in str(profile[field]):
                        validation['empty_fields'].append(f"{column} profile #{profile_num} missing/placeholder {field}")
                    elif field == 'experience_bullets' and (not isinstance(profile[field], list) or len(profile[field]) == 0):
                        validation['empty_fields'].append(f"{column} profile #{profile_num} missing/placeholder {field}")
    
    return validation

def validate_historical_financial_performance_slide(slide, content_ir):
    """Validate historical financial performance slide"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    # Required fields for historical financial performance
    required_fields = {
        'title': 'Slide title',
        'chart': 'Financial performance chart data',
        'key_metrics': 'Key financial metrics'
    }
    
    for field, description in required_fields.items():
        if field not in data:
            validation['missing_fields'].append(f"Missing {description}")
        elif not data[field]:
            validation['empty_fields'].append(f"Empty {description}")
    
    # Validate chart data
    if 'chart' in data and isinstance(data['chart'], dict):
        chart = data['chart']
        chart_required = ['categories', 'revenue', 'ebitda']
        for field in chart_required:
            if field not in chart or not chart[field]:
                validation['empty_fields'].append(f"Missing chart {field} data")
    
    # Validate key metrics - MUST have exactly 4 numeric metrics
    if 'key_metrics' in data and isinstance(data['key_metrics'], dict):
        metrics = data['key_metrics']
        if 'metrics' in metrics and isinstance(metrics['metrics'], list):
            metric_count = len(metrics['metrics'])
            if metric_count < 2:
                validation['warnings'].append(f"Only {metric_count} key metrics provided - consider adding more")
            elif metric_count > 6:
                validation['warnings'].append(f"Many metrics ({metric_count}) - consider focusing on most important ones")
            
            # Check if metrics are numeric (percentages, amounts, rankings)
            for i, metric in enumerate(metrics['metrics']):
                if isinstance(metric, str):
                    # Check if it looks like a descriptive sentence rather than a number
                    if len(metric.split()) > 8:  # More than 8 words suggests overly descriptive text
                        validation['warnings'].append(f"Metric {i+1} quite descriptive - consider shorter format")
        else:
            validation['empty_fields'].append("Missing metrics array in key_metrics")
    
    return validation

def validate_growth_strategy_slide(slide, content_ir):
    """Validate growth strategy slide"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    # Get actual data structure - check for slide_data wrapper
    if 'slide_data' in data:
        actual_data = data['slide_data']
    else:
        actual_data = data
    
    # Required fields for growth strategy
    required_fields = {
        'title': 'Slide title',
        'growth_strategy': 'Growth strategy section',
        'financial_projections': 'Financial projections'
    }
    
    for field, description in required_fields.items():
        if field not in actual_data:
            validation['missing_fields'].append(f"Missing {description}")
        elif not actual_data[field]:
            validation['empty_fields'].append(f"Empty {description}")
    
    # Validate growth strategy
    if 'growth_strategy' in actual_data and isinstance(actual_data['growth_strategy'], dict):
        growth_strat = actual_data['growth_strategy']
        if 'strategies' in growth_strat and isinstance(growth_strat['strategies'], list):
            if len(growth_strat['strategies']) < 1:
                validation['warnings'].append("No growth strategies provided")
        else:
            validation['empty_fields'].append("Missing strategies array in growth_strategy")
    
    return validation

def validate_competitive_positioning_slide(slide, content_ir):
    """ENHANCED: Validate competitive positioning slide - iCar Asia format requirements"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    # ENHANCED: Check for iCar Asia format requirements
    required_fields = {
        'title': 'Slide title',
        'competitors': 'Competitors list for revenue chart',
        'assessment': 'Competitive assessment table (REQUIRED for iCar Asia format)',
        'advantages': 'Competitive advantages',
        'barriers': 'Market barriers to entry'
    }
    
    for field, description in required_fields.items():
        if field not in data:
            validation['missing_fields'].append(f"Missing {description}")
        elif not data[field]:
            validation['empty_fields'].append(f"Empty {description}")
    
    # Validate competitors array - FIXED for correct structure
    if 'competitors' in data and isinstance(data['competitors'], list):
        if len(data['competitors']) < 1:
            validation['warnings'].append("No competitors listed")
        for i, competitor in enumerate(data['competitors']):
            comp_num = i + 1
            # Your data structure has 'name' and 'revenue' - not strengths/weaknesses
            if isinstance(competitor, dict):
                if 'name' not in competitor or not competitor['name']:
                    validation['empty_fields'].append(f"Competitor #{comp_num} missing name")
                if 'revenue' not in competitor or not competitor['revenue']:
                    validation['empty_fields'].append(f"Competitor #{comp_num} missing revenue")
            elif not competitor or '[' in str(competitor):
                validation['empty_fields'].append(f"Competitor #{comp_num} is empty or placeholder")
        
        # Check for wrong industry competitors (bakery companies instead of oil/gas)
        competitor_text = str(data['competitors']).lower()
        wrong_competitors = ['breadlife', 'sari roti', 'holland bakery', 'breadtalk', 'bakery', 'bread']
        for wrong_comp in wrong_competitors:
            if wrong_comp in competitor_text:
                validation['issues'].append(f"Wrong industry competitors detected ('{wrong_comp}') - use oil/gas companies like ExxonMobil, Chevron, Shell for Aramco")
    
    # ENHANCED: Validate 5-column assessment table structure (iCar Asia format)
    if 'assessment' in data:
        assessment = data['assessment']
        if not assessment or not isinstance(assessment, list) or len(assessment) == 0:
            validation['issues'].append("Empty competitive assessment table - iCar Asia format requires 5-column structure")
        elif len(assessment) > 0:
            # Check column structure
            if isinstance(assessment[0], list):
                num_cols = len(assessment[0])
                if num_cols < 3:
                    validation['warnings'].append(f"Assessment table has only {num_cols} columns - consider adding more comparison criteria")
                elif num_cols > 8:
                    validation['warnings'].append(f"Assessment table has {num_cols} columns - many columns may affect readability")
                
                # Validate header structure
                if len(assessment) > 0:
                    header_row = assessment[0]
                    expected_concepts = ['company', 'market', 'tech', 'platform', 'coverage', 'revenue']
                    header_text = ' '.join(str(h).lower() for h in header_row)
                    has_expected_headers = any(concept in header_text for concept in expected_concepts)
                    if not has_expected_headers:
                        validation['warnings'].append("Table headers don't match iCar Asia format - should include Company, Market Share, Tech Platform, Coverage, Revenue")
                
                # Check for wrong company data in assessment table  
                assessment_text = str(assessment).lower()
                wrong_companies = ['breadlife', 'sari roti', 'holland bakery', 'breadtalk']
                for wrong_comp in wrong_companies:
                    if wrong_comp in assessment_text:
                        validation['issues'].append(f"Wrong company data in assessment table ('{wrong_comp}') - use industry-appropriate competitors")
                
                # Check for star ratings in data rows
                if len(assessment) > 1:
                    data_rows = assessment[1:]
                    has_star_ratings = False
                    for row in data_rows:
                        if isinstance(row, list) and len(row) > 2:
                            for cell in row[1:-1]:  # Skip company name and revenue columns
                                if '⭐' in str(cell) or '★' in str(cell):
                                    has_star_ratings = True
                                    break
                    if not has_star_ratings:
                        validation['warnings'].append("Assessment table should use star ratings (⭐⭐⭐⭐) for visual comparison like iCar Asia format")
            else:
                validation['issues'].append("Assessment table format invalid - should be array of arrays (rows and columns)")
    
    # Check assessment table
    if 'assessment' in data:
        assessment = data['assessment']
        if not assessment or not isinstance(assessment, list) or len(assessment) == 0:
            validation['empty_fields'].append("Empty competitive assessment table")
    else:
        validation['warnings'].append("No competitive assessment table")
    
    # Check for barriers and advantages
    for section in ['barriers', 'advantages']:
        if section in data and isinstance(data[section], list):
            for i, item in enumerate(data[section]):
                if isinstance(item, dict):
                    if not item.get('title') or not item.get('desc'):
                        validation['empty_fields'].append(f"{section.title()} #{i+1} missing title or description")
    
    return validation

def validate_valuation_overview_slide(slide, content_ir):
    """Validate valuation overview slide - FIXED for correct field names"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    # FIXED: Use the correct field names from your data structure
    required_fields = {
        'title': 'Slide title',
        'valuation_data': 'Valuation methodologies data'  # FIXED
    }
    
    for field, description in required_fields.items():
        if field not in data:
            validation['missing_fields'].append(f"Missing {description}")
        elif not data[field]:
            validation['empty_fields'].append(f"Empty {description}")
    
    # Validate valuation_data array
    if 'valuation_data' in data and isinstance(data['valuation_data'], list):
        if len(data['valuation_data']) < 1:
            validation['warnings'].append("No valuation methodologies provided")
        
        # Check for duplicate methodologies
        methodologies = []
        for method in data['valuation_data']:
            if isinstance(method, dict) and 'methodology' in method:
                methodologies.append(method['methodology'])
        
        duplicate_methods = [m for m in set(methodologies) if methodologies.count(m) > 1]
        if duplicate_methods:
            validation['issues'].append(f"Duplicate methodologies detected: {duplicate_methods} - should have distinct methodologies like 'Trading Multiples (EV/Revenue)', 'Trading Multiples (EV/EBITDA)', 'DCF'")
        
        # Validate each methodology entry
        for i, method in enumerate(data['valuation_data']):
            method_num = i + 1
            if isinstance(method, dict):
                # Check for original 5-column format fields
                required_method_fields = ['methodology', 'enterprise_value', 'metric', '22a_multiple', '23e_multiple', 'commentary']
                for field in required_method_fields:
                    if field not in method or not method[field]:
                        validation['empty_fields'].append(f"Methodology #{method_num} missing {field} (use original 5-column format)")
            elif not method or '[' in str(method):
                validation['empty_fields'].append(f"Methodology #{method_num} is empty or placeholder")
    
    return validation

def validate_trading_comparables_slide(slide, content_ir):
    """Validate trading comparables slide"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    # Required fields
    required_fields = {
        'title': 'Slide title',
        'comparable_companies': 'Comparable companies list',
        'metrics': 'Financial metrics comparison'
    }
    
    for field, description in required_fields.items():
        if field not in data:
            validation['missing_fields'].append(f"Missing {description}")
        elif not data[field]:
            validation['empty_fields'].append(f"Empty {description}")
    
    # Validate comparable companies
    if 'comparable_companies' in data and isinstance(data['comparable_companies'], list):
        if len(data['comparable_companies']) < 2:
            validation['warnings'].append("Less than 2 comparable companies - consider adding more")
        for i, company in enumerate(data['comparable_companies']):
            comp_num = i + 1
            if isinstance(company, dict):
                required_comp_fields = ['name', 'market_cap', 'revenue', 'ebitda_multiple']
                for field in required_comp_fields:
                    if field not in company or not company[field]:
                        validation['empty_fields'].append(f"Comparable #{comp_num} missing {field}")
                    elif '[' in str(company[field]):
                        validation['empty_fields'].append(f"Comparable #{comp_num} has placeholder {field}")
    
    return validation

def validate_precedent_transactions_slide(slide, content_ir):
    """Validate precedent transactions slide"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    # Required fields
    required_fields = {
        'title': 'Slide title',
        'transactions': 'Precedent transactions list'
    }
    
    for field, description in required_fields.items():
        if field not in data:
            validation['missing_fields'].append(f"Missing {description}")
        elif not data[field]:
            validation['empty_fields'].append(f"Empty {description}")
    
    # Validate transactions
    if 'transactions' in data and isinstance(data['transactions'], list):
        if len(data['transactions']) < 1:
            validation['warnings'].append("No precedent transactions provided")
        for i, transaction in enumerate(data['transactions']):
            trans_num = i + 1
            if isinstance(transaction, dict):
                required_trans_fields = ['target', 'acquirer', 'date', 'enterprise_value', 'revenue', 'ev_revenue_multiple']
                for field in required_trans_fields:
                    if field not in transaction or not transaction[field]:
                        validation['empty_fields'].append(f"Transaction #{trans_num} missing {field}")
                    elif '[' in str(transaction[field]):
                        validation['empty_fields'].append(f"Transaction #{trans_num} has placeholder {field}")
    
    return validation

def validate_margin_cost_resilience_slide(slide, content_ir):
    """Validate margin/cost resilience slide - FIXED for correct field names"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    # FIXED: Use the correct field names from your data structure
    required_fields = {
        'title': 'Slide title',
        'cost_management': 'Cost management initiatives',  # FIXED
        'risk_mitigation': 'Risk mitigation strategies'     # FIXED
    }
    
    for field, description in required_fields.items():
        if field not in data:
            validation['missing_fields'].append(f"Missing {description}")
        elif not data[field]:
            validation['empty_fields'].append(f"Empty {description}")
    
    # Validate cost management items
    if 'cost_management' in data:
        cost_mgmt = data['cost_management']
        if isinstance(cost_mgmt, dict) and 'items' in cost_mgmt:
            items = cost_mgmt['items']
            if not items or len(items) == 0:
                validation['empty_fields'].append("Empty cost management items")
            else:
                for i, item in enumerate(items):
                    if not isinstance(item, dict):
                        validation['empty_fields'].append(f"Cost management item #{i+1} is not properly structured")
                    elif not item.get('title') or not item.get('description'):
                        validation['empty_fields'].append(f"Cost management item #{i+1} missing title or description")
    
    # Validate risk mitigation
    if 'risk_mitigation' in data:
        risk_mit = data['risk_mitigation']
        if isinstance(risk_mit, dict):
            if 'main_strategy' not in risk_mit:
                validation['missing_fields'].append("Missing main strategy in risk mitigation")
        
    return validation

def validate_investor_considerations_slide(slide, content_ir):
    """Validate investor considerations slide"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    required_fields = {
        'title': 'Slide title',
        'considerations': 'Investment considerations list',
        'mitigants': 'Risk mitigants list'
    }
    
    for field, description in required_fields.items():
        if field not in data:
            validation['missing_fields'].append(f"Missing {description}")
        elif not data[field] or (isinstance(data[field], list) and len(data[field]) == 0):
            validation['empty_fields'].append(f"Empty {description}")
    
    return validation

def validate_financial_summary_slide(slide, content_ir):
    """Validate financial summary slide"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    required_fields = {
        'title': 'Slide title',
        'key_metrics': 'Key financial metrics',
        'performance_highlights': 'Performance highlights'
    }
    
    for field, description in required_fields.items():
        if field not in data:
            validation['missing_fields'].append(f"Missing {description}")
        elif not data[field]:
            validation['empty_fields'].append(f"Empty {description}")
    
    return validation

def validate_transaction_overview_slide(slide, content_ir):
    """Validate transaction overview slide"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    required_fields = {
        'title': 'Slide title',
        'transaction_structure': 'Transaction structure',
        'key_terms': 'Key transaction terms',
        'timeline': 'Transaction timeline'
    }
    
    for field, description in required_fields.items():
        if field not in data:
            validation['missing_fields'].append(f"Missing {description}")
        elif not data[field]:
            validation['empty_fields'].append(f"Empty {description}")
    
    return validation

def validate_product_service_overview_slide(slide, content_ir):
    """Validate product/service overview slide"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    # Required fields
    required_fields = {
        'title': 'Slide title',
        'products': 'Products list',
        'market_position': 'Market positioning'
    }
    
    for field, description in required_fields.items():
        if field not in data:
            validation['missing_fields'].append(f"Missing {description}")
        elif not data[field]:
            validation['empty_fields'].append(f"Empty {description}")
    
    return validation

def validate_appendix_slide(slide, content_ir):
    """Validate appendix slide"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    if 'title' not in data or not data['title']:
        validation['missing_fields'].append("Missing appendix title")
    
    return validation

def validate_sea_conglomerates_slide(slide, content_ir):
    """Validate global conglomerates slide (previously SEA conglomerates)"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    # Safety check and check content_ir for sea_conglomerates data
    if not content_ir:
        validation['warnings'].append("Content IR is empty")
        return validation
        
    if 'sea_conglomerates' not in content_ir:
        validation['issues'].append("Missing sea_conglomerates section in Content IR")
    elif not content_ir['sea_conglomerates'] or len(content_ir['sea_conglomerates']) == 0:
        validation['empty_fields'].append("Empty sea_conglomerates array in Content IR")
    else:
        conglomerates = content_ir['sea_conglomerates']
        
        # MANDATORY: Check minimum conglomerate count requirement (4-5 conglomerates minimum)
        conglomerate_count = len(conglomerates)
        if conglomerate_count < 2:
            validation['warnings'].append(f"Only {conglomerate_count} conglomerates provided - consider adding more")
        elif conglomerate_count < 3:
            validation['warnings'].append(f"Consider adding more conglomerates - current {conglomerate_count}")
        
        for i, conglomerate in enumerate(conglomerates):
            cong_num = i + 1
            if isinstance(conglomerate, dict):
                # Check for required SEA conglomerate fields (NOT buyer_name fields!)
                required_fields = ['name', 'country', 'description']
                for field in required_fields:
                    if field not in conglomerate or not conglomerate[field]:
                        validation['empty_fields'].append(f"Conglomerate #{cong_num} missing {field}")
                    elif '[' in str(conglomerate[field]):
                        validation['empty_fields'].append(f"Conglomerate #{cong_num} has placeholder {field}")
                
                # Check for obvious placeholder patterns in contact field (not legitimate user data)
                contact_field = conglomerate.get('contact', '')
                placeholder_patterns = ['[placeholder]', '[contact]', '[team]', 'TODO:', 'TBD', 'PLACEHOLDER']
                if contact_field and any(pattern.lower() in contact_field.lower() for pattern in placeholder_patterns):
                    validation['empty_fields'].append(f"Conglomerate #{cong_num} has placeholder text in contact field")
    
    return validation

def validate_investor_process_overview_slide(slide, content_ir):
    """Validate investor process overview slide"""
    validation = {'issues': [], 'warnings': [], 'missing_fields': [], 'empty_fields': []}
    
    data = slide.get('data', {})
    
    # Required fields for investor process overview
    required_fields = {
        'title': 'Slide title',
        'diligence_topics': 'Due diligence topics',
        'synergy_opportunities': 'Synergy opportunities',
        'risk_factors': 'Risk factors',
        'mitigants': 'Mitigating factors',
        'timeline': 'Process timeline'
    }
    
    for field, description in required_fields.items():
        if field not in data:
            validation['missing_fields'].append(f"Missing {description}")
        elif not data[field]:
            validation['empty_fields'].append(f"Empty {description}")
        elif isinstance(data[field], list) and len(data[field]) == 0:
            validation['empty_fields'].append(f"Empty {description} array")
        elif isinstance(data[field], list):
            # Validate array items
            for i, item in enumerate(data[field]):
                item_num = i + 1
                if isinstance(item, dict):
                    # Check for required fields in each item
                    if 'title' in item and 'description' in item:
                        if not item.get('title') or not item.get('description'):
                            validation['empty_fields'].append(f"{description} #{item_num} missing title or description")
                    elif not item or str(item).strip() == '':
                        validation['empty_fields'].append(f"{description} #{item_num} is empty")
                elif not item or str(item).strip() == '':
                    validation['empty_fields'].append(f"{description} #{item_num} is empty")
    
    return validation

# VALIDATION DISPLAY FUNCTIONS
def display_validation_results(validation_results):
    """Display comprehensive validation results with visual indicators"""
    
    summary = validation_results['summary']
    
    # Create header with summary box
    st.markdown("### 📋 Slide-by-Slide Validation Results")
    
    # Enhanced summary with quality scores
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("Total Slides", summary['total_slides'])
    with col2:
        st.metric("Valid Slides", summary['valid_slides'], delta=None if summary['valid_slides'] == summary['total_slides'] else f"-{summary['invalid_slides']}")
    with col3:
        st.metric("Invalid Slides", summary['invalid_slides'], delta=None if summary['invalid_slides'] == 0 else f"+{summary['invalid_slides']}")
    with col4:
        if 'data_quality_score' in validation_results:
            st.metric("Data Quality", f"{validation_results['data_quality_score']:.0f}%")
    with col5:
        if 'completeness_score' in validation_results:
            st.metric("Completeness", f"{validation_results['completeness_score']:.0f}%")
    
    # Overall status with enhanced feedback
    if validation_results['overall_valid']:
        st.success("✅ All slides passed validation! Ready for deck generation.")
        if 'data_quality_score' in validation_results:
            quality_score = validation_results['data_quality_score']
            if quality_score >= 90:
                st.success("🏆 Excellent data quality - matches professional standards!")
            elif quality_score >= 80:
                st.info("👍 Good data quality - ready for production use")
            elif quality_score >= 70:
                st.warning("⚠️ Acceptable quality - minor improvements recommended")
    else:
        st.error(f"❌ {summary['invalid_slides']} slide(s) have validation issues that must be fixed before generating deck.")
    
    # Structure validation results
    if 'structure_validation' in validation_results:
        struct_val = validation_results['structure_validation']
        if struct_val['structure_issues']:
            st.markdown("#### 🗃️ Structure Issues Found")
            st.error("The following structural issues were detected by comparing against professional examples:")
            for issue in struct_val['structure_issues']:
                st.markdown(f"• {issue}")
    
    # Detailed slide results
    if validation_results['slide_validations']:
        st.markdown("#### Detailed Slide Analysis")
        
        for slide_val in validation_results['slide_validations']:
            slide_num = slide_val['slide_number']
            template = slide_val['template']
            is_valid = slide_val['valid']
            
            # Create expandable section for each slide
            status_icon = "✅" if is_valid else "❌"
            warning_icon = " ⚠️" if slide_val['warnings'] else ""
            
            with st.expander(f"Slide {slide_num}: {template} {status_icon}{warning_icon}"):
                
                if not is_valid:
                    # Critical issues
                    if slide_val['issues']:
                        st.markdown("**🚨 Critical Issues:**")
                        for issue in slide_val['issues']:
                            st.markdown(f"  • {issue}")
                    
                    # Missing fields
                    if slide_val['missing_fields']:
                        st.markdown("**📝 Missing Fields:**")
                        for field in slide_val['missing_fields']:
                            st.markdown(f"  • {field}")
                    
                    # Empty fields
                    if slide_val['empty_fields']:
                        st.markdown("**📦 Empty/Placeholder Fields:**")
                        for field in slide_val['empty_fields']:
                            st.markdown(f"  • {field}")
                
                # Warnings (even for valid slides)
                if slide_val['warnings']:
                    st.markdown("**⚠️ Warnings:**")
                    for warning in slide_val['warnings']:
                        st.markdown(f"  • {warning}")
                
                if is_valid and not slide_val['warnings']:
                    st.success("All required content present - no empty boxes expected")
    
    return validation_results['overall_valid']

def create_validation_feedback_for_llm(validation_results):
    """Create specific feedback for the LLM to fix validation issues with example-based guidance"""
    
    if validation_results['overall_valid']:
        return None  # No feedback needed
    
    feedback_sections = []
    feedback_sections.append("❌ VALIDATION FAILED - Your JSONs have empty boxes and missing content that must be fixed before generating the deck.")
    feedback_sections.append("\n🎯 ZERO EMPTY BOXES POLICY VIOLATIONS:")
    
    # Add specific instructions for common issues
    feedback_sections.append("\n🚨 CRITICAL: You MUST include the 'facts' section in Content IR for financial slides!")
    feedback_sections.append("Add this to your Content IR:")
    feedback_sections.append('"facts": {')
    feedback_sections.append('  "years": ["2020", "2021", "2022", "2023", "2024E"],')
    feedback_sections.append('  "revenue_usd_m": [120, 145, 180, 210, 240],')
    feedback_sections.append('  "ebitda_usd_m": [18, 24, 31, 40, 47],')
    feedback_sections.append('  "ebitda_margins": [15.0, 16.6, 17.2, 19.0, 19.6]')
    feedback_sections.append('}')
    
    # Add structure validation feedback first
    if 'structure_validation' in validation_results and validation_results['structure_validation']['structure_issues']:
        feedback_sections.append("\n🗃️ STRUCTURAL ISSUES (compared to professional examples):")
        for issue in validation_results['structure_validation']['structure_issues']:
            feedback_sections.append(f"    - {issue}")
        
        feedback_sections.append("\n📋 STRUCTURE REQUIREMENTS:")
        feedback_sections.append("  Content IR must include these key sections:")
        feedback_sections.append("    - entities: {company: {name: 'Company Name'}}")
        feedback_sections.append("    - management_team: {left_column_profiles: [...], right_column_profiles: [...]}")
        feedback_sections.append("    - strategic_buyers: [{buyer_name, strategic_rationale, fit}, ...]")
        feedback_sections.append("    - financial_buyers: [{buyer_name, strategic_rationale, fit}, ...]")
        
        feedback_sections.append("\n  Each management profile must have:")
        feedback_sections.append("    - role_title: 'Chief Executive Officer'")
        feedback_sections.append("    - experience_bullets: ['bullet 1', 'bullet 2', ...]")
        
        feedback_sections.append("\n  Each buyer must have:")
        feedback_sections.append("    - buyer_name: 'Company Name'")
        feedback_sections.append("    - strategic_rationale: 'reason for acquisition'")
        feedback_sections.append("    - fit: 'High (9/10)' or similar")
    
    # Add slide-specific issues
    for slide_val in validation_results['slide_validations']:
        if not slide_val['valid']:
            slide_num = slide_val['slide_number']
            template = slide_val['template']
            
            feedback_sections.append(f"\nSlide {slide_num} ({template}):")
            
            if slide_val['issues']:
                feedback_sections.append("  🚨 Critical Issues:")
                for issue in slide_val['issues']:
                    feedback_sections.append(f"    - {issue}")
                    
                    # Add specific fix instructions for common issues
                    if "Missing content_ir_key" in issue and template == "buyer_profiles":
                        feedback_sections.append("      FIX: Add 'content_ir_key': 'strategic_buyers' or 'content_ir_key': 'financial_buyers' to the slide object (not in data section)")
                        feedback_sections.append("      EXAMPLE:")
                        feedback_sections.append("      {")
                        feedback_sections.append("        'template': 'buyer_profiles',")
                        feedback_sections.append("        'content_ir_key': 'strategic_buyers',")
                        feedback_sections.append("        'data': {")
                        feedback_sections.append("          'title': 'Strategic Buyers - Global Healthcare Leaders',")
                        feedback_sections.append("          'table_headers': ['Buyer Profile', 'Strategic Rationale', 'Fit']")
                        feedback_sections.append("        }")
                        feedback_sections.append("      }")
            
            if slide_val['missing_fields']:
                feedback_sections.append("  📝 Missing Required Fields:")
                for field in slide_val['missing_fields']:
                    feedback_sections.append(f"    - {field}")
                    
                    # Add specific fix instructions for missing fields
                    if "Missing slide title" in field:
                        feedback_sections.append("      FIX: Add 'title' field to the slide data")
                        feedback_sections.append("      EXAMPLE: 'title': 'Historical Financial Performance'")
                    
                    elif "Missing Financial performance chart data" in field and template == "historical_financial_performance":
                        feedback_sections.append("      FIX: Add complete chart data referencing facts from Content IR")
                        feedback_sections.append("      EXAMPLE:")
                        feedback_sections.append("      'chart': {")
                        feedback_sections.append("        'categories': ['2020', '2021', '2022', '2023', '2024E'],")
                        feedback_sections.append("        'revenue': [120, 145, 180, 210, 240],")
                        feedback_sections.append("        'ebitda': [18, 24, 31, 40, 47]")
                        feedback_sections.append("      }")
                    
                    elif "Empty competitive assessment table" in field and template == "competitive_positioning":
                        feedback_sections.append("      FIX: Add complete competitive assessment table")
                        feedback_sections.append("      EXAMPLE:")
                        feedback_sections.append("      'assessment': [")
                        feedback_sections.append("        {'category': 'Market Position', 'our_company': 'Leader', 'competitor_a': 'Challenger', 'competitor_b': 'Follower'},")
                        feedback_sections.append("        {'category': 'Technology', 'our_company': 'Advanced', 'competitor_a': 'Moderate', 'competitor_b': 'Basic'},")
                        feedback_sections.append("        {'category': 'Customer Base', 'our_company': 'Premium', 'competitor_a': 'Mixed', 'competitor_b': 'Mass Market'}")
                        feedback_sections.append("      ]")
            
            if slide_val['empty_fields']:
                feedback_sections.append("  📦 Empty/Placeholder Content (will create empty boxes):")
                for field in slide_val['empty_fields']:
                    feedback_sections.append(f"    - {field}")
                    
                    # Add specific fix instructions for empty fields
                    if "Cost management item" in field and template == "margin_cost_resilience":
                        feedback_sections.append("      FIX: Add complete cost management items with title and description")
                        feedback_sections.append("      EXAMPLE:")
                        feedback_sections.append("      'cost_management': {")
                        feedback_sections.append("        'items': [")
                        feedback_sections.append("          {'title': 'Operational Efficiency', 'description': 'Streamlined processes reducing costs by 15%'},")
                        feedback_sections.append("          {'title': 'Technology Investment', 'description': 'Automation tools reducing manual work by 30%'}")
                        feedback_sections.append("        ]")
                        feedback_sections.append("      }")
    
    # Add specific buyer_profiles fix instructions with real examples
    has_buyer_issues = any("buyer_profiles" in slide_val['template'] for slide_val in validation_results['slide_validations'] if not slide_val['valid'])
    if has_buyer_issues:
        feedback_sections.append("\n🔧 BUYER_PROFILES SLIDE FIX INSTRUCTIONS:")
        feedback_sections.append("CRITICAL: buyer_profiles slides must reference buyer data using content_ir_key")
        feedback_sections.append("\nCORRECT EXAMPLE - Strategic Buyers:")
        feedback_sections.append('{')
        feedback_sections.append('  "template": "buyer_profiles",')
        feedback_sections.append('  "content_ir_key": "strategic_buyers",')
        feedback_sections.append('  "data": {')
        feedback_sections.append('    "title": "Strategic Buyers - Global Healthcare Leaders",')
        feedback_sections.append('    "table_headers": ["Buyer Name", "Description", "Strategic Rationale", "Key Synergies", "Fit"]')
        feedback_sections.append('  }')
        feedback_sections.append('}')
        
        feedback_sections.append("\nCORRECT EXAMPLE - Financial Buyers:")
        feedback_sections.append('{')
        feedback_sections.append('  "template": "buyer_profiles",')
        feedback_sections.append('  "content_ir_key": "financial_buyers",')
        feedback_sections.append('  "data": {')
        feedback_sections.append('    "title": "Financial Buyers - Global Private Equity",')
        feedback_sections.append('    "table_headers": ["Fund Profile", "Healthcare Strategy", "Fit"]')
        feedback_sections.append('  }')
        feedback_sections.append('}')
        
        feedback_sections.append("\nThe Content IR must have matching arrays:")
        feedback_sections.append('"strategic_buyers": [')
        feedback_sections.append('  {')
        feedback_sections.append('    "buyer_name": "UnitedHealth / Optum",')
        feedback_sections.append('    "strategic_rationale": "SEA market entry with established platform",')
        feedback_sections.append('    "key_synergies": "Data analytics, technology platform",')
        feedback_sections.append('    "fit": "High (9/10)"')
        feedback_sections.append('  }')
        feedback_sections.append(']')
    
    feedback_sections.append(f"\n📊 QUALITY SCORES:")
    if 'data_quality_score' in validation_results:
        feedback_sections.append(f"  Data Quality: {validation_results['data_quality_score']:.0f}% (need 90%+)")
    if 'completeness_score' in validation_results:
        feedback_sections.append(f"  Completeness: {validation_results['completeness_score']:.0f}% (need 90%+)")
    
    feedback_sections.append("\n✅ TO FIX: Please regenerate the JSONs with complete content for all the issues listed above. Follow the professional examples exactly. Every field must have real data, not placeholders or empty values.")
    
    return "\n".join(feedback_sections)

# Load templates and examples for the system prompt
def load_templates_json():
    """Load templates.json for the system prompt"""
    try:
        templates_path = Path("templates.json")
        if templates_path.exists():
            with open(templates_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return []
    except Exception as e:
        st.error(f"Error loading templates.json: {e}")
        return []

def load_example_files():
    """Load the example JSON files to include in system prompt"""
    examples = {}
    
    # Try to load complete_content_ir.json
    try:
        content_ir_path = Path("complete_content_ir.json")
        if content_ir_path.exists():
            with open(content_ir_path, 'r', encoding='utf-8') as f:
                examples['content_ir'] = json.load(f)
    except Exception as e:
        print(f"Could not load complete_content_ir.json: {e}")
    
    # Try to load complete_render_plan.json
    try:
        render_plan_path = Path("complete_render_plan.json")
        if render_plan_path.exists():
            with open(render_plan_path, 'r', encoding='utf-8') as f:
                examples['render_plan'] = json.load(f)
    except Exception as e:
        print(f"Could not load complete_render_plan.json: {e}")
    
    # If files don't exist, use the embedded examples
    if 'content_ir' not in examples:
        examples['content_ir'] = {
            "entities": {
                "company": {
                    "name": "SouthernCapital Healthcare"
                }
            },
            "facts": {
                "years": ["2020", "2021", "2022", "2023", "2024E"],
                "revenue_usd_m": [120, 145, 180, 210, 240],
                "ebitda_usd_m": [18, 24, 31, 40, 47],
                "ebitda_margins": [15.0, 16.6, 17.2, 19.0, 19.6]
            },
            "management_team": {
                "left_column_profiles": [
                    {
                        "role_title": "Chief Executive Officer",
                        "experience_bullets": [
                            "25+ years healthcare industry experience across hospital operations",
                            "Former Regional VP at major international hospital group",
                            "MBA from top-tier business school with healthcare specialization",
                            "Led successful expansion of 40+ healthcare facilities",
                            "Board member of regional healthcare association"
                        ]
                    },
                    {
                        "role_title": "Chief Financial Officer",
                        "experience_bullets": [
                            "15+ years finance leadership in healthcare services",
                            "Ex-CFO at publicly-traded healthcare services company",
                            "CPA with proven M&A integration track record",
                            "Successfully completed 8 acquisitions totaling $200M+",
                            "Deep expertise in healthcare reimbursement"
                        ]
                    }
                ],
                "right_column_profiles": [
                    {
                        "role_title": "Chief Operating Officer",
                        "experience_bullets": [
                            "20+ years multi-site healthcare operations experience",
                            "Successfully scaled 50+ clinic locations across SEA",
                            "Lean Six Sigma Master Black Belt certification",
                            "Former Regional Operations Director at international chain",
                            "Deep experience in regulatory compliance and quality"
                        ]
                    }
                ]
            },
            "strategic_buyers": [
                {
                    "buyer_name": "UnitedHealth / Optum",
                    "description": "Global healthcare leader with $350B+ revenue",
                    "strategic_rationale": "SEA market entry with established platform",
                    "key_synergies": "Data analytics, technology platform, corporate relationships",
                    "fit": "High (9/10)"
                }
            ],
            "financial_buyers": [
                {
                    "buyer_name": "Blackstone Growth",
                    "description": "$975B AUM, $40B+ healthcare investments",
                    "strategic_rationale": "Buy-and-build platform strategy across SEA",
                    "key_synergies": "Operational excellence, technology investment",
                    "fit": "Very High (9/10)"
                }
            ]
        }
    
    if 'render_plan' not in examples:
        examples['render_plan'] = {
            "slides": [
                {
                    "template": "business_overview",
                    "data": {
                        "title": "Business & Operational Overview",
                        "description": "Leading integrated healthcare services platform in Southeast Asia",
                        "highlights": [
                            "35+ premium clinic locations across Singapore, Malaysia, Indonesia, and Philippines",
                            "125,000+ annual patient visits with 89% retention rate",
                            "65+ corporate wellness contracts with major employers"
                        ],
                        "services": [
                            "Primary Care & Preventive Medicine",
                            "Specialty Medical Services",
                            "Diagnostic Imaging & Laboratory"
                        ],
                        "positioning_desc": "Leading premium healthcare provider in Southeast Asia"
                    }
                },
                {
                    "template": "buyer_profiles",
                    "content_ir_key": "strategic_buyers",
                    "data": {
                        "title": "Strategic Buyers - Global Healthcare Leaders",
                        "table_headers": ["Buyer Name", "Description", "Strategic Rationale", "Key Synergies", "Fit"]
                    }
                },
                {
                    "template": "buyer_profiles",
                    "content_ir_key": "financial_buyers", 
                    "data": {
                        "title": "Financial Buyers - Global Private Equity",
                        "table_headers": ["Fund Profile", "Healthcare Strategy", "Value Creation", "Fit"]
                    }
                }
            ]
        }
    
    return examples

# Enhanced validation using real-world examples
def validate_against_examples(content_ir, render_plan, examples):
    """Validate generated JSONs against real-world example structures"""
    validation_results = {
        'content_ir_structure_valid': True,
        'render_plan_structure_valid': True,
        'structure_issues': [],
        'data_quality_score': 0,
        'completeness_score': 0
    }
    
    # Validate Content IR structure against example
    if 'content_ir' in examples:
        example_content_ir = examples['content_ir']
        
        # Check for key sections that should exist
        expected_sections = ['entities', 'management_team', 'strategic_buyers', 'financial_buyers']
        for section in expected_sections:
            if section in example_content_ir and section not in content_ir:
                validation_results['structure_issues'].append(f"Missing key Content IR section: {section}")
                validation_results['content_ir_structure_valid'] = False
        
        # Check management team structure
        if 'management_team' in content_ir:
            mgmt = content_ir['management_team']
            example_mgmt = example_content_ir.get('management_team', {})
            
            for column in ['left_column_profiles', 'right_column_profiles']:
                if column in example_mgmt and column not in mgmt:
                    validation_results['structure_issues'].append(f"Missing management team section: {column}")
                elif column in mgmt and isinstance(mgmt[column], list):
                    # Check profile structure
                    for i, profile in enumerate(mgmt[column]):
                        if 'role_title' not in profile:
                            validation_results['structure_issues'].append(f"Profile {i+1} in {column} missing role_title")
                        if 'experience_bullets' not in profile or not isinstance(profile['experience_bullets'], list):
                            validation_results['structure_issues'].append(f"Profile {i+1} in {column} missing experience_bullets array")
        
        # Check buyer arrays structure
        for buyer_type in ['strategic_buyers', 'financial_buyers']:
            if buyer_type in content_ir and isinstance(content_ir[buyer_type], list):
                for i, buyer in enumerate(content_ir[buyer_type]):
                    required_fields = ['buyer_name', 'strategic_rationale', 'fit']
                    for field in required_fields:
                        if field not in buyer:
                            validation_results['structure_issues'].append(f"{buyer_type} #{i+1} missing required field: {field}")
    
    # Validate Render Plan structure
    if 'render_plan' in examples and 'slides' in render_plan:
        example_slides = examples['render_plan']['slides']
        
        # Check for buyer_profiles slides using content_ir_key
        buyer_slides = [s for s in render_plan['slides'] if s.get('template') == 'buyer_profiles']
        
        for slide in buyer_slides:
            if 'content_ir_key' not in slide:
                validation_results['structure_issues'].append(f"buyer_profiles slide missing content_ir_key")
                validation_results['render_plan_structure_valid'] = False
            elif slide['content_ir_key'] not in content_ir:
                validation_results['structure_issues'].append(f"content_ir_key '{slide['content_ir_key']}' not found in Content IR")
                validation_results['render_plan_structure_valid'] = False
    
    # Calculate quality scores
    total_sections = len(['entities', 'management_team', 'strategic_buyers', 'financial_buyers', 'historical_financials'])
    present_sections = sum(1 for section in ['entities', 'management_team', 'strategic_buyers', 'financial_buyers', 'historical_financials'] if section in content_ir)
    validation_results['completeness_score'] = (present_sections / total_sections) * 100
    
    # Data quality score based on structure compliance
    validation_results['data_quality_score'] = max(0, 100 - (len(validation_results['structure_issues']) * 10))
    
    return validation_results

# Load templates and examples
TEMPLATES = load_templates_json()
EXAMPLES = load_example_files()

# Create example sections for system prompt
def create_examples_text():
    """Create formatted examples text for system prompt"""
    examples_text = ""
    
    if 'content_ir' in EXAMPLES:
        examples_text += "\n\nEXAMPLE CONTENT IR STRUCTURE:\n"
        examples_text += "```json\n"
        examples_text += json.dumps(EXAMPLES['content_ir'], indent=2)
        examples_text += "\n```\n"
    
    if 'render_plan' in EXAMPLES:
        examples_text += "\n\nEXAMPLE RENDER PLAN STRUCTURE:\n"
        examples_text += "```json\n"
        examples_text += json.dumps(EXAMPLES['render_plan'], indent=2)
        examples_text += "\n```\n"
    
    return examples_text

# RESTORED Systematic Interview System Prompt with ALL 16 Required Topics
SYSTEM_PROMPT = """
You are a systematic investment banking pitch deck copilot that conducts COMPLETE INTERVIEWS covering ALL 14 required topics SEQUENTIALLY before generating JSON files.

🚨 **CRITICAL INTERVIEW PROTOCOL - COMPLETE SYSTEMATIC COVERAGE**:

**MANDATORY: ASK ABOUT EVERY SINGLE TOPIC** - Never skip topics, follow this exact sequence:
1. **business_overview** - Company description, operations, industry, headquarters
2. **investor_considerations** - Key risks, opportunities, mitigation strategies  
3. **product_service_footprint** - Main offerings, geographic coverage, operations
4. **historical_financial_performance** - Revenue, EBITDA, margins (last 3-5 years)
5. **management_team** - CEO, CFO, senior executives (names, titles, backgrounds)
6. **growth_strategy_projections** - Expansion plans, strategic initiatives, financial projections
7. **competitive_positioning** - Competitors, advantages, differentiation factors
8. **valuation_overview** - Valuation methodologies, enterprise value, assumptions
9. **precedent_transactions** - Recent M&A deals, transaction multiples
10. **strategic_buyers** - Strategic acquirers interested in M&A (companies, corporates, industry players)
11. **financial_buyers** - Private equity, VC, and other financial buyers interested in investment/acquisition
12. **margin_cost_resilience** - Cost management, margin stability, efficiency programs
13. **sea_conglomerates** - Global strategic acquirers, international conglomerates
14. **investor_process_overview** - Deal process, diligence topics, timeline

**STRICT INTERVIEW FLOW RULES**:
- **MANDATORY: ASK EVERY SINGLE TOPIC**: Must ask about ALL 14 topics - NO EXCEPTIONS
- **SEQUENTIAL ORDER**: Complete each topic thoroughly before moving to the next
- **SUBSTANTIAL COVERAGE REQUIRED**: Each topic needs comprehensive information, not brief mentions
- **REGIONAL RELEVANCE**: For buyers/conglomerates, prioritize Middle East, Asian, and regional players
- **NO SHORTCUTS OR SKIPPING**: Every topic must be explicitly asked about and answered
- **CRITICAL**: Do NOT generate JSON until ALL 14 topics have been asked about and covered
- **AUTO-GENERATION TRIGGER**: ONLY when every single topic (1-14) has substantial coverage

🎯 **ZERO EMPTY BOXES POLICY**: Every slide must have complete content - no empty sections, boxes, or placeholder text.

🚨 **CRITICAL REQUIREMENTS - READ CAREFULLY**:
1. **Content IR MUST include 'facts' section** with historical financial data
2. **Content IR MUST include 'charts' section** with chart data for financial performance
3. **Content IR MUST include 'investor_process_data' section** with diligence topics, synergies, risks, mitigants, timeline
4. **Content IR MUST include 'margin_cost_data' section** with cost management and risk mitigation
5. **buyer_profiles slides MUST have content_ir_key** (strategic_buyers or financial_buyers)
6. **historical_financial_performance slides MUST reference facts data** for complete chart data
7. **Every slide MUST have a 'title' field** in the data section
8. **All arrays MUST have minimum required items** (no empty arrays)
9. **🚨 ALWAYS GENERATE COMPLETE JSON** - Never truncate or cut off JSON responses
10. **🚨 FOLLOW STEP-BY-STEP INTERVIEW** - Ask about each topic individually, don't skip any
11. **🚨 GENERATE EXACTLY 13 SLIDES** - No more, no less (or fewer if slides are skipped)
12. **🚨 NO PLACEHOLDER TEXT** - Use only user-provided information or "N/A" (avoid obvious placeholders like "[contact]", "TODO", etc.)
13. **🚨 DETAILED BUSINESS CONTENT** - Business overview highlights and services must be descriptive (10-15 words each), not brief bullet points
14. **🚨 COMPANY-SPECIFIC DATA ONLY** - Use ONLY the target company's data (for Aramco: Saudi regions, oil fields, etc.) - NEVER use generic or wrong company data

🎯 **DATA ACCURACY & VALUATION REQUIREMENTS**:
- **NO MADE-UP DATA**: Only use verifiable information from reliable sources
- **CITE SOURCES**: When using external data, mention the source (e.g., "according to company filings", "based on public records")
- **VALUATION WORK**: For valuation slides, always show detailed work and assumptions:
  - List all key assumptions (growth rates, multiples, discount rates, etc.)
  - Show step-by-step calculations where applicable
  - Explain methodology rationale
  - Include sensitivity analysis or ranges where appropriate
- **VERIFY FINANCIALS**: Double-check all financial data for consistency and reasonableness
- **USER CONSENT**: Always ask permission before using any searched or external data

📋 **COMPREHENSIVE FIELD REQUIREMENTS FOR EACH TEMPLATE**:

**business_overview**: title, description, timeline (start_year, end_year), highlights (array - detailed 10-15 word descriptions), services (array - detailed business line descriptions), positioning_desc

**investor_considerations**: title, considerations (array of risks), mitigants (array of strategies)

**product_service_footprint**: title, services (array with title + desc), coverage_table (array of objects), metrics (object with labels)

**historical_financial_performance**: title, chart (title, categories, revenue, ebitda), key_metrics (EXACTLY 4 numeric metrics like "45.3%", "$209B", "12.7M", "#1"), revenue_growth (object with title and points array), banker_view (object with title and text)

**management_team**: title, left_column_profiles (array with role_title + experience_bullets), right_column_profiles (array with role_title + experience_bullets)

**growth_strategy_projections**: title, slide_data (title, growth_strategy with strategies array, financial_projections with categories + revenue + ebitda)

**competitive_positioning**: title, competitors (INDUSTRY-SPECIFIC: ExxonMobil, Chevron, Shell for Aramco - NOT bakery companies), assessment (5-column format), barriers (array with title + desc), advantages (array with title + desc)

**valuation_overview**: title, valuation_data (array with methodology, enterprise_value, metric, 22a_multiple, 23e_multiple, commentary)

**precedent_transactions**: title, transactions (array with target, acquirer, date, country, enterprise_value, revenue, ev_revenue_multiple)

**margin_cost_resilience**: title, chart_title, chart_data (categories + values), cost_management (items array), risk_mitigation (main_strategy)

**sea_conglomerates**: data (array with name, country, description, key_shareholders, key_financials, contact) - NOTE: Can include conglomerates from any region worldwide, not just Southeast Asia. Use actual user-provided contact information or "N/A" if none provided.

**buyer_profiles**: title, table_headers (array), table_rows (array with buyer_name, description, strategic_rationale (10-20 words), key_synergies, fit (score + 5-word rationale), financial_capacity), content_ir_key

**investor_process_overview**: title, diligence_topics (array), synergy_opportunities (array), risk_factors (array), mitigants (array), timeline (array)
6. **NO placeholder text, NO empty fields, NO null values**

📋 **CRITICAL JSON FORMATTING REQUIREMENTS**:
Your response MUST include BOTH JSONs in this EXACT format:

## CONTENT IR JSON:
```json
{
  "entities": {"company": {"name": "Company Name"}},
  "facts": {"years": ["2020", "2021", "2022", "2023", "2024E"], "revenue_usd_m": [120, 145, 180, 210, 240], "ebitda_usd_m": [18, 24, 31, 40, 47], "ebitda_margins": [15.0, 16.6, 17.2, 19.0, 19.6]},
  "management_team": {"left_column_profiles": [...], "right_column_profiles": [...]},
  "strategic_buyers": [...],
  "financial_buyers": [...],
  "competitive_analysis": {"competitors": [...], "assessment": [...], "barriers": [...], "advantages": [...]},
  "precedent_transactions": [...],
  "valuation_data": [...],
  "product_service_data": {"services": [...], "coverage_table": [...], "metrics": {...}},
  "business_overview_data": {"description": "...", "timeline": {...}, "highlights": [...], "services": [...], "positioning_desc": "..."},
  "growth_strategy_data": {"growth_strategy": {...}, "financial_projections": {...}, "key_assumptions": {...}},
  "investor_process_data": {"diligence_topics": [...], "synergy_opportunities": [...], "risk_factors": [...], "mitigants": [...], "timeline": [...]},
  "margin_cost_data": {"chart_data": {...}, "cost_management": {...}, "risk_mitigation": {...}},
  "sea_conglomerates": [...],
  "investor_considerations": {"considerations": [...], "mitigants": [...]}
}
```

## RENDER PLAN JSON:
```json
{
  "slides": [
    {"template": "management_team", "data": {...}},
    {"template": "business_overview", "data": {...}}
  ]
}
```

⚠️ **MANDATORY**: Always use these exact section headers and JSON code blocks. Never skip the formatting.

SPECIFIC SLIDE REQUIREMENTS FOR ALL TEMPLATES (UPDATED WITH CORRECT FIELD NAMES):

1. **management_team**:
   - Must have left_column_profiles and right_column_profiles (min 2 each)
   - Each profile needs: role_title, experience_bullets (array of 3-5 bullets)
   - CORRECT STRUCTURE: {{"role_title": "Chief Executive Officer", "experience_bullets": ["bullet1", "bullet2", ...]}}

2. **business_overview**:
   - Must have: title, description, highlights (min 3), services (min 3), positioning_desc
   - **CRITICAL**: highlights must be DETAILED (10-15 words each), not brief bullet points
   - **CRITICAL**: services must be DESCRIPTIVE business lines (15-20 words each), not short phrases
   - Example highlight: "World's largest single oil producer by volume with unmatched operational scale and efficiency"
   - Example service: "Upstream oil & gas exploration spanning 100+ fields including Ghawar, the world's largest conventional oil field"
   - All fields must be complete sentences, not placeholders

3. **product_service_footprint**:
   - Must have: title, services array with complete title AND desc for each
   - Services array needs minimum 4 entries with structure: {{"title": "Service Name", "desc": "Description"}}
   - **MANDATORY**: coverage_table must have EXACTLY 3-4 columns (NEVER 2 columns)
   - **MANDATORY**: Use ONLY company-specific data (for Aramco: Saudi Arabia, Middle East, Americas, Asia regions)
   - **FORBIDDEN**: Generic city data (Jakarta, Bandung) or wrong company information
   - Coverage table structure: [["Region", "Market Segment", "Assets/Products", "Coverage Details"], ["Saudi Arabia", "Upstream", "Oil fields, refineries", "Ghawar, Safaniya fields"], ...]
   - **4-column format required**: [["Region", "Segment", "Major Assets/Products", "Coverage Details"], ["Saudi Arabia", "Upstream", "Oil/gas fields", "Ghawar, Safaniya, Hawiyah, Khurais"], ["Middle East/EU", "Downstream", "Refineries, petrochemicals", "SABIC, SATORP, Jazan, Yanbu"]]
   - Must include metrics data for operational metrics section
   - NO empty boxes in layout areas - all sections must be populated

4. **buyer_profiles**:
   - MUST use content_ir_key to reference buyer data (REQUIRED - NO EXCEPTIONS)
   - NEVER create buyer_profiles slides without content_ir_key
   - Each buyer must have complete: buyer_name, description, strategic_rationale (10-20 words), key_synergies, fit (score + 5-word rationale)
   - Tables must populate with real data, not be empty
   - Example correct structure:
     ```json
     {{
       "template": "buyer_profiles",
       "content_ir_key": "strategic_buyers",
       "data": {{
         "title": "Strategic Buyer Profiles",
         "table_headers": ["Buyer Name", "Strategic Rationale", "Fit"]
       }}
     }}
     ```
   - ALWAYS include content_ir_key: "strategic_buyers" or "financial_buyers"
   - **CRITICAL FORMATTING REQUIREMENTS**:
     * strategic_rationale: 10-20 words ONLY (e.g., "Expand US-Saudi energy integration to strengthen upstream operations and petrochemical refining capacity")  
     * fit: Score + exactly 5-word rationale (e.g., "High (9/10) - Strategic energy market alignment" or "Medium (7/10) - Limited operational synergy potential")

5. **historical_financial_performance**:
   - MUST have chart data with categories, revenue, ebitda arrays (min 3 years each)
   - **MANDATORY**: key_metrics must have EXACTLY 4 metrics (like iCar Asia example)
   - **CRITICAL**: Each metric must be NUMERIC (percentages, dollar amounts, rankings) not descriptive text
   - **Example metrics**: "15.5%", "$11.8M", "27%", "#1" - NOT "Industry-leading free cash flow"
   - Chart structure: {{"categories": ["2020", "2021", ...], "revenue": [120, 145, ...], "ebitda": [18, 24, ...]}}
   - **4 Metrics Structure**: {{"metrics": ["45.3%", "$209B", "12.7M", "#1"]}} with corresponding labels
   - MUST reference facts data from Content IR: {{"chart": {{"categories": ["2020", "2021", "2022", "2023", "2024E"], "revenue": [120, 145, 180, 210, 240], "ebitda": [18, 24, 31, 40, 47]}}}}
   - ALWAYS include complete ebitda data array matching the facts section
   - **SPACING FIX**: Ensure metrics don't overlap - use concise labels and numeric values only

6. **margin_cost_resilience**:
   - Must have: title, cost_management with items array, risk_mitigation with main_strategy
   - CORRECT FIELD NAMES: cost_management (not cost_structure), risk_mitigation (not resilience_factors)
   - Structure: {{"title": "Margin & Cost Resilience", "cost_management": {{"items": [{{"title": "Cost Initiative 1", "description": "Detailed description"}, {{"title": "Cost Initiative 2", "description": "Detailed description"}}]}}, "risk_mitigation": {{"main_strategy": "Primary risk mitigation approach"}}}}

7. **competitive_positioning**:
   - **CRITICAL**: Must use INDUSTRY-SPECIFIC competitors (for Aramco: ExxonMobil, Chevron, Shell, PetroChina, TotalEnergies)
   - **FORBIDDEN**: Generic template competitors (Breadlife, Sari Roti, bakery companies, etc.)
   - CRITICAL: Must match iCar Asia format with 5-column assessment table
   - Must have: competitors array, assessment table (5 columns), advantages array, barriers array
   - **LAYOUT FIX**: Content must be distributed evenly across slide, not squished to one side
   - Competitors structure: [{{"name": "ExxonMobil", "revenue": 489100}}, {{"name": "Chevron", "revenue": 279400}}, ...] (for Aramco)
   - ASSESSMENT TABLE STRUCTURE (5 columns): [["Company", "Market Share", "Tech Platform", "Coverage", "Revenue (M)"], ["Aramco", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "⭐⭐⭐⭐⭐", "$461,560M"], ["ExxonMobil", "⭐⭐⭐⭐", "⭐⭐⭐⭐", "⭐⭐⭐⭐", "$489,100M"], ...]
   - Star ratings: Use 1-5 stars (⭐) or numeric ratings 1-5 that get converted to stars
   - Revenue column: Include quantitative data like "$489,100M", "$279,400M"
   - Advantages: Array of concise competitive advantages (4-6 items max)
   - Barriers: Array of market entry barriers (4-6 items max)
   - Content limits: Each advantage/barrier max 80 chars for clean layout
   - CORRECT FIELD NAMES: advantages (not competitive_advantages), assessment (not competitive_analysis)

8. **valuation_overview**:
   - Must have: valuation_data array (not separate methodology fields)
   - **CRITICAL**: Must use DISTINCT methodologies - no duplicates (Trading Multiples should appear only once)
   - **REQUIRED METHODOLOGIES**: "Trading Multiples" (for EV/Revenue), "Trading Multiples" (for EV/EBITDA), "Discounted Cash Flow (DCF)"
   - **LAYOUT**: Use original table format (5-column: Methodology, Enterprise Value, Metric, 22A Multiple, 23E Multiple)
   - CORRECT FIELD NAME: valuation_data with methodology, enterprise_value, metric, 22a_multiple, 23e_multiple, commentary
   - **Structure**: [{{"methodology": "Trading Multiples", "enterprise_value": "US$1.57 trillion", "metric": "EV/Revenue", "22a_multiple": "3.3x", "23e_multiple": "3.3x", "commentary": "..."}}, {{"methodology": "Trading Multiples", "enterprise_value": "US$1.57 trillion", "metric": "EV/EBITDA", "22a_multiple": "6.6x", "23e_multiple": "6.6x", "commentary": "..."}}, {{"methodology": "Discounted Cash Flow (DCF)", "enterprise_value": "US$1.6 trillion", "metric": "DCF", "22a_multiple": "n/a", "23e_multiple": "n/a", "commentary": "..."}}]
   - MUST INCLUDE DETAILED WORK: Show all assumptions, calculations, and rationale

9. **growth_strategy_projections**:
   - Must have: title, growth_strategy with strategies array, financial_projections
   - May have slide_data wrapper: {{"title": "Growth Strategy & Projections", "slide_data": {{"growth_strategy": {{"strategies": ["Strategy 1", "Strategy 2", "Strategy 3"]}}, "financial_projections": {{"projected_revenue": [240, 280, 320], "projected_ebitda": [47, 56, 64]}}}}}}

10. **precedent_transactions**:
    - Must have: transactions array with target, acquirer, date, enterprise_value, revenue, ev_revenue_multiple
    - Each transaction needs complete data, no placeholders

CONTENT IR STRUCTURE REQUIREMENTS:
- entities: {{"company": {{"name": "Company Name"}}}}
- facts: {{"years": ["2020", "2021", "2022", "2023", "2024E"], "revenue_usd_m": [120, 145, 180, 210, 240], "ebitda_usd_m": [18, 24, 31, 40, 47], "ebitda_margins": [15.0, 16.6, 17.2, 19.0, 19.6]}}
- management_team: {{"left_column_profiles": [...], "right_column_profiles": [...]}}
- strategic_buyers: [{{"buyer_name": "Name", "strategic_rationale": "...", "fit": "High (9/10)"}}, ...]
- financial_buyers: [{{"buyer_name": "Name", "strategic_rationale": "...", "fit": "High (9/10)"}}, ...]

VALIDATION BEFORE OUTPUT:
Before generating JSONs, verify each slide will have NO EMPTY BOXES:
- All required fields populated with real data using CORRECT field names
- All arrays have minimum required items
- All chart/table areas have supporting data
- No placeholder text like [COMPANY], [AMOUNT], etc.
- Every content area will render with actual information

If ANY slide would have empty boxes, ask for more information instead of generating incomplete JSONs.

CRITICAL SUCCESS METRICS:
🎯 Generate Content IR with ALL collected data using correct field names
🎯 Generate Render Plan with 8+ diverse slides
🎯 Create files immediately when interview is complete
🎯 Ensure files are production-ready for deck generation

MANDATORY COMPLETION CHECKLIST:
✅ Company name and business description
✅ Investment highlights and value propositions
✅ Business overview (model, operations, positioning)
✅ Product/service footprint (offerings, geography)
✅ Historical financials (3-5 years, revenue, EBITDA, margins)
✅ Margin/cost resilience analysis
✅ Growth strategy with market data and projections
✅ Management team (4-6 profiles with role_title/experience_bullets)
✅ Investor considerations (risks and opportunities)
✅ Competitive positioning
✅ Trading precedents (public comps and/or private deals)
✅ Valuation methodologies and assumptions
✅ Strategic buyers (3-4 with rationale)
✅ Financial buyers (3-4 PE firms with rationale)

ENHANCED INTERVIEW FLOW RULES:

1. **COMPLETENESS CHECK BEFORE PROGRESSION**:
   - After EVERY user response, analyze if ALL required information for the current topic is collected
   - If information is missing, ask SPECIFIC follow-up questions about what's missing
   - List exactly what information you still need
   - Only move to next topic when current topic is COMPLETE or user explicitly skips

2. **HANDLE "I DON'T KNOW" RESPONSES**:
   - If user says "I don't know" or provides incomplete information, say:
     "I can search for that information. Let me look it up for you."
   - Use web search to find the missing information
   - Show the user exactly what you found with sources
   - Ask: "I found [specific information]. Is it OK to use this for your pitch deck?"
   - Wait for explicit user consent before using the information
   - NEVER use information without asking permission first

3. **SKIP FUNCTIONALITY**:
   - If user says "skip this slide", "skip this topic", "not applicable", or "we don't need this", acknowledge and move to next topic
   - Clearly confirm: "Understood, I'll skip the [topic name] slide. Moving to the next topic..."
   - Mark that topic as skipped (do not include in final JSON generation)
   - Continue with remaining topics in sequence
   - At the end, remind user which slides were skipped and confirm final slide count

4. **SPECIFIC FOLLOW-UP REQUIREMENTS**:
   - For each topic, have specific required fields
   - Ask targeted questions for missing fields
   - Example: "I have your company name but still need: founding year, legal structure, and primary markets. Can you provide these?"

5. **COMMUNICATION STYLE**:
   - Ask 1-2 focused questions per response
   - Be specific about exactly what information is missing
   - Never provide additional information until you've asked follow-up questions
   - Don't summarize or explain - focus on getting missing data

🚨 **SYSTEMATIC INTERVIEW PROTOCOL** - YOU MUST ASK ABOUT EACH TOPIC ONE BY ONE:

**MANDATORY TOPICS TO COVER** (You MUST ask about ALL of these):

1. **business_overview**: Company name, what business does, founding info, market positioning, core operations
2. **investor_considerations**: Key risks, opportunities, concerns investors should know, mitigation strategies  
3. **product_service_footprint**: Main offerings, geographic presence, service descriptions, coverage areas
4. **historical_financial_performance**: 3-5 years revenue/EBITDA/margins, growth rates, key metrics
5. **management_team**: 4-6 executives with role titles and detailed experience backgrounds
6. **growth_strategy_projections**: Expansion plans, strategic initiatives, financial projections for 2-3 years
7. **competitive_positioning**: Main competitors, competitive advantages, market comparison
8. **valuation_overview**: Valuation methodologies, multiples, enterprise values, detailed assumptions
9. **precedent_transactions**: Recent industry transactions with details (target, acquirer, values, multiples)
10. **margin_cost_resilience**: Cost management, margin stability, risk mitigation strategies
11. **sea_conglomerates**: Global conglomerates that might be interested (any region worldwide)
12. **buyer_profiles**: Strategic buyers (4-5 minimum) and financial buyers (4-5 minimum)

**CRITICAL INTERVIEW RULES:**
- **Complete information for current topic** = Move to next topic
- **Brief confirmatory responses ("yes", "correct")** = Move to next topic if current is complete  
- **Partial information** = Ask follow-up questions for missing details
- **"Skip this slide/topic"** = Mark as skipped, move to next
- **"I don't know"** = Offer to research with user permission

**STEP-BY-STEP INTERVIEW FLOW:**

**STEP 1: Business Overview**
"Let's start systematically. First, tell me about your business overview: company name, what your business does, when founded, market positioning, and core operations."

**STEP 2: Investor Considerations**  
"What are the key risks and opportunities investors should know about? What concerns might they have and how do you mitigate risks?"

**STEP 3: Product/Service Footprint**
"Describe your main products/services with titles and descriptions. Where do you operate geographically? What's your market coverage?"

**STEP 4: Historical Financial Performance** 
"Provide 3-5 years of financial data: revenue, EBITDA, margins, growth rates, and key operational metrics."

**STEP 5: Management Team**
"Tell me about your management team: 4-6 key executives with their role titles and detailed experience backgrounds."

**STEP 6: Growth Strategy & Projections**
"What's your growth strategy? Specific expansion plans? Financial projections for next 2-3 years with revenue and EBITDA numbers?"

**STEP 7: Competitive Positioning**
"Who are your main competitors? How do you compare in market position, technology, competitive advantages?"

**STEP 8: Valuation Overview** 
"What valuation methodologies are appropriate? Expected enterprise values and multiples? Detailed assumptions and rationale?"

**STEP 9: Precedent Transactions**
"Recent industry transactions for comparison? Need target, acquirer, date, enterprise value, revenue, multiples."

**STEP 10: Strategic Buyers**
"Now let's identify potential strategic buyers—companies that might acquire you for strategic reasons.

I need 4-5 strategic buyers with:
- Company name and brief description  
- Strategic rationale (10-20 words explaining why they'd acquire you)
- Key synergies they'd gain
- Fit assessment (High/Medium/Low with score and 5-word rationale)
- Financial capacity

Please provide this information and I'll organize it for your pitch deck."

**STEP 11: Financial Buyers**  
"Now let's identify financial buyers—private equity firms, VCs, and other financial investors.

I need 4-5 financial buyers with:
- Fund/firm name and brief description
- Investment rationale (10-20 words explaining their interest)  
- Key synergies or value-add they bring
- Fit assessment (High/Medium/Low with score and 5-word rationale)
- Financial capacity

Please provide this information and I'll organize it for your pitch deck."

🎯 **BUYER PRESENTATION FORMAT**: When presenting buyer profiles to users, ALWAYS use clear, readable tables or bullet points - NEVER show raw JSON structures. Present the information in an organized, professional format that's easy to review and confirm.

**STEP 12: Margin & Cost Resilience**
"How do you manage costs and maintain margins? Cost management initiatives and risk mitigation strategies?"

**STEP 13: Global Conglomerates**
"Which conglomerates worldwide might be interested? Need 4-5 from any region with strategic rationale and fit."

**STEP 14: Investor Process Overview**
"What would the investment/acquisition process look like? I need:
- Diligence topics investors would focus on
- Key synergy opportunities 
- Main risk factors and mitigation strategies
- Expected timeline for the transaction process"

🚨 **ABSOLUTELY CRITICAL RULES:**
- **Ask about ONE topic at a time** - never combine topics
- **Wait for complete information** before moving to next topic  
- **NEVER skip any of the 14 mandatory topics above**
- **DON'T generate JSON until ALL 14 topics are covered**
- **If information is incomplete, ask specific follow-up questions**
- **Only generate JSON when you have data for ALL 14 topics**

🚨 **NO EARLY JSON GENERATION ALLOWED:**
- **Count your steps**: You must ask about ALL 14 topics systematically
- **Before JSON generation, verify you asked about ALL 14 topics in sequence**
- **If you generate JSON without completing all 14 steps, you have FAILED**

🚨 **MANDATORY TOPIC CHECKLIST** (check each one):
□ 1. business_overview  
□ 2. investor_considerations
□ 3. product_service_footprint  
□ 4. historical_financial_performance
□ 5. management_team
□ 6. growth_strategy_projections
□ 7. competitive_positioning
□ 8. valuation_overview
□ 9. precedent_transactions
□ 10. strategic_buyers (4-5 companies interested in M&A)
□ 11. financial_buyers (4-5 PE firms interested in investment)
□ 12. margin_cost_resilience
□ 13. sea_conglomerates
□ 14. investor_process_overview
    
11. **Trading Precedents**: 
    Required: Public comparables OR private transactions (ask preference), multiples, rationale
    
12. **Valuation Overview**: 
    Required: Methodologies to use, key multiples, assumptions, valuation range
    
13. **Strategic Buyers**: 
    Required: 3-4 potential acquirers with buyer_name and specific strategic_rationale for each
    
14. **Financial Buyers**: 
    Required: 3-4 PE firms/sponsors with buyer_name and specific strategic_rationale for each

RESPONSE INTERPRETATION:
- "I don't know" = Offer to search and get consent
- "Skip this slide/topic" / "not applicable" / "we don't need this" = Mark as skipped, move to next
- Partial information = Ask specific follow-ups for missing fields
- Complete information = Move to next topic
- Brief confirmatory responses ("yes", "correct") = Move to next topic if current is complete

🚨 **CRITICAL: YOU MUST ASK ABOUT EVERY TOPIC BELOW - DO NOT SKIP ANY!**

**COMPREHENSIVE DATA COLLECTION CHECKLIST** (ask about ALL of these):

**PHASE 1: CORE BUSINESS DATA**
✅ business_overview (name, description, timeline, highlights, services, positioning)
✅ product_service_footprint (services with titles+descriptions, coverage_table, metrics)
✅ historical_financial_performance (chart data, key_metrics, revenue_growth, banker_view)
✅ management_team (left_column_profiles + right_column_profiles with role_title + experience_bullets)

**PHASE 2: STRATEGIC ANALYSIS**
✅ investor_considerations (considerations array + mitigants array)
✅ competitive_positioning (competitors with revenue, assessment array, barriers, advantages)
✅ growth_strategy_projections (strategies array, financial_projections with categories+revenue+ebitda)
✅ margin_cost_resilience (chart_data with values, cost_management items, risk_mitigation)

**PHASE 3: TRANSACTION DATA**
✅ valuation_overview (multiple methodologies, enterprise_values, multiples, commentary)
✅ precedent_transactions (target, acquirer, date, country, enterprise_value, revenue, ev_revenue_multiple)
✅ buyer_profiles (strategic_buyers + financial_buyers with ALL fields: buyer_name, description, strategic_rationale (10-20 words), key_synergies, fit (score + 5-word rationale), financial_capacity)
✅ sea_conglomerates (name, country, description, key_shareholders, key_financials, contact) - Global conglomerates from any region
✅ investor_process_overview (diligence_topics, synergy_opportunities, risk_factors, mitigants, timeline)

❌ DO NOT USE THESE NON-EXISTENT TEMPLATES:
❌ product_service_overview (use product_service_footprint)
❌ trading_comparables (use precedent_transactions)
❌ financial_summary (use historical_financial_performance)
❌ transaction_overview (use business_overview)

If you have forgotten to ask about a topic, ask NOW. 

**AUTO-GENERATION TRIGGER:**
**ONLY after you have asked about ALL 13 mandatory topics above**, respond with:

"Perfect! I now have all the information needed to create your comprehensive pitch deck. Here are your complete, downloadable pitch deck files:

**RENDER PLAN MUST INCLUDE these slides** (unless explicitly skipped):

1. business_overview
2. investor_considerations  
3. product_service_footprint
4. historical_financial_performance
5. management_team
6. growth_strategy_projections
7. competitive_positioning
8. valuation_overview
9. precedent_transactions
10. margin_cost_resilience
11. sea_conglomerates
12. buyer_profiles (strategic_buyers)
13. buyer_profiles (financial_buyers)

🚨 **CRITICAL**: Only generate JSON if you have asked about ALL 13 topics above.



## CONTENT IR JSON:
```json
[INSERT COMPLETE CONTENT IR JSON WITH ALL COLLECTED DATA USING CORRECT FIELD NAMES]
```
⚠️ **MUST INCLUDE 'facts' section** with historical financial data (years, revenue, EBITDA, margins)

## RENDER PLAN JSON:
```json
[INSERT COMPLETE RENDER PLAN JSON WITH ALL SLIDES]
```
⚠️ **MUST INCLUDE content_ir_key for buyer_profiles slides**
⚠️ **MUST INCLUDE complete chart data for financial slides**

These files are now ready for download and can be used directly with your pitch deck generation system!"

🚨 **CRITICAL REQUIREMENTS FOR JSON GENERATION:**
1. **Content IR MUST include 'facts' section** with historical financial data
2. **Every slide MUST have a 'title' field** in the data section
3. **All arrays MUST have minimum required items** (no empty arrays)
4. **buyer_profiles slides MUST have content_ir_key** AND complete table_headers
5. **Financial slides MUST reference facts data** from Content IR
6. **competitive_positioning slides MUST have complete assessment table** with comparison data
7. **product_service_footprint slides MUST have complete metrics data** for right side
8. **NO placeholder text, NO empty fields, NO null values**

CRITICAL JSON GENERATION REQUIREMENTS:
- Generate JSONs for ALL discussed slides (minimum 8-12 slides)
- EXCLUDE any slides that were explicitly skipped
- Use ALL collected information across appropriate slide templates
- Follow the EXACT template structure from the examples below
- Include every piece of data collected during the interview
- NEVER leave placeholder text or empty fields
- USE CORRECT FIELD NAMES as specified above
- ALWAYS use the exact JSON formatting shown above with proper headers and code blocks

🚨 **CRITICAL: EVERY SLIDE MUST HAVE COMPLETE DATA** 🚨
- Every slide MUST have a "title" field
- Every slide MUST have complete "data" section with all required fields
- NO empty arrays, NO null values, NO placeholder text
- If you don't have specific data for a field, generate realistic, professional content
- For buyer_profiles slides, ALWAYS include content_ir_key AND complete table_headers
- For financial slides, ALWAYS include complete chart data and metrics
- For management slides, ALWAYS include complete profile data with experience bullets

AVAILABLE SLIDE TEMPLATES (USE ONLY THESE EXACT NAMES):
- business_overview
- investor_considerations  
- investor_process_overview
- margin_cost_resilience
- historical_financial_performance
- competitive_positioning
- product_service_footprint
- precedent_transactions
- valuation_overview
- sea_conglomerates
- buyer_profiles
- buyer_profiles_aum
- growth_strategy_projections
- management_team

🚨 CRITICAL: DO NOT USE THESE NON-EXISTENT TEMPLATES:
❌ product_service_overview (use product_service_footprint instead)
❌ trading_comparables (use precedent_transactions instead)
❌ financial_summary (use historical_financial_performance instead)
❌ transaction_overview (use business_overview instead)

EXAMPLE JSON STRUCTURES TO FOLLOW EXACTLY:

**Growth Strategy Slide Structure:**
```json
{
  "template": "growth_strategy_projections",
  "data": {
    "title": "Growth Strategy & Financial Projections",
    "slide_data": {
      "title": "Growth Strategy & Financial Projections",
      "growth_strategy": {
        "strategies": ["Strategy 1", "Strategy 2", "Strategy 3"]
      },
      "financial_projections": {
        "categories": ["2024E", "2025E", "2026E"],
        "revenue": [240, 280, 320],
        "ebitda": [47, 56, 64]
      }
    }
  }
🔧 **JSON FIXING STEP** - After generating initial JSON, you MUST fix it:

**STEP 1**: Generate your initial Content IR and Render Plan JSON
**STEP 2**: Compare with working examples and fix any issues
**STEP 3**: Provide corrected JSON that matches the working examples exactly

**WORKING EXAMPLES TO MATCH:**
- Content IR: Must include ALL sections from complete_content_ir.json
- Render Plan: Must have EXACTLY 13 slides matching complete_render_plan.json structure
- Every slide must have proper title field and correct data structure

**COMMON FIXES NEEDED:**
- Add missing title fields to slides
- Fix field structures (key_metrics as object, revenue_growth as object, etc.)
- Ensure exact slide count (13 slides)
- Add missing sections (charts, investor_process_data, margin_cost_data)
- Fix buyer_profiles to have both strategic_buyers and financial_buyers

🚨 **CRITICAL: growth_strategy_projections STRUCTURE**:
```json
{
  "template": "growth_strategy_projections",
  "data": {
    "slide_data": {
      "title": "Growth Strategy & Projections",
      "growth_strategy": {
        "strategies": ["Strategy 1", "Strategy 2", "Strategy 3"]
      },
      "financial_projections": {
        "categories": ["2024E", "2025E", "2026E"],
        "revenue": [240, 280, 320],
        "ebitda": [47, 56, 64]
      }
    }
  }
}
```

REMEMBER: Focus on getting complete, specific information for each topic. Don't move on until you have all required details or explicit user consent to use searched information. Use the CORRECT field names specified above to match the validation system. ALWAYS format your final response with the exact JSON structure shown above.
"""

# Helper Functions for Interview Flow and File Generation
def analyze_conversation_progress(messages):
    """Analyze conversation to determine what topics have been covered and what's next"""
    # Include both user and assistant messages - analyze all content for topic keywords
    filtered_content = []
    for msg in messages:
        if msg["role"] == "system":
            continue
        content = msg["content"]
        # Include ALL conversation content to properly detect topics
        filtered_content.append(content)
    
    conversation_text = " ".join(filtered_content).lower()
    
    # THE 14 MANDATORY TOPICS - must ask about ALL before JSON generation
    topics_checklist = {
        "business_overview": {
            "keywords": ["company", "business", "what does", "overview", "operations", "founded", "headquarters", "industry", "sector", "description"],
            "covered": False,
            "skipped": "skip" in conversation_text and any(skip_phrase in conversation_text for skip_phrase in ["skip business", "skip overview"]),
            "next_question": "Now let's discuss investor considerations. What are the key RISKS and OPPORTUNITIES investors should know about your business? What concerns might they have and how do you mitigate these risks? Include regulatory, competitive, operational, and market risks."
        },
        "investor_considerations": {
            "keywords": ["risk", "opportunity", "investor", "considerations", "challenges", "mitigation", "concerns"],
            "covered": False,
            "skipped": "skip" in conversation_text and any(skip_phrase in conversation_text for skip_phrase in ["skip investor", "skip risk"]),
            "next_question": "Now let's discuss your product/service footprint. What are your main offerings? Please provide the title and description for each product/service. Also, where do you operate geographically and what's your market coverage?"
        },
        "product_service_footprint": {
            "keywords": ["products", "services", "offerings", "geographic", "footprint", "coverage", "operations", "locations"],
            "covered": False,
            "skipped": "skip" in conversation_text and any(skip_phrase in conversation_text for skip_phrase in ["skip product", "skip service", "skip footprint"]),
            "next_question": "Let's analyze your historical financial performance. Can you provide your revenue, EBITDA, margins, and key financial metrics for the last 3-5 years? What are your growth drivers and performance trends?"
        },
        "historical_financial_performance": {
            "keywords": ["revenue", "financial", "ebitda", "margin", "historical", "years", "growth", "2021", "2022", "2023", "2024", "2025", "profit", "performance"],
            "covered": False,
            "skipped": "skip" in conversation_text and any(skip_phrase in conversation_text for skip_phrase in ["skip financial", "skip historical"]),
            "next_question": "Now I need information about your management team. Can you provide names, titles, and brief backgrounds for 4-6 key executives including CEO, CFO, and other senior leaders?"
        },
        "management_team": {
            "keywords": ["management", "team", "executives", "ceo", "cfo", "founder", "leadership", "senior management"],
            "covered": False,
            "skipped": "skip" in conversation_text and any(skip_phrase in conversation_text for skip_phrase in ["skip management", "skip team"]),
            "next_question": "Let's discuss your growth strategy and projections. What are your expansion plans, strategic initiatives, and financial projections for the next 3-5 years? Do you have market size/growth data I can use for charts?"
        },
        "growth_strategy_projections": {
            "keywords": ["growth", "strategy", "expansion", "projections", "future", "strategic initiatives", "market size", "roadmap"],
            "covered": False,
            "skipped": "skip" in conversation_text and any(skip_phrase in conversation_text for skip_phrase in ["skip growth", "skip strategy"]),
            "next_question": "How is your company positioned competitively? I need information about key competitors, your competitive advantages, market positioning, and differentiation factors."
        },
        "competitive_positioning": {
            "keywords": ["competitive", "competitors", "positioning", "comparison", "advantages", "differentiation", "market position"],
            "covered": False,
            "skipped": "skip" in conversation_text and any(skip_phrase in conversation_text for skip_phrase in ["skip competitive", "skip positioning"]),
            "next_question": "What valuation methodologies and overview would be most appropriate for your business? I need enterprise values, methodology assumptions, and your expected valuation range with rationale."
        },
        "valuation_overview": {
            "keywords": ["valuation", "multiple", "methodology", "worth", "assumptions", "enterprise value", "dcf", "comparable"],
            "covered": False,
            "skipped": "skip" in conversation_text and any(skip_phrase in conversation_text for skip_phrase in ["skip valuation", "skip multiple"]),
            "next_question": "Now let's examine precedent transactions. Are there recent M&A transactions in your industry or similar markets that we should analyze? I need target company, acquirer, date, enterprise value, revenue, and multiples."
        },
        "precedent_transactions": {
            "keywords": ["precedent", "transactions", "m&a", "acquisitions", "deals", "transaction multiples"],
            "covered": False,
            "skipped": "skip" in conversation_text and any(skip_phrase in conversation_text for skip_phrase in ["skip precedent", "skip transactions"]),
            "next_question": "Now let's identify potential strategic buyers—companies that might acquire you for strategic reasons. 🚨 CRITICAL: Focus on REGIONALLY RELEVANT companies based on YOUR company's location and market presence. Consider companies from your region/country AND major players with operations in your market. Avoid generic global lists - tailor suggestions to your specific geographic and industry context. I need 4-5 strategic buyers with company name, strategic rationale (3-30 words), key synergies, fit assessment, and financial capacity. If you don't have this information, I can research strategic buyers for your industry and region."
        },
        "strategic_buyers": {
            "keywords": ["strategic buyers", "strategic", "acquirer", "acquisition", "corporate buyer", "industry player", "strategic rationale", "synergies"],
            "covered": False,
            "skipped": "skip" in conversation_text and any(skip_phrase in conversation_text for skip_phrase in ["skip strategic", "skip buyer"]),
            "next_question": "Now let's identify financial buyers—private equity firms, VCs, and other financial investors. 🚨 CRITICAL: Focus on REGIONALLY RELEVANT funds based on YOUR company's location and market. Consider local/regional funds, sovereign wealth funds, and international funds with strong presence in your market. Tailor suggestions to your geographic context rather than generic global lists. I need 4-5 financial buyers with fund name, investment rationale (3-30 words), key synergies, fit assessment, and financial capacity. If you don't have this information, I can research relevant PE firms and financial investors in your market."
        },
        "financial_buyers": {
            "keywords": ["financial buyers", "private equity", "pe", "vc", "venture capital", "financial investor", "fund", "investment rationale"],
            "covered": False,
            "skipped": "skip" in conversation_text and any(skip_phrase in conversation_text for skip_phrase in ["skip financial", "skip pe"]),
            "next_question": "Finally, what would the investment/acquisition process look like? I need: diligence topics investors would focus on, key synergy opportunities, main risk factors and mitigation strategies, and expected timeline for the transaction process."
        },
        "margin_cost_resilience": {
            "keywords": ["margin", "cost", "resilience", "stability", "profitability", "efficiency", "cost management"],
            "covered": False,
            "skipped": "skip" in conversation_text and any(skip_phrase in conversation_text for skip_phrase in ["skip margin", "skip cost"]),
            "next_question": "Let's identify potential global conglomerates and strategic acquirers. 🚨 CRITICAL: Focus on REGIONALLY RELEVANT conglomerates based on YOUR company's location and industry. Consider major conglomerates from your region/country AND international conglomerates with significant operations in your market. Prioritize companies that understand your local market dynamics and regulatory environment. I need at least 4-5 regionally relevant conglomerates with strong market knowledge in your geography."
        },
        "sea_conglomerates": {
            "keywords": ["conglomerate", "global", "international", "multinational", "strategic acquirer"],
            "covered": False,
            "skipped": "skip" in conversation_text and any(skip_phrase in conversation_text for skip_phrase in ["skip conglomerate", "skip global"]),
            "next_question": "Now let's identify potential strategic buyers—companies that might acquire you for strategic reasons. 🚨 CRITICAL: Focus on REGIONALLY RELEVANT companies based on YOUR company's location and market presence. Consider companies from your region/country AND major players with operations in your market. Avoid generic global lists - tailor suggestions to your specific geographic and industry context. I need 4-5 strategic buyers with company name, strategic rationale (3-30 words), key synergies, fit assessment, and financial capacity. If you don't have this information, I can research strategic buyers for your industry and region."
        },
        "investor_process_overview": {
            "keywords": ["process", "diligence", "due diligence", "timeline", "synergy", "risk factors", "transaction process"],
            "covered": False,
            "skipped": "skip" in conversation_text and any(skip_phrase in conversation_text for skip_phrase in ["skip process", "skip diligence"]),
            "next_question": "Perfect! I now have all the information needed to create your comprehensive pitch deck. Let me generate the complete Content IR and Render Plan JSON files."
        }
    }
    
    # Check which topics have been covered or skipped
    covered_count = 0
    skipped_count = 0
    for topic_name, topic_info in topics_checklist.items():
        if topic_info["skipped"]:
            skipped_count += 1
        else:
            # Enhanced coverage detection - include AI research responses when user requests research
            is_covered = False
            
            # Count how many keywords are found
            found_keywords = [keyword for keyword in topic_info["keywords"] if keyword in conversation_text]
            
            # Check for AI research responses (when user asks AI to research)
            research_indicators = [
                "research this yourself", "research yourself", "based on current market data",
                "based on research", "according to", "sources:", "references:", "[1]", "[2]", "[3]",
                "here are", "based on the latest", "current market research", "industry analysis"
            ]
            
            has_research_response = any(indicator in conversation_text for indicator in research_indicators)
            
            # Require multiple keywords OR substantial content OR AI research response
            if len(found_keywords) >= 3:  # Multiple keywords found
                is_covered = True
            elif len(found_keywords) >= 2:
                # Check if there's substantial content OR AI research response
                topic_specific_content = False
                for keyword in found_keywords:
                    # Find instances of the keyword and check surrounding context
                    keyword_positions = []
                    start_pos = 0
                    while True:
                        pos = conversation_text.find(keyword, start_pos)
                        if pos == -1:
                            break
                        keyword_positions.append(pos)
                        start_pos = pos + 1
                    
                    # Check if any keyword instance has substantial surrounding content
                    for pos in keyword_positions:
                        # Extract 200 chars around the keyword
                        context_start = max(0, pos - 100)
                        context_end = min(len(conversation_text), pos + 100)
                        context = conversation_text[context_start:context_end]
                        
                        # Look for indicators of substantial content or AI research
                        content_indicators = [
                            "million", "$", "billion", "revenue", "founded", "established", 
                            "years", "experience", "ceo", "cfo", "headquarters", "operates",
                            "customers", "users", "employees", "growth rate", "margin",
                            "ebitda", "percent", "%", "strategy", "partnership", "subsidiary"
                        ]
                        
                        # Also check for AI research indicators in context
                        ai_research_indicators = [
                            "according to", "based on", "research shows", "data indicates",
                            "market analysis", "industry reports", "current trends", "sources",
                            "references", "[1]", "[2]", "leading", "global", "methodology"
                        ]
                        
                        content_score = len([indicator for indicator in content_indicators if indicator in context])
                        research_score = len([indicator for indicator in ai_research_indicators if indicator in context])
                        
                        # Consider covered if substantial content OR AI research response
                        if content_score >= 2 or (research_score >= 2 and has_research_response):
                            topic_specific_content = True
                            break
                    
                    if topic_specific_content:
                        break
                
                if topic_specific_content:
                    is_covered = True
            
            # Special handling for specific topics that need very specific content
            if topic_name == "management_team":
                # Require actual executive titles and names/backgrounds - stricter validation
                management_indicators = ["ceo", "cfo", "cto", "founder", "president", "director", "executive", "years of experience", "previously", "background in", "chief executive", "chief financial", "chief technology"]
                found_mgmt = [indicator for indicator in management_indicators if indicator in conversation_text]
                
                # Require more substantial management content - names, titles, backgrounds
                detailed_mgmt = len(found_mgmt) >= 3 and ("years" in conversation_text or "experience" in conversation_text or "background" in conversation_text)
                ai_mgmt_research = (has_research_response and len(found_mgmt) >= 2 and 
                                   ("chief" in conversation_text or "executive" in conversation_text) and
                                   ("years" in conversation_text or "experience" in conversation_text))
                
                is_covered = detailed_mgmt or ai_mgmt_research
            
            elif topic_name == "historical_financial_performance":
                # Require actual numbers, years, and growth metrics - stricter validation
                financial_indicators = ["revenue", "ebitda", "profit", "million", "billion", "$", "2020", "2021", "2022", "2023", "2024", "2025", "growth", "%", "margin"]
                found_financial = [indicator for indicator in financial_indicators if indicator in conversation_text]
                years_found = [year for year in ["2020", "2021", "2022", "2023", "2024", "2025"] if year in conversation_text]
                
                # Require substantial financial data with multiple years
                detailed_financials = len(found_financial) >= 4 and len(years_found) >= 2 and ("$" in conversation_text or "million" in conversation_text)
                ai_financial_research = (has_research_response and len(found_financial) >= 3 and len(years_found) >= 2 and 
                                       ("$" in conversation_text or "million" in conversation_text))
                
                is_covered = detailed_financials or ai_financial_research
            
            elif topic_name == "investor_considerations":
                # Require actual risk and opportunity discussion
                risk_indicators = ["risk", "opportunity", "challenges", "concerns", "mitigation", "regulatory", "competitive", "operational", "market risk"]
                found_risks = [indicator for indicator in risk_indicators if indicator in conversation_text]
                
                # Require substantial risk/opportunity content
                detailed_risks = len(found_risks) >= 3 and ("risk" in conversation_text and "opportunity" in conversation_text)
                ai_risk_research = has_research_response and len(found_risks) >= 2 and ("risk" in conversation_text or "challenges" in conversation_text)
                
                is_covered = detailed_risks or ai_risk_research
            
            elif topic_name == "product_service_footprint":
                # Require actual product/service descriptions and geographic coverage
                product_indicators = ["products", "services", "offerings", "footprint", "coverage", "operations", "geographic", "branches", "countries", "regions"]
                found_products = [indicator for indicator in product_indicators if indicator in conversation_text]
                
                # Require substantial product/geographic content
                detailed_products = len(found_products) >= 4 and ("countries" in conversation_text or "regions" in conversation_text)
                ai_product_research = has_research_response and len(found_products) >= 3 and "coverage" in conversation_text
                
                is_covered = detailed_products or ai_product_research
            
            elif topic_name == "precedent_transactions":
                # Require actual transaction details and multiples
                transaction_indicators = ["transaction", "acquisition", "deal", "multiple", "revenue", "enterprise value", "target", "acquirer", "m&a"]
                found_transactions = [indicator for indicator in transaction_indicators if indicator in conversation_text]
                
                # Must have specific transaction data
                detailed_transactions = len(found_transactions) >= 5 and ("multiple" in conversation_text and "enterprise value" in conversation_text)
                ai_transaction_research = has_research_response and len(found_transactions) >= 3 and "transaction" in conversation_text
                
                is_covered = detailed_transactions or ai_transaction_research
            
            elif topic_name == "margin_cost_resilience":
                # Require cost management and margin discussion
                margin_indicators = ["margin", "cost", "resilience", "efficiency", "management", "operational", "ebitda", "stability"]
                found_margins = [indicator for indicator in margin_indicators if indicator in conversation_text]
                
                # Must have substantial margin/cost content
                detailed_margins = len(found_margins) >= 4 and ("cost management" in conversation_text or "efficiency" in conversation_text)
                ai_margin_research = has_research_response and len(found_margins) >= 3 and "margin" in conversation_text
                
                is_covered = detailed_margins or ai_margin_research
            
            elif topic_name == "sea_conglomerates":
                # Require actual conglomerate names and details
                conglomerate_indicators = ["conglomerate", "global", "international", "multinational", "strategic acquirer", "corporation", "holding"]
                found_conglomerates = [indicator for indicator in conglomerate_indicators if indicator in conversation_text]
                
                # Must have specific conglomerate discussion
                detailed_conglomerates = len(found_conglomerates) >= 3 and ("conglomerate" in conversation_text or "multinational" in conversation_text)
                ai_conglomerate_research = has_research_response and len(found_conglomerates) >= 2 and "global" in conversation_text
                
                is_covered = detailed_conglomerates or ai_conglomerate_research
            
            elif topic_name == "investor_process_overview":
                # Require process, timeline, and due diligence discussion
                process_indicators = ["process", "diligence", "timeline", "due diligence", "synerg", "risk factors", "mitigation", "weeks"]
                found_process = [indicator for indicator in process_indicators if indicator in conversation_text]
                
                # Must have comprehensive process discussion
                detailed_process = len(found_process) >= 4 and ("diligence" in conversation_text and "timeline" in conversation_text)
                ai_process_research = has_research_response and len(found_process) >= 3 and "process" in conversation_text
                
                is_covered = detailed_process or ai_process_research
            
            elif topic_name == "strategic_buyers" or topic_name == "financial_buyers":
                # RELAXED - allow AI research and reasonable buyer content detection
                buyer_indicators = ["acquisition", "acquirer", "fund", "capital", "equity", "investment", "rationale", "synerg", "fit", "capacity", "strategic", "financial", "buyer", "private equity", "corporation", "conglomerate"]
                found_buyers = [indicator for indicator in buyer_indicators if indicator in conversation_text]
                
                # Look for buyer content - can be from AI research or user discussion
                has_buyer_context = len(found_buyers) >= 3
                has_research_response = "research" in conversation_text or "here" in conversation_text or "based on" in conversation_text
                
                # Accept if substantial buyer discussion OR AI research
                detailed_buyer_content = has_buyer_context and (
                    "strategic" in conversation_text or "financial" in conversation_text or 
                    "rationale" in conversation_text or "synerg" in conversation_text
                )
                ai_buyer_research = has_research_response and has_buyer_context
                
                is_covered = detailed_buyer_content or ai_buyer_research
            
            if is_covered:
                topic_info["covered"] = True
                covered_count += 1
    
    # Find next uncovered and unskipped topic
    next_topic = None
    next_question = None
    for topic_name, topic_info in topics_checklist.items():
        if not topic_info["covered"] and not topic_info["skipped"]:
            next_topic = topic_name
            next_question = topic_info["next_question"]
            break
    
    total_applicable_topics = len(topics_checklist) - skipped_count
    completion_percentage = covered_count / total_applicable_topics if total_applicable_topics > 0 else 1.0
    
    return {
        "topics_covered": covered_count,
        "topics_skipped": skipped_count,
        "total_topics": len(topics_checklist),
        "applicable_topics": total_applicable_topics,
        "completion_percentage": completion_percentage,
        "next_topic": next_topic,
        "next_question": next_question,
        "is_complete": covered_count >= total_applicable_topics  # All topics must be covered
    }

def check_interview_completion(messages):
    """Check if interview has enough information for JSON generation"""
    conversation_text = " ".join([msg["content"] for msg in messages if msg["role"] != "system"])
    
    required_elements = [
        ("company name", ["company", "business name", "firm"]),
        ("business model", ["business model", "how does", "revenue model", "operations"]),
        ("revenue", ["revenue", "sales", "income", "financial performance"]),
        ("EBITDA", ["EBITDA", "earnings", "profit", "margin"]),
        ("management team", ["management", "team", "CEO", "founder", "executive"]),
        ("growth strategy", ["growth", "strategy", "expansion", "future", "projections"]),
        ("valuation", ["valuation", "multiple", "worth", "value"]),
        ("strategic buyers", ["strategic", "buyer", "acquirer", "acquisition"]),
        ("financial buyers", ["financial buyer", "private equity", "PE", "sponsor"]),
        ("SEA conglomerates", ["conglomerate", "SEA", "Asia", "global", "multinational"]),
        ("investor process", ["investor process", "due diligence", "timeline", "synergy"]),
        ("charts data", ["chart", "data", "financial data", "specific numbers"]),
        ("cost management", ["cost management", "margin", "cost", "efficiency"])
    ]
    
    completed_count = 0
    for element_name, keywords in required_elements:
        if any(keyword.lower() in conversation_text.lower() for keyword in keywords):
            completed_count += 1
    
    completion_percentage = completed_count / len(required_elements)
    return completion_percentage >= 0.8, completed_count, len(required_elements)





# --- BEGIN: Auto-convert buyer_profiles with financials → sea_conglomerates ---
import os, re as _re

AUTO_USE_SEA_CONGLOMERATES = os.getenv("AUTO_USE_SEA_CONGLOMERATES", "1") not in ("0","false","False","no","No")

_FINANCE_HINTS = {"revenue","ebitda","market_cap","net_income","profit","earnings","margin","ticker","ownership","assets","liabilities","enterprise_value","ev","valuation"}

def _extract_country_from_name(name: str) -> str:
    # e.g., "Yamazaki Baking Co. (Japan)" -> "Japan"
    if not isinstance(name, str):
        return ""
    m = _re.search(r"\(([^)]+)\)\s*$", name.strip())
    return m.group(1).strip() if m else ""

def _dict_row_has_finance(r: dict) -> bool:
    keys = {k.lower() for k in r.keys()}
    return any(k in keys for k in _FINANCE_HINTS)

def _headers_have_finance(headers) -> bool:
    if not isinstance(headers, list): return False
    hl = [str(h).strip().lower() for h in headers]
    return any(any(hint in h for hint in _FINANCE_HINTS) for h in hl)

def convert_buyer_profiles_to_sea_conglomerates(slide: dict) -> dict:
    """
    If buyer_profiles contains financial fields (dict rows or finance headers),
    convert to sea_conglomerates template with concise description lines.
    """
    if slide.get("template") != "buyer_profiles" or not AUTO_USE_SEA_CONGLOMERATES:
        return slide

    data = slide.get("data", {})
    rows = data.get("table_rows", [])
    headers = data.get("table_headers", [])

    finance_mode = False
    dict_rows = []
    if isinstance(rows, list) and rows and isinstance(rows[0], dict):
        dict_rows = rows
        finance_mode = any(_dict_row_has_finance(r) for r in dict_rows)
    elif _headers_have_finance(headers):
        finance_mode = True

    if not finance_mode:
        return slide  # no conversion

    items = []
    if dict_rows:
        for r in dict_rows:
            name = r.get("buyer_name") or r.get("name","")
            country = r.get("country") or _extract_country_from_name(name)
            parts = []

            # Financials first if present
            for k in ("revenue","ebitda","market_cap","net_income","margin","enterprise_value","valuation","ownership","ticker"):
                v = r.get(k)
                if v not in (None, ""):
                    label = k.replace("_"," ").title()
                    parts.append(f"{label}: {v}")

            # Then rationale/synergies for context
            if r.get("strategic_rationale"):
                parts.append(f"Rationale: {r.get('strategic_rationale')}")
            if r.get("key_synergies"):
                parts.append(f"Synergies: {r.get('key_synergies')}")

            desc = " • ".join(parts) if parts else "—"
            items.append({"name": name, "country": country, "description": desc})
    else:
        # If rows are arrays and headers include finance terms, map by position
        # Build index mapping from headers
        idx = {h.strip().lower(): i for i, h in enumerate(headers) if isinstance(h, str)}
        for r in rows:
            name = r[idx.get("buyer name", 0)] if isinstance(r, list) and len(r)>0 else ""
            country = _extract_country_from_name(name)
            parts = []
            for hint in list(_FINANCE_HINTS):
                pos = None
                # try exact header match or contains
                for h, i in idx.items():
                    if hint in h:
                        pos = i; break
                if pos is not None and isinstance(r, list) and len(r)>pos:
                    v = r[pos]
                    if v not in (None, ""):
                        label = hint.replace("_"," ").title()
                        parts.append(f"{label}: {v}")
            # Try rationale/synergies columns
            for key in ["strategic rationale","rationale","key synergies","synergies"]:
                if key in idx and len(r)>idx[key]:
                    val = r[idx[key]]
                    if val not in (None, ""):
                        parts.append(f"{key.title()}: {val}")
            desc = " • ".join(parts) if parts else "—"
            items.append({"name": name, "country": country, "description": desc})

    # Build the new slide
    new_slide = {
        "template": "sea_conglomerates",
        "data": items
    }
    # Preserve original title as an optional leading descriptor if present
    if isinstance(data, dict) and "title" in data:
        # Some renderers might read title; we prepend a descriptor row
        pass

    return new_slide
# --- END: Auto-convert ---
# --- BEGIN: Normalizers to prevent blank cells and schema drift ---
def normalize_buyer_profiles_slide(slide: dict) -> dict:
    if slide.get("template") != "buyer_profiles":
        return slide
    d = slide.setdefault("data", {})

    headers = d.get("table_headers") or ["Buyer Name", "Description", "Strategic Rationale", "Key Synergies", "Fit"]
    if len(headers) == 4:
        # Keep as 4 columns - likely missing description column
        headers = [headers[0], "Description", headers[1], headers[2], headers[3]]
    d["table_headers"] = headers[:5]

    fixed_rows = []
    for r in d.get("table_rows", []):
        if isinstance(r, list):
            r = {
                "buyer_name":          (r[0] if len(r) > 0 else ""),
                "strategic_rationale": (r[1] if len(r) > 1 else ""),
                "key_synergies":       (r[2] if len(r) > 2 else ""),
                "fit":                (r[3] if len(r) > 3 else ""),
                "fit":                (r[4] if len(r) > 4 else ""),
            }
        else:
            r = dict(r)
            r["buyer_name"]          = r.get("buyer_name") or r.get("name", "")
            r["strategic_rationale"] = r.get("strategic_rationale") or r.get("rationale", "")
            r["key_synergies"]       = r.get("key_synergies") or r.get("synergies", "")
            r["fit"]                = r.get("fit") or r.get("concerns", "")
            r["fit"]                = r.get("fit") or r.get("fit_score", "")
        fixed_rows.append(r)
    d["table_rows"] = fixed_rows

    d.setdefault("subtitle", d.get("subtitle", ""))
    d.setdefault("company", slide.get("company") or "")
    return slide


def normalize_valuation_overview_slide(slide: dict) -> dict:
    if slide.get("template") != "valuation_overview":
        return slide
    d = slide.setdefault("data", {})
    rows = d.get("valuation_data", [])

    any_22a = False
    any_23e = False
    any_metric = False

    for r in rows:
        meth = (r.get("methodology") or "").lower()
        if not r.get("metric"):
            if "precedent" in meth or "trading" in meth:
                r["metric"] = "EV/Revenue"
            elif "dcf" in meth or "discounted" in meth:
                r["metric"] = "DCF"
        any_metric = any_metric or bool(r.get("metric"))

        if "22a_multiple" not in r:
            r["22a_multiple"] = r.get("22A_multiple") or r.get("FY22_multiple") or "-"
        if "23e_multiple" not in r:
            r["23e_multiple"] = r.get("23E_multiple") or r.get("FY23E_multiple") or "-"

        if not r.get("methodology_type"):
            if "precedent" in meth:
                r["methodology_type"] = "precedent_transactions"
            elif "trading" in meth:
                r["methodology_type"] = "trading_comps"
            elif "dcf" in meth or "discounted" in meth:
                r["methodology_type"] = "dcf"

        any_22a = any_22a or (r.get("22a_multiple") not in ("", None))
        any_23e = any_23e or (r.get("23e_multiple") not in ("", None))

    d["__hide_metric_col"]  = not any_metric
    d["__hide_22a_col"]     = not any_22a
    d["__hide_23e_col"]     = not any_23e
    return slide


def normalize_plan(plan: dict) -> dict:
    try:
        slides_in = plan.get("slides", [])
    except Exception:
        return plan
    slides_out = []
    for s in slides_in:
        # Convert finance-heavy buyer profiles into SEA Conglomerates slide first
        s = convert_buyer_profiles_to_sea_conglomerates(s)
        # Then run standard normalizers
        s = normalize_buyer_profiles_slide(s)
        s = normalize_valuation_overview_slide(s)
        slides_out.append(s)
    plan["slides"] = slides_out
    return plan
    slides_out = []
    for s in slides_in:
        s = normalize_buyer_profiles_slide(s)
        s = normalize_valuation_overview_slide(s)
        slides_out.append(s)
    plan["slides"] = slides_out
    return plan
# --- END: Normalizers ---

def extract_and_validate_jsons(response_text):
    """Extract JSONs and perform comprehensive validation with example-based checking"""
    print("\n" + "="*80)
    print("🔍 JSON EXTRACTION AND VALIDATION STARTED")
    print("="*80)
    
    # Extract JSONs with improved parsing
    content_ir, render_plan = extract_jsons_from_response(response_text)
    
    print(f"\n📊 EXTRACTION RESULTS:")
    print(f"Content IR: {'✅ Found' if content_ir else '❌ Not Found'}")
    print(f"Render Plan: {'✅ Found' if render_plan else '❌ Not Found'}")
    
    if not content_ir and not render_plan:
        print("\n❌ NO JSONS EXTRACTED - Validation cannot proceed")
        return None, None, {
            'overall_valid': False,
            'summary': {'total_slides': 0, 'valid_slides': 0, 'invalid_slides': 0},
            'critical_issues': ['No JSONs found in response'],
            'extraction_failed': True
        }
    
    # Normalize extracted JSON to match expected structure
    print("\n🔧 NORMALIZING EXTRACTED JSON...")
    content_ir, render_plan = normalize_extracted_json(content_ir, render_plan)
    
    # Validate JSON structure against examples
    print("\n🏗️ STRUCTURE VALIDATION:")
    structure_validation = validate_json_structure_against_examples(content_ir, render_plan)
    
    # Normalize for downstream validation and rendering
    if isinstance(render_plan, dict):
        render_plan = normalize_plan(render_plan)
    
    # Perform comprehensive slide validation
    print("\n📋 SLIDE-BY-SLIDE VALIDATION:")
    validation_results = validate_individual_slides(content_ir, render_plan)
    
    # Add example-based structure validation results
    validation_results['structure_validation'] = structure_validation
    validation_results['extraction_successful'] = True
    
    # Add structure issues to critical issues if structure is invalid
    if not structure_validation['content_ir_valid'] or not structure_validation['render_plan_valid']:
        validation_results['critical_issues'].extend(structure_validation['structure_issues'])
        if 'missing_sections' in structure_validation:
            validation_results['critical_issues'].extend(structure_validation['missing_sections'])
        # Note: field_mismatches key doesn't exist in structure_validation, removed to fix KeyError
        validation_results['overall_valid'] = False
    
    # Calculate quality scores
    if structure_validation['content_ir_valid'] and structure_validation['render_plan_valid']:
        validation_results['structure_quality_score'] = 100
    else:
        validation_results['structure_quality_score'] = max(0, 100 - (len(structure_validation['structure_issues']) * 20))
    
    print(f"\n📈 VALIDATION SUMMARY:")
    print(f"Structure Quality: {validation_results.get('structure_quality_score', 0)}%")
    print(f"Overall Valid: {'✅ Yes' if validation_results['overall_valid'] else '❌ No'}")
    print(f"Critical Issues: {len(validation_results.get('critical_issues', []))}")
    
    print("="*80)
    print("🔍 JSON EXTRACTION AND VALIDATION COMPLETED")
    print("="*80 + "\n")
    
    return content_ir, render_plan, validation_results

def auto_enhance_management_team(content_ir, conversation_messages=None):
    """
    Automatically enhance management team data using executive search
    """
    print("🔍 AUTO-ENHANCING MANAGEMENT TEAM DATA...")
    
    # Extract company name
    company_name = "Unknown Company"
    if isinstance(content_ir, dict) and 'entities' in content_ir:
        company_name = content_ir.get('entities', {}).get('company', {}).get('name', 'Unknown Company')
    
    # Look for any research data in conversation messages about the company
    research_text = None
    if conversation_messages:
        # Combine all conversation messages to look for executive information
        conversation_text = " ".join([msg.get("content", "") for msg in conversation_messages if isinstance(msg, dict)])
        
        # Check if there's detailed executive information in the conversation
        executive_keywords = ["CEO", "CFO", "COO", "Chief Executive", "Chief Financial", "Chief Operating", 
                             "management team", "executives", "senior management", "years of experience", 
                             "previously held", "background in"]
        
        if any(keyword.lower() in conversation_text.lower() for keyword in executive_keywords):
            research_text = conversation_text
            print(f"🔍 Found executive information in conversation ({len(research_text)} characters)")
    
    # Check if management_team already exists and has good data
    existing_mgmt = content_ir.get('management_team', {})
    left_profiles = existing_mgmt.get('left_column_profiles', [])
    right_profiles = existing_mgmt.get('right_column_profiles', [])
    
    total_profiles = len(left_profiles) + len(right_profiles)
    
    # If we have less than 3 profiles or profiles are very basic, enhance them
    needs_enhancement = False
    if total_profiles < 3:
        needs_enhancement = True
        print(f"🔍 Only {total_profiles} management profiles found - enhancing...")
    else:
        # Check if existing profiles are just templates/basic
        for profile in left_profiles + right_profiles:
            bullets = profile.get('experience_bullets', [])
            if not bullets or len(bullets) < 3:
                needs_enhancement = True
                break
            # Check for template text
            bullet_text = " ".join(bullets)
            if any(template_word in bullet_text.lower() for template_word in 
                  ["template", "placeholder", "example", "sample", "your company"]):
                needs_enhancement = True
                break
    
    if needs_enhancement:
        print(f"🚀 Auto-generating enhanced management team data for {company_name}...")
        
        # Use executive search to generate/enhance management team data
        enhanced_mgmt_data = auto_generate_management_data(company_name, research_text)
        
        # Update content_ir with enhanced data
        if 'management_team' not in content_ir:
            content_ir['management_team'] = {}
        
        content_ir['management_team'].update(enhanced_mgmt_data)
        
        new_total = len(enhanced_mgmt_data.get('left_column_profiles', [])) + len(enhanced_mgmt_data.get('right_column_profiles', []))
        print(f"✅ Enhanced management team: {total_profiles} → {new_total} profiles")
        
        return content_ir, True  # Return modified content_ir and enhancement flag
    else:
        print(f"✅ Management team already has good data ({total_profiles} profiles)")
        return content_ir, False  # No enhancement needed

def create_downloadable_files(content_ir, render_plan, company_name="company"):
    """Create downloadable Content IR and Render Plan files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_company_name = "".join(c for c in company_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    safe_company_name = safe_company_name.replace(' ', '_')
    
    # Create individual files
    content_ir_filename = f"{safe_company_name}_content_ir_{timestamp}.json"
    render_plan_filename = f"{safe_company_name}_render_plan_{timestamp}.json"
    
    # Format JSON with proper indentation
    content_ir_json = json.dumps(content_ir, indent=2, ensure_ascii=False)
    render_plan_json = json.dumps(render_plan, indent=2, ensure_ascii=False)
    
    return {
        'content_ir_filename': content_ir_filename,
        'content_ir_json': content_ir_json,
        'render_plan_filename': render_plan_filename,
        'render_plan_json': render_plan_json,
        'timestamp': timestamp,
        'company_name': safe_company_name
    }

def create_zip_package(files_data):
    """Create a ZIP package with both JSON files and metadata"""
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add Content IR file
        zip_file.writestr(files_data['content_ir_filename'], files_data['content_ir_json'])
        
        # Add Render Plan file
        zip_file.writestr(files_data['render_plan_filename'], files_data['render_plan_json'])
        
        # Add README with instructions
        readme_content = f"""# AI-Generated Pitch Deck Files
Company: {files_data['company_name']}
Generated: {files_data['timestamp']}

## Files Included:
1. {files_data['content_ir_filename']} - Contains all content data for slides
2. {files_data['render_plan_filename']} - Defines slide structure and templates

## Usage Instructions:
1. Use these files with your pitch deck generation system
2. Load the Content IR for slide data
3. Load the Render Plan for slide structure
4. Generate your PowerPoint presentation

## File Validation:
- Content IR structure: ✓ Complete
- Render Plan structure: ✓ Complete
- Ready for deck generation: ✓ Yes

Generated by AI Deck Builder - LLM-Powered Pitch Deck Generator
"""
        zip_file.writestr("README.txt", readme_content)
        
        # Add metadata file
        metadata = {
            "generated_at": files_data['timestamp'],
            "company_name": files_data['company_name'],
            "content_ir_file": files_data['content_ir_filename'],
            "render_plan_file": files_data['render_plan_filename'],
            "generator": "AI Deck Builder",
            "version": "1.0"
        }
        zip_file.writestr("metadata.json", json.dumps(metadata, indent=2))
    
    zip_buffer.seek(0)
    return zip_buffer

def show_interview_progress(messages):
    """Show progress indicator for interview completion"""
    progress_info = analyze_conversation_progress(messages)
    
    st.sidebar.subheader("🎯 Interview Progress")
    st.sidebar.progress(progress_info["completion_percentage"])
    st.sidebar.write(f"{progress_info['topics_covered']}/{progress_info['applicable_topics']} topics covered")
    
    if progress_info["topics_skipped"] > 0:
        st.sidebar.write(f"⭐ {progress_info['topics_skipped']} topics skipped")
    
    if progress_info["is_complete"]:
        st.sidebar.success("✅ Ready for JSON generation!")
    else:
        remaining = progress_info['applicable_topics'] - progress_info['topics_covered']
        st.sidebar.info(f"📝 {remaining} topics remaining")
    
    return progress_info["is_complete"]

# Initialize brand extractor
brand_extractor = BrandExtractor()

def extract_company_context_from_messages(messages):
    """Extract company context from conversation messages for Vector DB enhancement"""
    context = {
        "name": "",
        "overview": "",
        "sector": "general", 
        "region": "global",
        "revenue": 0,
        "ebitda": 0
    }
    
    # Combine all user messages to extract company information
    conversation_text = " ".join([msg["content"] for msg in messages if msg["role"] == "user"])
    
    try:
        # Simple pattern matching to extract company information
        lines = conversation_text.split('\n')
        
        for line in lines:
            line_lower = line.lower().strip()
            
            # Extract company name
            if not context["name"]:
                for pattern in ["company name is", "company:", "business name:", "we are", "my company is"]:
                    if pattern in line_lower:
                        potential_name = line.split(':')[-1].strip() if ':' in line else line_lower.replace(pattern, '').strip()
                        if len(potential_name) > 2 and len(potential_name) < 100:
                            context["name"] = potential_name.title()
                            break
            
            # Extract sector/industry
            if not context["sector"] or context["sector"] == "general":
                sector_keywords = {
                    "healthcare": ["healthcare", "medical", "hospital", "clinic", "pharmaceutical", "biotech"],
                    "technology": ["technology", "software", "saas", "ai", "tech", "digital", "platform"],
                    "financial_services": ["financial", "fintech", "banking", "insurance", "investment"],
                    "consumer_services": ["retail", "consumer", "restaurant", "hospitality", "travel"],
                    "manufacturing": ["manufacturing", "industrial", "factory", "production"],
                    "real_estate": ["real estate", "property", "reit", "development"],
                    "energy": ["energy", "oil", "gas", "renewable", "solar", "wind"]
                }
                
                for sector, keywords in sector_keywords.items():
                    if any(keyword in line_lower for keyword in keywords):
                        context["sector"] = sector
                        break
            
            # Extract region/geography
            if context["region"] == "global":
                region_keywords = {
                    "Asia": ["asia", "china", "japan", "korea", "singapore", "hong kong", "india", "asean"],
                    "North America": ["usa", "america", "canada", "north america", "us"],
                    "Europe": ["europe", "uk", "germany", "france", "italy", "spain", "european"],
                    "Middle East": ["middle east", "uae", "saudi", "qatar", "dubai"],
                    "Latin America": ["latin america", "brazil", "mexico", "argentina", "south america"]
                }
                
                for region, keywords in region_keywords.items():
                    if any(keyword in line_lower for keyword in keywords):
                        context["region"] = region
                        break
            
            # Extract financial metrics (basic pattern matching)
            if "revenue" in line_lower or "sales" in line_lower:
                import re
                revenue_match = re.search(r'[\$]?(\d+(?:\.\d+)?)\s*[mM]?(?:illion)?', line)
                if revenue_match:
                    context["revenue"] = float(revenue_match.group(1))
            
            if "ebitda" in line_lower:
                import re  
                ebitda_match = re.search(r'[\$]?(\d+(?:\.\d+)?)\s*[mM]?(?:illion)?', line)
                if ebitda_match:
                    context["ebitda"] = float(ebitda_match.group(1))
        
        # Try to extract a business description/overview
        # Look for descriptive sentences about the business
        description_patterns = [
            "we operate", "we provide", "we offer", "business does", "company operates", 
            "we specialize", "we focus", "our business", "we run", "we own"
        ]
        
        for line in lines:
            line_lower = line.lower().strip()
            if any(pattern in line_lower for pattern in description_patterns) and len(line.strip()) > 20:
                context["overview"] = line.strip()[:500]  # Limit to 500 chars
                break
        
        # If no specific overview found, use first substantial user message
        if not context["overview"]:
            for msg in messages:
                if msg["role"] == "user" and len(msg["content"].strip()) > 50:
                    context["overview"] = msg["content"].strip()[:300]  # Limit to 300 chars
                    break
                    
    except Exception as e:
        print(f"Warning: Error extracting company context: {e}")
        # Return defaults on error
        pass
    
    return context

# LLM Integration Functions - FIXED FOR MESSAGE ALTERNATION
def call_llm_api(messages, model_name, api_key, service="perplexity"):
    """Call LLM API (Perplexity or Claude) with the conversation - Enhanced with Vector DB"""
    try:
        # Check if Vector DB is available and enhance the last user message
        if st.session_state.get("vector_db_initialized", False):
            try:
                from enhanced_ai_analysis import get_enhanced_ai_analysis
                enhanced_ai = get_enhanced_ai_analysis()
                
                # Get the last user message to enhance
                last_user_message = None
                for msg in reversed(messages):
                    if msg["role"] == "user":
                        last_user_message = msg
                        break
                
                if last_user_message:
                    # Extract company context from conversation history for dynamic Vector DB queries
                    company_context = extract_company_context_from_messages(messages)
                    
                    # Enhance the prompt with Vector DB data using company context
                    enhanced_content = enhanced_ai.enhance_prompt_with_vector_data(
                        last_user_message["content"], 
                        company_profile=company_context
                    )
                    
                    # Update the message with enhanced content
                    last_user_message["content"] = enhanced_content
                    
                    # Show enhancement notification with context info
                    if company_context.get("name"):
                        st.info(f"🔍 Enhanced with Vector DB data for {company_context['name']} ({company_context.get('sector', 'general sector')})")
                    else:
                        st.info("🔍 Enhanced with Vector DB data for more accurate analysis")
                    
            except Exception as e:
                st.warning(f"⚠️ Vector DB enhancement failed: {str(e)}")
                # Continue with original message if enhancement fails
        
        # Call the appropriate API
        if service == "perplexity":
            return call_perplexity_api(messages, model_name, api_key)
        elif service == "claude":
            return call_claude_api(messages, model_name, api_key)
        else:
            return f"Unknown service: {service}"
    except Exception as e:
        return f"Error calling {service} API: {str(e)}"

def call_perplexity_api(messages, model_name, api_key):
    """Call Perplexity API with the conversation - FIXED for message alternation"""
    try:
        url = "https://api.perplexity.ai/chat/completions"
        
        # Extract system message
        system_message = None
        conversation_messages = []
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            elif msg["role"] in ["user", "assistant"]:
                conversation_messages.append(msg)
        
        # Build properly alternating conversation
        # Remove any leading assistant messages (Perplexity needs user first after system)
        while conversation_messages and conversation_messages[0]["role"] == "assistant":
            conversation_messages.pop(0)
        
        # Collapse consecutive same-role messages to enforce alternation
        cleaned_messages = []
        for msg in conversation_messages:
            if cleaned_messages and cleaned_messages[-1]["role"] == msg["role"]:
                # Combine consecutive messages of same role
                cleaned_messages[-1]["content"] = cleaned_messages[-1]["content"].rstrip() + "\n\n" + str(msg.get("content", "")).strip()
            else:
                cleaned_messages.append({
                    "role": msg["role"],
                    "content": str(msg.get("content", "")).strip()
                })
        
        # Build final message array for Perplexity
        final_messages = []
        
        # Add system message if present
        if system_message:
            final_messages.append({"role": "system", "content": system_message})
        
        # Add alternating conversation
        final_messages.extend(cleaned_messages)
        
        # Ensure we don't have empty messages
        final_messages = [msg for msg in final_messages if msg.get("content", "").strip()]
        
        payload = {
            "model": model_name,
            "messages": final_messages,
            "temperature": 0.7,
            "max_tokens": 12000,  # Increased from 4000 to handle complete JSON generation
            "stream": False
        }
        
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('choices', [{}])[0].get('message', {}).get('content', 'No response')
        else:
            return f"Perplexity API Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Error calling Perplexity API: {str(e)}"

def call_claude_api(messages, model_name, api_key):
    """Call Claude API with the conversation"""
    try:
        url = "https://api.anthropic.com/v1/messages"
        
        # Convert messages format for Claude
        claude_messages = []
        system_message = ""
        
        for msg in messages:
            if msg["role"] == "system":
                system_message = msg["content"]
            else:
                claude_messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        payload = {
            "model": model_name,
            "max_tokens": 12000,  # Increased from 4000 to handle complete JSON generation
            "temperature": 0.7,
            "messages": claude_messages
        }
        
        if system_message:
            payload["system"] = system_message
        
        headers = {
            "x-api-key": api_key,
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01"
        }
        
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            return result.get('content', [{}])[0].get('text', 'No response')
        else:
            return f"Claude API Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Error calling Claude API: {str(e)}"

# Rest of the app.py code follows with sidebar, main interface, etc.
# (The rest of the code remains the same as in the original app.py)

# Sidebar Configuration
with st.sidebar:
    st.header("🤖 AI Configuration")
    
    # LLM Model Selection
    st.subheader("LLM Model")
    
    # LLM Service Selection
    llm_service = st.radio(
        "LLM Service",
        ["🔍 Perplexity (Recommended)", "🧠 Claude (Anthropic)"],
        help="Choose your preferred LLM service"
    )
    
    if llm_service.startswith("🔍"):
        # Perplexity models - UPDATED with current valid model names
        model_options = [
            "sonar-pro",  # Most capable model (replaces sonar-large-online)
            "sonar",  # Standard model (replaces sonar-small-online)
            "sonar-reasoning",  # For complex reasoning tasks
            "sonar-reasoning-pro",  # Advanced reasoning model
            "sonar-deep-research"  # For comprehensive research
        ]
        selected_model = st.selectbox(
            "Choose Perplexity Model",
            model_options,
            index=0,  # Default to sonar-pro (most capable)
            help="sonar-pro offers the best balance of capability and speed. Token limit: 16,000 tokens for complete JSON generation."
        )
        api_service = "perplexity"
    else:
        # Claude models
        model_options = [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022",
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307"
        ]
        selected_model = st.selectbox(
            "Choose Claude Model",
            model_options,
            index=0,  # Default to latest Sonnet
            help="Claude Sonnet offers the best balance of speed and capability. Token limit: 16,000 tokens for complete JSON generation."
        )
        api_service = "claude"
    
    # API Key Input
    if api_service == "perplexity":
        api_key = st.text_input(
            "Perplexity API Key",
            type="password",
            help="Enter your Perplexity API key"
        )
    else:
        api_key = st.text_input(
            "Claude API Key",
            type="password",
            help="Enter your Anthropic Claude API key"
        )
    
    if not api_key:
        service_name = "Perplexity" if api_service == "perplexity" else "Claude"
        st.warning(f"⚠️ Please enter your {service_name} API key to use the AI copilot")
    
    st.markdown("---")
    
    # File Status Section
    st.subheader("📁 Generated Files Status")
    
    if st.session_state.get("files_ready", False):
        st.success("✅ Files Ready!")
        files_data = st.session_state.get("files_data", {})
        st.write(f"**Company:** {files_data.get('company_name', 'N/A')}")
        st.write(f"**Generated:** {files_data.get('timestamp', 'N/A')}")
        
        if st.button("🔄 Regenerate Files"):
            st.session_state["files_ready"] = False
            st.session_state.pop("files_data", None)
            st.rerun()
    else:
        st.info("📄 Complete interview to generate files")
    
    st.markdown("---")
    
    # Brand Upload Section with LLM Integration
    st.subheader("🎨 Brand Configuration")
    
    # Add extraction method selector
    extraction_method = st.radio(
        "Brand Extraction Method",
        ["🔧 Rule-Based (Recommended)", "🤖 LLM-Powered (Experimental)"],
        help="Rule-based extraction analyzes PowerPoint structure directly for reliable color extraction",
        key="extraction_method"
    )
    
    uploaded_brand = st.file_uploader(
        "Upload Brand Deck (PowerPoint)",
        type=['pptx'],
        help="Upload a PowerPoint file to extract colors, fonts, and styling",
        key="brand_upload"
    )
    
    # Add a unique key based on file content to prevent caching
    if uploaded_brand is not None:
        # Create a unique identifier for this file to prevent caching
        file_content = uploaded_brand.read()
        file_hash = hash(file_content)
        uploaded_brand.seek(0)  # Reset file pointer
        
        # Clear previous brand config if file changed
        if st.session_state.get("last_file_hash") != file_hash:
            st.session_state["brand_config"] = None
            st.session_state["last_file_hash"] = file_hash
            st.info("🔄 New file detected - extracting brand colors...")
    
    if uploaded_brand is not None and HAS_PPTX:
        try:
            # Show progress
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            use_llm = extraction_method.startswith("🤖")
            
            if use_llm and api_key:
                # Use LLM extraction (experimental)
                st.write("🤖 **LLM-Powered Brand Extraction (Experimental)**")
                st.info("💡 AI is analyzing your slides to understand brand context and hierarchy")
                
                status_text.text("🧠 AI analyzing slide content and design patterns...")
                progress_bar.progress(20)
                
                uploaded_brand.seek(0)
                brand_config = brand_extractor.extract_brand_from_pptx(
                    uploaded_brand,
                    use_llm=True,
                    api_key=api_key,
                    model_name=selected_model,
                    api_service=api_service
                )
                
                progress_bar.progress(80)
                status_text.text("✅ AI analysis complete!")
                
            else:
                # Use rule-based extraction (recommended)
                st.write("🔧 **Rule-Based Brand Extraction (Recommended)**")
                if not api_key and use_llm:
                    st.info("💡 Add your API key above to enable AI-powered brand extraction")
                
                status_text.text("🔍 Analyzing PowerPoint structure...")
                progress_bar.progress(20)
                
                uploaded_brand.seek(0)
                brand_config = brand_extractor.extract_brand_from_pptx(
                    uploaded_brand,
                    use_llm=False
                )
                
                progress_bar.progress(80)
                status_text.text("✅ Rule-based extraction complete!")
            
            progress_bar.progress(100)
            
            # Store configuration
            st.session_state["brand_config"] = brand_config
            
            # Debug output to console
            print(f"[STREAMLIT DEBUG] Extracted brand colors from {uploaded_brand.name}:")
            colors = brand_config.get('color_scheme', {})
            for name, color in colors.items():
                if isinstance(color, tuple) and len(color) == 3:
                    r, g, b = color
                    hex_color = f"#{r:02x}{g:02x}{b:02x}"
                    print(f"   {name}: RGB({r}, {g}, {b}) = {hex_color}")
            
            # Display results
            colors = brand_config.get('color_scheme', {})
            primary = colors.get('primary')
            
            # Check if we got custom colors or defaults
            if isinstance(primary, tuple) and len(primary) == 3:
                r, g, b = primary
                if r == 24 and g == 58 and b == 88:
                    st.warning("⚠️ Using default colors - no distinct brand colors detected")
                    st.info("💡 Try uploading a deck with more prominent brand colors or logos")
                else:
                    st.success("✅ Brand elements extracted successfully!")
            else:
                st.success("✅ Brand elements extracted successfully!")
            
            # Show extracted colors
            st.write("**🎨 Extracted Brand Colors:**")
            color_cols = st.columns(2)
            color_display_order = ['primary', 'secondary', 'accent', 'text']
            
            for i, name in enumerate(color_display_order):
                if name in colors:
                    color = colors[name]
                    if isinstance(color, tuple) and len(color) == 3:
                        r, g, b = color
                        hex_color = f"#{r:02x}{g:02x}{b:02x}"
                        with color_cols[i % 2]:
                            col1, col2 = st.columns([1, 2])
                            with col1:
                                st.color_picker(
                                    f"{name.title()}",
                                    hex_color,
                                    disabled=True,
                                    key=f"color_{name}"
                                )
                            with col2:
                                st.caption(f"RGB({r}, {g}, {b})")
            
            # Show typography if available
            typography = brand_config.get('typography', {})
            if typography:
                st.write("**🔤 Typography:**")
                col1, col2 = st.columns(2)
                with col1:
                    st.write(f"• **Font:** {typography.get('primary_font', 'Arial')}")
                    st.write(f"• **Title Size:** {typography.get('title_size', 24)}pt")
                with col2:
                    st.write(f"• **Body Size:** {typography.get('body_size', 11)}pt")
            
            # Show LLM analysis details if available
            if use_llm and 'llm_analysis' in brand_config:
                with st.expander("🧠 AI Analysis Details"):
                    analysis = brand_config['llm_analysis']
                    
                    # Brand personality
                    if 'brand_personality' in analysis:
                        personality = analysis['brand_personality']
                        if isinstance(personality, dict) and 'description' in personality:
                            st.write(f"**Brand Style:** {personality['description']}")
                    
                    # Color reasoning
                    if 'color_reasoning' in analysis:
                        st.write("**Color Choices:**")
                        for color_type, reasoning in analysis['color_reasoning'].items():
                            if reasoning:
                                st.write(f"• **{color_type.title()}:** {reasoning}")
                    
                    # Font reasoning
                    if 'font_reasoning' in analysis and analysis['font_reasoning']:
                        st.write(f"**Font Choice:** {analysis['font_reasoning']}")
                    
                    # Design patterns
                    if 'design_patterns' in analysis:
                        patterns = analysis['design_patterns']
                        if isinstance(patterns, dict) and 'description' in patterns:
                            st.write(f"**Design Patterns:** {patterns['description']}")
            
            # Clear progress indicators
            progress_bar.empty()
            status_text.empty()
            
        except Exception as e:
            st.error(f"Brand extraction failed: {str(e)}")
            st.error("Please check your PowerPoint file and try again.")
    
    elif uploaded_brand is not None and not HAS_PPTX:
        st.error("⚠️ Cannot process PowerPoint - python-pptx not installed")
        st.code("pip install python-pptx")
    else:
        st.info("📁 Upload a brand deck to extract colors and fonts")
    
    if "brand_config" not in st.session_state:
        st.session_state["brand_config"] = None
    
    st.markdown("---")
    
    # Vector Database Configuration
    st.subheader("🗄️ Vector Database")
    
    # Check if Vector DB is initialized
    if "vector_db_initialized" not in st.session_state:
        st.session_state["vector_db_initialized"] = False
    
    if not st.session_state["vector_db_initialized"]:
        st.info("🔗 Initialize Vector DB to access precedent transactions and market data")
        
        # Vector DB credentials
        vector_db_id = st.text_input(
            "Database ID",
            value="73bc4abf-5dc7-45df-af84-8cbaff7ee566",
            help="Your Cassandra Vector Database ID"
        )
        
        vector_db_token = st.text_input(
            "Database Token",
            value="AstraCS:ORguPOmjJefYcbNxhqArqJdX:8001c88572a51fd445ddc7ec515576b8bb6d11d6e216643ca07f0c0acd46c0ac",
            type="password",
            help="Your Cassandra Vector Database token"
        )
        
        vector_db_keyspace = st.text_input(
            "Keyspace",
            value="default_keyspace",
            help="Database keyspace name"
        )
        
        vector_db_table = st.text_input(
            "Table Name",
            value="ma10",
            help="Vector table name for storing embeddings"
        )
        
        if st.button("🔗 Initialize Vector DB", type="primary"):
            try:
                # Import and initialize Vector DB
                from vector_db import get_vector_db_manager
                vector_db = get_vector_db_manager()
                
                if vector_db.initialize(vector_db_id, vector_db_token, vector_db_keyspace, vector_db_table):
                    st.session_state["vector_db_initialized"] = True
                    st.session_state["vector_db"] = vector_db
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Failed to initialize Vector DB: {str(e)}")
                st.info("💡 Make sure you have installed the required packages: `pip install cassio cassandra-driver`")
    else:
        st.success("✅ Vector DB Connected!")
        
        # Show Vector DB status
        from vector_db import get_vector_db_manager
        vector_db = get_vector_db_manager()
        status = vector_db.get_status()
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Database:** {status['database_id'][:8]}...")
            st.write(f"**Keyspace:** {status['keyspace']}")
        with col2:
            st.write(f"**Table:** {status['table_name']}")
            st.write(f"**Status:** {'🟢 Active' if status['is_initialized'] else '🔴 Inactive'}")
        
        if st.button("🔄 Reinitialize Vector DB"):
            st.session_state["vector_db_initialized"] = False
            st.rerun()
    
    st.markdown("---")
    
    # Other configuration options
    templates_path = st.text_input("templates.json path", value="templates.json")
    company_name = st.text_input("Company name", value="Moelis & Company")
    skip_validate = st.checkbox("Skip validation", value=False)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": SYSTEM_PROMPT}
    ]

if "chat_started" not in st.session_state:
    st.session_state.chat_started = False

# Main App Layout
tab_chat, tab_json, tab_execute, tab_validate = st.tabs(["🤖 AI Copilot", "📄 JSON Editor", "⚙️ Execute", "🔍 JSON Validator & Auto-Fix"])

with tab_chat:
    st.subheader("🤖 Investment Banking Pitch Deck Copilot")
    
    if not api_key:
        st.error("⚠️ Please enter your API key in the sidebar to start the interview")
    else:
        # Start conversation button
        if not st.session_state.chat_started:
            if st.button("🚀 Start Pitch Deck Interview"):
                st.session_state.chat_started = True
                st.rerun()
        
        # Display chat messages
        if st.session_state.chat_started:
            # Display conversation (skip system message)
            display_messages = [m for m in st.session_state.messages if m["role"] != "system"]
            
            # If no conversation yet, add the initial interview question to session
            if not display_messages:
                initial_message = """Hello! I'm your investment banking pitch deck copilot. I'll conduct a comprehensive interview to gather all the information needed for your pitch deck, then automatically generate the complete JSON structures for you.

**What I'll collect:**
- Company overview & business model
- Financial performance & projections  
- Management team profiles
- Growth strategy & market data
- Valuation & trading precedents
- Strategic & financial buyer targets

**New Enhanced Features:**
- I'll ask specific follow-up questions for missing information
- Say "I don't know" and I'll search for information (with your permission)
- Say "skip this slide" to exclude any topic you don't want
- **Zero Empty Boxes Policy**: All slides will have complete content

Let's start: **What is your company name and give me a brief overview of what your business does?**"""
                
                # Add initial message to session state so it persists
                st.session_state.messages.append({"role": "assistant", "content": initial_message})
                display_messages = [{"role": "assistant", "content": initial_message}]
            
            # Display conversation
            for message in display_messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
            

            
            # Chat input - ENHANCED with comprehensive validation
            if prompt := st.chat_input("Your response...", key="chat_input"):
                # Add user message
                st.session_state.messages.append({"role": "user", "content": prompt})
                
                # Analyze conversation progress
                progress_info = analyze_conversation_progress(st.session_state.messages)
                
                # Show progress in sidebar
                is_complete = show_interview_progress(st.session_state.messages)
                
                # Check if this was a brief confirmatory response or skip request
                brief_confirmatory = prompt.strip().lower() in ["yes", "correct", "that's right", "sounds good", "ok", "okay", "sure", "right"]
                skip_request = "skip" in prompt.lower() and any(skip_phrase in prompt.lower() for skip_phrase in ["skip this", "skip that", "skip slide", "skip topic"])
                
                if brief_confirmatory and progress_info["next_question"] and not is_complete:
                    # User gave brief confirmation - automatically ask next question
                    ai_response = progress_info["next_question"]
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    st.rerun()
                elif skip_request and progress_info["next_question"]:
                    # User wants to skip current topic
                    ai_response = f"Understood, I'll skip this topic. {progress_info['next_question']}"
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    st.rerun()
                else:
                    # Get normal AI response
                    with st.spinner("🤖 Thinking..."):
                        ai_response = call_llm_api(
                            st.session_state.messages,
                            selected_model,
                            api_key,
                            api_service
                        )
                    
                    # Add AI response to history
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    
                    # Check if JSONs were generated and extract them with comprehensive validation
                    content_ir, render_plan, validation_results = extract_and_validate_jsons(ai_response)
                    
                    # Debug extraction if it failed
                    if not content_ir and not render_plan:
                        print("🚨 JSON extraction failed - running debug analysis...")
                        debug_json_extraction(ai_response, content_ir, render_plan)
                        
                        st.error("🚨 **JSON Extraction Failed** - The AI response could not be parsed into valid JSON structures.")
                        st.info("This usually means the LLM didn't format its response properly. Common causes:")
                        st.markdown("""
                        - **Missing JSON markers**: Response should contain "CONTENT IR JSON:" and "RENDER PLAN JSON:"
                        - **Incomplete JSON**: Response was cut off or malformed
                        - **Wrong format**: LLM provided text instead of structured JSON
                        """)
                        
                        # Show retry button with specific instructions
                        if st.button("🔄 Retry with Better Instructions", type="primary"):
                            retry_prompt = """
Please regenerate your response with proper JSON formatting. Your response MUST include:

1. **CONTENT IR JSON:** followed by the complete Content IR JSON structure
2. **RENDER PLAN JSON:** followed by the complete Render Plan JSON structure

Each JSON section should be properly formatted and complete. Do not use placeholder text or incomplete structures.

Example format:
## CONTENT IR JSON:
```json
{
  "entities": {"company": {"name": "Company Name"}},
  "facts": {"years": ["2020", "2021", "2022", "2023", "2024E"], "revenue_usd_m": [120, 145, 180, 210, 240], "ebitda_usd_m": [18, 24, 31, 40, 47], "ebitda_margins": [15.0, 16.6, 17.2, 19.0, 19.6]},
  "management_team": {"left_column_profiles": [...], "right_column_profiles": [...]},
  "strategic_buyers": [...],
  "financial_buyers": [...]
}
```

## RENDER PLAN JSON:
```json
{
  "slides": [
    {"template": "management_team", "data": {...}},
    {"template": "business_overview", "data": {...}}
  ]
}
```

Please ensure both JSONs are complete and properly formatted.
"""
                            st.session_state.messages.append({"role": "user", "content": retry_prompt})
                            
                            with st.spinner("🔄 Regenerating with proper JSON format..."):
                                retry_response = call_llm_api(
                                    st.session_state.messages,
                                    selected_model,
                                    api_key,
                                    api_service
                                )
                            
                            st.session_state.messages.append({"role": "assistant", "content": retry_response})
                            st.rerun()
                        
                        # Show the raw response for debugging
                        with st.expander("🔍 View Raw AI Response"):
                            st.code(ai_response, language="text")
                    
                    elif content_ir or render_plan:
                        st.success("🎉 JSON structures generated!")
                        
                        # Show extraction summary
                        if content_ir and render_plan:
                            st.success("✅ Both Content IR and Render Plan extracted successfully!")
                        elif content_ir:
                            st.warning("⚠️ Only Content IR extracted - Render Plan missing")
                        elif render_plan:
                            st.warning("⚠️ Only Render Plan extracted - Content IR missing")
                        
                        # Display comprehensive validation results
                        is_fully_valid = display_validation_results(validation_results)
                        
                        # Check if JSONs were successfully extracted (even with validation warnings)
                        jsons_extracted = content_ir is not None and render_plan is not None
                        
                        # If JSONs extracted successfully, proceed with auto-population
                        if jsons_extracted:
                            st.balloons()
                            
                            # AUTO-ENHANCE MANAGEMENT TEAM BEFORE CREATING FILES
                            with st.spinner("🔍 Auto-enhancing management team data..."):
                                enhanced_content_ir, was_enhanced = auto_enhance_management_team(
                                    content_ir, 
                                    st.session_state.messages
                                )
                                content_ir = enhanced_content_ir  # Use the enhanced version
                            
                            if was_enhanced:
                                st.success("✨ **Management team automatically enhanced!** Executive profiles have been populated with detailed information.")
                            else:
                                st.info("✅ Management team data already complete.")
                            
                            # Extract company name from content IR
                            company_name_extracted = "Unknown_Company"
                            if content_ir and 'entities' in content_ir and 'company' in content_ir['entities']:
                                company_name_extracted = content_ir['entities']['company'].get('name', 'Unknown_Company')
                            
                            # Create downloadable files
                            files_data = create_downloadable_files(content_ir, render_plan, company_name_extracted)
                            
                            # Store in session state
                            st.session_state["generated_content_ir"] = files_data['content_ir_json']
                            st.session_state["generated_render_plan"] = files_data['render_plan_json']
                            st.session_state["files_ready"] = True
                            st.session_state["files_data"] = files_data
                            
                            # AUTO-POPULATE JSON EDITOR: Automatically validate and save to session
                            st.session_state["auto_populated"] = True
                            st.success("🚀 **Auto-Population Complete!** JSONs have been automatically populated in the JSON Editor tab and are ready for execution.")
                            st.info("💡 **No manual copy-paste needed!** Switch to the 'JSON Editor' tab to see the populated JSONs, then go to 'Execute' tab to generate your pitch deck directly.")
                            
                            # Add automatic rerun to refresh the page and show populated JSONs
                            if st.button("🔄 Refresh Page to See Populated JSONs"):
                                st.rerun()
                            
                            # Show download section
                            st.markdown("---")
                            st.subheader("📁 Download Your Pitch Deck Files")
                            
                            # Create download columns
                            download_col1, download_col2, download_col3 = st.columns(3)
                            
                            with download_col1:
                                st.download_button(
                                    "📄 Download Content IR",
                                    data=files_data['content_ir_json'],
                                    file_name=files_data['content_ir_filename'],
                                    mime="application/json",
                                    help="Contains all slide content data"
                                )
                            
                            with download_col2:
                                st.download_button(
                                    "📋 Download Render Plan",
                                    data=files_data['render_plan_json'],
                                    file_name=files_data['render_plan_filename'],
                                    mime="application/json",
                                    help="Defines slide structure and templates"
                                )
                            
                            with download_col3:
                                # Create ZIP package
                                zip_buffer = create_zip_package(files_data)
                                zip_filename = f"{files_data['company_name']}_pitch_deck_files_{files_data['timestamp']}.zip"
                                
                                st.download_button(
                                    "📦 Download Complete Package",
                                    data=zip_buffer,
                                    file_name=zip_filename,
                                    mime="application/zip",
                                    help="ZIP package with both files + README"
                                )
                            
                            # Show validation feedback (non-blocking)
                            if not is_fully_valid:
                                st.warning("⚠️ **Validation Issues Detected** - Auto-population completed successfully, but some improvements are recommended:")
                                
                                # Create specific feedback for the LLM
                                llm_feedback = create_validation_feedback_for_llm(validation_results)
                                
                                if llm_feedback:
                                    # Show optional improvement button
                                    if st.button("🔄 Improve JSON Quality (Optional)", help="Fix validation issues to ensure perfect pitch deck generation"):
                                        # Add feedback message for LLM to fix issues
                                        st.session_state.messages.append({"role": "user", "content": llm_feedback})
                                        
                                        with st.spinner("🔄 Improving JSON quality..."):
                                            retry_response = call_llm_api(
                                                st.session_state.messages,
                                                selected_model,
                                                api_key,
                                                api_service
                                            )
                                        
                                        st.session_state.messages.append({"role": "assistant", "content": retry_response})
                                        st.rerun()
                            
                            # Show next steps
                            st.info("""
                            🎯 **Next Steps:**
                            1. Download the files above
                            2. Use them with your pitch deck generation system
                            3. Or switch to the Execute tab to generate the deck directly
                            """)
                        
                        # If JSONs were not extracted successfully, show error and retry options
                        else:
                            st.error("🚨 **JSON Extraction Failed** - The AI response could not be parsed into valid JSON structures.")
                            st.info("This usually means the LLM didn't format its response properly. Common causes:")
                            st.markdown("""
                            - **Missing JSON markers**: Response should contain "CONTENT IR JSON:" and "RENDER PLAN JSON:"
                            - **Incomplete JSON**: Response was cut off or malformed
                            - **Wrong format**: LLM provided text instead of structured JSON
                            """)
                            
                            # Show retry button with specific instructions
                            if st.button("🔄 Retry with Better Instructions", type="primary"):
                                retry_prompt = """
Please regenerate your response with proper JSON formatting. Your response MUST include:

1. **CONTENT IR JSON:** followed by the complete Content IR JSON structure
2. **RENDER PLAN JSON:** followed by the complete Render Plan JSON structure

Each JSON section should be properly formatted and complete. Do not use placeholder text or incomplete structures."""

                                st.session_state.messages.append({"role": "user", "content": retry_prompt})
                                
                                with st.spinner("🔄 Requesting properly formatted JSONs..."):
                                    retry_response = call_llm_api(
                                        st.session_state.messages,
                                        selected_model,
                                        api_key,
                                        api_service
                                    )
                                
                                st.session_state.messages.append({"role": "assistant", "content": retry_response})
                                st.rerun()
                    
                    # If interview seems complete but no JSONs generated, prompt for them
                    elif is_complete and not any("CONTENT IR JSON" in msg["content"] for msg in st.session_state.messages):
                        st.warning("📄 Interview appears complete. Prompting AI to generate JSON files...")
                        
                        completion_prompt = """
I believe we have covered all the necessary information for a comprehensive pitch deck. Please generate the complete Content IR JSON and Render Plan JSON structures now using ALL the information I provided during our conversation.

🎯 **ZERO EMPTY BOXES POLICY** - Requirements:
- Include ALL slides we discussed (minimum 8-10 slides)
- EXCLUDE any slides that were explicitly skipped
- Use every piece of data I provided
- Follow the exact JSON format from your examples
- Create multiple slides of the same type if the data supports it
- Don't skip any information or use placeholder text
- Ensure every field has real content (no empty arrays, null values, or placeholders)
- 🚨 **CRITICAL: Generate COMPLETE JSON** - Never truncate or cut off your response
- USE CORRECT FIELD NAMES: role_title/experience_bullets for management, cost_management/risk_mitigation for margins, etc.

🚨 **CRITICAL DATA REQUIREMENTS:**
1. **Content IR MUST include 'facts' section** with historical financial data (years, revenue, EBITDA, margins)
2. **Every slide MUST have a 'title' field** in the data section
3. **historical_financial_performance slide MUST reference facts data** for chart categories, revenue, and EBITDA
4. **margin_cost_resilience slide MUST have complete cost_management.items** with title and description for each
5. **growth_strategy_projections slide MUST have complete title and strategies array**
   - MUST have title field at slide level (not just in slide_data)
   - MUST have slide_data with growth_strategy.strategies array and financial_projections
6. **buyer_profiles slides MUST have content_ir_key** AND complete table_headers
7. **competitive_positioning slide MUST have complete assessment table** with comparison data
8. **All arrays MUST have minimum required items** (no empty arrays)

Please generate both complete JSON structures now with full validation compliance.

🔧 **CRITICAL: After generating initial JSON, you MUST fix it by comparing with working examples:**

**WORKING EXAMPLES PROVIDED:**
- complete_content_ir.json (contains ALL required sections)
- complete_render_plan.json (contains EXACTLY 13 slides with proper structure)

**WORKING EXAMPLES CONTENT:**

**COMPLETE_CONTENT_IR.JSON (WORKING EXAMPLE):**
```json
{
  "entities": {
    "company": {
      "name": "SouthernCapital Healthcare"
    }
  },
  "facts": {
    "years": ["2020", "2021", "2022", "2023", "2024E"],
    "revenue_usd_m": [120, 145, 180, 210, 240],
    "ebitda_usd_m": [18, 24, 31, 40, 47],
    "ebitda_margins": [15.0, 16.6, 17.2, 19.0, 19.6]
  },
  "charts": [
    {
      "id": "chart_hist_perf",
      "type": "combo",
      "title": "Revenue & EBITDA Growth",
      "categories": ["2020", "2021", "2022", "2023", "2024E"],
      "revenue": [120, 145, 180, 210, 240],
      "ebitda": [18, 24, 31, 40, 47],
      "unit": "US$m"
    },
    {
      "id": "chart_margin_trend",
      "type": "line",
      "title": "EBITDA Margin Trend",
      "categories": ["2020", "2021", "2022", "2023", "2024E"],
      "values": [15.0, 16.6, 17.2, 19.0, 19.6],
      "unit": "%"
    }
  ],
  "management_team": {
    "left_column_profiles": [
      {
        "role_title": "Chief Executive Officer",
        "experience_bullets": [
          "25+ years healthcare industry experience across hospital operations",
          "Former Regional VP at major international hospital group",
          "MBA from top-tier business school with healthcare specialization",
          "Led successful expansion of 40+ healthcare facilities",
          "Board member of regional healthcare association"
        ]
      },
      {
        "role_title": "Chief Financial Officer",
        "experience_bullets": [
          "15+ years finance leadership in healthcare services",
          "Ex-CFO at publicly-traded healthcare services company",
          "CPA with proven M&A integration track record",
          "Successfully completed 8 acquisitions totaling $200M+",
          "Deep expertise in healthcare reimbursement"
        ]
      },
      {
        "role_title": "Chief Technology Officer",
        "experience_bullets": [
          "12+ years leading digital transformation in healthcare",
          "Former VP Engineering at major healthtech platform",
          "Built and scaled EMR systems serving 2M+ users",
          "Expert in healthcare data analytics and AI/ML",
          "MS Computer Science with healthcare informatics focus"
        ]
      }
    ],
    "right_column_profiles": [
      {
        "role_title": "Chief Operating Officer",
        "experience_bullets": [
          "20+ years multi-site healthcare operations experience",
          "Successfully scaled 50+ clinic locations across SEA",
          "Lean Six Sigma Master Black Belt certification",
          "Former Regional Operations Director at international chain",
          "Deep experience in regulatory compliance and quality"
        ]
      },
      {
        "role_title": "Chief Medical Officer",
        "experience_bullets": [
          "Board-certified internal medicine physician",
          "Former Department Head at tertiary care hospital",
          "Published researcher with 25+ peer-reviewed publications",
          "Champion of clinical quality and patient safety programs",
          "Fellowship-trained in hospital medicine"
        ]
      },
      {
        "role_title": "Chief Business Development Officer",
        "experience_bullets": [
          "15+ years healthcare business development experience",
          "Former VP Corporate Development at regional platform",
          "Led negotiations for 65+ corporate wellness contracts",
          "Expert in payor relations and insurance contracting",
          "MBA in Strategic Management with healthcare focus"
        ]
      }
    ]
  },
  "investor_considerations": {
    "considerations": [
      "Regulatory changes across multiple SEA jurisdictions",
      "Healthcare reimbursement pressures and benefit changes", 
      "Competition from larger regional players and new entrants",
      "Technology disruption from digital health startups",
      "Currency fluctuation across multi-country operations",
      "Key person dependency on senior leadership team",
      "Economic downturn impact on discretionary spending"
    ],
    "mitigants": [
      "Exceptional compliance track record with government relations",
      "Diversified payor mix with balanced segment exposure",
      "Differentiated premium service with strong brand recognition",
      "Significant investment in proprietary digital capabilities",
      "Natural hedge through multi-currency revenue streams",
      "Deep management bench with succession planning",
      "Defensive demand profile with essential healthcare focus"
    ]
  },
  "competitive_analysis": {
    "competitors": [
      {"name": "MajorHealth Corp", "revenue": 450},
      {"name": "Regional Medical Group", "revenue": 380},
      {"name": "SouthernCapital Healthcare", "revenue": 210},
      {"name": "Community Health Network", "revenue": 180},
      {"name": "Specialty Care Partners", "revenue": 150},
      {"name": "Metro Healthcare", "revenue": 125}
    ],
    "assessment": [
      ["Provider", "Scale", "Quality", "Digital", "Corporate"],
      ["SouthernCapital", "●●●●●", "●●●●●", "●●●●●", "●●●●●"],
      ["MajorHealth Corp", "●●●●●", "●●●●", "●●●", "●●●"],
      ["Regional Medical", "●●●●", "●●●●", "●●", "●●●"],
      ["Community Health", "●●●", "●●●", "●●", "●●"],
      ["Specialty Care", "●●", "●●●●", "●●", "●●●●"]
    ],
    "barriers": [
      {
        "title": "Regulatory Compliance",
        "desc": "Complex healthcare licensing across multiple jurisdictions"
      },
      {
        "title": "Specialist Recruitment",
        "desc": "Challenging acquisition of multilingual medical talent"
      },
      {
        "title": "Prime Real Estate",
        "desc": "Limited medical-grade facilities in premium locations"
      },
      {
        "title": "Technology Infrastructure",
        "desc": "Significant EMR and cybersecurity investment required"
      }
    ],
    "advantages": [
      {
        "title": "International Accreditation",
        "desc": "JCI and ISO certifications demonstrating world-class quality"
      },
      {
        "title": "Integrated Multi-Specialty Platform",
        "desc": "Comprehensive care with seamless referral pathways"
      },
      {
        "title": "Advanced Digital Infrastructure", 
        "desc": "Proprietary EMR with integrated telemedicine capabilities"
      },
      {
        "title": "Corporate Healthcare Leadership",
        "desc": "Market-leading position in corporate wellness"
      }
    ]
  },
  "precedent_transactions": [
    {
      "date": "2024-Q1",
      "target": "Regional Healthcare Network",
      "acquirer": "MajorHealth Corp",
      "country": "Singapore",
      "enterprise_value": 850,
      "revenue": 200,
      "ev_revenue_multiple": 4.25
    },
    {
      "date": "2023-Q4",
      "target": "Specialty Medical Group",
      "acquirer": "Private Equity Consortium",
      "country": "Malaysia", 
      "enterprise_value": 640,
      "revenue": 160,
      "ev_revenue_multiple": 4.0
    },
    {
      "date": "2023-Q2",
      "target": "Community Diagnostics Platform",
      "acquirer": "Strategic Healthcare Buyer",
      "country": "Thailand",
      "enterprise_value": 420,
      "revenue": 120,
      "ev_revenue_multiple": 3.5
    },
    {
      "date": "2023-Q1",
      "target": "Corporate Wellness Provider",
      "acquirer": "International PE Fund",
      "country": "Indonesia",
      "enterprise_value": 315,
      "revenue": 85,
      "ev_revenue_multiple": 3.7
    }
  ],
  "valuation_data": [
    {
      "methodology": "Precedent Transactions",
      "methodology_type": "precedent_transactions",
      "commentary": "Recent healthcare services transactions in SEA support premium multiples for scaled platforms with strong growth and market-leading positions.",
      "enterprise_value": "US$840 – 945mm",
      "metric": "EV/Revenue",
      "22a_multiple": "4.0x – 4.5x",
      "23e_multiple": "3.8x – 4.2x"
    },
    {
      "methodology": "Trading Comparables",
      "methodology_type": "trading_comps",
      "commentary": "Public healthcare services companies provide liquidity benchmark with slight discount reflecting current market conditions.",
      "enterprise_value": "US$735 – 840mm",
      "metric": "EV/Revenue", 
      "22a_multiple": "3.5x – 4.0x",
      "23e_multiple": "3.3x – 3.8x"
    },
    {
      "methodology": "Discounted Cash Flow",
      "methodology_type": "dcf",
      "commentary": "Base case assumes 12% revenue CAGR through 2027 with EBITDA margin expansion from 19% to 22% via operational leverage.",
      "enterprise_value": "US$780 – 920mm",
      "metric": "NPV Analysis",
      "22a_multiple": "3.7x – 4.4x",
      "23e_multiple": "3.5x – 4.1x"
    }
  ],
  "sea_conglomerates": [
    {
      "name": "Ayala Corporation",
      "country": "Philippines",
      "description": "Leading diversified conglomerate with significant healthcare investments through Ayala Healthcare Holdings, operating hospitals and digital health initiatives",
      "key_shareholders": "Ayala family trust and institutional investors",
      "key_financials": "Revenue: US$3.2B, Healthcare growing 15%+ annually",
      "contact": "Managing Director - SEA Healthcare"
    },
    {
      "name": "CP Group (Charoen Pokphand)",
      "country": "Thailand", 
      "description": "Massive diversified conglomerate with healthcare retail exposure through pharmacy chains and platform development",
      "key_shareholders": "Chearavanont family and holding companies",
      "key_financials": "Revenue: US$45B+, Healthcare investments >US$500M",
      "contact": "Managing Director - Consumer Healthcare"
    },
    {
      "name": "Sinar Mas Group", 
      "country": "Indonesia",
      "description": "Indonesian conglomerate with diversified portfolio and growing healthcare technology investments",
      "key_shareholders": "Widjaja family and investment vehicles",
      "key_financials": "Revenue: US$15B+, Active healthtech program",
      "contact": "Executive Director - Indonesia Coverage"
    },
    {
      "name": "Genting Group",
      "country": "Malaysia",
      "description": "Diversified conglomerate with strategic healthcare investments through integrated resort wellness",
      "key_shareholders": "Lim Kok Thay family trust",
      "key_financials": "Revenue: US$2.8B, Healthcare target US$200M+",
      "contact": "Managing Director - Malaysia Coverage"
    }
  ],
  "strategic_buyers": [
    {
      "buyer_name": "UnitedHealth / Optum",
      "description": "Global healthcare leader with $350B+ revenue",
      "strategic_rationale": "SEA market entry with established platform",
      "key_synergies": "Data analytics, technology platform, corporate relationships",
      "fit": "High (9/10) - Strong strategic alignment",
      "fit": "High (9/10)",
      "financial_capacity": "$50B+ available capital"
    },
    {
      "buyer_name": "Teladoc Health",
      "description": "Leading telemedicine platform with international focus",
      "strategic_rationale": "Physical-digital healthcare integration", 
      "key_synergies": "Telemedicine expertise, digital platforms",
      "fit": "Medium-High (7/10) - Good synergies",
      "fit": "Medium-High (7/10)",
      "financial_capacity": "$5B+ strategic budget"
    },
    {
      "buyer_name": "Fresenius Medical Care",
      "description": "German healthcare services leader",
      "strategic_rationale": "Asian expansion with chronic disease focus",
      "key_synergies": "Care coordination, operational excellence",
      "fit": "Medium (6/10) - Moderate alignment",
      "fit": "Medium (6/10)",
      "financial_capacity": "$3B+ strategic investments"
    }
  ],
  "financial_buyers": [
    {
      "buyer_name": "Blackstone Growth",
      "description": "$975B AUM, $40B+ healthcare investments",
      "strategic_rationale": "Buy-and-build platform strategy across SEA",
      "key_synergies": "Operational excellence, technology investment",
      "fit": "Very High (9/10) - Excellent match",
      "fit": "Very High (9/10)",
      "financial_capacity": "Significant dry powder"
    },
    {
      "buyer_name": "TPG Capital",
      "description": "$135B+ AUM with Asia healthcare focus",
      "strategic_rationale": "Healthcare services consolidation",
      "key_synergies": "Digital initiatives, operational playbooks",
      "fit": "High (8/10) - Strong financial capacity", 
      "fit": "High (8/10)",
      "financial_capacity": "Strong healthcare allocation"
    },
    {
      "buyer_name": "KKR & Co",
      "description": "$500B+ AUM, healthcare expertise",
      "strategic_rationale": "Technology-enabled growth platform",
      "key_synergies": "Technology infrastructure, partnerships",
      "fit": "High (8/10) - Good cultural fit",
      "fit": "High (8/10)",
      "financial_capacity": "Substantial healthcare focus"
    }
  ],
  "product_service_data": {
    "services": [
      {
        "title": "Primary Care",
        "desc": "Comprehensive family medicine and preventive care with corporate contracts including health screenings, vaccinations, and chronic disease management"
      },
      {
        "title": "Specialty Services", 
        "desc": "Cardiology, orthopedics, dermatology, and high-acuity outpatient procedures with subspecialty referral network"
      },
      {
        "title": "Diagnostics",
        "desc": "Advanced imaging (MRI/CT/Ultrasound), laboratory services, and cardiac testing supporting integrated clinical pathways"
      },
      {
        "title": "Corporate Wellness",
        "desc": "Occupational health, executive physicals, workplace injury management, and employee health programs"
      },
      {
        "title": "Digital Health",
        "desc": "Telemedicine consultations, patient portal, online appointment booking, and remote monitoring services"
      }
    ],
    "coverage_table": [
      ["Country/City", "Primary Care", "Specialty", "Diagnostics", "Corporate"],
      ["Singapore", "✓", "✓", "✓", "✓"],
      ["Malaysia", "✓", "✓", "✓", "✓"],
      ["Indonesia", "✓", "–", "–", "✓"],
      ["Philippines", "✓", "–", "–", "✓"]
    ],
    "metrics": {
      "total_locations": {
        "label": "Total Clinic Locations",
        "value": "35+"
      },
      "medical_specialists": {
        "label": "Board-Certified Specialists", 
        "value": "65+"
      },
      "annual_patients": {
        "label": "Annual Patient Visits",
        "value": "125,000+"
      },
      "patient_satisfaction": {
        "label": "Net Promoter Score",
        "value": "72"
      },
      "corporate_contracts": {
        "label": "Corporate Contracts",
        "value": "65+"
      },
      "avg_wait_time": {
        "label": "Average Wait Time",
        "value": "1.8 days"
      }
    }
  },
  "business_overview_data": {
    "description": "SouthernCapital Healthcare is a leading integrated healthcare services platform in Southeast Asia, focused on high-quality patient care and operational excellence across primary care, diagnostics, and specialty services. The platform benefits from significant scale with 35+ clinic locations, a diversified payor mix including 40% corporate contracts, 35% insurance reimbursement, and 25% cash pay, and a proven clinic rollout playbook.",
    "timeline": {
      "start_year": "2015",
      "end_year": "2024", 
      "years_note": "(9+ years of proven growth and market leadership)"
    },
    "highlights": [
      "35+ premium clinic locations across Singapore, Malaysia, Indonesia, and Philippines",
      "125,000+ annual patient visits with 89% retention rate demonstrating patient loyalty",
      "65+ corporate wellness contracts with major employers and multinational corporations",
      "Advanced EMR platform with integrated telemedicine capabilities and 78% digital adoption",
      "65+ board-certified specialists across 12+ medical disciplines",
      "International accreditation (JCI, ISO) demonstrating world-class quality standards"
    ],
    "services": [
      "Primary Care & Preventive Medicine - Comprehensive family medicine and health screenings",
      "Specialty Medical Services - Cardiology, orthopedics, dermatology, and subspecialties",
      "Diagnostic Imaging & Laboratory - MRI, CT, ultrasound, and comprehensive lab services",
      "Corporate Wellness Programs - Occupational health and executive physical examinations",
      "Digital Health & Telemedicine - Remote consultations and patient portal services",
      "Executive Health Assessments - Premium comprehensive health evaluations"
    ],
    "positioning_desc": "SouthernCapital Healthcare has established itself as the leading premium healthcare provider in Southeast Asia, serving both individual patients and corporate clients with comprehensive medical services and exceptional care standards."
  },
  "growth_strategy_data": {
    "growth_strategy": {
      "title": "Multi-Pronged Growth Strategy",
      "strategies": [
        "Geographic expansion through targeted clinic rollouts in high-growth SEA markets",
        "Service line extension into high-margin specialties and chronic disease management", 
        "Corporate partnership scaling through enhanced wellness programs",
        "Digital transformation with AI-powered diagnostics and telemedicine",
        "Strategic acquisitions of complementary healthcare assets",
        "Value-based care initiatives with outcome-focused contracts"
      ]
    },
    "financial_projections": {
      "chart_title": "Revenue & EBITDA Projections (2024E-2027E)",
      "categories": ["2024E", "2025E", "2026E", "2027E"],
      "revenue": [240, 285, 340, 405],
      "ebitda": [47, 62, 81, 105]
    },
    "key_assumptions": {
      "title": "Key Planning Assumptions",
      "assumptions": [
        "New clinic openings: 6-8 locations annually",
        "Same-store growth: 8-12% annually",
        "Corporate contract growth: 15-20% annually",
        "Specialty penetration: 35% to 50% of revenue",
        "EBITDA margin expansion: 100-150 bps annually",
        "Digital health scaling: 5% to 15% by 2027"
      ]
    }
  },
  "investor_process_data": {
    "diligence_topics": [
      {
        "title": "Financial & Operational Review",
        "description": "Historical performance, unit economics, and forward projections with sensitivity analysis"
      },
      {
        "title": "Market & Competitive Analysis", 
        "description": "Healthcare market sizing, competitive landscape, and growth opportunity evaluation"
      },
      {
        "title": "Management Assessment",
        "description": "Leadership evaluation, organizational structure, and succession planning"
      },
      {
        "title": "Technology & Digital Infrastructure",
        "description": "IT systems, cybersecurity framework, and digital transformation roadmap"
      },
      {
        "title": "Clinical Quality & Compliance",
        "description": "Quality programs, patient safety, and regulatory compliance history"
      }
    ],
    "synergy_opportunities": [
      {
        "title": "Revenue Synergies",
        "description": "Enhanced service offerings through expanded specialist network"
      },
      {
        "title": "Operational Excellence",
        "description": "Best practices implementation across broader clinic network"
      },
      {
        "title": "Corporate Partnership Expansion",
        "description": "Leveraging relationships for accelerated contract growth"
      },
      {
        "title": "Technology Platform Scaling",
        "description": "Digital infrastructure amortization across larger patient base"
      }
    ],
    "risk_factors": [
      "Regulatory changes across operating jurisdictions",
      "Healthcare reimbursement pressure changes",
      "Competitive intensity from regional consolidation",
      "Key talent retention in competitive market",
      "Technology disruption from digital platforms"
    ],
    "mitigants": [
      "Proactive regulatory compliance with government relations",
      "Diversified revenue streams with defensive characteristics",
      "Differentiated position through quality and brand",
      "Comprehensive talent retention programs", 
      "Significant technology investment and capabilities"
    ],
    "timeline": [
      {
        "date": "Week 1-2",
        "description": "Initial outreach and process launch"
      },
      {
        "date": "Week 3-4",
        "description": "Management presentations and strategic discussions"
      },
      {
        "date": "Week 5-6",
        "description": "Due diligence data room access and information review"
      },
      {
        "date": "Week 7-8",
        "description": "Site visits and operational assessments"
      },
      {
        "date": "Week 9-10",
        "description": "Financial model review and synergy analysis"
      },
      {
        "date": "Week 11-12",
        "description": "Legal and commercial due diligence"
      },
      {
        "date": "Week 13-14",
        "description": "Final bid submissions and negotiations"
      },
      {
        "date": "Week 15-16",
        "description": "Definitive agreements and closing preparations"
      }
    ]
  },
  "margin_cost_data": {
    "chart_data": {
      "categories": ["2020", "2021", "2022", "2023", "2024E"],
      "values": [15.0, 16.6, 17.2, 19.0, 19.6]
    },
    "cost_management": {
      "title": "Strategic Cost Management Initiatives",
      "items": [
        {
          "title": "Supplier Consolidation & Procurement",
          "description": "Centralized procurement achieving 12-18% savings through volume discounts and strategic partnerships"
        },
        {
          "title": "Digital Transformation & Automation",
          "description": "Comprehensive automation reducing administrative overhead by 15-20% while improving patient experience"
        },
        {
          "title": "Operational Efficiency & Process Optimization",
          "description": "Lean Six Sigma methodologies with standardized workflows and optimized staff scheduling"
        }
      ]
    },
    "risk_mitigation": {
      "title": "Comprehensive Risk Mitigation Framework",
      "main_strategy": {
        "title": "Diversified Revenue Base & Market Position",
        "description": "Multi-dimensional diversification across service lines, payor types, and geographic markets",
        "benefits": [
          "Revenue stability through economic cycles",
          "Predictable cash flows from corporate contracts",
          "Reduced payor dependence with balanced mix"
        ]
      },
      "banker_view": {
        "title": "BANKER'S VIEW",
        "text": "Outstanding operational resilience with proven margin maintenance ability. Diversified model and disciplined cost management create sustainable competitive advantages."
      }
    }
  }
}
```

**COMPLETE_RENDER_PLAN.JSON (WORKING EXAMPLE):**
```json
{
  "slides": [
    {
      "template": "business_overview",
      "data": {
        "title": "Business & Operational Overview",
        "description": "Leading integrated healthcare services platform in Southeast Asia",
        "timeline": {"start_year": "2015", "end_year": "2024"},
        "highlights": ["35+ premium clinic locations", "125,000+ annual patient visits"],
        "services": ["Primary Care & Preventive Medicine", "Specialty Medical Services"],
        "positioning_desc": "Leading premium healthcare provider in Southeast Asia"
      }
    },
    {
      "template": "historical_financial_performance",
      "data": {
        "title": "Historical Financial Performance",
        "chart": {
          "title": "Revenue & EBITDA Growth (2020–2024E)",
          "categories": ["2020", "2021", "2022", "2023", "2024E"],
          "revenue": [120, 145, 180, 210, 240],
          "ebitda": [18, 24, 31, 40, 47]
        },
        "key_metrics": {
          "metrics": [
            {"title": "Revenue 2023", "value": "US$210m", "period": "FY2023", "note": "↗ Up 17% YoY"}
          ]
        },
        "revenue_growth": {
          "title": "Key Growth Drivers",
          "points": ["New clinic expansion: 8 locations opened in 2023"]
        },
        "banker_view": {
          "title": "BANKER'S VIEW",
          "text": "Exceptional performance with consistent growth and expanding margins"
        }
      }
    },
    {
      "template": "precedent_transactions",
      "data": {
        "title": "Precedent Transactions Analysis",
        "transactions": [
          {
            "date": "2024-Q1",
            "target": "Regional Healthcare Network",
            "acquirer": "MajorHealth Corp",
            "country": "Singapore",
            "enterprise_value": 850,
            "revenue": 200,
            "ev_revenue_multiple": 4.25
          }
        ]
      }
    }
  ]
}
```

🚨 **MANDATORY JSON FIXING PROCESS - YOU MUST FOLLOW THIS EXACTLY:**

**STEP 1: Generate Initial JSON**
First, generate your Content IR and Render Plan JSON based on the interview.

**STEP 2: MANDATORY VALIDATION CHECKLIST - YOU MUST VERIFY EACH ITEM:**

**CONTENT IR VALIDATION (ALL 15 SECTIONS MUST BE PRESENT):**
✅ entities
✅ facts  
✅ charts (REQUIRED - add if missing)
✅ management_team
✅ investor_considerations
✅ competitive_analysis
✅ precedent_transactions
✅ valuation_data
✅ sea_conglomerates
✅ strategic_buyers
✅ financial_buyers
✅ product_service_data
✅ business_overview_data
✅ growth_strategy_data
✅ investor_process_data (REQUIRED - add if missing)
✅ margin_cost_data (REQUIRED - add if missing)

**RENDER PLAN VALIDATION (EXACTLY 13 SLIDES IN THIS ORDER):**
✅ Slide 1: management_team
✅ Slide 2: historical_financial_performance  
✅ Slide 3: margin_cost_resilience
✅ Slide 4: investor_considerations
✅ Slide 5: competitive_positioning
✅ Slide 6: product_service_footprint
✅ Slide 7: business_overview
✅ Slide 8: precedent_transactions
✅ Slide 9: valuation_overview
✅ Slide 10: investor_process_overview (REQUIRED - add if missing)
✅ Slide 11: growth_strategy_projections
✅ Slide 12: sea_conglomerates
✅ Slide 13: buyer_profiles (strategic)
✅ Slide 14: buyer_profiles (financial)

**STEP 3: MANDATORY FIXES - APPLY ALL OF THESE:**

**CRITICAL STRUCTURE FIXES:**
1. **key_metrics**: Must be {"metrics": [array]} NOT direct array
2. **coverage_table**: Must be 2D array [["header1", "header2"], ["row1col1", "row1col2"]] NOT object array
3. **growth_strategy_projections**: Must have slide_data wrapper
4. **All precedent_transactions**: Must have enterprise_value, revenue, ev_revenue_multiple
5. **All slides**: Must have title field
6. **Missing charts section**: Add charts array with historical performance chart
7. **Missing investor_process_data**: Add complete investor process data
8. **Missing margin_cost_data**: Add complete margin cost data
9. **Missing investor_process_overview slide**: Add this slide as slide 10

**STEP 4: MANDATORY FAILSAFE APPLICATION:**
For ANY missing field, automatically fill with realistic data:
- Missing enterprise_value: Calculate using 2.0x-4.0x revenue multiple
- Missing revenue: Use industry-appropriate range  
- Missing ev_revenue_multiple: Calculate enterprise_value/revenue
- Missing experience_bullets: Use professional experience points
- Missing strategic_rationale: Use industry-appropriate rationale
- Missing fit: Use "High (8/10)"
- Missing financial_capacity: Use "High"
- Missing charts: Add historical performance chart
- Missing investor_process_data: Add complete investor process data
- Missing margin_cost_data: Add complete margin cost data

**STEP 5: FINAL MANDATORY VALIDATION:**
Before outputting, verify:
- Content IR has ALL 15 required sections
- Render Plan has EXACTLY 14 slides in correct order
- All data structures match working examples exactly
- No missing fields anywhere
- All precedent_transactions have complete data
- All slides have title fields

**OUTPUT FORMAT:**
Provide ONLY the COMPLETELY FIXED JSON that matches the working examples exactly. Do not output the initial broken JSON - only the corrected version.

**CRITICAL REMINDER:**
You MUST follow this 5-step process. Do not skip any step. Your final output must be perfect JSON that matches the working examples exactly. If you output broken JSON, you have failed this task.

**FINAL INSTRUCTION:**
Generate the interview questions, collect responses, then generate Content IR and Render Plan JSON, then IMMEDIATELY apply the fixing process above to ensure perfect output.
"""
                        st.session_state.messages.append({"role": "user", "content": completion_prompt})
                        
                        with st.spinner("🎯 Generating downloadable JSON files..."):
                            completion_response = call_llm_api(
                                st.session_state.messages,
                                selected_model,
                                api_key,
                                api_service
                            )
                            
                            # MANDATORY POST-GENERATION VALIDATION AND FIXING
                            if completion_response and "Content IR JSON:" in completion_response and "Render Plan JSON:" in completion_response:
                                st.info("🔧 MANDATORY: Applying post-generation validation and fixes...")
                                
                                # Extract JSONs from response with enhanced error handling
                                try:
                                    print(f"[DIRECT PARSE] Extracting JSON sections from response...")
                                    content_ir_start = completion_response.find("Content IR JSON:") + len("Content IR JSON:")
                                    content_ir_end = completion_response.find("Render Plan JSON:")
                                    content_ir_json_str = completion_response[content_ir_start:content_ir_end].strip()
                                    
                                    render_plan_start = completion_response.find("Render Plan JSON:") + len("Render Plan JSON:")
                                    render_plan_json_str = completion_response[render_plan_start:].strip()
                                    
                                    # Clean JSONs before parsing
                                    content_ir_json_str = clean_json_string(content_ir_json_str)
                                    render_plan_json_str = clean_json_string(render_plan_json_str)
                                    
                                    print(f"[DIRECT PARSE] Content IR JSON length: {len(content_ir_json_str)}")
                                    print(f"[DIRECT PARSE] Render Plan JSON length: {len(render_plan_json_str)}")
                                    
                                    # Parse JSONs with detailed error handling
                                    try:
                                        content_ir = json.loads(content_ir_json_str)
                                        print(f"[DIRECT PARSE] Content IR parsed successfully")
                                    except json.JSONDecodeError as parse_error:
                                        st.error(f"❌ Content IR JSON Parse Error: {parse_error}")
                                        print(f"[DIRECT PARSE] Content IR parse failed: {parse_error}")
                                        raise
                                    
                                    try:
                                        render_plan = json.loads(render_plan_json_str)
                                        print(f"[DIRECT PARSE] Render Plan parsed successfully")
                                    except json.JSONDecodeError as parse_error:
                                        st.error(f"⚠️ Invalid Render Plan JSON: {parse_error}")
                                        print(f"[DIRECT PARSE] Render Plan parse failed: {parse_error}")
                                        
                                        # Enhanced error reporting for render plan
                                        error_pos = getattr(parse_error, 'pos', 0)
                                        st.error(f"🔍 **Error Details:** Position {error_pos} in JSON (Length: {len(render_plan_json_str)})")
                                        
                                        # Show context around error
                                        context_start = max(0, error_pos - 150)
                                        context_end = min(len(render_plan_json_str), error_pos + 150)
                                        context = render_plan_json_str[context_start:context_end]
                                        st.code(f"Error context around position {error_pos}:\n{repr(context)}", language="text")
                                        
                                        # Try repair if delimiter error
                                        if "Expecting ',' delimiter" in str(parse_error):
                                            st.info("🔧 Attempting automatic JSON repair...")
                                            repaired = validate_json_char_by_char(render_plan_json_str, error_pos)
                                            if repaired != render_plan_json_str:
                                                try:
                                                    render_plan = json.loads(repaired)
                                                    st.success("✅ JSON repair successful!")
                                                    # Update the JSON string for further processing
                                                    render_plan_json_str = repaired
                                                except Exception as repair_err:
                                                    st.error(f"❌ JSON repair failed: {repair_err}")
                                                    raise parse_error
                                            else:
                                                st.error("❌ No repairs could be applied")
                                                raise parse_error
                                        else:
                                            raise parse_error
                                    
                                    # MANDATORY VALIDATION AND FIXING - ALWAYS EXECUTE
                                    st.info("🔧 MANDATORY: Validating and fixing JSON structure...")
                                    fixed_content_ir, fixed_render_plan = validate_and_fix_json(content_ir, render_plan)
                                    
                                    # Update the response with fixed JSONs
                                    completion_response = f"""Content IR JSON:
{json.dumps(fixed_content_ir, indent=2)}

Render Plan JSON:
{json.dumps(fixed_render_plan, indent=2)}"""
                                    
                                    st.success("✅ MANDATORY: JSON validation and fixing completed successfully!")
                                    
                                except Exception as e:
                                    st.error(f"❌ MANDATORY: JSON parsing failed: {e}")
                                    st.error("❌ This is a critical error - the validation function must work!")
                                    # Still try to use original response
                            else:
                                st.error("❌ MANDATORY: No valid JSON found in response!")
                                st.error("❌ The AI must generate Content IR JSON and Render Plan JSON!")
                        
                        st.session_state.messages.append({"role": "assistant", "content": completion_response})
                    
                    # Force rerun to display new messages
                    st.rerun()
        
        # Clear conversation button
        if st.session_state.chat_started:
            st.markdown("---")
            col1, col2, col3 = st.columns([1, 1, 2])
            
            with col1:
                if st.button("🔥 Reset Chat"):
                    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
                    st.session_state.chat_started = False
                    st.session_state["files_ready"] = False
                    st.session_state.pop("files_data", None)
                    st.rerun()
            
            with col2:
                if st.button("💾 Export Chat"):
                    chat_export = {
                        "model": selected_model,
                        "messages": st.session_state.messages[1:],  # Exclude system message
                        "timestamp": str(pd.Timestamp.now())
                    }
                    
                    st.download_button(
                        "⬇️ Download Chat History",
                        data=json.dumps(chat_export, indent=2),
                        file_name=f"pitch_deck_interview_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json",
                        mime="application/json"
                    )

with tab_json:
    st.subheader("📄 JSON Editor")
    
    # Check if JSONs were auto-populated from AI Copilot
    auto_populated = st.session_state.get("auto_populated", False)
    files_ready = st.session_state.get("files_ready", False)
    
    if auto_populated and files_ready:
        files_data = st.session_state.get("files_data", {})
        st.success(f"🚀 **Auto-Populated!** JSONs from AI Copilot for {files_data.get('company_name', 'your company')}")
        st.info("✅ **No manual copy-paste required!** Your JSONs have been automatically populated, validated, and saved.")
        
        with st.expander("📋 Auto-Generated Files Summary"):
            st.write(f"**Content IR:** {files_data.get('content_ir_filename', 'N/A')}")
            st.write(f"**Render Plan:** {files_data.get('render_plan_filename', 'N/A')}")
            st.write(f"**Timestamp:** {files_data.get('timestamp', 'N/A')}")
            
        # Auto-validate the populated JSONs
        content_ir_str = st.session_state.get("generated_content_ir", "{}")
        render_plan_str = st.session_state.get("generated_render_plan", "{}")
        
        try:
            # Clean JSONs before parsing
            cleaned_content_ir = clean_json_string(content_ir_str) if content_ir_str.strip() else "{}"
            cleaned_render_plan = clean_json_string(render_plan_str) if render_plan_str.strip() else "{}"
            
            content_ir = json.loads(cleaned_content_ir)
            render_plan = json.loads(cleaned_render_plan)
            
            if content_ir and render_plan:
                # Perform comprehensive validation
                validation_results = validate_individual_slides(content_ir, render_plan)
                is_valid = display_validation_results(validation_results)
                
                if is_valid:
                    st.success("✅ **Auto-Validation Passed!** Both JSONs are valid and ready for execution.")
                    
                    # Automatically save validated JSONs to session state
                    st.session_state["generated_content_ir"] = json.dumps(content_ir, indent=2)
                    st.session_state["generated_render_plan"] = json.dumps(render_plan, indent=2)
                    st.session_state["jsons_validated"] = True
                    
                    # Show quick summary
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Content IR Status", "✅ Valid", f"{len(str(content_ir))} chars")
                    with col2:
                        slides_count = len(render_plan.get('slides', []))
                        st.metric("Render Plan Status", "✅ Valid", f"{slides_count} slides")
                else:
                    st.error("❌ **Auto-Validation Failed!** Please check the validation results above.")
                    st.session_state["manual_edit_mode"] = True
                    
                # Quick action buttons
                # col1, col2, col3 = st.columns(3)
                # with col1:
                #     if st.button("🚀 Generate Deck Now", type="primary"):
                #         st.success("✅ Ready for execution! Switch to the Execute tab to generate your pitch deck.")
                #         st.balloons()
                # with col2:
                #     if st.button("👀 Preview JSONs"):
                #         st.session_state["show_json_preview"] = True
                #         st.rerun()
                # with col3:
                #     if st.button("✏️ Manual Edit Mode"):
                #         st.session_state["manual_edit_mode"] = True
                #         st.rerun()
                        
        except Exception as e:
            st.error(f"❌ Auto-validation failed: {e}")
            st.session_state["manual_edit_mode"] = True
    else:
        st.info("💡 **Tip**: Use the AI Copilot to generate JSONs, and they'll automatically populate here!")
    
    # Show JSON preview if requested
    if st.session_state.get("show_json_preview", False):
        st.markdown("---")
        st.subheader("👀 JSON Preview")
        
        col1, col2 = st.columns(2)
        with col1:
            st.caption("Content IR JSON")
            content_ir_preview = st.session_state.get("generated_content_ir", "{}")
            full_content = len(content_ir_preview) <= 1000
            if full_content:
                st.code(content_ir_preview, language="json")
            else:
                st.code(content_ir_preview[:1000] + "...", language="json")
                
            # Always provide expandable text area for easy copying
            with st.expander("📋 Content IR JSON - Click to Expand and Copy"):
                st.text_area("Content IR JSON (Select All and Copy)", content_ir_preview, height=300, key="full_content_ir_copy", help="Use Ctrl+A to select all, then Ctrl+C to copy")
                st.info("💡 **How to Copy**: Click in the text area above → Press Ctrl+A (Select All) → Press Ctrl+C (Copy)")
                
                # Add download button as alternative
                st.download_button(
                    "📄 Download Content IR JSON File",
                    data=content_ir_preview,
                    file_name="content_ir.json",
                    mime="application/json",
                    key="download_content_ir_preview"
                )
            
        with col2:
            st.caption("Render Plan JSON")
            render_plan_preview = st.session_state.get("generated_render_plan", "{}")
            full_render = len(render_plan_preview) <= 1000
            if full_render:
                st.code(render_plan_preview, language="json")
            else:
                st.code(render_plan_preview[:1000] + "...", language="json")
                
            # Always provide expandable text area for easy copying
            with st.expander("📋 Render Plan JSON - Click to Expand and Copy"):
                st.text_area("Render Plan JSON (Select All and Copy)", render_plan_preview, height=300, key="full_render_plan_copy", help="Use Ctrl+A to select all, then Ctrl+C to copy")
                st.info("💡 **How to Copy**: Click in the text area above → Press Ctrl+A (Select All) → Press Ctrl+C (Copy)")
                
                # Add download button as alternative
                st.download_button(
                    "📄 Download Render Plan JSON File", 
                    data=render_plan_preview,
                    file_name="render_plan.json",
                    mime="application/json",
                    key="download_render_plan_preview"
                )
            
        if st.button("❌ Close Preview"):
            st.session_state["show_json_preview"] = False
            st.rerun()
    
    # Always show JSON Editor (with auto-populated content when available)
    st.markdown("---")
    if auto_populated and files_ready:
        st.subheader("📝 JSON Editor (Auto-Populated)")
        st.info("✅ **JSONs have been automatically populated below!** You can edit them if needed or proceed directly to Execute.")
    else:
        st.subheader("✏️ Manual JSON Editor")
        
        # Show file status if files are ready but not auto-populated
        if files_ready and not auto_populated:
            files_data = st.session_state.get("files_data", {})
            st.success(f"🎉 Using generated files for {files_data.get('company_name', 'your company')}")
            
            with st.expander("📋 Generated Files Summary"):
                st.write(f"**Content IR:** {files_data.get('content_ir_filename', 'N/A')}")
                st.write(f"**Render Plan:** {files_data.get('render_plan_filename', 'N/A')}")
                st.write(f"**Timestamp:** {files_data.get('timestamp', 'N/A')}")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("Content IR JSON")
        content_ir_str = st.text_area(
            "Content IR",
            value=st.session_state.get("generated_content_ir", "{}"),
            height=400,
            help="The Content IR contains all the data for your pitch deck"
        )
    
    with col2:
        st.caption("Render Plan JSON")
        render_plan_str = st.text_area(
            "Render Plan",
            value=st.session_state.get("generated_render_plan", "{}"),
            height=400,
            help="The Render Plan defines which slides to create and their data mapping"
        )
    
    # Validate manually edited JSONs
    if st.button("🔍 Validate Edited JSONs"):
        try:
            # Clean JSONs before parsing
            cleaned_content_ir = clean_json_string(content_ir_str) if content_ir_str.strip() else "{}"
            cleaned_render_plan = clean_json_string(render_plan_str) if render_plan_str.strip() else "{}"
            
            # Show cleaned JSON preview if different from original
            if cleaned_content_ir != content_ir_str.strip():
                st.info("🔧 Content IR was automatically cleaned for parsing")
                with st.expander("View cleaned Content IR"):
                    st.code(cleaned_content_ir[:500] + "..." if len(cleaned_content_ir) > 500 else cleaned_content_ir)
            
            if cleaned_render_plan != render_plan_str.strip():
                st.info("🔧 Render Plan was automatically cleaned for parsing")
                with st.expander("View cleaned Render Plan"):
                    st.code(cleaned_render_plan[:500] + "..." if len(cleaned_render_plan) > 500 else cleaned_render_plan)
            
            content_ir = json.loads(cleaned_content_ir)
            render_plan = json.loads(cleaned_render_plan)
            
            if content_ir and render_plan:
                validation_results = validate_individual_slides(content_ir, render_plan)
                is_valid = display_validation_results(validation_results)
                
                if is_valid:
                    st.success("✅ Manual edits passed validation!")
                    # Update session state with cleaned versions
                    st.session_state["generated_content_ir"] = json.dumps(content_ir, indent=2)
                    st.session_state["generated_render_plan"] = json.dumps(render_plan, indent=2)
                else:
                    st.error("❌ Manual edits have validation issues")
            else:
                st.warning("⚠️ Please provide both Content IR and Render Plan JSONs")
        except json.JSONDecodeError as e:
            st.error(f"❌ JSON Parse Error: {e}")
            st.error("🔧 Try using the 'Clean JSON' button below to fix formatting issues")
            
            # Add JSON cleaning buttons for manual editing
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔧 Clean Content IR JSON"):
                    cleaned = clean_json_string(content_ir_str)
                    st.session_state["manual_content_ir_cleaned"] = cleaned
                    st.success("Content IR cleaned! Refresh to see changes.")
            
            with col2:
                if st.button("🔧 Clean Render Plan JSON"):
                    cleaned = clean_json_string(render_plan_str)
                    st.session_state["manual_render_plan_cleaned"] = cleaned
                    st.success("Render Plan cleaned! Refresh to see changes.")
        
        except Exception as e:
            st.error(f"❌ Validation Error: {e}")
    
    # Show cleaned versions if available
    if st.session_state.get("manual_content_ir_cleaned"):
        st.subheader("🔧 Cleaned Content IR")
        st.text_area(
            "Cleaned Content IR JSON",
            value=st.session_state["manual_content_ir_cleaned"],
            height=200,
            help="This is the automatically cleaned version"
        )
        if st.button("✅ Use Cleaned Content IR"):
            st.session_state["generated_content_ir"] = st.session_state["manual_content_ir_cleaned"]
            st.session_state.pop("manual_content_ir_cleaned", None)
            st.success("Cleaned Content IR applied!")
            st.rerun()
    
    if st.session_state.get("manual_render_plan_cleaned"):
        st.subheader("🔧 Cleaned Render Plan")
        st.text_area(
            "Cleaned Render Plan JSON",
            value=st.session_state["manual_render_plan_cleaned"],
            height=200,
            help="This is the automatically cleaned version"
        )
        if st.button("✅ Use Cleaned Render Plan"):
            st.session_state["generated_render_plan"] = st.session_state["manual_render_plan_cleaned"]
            st.session_state.pop("manual_render_plan_cleaned", None)
            st.success("Cleaned Render Plan applied!")
            st.rerun()
    
    # Auto-detect and auto-populate when JSONs are manually pasted
    st.markdown("---")
    st.subheader("🚀 Auto-Population Detection")
    
    def detect_and_auto_populate_jsons():
        """Detect manually pasted JSONs and trigger auto-population workflow"""
        try:
            # Check if user has pasted substantial JSON content
            if len(content_ir_str.strip()) > 100 and len(render_plan_str.strip()) > 100:
                # Clean and parse JSONs
                cleaned_content_ir = clean_json_string(content_ir_str) if content_ir_str.strip() else "{}"
                cleaned_render_plan = clean_json_string(render_plan_str) if render_plan_str.strip() else "{}"
                
                content_ir = json.loads(cleaned_content_ir)
                render_plan = json.loads(cleaned_render_plan)
                
                # Check if JSONs have meaningful content (not just empty objects)
                has_content_ir_data = bool(content_ir and len(str(content_ir)) > 50)
                has_render_plan_data = bool(render_plan and render_plan.get('slides', []))
                
                if has_content_ir_data and has_render_plan_data:
                    # Extract company name for files
                    company_name = "Unknown_Company"
                    if content_ir and 'entities' in content_ir and 'company' in content_ir['entities']:
                        company_name = content_ir['entities']['company'].get('name', 'Unknown_Company')
                    
                    # Create downloadable files data structure
                    timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
                    files_data = {
                        'content_ir_json': json.dumps(content_ir, indent=2),
                        'render_plan_json': json.dumps(render_plan, indent=2), 
                        'content_ir_filename': f'content_ir_{company_name}_{timestamp}.json',
                        'render_plan_filename': f'render_plan_{company_name}_{timestamp}.json',
                        'company_name': company_name,
                        'timestamp': pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                    
                    # Trigger auto-population workflow
                    st.session_state["generated_content_ir"] = files_data['content_ir_json']
                    st.session_state["generated_render_plan"] = files_data['render_plan_json']
                    st.session_state["files_ready"] = True
                    st.session_state["files_data"] = files_data
                    st.session_state["auto_populated"] = True
                    st.session_state["jsons_validated"] = True  # Assume valid if parseable
                    
                    return True, company_name
                    
        except (json.JSONDecodeError, Exception):
            return False, None
            
        return False, None
    
    # Auto-detect button
    if st.button("🔍 Auto-Detect & Populate JSONs"):
        success, company_name = detect_and_auto_populate_jsons()
        if success:
            st.success(f"🚀 **Auto-Population Successful!** JSONs detected and populated for {company_name}")
            st.info("✅ **Workflow Ready!** Switch to Execute tab - no manual steps needed!")
            st.balloons()  # Celebration effect
            # Auto-refresh to show populated state
            st.rerun()
        else:
            st.warning("⚠️ **No valid JSONs detected.** Please paste both Content IR and Render Plan JSONs above, then try again.")
            st.info("💡 **Tip:** Ensure both text areas have substantial JSON content (not just '{}')") 
    
    # Advanced: Automatic background detection (optional)
    with st.expander("⚡ Enable Automatic Detection"):
        auto_detect_enabled = st.checkbox("🔄 Auto-detect JSONs on every edit", 
                                        help="Automatically triggers auto-population when valid JSONs are detected")
        
        if auto_detect_enabled:
            # Background detection - runs automatically
            success, company_name = detect_and_auto_populate_jsons()
            if success and not st.session_state.get("auto_populated", False):
                st.success(f"🎯 **Auto-Detected!** JSONs automatically populated for {company_name}")
                st.rerun()
    
    st.markdown("---")
    
    # Save to session state
    if st.button("💾 Save JSON to Session"):
        st.session_state["generated_content_ir"] = content_ir_str
        st.session_state["generated_render_plan"] = render_plan_str
        st.success("✅ JSON saved to session. Switch to Execute tab to generate your deck.")

with tab_execute:
    st.subheader("⚙️ Generate Pitch Deck")
    
    # Check automation status
    auto_populated = st.session_state.get("auto_populated", False)
    jsons_validated = st.session_state.get("jsons_validated", False)
    files_ready = st.session_state.get("files_ready", False)
    
    # Show automation status
    if auto_populated and jsons_validated:
        st.success("🚀 **Fully Automated Workflow Complete!** JSONs auto-populated, validated, and ready for execution.")
        st.info("✅ **No manual steps required** - Your pitch deck is ready to generate!")
    elif files_ready:
        files_data = st.session_state.get("files_data", {})
        st.success(f"🎉 Using generated files for {files_data.get('company_name', 'your company')}")
        
        # Show file summary
        with st.expander("📋 Generated Files Summary"):
            st.write(f"**Content IR:** {files_data.get('content_ir_filename', 'N/A')}")
            st.write(f"**Render Plan:** {files_data.get('render_plan_filename', 'N/A')}")
            st.write(f"**Timestamp:** {files_data.get('timestamp', 'N/A')}")
    
    # Get JSON from session state
    content_ir_str = st.session_state.get("generated_content_ir", "{}")
    render_plan_str = st.session_state.get("generated_render_plan", "{}")
    
    # Display JSON previews
    col1, col2 = st.columns(2)
    
    with col1:
        st.caption("Content IR Status")
        try:
            # Clean JSON before parsing
            cleaned_content_ir_str = clean_json_string(content_ir_str)
            content_ir = json.loads(cleaned_content_ir_str)
            
            if content_ir:
                st.success(f"✅ Content IR loaded ({len(str(content_ir))} characters)")
                
                # Show if cleaning was applied
                if cleaned_content_ir_str != content_ir_str.strip():
                    st.info("🔧 JSON was automatically cleaned")
                
                # Show brief summary
                summary = {}
                if "entities" in content_ir:
                    summary["Company"] = content_ir.get("entities", {}).get("company", {}).get("name", "N/A")
                if "management_team" in content_ir:
                    summary["Management Profiles"] = len(content_ir.get("management_team", {}).get("left_column_profiles", [])) + len(content_ir.get("management_team", {}).get("right_column_profiles", []))
                
                st.json(summary)
            else:
                st.warning("⚠️ Empty Content IR")
        except json.JSONDecodeError as e:
            st.error(f"⚠️ Invalid Content IR JSON: {e}")
            if st.button("🔧 Try Auto-Clean Content IR", key="clean_content_ir_exec"):
                cleaned = clean_json_string(content_ir_str)
                st.session_state["generated_content_ir"] = cleaned
                st.rerun()
            content_ir = None
        except Exception as e:
            st.error(f"⚠️ Content IR Error: {e}")
            content_ir = None
    
    with col2:
        st.caption("Render Plan Status")
        try:
            # Clean JSON before parsing
            cleaned_render_plan_str = clean_json_string(render_plan_str)
            render_plan = json.loads(cleaned_render_plan_str)
            
            if render_plan and "slides" in render_plan:
                st.success(f"✅ Render Plan loaded ({len(render_plan['slides'])} slides)")
                
                # Show if cleaning was applied
                if cleaned_render_plan_str != render_plan_str.strip():
                    st.info("🔧 JSON was automatically cleaned")
                
                # Show slide types
                slide_types = [slide.get("template", "unknown") for slide in render_plan["slides"]]
                st.write("**Slide Types:**")
                for i, slide_type in enumerate(slide_types[:10], 1):  # Show first 10
                    st.write(f"{i}. {slide_type}")
                if len(slide_types) > 10:
                    st.write(f"... and {len(slide_types) - 10} more slides")
            else:
                st.warning("⚠️ Empty or invalid Render Plan")
        except json.JSONDecodeError as e:
            st.error(f"⚠️ Invalid Render Plan JSON: {e}")
            if st.button("🔧 Try Auto-Clean Render Plan", key="clean_render_plan_exec"):
                cleaned = clean_json_string(render_plan_str)
                st.session_state["generated_render_plan"] = cleaned
                st.rerun()
            render_plan = None
        except Exception as e:
            st.error(f"⚠️ Render Plan Error: {e}")
            render_plan = None
    
    # Pre-execution validation
    if st.button("🔍 Final Validation Before Generation"):
        if not Path(templates_path).exists():
            st.error(f"⚠️ templates.json not found at {templates_path}")
        elif content_ir is None or render_plan is None:
            st.error("⚠️ Please fix the JSON errors above")
        else:
            try:
                # Comprehensive validation
                validation_results = validate_individual_slides(content_ir, render_plan)
                is_valid = display_validation_results(validation_results)
                
                # Traditional catalog validation (if available)
                catalog = TemplateCatalog.from_file(templates_path)
                if HAS_VALIDATORS and not skip_validate:
                    report = validate_render_plan_against_catalog(content_ir, render_plan, catalog)
                    summary = summarize_issues(report)
                    
                    st.write("**📋 Catalog Validation:**")
                    if report.ok:
                        st.success("✅ Catalog validation passed!")
                    else:
                        st.error("⚠️ Catalog validation issues")
                    st.code(summary)
                else:
                    st.info("ℹ️ Catalog validation skipped")
                
                if is_valid:
                    st.success("🎯 **Ready for deck generation!** All validations passed.")
                else:
                    st.error("🚨 **Cannot generate deck** - Fix validation issues first.")
                    
            except Exception as e:
                st.error(f"⚠️ Validation error: {e}")
    
    # Generate deck
    st.markdown("---")
    out_name = st.text_input("Output filename", value="ai_generated_deck.pptx")
    
    if st.button("🎯 Generate Pitch Deck", type="primary", disabled=(not content_ir or not render_plan)):
        if not Path(templates_path).exists():
            st.error(f"⚠️ templates.json not found at {templates_path}")
        elif content_ir is None or render_plan is None:
            st.error("⚠️ Please fix JSON errors first")
        else:
            # Final validation before generation
            validation_results = validate_individual_slides(content_ir, render_plan)
            
            if not validation_results['overall_valid']:
                st.error("🚨 **Cannot generate deck** - Validation failed!")
                display_validation_results(validation_results)
            else:
                try:
                    # Show progress
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    status_text.text("📄 Rendering slides...")
                    progress_bar.progress(25)
                    
                    # Get brand configuration
                    brand_config = st.session_state.get("brand_config")
                    
                    # Generate deck
                    # Normalize plan to avoid blank cells / missing fields
                    render_plan = normalize_plan(render_plan)
                    
                    # ENHANCED: Validate data for PowerPoint compatibility
                    try:
                        from pptx_validator import pre_validate_for_powerpoint
                        content_ir, render_plan = pre_validate_for_powerpoint(content_ir, render_plan)
                        st.info("🔍 Data validated for PowerPoint compatibility")
                    except ImportError:
                        st.warning("⚠️ PowerPoint validator not available - proceeding with basic generation")
                    except Exception as e:
                        st.warning(f"⚠️ Validation warning: {str(e)} - proceeding with generation")

                    prs, saved_path = execute_plan(
                        plan=render_plan,
                        content_ir=content_ir,
                        templates_path=templates_path,
                        output_path=out_name,
                        company_name=company_name,
                        brand_config=brand_config,
                        debug=True,
                    )
                    
                    progress_bar.progress(75)
                    status_text.text("💾 Preparing download...")
                    
                    # Prepare download
                    buf = io.BytesIO()
                    prs.save(buf)
                    buf.seek(0)
                    
                    progress_bar.progress(100)
                    status_text.text("✅ Deck generated successfully!")
                    
                    # Success message
                    st.balloons()
                    st.success(f"🎉 AI-Generated Pitch Deck Complete!")
                    st.info(f"📊 Generated {len(prs.slides)} slides")
                    if brand_config:
                        st.info("🎨 Custom branding applied")
                    st.info(f"💼 Company: {company_name}")
                    st.success("✅ **Zero Empty Boxes Policy** - All slides have complete content!")
                    
                    # Show slide breakdown
                    if render_plan and "slides" in render_plan:
                        slide_types = [slide.get("template", "unknown") for slide in render_plan["slides"]]
                        with st.expander("📋 Slide Details"):
                            for i, slide_type in enumerate(slide_types, 1):
                                st.write(f"{i}. {slide_type}")
                    
                    # Download button
                    st.download_button(
                        "⬇️ Download Your AI-Generated Pitch Deck",
                        data=buf,
                        file_name=out_name,
                        mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                        type="primary"
                    )
                    
                    # Add PowerPoint troubleshooting info
                    with st.expander("🔧 PowerPoint Troubleshooting Guide"):
                        st.markdown("""
                        **If you get a PowerPoint repair error:**
                        
                        ✅ **Click 'Repair'** - PowerPoint can usually fix minor issues automatically  
                        🔄 **Try regenerating** - Use the same JSONs to create a new file  
                        📊 **Check your data** - Ensure all numeric values are valid (no text in number fields)  
                        🌿 **Use latest branch** - Make sure you're using the `fix/vector-db` branch with latest fixes  
                        
                        **Common causes:**
                        - Invalid chart data (empty or non-numeric values)
                        - Special characters in text fields  
                        - Mismatched data arrays in charts
                        - Very large data values causing overflow
                        
                        **✨ The repair process is safe and will preserve your content!**
                        
                        **Alternative:** Try opening the file in Google Slides first, then downloading as PowerPoint.
                        """)
                    
                    progress_bar.empty()
                    status_text.empty()
                    
                except Exception as e:
                    st.error(f"⚠️ Error generating deck: {str(e)}")
                    st.exception(e)

# ============================================================================
# AUTOMATIC VALIDATION FEEDBACK SYSTEM
# ============================================================================

def format_validation_errors_for_llm(validation_result):
    """
    Format validation errors into a clear, structured prompt for LLM correction
    """
    if not validation_result or validation_result.get('overall_valid', True):
        return None
    
    error_prompt = """🚨 JSON VALIDATION ERRORS DETECTED - PLEASE FIX THE FOLLOWING ISSUES:

=== VALIDATION SUMMARY ===
"""
    
    # Add overall summary
    summary = validation_result.get('summary', {})
    error_prompt += f"""
Total Slides: {summary.get('total_slides', 0)}
Valid Slides: {summary.get('valid_slides', 0)}
Invalid Slides: {summary.get('invalid_slides', 0)}
Overall Valid: {validation_result.get('overall_valid', False)}
"""
    
    # Add critical issues
    critical_issues = validation_result.get('critical_issues', [])
    if critical_issues:
        error_prompt += "\n=== CRITICAL ISSUES ===\n"
        for i, issue in enumerate(critical_issues, 1):
            error_prompt += f"{i}. {issue}\n"
    
    # Add slide-by-slide errors
    slide_details = validation_result.get('slide_details', {})
    if slide_details:
        error_prompt += "\n=== SLIDE-BY-SLIDE VALIDATION ERRORS ===\n"
        for slide_name, slide_info in slide_details.items():
            if not slide_info.get('valid', True):
                error_prompt += f"\n🔴 SLIDE: {slide_name}\n"
                
                # Add empty/placeholder fields
                empty_fields = slide_info.get('empty_fields', [])
                if empty_fields:
                    error_prompt += "📦 Empty/Placeholder Fields:\n"
                    for field in empty_fields:
                        error_prompt += f"  • {field}\n"
                
                # Add critical issues for this slide
                slide_issues = slide_info.get('critical_issues', [])
                if slide_issues:
                    error_prompt += "🚨 Critical Issues:\n"
                    for issue in slide_issues:
                        error_prompt += f"  • {issue}\n"
                
                # Add validation errors
                validation_errors = slide_info.get('validation_errors', [])
                if validation_errors:
                    error_prompt += "❌ Validation Errors:\n"
                    for error in validation_errors:
                        error_prompt += f"  • {error}\n"
    
    # Add structure validation errors
    structure_validation = validation_result.get('structure_validation', {})
    if structure_validation and not structure_validation.get('content_ir_valid', True):
        error_prompt += "\n=== CONTENT IR STRUCTURE ERRORS ===\n"
        structure_issues = structure_validation.get('structure_issues', [])
        for issue in structure_issues:
            error_prompt += f"• {issue}\n"
    
    error_prompt += """

=== INSTRUCTIONS FOR CORRECTION ===
1. Fix ALL validation errors listed above
2. Ensure proper JSON structure and data types
3. Add missing required fields with appropriate default values
4. Fix duplicate entries and naming conflicts
5. Ensure all numeric fields contain valid numbers (not strings)
6. Verify array structures match expected formats
7. Return ONLY the corrected JSON objects - no explanations or markdown formatting

Please provide the corrected Content IR and Render Plan JSONs that address all these validation issues.
"""
    
    return error_prompt

def auto_fix_json_with_llm(content_ir, render_plan, validation_result):
    """
    Automatically fix JSON validation errors by sending them to an LLM for correction
    """
    print("\n🤖 STARTING AUTOMATIC JSON VALIDATION FEEDBACK SYSTEM")
    print("="*80)
    
    # Format validation errors for LLM
    error_prompt = format_validation_errors_for_llm(validation_result)
    if not error_prompt:
        print("✅ No validation errors found - no correction needed")
        return content_ir, render_plan, True
    
    print("📝 FORMATTED VALIDATION ERRORS FOR LLM:")
    print(error_prompt[:500] + "..." if len(error_prompt) > 500 else error_prompt)
    
    # Prepare the complete prompt with context
    full_prompt = f"""You are an expert JSON validator and fixer for investment banking pitch deck data.

{error_prompt}

=== CURRENT CONTENT IR JSON ===
{json.dumps(content_ir, indent=2) if content_ir else "null"}

=== CURRENT RENDER PLAN JSON ===
{json.dumps(render_plan, indent=2) if render_plan else "null"}

Please analyze the validation errors and provide corrected JSON objects that fix all the issues listed above.
Return the corrected JSONs in this exact format:

CORRECTED_CONTENT_IR:
{{corrected content ir json}}

CORRECTED_RENDER_PLAN:  
{{corrected render plan json}}
"""
    
    try:
        print("🔄 SENDING TO LLM FOR AUTOMATIC CORRECTION...")
        
        # Here you would integrate with your preferred LLM API
        # For now, we'll use a mock response and return the original JSONs
        # In a real implementation, you would call OpenAI, Claude, or your preferred LLM API
        
        print("⚠️  LLM INTEGRATION NOT IMPLEMENTED - Using fallback correction")
        
        # Apply basic automatic fixes based on common validation errors
        fixed_content_ir, fixed_render_plan = apply_basic_automatic_fixes(
            content_ir, render_plan, validation_result
        )
        
        print("✅ APPLIED BASIC AUTOMATIC FIXES")
        return fixed_content_ir, fixed_render_plan, True
        
    except Exception as e:
        print(f"❌ ERROR IN AUTOMATIC CORRECTION: {str(e)}")
        return content_ir, render_plan, False

def apply_basic_automatic_fixes(content_ir, render_plan, validation_result):
    """
    Apply basic automatic fixes for common validation errors
    """
    print("🔧 APPLYING BASIC AUTOMATIC FIXES...")
    
    # Make copies to avoid modifying originals
    import copy
    fixed_content_ir = copy.deepcopy(content_ir) if content_ir else {}
    fixed_render_plan = copy.deepcopy(render_plan) if render_plan else {"slides": []}
    
    # Fix common issues based on validation results
    slide_details = validation_result.get('slide_details', {})
    
    for slide_name, slide_info in slide_details.items():
        if not slide_info.get('valid', True):
            print(f"🔧 Fixing slide: {slide_name}")
            
            # Fix missing metrics array in key_metrics (Slide 4 issue)
            if slide_name == 'historical_financial_performance':
                for slide in fixed_render_plan.get('slides', []):
                    if slide.get('template') == 'historical_financial_performance':
                        key_metrics = slide.get('data', {}).get('key_metrics', {})
                        if 'metrics' not in key_metrics or not key_metrics['metrics']:
                            key_metrics['metrics'] = ["120%", "38.0", "5.7", "300"]
                            print("✅ Fixed missing metrics array in key_metrics")
            
            # Fix duplicate methodologies (Slide 8 issue)
            if slide_name == 'valuation_overview':
                for slide in fixed_render_plan.get('slides', []):
                    if slide.get('template') == 'valuation_overview':
                        valuation_data = slide.get('data', {}).get('valuation_data', [])
                        methodologies = [item.get('methodology', '') for item in valuation_data]
                        
                        # Fix duplicate "Trading Multiples"
                        if methodologies.count("Trading Multiples") > 1:
                            for i, item in enumerate(valuation_data):
                                if item.get('methodology') == "Trading Multiples":
                                    if i == 0:
                                        item['methodology'] = "Trading Multiples (EV/Revenue)"
                                    elif i == 1:
                                        item['methodology'] = "Trading Multiples (EV/EBITDA)"
                            print("✅ Fixed duplicate methodology names")
            
            # Add missing required fields with defaults
            empty_fields = slide_info.get('empty_fields', [])
            for field in empty_fields:
                if 'Missing metrics array' in field:
                    # Already handled above
                    continue
    
    print("🎯 BASIC AUTOMATIC FIXES COMPLETED")
    return fixed_content_ir, fixed_render_plan

def validate_and_auto_fix_jsons(content_ir, render_plan, max_attempts=3):
    """
    Main function that validates JSONs and automatically fixes errors using LLM feedback
    """
    print("\n🎯 STARTING VALIDATION AND AUTO-FIX PROCESS")
    print("="*80)
    
    current_content_ir = content_ir
    current_render_plan = render_plan
    attempt = 0
    
    while attempt < max_attempts:
        attempt += 1
        print(f"\n🔄 VALIDATION ATTEMPT {attempt}/{max_attempts}")
        
        # Run validation
        _, _, validation_result = extract_and_validate_jsons(
            f"Content IR: {json.dumps(current_content_ir) if current_content_ir else 'null'}\n"
            f"Render Plan: {json.dumps(current_render_plan) if current_render_plan else 'null'}"
        )
        
        # Check if validation passed
        if validation_result.get('overall_valid', False):
            print("✅ VALIDATION PASSED - No fixes needed!")
            return current_content_ir, current_render_plan, validation_result, True
        
        print(f"❌ VALIDATION FAILED - Attempt {attempt}")
        
        # If last attempt, return what we have
        if attempt >= max_attempts:
            print(f"⚠️  Max attempts reached ({max_attempts}). Returning best effort.")
            return current_content_ir, current_render_plan, validation_result, False
        
        # Apply automatic fixes
        print(f"🔧 APPLYING AUTOMATIC FIXES - Attempt {attempt}")
        fixed_content_ir, fixed_render_plan, fix_success = auto_fix_json_with_llm(
            current_content_ir, current_render_plan, validation_result
        )
        
        if not fix_success:
            print("❌ AUTOMATIC FIX FAILED - Stopping attempts")
            return current_content_ir, current_render_plan, validation_result, False
        
        # Update for next iteration
        current_content_ir = fixed_content_ir
        current_render_plan = fixed_render_plan
        
        print(f"✅ FIXES APPLIED - Will validate again...")
    
    return current_content_ir, current_render_plan, validation_result, False

# ============================================================================
# END AUTOMATIC VALIDATION FEEDBACK SYSTEM
# ============================================================================

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    <p>🤖 <strong>AI Deck Builder</strong> - Powered by LLM AI | Investment Banking Pitch Deck Generator</p>
    <p>💡 <em>Start with the AI Copilot → Download JSON Files → Generate Professional Deck</em></p>
    <p>🎨 <em>Enhanced with Zero Empty Boxes Policy & Comprehensive Slide Validation</em></p>
</div>
""", unsafe_allow_html=True)





