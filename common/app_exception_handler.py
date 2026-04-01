from fastapi import Request
from starlette.responses import JSONResponse

from common.app_exception import AppException


async def app_exception_handler(request: Request, app_exception: AppException) -> JSONResponse:
    return JSONResponse(
        status_code=app_exception.http_status_code,
        content={
            "message": app_exception.message,
            "exception_source": app_exception.exception_source
        }
    )
