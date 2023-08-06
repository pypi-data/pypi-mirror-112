from typing import TypeVar, Optional

from pydantic.generics import GenericModel, Generic
from typing import Optional


T = TypeVar('T')


class ResponseData(GenericModel, Generic[T]):
    status_code: Optional[int]
    url: Optional[str]
    data: Optional[T]
    message: Optional[str]
    error_description: Optional[str]
    error: Optional[str]
    error_code: Optional[str]
