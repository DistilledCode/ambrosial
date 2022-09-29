from collections import Counter, defaultdict
from itertools import chain
from typing import Union

from ambrosial.swiggy import Swiggy
from ambrosial.swiggy.datamodel.restaurant import Restaurant


class RestaurantAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_restaurants: list[Restaurant] = self.swiggy.get_restaurants()
        self._cuisine: dict[Restaurant, list] = defaultdict(list)
        for restaurant in reversed(self.all_restaurants):
            self._cuisine[restaurant].extend(i.lower() for i in restaurant.cuisine)
            restaurant.cuisine = list(set(self._cuisine[restaurant]))

    def group(self, attr: str = None) -> dict[Union[Restaurant, str], int]:
        if attr is None:
            return dict(Counter(self.all_restaurants).most_common())
        if attr == "cuisine":
            raise NotImplementedError("use .cuisines() method instead")
        if attr == "coordinates":
            raise TypeError(f"attribute {repr(attr)} of 'Restaurant' is unhashable")
        return dict(
            Counter(getattr(i, attr) for i in self.all_restaurants).most_common()
        )

    def cuisines(self) -> dict:
        return dict(
            Counter(
                list(
                    chain.from_iterable(
                        restaurant.cuisine for restaurant in set(self.all_restaurants)
                    )
                )
            ).most_common()
        )

    def search_cuisine(self, cuisine: str, exact: bool = True) -> set:
        # TODO: option to search multiple cuisines at once
        return (
            {
                restaurant
                for restaurant in self.all_restaurants
                if cuisine.lower() in restaurant.cuisine
            }
            if exact
            else {
                restaurant
                for restaurant in self.all_restaurants
                if any(cuisine.lower() in c for c in restaurant.cuisine)
            }
        )
