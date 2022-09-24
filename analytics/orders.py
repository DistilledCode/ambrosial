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
        bin_ = set(attr for attr in bins.split("+") if attr)
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
        """
        Delivery charges are zero only when the order had free delivery (Swiggy Super)
        In that case check free_delivery_discount_hit attribute
        """
        crb = self._chronoligally_binned(bins)
        charges = (
            "GST",
            "Packing Charges",
            "Delivery Charges",
            "Cancellation Fee",
            "Service Charges",
            "Convenience Fee",
            "Service Tax",
            "Vat",
        )
        charges_dict = dict()
        for key, orders in groupby(crb, lambda x: self._cmp(x, bins)):
            orders_ = list(orders)
            charges_dict[" ".join(str(i) for i in key)] = {
                charge: round(sum(order.charges.get(charge) for order in orders_), 3)
                for charge in charges
            }
        return charges_dict

    def tseries_delivery_time(self, bins: str = "year+month_", unit: str = "minute"):
        conv = {"minute": 60, "hour": 3600}.get(unit, 1)
        crb = self._chronoligally_binned(bins)
        deltime_dict = dict()
        for key, orders in groupby(crb, lambda x: self._cmp(x, bins)):
            orders_ = list(orders)
            deltime = [
                order.delivery_time_in_seconds / conv
                for order in orders_
                if order.delivery_time_in_seconds != 0
            ]
            sla_time = [
                order.sla_time
                for order in orders_
                if order.delivery_time_in_seconds != 0
            ]
            max_time = max(orders_, key=lambda x: x.delivery_time_in_seconds)
            min_time = min(
                orders_, key=lambda x: (x.mCancellationTime, x.delivery_time_in_seconds)
            )
            deltime_dict[" ".join(str(i) for i in key)] = {
                "deliveries": len(deltime),
                "mean_promised": round(st.mean(sla_time), 4),
                "mean_actual": round(st.mean(deltime), 4),
                "median": round(st.median(deltime), 4),
                "std_dev": round(st.stdev(deltime), 4) if len(deltime) > 1 else None,
                "maximum": {
                    "promsied": max_time.sla_time,
                    "actual": round(max_time.delivery_time_in_seconds / conv, 4),
                    "order_id": max_time.order_id,
                    "distance": max_time.restaurant.customer_distance[1],
                },
                "minimum": {
                    "promsied": min_time.sla_time,
                    "actual": round(min_time.delivery_time_in_seconds / conv, 4),
                    "order_id": min_time.order_id,
                    "distance": min_time.restaurant.customer_distance[1],
                },
            }
        return deltime_dict

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
            dist_travelled = sum(
                order.restaurant.customer_distance[1]
                for order in orders_
                if not order.mCancellationTime
            )
            orders_placed = sum(1 for order in orders_ if not order.mCancellationTime)
            distance_dict[" ".join(str(i) for i in key)] = {
                "distance_covered": round(dist_travelled, 4),
                "orders_placed": orders_placed,
                "distance_cov_per_order": round(dist_travelled / orders_placed, 4),
            }
        return distance_dict

    def tseries_super_benefits(self, bins: str = "year+month_"):
        """
        there are cases when free_delivery_discount > 0 but super_specific_discount = 0
        this happened in Oct 2021 and Nov 2021
        therefore recommended to only use free_delivery_discount
        trade_discount includes extra % discounts offered in Super
        trade_discount_effective include tracde_discount plus cost of freebies
        """
        crb = self._chronoligally_binned(bins)
        free_delivery_breakup = ("thresholdFee", "distanceFee", "timeFee", "specialFee")
        super_benefit = dict()
        for key, orders in groupby(crb, lambda x: self._cmp(x, bins)):
            orders_ = list(orders)
            free_deliveries = sum(order.free_delivery_discount_hit for order in orders_)
            other_benefits = sum(order.trade_discount for order in orders_)
            super_benefit[" ".join(str(i) for i in key)] = {
                "total_benefit": round(free_deliveries + other_benefits, 3),
                "other_super_discount": round(other_benefits, 3),
                "free_deliveries": {
                    "total_amount": round(free_deliveries, 3),
                    "break_up": {
                        type_: round(
                            sum(
                                order.free_del_break_up.get(type_) for order in orders_
                            ),
                            3,
                        )
                        for type_ in free_delivery_breakup
                    },
                },
            }
        return super_benefit

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
        disc_types = ("swiggy_discount", "store_discount", "alliance_discount")
        discounts = [offer.total_offer_discount for offer in self.all_offers]
        sorted_offers = sorted(self.all_offers, key=lambda x: x.total_offer_discount)
        min_ = sorted_offers[0]
        max_ = sorted_offers[-1]
        return {
            "total_discount": round(sum(discounts), 3),
            "discount_breakup": {
                attr: round(sum(i.discount_share.get(attr) for i in self.all_offers), 3)
                for attr in disc_types
            },
            "average_discount": {
                "orders_w_offers": round(st.mean(discounts), 3),
                "all_orders": round(sum(discounts) / len(self.swiggy.order()), 3),
            },
            "std_dev_discount": round(st.stdev(discounts), 4)
            if len(discounts) > 1
            else None,
            "minimum_discount": {
                "amount": round(min_.total_offer_discount, 3),
                "coupon": f"{min_.coupon_applied}: {min_.description}",
                "order_id": [
                    offer.order_id
                    for offer in takewhile(
                        lambda x: x.total_offer_discount <= min_.total_offer_discount,
                        sorted_offers,
                    )
                ],
            },
            "maximum_discount": {
                "amount": round(max_.total_offer_discount, 3),
                "coupon": f"{max_.coupon_applied}: {max_.description}",
                "order_id": [
                    offer.order_id
                    for offer in takewhile(
                        lambda x: x.total_offer_discount >= max_.total_offer_discount,
                        reversed(sorted_offers),
                    )
                ],
            },
            "mode_discount": st.multimode(discounts),
        }


class PaymentAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
