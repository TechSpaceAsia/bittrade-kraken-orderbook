from bittrade_kraken_orderbook.models import Order, RepublishOrder
from bittrade_kraken_orderbook.models.order import is_republish_order, find_index_by_price


def test_is_republish_order():
    a = ['1', '2', '3']
    b = ['1', '2', '3', '4']

    assert not is_republish_order(a)
    assert is_republish_order(b)


def test_find_index_by_price():
    orders = [Order(str(i + 1), "", "") for i in range(30)]
    assert find_index_by_price(orders, "5") == 4, 'Could not find "5"'
    assert find_index_by_price(orders, "5.0") == 4, 'Could not find with different decimal'
    assert find_index_by_price(orders, "5.5") == -1, 'Should not have found non-exact match'
