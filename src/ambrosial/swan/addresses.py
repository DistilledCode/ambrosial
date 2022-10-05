import statistics as st
from collections import Counter, defaultdict

from ambrosial.swiggy import Swiggy
from ambrosial.swiggy.datamodel.address import Address
from ambrosial.swiggy.datamodel.order import Order


class AddressAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy: Swiggy = swiggy
        self.all_orders: list[Order] = self.swiggy.get_orders()
        self.all_addresses: list[Address] = self.swiggy.get_addresses()

    def group(self) -> dict[Address, int]:
        return dict(Counter(self.all_addresses).most_common())

    def group_by(self, attr: str) -> dict[str, int]:
        return dict(Counter(getattr(i, attr) for i in self.all_addresses).most_common())

    def coordinates(self) -> list[dict]:
        return [
            {
                "id_version": f"{address.add_id}_{address.version}",
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
        return str(
            f"{order.address.add_id}_{order.address.version}"
            if self.swiggy.ddav
            else order.address.add_id  # because add_id is int
        )

    def _conv_factor(self, unit: str) -> int:
        return {"minute": 60, "hour": 3600}.get(unit, 1)
