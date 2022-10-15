import statistics as st
from collections import Counter, defaultdict
from itertools import takewhile
from typing import Any, NoReturn, Optional, Union

from ambrosial.swiggy import Swiggy
from ambrosial.swiggy.datamodel.order import Offer


class OfferAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_offers = self.swiggy.get_offers()

    def group(self) -> NoReturn:
        raise NotImplementedError("Each offer is unique. Same as Swiggy.get_offers()")

    def group_by(self, attr: str) -> dict[str, int]:
        if attr not in list(Offer.__annotations__):
            raise TypeError(f"type object 'Offer' has no attribute {repr(attr)}")
        if attr == "discount_share":
            raise NotImplementedError("use .statistics() instead")
        return dict(Counter(getattr(i, attr) for i in self.all_offers).most_common())

    def grouped_instances(self, key: str, attr: Optional[str] = None) -> dict[Any, Any]:
        group_dict = defaultdict(list)
        for offer in self.all_offers:
            if attr is not None:
                group_dict[getattr(offer, key)].append(getattr(offer, attr))
            else:
                group_dict[getattr(offer, key)].append(offer)
        return dict(group_dict)

    def statistics(self) -> dict[str, Union[int, float, dict, list[float]]]:
        discounts = [offer.total_offer_discount for offer in self.all_offers]
        sorted_offers = sorted(self.all_offers, key=lambda x: x.total_offer_discount)
        min_ = sorted_offers[0]
        max_ = sorted_offers[-1]
        return {
            "total_discount": round(sum(discounts), 3),
            "discount_breakup": dict(
                sum(
                    [Counter(offer.discount_share) for offer in self.all_offers],
                    Counter(),
                )
            ),
            "average_discount": {
                "orders_w_offers": round(st.mean(discounts), 3),
                "all_orders": round(sum(discounts) / len(self.swiggy.get_orders()), 3),
            },
            "std_dev_discount": round(st.stdev(discounts), 4)
            if len(discounts) > 1
            else -1,
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
        self.all_payments = self.swiggy.get_payments()

    def group_by(self, attr: str) -> dict[str, int]:
        return dict(Counter(getattr(i, attr) for i in self.all_payments).most_common())

    def grouped_instances(self, key: str, attr: Optional[str] = None) -> dict[Any, Any]:
        group_dict = defaultdict(list)
        for payment in self.all_payments:
            if attr is not None:
                group_dict[getattr(payment, key)].append(getattr(payment, attr))
            else:
                group_dict[getattr(payment, key)].append(payment)
        return dict(group_dict)
