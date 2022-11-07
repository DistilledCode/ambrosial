from typing import Optional

from ambrosial.swan.addresses import AddressAnalytics
from ambrosial.swan.items import ItemAnalytics
from ambrosial.swan.offers import OfferAnalytics, PaymentAnalytics
from ambrosial.swan.orders import OrderAnalytics
from ambrosial.swan.restaurants import RestaurantAnalytics
from ambrosial.swiggy import Swiggy


class SwiggyAnalytics:
    def __init__(self, swiggy: Optional[Swiggy] = None) -> None:
        self.swiggy = Swiggy() if swiggy is None else swiggy
        if self.swiggy._fetched is False:
            self.swiggy.loadb()
        self.orders = OrderAnalytics(self.swiggy)
        self.offers = OfferAnalytics(self.swiggy)
        self.items = ItemAnalytics(self.swiggy)
        self.restaurants = RestaurantAnalytics(self.swiggy)
        self.addresses = AddressAnalytics(self.swiggy)
        self.payments = PaymentAnalytics(self.swiggy)

    def __repr__(self) -> str:
        return f"SwiggyAnalytics({self.swiggy})"
