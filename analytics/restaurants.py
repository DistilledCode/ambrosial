from collections import Counter
from typing import Union

from swiggy import Swiggy
from swiggy.restaurant import Restaurant


class RestaurantsAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_rst = self.swiggy.restaurant()

    def group_by(self, attr: str = None) -> dict[Union[Restaurant, str], int]:
        if attr is None:
            return dict(Counter(self.all_rst).most_common())
        if attr == "coordinates":
            raise TypeError(f"attribute {repr(attr)} of 'Restaurant' is unhashable")
        return dict(Counter(getattr(i, attr) for i in self.all_rst).most_common())

    def distance(self):
        pass
