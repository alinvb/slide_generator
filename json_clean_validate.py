
import json, ast, re, typing as t
from dataclasses import dataclass
import pandas as pd

CODE_FENCE_RE_START = re.compile(r"^\s*```(?:json|javascript|js)?\s*", flags=re.IGNORECASE)
CODE_FENCE_RE_END   = re.compile(r"\s*```\s*$")

ODD_QUOTES_MAP = {
    "\u201c": '"', "\u201d": '"',
    "\u2018": "'", "\u2019": "'",
    "\u2013": "-", "\u2014": "-",
    "\u00a0": " ",
    "\ufeff": "",
}

def strip_code_fences(s: str) -> str:
    s = s.strip()
    s = CODE_FENCE_RE_START.sub("", s)
    s = CODE_FENCE_RE_END.sub("", s)
    return s.strip()

def replace_odd_quotes(s: str) -> str:
    for bad, good in ODD_QUOTES_MAP.items():
        s = s.replace(bad, good)
    return s

def remove_trailing_commas(s: str) -> str:
    return re.sub(r",\s*(?=[}\]])", "", s)

def sanitize_text(s: str) -> str:
    return replace_odd_quotes(strip_code_fences(s))

def parse_json_with_fallbacks(s: str):
    try:
        return json.loads(s)
    except Exception:
        pass
    try:
        s2 = remove_trailing_commas(s)
        return json.loads(s2)
    except Exception:
        pass
    try:
        return ast.literal_eval(s)
    except Exception:
        pass
    try:
        s2 = remove_trailing_commas(s)
        return ast.literal_eval(s2)
    except Exception as e:
        raise ValueError(f"Unable to parse chatbot JSON. Last error: {e}")

def sanitize_and_parse(raw: str):
    return parse_json_with_fallbacks(sanitize_text(raw))

@dataclass
class VError:
    path: str
    message: str
    level: str = "ERROR"

def _type_name(tp): 
    if isinstance(tp, tuple): 
        return " or ".join(t.__name__ for t in tp) 
    return tp.__name__

def require(obj, key, expected_type, path, errors: list, non_empty=True):
    if not isinstance(obj, dict):
        errors.append(VError(path, f"Expected object/dict but got {type(obj).__name__}"))
        return None
    if key not in obj:
        errors.append(VError(f"{path}.{key}", "Missing required key"))
        return None
    val = obj[key]
    if not isinstance(val, expected_type):
        errors.append(VError(f"{path}.{key}", f"Expected type {_type_name(expected_type)}, got {type(val).__name__}"))
        return None
    if non_empty and ( (isinstance(val, (list, dict, str)) and len(val)==0) ):
        errors.append(VError(f"{path}.{key}", "Must be non-empty"))
    return val

def require_list_of(obj, key, elem_type, path, errors: list, min_len=1):
    val = require(obj, key, list, path, errors)
    if isinstance(val, list):
        if len(val) < min_len:
            errors.append(VError(f"{path}.{key}", f"List must have ≥{min_len} items"))
        for i, e in enumerate(val):
            if not isinstance(e, elem_type):
                errors.append(VError(f"{path}.{key}[{i}]", f"Expected {_type_name(elem_type)}, got {type(e).__name__}"))
    return val

def assert_equal_lengths(arrays: list, path, errors: list):
    lens = [len(a) for _, a in arrays if isinstance(a, list)]
    if len(set(lens)) > 1:
        lengths = ", ".join(f"{name}={len(a)}" for name, a in arrays)
        errors.append(VError(path, f"Arrays must have equal length: {lengths}"))

def approx_equal(a: float, b: float, tol=1e-6) -> bool:
    if a == 0 and b == 0: 
        return True
    if a == 0 or b == 0:
        return abs(a - b) < tol
    return abs(a-b)/max(abs(a),abs(b)) <= 0.02

def validate_buyer_profiles(data, path, errors):
    require(data, "title", str, path, errors)
    require(data, "subtitle", str, path, errors)
    require(data, "company", str, path, errors)
    headers = require_list_of(data, "table_headers", str, path, errors, min_len=3)
    rows = require(data, "table_rows", list, path, errors)
    if isinstance(rows, list):
        for i, row in enumerate(rows):
            if not isinstance(row, dict):
                errors.append(VError(f"{path}.table_rows[{i}]", "Row must be an object"))
                continue
            for k in ("buyer_name", "description", "fit_score"):
                if k not in row:
                    errors.append(VError(f"{path}.table_rows[{i}].{k}", "Missing required field"))

def validate_hist_fin_perf(data, path, errors):
    require(data, "title", str, path, errors)
    chart = require(data, "chart", dict, path, errors)
    if isinstance(chart, dict):
        cats = require_list_of(chart, "categories", str, f"{path}.chart", errors, min_len=2)
        rev = require_list_of(chart, "revenue", (int,float), f"{path}.chart", errors, min_len=2)
        ebd = require_list_of(chart, "ebitda", (int,float), f"{path}.chart", errors, min_len=2)
        if all(isinstance(x, list) for x in [cats, rev, ebd]):
            assert_equal_lengths([("categories", cats), ("revenue", rev), ("ebitda", ebd)], f"{path}.chart", errors)

def validate_margin_cost(data, path, errors):
    require(data, "title", str, path, errors)
    cd = require(data, "chart_data", dict, path, errors)
    if isinstance(cd, dict):
        cats = require_list_of(cd, "categories", str, f"{path}.chart_data", errors, min_len=2)
        vals = require_list_of(cd, "values", (int,float), f"{path}.chart_data", errors, min_len=2)
        if isinstance(cats, list) and isinstance(vals, list):
            assert_equal_lengths([("categories", cats), ("values", vals)], f"{path}.chart_data", errors)
    cm = require(data, "cost_management", dict, path, errors)
    if isinstance(cm, dict):
        items = require_list_of(cm, "items", dict, f"{path}.cost_management", errors, min_len=1)
        if isinstance(items, list):
            for i, it in enumerate(items):
                require(it, "title", str, f"{path}.cost_management.items[{i}]", errors)
                require(it, "description", str, f"{path}.cost_management.items[{i}]", errors)

def validate_investor_considerations(data, path, errors):
    require_list_of(data, "considerations", str, path, errors, min_len=3)
    require_list_of(data, "mitigants", str, path, errors, min_len=3)

def validate_competitive_positioning(data, path, errors):
    comps = require_list_of(data, "competitors", dict, path, errors, min_len=3)
    require_list_of(data, "assessment", list, path, errors, min_len=2)
    require_list_of(data, "barriers", dict, path, errors, min_len=1)
    require_list_of(data, "advantages", dict, path, errors, min_len=1)
    if isinstance(comps, list):
        for i, c in enumerate(comps):
            require(c, "name", str, f"{path}.competitors[{i}]", errors)
            require(c, "revenue", (int,float), f"{path}.competitors[{i}]", errors)

def validate_product_service_footprint(data, path, errors):
    svcs = require_list_of(data, "services", dict, path, errors, min_len=3)
    if isinstance(svcs, list):
        for i, s in enumerate(svcs):
            require(s, "title", str, f"{path}.services[{i}]", errors)
            require(s, "desc", str, f"{path}.services[{i}]", errors)
    cov = require_list_of(data, "coverage_table", list, path, errors, min_len=2)
    if isinstance(cov, list):
        hdr = cov[0] if cov else None
        if not isinstance(hdr, list) or len(hdr) < 2:
            errors.append(VError(f"{path}.coverage_table[0]", "First row must be header with ≥2 columns"))
    metrics = require(data, "metrics", dict, path, errors)

def validate_business_overview(data, path, errors):
    require(data, "description", str, path, errors)
    tl = require(data, "timeline", dict, path, errors)
    if isinstance(tl, dict):
        require(tl, "start_year", str, f"{path}.timeline", errors)
        require(tl, "end_year", str, f"{path}.timeline", errors)
    require_list_of(data, "highlights", str, path, errors, min_len=3)
    require_list_of(data, "services", str, path, errors, min_len=3)

def validate_precedent_transactions(data, path, errors):
    txs = require_list_of(data, "transactions", dict, path, errors, min_len=1)
    if isinstance(txs, list):
        for i, tx in enumerate(txs):
            require(tx, "date", str, f"{path}.transactions[{i}]", errors)
            require(tx, "target", str, f"{path}.transactions[{i}]", errors)
            require(tx, "acquirer", str, f"{path}.transactions[{i}]", errors)
            require(tx, "country", str, f"{path}.transactions[{i}]", errors)
            ev  = require(tx, "enterprise_value", (int,float), f"{path}.transactions[{i}]", errors)
            rev = require(tx, "revenue", (int,float), f"{path}.transactions[{i}]", errors)
            mult = require(tx, "ev_revenue_multiple", (int,float), f"{path}.transactions[{i}]", errors)
            if isinstance(ev, (int,float)) and isinstance(rev, (int,float)) and isinstance(mult, (int,float)) and rev:
                calc = ev / rev
                if not approx_equal(calc, mult):
                    errors.append(VError(f"{path}.transactions[{i}].ev_revenue_multiple", f"Multiple {mult} not ~ EV/Revenue ({calc:.2f})"))

def validate_valuation_overview(data, path, errors):
    v = require_list_of(data, "valuation_data", dict, path, errors, min_len=1)
    if isinstance(v, list):
        for i, row in enumerate(v):
            require(row, "methodology", str, f"{path}.valuation_data[{i}]", errors)
            require(row, "enterprise_value", str, f"{path}.valuation_data[{i}]", errors)
            require(row, "metric", str, f"{path}.valuation_data[{i}]", errors)
            require(row, "22a_multiple", str, f"{path}.valuation_data[{i}]", errors)
            require(row, "23e_multiple", str, f"{path}.valuation_data[{i}]", errors)

def validate_investor_process_overview(data, path, errors):
    require_list_of(data, "diligence_topics", dict, path, errors, min_len=3)
    require_list_of(data, "synergy_opportunities", dict, path, errors, min_len=2)
    require_list_of(data, "risk_factors", str, path, errors, min_len=2)
    require_list_of(data, "mitigants", str, path, errors, min_len=2)
    require_list_of(data, "timeline", dict, path, errors, min_len=2)

def validate_growth_strategy_projections(data, path, errors):
    sd = require(data, "slide_data", dict, path, errors)
    if isinstance(sd, dict):
        require(sd, "title", str, f"{path}.slide_data", errors)
        fs = require(sd, "financial_projections", dict, f"{path}.slide_data", errors)
        if isinstance(fs, dict):
            cats = require_list_of(fs, "categories", str, f"{path}.slide_data.financial_projections", errors, min_len=2)
            rev  = require_list_of(fs, "revenue", (int,float), f"{path}.slide_data.financial_projections", errors, min_len=2)
            ebd  = require_list_of(fs, "ebitda", (int,float), f"{path}.slide_data.financial_projections", errors, min_len=2)
            if all(isinstance(x, list) for x in [cats, rev, ebd]):
                assert_equal_lengths([("categories", cats), ("revenue", rev), ("ebitda", ebd)], f"{path}.slide_data.financial_projections", errors)

def validate_sea_conglomerates(data, path, errors):
    if not isinstance(data, list):
        errors.append(VError(path, "Expected a list of conglomerates"))
        return
    if len(data) == 0:
        errors.append(VError(path, "List must be non-empty"))
        return
    for i, row in enumerate(data):
        if not isinstance(row, dict):
            errors.append(VError(f"{path}[{i}]", "Item must be object"))
            continue
        for k in ("name", "country", "description"):
            if k not in row:
                errors.append(VError(f"{path}[{i}].{k}", "Missing required field"))

TEMPLATE_VALIDATORS = {
    "management_team": lambda d,p,e: (require(d, "title", str, p, e), require_list_of(d, "left_column_profiles", dict, p, e), require_list_of(d, "right_column_profiles", dict, p, e)),
    "historical_financial_performance": validate_hist_fin_perf,
    "margin_cost_resilience": validate_margin_cost,
    "investor_considerations": validate_investor_considerations,
    "competitive_positioning": validate_competitive_positioning,
    "product_service_footprint": validate_product_service_footprint,
    "business_overview": validate_business_overview,
    "precedent_transactions": validate_precedent_transactions,
    "valuation_overview": validate_valuation_overview,
    "investor_process_overview": validate_investor_process_overview,
    "growth_strategy_projections": validate_growth_strategy_projections,
    "sea_conglomerates": validate_sea_conglomerates,
    "buyer_profiles": validate_buyer_profiles,
}

def validate_render_plan(plan: dict) -> list:
    errors: list[VError] = []
    slides = require(plan, "slides", list, "render_plan", errors)
    if isinstance(slides, list):
        for i, slide in enumerate(slides):
            path = f"render_plan.slides[{i}]"
            tpl = require(slide, "template", str, path, errors)
            data = require(slide, "data", (dict, list), path, errors)
            if isinstance(tpl, str) and tpl in TEMPLATE_VALIDATORS and data is not None:
                TEMPLATE_VALIDATORS[tpl](data, f"{path}.data", errors)
            elif isinstance(tpl, str) and tpl not in TEMPLATE_VALIDATORS:
                errors.append(VError(path + ".template", f"Unknown template '{tpl}' — add a validator or correct the name"))
    return errors

def validate_content_ir(ir: dict) -> list:
    errors: list[VError] = []
    require(ir, "entities", dict, "content_ir", errors)
    require(ir, "facts", dict, "content_ir", errors)
    require(ir, "charts", list, "content_ir", errors)
    require(ir, "management_team", dict, "content_ir", errors)
    require(ir, "investor_considerations", dict, "content_ir", errors)
    require(ir, "competitive_analysis", dict, "content_ir", errors)
    require(ir, "precedent_transactions", list, "content_ir", errors)
    require(ir, "valuation_data", list, "content_ir", errors)
    require(ir, "product_service_data", dict, "content_ir", errors)
    require(ir, "business_overview_data", dict, "content_ir", errors)
    require(ir, "growth_strategy_data", dict, "content_ir", errors)
    require(ir, "investor_process_data", dict, "content_ir", errors)
    require(ir, "margin_cost_data", dict, "content_ir", errors)
    return errors

def validate_report(name: str, errors: list) -> pd.DataFrame:
    rows = [{"file": name, "level": e.level, "path": e.path, "message": e.message} for e in errors]
    return pd.DataFrame(rows) if rows else pd.DataFrame([{"file": name, "level": "OK", "path": "-", "message": "No errors"}])
