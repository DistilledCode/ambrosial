from collections import Counter
from itertools import groupby

from swiggy import Swiggy
from swiggy.order import Offer, Order, Payment


class OrderAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_orders = self.swiggy.order()

    def group_by(self, attr: str):
        attrs = [i for i, j in Order.__annotations__.items() if j.__hash__ is not None]
        if attr not in list(Order.__annotations__):
            raise TypeError(f"type object 'Order' has no attribute {repr(attr)}")
        if attr not in attrs:
            raise TypeError(f"attribute {repr(attr)} of 'Order' is unhashable")
        return dict(Counter(getattr(i, attr) for i in self.all_orders).most_common())

    def _cmp(self, order: Order, bins: str, chrono: bool = False):
        # TODO: include an option to groupby according to custom strftime string
        bin_ = tuple(attr for attr in bins.split("+") if attr)
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

    def slot_amount(self, bins: str = "year+month_+day"):
        chrono_binned = sorted(
            self.all_orders, key=lambda x: self._cmp(x, bins, chrono=True)
        )
        return {
            " ".join(str(i) for i in key): sum(order.order_total for order in list(val))
            for key, val in groupby(chrono_binned, lambda x: self._cmp(x, bins))
        }

    def slot_orders(self, bins: str = "year+month_+day"):
        chrono_binned = sorted(
            self.all_orders, key=lambda x: self._cmp(x, bins, chrono=True)
        )
        return {
            " ".join(str(i) for i in key): len(list(val))
            for key, val in groupby(chrono_binned, lambda x: self._cmp(x, bins))
        }

    def slot_punctuality(self):
        pass


class OfferAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy


class PaymentAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
