from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich import SwiggyChart
from ambrosial.swiggy import Swiggy

swiggy = Swiggy(ddav=True)
swiggy.loadj()
swan = SwiggyAnalytics(swiggy)
swich = SwiggyChart(swan)


def test_init():
    swiggy = Swiggy()
    assert swiggy.ddav is False
    assert swiggy._fetched is False
    assert type(swiggy.orders_raw) is list
    assert len(swiggy.orders_raw) == 0
    assert type(swiggy.orders_refined) is list
    assert len(swiggy.orders_refined) == 0


def test_startup():
    swiggy = Swiggy(ddav=True)
    swiggy.loadj()
    swan = SwiggyAnalytics(swiggy)
    SwiggyChart(swan)
    assert 1 == 1


def test_swiggy_fetch_methods():
    swiggy.fetch_orders()
    assert 1 == 1


def test_swiggy_io():
    swiggy.loadb()
    swiggy.loadj()
    swiggy.saveb()
    swiggy.savej()


def test_swiggy_get_order():
    for order in swiggy.get_orders():
        assert order == swiggy.get_order(order.order_id)


def test_swiggy_get_item():
    for item in swiggy.get_items():
        assert item == swiggy.get_item(item.item_id)


def test_swiggy_get_rest():
    for rest in swiggy.get_restaurants():
        assert rest == swiggy.get_restaurant(rest.rest_id)


def test_swiggy_get_address():
    for address in swiggy.get_addresses():
        assert address == swiggy.get_address(address.address_id, ver=address.version)


def test_swiggy_get_address_wo_ver():
    swiggy2 = Swiggy(ddav=False)
    for address in swiggy2.get_addresses():
        assert address == swiggy2.get_address(address.address_id)


def test_swiggy_get_payment():
    for payment in swiggy.get_payments():
        assert payment in swiggy.get_payment(payment.transactionId)


def test_swiggy_get_offer():
    for offer in swiggy.get_offers():
        assert offer in swiggy.get_offer(offer.order_id)
