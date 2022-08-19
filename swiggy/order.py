from dataclasses import dataclass, field
from typing import Optional, Union


@dataclass(kw_only=True, frozen=True)
class Order:
    pass


@dataclass(kw_only=True, frozen=True)
class Payment:
    paymentMethod: str
    paymentMethodDisplayName: str
    transactionId: str
    amount: str  # could be int
    paymentMeta: dict[str, Optional[Union[str, dict]]]
    transactionStatus: str
    swiggyTransactionId: str
    pgTransactionId: str
    couponApplied: str
    paymentGateway: Optional[str]
    pgResponseTime: str


@dataclass(kw_only=True, frozen=True)
class OffersData:
    id: str
    super_type: str
    total_offer_discount: float
    discount_share: dict[str, Union[int, float]]
    discount_type: str
    description: str
    fixed_charges: dict[str, dict[str, Union[int, str]]]
