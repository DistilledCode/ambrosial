from collections import Counter

from swiggy import Swiggy
from swiggy.order import Offer, Order, Payment


class OrderAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy


class OfferAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy


class PaymentAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
