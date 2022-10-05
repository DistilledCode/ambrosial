from typing import Any, Union


def _order(
    order_list: list[dict[str, Any]],
    obj_id: Union[str, int],
) -> dict:
    for order in order_list:
        if order["order_id"] == obj_id:
            return order
    raise ValueError(f"order with id = {repr(obj_id)} doesn't exist.")


def _item(
    order_list: list[dict[str, Any]],
    obj_id: Union[str, int],
) -> dict:
    for order in order_list:
        for item in order["order_items"]:
            if item["item_id"] == obj_id:
                return order
    raise ValueError(f"order item with id = {repr(obj_id)} doesn't exist.")


def _restaurant(
    order_list: list[dict[str, Any]],
    obj_id: Union[str, int],
) -> dict:
    for order in order_list:
        if order["restaurant_id"] == obj_id:
            return order
    raise ValueError(f"restaurant with id = {repr(obj_id)} doesn't exist.")


def _address(
    order_list: list[dict[str, Any]],
    obj_id: Union[str, int],
    **kwargs: dict[str, Any],
) -> dict:
    ddav = kwargs["ddav"]
    ver = kwargs["ver"]
    for order in order_list:
        if all(
            (
                ddav is True,
                order["delivery_address"]["id"] == obj_id,
                order["delivery_address"]["version"] == ver,
            )
        ):
            return order
        if ddav is False and order["delivery_address"]["id"] == obj_id:
            return order
    raise ValueError(
        f"Address with (id,ver) = ({obj_id},{ver}) doesn't exist."
    ) if ddav else ValueError(f"Address with id = {obj_id} doesn't exist.")


def _payment(
    order_list: list[dict[str, Any]],
    obj_id: Union[str, int],
) -> dict:
    for order in order_list:
        if order["transactionId"] == obj_id:
            return order
    raise ValueError(f"payment with transaction id = {repr(obj_id)} doesn't exist.")


def _offer(
    order_list: list[dict[str, Any]],
    obj_id: Union[str, int],
) -> dict:
    for order in order_list:
        for offer in order["offers_data"]:
            if offer["id"] == obj_id:
                return order
    raise ValueError(f"Address with id = {repr(obj_id)} doesn't exist.")


def find_order(
    obj: str,
    order_list: list[dict[str, Any]],
    obj_id: Union[str, int],
    **kwargs: dict[str, Any],
) -> dict:

    if obj == "address":
        return _address(order_list, obj_id, **kwargs)

    obj_dict = {
        "order": _order,
        "item": _item,
        "restaurant": _restaurant,
        "payment": _payment,
        "offer": _offer,
    }
    return obj_dict[obj](order_list, obj_id)
