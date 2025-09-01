
# catalog_loader.py (patched to accept {"templates":[...]} as well)
from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Union

PathLike = Union[str, os.PathLike]

@dataclass
class TemplateDef:
    id: str
    purpose: str
    render_fn: str
    required_slots: Dict[str, Any]
    optional_slots: Dict[str, Any]
    chart_frames: List[Dict[str, Any]]
    validators: Dict[str, Any]
    layout_specs: Dict[str, Any]
    function_signature: Dict[str, Any]

@dataclass
class TemplateCatalog:
    templates: Dict[str, TemplateDef]

    @classmethod
    def from_file(cls, path: PathLike) -> "TemplateCatalog":
        path_str = os.fspath(path)
        ext = os.path.splitext(path_str.lower())[1]
        if ext not in (".json",):
            raise ValueError(f"Unsupported catalog file type: {ext}")
        with open(path_str, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Accept several shapes:
        items = None
        if isinstance(data, dict):
            items = data.get("slide_templates") or data.get("templates")
        if items is None:
            items = data
        if not isinstance(items, list):
            raise ValueError("Invalid templates.json format: expected list or {'slide_templates': [...]} or {'templates': [...]}")
        templates: Dict[str, TemplateDef] = {}
        for obj in items:
            tid = obj.get("id")
            if not tid:
                raise ValueError("Template missing 'id'")
            templates[tid] = TemplateDef(
                id=tid,
                purpose=obj.get("purpose",""),
                render_fn=obj.get("render_fn",""),
                required_slots=obj.get("required_slots", {}),
                optional_slots=obj.get("optional_slots", {}),
                chart_frames=obj.get("chart_frames", []),
                validators=obj.get("validators", {}),
                layout_specs=obj.get("layout_specs", {}),
                function_signature=obj.get("function_signature", {}),
            )
        return cls(templates=templates)

    def get(self, template_id: str) -> Optional[TemplateDef]:
        return self.templates.get(template_id)

    def __contains__(self, template_id: str) -> bool:
        return template_id in self.templates
