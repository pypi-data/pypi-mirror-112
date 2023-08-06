from datetime import datetime
from decimal import Decimal
from typing import Optional, Generic, TypeVar, List, Dict
from pydantic import BaseModel, Extra, root_validator
from pydantic.generics import GenericModel
from .utils import decrypt

T = TypeVar('T')


class ResponseInfo(BaseModel):

    class Config:
        extra = Extra.allow


class UserBase(ResponseInfo):
    name: Optional[str]
    email: Optional[str]
    status: Optional[str]
    surname: Optional[str]
    job_title: Optional[str]
    custom_reference_id: Optional[str]


class UserResponse(UserBase):
    id: Optional[str]


class Order(GenericModel, Generic[T]):
# {
# "id":"6a5e0887-eaf6-4f49-95cb-6b7f245d04f3",
# "status":"PLACED","creation_time":"2021-06-29T10:42:06",
# "last_update_time":"2021-06-29T10:42:06","is_valid":true,"total_paid_amount":0.000000,
# "total_paid_currency":"EUR",
# "items":[{"id":"87d95150-41f3-46a5-9501-ca1b368696ca","itemType":"WALLET","category":"WALLET"}]}
    id: str
    status: str
    creation_time: datetime
    last_update_time: datetime
    is_valid: bool
    total_paid_amount: Decimal
    total_paid_currency: str
    items: Optional[List[T]]


class OrderItem(ResponseInfo):
    id: Optional[str]
    itemType: Optional[str]
    category: Optional[str]


class CardResponse(ResponseInfo):
    id: str
    label: Optional[str]
    name: Optional[str]
    status: str
    sensitive_data: Optional[Dict]
    expiration_date: datetime
    creation_time: datetime
    wallet_id: Optional[str]
    type: Optional[str]
    owner_type: str
    owner_public_id: Optional[str]
    masked_pan: str
    pan: Optional[str] = None
    cvv: Optional[str] = None

    @root_validator(pre=True)
    def validate_root(cls, values):
        if values.get("sensitive_data"):
            if values['sensitive_data'].get("encrypted_full_pan"):
                values["pan"] = decrypt(values['sensitive_data'].get("encrypted_full_pan"))
            if values['sensitive_data'].get("encrypted_cvv"):
                values["cvv"] = decrypt(values['sensitive_data'].get("encrypted_cvv"))
        if not values.get("pan"):
            values["pan"] = values.get("masked_pan")
        return values


class CardRule(BaseModel):
    name: str
    enabled: Optional[bool]
    amount: Optional[Decimal]


class ListRules(BaseModel):
    rules: List[CardRule]


class PaginateList(GenericModel, Generic[T]):
    results: List[T]
    current_page: int
    page_size: int
    pages: int
    results_size: int
    total: int


class WalletBase(ResponseInfo):
    id: Optional[str]
    name: Optional[str]
    primary_user_public_id: Optional[str]
    available_amount: Optional[Decimal]
    currency_code: Optional[str]
    blocked_amount: Optional[Decimal]