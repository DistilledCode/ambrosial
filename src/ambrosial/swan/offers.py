import statistics as st
from collections import Counter, defaultdict
from itertools import takewhile
from typing import Any, NoReturn, Optional

from ambrosial.swan.typealiases import ExtremeDiscount, OfferStatistics
from ambrosial.swiggy import Swiggy
from ambrosial.swiggy.datamodel.order import Offer


class OfferAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_offers = self.swiggy.get_offers()

    def group(self) -> NoReturn:
        raise NotImplementedError("Each offer is unique. Use Swiggy.get_offers()")

    def grouped_count(self, group_by: str) -> dict[str, int]:
        if group_by not in list(Offer.__annotations__):
            raise TypeError(f"type object 'Offer' has no attribute {repr(group_by)}")
        if group_by == "discount_share":
            raise NotImplementedError("use .statistics() instead")
        return dict(
            Counter(getattr(i, group_by) for i in self.all_offers).most_common()
        )

    def grouped_instances(self, key: str, attr: Optional[str] = None) -> dict[Any, Any]:
        group_dict = defaultdict(list)
        for offer in self.all_offers:
            if attr is not None:
                group_dict[getattr(offer, key)].append(getattr(offer, attr))
            else:
                group_dict[getattr(offer, key)].append(offer)
        return dict(group_dict)

    def statistics(self) -> OfferStatistics:
        discounts = [offer.total_offer_discount for offer in self.all_offers]
        sorted_offers = sorted(self.all_offers, key=lambda x: x.total_offer_discount)
        min_ = sorted_offers[0]
        max_ = sorted_offers[-1]
        min_discount_info = ExtremeDiscount(
            amount=round(min_.total_offer_discount, 3),
            coupon=f"{min_.coupon_applied}: {min_.description}",
            order_id=[
                offer.order_id
                for offer in takewhile(
                    lambda x: x.total_offer_discount <= min_.total_offer_discount,
                    sorted_offers,
                )
            ],
        )
        max_discount_info = ExtremeDiscount(
            amount=round(max_.total_offer_discount, 3),
            coupon=f"{max_.coupon_applied}: {max_.description}",
            order_id=[
                offer.order_id
                for offer in takewhile(
                    lambda x: x.total_offer_discount >= max_.total_offer_discount,
                    reversed(sorted_offers),
                )
            ],
        )
        return OfferStatistics(
            total_discount=round(sum(discounts), 3),
            discount_breakup=dict(
                sum(
                    [Counter(offer.discount_share) for offer in self.all_offers],
                    Counter(),
                )
            ),
            average_discount={
                "orders_w_offers": round(st.mean(discounts), 3),
                "all_orders": round(sum(discounts) / len(self.swiggy.get_orders()), 3),
            },
            mode_discount=st.multimode(discounts),
            median_discount=st.median(discounts),
            std_dev_discount=round(st.stdev(discounts), 4)
            if len(discounts) > 1
            else -1.0,
            minimum_discount=min_discount_info,
            maximum_discount=max_discount_info,
        )


class PaymentAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_payments = self.swiggy.get_payments()

    def group(self) -> NoReturn:
        raise NotImplementedError("Each payment is unique. Use Swiggy.get_payments()")

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
