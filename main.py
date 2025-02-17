from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from api.main import api_router # Assuming api_router is defined
from exceptions.exception_handler import validation_exception_handler # Assuming handlers are defined
from infra.database import get_database, database_instance # Import get_database dependency
import logging
from logging.config import dictConfig
from configs.config import LOGGING_CONFIG # Assuming LOGGING_CONFIG is defined
from middlewares.request_logger import log_requests # Assuming middleware is defined


def create_app() -> FastAPI:
    dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger("app")

    app = FastAPI()
    app.include_router(api_router) # Include your API routes
    app.middleware("http")(log_requests) # Register request logging middleware
    app.add_exception_handler(RequestValidationError, validation_exception_handler) # Register exception handlers

    logger.info("FastAPI app created")
    return app

app = create_app()

@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("app")
    database_instance
    logger.info("Database initialized via dependency injection.")

    logger.info("Application startup tasks finished.")

    # app.dependency_overrides[get_database] = lambda: database_instance # Override dependency