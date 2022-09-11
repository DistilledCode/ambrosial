import statistics as st
from collections import Counter, defaultdict
from typing import Union

from swiggy import Swiggy
from swiggy.address import DeliveryAddress
from swiggy.order import Order


class AddressAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_orders = self.swiggy.order()
        self.all_addresses = self.swiggy.deliveryaddress()

    def groupby(self, attr: str = None) -> dict[Union[DeliveryAddress, str], int]:
        if attr is None:
            return dict(Counter(self.all_addresses).most_common())
        return dict(Counter(getattr(i, attr) for i in self.all_addresses).most_common())

    def coordinates(self):
        return [
            {
                "id_version": f"{address.id}_{address.version}",
                "annotation": address.annotation,
                "latitude": address.lat,
                "longitude": address.lng,
            }
            for address in set(self.all_addresses)
        ]

    def _get_key(self, order: Order):
        return (
            f"{order.delivery_address.id}_{order.delivery_address.version}"
            if self.swiggy.ddav
            else order.delivery_address.id
        )

    def history(self):
        hist = defaultdict(list)
        for order in self.all_orders:
            hist[self._get_key(order)].append(
                {
                    "order_id": order.order_id,
                    "order_time": order.order_time,
                }
            )
        return dict(hist)

    def _conv_factor(self, unit: str) -> int:
        return {"minute": 60, "hour": 3600}.get(unit, 1)

    def del_time_stats(self, unit: str = "secs"):
        del_time = defaultdict(list)
        for order in self.all_orders:
            if (dt := order.delivery_time_in_seconds) != 0:
                del_time[self._get_key(order)].append(dt / self._conv_factor(unit))
        return dict(
            {
                address: {
                    "mean": round(st.mean(total_dt), 4),
                    "median": round(st.median(total_dt), 4),
                    "std_dev": round(st.stdev(total_dt), 4)
                    if len(total_dt) > 1
                    else None,
                    "maximum": round(max(total_dt), 4),
                    "minimum": round(min(total_dt), 4),
                    "total_deliveries": len(total_dt),
                }
                for address, total_dt in del_time.items()
            }
        )
