from fastapi import HTTPException, status


class ApiException(HTTPException):
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = "API_ERROR",
    ):
        self.error_code = error_code
        super().__init__(status_code=status_code, detail=detail)


class NotFoundException(ApiException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            error_code="NOT_FOUND",
        )


class ConflictException(ApiException):
    def __init__(self, detail: str = "Conflict detected"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code="CONFLICT",
        )


class VersionMismatchException(ApiException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="Resource version mismatch",
            error_code="VERSION_CONFLICT",
        )
