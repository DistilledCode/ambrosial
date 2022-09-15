from collections import Counter, defaultdict
from itertools import chain
from typing import Union

from swiggy import Swiggy
from swiggy.restaurant import Restaurant


class RestaurantsAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_rst = self.swiggy.restaurant()
        self._cuisine = defaultdict(list)
        for restaurant in reversed(self.all_rst):
            self._cuisine[restaurant].extend(i.lower() for i in restaurant.cuisine)
            restaurant.cuisine = list(set(self._cuisine[restaurant]))

    def group(self, attr: str = None) -> dict[Union[Restaurant, str], int]:
        if attr is None:
            return dict(Counter(self.all_rst).most_common())
        if attr == "cuisine":
            raise NotImplementedError("use .cuisines() method instead")
        if attr == "coordinates":
            raise TypeError(f"attribute {repr(attr)} of 'Restaurant' is unhashable")
        return dict(Counter(getattr(i, attr) for i in self.all_rst).most_common())

    def cuisines(self):
        return dict(
            Counter(
                list(
                    chain.from_iterable(
                        restaurant.cuisine for restaurant in set(self.all_rst)
                    )
                )
            ).most_common()
        )

    def search_cuisine(self, cuisine: str, exact: bool = True):
        # TODO: option to search multiple cuisines at once
        return (
            set(
                restaurant
                for restaurant in self.all_rst
                if cuisine.lower() in restaurant.cuisine
            )
            if exact
            else set(
                restaurant
                for restaurant in self.all_rst
                if any(cuisine.lower() in c for c in restaurant.cuisine)
            )
        )
