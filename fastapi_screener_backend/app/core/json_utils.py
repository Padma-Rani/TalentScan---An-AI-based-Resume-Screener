"""
app/core/json_utils.py

Robust extraction of a JSON object from raw LLM text output.

LLMs may return:
    - Markdown code fences (```json ... ```)
    - Extra prose before/after the JSON
    - Trailing commas or other minor malformations
    - Nothing at all

This module tries progressively more forgiving strategies and returns
None (never raises) if no valid JSON object can be recovered, so
callers can apply a deterministic fallback.
"""
from __future__ import annotations

import json
import re
from typing import Optional


def extract_json_object(raw_text: str) -> Optional[dict]:
    if not raw_text or not raw_text.strip():
        return None

    text = raw_text.strip()

    # 1. Strip a ```json ... ``` or ``` ... ``` fence if present.
    fence_match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1).strip()

    # 2. Try a direct parse.
    parsed = _try_parse(text)
    if parsed is not None:
        return parsed

    # 3. Locate the outermost {...} block and try again.
    start = text.find("{")
    end = text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = text[start:end + 1]
        parsed = _try_parse(candidate)
        if parsed is not None:
            return parsed

        # 4. Light repair: remove trailing commas before } or ].
        repaired = re.sub(r",\s*([}\]])", r"\1", candidate)
        parsed = _try_parse(repaired)
        if parsed is not None:
            return parsed

    return None


def _try_parse(text: str) -> Optional[dict]:
    try:
        result = json.loads(text)
        return result if isinstance(result, dict) else None
    except (json.JSONDecodeError, ValueError):
        return None
