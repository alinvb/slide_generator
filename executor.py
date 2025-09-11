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

# RESTORED: Import proper adapters module for sophisticated slide generation
import adapters


def _ensure_prs(prs=None):
    """Return a python-pptx Presentation or create a new one."""
    if Presentation is None:
        raise RuntimeError("python-pptx is not installed. Please `pip install python-pptx`.")
    if prs is None or not hasattr(prs, "slides"):
        return Presentation()
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
    # 🔍 [EXECUTOR DEBUG] Log all inputs to execute_plan
    print(f"🔍 [EXECUTOR DEBUG] execute_plan called with:")
    print(f"🔍 [EXECUTOR DEBUG] - plan type: {type(plan)}")
    print(f"🔍 [EXECUTOR DEBUG] - content type: {type(content)}")
    print(f"🔍 [EXECUTOR DEBUG] - content_ir type: {type(content_ir)}")
    print(f"🔍 [EXECUTOR DEBUG] - company_name: {company_name}")
    
    if isinstance(plan, dict):
        print(f"🔍 [EXECUTOR DEBUG] - plan keys: {list(plan.keys())}")
        if 'slides' in plan:
            print(f"🔍 [EXECUTOR DEBUG] - plan slides count: {len(plan['slides'])}")
    else:
        print(f"🔍 [EXECUTOR DEBUG] - plan is NOT a dict: {plan}")
        
    if isinstance(content_ir, dict):
        print(f"🔍 [EXECUTOR DEBUG] - content_ir keys: {list(content_ir.keys())}")
    else:
        print(f"🔍 [EXECUTOR DEBUG] - content_ir is NOT a dict: {content_ir}")
    
    prs_obj = _ensure_prs(prs)
    
    # Use the sophisticated adapters.render_plan_to_pptx function
    try:
        print("🎯 RESTORED: Using sophisticated adapters.render_plan_to_pptx")
        prs_obj = adapters.render_plan_to_pptx(
            plan=plan,
            content=content,
            content_ir=content_ir,
            prs=prs_obj,
            company_name=company_name,
            brand_config=brand_config
        )
        print("✅ Successfully used sophisticated adapters rendering")
    except Exception as e:
        print(f"❌ Error using adapters.render_plan_to_pptx: {e}")
        # Fallback to basic rendering if adapters fails
        if plan and 'slides' in plan:
            print("⚠️ Falling back to basic slide rendering")
            # Simple fallback - this should rarely be needed
            import slide_templates
            for slide_config in plan['slides']:
                template = slide_config.get('template')
                try:
                    render_func = getattr(slide_templates, f'render_{template}_slide', None)
                    if render_func:
                        prs_obj = render_func(
                            data=slide_config.get('data'),
                            prs=prs_obj,
                            company_name=company_name
                        )
                        print(f"✅ Fallback rendered {template} slide")
                except Exception as fallback_error:
                    print(f"❌ Fallback error for {template}: {fallback_error}")

    # Determine output path
    save_path = out_path or output_path or deck_path
    if not save_path:
        save_path = "output_presentation.pptx"
    
    # Ensure the output path has the correct extension
    if not save_path.endswith('.pptx'):
        save_path += '.pptx'
    
    # Save the presentation
    try:
        prs_obj.save(save_path)
        print(f"✅ Presentation saved successfully to: {save_path}")
    except Exception as e:
        print(f"❌ Error saving presentation: {e}")
        # Return a default path even if save failed
        save_path = "failed_to_save.pptx"
    
    return prs_obj, save_path