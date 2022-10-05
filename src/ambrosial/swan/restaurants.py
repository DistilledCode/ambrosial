from collections import Counter, defaultdict
from itertools import chain

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

    def group(self) -> dict[Restaurant, int]:
        return dict(Counter(self.all_restaurants).most_common())

    def group_by(self, attr: str) -> dict[str, int]:
        if attr == "cuisine":
            raise NotImplementedError("use .cuisines() instead.")
        if attr == "coordinates":
            raise TypeError(f"Unhashable attribute of Restaurant: {repr(attr)}")
        return dict(
            Counter(
                getattr(restaurant, attr) for restaurant in self.all_restaurants
            ).most_common()
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
