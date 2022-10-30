from typing import Any


def july_calmon_args(kwargs: dict[str, Any]) -> dict[str, Any]:
    july_args = {
        "cmap": kwargs.pop("cmap", "golden"),
        "value_label": kwargs.pop("value_label", True),
        "colorbar": kwargs.pop("colorbar", True),
        "fontsize": kwargs.pop("fontsize", 15),
        "titlepad": kwargs.pop("titlepad", 40),
        "month_label": kwargs.pop("month_label", False),
    }
    return {**kwargs, **july_args}
