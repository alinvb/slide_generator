"""
PowerPoint Validation and Repair Module
Validates data before PowerPoint generation to prevent corruption issues.
"""

import json
import re
from typing import Dict, Any, List, Union
from pathlib import Path

def sanitize_text(text: str) -> str:
    """Sanitize text content to prevent PowerPoint issues"""
    if not isinstance(text, str):
        text = str(text)
    
    # Remove problematic characters
    text = re.sub(r'[^\x00-\x7F\u00A0-\u024F\u1E00-\u1EFF\u2000-\u206F\u20A0-\u20CF\u2100-\u214F]', '', text)
    
    # Replace smart quotes and dashes
    text = text.replace('"', '"').replace('"', '"')
    text = text.replace(''', "'").replace(''', "'")  
    text = text.replace('—', '-').replace('–', '-')
    
    # Limit length to prevent overflow
    if len(text) > 1000:
        text = text[:997] + "..."
    
    return text.strip()

def validate_numeric_data(data: List[Union[int, float, str]]) -> List[float]:
    """Validate and clean numeric data for charts"""
    cleaned_data = []
    
    for item in data:
        try:
            if isinstance(item, str):
                # Remove currency symbols, commas, etc.
                cleaned_item = re.sub(r'[^\d.-]', '', item)
                if cleaned_item:
                    num_val = float(cleaned_item)
                else:
                    num_val = 0.0
            else:
                num_val = float(item)
            
            # Check for invalid numbers
            if num_val != num_val:  # NaN check
                num_val = 0.0
            elif num_val == float('inf') or num_val == float('-inf'):
                num_val = 0.0
            
            cleaned_data.append(num_val)
        except (ValueError, TypeError):
            cleaned_data.append(0.0)
    
    return cleaned_data

def validate_chart_data(chart_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate chart data structure and content"""
    if not isinstance(chart_data, dict):
        return {"categories": ["2020", "2021", "2022"], "values": [0, 0, 0]}
    
    # Validate categories
    categories = chart_data.get('categories', [])
    if not isinstance(categories, list) or len(categories) == 0:
        categories = ["2020", "2021", "2022"]
    else:
        categories = [sanitize_text(str(cat)) for cat in categories[:10]]  # Limit to 10 items
    
    # Validate numeric data series
    validated_chart = {"categories": categories}
    
    for key in ['values', 'revenue', 'ebitda']:
        if key in chart_data:
            values = chart_data[key]
            if isinstance(values, list):
                cleaned_values = validate_numeric_data(values)
                # Ensure same length as categories
                while len(cleaned_values) < len(categories):
                    cleaned_values.append(0.0)
                validated_chart[key] = cleaned_values[:len(categories)]
    
    return validated_chart

def validate_slide_data(slide_data: Dict[str, Any]) -> Dict[str, Any]:
    """Validate individual slide data"""
    if not isinstance(slide_data, dict):
        return {}
    
    validated_data = {}
    
    for key, value in slide_data.items():
        if isinstance(value, str):
            validated_data[key] = sanitize_text(value)
        elif isinstance(value, dict):
            if 'chart' in key.lower() or key in ['chart_data', 'chart_info']:
                validated_data[key] = validate_chart_data(value)
            else:
                validated_data[key] = validate_slide_data(value)
        elif isinstance(value, list):
            if key == 'categories' or 'categories' in str(value):
                validated_data[key] = [sanitize_text(str(item)) for item in value[:10]]
            elif all(isinstance(item, (int, float, str)) and str(item).replace('.', '').replace('-', '').isdigit() for item in value if item is not None):
                validated_data[key] = validate_numeric_data(value)
            else:
                validated_data[key] = [validate_slide_data(item) if isinstance(item, dict) else sanitize_text(str(item)) for item in value]
        else:
            validated_data[key] = value
    
    return validated_data

def validate_render_plan(render_plan: Dict[str, Any]) -> Dict[str, Any]:
    """Validate entire render plan structure"""
    if not isinstance(render_plan, dict) or 'slides' not in render_plan:
        return {"slides": []}
    
    validated_plan = {"slides": []}
    
    for slide in render_plan['slides']:
        if not isinstance(slide, dict):
            continue
        
        validated_slide = {
            "template": sanitize_text(slide.get('template', 'business_overview')),
            "data": validate_slide_data(slide.get('data', {}))
        }
        
        # Add content_ir_key if present
        if 'content_ir_key' in slide:
            validated_slide['content_ir_key'] = sanitize_text(slide['content_ir_key'])
        
        validated_plan['slides'].append(validated_slide)
    
    return validated_plan

def validate_content_ir(content_ir: Dict[str, Any]) -> Dict[str, Any]:
    """Validate Content IR structure"""
    if not isinstance(content_ir, dict):
        return {}
    
    validated_ir = {}
    
    for key, value in content_ir.items():
        if key == 'facts' and isinstance(value, dict):
            # Special handling for financial facts
            validated_facts = {}
            for fact_key, fact_value in value.items():
                if isinstance(fact_value, list) and fact_key in ['revenue_usd_m', 'ebitda_usd_m', 'ebitda_margins']:
                    validated_facts[fact_key] = validate_numeric_data(fact_value)
                else:
                    validated_facts[fact_key] = fact_value
            validated_ir[key] = validated_facts
        else:
            validated_ir[key] = validate_slide_data(value) if isinstance(value, dict) else value
    
    return validated_ir

def pre_validate_for_powerpoint(content_ir: Dict[str, Any], render_plan: Dict[str, Any]) -> tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Main validation function to call before PowerPoint generation
    Returns validated content_ir and render_plan
    """
    print("🔍 Validating data for PowerPoint compatibility...")
    
    try:
        validated_content_ir = validate_content_ir(content_ir)
        validated_render_plan = validate_render_plan(render_plan)
        
        print("✅ PowerPoint validation completed successfully")
        return validated_content_ir, validated_render_plan
    
    except Exception as e:
        print(f"⚠️ Validation error: {e}")
        # Return original data if validation fails
        return content_ir, render_plan

def diagnose_pptx_file(file_path: str) -> Dict[str, Any]:
    """Diagnose potential issues with generated PowerPoint file"""
    diagnosis = {
        "file_exists": False,
        "file_size": 0,
        "is_valid_zip": False,
        "potential_issues": [],
        "recommendations": []
    }
    
    try:
        path = Path(file_path)
        if path.exists():
            diagnosis["file_exists"] = True
            diagnosis["file_size"] = path.stat().st_size
            
            # Check if file is too small (likely corrupted)
            if diagnosis["file_size"] < 10000:  # Less than 10KB
                diagnosis["potential_issues"].append("File size too small - likely corrupted")
                diagnosis["recommendations"].append("Regenerate the presentation")
            
            # Check if it's a valid ZIP (PPTX files are ZIP archives)
            import zipfile
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    diagnosis["is_valid_zip"] = True
                    
                    # Check for required PPTX structure
                    required_files = ['[Content_Types].xml', 'ppt/presentation.xml']
                    missing_files = [f for f in required_files if f not in zip_ref.namelist()]
                    
                    if missing_files:
                        diagnosis["potential_issues"].append(f"Missing required files: {missing_files}")
                        diagnosis["recommendations"].append("Regenerate with data validation")
                        
            except zipfile.BadZipFile:
                diagnosis["potential_issues"].append("File is not a valid ZIP/PPTX structure")
                diagnosis["recommendations"].append("Regenerate the presentation with clean data")
        
        else:
            diagnosis["potential_issues"].append("File does not exist")
            diagnosis["recommendations"].append("Check file generation process")
            
    except Exception as e:
        diagnosis["potential_issues"].append(f"Error during diagnosis: {str(e)}")
    
    return diagnosis