from typing import List

from bittrade_kraken_orderbook.models import Order


def list_to_orders(details: List):
    return [tuple(x) for x in details]
