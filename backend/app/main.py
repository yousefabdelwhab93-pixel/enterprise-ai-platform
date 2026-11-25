from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends

from backend.app.api.routes.health import router as health_router
from backend.app.core.config import settings
from backend.app.schemas.common import HealthResponse
from backend.app.api.dependencies import get_app_name
from backend.app.api.routes import tenants
from backend.app.api.routes import users
from backend.app.api.routes import auth
from backend.app.api.routes import documents

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print("🚀 Application is starting...")

    yield

    # Shutdown
    print("🛑 Application is shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Bilingual AI Knowledge Retrieval and Support Automation API",
    version="0.1.0",
    lifespan=lifespan,
)
# Existing Health Router
app.include_router(health_router)
# Tenants Router
app.include_router(
    tenants.router,
    prefix="/api/v1",
)

# Users Router
app.include_router(
    users.router,
    prefix="/api/v1",
)

app.include_router(auth.router, prefix="/api/v1")

# Documents Router
app.include_router(
    documents.router,
    prefix="/api/v1",
)


@app.get("/", response_model=HealthResponse)
def root(app_name: str = Depends(get_app_name)):
    return {
        "message": f"{app_name} is running!",
        "status": "success",
    }


