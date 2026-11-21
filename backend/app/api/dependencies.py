from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.core.config import Settings, settings
from backend.app.core.database import SessionLocal


def get_settings() -> Settings:
    return settings


def get_app_name(app_settings: Settings = Depends(get_settings)):
    return app_settings.APP_NAME


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()