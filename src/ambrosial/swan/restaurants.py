from collections import Counter, defaultdict
from typing import Any, Optional

from ambrosial.swan.typealiases import RestaurantSummary
from ambrosial.swiggy import Swiggy
from ambrosial.swiggy.datamodel.order import Order
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

    def associated_orders(self, restaurant_id: int) -> list[Order]:
        return [
            self.swiggy.get_order(order_id=order_id)
            for order_id in self.swiggy.cache.resturants[str(restaurant_id)]
        ]

    def grouped_instances(self, key: str, attr: Optional[str] = None) -> dict[Any, Any]:
        group_dict = defaultdict(list)
        for rest in self.all_restaurants:
            if attr is not None:
                group_dict[getattr(rest, key)].append(getattr(rest, attr))
            else:
                group_dict[getattr(rest, key)].append(rest)
        return dict(group_dict)

    def summarise(self, restaurant_id: int) -> RestaurantSummary:
        instances = self.associated_orders(restaurant_id)
        count = len(instances)
        total_distance = 0.0
        total_spent = 0
        total_save = 0.0
        total_charges = 0.0
        items_ordered: list[list[str]] = []
        weekday_frequency: list[str] = []
        hour_frequency: list[str] = []
        restaurant = instances[0].restaurant
        name = f"{restaurant.name}, {restaurant.area_name} ({restaurant.city_name})"
        image_url = restaurant.cover_image
        for order in instances:
            if order.mCancellationTime:
                continue
            total_spent += order.order_total
            total_save += sum(offer.total_offer_discount for offer in order.offers_data)
            total_charges += sum(order.charges.values())
            weekday_frequency.append(order.order_time.strftime("%A"))
            hour_frequency.append(order.order_time.strftime("%H"))
            items_ordered.extend([item.name] * item.quantity for item in order.items)
            total_distance += order.restaurant.customer_distance[1]
        return RestaurantSummary(
            name=name,
            restaurant_id=restaurant_id,
            count=count,
            total_spent=total_spent,
            avg_spent=round(total_spent / count, 3),
            total_saving=round(total_save, 3),
            avg_saving=round(total_save / count, 3),
            total_charges=round(total_charges, 3),
            avg_charges=round(total_charges / count, 3),
            saving_percentage=round(total_save / (total_save + total_spent) * 100, 3),
            total_distance=round(total_distance, 3),
            items_ordered=dict(
                Counter(
                    [
                        item_name
                        for item_list in items_ordered
                        for item_name in item_list
                    ]
                ).most_common()
            ),
            weekday_frequency=dict(Counter(weekday_frequency).most_common()),
            hour_frequency=dict(Counter(hour_frequency).most_common()),
            image_url=image_url,
        )

    def cuisines(self) -> dict[str, int]:
        return dict(
            Counter(
                cuisine
                for restaurant in set(self.all_restaurants)
                for cuisine in restaurant.cuisine
            ).most_common()
        )

    def search_restaurant(
        self,
        name: str,
        area: Optional[str] = None,
        exact: bool = True,
    ) -> list[Restaurant]:
        if exact:
            return [
                restaurant
                for restaurant in self.all_restaurants
                if name.lower() == restaurant.name.lower()
                and bool(
                    area.lower() == restaurant.area_name.lower()
                    if area is not None
                    else True
                )
            ]

        return [
            restaurant
            for restaurant in self.all_restaurants
            if name.lower() in restaurant.name.lower()
            and bool(
                area.lower() in restaurant.area_name.lower()
                if area is not None
                else True
            )
        ]

    def search_cuisine(self, cuisine: str, exact: bool = True) -> list[Restaurant]:
        return (
            [
                restaurant
                for restaurant in self.all_restaurants
                if cuisine.lower() in restaurant.cuisine
            ]
            if exact
            else [
                restaurant
                for restaurant in self.all_restaurants
                if any(cuisine.lower() in c for c in restaurant.cuisine)
            ]
        )
