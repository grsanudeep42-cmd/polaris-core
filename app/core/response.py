from typing import Generic, TypeVar, Optional
from pydantic import BaseModel


T = TypeVar("T")


class ResponseEnvelope(BaseModel, Generic[T]):
    success: bool = True
    message: Optional[str] = None
    data: Optional[T] = None
