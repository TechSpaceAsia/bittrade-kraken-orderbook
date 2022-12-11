from decimal import Decimal
from typing import Literal, List, Dict

from bittrade_kraken_orderbook.models import OrderBook
from bittrade_kraken_orderbook.models.order import GenericOrder, Order, find_index_by_price, get_volume, get_price

from logging import getLogger

LOGGER = getLogger(__name__)


def update_side(side: Literal['bids', 'asks'], order_book: OrderBook, updated_orders: List[List[str]]):
    orders_list: List[Order] = getattr(order_book, side)
    order: List[str]
    for order in updated_orders:
        volume = Decimal(get_volume(order))
        price = get_price(order)
        if volume == 0:
            # Removing order
            order_index = find_index_by_price(orders_list, price)
            if order_index == -1:
                LOGGER.error('Expected to find an order with price %s but did not. Orders: %s', price, orders_list)
            else:
                orders_list.pop(order_index)

def update_bids(order_book: OrderBook, payload: Dict):
    update_side('bids', order_book, payload['b'])


def update_asks(order_book: OrderBook, payload: Dict):
    update_side('asks', order_book, payload['a'])