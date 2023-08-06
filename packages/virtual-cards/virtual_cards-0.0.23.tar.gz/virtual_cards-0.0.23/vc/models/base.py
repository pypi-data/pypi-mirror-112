from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Column, func, Numeric, Integer, ForeignKey, String, Date
from sqlalchemy.ext.declarative import declared_attr

from vc.db.base_class import Base
from vc.db.models import StatusCard


class UserBase(Base):
    __tablename__ = "user"
    email = Column(String, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    job_title = Column(String)

    def __repr__(self, input_str=None):
        return super().__repr__(f"{self.email} {self.id}")


class WalletStatus(str, Enum):
    deactivated = "Deactivated"
    paid = "Paid"
    beta = "Beta"


class CardStatus(str, Enum):
    pending = "pending"
    active = "activated"
    block = "blocked"
    deleted = "deleted"


class CardType(str, Enum):
    virtual_multi_use = "Virtual multi use"
    virtual = "VIRTUAL"
    google = "GOOGLE_CARD"
    single_load_card = "Single load card"


class DateFixedMixin:
    created_on = Column(
        DateTime, default=datetime.now, server_default=func.now(), index=True
    )
    updated_on = Column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        server_default=func.now(),
    )


class WalletBase:
    search_id = Column(String)
    status = Column(String(15), default=WalletStatus.deactivated.value)
    balance = Column(Numeric, nullable=False, default=0)
    currency = Column(String(10), default="EUR")

    @declared_attr
    def user_id(cls):
        return Column(Integer,
                      # ForeignKey("user.id", ondelete="CASCADE"),
                      nullable=False)


class CardBase:
    search_id = Column(String)
    PAN = Column(String, index=True)
    cvv = Column(String(5))
    expiry = Column(Date)
    status = Column(String(20), default=CardStatus.pending.value)
    type = Column(String, default=CardType.virtual_multi_use.value)
