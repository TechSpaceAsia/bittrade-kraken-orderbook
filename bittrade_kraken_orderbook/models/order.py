from decimal import Decimal
from typing import NamedTuple, Union, List, Optional
from bisect import bisect_left
from bittrade_kraken_orderbook.models.bisection_extended import index

class Order(NamedTuple):
    price: str
    volume: str
    timestamp: str


class RepublishOrder(NamedTuple):
    price: str
    volume: str
    timestamp: str
    republish = "r"


GenericOrder = Union[Order, RepublishOrder]

RawOrder = List[str]
def is_republish_order(order: GenericOrder) -> bool:
    return len(order) == 4

def get_volume(order: RawOrder):
    return order[1]


def get_price(order: RawOrder):
    return order[0]

def find_index_by_price(orders_list: List[GenericOrder], price: str) -> int:
    def key(item: GenericOrder):
        return Decimal(item.price)
    try:
        return index(orders_list, Decimal(price), key=key)
    except ValueError as exc:
        return -1
