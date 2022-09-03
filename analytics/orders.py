from swiggy.order import Offer, Order, Payment


class OrdersAnalytics:
    def __init__(self, orders: list[Order]) -> None:
        self.orders = orders
        pass

    pass


class OffersAnalytics:
    def __init__(self, offers: list[Offer]) -> None:
        self.offers = offers
        pass

    pass


class PaymentAnalytics:
    def __init__(self, payments: list[Payment]) -> None:
        self.payments = payments
        pass

    pass
