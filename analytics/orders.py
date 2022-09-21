from collections import Counter
from itertools import groupby

from swiggy import Swiggy
from swiggy.order import Offer, Order, Payment


class OrderAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_orders = self.swiggy.order()

    def group(self, attr: str):
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

    def tseries_amount(self, bins: str = "year+month_"):
        chrono_binned = sorted(
            self.all_orders, key=lambda x: self._cmp(x, bins, chrono=True)
        )
        return {
            " ".join(str(i) for i in key): sum(order.order_total for order in list(val))
            for key, val in groupby(chrono_binned, lambda x: self._cmp(x, bins))
        }

    def tseries_orders(self, bins: str = "year+month_"):
        chrono_binned = sorted(
            self.all_orders, key=lambda x: self._cmp(x, bins, chrono=True)
        )
        return {
            " ".join(str(i) for i in key): len(list(val))
            for key, val in groupby(chrono_binned, lambda x: self._cmp(x, bins))
        }

    def tseries_punctuality(self, bins: str = "year+month_"):
        chrono_binned = sorted(
            self.all_orders, key=lambda x: self._cmp(x, bins, chrono=True)
        )
        punctuality_dict = dict()
        for key, orders in groupby(chrono_binned, lambda x: self._cmp(x, bins)):
            # values of groupby() are exhausted once iterated over. thus making a copy
            orders_ = list(orders)
            punctuality_dict[" ".join(str(i) for i in key)] = {
                "on_time": sum(
                    1
                    for order in orders_
                    if not order.mCancellationTime and order.on_time is True
                ),
                "late": sum(
                    1
                    for order in orders_
                    if not order.mCancellationTime and order.on_time is False
                ),
                "max_delivery_time": max(
                    orders_, key=lambda x: x.actual_sla_time
                ).actual_sla_time,
                "min_delivery_time": min(
                    orders_,
                    key=lambda x: (x.mCancellationTime, x.actual_sla_time),
                ).actual_sla_time,
            }
        return punctuality_dict

    def tseries_distance(self, bins: str = "year+month_"):
        chrono_binned = sorted(
            self.all_orders, key=lambda x: self._cmp(x, bins, chrono=True)
        )
        distance_dict = dict()
        for key, orders in groupby(chrono_binned, lambda x: self._cmp(x, bins)):
            # values of groupby() are exhausted once iterated over. thus making a copy
            orders_ = list(orders)
            dist_travelled = round(
                sum(
                    order.restaurant.customer_distance[1]
                    for order in orders_
                    if not order.mCancellationTime
                ),
                4,
            )
            orders_placed = sum(1 for order in orders_ if not order.mCancellationTime)
            distance_dict[" ".join(str(i) for i in key)] = {
                "distance_covered": dist_travelled,
                "orders_placed": orders_placed,
                "distance_cov_per_order": round(dist_travelled / orders_placed, 4),
            }
        return distance_dict

    def tseries_furthest_order(self, bins: str = "week_"):
        chrono_binned = sorted(
            self.all_orders, key=lambda x: self._cmp(x, bins, chrono=True)
        )
        furthest_dict = dict()
        for key, orders in groupby(chrono_binned, lambda x: self._cmp(x, bins)):
            orders_ = list(orders)
            furthest = max(orders_, key=lambda x: x.restaurant.customer_distance[1])
            f_rest = furthest.restaurant
            furthest_dict[" ".join(str(i) for i in key)] = {
                "distance_covered": furthest.restaurant.customer_distance[1],
                "ordered from": f"{f_rest.name}, {f_rest.area_name}, {f_rest.city_name}",
                "items": [item.name for item in furthest.items],
                "delivered_by": furthest.delivery_boy["name"],
                "time_taken": f"{furthest.delivery_time_in_seconds/60:.2f} mins",
                "was_on_time": furthest.on_time,
            }
        return furthest_dict


class OfferAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy


class PaymentAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
