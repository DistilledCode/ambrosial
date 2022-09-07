from collections import Counter

from swiggy import Swiggy


class SwiggyAnalytics:
    def __init__(self, swiggy: Swiggy = None) -> None:
        self.swiggy = swiggy
        if self.swiggy is None:
            self.swiggy = Swiggy()
            self.swiggy.fetchall()
        if self.swiggy._fetched is False:
            self.swiggy.fetchall()
        self.orders = self.swiggy.order()
        self.orderitems = self.swiggy.orderitem()
        self.restaurants = self.swiggy.restaurant()
        self.addresses = self.swiggy.deliveryaddress()
        self.payments = self.swiggy.payment()
        self.offers = self.swiggy.offer()

    # def most_common(self):
    #     return {
    #         "restaurant": Counter(self.restaurants).most_common(),
    #         "orderitem": Counter(self.orderitems).most_common(),
    #         "address": Counter(self.addresses).most_common(),
    #     }
