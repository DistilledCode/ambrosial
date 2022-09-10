from swiggy import Swiggy

from analytics.addresses import AddressAnalytics
from analytics.orderitems import OrderitemAnalytics
from analytics.orders import OfferAnalytics, OrderAnalytics, PaymentAnalytics
from analytics.restaurants import RestaurantsAnalytics


class SwiggyAnalytics:
    def __init__(self, swiggy: Swiggy = None) -> None:
        self.swiggy = swiggy
        if self.swiggy is None:
            self.swiggy = Swiggy()
            self.swiggy.fetchall()
        elif self.swiggy._fetched is False:
            self.swiggy.fetchall()
        self.orders = OrderAnalytics(swiggy)
        self.offers = OfferAnalytics(swiggy)
        self.orderitems = OrderitemAnalytics(swiggy)
        self.restaurants = RestaurantsAnalytics(swiggy)
        self.addresses = AddressAnalytics(swiggy)
        self.payments = PaymentAnalytics(swiggy)
