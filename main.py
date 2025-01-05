from fastapi import FastAPI
from api.main_controller import router
from middlewares.exception_handler import global_exception_handler
from utils.logger import logger
from infra.database import Base, engine

def create_app() -> FastAPI:
    # Initialize database
    Base.metadata.create_all(bind=engine)

    app = FastAPI()

    # Include routes
    app.include_router(router)

    # Add custom exception handler
    app.add_exception_handler(Exception, global_exception_handler)

    logger.info("Starting FastAPI application")
    return app

app = create_app()

