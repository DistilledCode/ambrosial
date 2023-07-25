from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich import SwiggyChart
from ambrosial.swiggy import Swiggy
from ambrosial.swiggy.datamodel.order import Order
from ambrosial.swiggy.datamodel.restaurant import Restaurant

swiggy = Swiggy(ddav=True)
swiggy.loadj()
swan = SwiggyAnalytics(swiggy)
swich = SwiggyChart(swan)


def test_associated_order():
    total_result = 0
    for restaurant in set(swiggy.get_restaurants()):
        result = swan.restaurants.associated_orders(restaurant_id=restaurant.rest_id)
        assert result.__class__ is list
        assert len(result) > 0
        assert all(order.__class__ is Order for order in result)
        total_result += len(result)
        assert all(order.restaurant == restaurant for order in result)
    assert total_result == len(swiggy.get_orders())


def test_swan_restaurants():
    hashable_attr = [
        attr
        for attr, atype in Restaurant.__annotations__.items()
        if atype.__hash__ is not None
    ]
    swan.restaurants.group()
    for attr in hashable_attr:
        swan.restaurants.grouped_count(attr)
        swan.restaurants.grouped_instances(key=attr)
        for attr2 in Restaurant.__annotations__:
            swan.restaurants.grouped_instances(key=attr, attr=attr2)
    swan.restaurants.cuisines()
    for rest in swiggy.get_restaurants():
        for cuisine in rest.cuisine:
            swan.restaurants.search_cuisine(cuisine=cuisine, exact=True)
            swan.restaurants.search_cuisine(cuisine=cuisine[1:-1], exact=False)
    assert 1 == 1
