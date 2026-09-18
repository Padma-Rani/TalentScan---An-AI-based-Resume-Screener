"""
app/core/similarity.py

Single shared cosine-similarity implementation, used by both the
skill matcher and the qualification (education) matcher, so there is
exactly one definition of "similarity" anywhere in the codebase.
"""
from __future__ import annotations

import numpy as np


def cosine_similarity(vector_a: np.ndarray, vector_b: np.ndarray) -> float:
    denom = float(np.linalg.norm(vector_a) * np.linalg.norm(vector_b))
    if denom == 0:
        return 0.0
    return float(np.dot(vector_a, vector_b) / denom)
