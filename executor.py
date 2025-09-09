"""
executor.py - patched and fixed
Orchestrates reading a plan (or content/content_ir), calls adapters.render_plan_to_pptx,
and optionally saves to disk. Returns both presentation and save path for compatibility.
Now supports brand configuration.
"""
from typing import Any, Dict, Optional, Tuple
from pathlib import Path
try:
    from pptx import Presentation  # type: ignore
except Exception:
    Presentation = None  # type: ignore

import importlib

# Import slide templates directly instead of adapters
from slide_templates import (
    render_business_overview_slide,
    render_historical_financial_performance_slide, 
    render_management_team_slide,
    render_product_service_footprint_slide,
    render_growth_strategy_projections_slide,
    render_competitive_positioning_slide,
    render_precedent_transactions_slide,
    render_valuation_overview_slide,
    render_buyer_profiles_slide,
    render_sea_conglomerates_slide,
    render_margin_cost_resilience_slide,
    render_investor_considerations_slide,
    render_investor_process_overview_slide
)

def _ensure_prs(prs=None):
    """Return a python-pptx Presentation or create a new one."""
    if Presentation is None:
        raise RuntimeError("python-pptx is not installed. Please `pip install python-pptx`.")
    if prs is None or not hasattr(prs, "slides"):
        return Presentation()
    return prs

def render_plan_to_pptx(plan=None, content=None, content_ir=None, prs=None, company_name="Your Company", brand_config=None):
    """
    Simple render function to replace adapters.render_plan_to_pptx
    """
    if prs is None:
        prs = _ensure_prs()
    
    if not plan or 'slides' not in plan:
        print("❌ No plan or slides found")
        return prs
    
    # Map of template names to render functions
    template_map = {
        'business_overview': render_business_overview_slide,
        'historical_financial_performance': render_historical_financial_performance_slide,
        'management_team': render_management_team_slide,
        'product_service_footprint': render_product_service_footprint_slide,
        'growth_strategy_projections': render_growth_strategy_projections_slide,
        'competitive_positioning': render_competitive_positioning_slide,
        'precedent_transactions': render_precedent_transactions_slide,
        'valuation_overview': render_valuation_overview_slide,
        'buyer_profiles': render_buyer_profiles_slide,
        'sea_conglomerates': render_sea_conglomerates_slide,
        'margin_cost_resilience': render_margin_cost_resilience_slide,
        'investor_considerations': render_investor_considerations_slide,
        'investor_process_overview': render_investor_process_overview_slide
    }
    
    # Render each slide
    for slide_config in plan['slides']:
        template = slide_config.get('template')
        if template in template_map:
            try:
                render_func = template_map[template]
                prs = render_func(
                    data=slide_config.get('data'),
                    content_ir=content_ir,
                    prs=prs,
                    company_name=company_name,
                    brand_config=brand_config
                )
                print(f"✅ Rendered {template} slide")
            except Exception as e:
                print(f"❌ Error rendering {template}: {e}")
        else:
            print(f"⚠️ Unknown template: {template}")
    
    return prs

def execute_plan(
    plan: Optional[Dict] = None,
    content: Optional[Any] = None,
    content_ir: Optional[Any] = None,
    prs=None,
    out_path: Optional[str] = None,
    output_path: Optional[str] = None,
    deck_path: Optional[str] = None,
    company_name: str = "Moelis",
    brand_config: Optional[Dict] = None,  # NEW: Brand configuration
    **kwargs,  # Changed from _ignore_kwargs to handle additional parameters
) -> Tuple[Any, str]:
    """
    Build a deck from a plan/content/content_ir and return the pptx.Presentation and save path.
    If out_path/output_path/deck_path is provided, save the deck there.
    Extra kwargs are handled to support various parameter naming conventions.
    
    Args:
        plan: Render plan dictionary
        content: Content data
        content_ir: Content IR data
        prs: Existing presentation object
        out_path/output_path/deck_path: Save path for the presentation
        company_name: Company name for footer
        brand_config: Brand configuration extracted from uploaded deck
    
    Returns:
        Tuple[Presentation, str]: The presentation object and the path where it was saved
    """
    prs_obj = _ensure_prs(prs)

    # Handle alternative parameter names for render plan
    if plan is None and 'render_plan' in kwargs:
        plan = kwargs['render_plan']
        print(f"[DEBUG] Using render_plan parameter as plan")
    
    # Handle alternative parameter names for output file
    output_file = kwargs.get('output_file')
    
    # Determine the save path (try all possible parameter names)
    save_path = out_path or output_path or deck_path or output_file or "deck.pptx"

    prs_out = render_plan_to_pptx(
        plan=plan, 
        content=content, 
        content_ir=content_ir, 
        prs=prs_obj, 
        company_name=company_name,
        brand_config=brand_config
    )

    # Save if path is provided
    if save_path:
        save_path = str(save_path)
        try:
            Path(save_path).parent.mkdir(parents=True, exist_ok=True)
            prs_out.save(save_path)
        except Exception as e:
            # Fallback to current directory if save fails
            fallback_path = "deck.pptx"
            try:
                prs_out.save(fallback_path)
                save_path = fallback_path
            except Exception as e2:
                print(f"Failed to save to both {save_path} and {fallback_path}: {e2}")
                save_path = "failed_to_save.pptx"

    return prs_out, save_path

# Convenience for CLI/manual testing
if __name__ == "__main__":
    import json, sys
    input_json = None
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            input_json = json.load(f)
    else:
        # Minimal demo
        input_json = {"slides": [{"template": "management_team", "data": {"title": "Demo", "left_column_profiles": [], "right_column_profiles": []}}]}
    
    prs, path = execute_plan(plan=input_json, out_path="deck.pptx")
    print(f"Wrote {path}")