import pytest

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich import SwiggyChart
from ambrosial.swiggy import Swiggy
from ambrosial.swiggy.datamodel.item import Item
from ambrosial.swiggy.datamodel.order import Order

swiggy = Swiggy(ddav=True)
swiggy.loadj()
swan = SwiggyAnalytics(swiggy)
swich = SwiggyChart(swan)


def test_group():
    result = swan.items.group()
    k, v = list(result.keys()), list(result.values())
    assert all(i.__class__ is Item for i in k)
    assert all(i.__class__ is int for i in v)
    assert sorted(v, reverse=True) == v


def test_group_by():
    attrs = list(Item.__annotations__)
    attrs.remove("item_charges")
    with pytest.raises(NotImplementedError) as ex:
        swan.items.grouped_count("item_charges")
    assert ex.match("unhashable type: 'dict'")
    tot_len = len(swan.items.all_items)
    for attr in attrs:
        result = swan.items.grouped_count(attr)
        v = list(result.values())
        assert all(i.__class__ is int for i in v)
        assert sorted(v, reverse=True) == v
        if attr not in ("addons", "variants", "category_details"):
            assert sum(v) == tot_len


def test_grouped_instances():
    attrs = list(Item.__annotations__)
    hashable_attrs = attrs[:]
    unhashable_ = ["item_charges", "category_details", "variants", "addons"]
    for i in unhashable_:
        hashable_attrs.remove(i)
        with pytest.raises(TypeError):
            swan.items.grouped_instances(key=i)
    tot_len = len(swan.items.all_items)
    for h_attr in hashable_attrs:
        result = swan.items.grouped_instances(key=h_attr)
        _, v = result.keys(), result.values()
        for val in v:
            assert val.__class__ is list
            assert len(val) > 0
        assert sum(len(val) for val in v) == tot_len
        for attr in attrs:
            result = swan.items.grouped_instances(key=h_attr, attr=attr)
            _, v = result.keys(), result.values()
            for val in v:
                assert val.__class__ is list
                assert len(val) > 0
            assert sum(len(val) for val in v) == tot_len


def test_associated_orders():
    for item in set(swiggy.get_items()):
        aorders = swan.items.associated_orders(item.item_id)
        order_id_list = swiggy.cache.items[str(item.item_id)]
        assert aorders.__class__ is list
        assert len(aorders) > 0
        assert len(aorders) == len(order_id_list)
        # all are present and **in the same order**
        assert [o.order_id for o in aorders] == order_id_list
        assert all(element.__class__ is Order for element in aorders)
        assert all(item in order.items for order in aorders)


def test_swan_items():
    for item in swiggy.get_items():
        swan.items.summarise(item_id=item.item_id)
        swan.items.search_item(name=item.name[1:-1], exact=False)
        swan.items.search_item(name=item.name, exact=True)
    assert 1 == 1
