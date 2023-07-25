import pytest

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich import SwiggyChart
from ambrosial.swiggy import Swiggy
from ambrosial.swiggy.datamodel.address import Address
from ambrosial.swiggy.datamodel.order import Offer

swiggy = Swiggy(ddav=True)
swiggy.loadj()
swan = SwiggyAnalytics(swiggy)
swich = SwiggyChart(swan)


def test_swan_address():
    swan.addresses.group()
    for attr in Address.__annotations__:
        swan.addresses.grouped_count(attr)
        swan.addresses.grouped_instances(attr)
        for attr2 in Address.__annotations__:
            swan.addresses.grouped_instances(key=attr, attr=attr2)

    swan.addresses.coordinates()
    swan.addresses.order_history()
    swan.addresses.delivery_time_stats()
    assert 1 == 1


def test_swan_offer():
    hashable_attr = [
        attr
        for attr, atype in Offer.__annotations__.items()
        if atype.__hash__ is not None
    ]
    with pytest.raises(NotImplementedError):
        swan.offers.group()
    swan.offers.statistics()
    for attr in hashable_attr:
        swan.offers.grouped_count(attr)
        swan.offers.grouped_instances(attr)
        for attr2 in Offer.__annotations__:
            swan.offers.grouped_instances(key=attr, attr=attr2)
