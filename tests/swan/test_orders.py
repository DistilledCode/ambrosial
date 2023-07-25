from itertools import combinations
from random import choices

import pytest

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich import SwiggyChart
from ambrosial.swiggy import Swiggy
from ambrosial.swiggy.datamodel.order import Order

swiggy = Swiggy(ddav=True)
swiggy.loadj()
swan = SwiggyAnalytics(swiggy)
swich = SwiggyChart(swan)


hashable_attr = [
    attr for attr, atype in Order.__annotations__.items() if atype.__hash__ is not None
]

x = list(swan.orders.strftime_mapping)
possible_bins = []
for i in range(1, len(x) + 1):
    for comb in combinations(x, i):
        possible_bins.append("+".join(comb))


def test_group():
    with pytest.raises(NotImplementedError):
        swan.orders.group()


def test_group_by():
    for attr in hashable_attr:
        result = swan.orders.grouped_count(attr)
        value_list = list(result.values())
        assert all(i.__class__ is int for i in value_list)
        assert sorted(value_list, reverse=True) == value_list


def test_swan_orders():
    for attr in hashable_attr:
        swan.orders.grouped_instances(attr)
        for eachattr in Order.__annotations__:
            swan.orders.grouped_instances(key=attr, attr=eachattr)
    for bins in choices(possible_bins, k=100):
        swan.orders.tseries_amount(bins)
        swan.orders.tseries_count(bins)
        swan.orders.tseries_charges(bins)
        swan.orders.tseries_del_time(bins)
        swan.orders.tseries_punctuality(bins)
        swan.orders.tseries_distance(bins)
        swan.orders.tseries_super_benefits(bins)
        swan.orders.tseries_furthest_order(bins)
    assert 1 == 1
