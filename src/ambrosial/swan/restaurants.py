from collections import Counter, defaultdict
from typing import Any, Optional

from ambrosial.swiggy import Swiggy
from ambrosial.swiggy.datamodel.restaurant import Restaurant


class RestaurantAnalytics:
    def __init__(self, swiggy: Swiggy) -> None:
        self.swiggy = swiggy
        self.all_restaurants: list[Restaurant] = self.swiggy.get_restaurants()
        self._cuisine: dict[Restaurant, set[str]] = defaultdict(set)
        for restaurant in reversed(self.all_restaurants):
            self._cuisine[restaurant] |= {i.lower() for i in restaurant.cuisine}
            restaurant.cuisine = self._cuisine[restaurant]

    def group(self) -> dict[Restaurant, int]:
        return dict(Counter(self.all_restaurants).most_common())

    def grouped_count(self, group_by: str) -> dict[str, int]:
        if group_by == "cuisine":
            raise NotImplementedError("use .cuisines() instead.")
        if group_by == "coordinates":
            raise TypeError(f"Unhashable attribute of Restaurant: {repr(group_by)}")
        return dict(
            Counter(
                getattr(restaurant, group_by) for restaurant in self.all_restaurants
            ).most_common()
        )

    def grouped_instances(self, key: str, attr: Optional[str] = None) -> dict[Any, Any]:
        group_dict = defaultdict(list)
        for rest in self.all_restaurants:
            if attr is not None:
                group_dict[getattr(rest, key)].append(getattr(rest, attr))
            else:
                group_dict[getattr(rest, key)].append(rest)
        return dict(group_dict)

    def cuisines(self) -> dict[str, int]:
        return dict(
            Counter(
                cuisine
                for restaurant in set(self.all_restaurants)
                for cuisine in restaurant.cuisine
            ).most_common()
        )

    def search_cuisine(self, cuisine: str, exact: bool = True) -> set[Restaurant]:
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
