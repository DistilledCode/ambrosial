from swiggy.address import DeliveryAddress
from swiggy.order import OffersData, Order, Payment
from swiggy.orderitem import OrderItem
from swiggy.restaurant import Restaurant

attrs = {
    "order": list(Order.__annotations__),
    "order_items": list(OrderItem.__annotations__),
    "restaurant": ["restaurant_" + attr for attr in list(Restaurant.__annotations__)],
    "delivery_address": list(DeliveryAddress.__annotations__),
    "offers_data": list(OffersData.__annotations__),
    "payment": list(Payment.__annotations__),
}

attrs["order"].remove("restaurant")
attrs["order"].remove("payment_transaction")
attrs["order"].remove("offers_data")
attrs["order"].remove("order_items")
attrs["order"].remove("delivery_address")
attrs["order_items"].remove("order_id")
attrs["order_items"].remove("restaurant_id")
attrs["restaurant"].remove("restaurant_customer_distance")
attrs["restaurant"].remove("restaurant_coordinates")
attrs["offers_data"].remove("order_id")
attrs["offers_data"].remove("coupon_applied")


def order(_order: dict) -> list[Order]:
    return Order(
        **{attr: _order[attr] for attr in attrs["order"]},
        restaurant=restaurant(_order),
        payment_transaction=payment(_order),
        order_items=orderitem(_order),
        offers_data=offers_data(_order),
        delivery_address=deliveryaddress(_order),
    )


def orderitem(order: dict) -> list[OrderItem]:
    for item in order["order_items"]:
        for attr in attrs["order_items"]:
            item.setdefault(attr, None)
        if item["image_id"] is None or not item["image_id"]:
            item["image_id"] = "swiggy_pay/SwiggyLogo"
    return [
        OrderItem(
            **{attr: item[attr] for attr in attrs["order_items"]},
            order_id=order["order_id"],
            restaurant_id=order["restaurant_id"],
        )
        for item in order["order_items"]
    ]


def restaurant(order: dict) -> list[Restaurant]:
    return Restaurant(
        **{
            attr.replace("restaurant_", ""): order[attr] for attr in attrs["restaurant"]
        },
        coordinates=order["restaurant_lat_lng"],
        customer_distance=(
            float(order["restaurant_customer_distance"]),
            order["delivery_address"]["id"],
        ),
    )


def deliveryaddress(order: dict) -> list[DeliveryAddress]:
    return DeliveryAddress(
        **{attr: order["delivery_address"][attr] for attr in attrs["delivery_address"]}
    )


def payment(order: dict) -> list[Payment]:
    if not order["payment_transactions"]:
        return []
    return [
        Payment(**{attr: pay[attr] for attr in attrs["payment"]})
        for pay in order["payment_transactions"]
    ]


def offers_data(order: dict) -> list[OffersData]:
    if order["offers_data"] == "":
        return []
    return [
        OffersData(
            **{attr: offer[attr] for attr in attrs["offers_data"]},
            order_id=order["order_id"],
            coupon_applied=order["coupon_applied"],
        )
        for offer in order["offers_data"]
    ]
