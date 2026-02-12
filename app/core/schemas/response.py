from typing import Generic, Optional, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel


T = TypeVar("T")


class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[dict] = None


class ResponseEnvelope(GenericModel, Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[ErrorDetail] = None
    meta: Optional[dict] = None

    @classmethod
    def success_response(cls, data: T, meta: Optional[dict] = None):
        return cls(
            success=True,
            data=data,
            error=None,
            meta=meta,
        )

    @classmethod
    def error_response(cls, code: str, message: str, details: Optional[dict] = None):
        return cls(
            success=False,
            data=None,
            error=ErrorDetail(code=code, message=message, details=details),
            meta=None,
        )
