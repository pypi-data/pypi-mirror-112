from datetime import datetime
from .base_class import Base
from enum import Enum
from sqlalchemy import Column, Integer, ForeignKey, String, Date, DateTime, func, Numeric, Boolean
from sqlalchemy.orm import relationship


class StatusAccountVC(str, Enum):
    deactivated = "Deactivated"
    paid = "Paid"
    beta = "Beta"


class AccountVC(Base):
    __tablename__ = "vc_account"
    number = Column(String(100))
    balance = Column(Numeric, default=0)
    status = Column(String(15), default=StatusAccountVC.deactivated.value)

    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    # user = relationship("User", backref="vc_accounts")
    # campaigns = relationship("CampaignVC", back_populates="account")

    activated_on = Column(DateTime, index=True)
    created_on = Column(DateTime, default=datetime.now, server_default=func.now(), index=True)

    @property
    def is_active(self) -> bool:
        return bool(
            (self.status == StatusAccountVC.beta.value) or (self.status == StatusAccountVC.paid.value))

    def __repr__(self, **kwargs):
        return super().__repr__(f"id: {self.id}| user: {self.user.id}")


class CampaignType(str, Enum):
    # facebook = "facebook"
    # google = "google"
    facebook = "2"
    google = "1"
    prepaidcard = "3"


class CustomStatus(str, Enum):
    hidden = "Hidden"
    not_set = " "


class CampaignVC(Base):
    __tablename__ = "vc_campaign"
    number = Column(String(100))
    balance = Column(Numeric, default=0)
    account_id = Column(Integer, ForeignKey("vc_account.id", ondelete="CASCADE"), index=True, nullable=False)

    # account = relationship("AccountVC", back_populates="campaigns")

    type = Column(String, default=CampaignType.facebook.value)
    # cards = relationship("CardVC", back_populates="campaign")

    @property
    def count_cards(self):
        return len(self.cards)

    def __repr__(self, **kwargs):
        return super().__repr__(f"id {self.id} type - {self.type}")

    @property
    def sum_cards(self):
        return sum([card.balance for card in self.cards])


class StatusCard(str, Enum):
    pending = "PENDING"
    active = "ACT"
    block = "BLO"
    deleted = "DELETED"


class TypeCard(str, Enum):
    virtual_multi_use = "Virtual multi use"
    single_load_card = "Single load card"


class PaymentSystem(str, Enum):
    master_card = "MASTERCARD"
    visa = "VISA"


class CardVC(Base):
    __tablename__ = "vc_card"
    bin_id = Column(Integer)
    system_id = Column(Integer, index=True)
    reference = Column(String, index=True, unique=True, nullable=False)
    is_slave = Column(Boolean, default=False)
    campaign_vc_id = Column(Integer, ForeignKey("vc_campaign.id", ondelete="CASCADE"))
    # campaign = relationship("CampaignVC", back_populates="cards")
    balance = Column(Numeric, default=0)
    PAN = Column(String, index=True)
    cvv = Column(String(5))
    expiry = Column(Date)
    custom_status = Column(String)
    custom_comment = Column(String)
    custom_comment2 = Column(String)
    status = Column(String(20), default=StatusCard.pending.value)
    type = Column(String, default=TypeCard.virtual_multi_use.value)
    payment_system = Column(String, default=PaymentSystem.master_card.value)
    created_on = Column(DateTime, default=datetime.now, server_default=func.now(), index=True)


    def __repr__(self, **kwargs):
        return super().__repr__(f"id {self.id} | PAN: {self.PAN}")
