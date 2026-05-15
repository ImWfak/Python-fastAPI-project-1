from http import HTTPStatus

from exception.exeption_source_enum import ExceptionSourceEnum


class AppException(Exception):
    message: str
    exception_source: ExceptionSourceEnum
    http_status_code: HTTPStatus

    def __init__(
            self,
            message: str,
            exception_source: ExceptionSourceEnum,
            http_status_code: HTTPStatus
    ) -> None:
        self.message = message
        self.exception_source = exception_source
        self.http_status_code = http_status_code
