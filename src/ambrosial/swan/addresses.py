import statistics as st
from collections import Counter, defaultdict
from typing import Union

from ambrosial.swiggy import Swiggy
from ambrosial.swiggy.address import Address
from ambrosial.swiggy.order import Order


class AddressAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy: Swiggy = swiggy
        self.all_orders: list[Order] = self.swiggy.get_orders()
        self.all_addresses: list[Address] = self.swiggy.get_addresses()

    def group(self, attr: str = None) -> dict[Union[Address, str], int]:
        if attr is None:
            return dict(Counter(self.all_addresses).most_common())
        return dict(Counter(getattr(i, attr) for i in self.all_addresses).most_common())

    def coordinates(self) -> list[dict]:
        return [
            {
                "id_version": f"{address.id}_{address.version}",
                "annotation": address.annotation,
                "latitude": address.lat,
                "longitude": address.lng,
            }
            for address in set(self.all_addresses)
        ]

    def order_history(self) -> dict:
        hist = defaultdict(list)
        for order in self.all_orders:
            hist[self._get_key(order)].append(
                {
                    "order_id": order.order_id,
                    "order_time": order.order_time,
                }
            )
        return dict(hist)

    def delivery_time_stats(self, unit: str = "minute") -> dict:
        delivery_time = defaultdict(list)
        for order in self.all_orders:
            if (dt := order.delivery_time_in_seconds) != 0:
                delivery_time[self._get_key(order)].append(dt / self._conv_factor(unit))
        return {
            address: {
                "mean": round(st.mean(total_dt), 4),
                "median": round(st.median(total_dt), 4),
                "std_dev": round(st.stdev(total_dt), 4) if len(total_dt) > 1 else None,
                "maximum": round(max(total_dt), 4),
                "minimum": round(min(total_dt), 4),
                "total_deliveries": len(total_dt),
            }
            for address, total_dt in delivery_time.items()
        }

    def _get_key(self, order: Order) -> str:
        return (
            f"{order.address.id}_{order.address.version}"
            if self.swiggy.ddav
            else order.address.id
        )

    def _conv_factor(self, unit: str) -> int:
        return {"minute": 60, "hour": 3600}.get(unit, 1)