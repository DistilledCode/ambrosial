from utils import dict2dataclass, get_orders, recursive_evaluation

orders = []

for index, order in enumerate(get_orders()):
    orders.append(dict2dataclass(f"order{index}", recursive_evaluation(order)))
