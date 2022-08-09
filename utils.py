from dataclasses import make_dataclass


def dict2dataclass(name: str, dict_to_conv: dict, **kwargs: dict) -> type:
    if any(
        not isinstance((x := key), str) or not x.replace(" ", "_").isidentifier()
        for key in dict_to_conv
    ):
        raise TypeError(f"Field names must be valid identifiers: {x!r}")
    field_list = []
    for key, val in dict_to_conv.items():
        new_key = key.replace(" ", "_").lower()
        if val.__class__ in [list, set, tuple]:
            value_list = []
            for ind, i in enumerate(val):
                if i.__class__ is dict:
                    value_list.append(dict2dataclass(f"{new_key}{ind}", i, **kwargs))
                else:
                    value_list.append(i)
            val = tuple(value_list)
        if val.__class__ is dict:
            val = dict2dataclass(new_key, val, **kwargs)
        field_list.append((new_key, val.__class__, val))
    DataClass = make_dataclass(name, field_list, **kwargs)
    return DataClass()
