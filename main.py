from fastapi import FastAPI
from api.main_controller import router
from middlewares.exception_handler import global_exception_handler
from utils.logger import logger
from infra.database import startup
import logging
from utils.migration import run_migrations 
import os 
def create_app() -> FastAPI:
    app = FastAPI()
    logging.basicConfig(level=logging.DEBUG)
    # Include routes
    app.include_router(router)

    # Add custom exception handler
    app.add_exception_handler(Exception, global_exception_handler)

    logger.info("Starting FastAPI application")
    return app

app = create_app()

# Ensure the async initialization is called during startup
@app.on_event("startup")
async def startup_event():
    await startup()
    run_migrations()