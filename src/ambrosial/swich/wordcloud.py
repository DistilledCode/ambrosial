from pathlib import Path
from random import choice, shuffle
from typing import Any, Optional

import stylecloud

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.utils import WC_ICONS, WC_PALETTES, get_curr_time
from ambrosial.swiggy.utils import create_path


class WordCloud:
    def __init__(self, swan: SwiggyAnalytics) -> None:
        self.swan = swan
        self.save_path = self.swan.swiggy.home_path / "swich" / "word_cloud"
        create_path(self.save_path)

    def item_category(
        self,
        path: Optional[Path] = None,
        fname: str = "item_category.png",
        freq_weight: bool = False,
        **kwargs: Any,
    ) -> None:
        data = self.swan.items.grouped_count("category_details")
        self._make_wc(
            data=data,
            path=path,
            fname=fname,
            freq_weight=freq_weight,
            kwargs=kwargs,
        )

    def item_name(
        self,
        path: Optional[Path] = None,
        fname: str = "item_name.png",
        freq_weight: bool = True,
        **kwargs: Any,
    ) -> None:
        data = self.swan.items.grouped_count("name")
        self._make_wc(
            data=data,
            path=path,
            fname=fname,
            freq_weight=freq_weight,
            kwargs=kwargs,
        )

    def restaurant_cuisine(
        self,
        path: Optional[Path] = None,
        fname: str = "restaurant_cuisine.png",
        freq_weight: bool = False,
        **kwargs: Any,
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
        path: Optional[Path] = None,
        fname: str = "restaurant_name.png",
        freq_weight: bool = True,
        **kwargs: Any,
    ) -> None:
        data = self.swan.restaurants.grouped_count("name")
        self._make_wc(
            data=data,
            path=path,
            fname=fname,
            freq_weight=freq_weight,
            kwargs=kwargs,
        )

    def coupon_code(
        self,
        path: Optional[Path] = None,
        fname: str = "coupon_code.png",
        freq_weight: bool = True,
        **kwargs: Any,
    ) -> None:
        data = self.swan.offers.grouped_count("coupon_applied")
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
        path: Optional[Path],
        fname: str,
        freq_weight: bool,
        kwargs: dict[str, Any],
    ) -> None:

        if path is None:
            save_path = self.save_path / f"{get_curr_time()}{fname}"
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
            icon_name=kwargs.get("icon_name", choice(WC_ICONS)),
            palette=kwargs.get("palette", choice(WC_PALETTES)),
            max_font_size=kwargs.get("max_font_size", 150),
            background_color=kwargs.get("background_color", "#191919"),
            gradient=kwargs.get("gradient", "vertical"),
            output_name=save_path,
        )
