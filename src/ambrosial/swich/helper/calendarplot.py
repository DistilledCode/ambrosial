from datetime import date
from typing import Any, Literal, Optional

from ambrosial.swan import SwiggyAnalytics
from ambrosial.swich.helper import heatmap


def july_calmon_args(kwargs: dict[str, Any]) -> dict[str, Any]:
    july_args = {
        "cmap": kwargs.pop("cmap", "golden"),
        "value_label": kwargs.pop("value_label", True),
        "colorbar": kwargs.pop("colorbar", True),
        "fontsize": kwargs.pop("fontsize", 15),
        "titlepad": kwargs.pop("titlepad", 50),
        "month_label": kwargs.pop("month_label", False),
    }
    return {**kwargs, **july_args}


def get_details(
    code: Literal["oa", "on"],
    swan: SwiggyAnalytics,
    drange: Optional[tuple[str, str]],
    bins: str,
) -> tuple[list[date], list[int]]:
    return heatmap.get_details(
        code=code,
        swan=swan,
        drange=drange,
        bins=bins,
    )
