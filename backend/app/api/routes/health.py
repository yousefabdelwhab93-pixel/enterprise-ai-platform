
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from backend.app.schemas.common import HealthResponse
from backend.app.api.dependencies import get_db


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

@router.get("/db")
def database_health(db: Session = Depends(get_db)):
    database_name = db.execute(
        text("SELECT current_database()")
    ).scalar()

    return {
        "status": "success",
        "database": database_name,
        "message": "Database connection is working!"
    }
