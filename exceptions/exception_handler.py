import logging
from fastapi import Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger("app")  # Get logger instance


async def universal_exception_handler(request: Request, exc: Exception):
    logger.error(
        "Unhandled exception occurred",
        exc_info=exc,
        extra={"path": request.url.path, "method": request.method},
    )
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    logger.error(
        "Validation error",
        exc_info=exc,
        extra={
            "path": request.url.path,
            "method": request.method,
            "body": exc.body,
        },
    )
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )
