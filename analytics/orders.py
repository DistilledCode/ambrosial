from collections import Counter

from swiggy import Swiggy
from swiggy.order import Offer, Order, Payment

from analytics import SwiggyAnalytics


class OrderAnalytics(SwiggyAnalytics):
    def __init__(self, swiggy: Swiggy = None) -> None:
        SwiggyAnalytics.__init__(self, swiggy)
        self.counter = Counter(self.orders)

    pass


class OfferAnalytics(SwiggyAnalytics):
    def __init__(self, swiggy: Swiggy = None) -> None:
        SwiggyAnalytics.__init__(self, swiggy)
        self.counter = Counter(self.offers)

    pass


class PaymentAnalytics(SwiggyAnalytics):
    def __init__(self, swiggy: Swiggy = None) -> None:
        SwiggyAnalytics.__init__(self, swiggy)
        self.counter = Counter(self.payments)

    pass
