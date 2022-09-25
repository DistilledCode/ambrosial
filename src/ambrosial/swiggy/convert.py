from ambrosial.swiggy.address import Address
from ambrosial.swiggy.item import Item
from ambrosial.swiggy.order import Offer, Order, Payment
from ambrosial.swiggy.restaurant import Restaurant

attrs = {
    "order": list(Order.__annotations__),
    "items": list(Item.__annotations__),
    "restaurant": ["restaurant_" + attr for attr in list(Restaurant.__annotations__)],
    "address": list(Address.__annotations__),
    "offers_data": list(Offer.__annotations__),
    "payment": list(Payment.__annotations__),
}

attrs["order"].remove("restaurant")
attrs["order"].remove("payment_transaction")
attrs["order"].remove("offers_data")
attrs["order"].remove("items")
attrs["order"].remove("address")
attrs["items"].remove("order_id")
attrs["items"].remove("restaurant_id")
attrs["restaurant"].remove("restaurant_customer_distance")
attrs["restaurant"].remove("restaurant_coordinates")
attrs["address"].remove("ddav")
attrs["offers_data"].remove("order_id")
attrs["offers_data"].remove("coupon_applied")


def order(_order: dict, ddav: bool) -> Order:
    return Order(
        **{attr: _order[attr] for attr in attrs["order"]},
        restaurant=restaurant(_order, ddav),
        payment_transaction=payment(_order),
        items=item(_order),
        offers_data=offer(_order),
        address=address(_order, ddav),
    )


def item(order: dict) -> list[Item]:
    for item in order["order_items"]:
        for attr in attrs["items"]:
            item.setdefault(attr, None)
        if item["image_id"] is None or not item["image_id"]:
            item["image_id"] = "swiggy_pay/SwiggyLogo"
    return [
        Item(
            **{attr: item[attr] for attr in attrs["items"]},
            order_id=order["order_id"],
            restaurant_id=order["restaurant_id"],
        )
        for item in order["order_items"]
    ]


def restaurant(order: dict, ddav: bool) -> Restaurant:
    address = order["delivery_address"]
    customer_distance = (
        f'{address["id"]}_{address["version"]}' if ddav else address["id"],
        float(order["restaurant_customer_distance"]),
    )
    return Restaurant(
        **{
            attr.replace("restaurant_", ""): order[attr] for attr in attrs["restaurant"]
        },
        coordinates=order["restaurant_lat_lng"],
        customer_distance=customer_distance,
    )


def address(order: dict, ddav: bool) -> Address:
    return Address(
        ddav=ddav,
        **{attr: order["delivery_address"][attr] for attr in attrs["address"]},
    )


def payment(order: dict) -> list[Payment]:
    if not order["payment_transactions"]:
        return []
    return [
        Payment(**{attr: pay[attr] for attr in attrs["payment"]})
        for pay in order["payment_transactions"]
    ]


def offer(order: dict) -> list[Offer]:
    if order["offers_data"] == "":
        return []
    return [
        Offer(
            **{attr: offer[attr] for attr in attrs["offers_data"]},
            order_id=order["order_id"],
            coupon_applied=order["coupon_applied"],
        )
        for offer in order["offers_data"]
    ]
