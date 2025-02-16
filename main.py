from fastapi import FastAPI
from api.main import api_router
from middlewares.exception_handler import global_exception_handler
from infra.database import Database
# from logging.logger import logger
from utils.migration import run_migrations 
import os 


def create_app() -> FastAPI:
    app = FastAPI()
    # Include routes
    app.include_router(api_router)

    # Add custom exception handler
    app.add_exception_handler(Exception, global_exception_handler)

    # logger.info("Starting FastAPI application")
    return app

app : FastAPI = create_app()


# Ensure the async initialization is called during startup
@app.on_event("startup")
async def startup_event():
    database : Database = Database()
    await database.startup()
    run_migrations()
