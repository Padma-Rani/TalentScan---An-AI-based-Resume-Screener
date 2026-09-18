"""
run.py

Starts the FastAPI AI service (app.main:app) on the port Spring Boot's
ai-service.base-url points at (see server/src/main/resources/application.yml).

Usage:
    python run.py
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000)
