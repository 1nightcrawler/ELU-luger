from random import randint
from flask import current_app

# How many children/branches can diverge from a book
# Can change params in config.py
def choose_child_count(eligible_count: int, *, is_root: bool) -> int:
    if eligible_count <= 0:
        return 0

    if is_root:
        minimum = current_app.config["BOOK_MAP_ROOT_CHILDREN_MIN"]
        maximum = current_app.config["BOOK_MAP_ROOT_CHILDREN_MAX"]
    else:
        minimum = current_app.config["BOOK_MAP_FOLLOWUP_CHILDREN_MIN"]
        maximum = current_app.config["BOOK_MAP_FOLLOWUP_CHILDREN_MAX"]

    low = min(minimum, eligible_count)
    high = min(maximum, eligible_count)
    return randint(low, high)