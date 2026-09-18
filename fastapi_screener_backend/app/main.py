"""
app/main.py

FastAPI application exposing the resume-screening pipeline over HTTP
for the Spring Boot service (ai-service.base-url in application.yml).
"""
from __future__ import annotations

from fastapi import FastAPI

from app.api.routes import get_engine, router

app = FastAPI(title="AI Resume Screener - AI Service")
app.include_router(router)


@app.on_event("startup")
def _load_models() -> None:
    # Load the LLM/embedding models once at startup instead of on the
    # first request, so the first real /api/analyze call isn't slow.
    get_engine()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
