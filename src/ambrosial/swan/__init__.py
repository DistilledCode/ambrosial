from ambrosial.swan.addresses import AddressAnalytics
from ambrosial.swan.items import ItemAnalytics
from ambrosial.swan.orders import OfferAnalytics, OrderAnalytics, PaymentAnalytics
from ambrosial.swan.restaurants import RestaurantAnalytics
from ambrosial.swiggy import Swiggy


class SwiggyAnalytics:
    def __init__(self, swiggy: Swiggy = None) -> None:
        self.swiggy = swiggy
        if self.swiggy is None:
            self.swiggy = Swiggy()
            self.swiggy.fetchall()
        elif self.swiggy._fetched is False:
            self.swiggy.fetchall()
        self.orders = OrderAnalytics(self.swiggy)
        self.offers = OfferAnalytics(self.swiggy)
        self.items = ItemAnalytics(self.swiggy)
        self.restaurants = RestaurantAnalytics(self.swiggy)
        self.addresses = AddressAnalytics(self.swiggy)
        self.payments = PaymentAnalytics(self.swiggy)

    def __repr__(self) -> str:
        return f"SwiggyAnalytics({self.swiggy})"
