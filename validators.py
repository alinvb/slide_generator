
# validators.py (smarter, chart_ref-aware)
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

from catalog_loader import TemplateCatalog

@dataclass
class PlanIssue:
    severity: str  # "missing" | "error" | "warning" | "info"
    slot: str
    message: str

@dataclass
class TemplateReport:
    template_id: str
    issues: List[PlanIssue] = field(default_factory=list)

@dataclass
class ValidationReport:
    ok: bool
    issues: List[PlanIssue]
    by_template: Dict[str, List[Dict[str, str]]]
    counts: Dict[str, int]

def _add_issue(collector: List[PlanIssue], severity: str, slot: str, msg: str):
    collector.append(PlanIssue(severity, slot, msg))

def _chart_by_id(content_ir: Dict[str, Any], chart_id: str) -> Optional[Dict[str, Any]]:
    for ch in content_ir.get("charts", []):
        if ch.get("id") == chart_id:
            return ch
    return None

def _len_categories(chart: Dict[str, Any]) -> Optional[int]:
    cats = chart.get("categories")
    if isinstance(cats, list):
        return len(cats)
    return None

def _chart_type_ok_for_template(tpl_id: str, chart_type: str, tpl_obj) -> bool:
    # Normalize
    t = (chart_type or "").lower().strip()
    # Historical Financial Performance accepts combo / combination_column_clustered / column+line
    if tpl_id == "historical_financial_performance":
        return t in {"combo", "combination_column_clustered", "column_clustered", "line"}
    # Margin & Cost Resilience expects a line-ish series
    if tpl_id == "margin_cost_resilience":
        return t in {"line", "line_with_markers", "area", "bar"}
    # Growth strategy uses clustered columns for "industry growth"
    if tpl_id == "growth_strategy_projections":
        return t in {"column_clustered", "bar", "combo"}
    # Competitive positioning revenue chart is a column chart
    if tpl_id == "competitive_positioning":
        return t in {"column_clustered", "bar"}
    # Default: allow common types
    return t in {"bar", "line", "area", "column_clustered", "combo", "line_with_markers"}

def _points_ok(tpl_id: str, n: int) -> Tuple[bool, int, int]:
    # Return (in_range, min, max) for warnings
    ranges = {
        "historical_financial_performance": (3, 7),
        "margin_cost_resilience": (3, 10),
        "growth_strategy_projections": (3, 7),
    }
    mn, mx = ranges.get(tpl_id, (1, 9999))
    return (mn <= n <= mx, mn, mx)

def _summarize(issues: List[PlanIssue]) -> Dict[str, int]:
    counts = {"missing": 0, "error": 0, "warning": 0, "info": 0}
    for i in issues:
        counts[i.severity] += 1
    return counts

def validate_render_plan_against_catalog(
    content_ir: Dict[str, Any],
    render_plan: Dict[str, Any],
    catalog: TemplateCatalog,
) -> ValidationReport:
    all_issues: List[PlanIssue] = []
    by_template: Dict[str, List[Dict[str, str]]] = {}

    plan_items = render_plan.get("render_plan", [])
    if not isinstance(plan_items, list):
        _add_issue(all_issues, "error", "render_plan", "render_plan must be a list")
        return ValidationReport(False, all_issues, {}, _summarize(all_issues))

    for item in plan_items:
        tpl_id = item.get("template_id")
        slots = item.get("slots", {})
        tpl_obj = catalog.get(tpl_id) if tpl_id else None
        local_issues: List[PlanIssue] = []

        if not tpl_id:
            _add_issue(local_issues, "error", "template_id", "Missing template_id")
            continue
        if tpl_obj is None:
            _add_issue(local_issues, "error", "template_id", f"Unknown template '{tpl_id}'")
            by_template[tpl_id] = [vars(i) for i in local_issues]
            all_issues.extend(local_issues)
            continue

        # Required slots check (with chart_ref awareness)
        required = (tpl_obj.required_slots or {}).keys()
        for slot in required:
            if slot in slots:
                continue
            # Allow chart_ref to satisfy "chart" or "chart_data" if resolvable
            if slot in {"chart", "chart_data"} and "chart_ref" in slots:
                ch = _chart_by_id(content_ir, slots["chart_ref"])
                if ch is not None:
                    continue
            _add_issue(local_issues, "missing", slot, f"Missing required slot '{slot}'")

        # If chart_ref provided, validate its type and point count when possible
        ch_ref = slots.get("chart_ref")
        if ch_ref:
            chart = _chart_by_id(content_ir, ch_ref)
            if not chart:
                _add_issue(local_issues, "error", "chart_ref", f"chart_ref '{ch_ref}' not found in content_ir.charts")
            else:
                ctype = chart.get("type", "")
                if not _chart_type_ok_for_template(tpl_id, ctype, tpl_obj):
                    _add_issue(
                        local_issues,
                        "warning",
                        "chart_ref",
                        f"Chart type '{ctype}' may not be ideal for template '{tpl_id}'"
                    )
                n = _len_categories(chart)
                if isinstance(n, int) and n > 0:
                    ok, mn, mx = _points_ok(tpl_id, n)
                    if not ok:
                        _add_issue(local_issues, "warning", "chart", f"chart should have {mn}–{mx} data points")

        # Record and accumulate
        by_template[tpl_id] = [vars(i) for i in local_issues]
        all_issues.extend(local_issues)

    ok = all(i.severity not in {"error", "missing"} for i in all_issues)
    return ValidationReport(ok, all_issues, by_template, _summarize(all_issues))

def summarize_issues(report: ValidationReport) -> str:
    return (
        f"{ {'ok': report.ok, 'counts': report.counts, 'by_template': report.by_template} }"
    )
