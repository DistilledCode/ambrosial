from datetime import datetime
from pathlib import Path
from typing import Literal

from ambrosial.swiggy.utils import create_path

__all__ = [
    "WC_ICONS",
    "WC_PALETTES",
    "get_curr_time",
    "get_output_folder",
    "create_output_folder",
]


WC_ICONS = (
    "fas fa-fish",
    "fas fa-bone",
    "fas fa-ice-cream",
    "fas fa-pepper-hot",
    "fas fa-wine-glass",
    "fas fa-bread-slice",
    "fas fa-drumstick-bite",
)

WC_PALETTES = (
    "cmocean.sequential.Matter_20",
    "colorbrewer.diverging.RdBu_11",
    "cartocolors.sequential.Purp_7",
    "colorbrewer.diverging.RdYlBu_9",
    "cartocolors.sequential.Peach_7",
    "cartocolors.diverging.Tropic_7",
    "cartocolors.sequential.BluGrn_7",
    "colorbrewer.diverging.Spectral_11",
    "lightbartlein.sequential.Blues7_7",
    "cartocolors.sequential.agSunset_7_r",
    "lightbartlein.diverging.BlueDarkOrange12_12",
)


_OUTPUT_PATH = Path.home() / ".ambrosial" / "swich"


_OUTPUT_SUBPATHS = {
    "wc": "word_cloud",
    "mp": "map",
}


def get_curr_time() -> str:
    return datetime.today().strftime("%Y%m%d_%H%M%S_")


def get_output_folder(code: Literal["wc", "mp"]) -> Path:
    return _OUTPUT_PATH / _OUTPUT_SUBPATHS[code]


def create_output_folder() -> None:
    for subfolder in _OUTPUT_SUBPATHS.values():
        create_path(_OUTPUT_PATH / subfolder)
