from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich import SwiggyChart
from ambrosial.swiggy import Swiggy

swiggy = Swiggy(ddav=True)
swiggy.loadj()
swan = SwiggyAnalytics(swiggy)
swich = SwiggyChart(swan)


def test_swich_wcloud():
    swich.wcloud.coupon_code()
    swich.wcloud.item_category()
    swich.wcloud.item_name()
    swich.wcloud.restaurant_cuisine()
    swich.wcloud.restaurant_name()
    assert 1 == 1


def test_swich_heatmap():
    swich.ghubmap.order_amount()
    swich.ghubmap.order_count()
    assert 1 == 1


def test_swich_calplot():
    swich.calplot.cal_order_amount()
    swich.calplot.cal_order_count()
    for month in range(1, 13):
        swich.calplot.month_order_amount(month=month, year=2022)
        swich.calplot.month_order_count(month=month, year=2022)
    assert 1 == 1


def test_swich_regplot():
    swich.regplot.order_amount()
    swich.regplot.ordamt_ordfeeprcnt()
    swich.regplot.ordamt_ordfee()
    swich.regplot.ordtime_orddist()
    swich.regplot.ordtime_punctuality_bool()
    swich.regplot.ordtime_punctuality()
    assert 1 == 1


def test_swich_map():
    swich.map.count_density(city="chennai")
    assert 1 == 1
