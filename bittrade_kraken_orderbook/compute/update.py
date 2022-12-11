from decimal import Decimal
from typing import Literal, List, Dict, Optional

from bittrade_kraken_orderbook.models import OrderBook
from bittrade_kraken_orderbook.models.order import GenericOrder, Order, find_by_price, get_volume, get_price

from logging import getLogger

LOGGER = getLogger(__name__)


def update_side(side: Literal['bids', 'asks'], order_book: OrderBook, updated_orders: List[List[str]]):
    orders_list: List[Order] = getattr(order_book, side)
    order: List[str]
    is_descending = side == 'bids'
    for order in updated_orders:
        volume = Decimal(get_volume(order))
        price = get_price(order)
        if volume == 0:
            # Removing order
            matching_order = find_by_price(orders_list, price)
            if not matching_order:
                LOGGER.error('Expected to find an order with price %s but did not. Orders: %s', price, orders_list)
            else:
                orders_list.remove(matching_order)
        else:
            # Matching order may not exist
            order_index: int
            matching_order: Optional[Order]
            order_index, matching_order = find_insert_index_by_price(orders_list, price, is_descending=is_descending)


def update_bids(order_book: OrderBook, payload: Dict):
    # Bids come in descending order
    update_side('bids', order_book, payload['b'])


def update_asks(order_book: OrderBook, payload: Dict):
    update_side('asks', order_book, payload['a'])