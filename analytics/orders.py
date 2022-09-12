from collections import Counter
from itertools import groupby

from swiggy import Swiggy
from swiggy.order import Offer, Order, Payment


class OrderAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_orders = self.swiggy.order()

    def order_time_stats(self):
        # TODO: Allow combinations, like Month + Year, Year + Day, etc
        week = lambda x: x.order_time.weekday()
        month = lambda x: x.order_time.month
        week_ = lambda x: x.order_time.strftime("%A")
        month_ = lambda x: x.order_time.strftime("%B")
        return [
            {
                key: len(list(val))
                for key, val in groupby(sorted(self.all_orders, key=week), week_)
            },
            {
                key: len(list(val))
                for key, val in groupby(sorted(self.all_orders, key=month), month_)
            },
        ]


class OfferAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy


class PaymentAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
