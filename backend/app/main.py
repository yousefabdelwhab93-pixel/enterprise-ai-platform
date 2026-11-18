
from fastapi import FastAPI

from backend.app.api.routes.health import router as health_router
from backend.app.schemas.common import HealthResponse


app = FastAPI(
    title="Enterprise AI Knowledge & Support Platform",
    description="Bilingual AI Knowledge Retrieval and Support Automation API",
    version="0.1.0",
)


app.include_router(health_router)


@app.get("/",response_model=HealthResponse)
def root():
    return {
        "message": "Enterprise AI Platform is running!",
        "status": "success"
    }
