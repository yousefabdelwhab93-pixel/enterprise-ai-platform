
from fastapi import APIRouter

from backend.app.schemas.common import HealthResponse


router = APIRouter(
    prefix="/health",
    tags=["Health"]
)


@router.get("/", response_model=HealthResponse)
def health_check():
    return {
        "message": "Enterprise AI Platform is healthy!",
        "status": "success"
    }
