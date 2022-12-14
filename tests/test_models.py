from bittrade_kraken_orderbook.models import Order, RepublishOrder
from bittrade_kraken_orderbook.models.message import get_checksum, get_pair
from bittrade_kraken_orderbook.models.order import is_republish_order, find_by_price, find_insert_index_by_price


def test_is_republish_order():
    a = ['1', '2', '3']
    b = ['1', '2', '3', '4']

    assert not is_republish_order(a)
    assert is_republish_order(b)


def test_get_checksum():
    assert get_checksum([1, {"a": [], "c": "lala"}, "book-25", "XRP/USD"]) == "lala"
    assert get_checksum([1, {"a": []}, {"b": [], "c": "red"}, "book-25", "XRP/USD"]) == "red"
    assert get_checksum([432, {'a': [['76.28000', '0.00000000', '1670883993.134315'], ['76.73000', '0.46274251', '1670883428.136306', 'r']], 'c': '2582013099'}, 'book-25', 'LTC/USD']) == "2582013099"

def test_get_pair():
    assert get_pair([432, {'a': [['76.28000', '0.00000000', '1670883993.134315'], ['76.73000', '0.46274251', '1670883428.136306', 'r']], 'c': '2582013099'}, 'book-25', 'LTC/USD']) == "LTC/USD"
    assert get_pair([432, {
        'a': [['76.28000', '0.00000000', '1670883993.134315'], ['76.73000', '0.46274251', '1670883428.136306', 'r']]}, {"b": [],
        'c': '2582013099'}, 'book-25', 'XRP/USD']) == "XRP/USD"



def test_find_by_price():
    orders = [Order(str(i + 1), "", "") for i in range(30)]
    assert find_by_price(orders, "1") == Order("1", "", ""), 'Could not find first element'
    assert find_by_price(orders, "5") == Order("5", "", ""), 'Could not find "5"'
    assert find_by_price(orders, "5.0") == Order("5", "", ""), 'Could not find with different decimal'
    assert find_by_price(orders, "30") == Order("30", "", ""), 'Could not find last element'
    assert find_by_price(orders, "5.5") is None, 'Should not have found non-exact match'
    assert find_by_price(orders, "42") is None, 'Should not have found non-exact match outside range'

    # With a descending order
    orders = [Order(str(50 - i), "", "") for i in range(30)]
    assert find_by_price(orders, "50") == Order("50", "", ""), 'Could not find first element'
    assert find_by_price(orders, "46") == Order("46", "", ""), 'Could not find "5"'
    assert find_by_price(orders, "44.0") == Order("44", "", ""), 'Could not find with different decimal'
    assert find_by_price(orders, "21") == Order("21", "", ""), 'Could not find last element'
    assert find_by_price(orders, "35.5") is None, 'Should not have found non-exact match'
    assert find_by_price(orders, "10") is None, 'Should not have found non-exact match outside range'

def test_find_insert_index_by_price():
    orders = [Order(str(i + 1), "", "") for i in range(30)]
    assert find_insert_index_by_price(orders, "0.1", False) == 0, 'Lower than first should give index 0'
    assert find_insert_index_by_price(orders, "1.0", False) == 0, 'Equal to first should give index 0'
    assert find_insert_index_by_price(orders, "5", False) == 4, 'Exact match should give correct index'
    assert find_insert_index_by_price(orders, "10.2", False) == 10, 'Not exact match should give index one higher than nearest'
    assert find_insert_index_by_price(orders, "30",
                                      False) == 29, 'Equal to last should give last index'
    assert find_insert_index_by_price(orders, "35",
                                      False) == 30, 'Higher than highest should give index len(original)'

    orders = [Order(str(100 - i), "", "") for i in range(30)]
    assert find_insert_index_by_price(orders, "100.1", True) == 0, 'Higher than first should give index 0'
    assert find_insert_index_by_price(orders, "100.000", True) == 0, 'Equal to first should give index 0'
    assert find_insert_index_by_price(orders, "90", True) == 10, 'Exact match should give correct index'
    assert find_insert_index_by_price(orders, "85.5",
                                      True) == 15, 'Not exact match should give index one higher than nearest'
    assert find_insert_index_by_price(orders, "71",
                                      True) == 29, 'Equal to last should give last index'
    assert find_insert_index_by_price(orders, "42",
                                      True) == 30, 'Lower than lowest should give index len(original)'