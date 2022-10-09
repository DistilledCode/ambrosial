from ambrosial.swiggy.datamodel.address import Address
from ambrosial.swiggy.datamodel.item import Item
from ambrosial.swiggy.datamodel.order import Offer, Order, Payment
from ambrosial.swiggy.datamodel.restaurant import Restaurant
from ambrosial.swiggy.utils import SwiggyOrderDict

URL = "https://res.cloudinary.com/swiggy/image/upload/"
ATTRS = {
    "order": list(Order.__annotations__),
    "items": list(Item.__annotations__),
    "restaurant": ["restaurant_" + attr for attr in list(Restaurant.__annotations__)],
    "address": list(Address.__annotations__),
    "offers_data": list(Offer.__annotations__),
    "payment": list(Payment.__annotations__),
}

ATTRS["order"].remove("restaurant")
ATTRS["order"].remove("payment_transaction")
ATTRS["order"].remove("offers_data")
ATTRS["order"].remove("items")
ATTRS["order"].remove("address")
ATTRS["order"].remove("on_time")
ATTRS["items"].remove("order_id")
ATTRS["items"].remove("restaurant_id")
ATTRS["items"].remove("image")
ATTRS["restaurant"].remove("restaurant_customer_distance")
ATTRS["restaurant"].remove("restaurant_coordinates")
ATTRS["restaurant"].remove("restaurant_cover_image")
ATTRS["restaurant"].remove("restaurant_rest_id")
ATTRS["restaurant"].remove("restaurant_rest_type")
ATTRS["address"].remove("ddav")
ATTRS["address"].remove("address_id")
ATTRS["offers_data"].remove("order_id")
ATTRS["offers_data"].remove("coupon_applied")
ATTRS["payment"].remove("order_id")


def order(_order: SwiggyOrderDict, ddav: bool) -> Order:
    return Order(
        **{attr: _order.get(attr, None) for attr in ATTRS["order"]},
        restaurant=restaurant(_order, ddav),
        payment_transaction=payment(_order),
        items=item(_order),
        offers_data=offer(_order),
        address=address(_order, ddav),
        on_time=int(_order["sla_difference"]) >= 0,
    )


def item(order: SwiggyOrderDict) -> list[Item]:
    for item in order["order_items"]:
        if not item["free_item_quantity"]:
            item["free_item_quantity"] = 0
        if item["image_id"] is None or not item["image_id"]:
            item["image_id"] = "swiggy_pay/SwiggyLogo"
    return [
        Item(
            **{attr: item.get(attr, None) for attr in ATTRS["items"]},
            image=URL + item["image_id"],
            order_id=order["order_id"],
            restaurant_id=order["restaurant_id"],
        )
        for item in order["order_items"]
    ]


def restaurant(order: dict, ddav: bool) -> Restaurant:
    address = order["delivery_address"]
    address_id = f'{address["id"]}_{address["version"]}' if ddav else address["id"]
    customer_distance = (address_id, order["restaurant_customer_distance"])
    lat_lng = order["restaurant_lat_lng"].split(",")
    coordinates = {
        "lat": lat_lng[0],
        "lng": lat_lng[1],
    }
    return Restaurant(
        **{
            attr.replace("restaurant_", ""): order.get(attr, None)
            for attr in ATTRS["restaurant"]
        },
        rest_id=order["restaurant_id"],
        rest_type=order["restaurant_type"],
        coordinates=coordinates,
        customer_distance=customer_distance,
        cover_image=URL + order["restaurant_cover_image"],
    )


def address(order: SwiggyOrderDict, ddav: bool) -> Address:
    return Address(
        ddav=ddav,
        **{
            attr: order["delivery_address"].get(attr, None) for attr in ATTRS["address"]
        },
        address_id=order["delivery_address"]["id"],
    )


def payment(order: SwiggyOrderDict) -> list[Payment]:
    if not order["payment_transactions"]:
        return []
    return [
        Payment(
            **{attr: pay.get(attr, None) for attr in ATTRS["payment"]},
            order_id=order["order_id"],
        )
        for pay in order["payment_transactions"]
    ]


def offer(order: SwiggyOrderDict) -> list[Offer]:
    if order["offers_data"] == "":
        return []
    return [
        Offer(
            **{attr: offer.get(attr, None) for attr in ATTRS["offers_data"]},
            order_id=order["order_id"],
            coupon_applied=order["coupon_applied"],
        )
        for offer in order["offers_data"]
    ]
