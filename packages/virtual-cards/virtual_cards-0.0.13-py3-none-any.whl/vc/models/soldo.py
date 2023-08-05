from enum import Enum

from sqlalchemy import Column, Numeric, String, ForeignKey, Integer
from sqlalchemy.orm import relationship

from .base import CardBase, WalletBase, DateFixedMixin, CardType, CardStatus
from vc.db.base_class import Base


class WalletSo(WalletBase, DateFixedMixin, Base):
    __tablename__ = "soldo_wallet"
    blocked_balance = Column(Numeric, default=0)
    user = relationship("UserBase", back_populates="wallet_soldo")


class CardStatus(str, Enum):
    normal = "Normal"
    not_honor = "Do not honor"
    lost_card = "Lost card"
    stolen_card = "Stolen card"
    expired_card = "Expired card"
    restricted_card = "Restricted card"
    security_violation = "Security Violation"
    card_holder = "Cardholder to contact the issuer"
    destroyed = "Card Destroyed"
    pending = "pending"


class CardSo(CardBase, DateFixedMixin, Base):
    __tablename__ = "soldo_card"
    label = Column(String)
    wallet_id = Column(Integer, ForeignKey("soldo_wallet.id", ondelete="CASCADE"))
    wallet = relationship("WalletSo", backref="cards")
    type = Column(String, default=CardType.virtual.value)
    status = Column(String(20), default=CardStatus.pending.value)