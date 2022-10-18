from typing import Literal, Optional, Union

from ambrosial.swiggy.utils import SwiggyOrderDict


def _order(
    order_list: list[SwiggyOrderDict],
    obj_id: Union[str, int],
) -> SwiggyOrderDict:
    for order in order_list:
        if order["order_id"] == int(obj_id):
            return order
    raise ValueError(f"order with id = {repr(obj_id)} doesn't exist.")


def _item(
    order_list: list[SwiggyOrderDict],
    obj_id: Union[str, int],
) -> SwiggyOrderDict:
    for order in order_list:
        for item in order["order_items"]:
            if item["item_id"] == str(obj_id):
                return order
    raise ValueError(f"order item with id = {repr(obj_id)} doesn't exist.")


def _restaurant(
    order_list: list[SwiggyOrderDict],
    obj_id: Union[str, int],
) -> SwiggyOrderDict:
    for order in order_list:
        if order["restaurant_id"] == str(obj_id):
            return order
    raise ValueError(f"restaurant with id = {repr(obj_id)} doesn't exist.")


def _address(
    order_list: list[SwiggyOrderDict],
    obj_id: Union[str, int],
    **kwargs: Union[Optional[int], bool],
) -> SwiggyOrderDict:
    ddav = kwargs["ddav"]
    ver = kwargs["ver"]
    for order in order_list:
        if all(
            (
                ddav is True,
                order["delivery_address"]["id"] == str(obj_id),
                order["delivery_address"]["version"] == ver,
            )
        ):
            return order
        if ddav is False and order["delivery_address"]["id"] == str(obj_id):
            return order
    raise ValueError(
        f"Address with (id,ver) = ({repr(obj_id)},{repr(ver)}) doesn't exist."
    ) if ddav else ValueError(f"Address with id = {repr(obj_id)} doesn't exist.")


def _payment(
    order_list: list[SwiggyOrderDict],
    obj_id: Union[str, int],
) -> SwiggyOrderDict:
    for order in order_list:
        for payment in order["payment_transactions"]:
            if payment["transactionId"] == str(obj_id):
                return order
    raise ValueError(f"Payment with transaction id = {repr(obj_id)} doesn't exist.")


def find_order(
    obj: Literal["order", "item", "restaurant", "payment", "offer", "address"],
    order_list: list[SwiggyOrderDict],
    obj_id: Union[str, int],
    **kwargs: Union[Optional[int], bool],
) -> SwiggyOrderDict:

    if obj == "address":
        return _address(order_list, obj_id, **kwargs)

    obj_dict = {
        "order": _order,
        "item": _item,
        "restaurant": _restaurant,
        "payment": _payment,
        "offer": _order,
    }
    return obj_dict[obj](order_list, obj_id)
