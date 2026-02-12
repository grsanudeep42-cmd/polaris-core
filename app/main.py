from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.middleware import RequestIDMiddleware
from app.core.exceptions import ApiException
from app.db.session import engine
from app.api.v1.api import api_router
from app.core.events.registry import event_bus
from app.modules.test.handlers import TestCreatedHandler
from app.modules.test.events import TestCreatedEvent
from app.core.events.registry import event_bus
from app.core.events.audit_event import AuditEvent
from app.core.events.audit_handler import AuditEventHandler
# ------------------------------------------------------------------
# Logging Setup (initialize once at import time)
# ------------------------------------------------------------------

setup_logging()
logger = logging.getLogger(__name__)


# ------------------------------------------------------------------
# Lifespan Management
# ------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting Polaris Core...")
    event_bus.register(TestCreatedEvent, TestCreatedHandler())
    event_bus.register(AuditEvent, AuditEventHandler())

    yield

    logger.info("Shutting down Polaris Core...")
    await engine.dispose()


# ------------------------------------------------------------------
# Application Factory
# ------------------------------------------------------------------

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version="1.0.0",
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    # --------------------------------------------------------------
    # Middleware
    # --------------------------------------------------------------

    app.add_middleware(RequestIDMiddleware)

    # --------------------------------------------------------------
    # Routers
    # --------------------------------------------------------------

    app.include_router(
        api_router,
        prefix=settings.API_V1_STR,
    )

    # --------------------------------------------------------------
    # System Endpoints (Infrastructure Only)
    # --------------------------------------------------------------

    @app.get("/health", tags=["System"])
    async def health_check():
        return {
            "status": "healthy",
            "service": settings.PROJECT_NAME,
        }

    @app.get("/db-check", tags=["System"])
    async def db_check():
        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            return {
                "database": result.scalar(),
                "status": "connected",
            }

    # --------------------------------------------------------------
    # Exception Handlers
    # --------------------------------------------------------------

    @app.exception_handler(ApiException)
    async def api_exception_handler(request: Request, exc: ApiException):
        logger.warning(
            "API Exception",
            extra={
                "path": request.url.path,
                "method": request.method,
                "detail": exc.detail,
            },
        )
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "success": False,
                "error": {
                    "code": exc.error_code,
                    "message": exc.detail,
                },
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception(
            "Unhandled exception",
            extra={
                "path": request.url.path,
                "method": request.method,
            },
        )

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "data": None,
                "error": {
                    "code": "INTERNAL_SERVER_ERROR",
                    "message": "An unexpected error occurred",
                },
            },
        )

    return app


# ------------------------------------------------------------------
# ASGI App Instance
# ------------------------------------------------------------------

app = create_app()
