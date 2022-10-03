from pathlib import Path
from random import choice, shuffle
from typing import Any

import stylecloud

import ambrosial.swich.utils as utils
from ambrosial.swan import SwiggyAnalytics

_OUTPUT_PATH = utils.get_output_folder(code="wc")


class WordCloud:
    def __init__(self, swan: SwiggyAnalytics) -> None:
        self.swan = swan

    def item_category(
        self,
        path: Path = _OUTPUT_PATH,
        fname: str = "item_category.png",
        freq_weight: bool = False,
        **kwargs: dict[str, Any],
    ) -> None:
        data = self.swan.items.group("category_details")
        self._make_wc(
            data=data,
            path=path,
            fname=fname,
            freq_weight=freq_weight,
            kwargs=kwargs,
        )

    def item_name(
        self,
        path: Path = _OUTPUT_PATH,
        fname: str = "item_name.png",
        freq_weight: bool = True,
        **kwargs: dict[str, Any],
    ) -> None:
        data = self.swan.items.group("name")
        self._make_wc(
            data=data,
            path=path,
            fname=fname,
            freq_weight=freq_weight,
            kwargs=kwargs,
        )

    def restaurant_cuisine(
        self,
        path: Path = _OUTPUT_PATH,
        fname: str = "restaurant_cuisine.png",
        freq_weight: bool = False,
        **kwargs: dict[str, Any],
    ) -> None:
        data = self.swan.restaurants.cuisines()
        self._make_wc(
            data=data,
            path=path,
            fname=fname,
            freq_weight=freq_weight,
            kwargs=kwargs,
        )

    def restaurant_name(
        self,
        path: Path = _OUTPUT_PATH,
        fname: str = "restaurant_name.png",
        freq_weight: bool = True,
        **kwargs: dict[str, Any],
    ) -> None:
        data = self.swan.restaurants.group("name")
        self._make_wc(
            data=data,
            path=path,
            fname=fname,
            freq_weight=freq_weight,
            kwargs=kwargs,
        )

    def coupon_code(
        self,
        path: Path = _OUTPUT_PATH,
        fname: str = "coupon_code.png",
        freq_weight: bool = True,
        **kwargs: dict[str, Any],
    ) -> None:
        data = self.swan.offers.group("coupon_applied")
        self._make_wc(
            data=data,
            path=path,
            fname=fname,
            freq_weight=freq_weight,
            kwargs=kwargs,
        )

    def _make_wc(
        self,
        data: dict[str, int],
        path: Path,
        fname: str,
        freq_weight: bool,
        kwargs: dict[str, Any],
    ) -> None:

        save_path = path / f"{utils.get_curr_time()}{fname}"
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
            icon_name=kwargs.get("icon_name", choice(utils.WC_ICONS)),
            palette=kwargs.get("palette", choice(utils.WC_PALETTES)),
            max_font_size=kwargs.get("max_font_size", 150),
            background_color=kwargs.get("background_color", "#191919"),
            gradient=kwargs.get("gradient", "vertical"),
            output_name=save_path,
        )
