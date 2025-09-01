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

# Local import (must be importable from working dir)
adapters = importlib.import_module("adapters")

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
    **_ignore_kwargs,
) -> Tuple[Any, str]:
    """
    Build a deck from a plan/content/content_ir and return the pptx.Presentation and save path.
    If out_path/output_path/deck_path is provided, save the deck there.
    Extra kwargs are ignored to be compatible with older callers.
    
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

    # Determine the save path
    save_path = out_path or output_path or deck_path or "deck.pptx"

    prs_out = adapters.render_plan_to_pptx(
        plan=plan, 
        content=content, 
        content_ir=content_ir, 
        prs=prs_obj, 
        company_name=company_name,
        brand_config=brand_config  # Pass brand configuration to adapters
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