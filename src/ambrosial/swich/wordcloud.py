from random import choice, shuffle
from typing import Any

import stylecloud

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.utils import get_curr_time


class WordCloud:
    def __init__(self, swan: SwiggyAnalytics) -> None:
        self.swan = swan

    def item_category(
        self,
        freq_weight: bool = False,
        **kwargs: dict[str, Any],
    ) -> None:
        data = self.swan.items.group("category_details")
        self._make_wc(
            data=data,
            fname="wcloud_item_category.png",
            freq_weight=freq_weight,
            kwargs=kwargs,
        )

    def item_name(
        self,
        freq_weight: bool = True,
        **kwargs: dict[str, Any],
    ) -> None:
        data = self.swan.items.group("name")
        self._make_wc(
            data=data,
            fname="wcloud_item_name.png",
            freq_weight=freq_weight,
            kwargs=kwargs,
        )

    def restaurant_cuisine(
        self,
        freq_weight: bool = False,
        **kwargs: dict[str, Any],
    ) -> None:
        data = self.swan.restaurants.cuisines()
        self._make_wc(
            data=data,
            fname="wcloud_restaurant_cuisine.png",
            freq_weight=freq_weight,
            kwargs=kwargs,
        )

    def restaurant_name(
        self,
        freq_weight: bool = True,
        **kwargs: dict[str, Any],
    ) -> None:
        data = self.swan.restaurants.group("name")
        self._make_wc(
            data=data,
            fname="wcloud_restaurant_name.png",
            freq_weight=freq_weight,
            kwargs=kwargs,
        )

    def coupon_code(
        self,
        freq_weight: bool = True,
        **kwargs: dict[str, Any],
    ) -> None:
        data = self.swan.offers.group("coupon_applied")
        self._make_wc(
            data=data,
            fname="wcloud_coupon_code.png",
            freq_weight=freq_weight,
            kwargs=kwargs,
        )

    def _make_wc(
        self,
        data: dict[str, int],
        fname: str,
        freq_weight: bool,
        kwargs: dict[str, Any],
    ) -> None:
        icons = (
            "fas fa-ice-cream",
            "fas fa-bread-slice",
            "fas fa-pepper-hot",
            "fas fa-fish",
            "fas fa-wine-glass",
            "fas fa-drumstick-bite",
            "fas fa-bone",
        )
        palettes = (
            "cartocolors.sequential.Peach_7",
            "cartocolors.sequential.BluGrn_7",
            "cartocolors.sequential.Purp_7",
            "cartocolors.sequential.agSunset_7_r",
            "lightbartlein.sequential.Blues7_7",
            "cmocean.sequential.Matter_20",
            "colorbrewer.diverging.Spectral_11",
            "colorbrewer.diverging.RdYlBu_9",
            "colorbrewer.diverging.RdBu_11",
            "cartocolors.diverging.Tropic_7",
            "lightbartlein.diverging.BlueDarkOrange12_12",
        )
        word_list = []
        for key, value in data.items():
            if freq_weight:
                word_list.extend([key for _ in range(value)])
            word_list.append(key)
        # if exact words are too close styplecloud goes crazy
        shuffle(word_list)
        stylecloud.gen_stylecloud(
            text=",".join(word_list),
            size=kwargs.get("size", 1000),
            icon_name=kwargs.get("icon_name", choice(icons)),
            palette=kwargs.get("palette", choice(palettes)),
            max_font_size=kwargs.get("max_font_size", 150),
            background_color=kwargs.get("background_color", "#191919"),
            gradient=kwargs.get("gradient", "vertical"),
            output_name=f"{get_curr_time()}{fname}",
        )
