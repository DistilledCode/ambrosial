from collections import Counter
from typing import Union

from swiggy import Swiggy
from swiggy.restaurant import Restaurant


class RestaurantsAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_rst = self.swiggy.restaurant()

    def groupby(self, attr: str = None) -> dict[Union[Restaurant, str], int]:
        if attr is None:
            return dict(Counter(self.all_rst).most_common())
        if attr == "coordinates":
            return NotImplemented
        return dict(Counter(getattr(i, attr) for i in self.all_rst).most_common())
