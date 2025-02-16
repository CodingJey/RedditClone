# middleware.py
import time
import logging
from fastapi import Request

logger = logging.getLogger("app")  # Get logger instance

async def log_requests(request: Request, call_next):
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = f"{process_time:.2f}ms"

    logger.info(
        "Request processed",
        extra={
            "path": request.url.path,
            "method": request.method,
            "processing_time": formatted_process_time,
            "status_code": response.status_code,
        },
    )

    return response