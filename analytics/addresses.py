from collections import Counter
from typing import Union

from swiggy import Swiggy
from swiggy.address import DeliveryAddress

from analytics import SwiggyAnalytics


class AddressAnalytics(SwiggyAnalytics):
    def __init__(self, swiggy: Swiggy = None) -> None:
        SwiggyAnalytics.__init__(self, swiggy)

    def most_common(self, attr: str = None) -> dict[Union[DeliveryAddress, str], int]:
        if attr is None:
            return dict(Counter(self.addresses).most_common())
        return dict(Counter(getattr(i, attr) for i in self.addresses).most_common())
