from random import choices

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich import SwiggyChart
from ambrosial.swiggy import Swiggy

swiggy = Swiggy(ddav=True)
swiggy.loadj()
swan = SwiggyAnalytics(swiggy)
swich = SwiggyChart(swan)

items = swiggy.get_items()
restaurants = swiggy.get_restaurants()


def test_swich_wcloud():
    swich.wcloud.coupon_code()
    swich.wcloud.item_category()
    swich.wcloud.item_name()
    swich.wcloud.restaurant_cuisine()
    swich.wcloud.restaurant_name()
    assert 1 == 1


def test_swich_heatmap():
    swich.heatmap.order_amount()
    swich.heatmap.order_count()
    swich.heatmap.avg_delivery_time()
    swich.heatmap.offer_discount()
    swich.heatmap.super_benefits()
    swich.heatmap.total_saving()
    assert 1 == 1


def test_swich_ghubmap():
    swich.ghubmap.order_amount()
    swich.ghubmap.order_count()
    swich.ghubmap.offer_discount()
    swich.ghubmap.super_benefits()
    swich.ghubmap.total_saving()
    for resturant in choices(restaurants, k=5):
        swich.ghubmap.restaurant_count(restaurant_id=resturant.rest_id)
        swich.ghubmap.restaurant_amount(restaurant_id=resturant.rest_id)
    for item in choices(items, k=5):
        swich.ghubmap.item_count(item_id=item.item_id)
        swich.ghubmap.item_amount(item_id=item.item_id)
    assert 1 == 1


def test_swich_calplot():
    swich.calplot.cal_order_amount()
    swich.calplot.cal_order_count()
    swich.calplot.cal_offer_amount()
    for month in range(1, 13):
        swich.calplot.month_order_amount(month=month, year=2022)
        swich.calplot.month_order_count(month=month, year=2022)
        swich.calplot.month_offer_amount(month=month, year=2022)
    assert 1 == 1


def test_swich_regplot():
    swich.regplot.order_amount()
    swich.regplot.ordamt_ordfeeprcnt()
    swich.regplot.ordamt_ordfee()
    swich.regplot.ordtime_orddist()
    swich.regplot.ordtime_punctuality_bool()
    swich.regplot.ordtime_punctuality()
    swich.regplot.ordamt_offramt()
    assert 1 == 1


def test_swich_map():
    swich.map.count_density(city="chennai")
    swich.map.amount_density(nationwide=True)
    assert 1 == 1
