import statistics as st
from collections import Counter, defaultdict
from itertools import groupby
from typing import Any, NoReturn, Optional

import ambrosial.swan.typealiases as alias
from ambrosial.swiggy import Swiggy
from ambrosial.swiggy.datamodel.order import Order
from ambrosial.swiggy.datamodel.typealiases import OrderTypeHint


class OrderAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_orders: list[Order] = self.swiggy.get_orders()

    def group(self) -> NoReturn:
        raise NotImplementedError("Each order is unique. Same as Swiggy.get_orders()")

    def group_by(self, attr: str) -> dict[str, int]:
        return dict(Counter(getattr(i, attr) for i in self.all_orders).most_common())

    def grouped_instances(self, key: str, attr: Optional[str] = None) -> dict[Any, Any]:
        special = ("items", "offers_data", "payment_transaction")
        if key in special:
            return self._packed_instances(key=key, attr=attr)
        group_dict = defaultdict(list)
        for order in self.all_orders:
            if attr is not None:
                group_dict[getattr(order, key)].append(getattr(order, attr))
            else:
                group_dict[getattr(order, key)].append(order)
        return dict(group_dict)

    def _packed_instances(self, key: str, attr: Optional[str]) -> dict[Any, Any]:
        group_dict = defaultdict(list)
        for order in self.all_orders:
            for unpacked in getattr(order, key):
                if attr is not None:
                    group_dict[unpacked].append(getattr(order, attr))
                else:
                    group_dict[unpacked].append(order)
        return dict(group_dict)

    def tseries_amount(self, bins: str = "year+month_") -> dict[str, int]:
        crb = self._chronoligally_binned(bins)
        return {
            " ".join(str(i).rjust(2, "0") for i in key): sum(
                order.order_total for order in list(val)
            )
            for key, val in groupby(crb, lambda x: self._cmp(x, bins))
        }

    def tseries_orders(self, bins: str = "year+month_") -> dict[str, int]:
        crb = self._chronoligally_binned(bins)
        return {
            " ".join(str(i).rjust(2, "0") for i in key): len(list(val))
            for key, val in groupby(crb, lambda x: self._cmp(x, bins))
        }

    def tseries_charges(
        self, bins: str = "year+month_"
    ) -> dict[str, OrderTypeHint.CHARGES]:
        """
        Delivery charges are zero only when the order had free delivery (Swiggy Super)
        In that case check free_delivery_discount_hit attribute
        """
        crb = self._chronoligally_binned(bins)
        return {
            " ".join(str(i).rjust(2, "0") for i in key): dict(
                sum(
                    [Counter(order.charges) for order in orders],
                    Counter(),
                )
            )
            for key, orders in groupby(crb, lambda x: self._cmp(x, bins))
        }

    def tseries_del_time(
        self,
        bins: str = "year+month_",
        unit: str = "minute",
    ) -> dict[str, alias.DelTime]:
        conv = {"minute": 60, "hour": 3600}.get(unit, 1)
        crb = self._chronoligally_binned(bins)
        deltime_dict = {}
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
            deltime_dict[" ".join(str(i).rjust(2, "0") for i in key)] = alias.DelTime(
                deliveries=len(deltime),
                mean_promised=round(st.mean(sla_time), 4),
                mean_actual=round(st.mean(deltime), 4),
                median=round(st.median(deltime), 4),
                std_dev=round(st.stdev(deltime), 4) if len(deltime) > 1 else -1,
                maximum=alias.DelTimeExtreme(
                    promised=max_time.sla_time,
                    actual=round(max_time.delivery_time_in_seconds / conv, 4),
                    order_id=max_time.order_id,
                    distance=max_time.restaurant.customer_distance[1],
                ),
                minimum=alias.DelTimeExtreme(
                    promised=min_time.sla_time,
                    actual=round(min_time.delivery_time_in_seconds / conv, 4),
                    order_id=min_time.order_id,
                    distance=min_time.restaurant.customer_distance[1],
                ),
            )
        return deltime_dict

    def tseries_punctuality(
        self, bins: str = "year+month_"
    ) -> dict[str, alias.Punctuality]:
        crb = self._chronoligally_binned(bins)
        return {
            " ".join(
                str(i).rjust(2, "0") for i in key
            ): self._get_order_punctuality_details(list(orders))
            for key, orders in groupby(crb, lambda x: self._cmp(x, bins))
        }

    def tseries_distance(self, bins: str = "year+month_") -> dict[str, alias.Distance]:
        crb = self._chronoligally_binned(bins)
        distance_dict = {}
        for key, orders in groupby(crb, lambda x: self._cmp(x, bins)):
            orders_ = list(orders)
            dist_travelled: float = 0.0
            orders_placed = 0
            for order in orders_:
                if order.mCancellationTime:
                    continue
                dist_travelled += order.restaurant.customer_distance[1]
                orders_placed += 1
            distance_dict[" ".join(str(i).rjust(2, "0") for i in key)] = alias.Distance(
                distance_covered=round(dist_travelled, 4),
                orders_placed=orders_placed,
                distance_covered_per_order=round(dist_travelled / orders_placed, 4),
            )
        return distance_dict

    def tseries_super_benefits(
        self,
        bins: str = "year+month_",
    ) -> dict[str, alias.SuperBenefits]:
        crb = self._chronoligally_binned(bins)
        return {
            " ".join(
                str(i).rjust(2, "0") for i in key
            ): self._get_super_benefits_detail(list(orders))
            for key, orders in groupby(crb, lambda x: self._cmp(x, bins))
        }

    def _get_super_benefits_detail(
        self,
        orders: list[Order],
    ) -> alias.SuperBenefits:
        free_deliveries = 0
        other_benefits: float = 0.0
        fd_break_up: Counter = Counter()
        for order in orders:
            free_deliveries += order.free_delivery_discount_hit
            other_benefits += order.trade_discount
            fd_break_up += Counter(order.free_del_break_up)

        return alias.SuperBenefits(
            total_benefit=round(free_deliveries + other_benefits, 3),
            other_super_discount=round(other_benefits, 3),
            free_deliveries=alias.FreeDeliveries(
                total_amount=free_deliveries,
                break_up=dict(fd_break_up),
            ),
        )

    def tseries_furthest_order(
        self,
        bins: str = "week_",
    ) -> dict[str, alias.FurthestOrder]:
        crb = self._chronoligally_binned(bins)
        furthest_dict = {}
        for key, orders in groupby(crb, lambda x: self._cmp(x, bins)):
            orders_ = list(orders)
            furthest = max(orders_, key=lambda x: x.restaurant.customer_distance[1])
            f_rest = furthest.restaurant
            furthest_dict[
                " ".join(str(i).rjust(2, "0") for i in key)
            ] = alias.FurthestOrder(
                distance_covered=furthest.restaurant.customer_distance[1],
                restaurant=f"{f_rest.name}, {f_rest.area_name}, {f_rest.city_name}",
                items=[item.name for item in furthest.items],
                delivered_by=str(furthest.delivery_boy["name"]),
                time_taken=f"{furthest.delivery_time_in_seconds/60:.2f} mins",
                was_on_time=furthest.on_time,
            )
        return furthest_dict

    def _chronoligally_binned(self, bins: str) -> list[Order]:
        return sorted(self.all_orders, key=lambda x: self._cmp(x, bins, chrono=True))

    def _get_order_punctuality_details(
        self,
        orders: list[Order],
    ) -> alias.Punctuality:
        on_time = 0
        late = 0
        max_time = 0
        min_time = 24 * 60  # one day
        for order in orders:
            if order.mCancellationTime:
                continue
            if order.on_time:
                on_time += 1
            else:
                late += 1
            actual_time = order.actual_sla_time
            max_time = max(max_time, actual_time)
            min_time = min(min_time, actual_time)
        return alias.Punctuality(
            on_time=on_time,
            late=late,
            max_delivery_time=max_time,
            min_delivery_time=min_time,
        )

    def _cmp(self, order: Order, bins: str, chrono: bool = False) -> tuple:
        # TODO: include an option to groupby according to custom strftime string
        bin_ = [attr for attr in bins.split("+") if attr]
        # cannot use set() as it doesnot preserve order
        bin_ = list(dict.fromkeys(bin_))
        attr_mapping = {
            "hour": order.order_time.hour,
            "day": order.order_time.day,
            "week": order.order_time.isoweekday(),
            "week_": order.order_time.strftime("%A"),
            "calweek": order.order_time.isocalendar().week,
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
