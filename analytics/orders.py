import statistics as st
from collections import Counter
from itertools import groupby, takewhile

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

    def _chronoligally_binned(self, bins: str):
        return sorted(self.all_orders, key=lambda x: self._cmp(x, bins, chrono=True))

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
            # else keys will be sorted in alphabetical order instead of chronological
            attr_mapping["month_"] = attr_mapping["month"]
            attr_mapping["week_"] = attr_mapping["week"]

        return tuple(attr_mapping.get(attr) for attr in bin_)

    def tseries_amount(self, bins: str = "year+month_"):
        crb = self._chronoligally_binned(bins)
        return {
            " ".join(str(i) for i in key): sum(order.order_total for order in list(val))
            for key, val in groupby(crb, lambda x: self._cmp(x, bins))
        }

    def tseries_orders(self, bins: str = "year+month_"):
        crb = self._chronoligally_binned(bins)
        return {
            " ".join(str(i) for i in key): len(list(val))
            for key, val in groupby(crb, lambda x: self._cmp(x, bins))
        }

    def tseries_charges(self, bins: str = "year+month_"):
        crb = self._chronoligally_binned(bins)
        charges = list(self.all_orders[0].charges.keys())
        charges_dict = dict()
        for key, orders in groupby(crb, lambda x: self._cmp(x, bins)):
            orders_ = list(orders)
            charges_dict[" ".join(str(i) for i in key)] = {
                charge: round(sum(order.charges.get(charge) for order in orders_), 3)
                for charge in charges
            }
        return charges_dict

    def tseries_punctuality(self, bins: str = "year+month_"):
        crb = self._chronoligally_binned(bins)
        punctuality_dict = dict()
        for key, orders in groupby(crb, lambda x: self._cmp(x, bins)):
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
        crb = self._chronoligally_binned(bins)
        distance_dict = dict()
        for key, orders in groupby(crb, lambda x: self._cmp(x, bins)):
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
        crb = self._chronoligally_binned(bins)
        furthest_dict = dict()
        for key, orders in groupby(crb, lambda x: self._cmp(x, bins)):
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
        self.all_offers = self.swiggy.offer()

    def group(self, attr: str):
        if attr not in list(Offer.__annotations__):
            raise TypeError(f"type object 'Offer' has no attribute {repr(attr)}")
        if attr == "discount_share":
            raise NotImplementedError("use .statistics() instead")
        return dict(Counter(getattr(i, attr) for i in self.all_offers).most_common())

    def statistics(self):
        _disc_types = ("swiggy_discount", "store_discount", "alliance_discount")
        _discounts = [offer.total_offer_discount for offer in self.all_offers]
        _sorted_offers = sorted(self.all_offers, key=lambda x: x.total_offer_discount)
        _min_discount = _sorted_offers[0]
        _max_discount = _sorted_offers[-1]
        return {
            "overall_total_discount": round(sum(_discounts), 3),
            "discount_breakup": {
                attr: round(sum(i.discount_share.get(attr) for i in self.all_offers), 3)
                for attr in _disc_types
            },
            "average_discount": {
                "orders_w_offers": round(st.mean(_discounts), 3),
                "all_orders": round(sum(_discounts) / len(self.swiggy.order()), 3),
            },
            "minimum_discount": {
                "amount": round(_min_discount.total_offer_discount, 3),
                "coupon": f"{_min_discount.coupon_applied}: {_min_discount.description}",
                "order_id": [
                    offer.order_id
                    for offer in takewhile(
                        lambda x: x.total_offer_discount
                        <= _min_discount.total_offer_discount,
                        _sorted_offers,
                    )
                ],
            },
            "maximum_discount": {
                "amount": round(_max_discount.total_offer_discount, 3),
                "coupon": f"{_max_discount.coupon_applied}: {_max_discount.description}",
                "order_id": [
                    offer.order_id
                    for offer in takewhile(
                        lambda x: x.total_offer_discount
                        >= _max_discount.total_offer_discount,
                        reversed(_sorted_offers),
                    )
                ],
            },
            "mode_discount": st.multimode(_discounts),
        }


class PaymentAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
