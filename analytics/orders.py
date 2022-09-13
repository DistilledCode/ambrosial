from collections import Counter
from itertools import groupby

from swiggy import Swiggy
from swiggy.order import Offer, Order, Payment


class OrderAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_orders = self.swiggy.order()

    def order_time_stats(self, bin: str):
        # TODO: include an option to groupby according to custom strftime string
        def cmp_fnc(order, chrono: bool = False):
            bin_ = tuple(attr for attr in bin.split("+") if attr)
            attr_mapping = {
                "hour": order.order_time.hour,
                "day": order.order_time.day,
                "week": order.order_time.isoweekday(),
                "week_": order.order_time.strftime("%A"),
                "month": order.order_time.month,
                "month_": order.order_time.strftime("%B"),
                "year": order.order_time.year,
            }
            if any((x := attr) not in attr_mapping for attr in bin_):
                raise KeyError(f"cannot group using key: {repr(x)}")

            if chrono:
                # else keys will be sorted in alphabetical order insteadl of chronological
                attr_mapping["month_"] = attr_mapping["month"]
                attr_mapping["week_"] = attr_mapping["week"]

            return tuple(attr_mapping.get(attr) for attr in bin_)

        chrono_sorted = sorted(self.all_orders, key=lambda x: cmp_fnc(x, chrono=True))
        return {key: len(list(val)) for key, val in groupby(chrono_sorted, cmp_fnc)}


class OfferAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy


class PaymentAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
