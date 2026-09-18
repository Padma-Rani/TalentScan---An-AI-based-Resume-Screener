"""
app/qualification/experience_calculator.py

Best-effort calculation of total professional experience (in months)
from the free-form employment dates extracted by ResumeAnalyzer.

This is a small, deterministic date-parsing helper - not an AI call.
Date arithmetic does not benefit from an LLM, and the project spec
explicitly allows small deterministic normalization rules as long as
the actual technology/requirement extraction stays AI-driven.
"""
from __future__ import annotations

from datetime import date, datetime
from typing import Any, Dict, List, Optional

from dateutil import parser as date_parser


PRESENT_MARKERS = {"present", "current", "now", "ongoing", "till date", "to date"}

# dateutil.parser.parse's `default` must be a datetime (it fills in any
# date/time fields missing from the parsed string) - passing a bare
# `date` object here causes parse() to hand back a `date`, which has no
# `.date()` method and breaks downstream arithmetic.
_DEFAULT_DATETIME = datetime(1900, 1, 1)


def _parse_date(raw: str) -> Optional[date]:
    if not raw:
        return None
    cleaned = raw.strip().lower()
    if any(marker in cleaned for marker in PRESENT_MARKERS):
        return date.today()
    try:
        parsed = date_parser.parse(raw, default=_DEFAULT_DATETIME, fuzzy=True)
        return parsed.date()
    except (ValueError, OverflowError, TypeError):
        return None


def _months_between(start: date, end: date) -> int:
    if end < start:
        return 0
    return (end.year - start.year) * 12 + (end.month - start.month)


def calculate_total_experience_months(experience_entries: List[Dict[str, Any]]) -> int:
    """
    Sums month counts across all experience entries. Overlap between
    concurrent roles is not de-duplicated - this is a best-effort
    estimate, and the original dates are always shown alongside it in
    the final screening result for transparency.
    """
    total_months = 0

    for entry in experience_entries:
        start_raw = str(entry.get("start_date", "")).strip()
        end_raw = str(entry.get("end_date", "")).strip()

        start = _parse_date(start_raw)
        if start is None:
            continue

        end = _parse_date(end_raw) if end_raw else date.today()
        if end is None:
            end = date.today()

        total_months += _months_between(start, end)

    return max(0, total_months)
