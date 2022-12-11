from typing import Dict

from bittrade_kraken_orderbook.models import OrderBook, Message, Order


# Note: payload just remains as a dict here because of the name of the key: "as" making it troublesome / unnecessary to use a dataclass
def load_snapshot(order_book: OrderBook, payload: Dict):
    for details in payload['as']:
        order_book.asks.append(Order(*details))
    for details in payload['bs']:
        order_book.bids.append(Order(*details))
