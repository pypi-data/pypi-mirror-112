# noinspection PyPackageRequirements
import pytest
from trapeza.account.order_management import monkey_patch
from trapeza.account import FXAccount
from trapeza.exception import AccountError, OperatingError


# noinspection PyUnresolvedReferences
def test_monkey_patch():
    acc = FXAccount('EUR')
    monkey_patch(acc)

    _ = acc.stop_loss(1, 1, 0.5, 'EUR', 'USD', 5)
    _ = acc._exec_order_manager_heap
    _ = acc.exec_heap
    _ = acc._cum_sum_heap

    acc_2 = FXAccount('EUR')
    try:
        _ = acc_2._exec_order_manager_heap
        assert False
    except AttributeError:
        pass

    monkey_patch(acc_2)
    _ = acc_2._exec_order_manager_heap

    assert (acc_2 == acc) is False

    order_manager_heap = acc._order_heap
    assert dict(order_manager_heap) == order_manager_heap

    is_order_manager_heap = acc._is_order_manager_heap
    assert is_order_manager_heap is False

    is_setup_order_called = acc._is_setup_order_called
    assert is_setup_order_called is False

    is_tear_down_order_called = acc._is_tear_down_order_called
    assert is_tear_down_order_called is False

    temp_kwargs_order = acc._temp_kwargs_order
    assert dict(temp_kwargs_order) == temp_kwargs_order
    assert len(temp_kwargs_order) == 0

    try:
        a = 1
        monkey_patch(a)
        assert False
    except AccountError:
        pass

    try:
        monkey_patch(acc)
        assert False
    except AccountError:
        pass

    acc = FXAccount('EUR')
    monkey_patch(acc, only_basic=True)
    try:
        _ = acc.stop_loss(1, 1, 0.5, 'EUR', 'USD', 5)
        assert False
    except AttributeError:
        pass


def test_re_patch():
    acc = FXAccount('EUR')
    acc._tick = None
    try:
        monkey_patch(acc)
        assert False
    except AccountError:
        pass

    acc = FXAccount('EUR')
    acc.__reset = None
    try:
        monkey_patch(acc)
        assert False
    except AccountError:
        pass


# noinspection PyUnresolvedReferences,PyArgumentList,PyPep8Naming,PyTypeChecker
def test_reset():
    acc = FXAccount('EUR')
    acc._c_depot[b'EUR'] = 10
    depot_EUR = acc.depot['EUR']
    monkey_patch(acc)

    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 10)
    acc.buy(1, 1, 'BTC', 'EUR', processing_duration=100)
    assert depot_EUR == acc.depot['EUR']
    assert len(acc.exec_heap) != 0
    assert len(acc._order_heap) != 0

    acc._reset()
    assert len(acc.depot) == 0
    assert len(acc.exec_heap) == 0
    assert len(acc._order_heap) == 0


# noinspection PyUnresolvedReferences,PyArgumentList,PyPep8Naming
def test_order_series():
    acc = FXAccount('EUR')
    acc._c_depot[b'EUR'] = 10
    depot_EUR = acc.depot['EUR']
    monkey_patch(acc)

    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 10)
    assert depot_EUR == acc.depot['EUR']

    acc.tick({('EUR', 'USD'): 2.1})
    assert depot_EUR == acc.depot['EUR']

    acc.tick({('EUR', 'USD'): 1.9})
    assert acc.depot['EUR'] == 9
    assert acc.depot['USD'] == 1.9

    acc.tick({('EUR', 'USD'): 1.9})
    assert acc.depot['EUR'] == 9
    assert acc.depot['USD'] == 1.9

    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 10)
    acc.tick({('EUR', 'USD'): 2.1}, acc.clock+11)
    assert acc.depot['EUR'] == 9
    assert acc.depot['USD'] == 1.9
    assert len(acc._order_heap[('EUR', 'USD')]) == 0
    assert len(acc.exec_heap) == 0

    try:
        acc.stop_loss(2, -1, 2, 'EUR', 'USD', 10)
        assert False
    except OperatingError:
        pass


# noinspection PyUnresolvedReferences,PyArgumentList,PyPep8Naming,DuplicatedCode
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_multi_order_series():
    # test that two orders are cleaned from heap at the right expiration time
    # test that filling of two orders are done correctly
    # def stop_loss(self, current_rate, amount, ask_stop_price, base, quote, order_lifetime_duration, **kwargs)

    acc = FXAccount('EUR')
    acc._c_depot[b'EUR'] = 10
    depot_EUR = acc.depot['EUR']
    monkey_patch(acc)

    # two order of same type executed correctly
    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 2)
    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 2)
    assert depot_EUR == acc.depot['EUR']

    acc.tick({('EUR', 'USD'): 2.1})
    assert depot_EUR == acc.depot['EUR']

    acc.tick({('EUR', 'USD'): 1.9})
    assert acc.depot['EUR'] == 8
    assert acc.depot['USD'] == 2 * 1.9
    assert len(acc._order_heap['EUR', 'USD']) == 0

    # two orders of same type: one expires, one executed
    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 1)
    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 5)
    assert acc.depot['EUR'] == 8
    assert acc.depot['USD'] == 2 * 1.9

    acc.tick(clock=4)
    acc.tick({('EUR', 'USD'): 1.9})
    assert acc.depot['EUR'] == 7
    assert acc.depot['USD'] == 5.7
    assert len(acc._order_heap['EUR', 'USD']) == 0

    # two orders of same type both expire
    acc.clock = 0
    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 1)
    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 5)
    acc.tick({('EUR', 'USD'): 1.9}, clock=6)
    assert acc.depot['EUR'] == 7
    assert acc.depot['USD'] == 5.7
    assert len(acc._order_heap['EUR', 'USD']) == 0

    # two orders of different type both executed correctly
    acc.clock = 0
    acc.stop_loss(3, 1, 1.9, 'EUR', 'USD', 3)
    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 5)
    acc.tick({('EUR', 'USD'): 1.9}, clock=2)
    assert acc.depot['EUR'] == 5
    assert acc.depot['USD'] == 5 * 1.9
    assert len(acc._order_heap['EUR', 'USD']) == 0

    # three orders: one executed, two expired
    acc.clock = 0
    acc.stop_loss(3, 1, 1.8, 'EUR', 'USD', 3)
    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 5)
    acc.stop_loss(3, 1, 2.2, 'EUR', 'USD', 7)
    acc.tick({('EUR', 'USD'): 2.3}, clock=2)
    assert acc.depot['EUR'] == 5
    assert acc.depot['USD'] == 5 * 1.9
    acc.tick({('EUR', 'USD'): 2.1}, clock=4)
    assert acc.depot['EUR'] == 4
    assert acc.depot['USD'] == 5 * 1.9 + 1 * 2.1
    acc.tick({('EUR', 'USD'): 1.5}, clock=6)
    assert acc.depot['EUR'] == 4
    assert acc.depot['USD'] == 5 * 1.9 + 1 * 2.1
    assert len(acc._order_heap['EUR', 'USD']) == 0

    # four orders, two of same type, which get executed, rest expires
    acc.clock = 0
    acc.stop_loss(3, 1, 1.8, 'EUR', 'USD', 3)
    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 5)
    acc.stop_loss(3, 1, 2.2, 'EUR', 'USD', 7)
    acc.stop_loss(3, 1, 2.2, 'EUR', 'USD', 7)
    acc.tick({('EUR', 'USD'): 2.3}, clock=2)
    assert acc.depot['EUR'] == 4
    assert acc.depot['USD'] == 5 * 1.9 + 1 * 2.1
    acc.tick({('EUR', 'USD'): 2.1}, clock=4)
    assert acc.depot['EUR'] == 2
    assert acc.depot['USD'] == 5 * 1.9 + 3 * 2.1
    acc.tick({('EUR', 'USD'): 1.5}, clock=6)
    assert acc.depot['EUR'] == 2
    assert acc.depot['USD'] == 5 * 1.9 + 3 * 2.1
    assert len(acc._order_heap['EUR', 'USD']) == 0

    # four orders, two of same type, all expired
    acc.clock = 0
    acc.stop_loss(3, 1, 1.8, 'EUR', 'USD', 3)
    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 5)
    acc.stop_loss(3, 1, 2.2, 'EUR', 'USD', 7)
    acc.stop_loss(3, 1, 2.2, 'EUR', 'USD', 7)
    acc.tick({('EUR', 'USD'): 2.3}, clock=2)
    acc.tick({('EUR', 'USD'): 2.3}, clock=4)
    acc.tick({('EUR', 'USD'): 2.3}, clock=6)
    acc.tick({('EUR', 'USD'): 1.7}, clock=8)
    assert acc.depot['EUR'] == 2
    assert acc.depot['USD'] == 5 * 1.9 + 3 * 2.1
    assert len(acc._order_heap['EUR', 'USD']) == 0

    # two orders, executed consecutively
    acc.clock = 0
    acc.stop_loss(3, 1, 1.8, 'EUR', 'USD', 4)
    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 5)
    acc.tick({('EUR', 'USD'): 2.3}, clock=2)
    assert acc.depot['EUR'] == 2
    assert acc.depot['USD'] == 5 * 1.9 + 3 * 2.1
    acc.tick({('EUR', 'USD'): 2}, clock=3)
    assert acc.depot['EUR'] == 1
    assert acc.depot['USD'] == 5 * 1.9 + 3 * 2.1 + 1 * 2
    assert len(acc._order_heap['EUR', 'USD']) == 1
    acc.tick({('EUR', 'USD'): 1.795555}, clock=4)
    assert acc.depot['EUR'] == 0
    assert acc.depot['USD'] == 5 * 1.9 + 3 * 2.1 + 1 * 2 + 1 * 1.795555
    assert len(acc._order_heap['EUR', 'USD']) == 0

    # multiple currencies
    acc = FXAccount('EUR')
    monkey_patch(acc)
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'USD'] = 100
    acc._c_depot[b'ETH'] = 100
    acc._c_depot[b'BTC'] = 100
    acc.stop_loss(3, 1, 1.8, 'EUR', 'USD', 3)   # expired
    acc.stop_loss(3, 1, 1.8, 'EUR', 'USD', 5)   # executed
    acc.stop_loss(35, 1, 18, 'BTC', 'ETH', 3)   # expired
    acc.stop_loss(35, 1, 15, 'BTC', 'ETH', 5)   # expired
    acc.stop_loss(35, 1, 20, 'BTC', 'ETH', 30)  # executed
    acc.stop_loss(35, 1, 18, 'BTC', 'ETH', 15)  # executed

    acc.tick({('EUR', 'USD'): 3, ('BTC', 'ETH'): 30})
    assert acc.depot['EUR'] == 100
    assert acc.depot['USD'] == 100
    assert acc.depot['ETH'] == 100
    assert acc.depot['BTC'] == 100
    acc.tick({('EUR', 'USD'): 3, ('BTC', 'ETH'): 30}, clock=4)
    assert acc.depot['EUR'] == 100
    assert acc.depot['USD'] == 100
    assert acc.depot['ETH'] == 100
    assert acc.depot['BTC'] == 100
    acc.tick({('EUR', 'USD'): 1.7, ('BTC', 'ETH'): 20}, clock=5)
    assert acc.depot['EUR'] == 99
    assert acc.depot['USD'] == 100 + 1 * 1.7
    assert acc.depot['ETH'] == 100 + 1 * 20
    assert acc.depot['BTC'] == 99
    acc.tick({('EUR', 'USD'): 1.7, ('BTC', 'ETH'): 20}, clock=12)
    assert acc.depot['EUR'] == 99
    assert acc.depot['USD'] == 100 + 1 * 1.7
    assert acc.depot['ETH'] == 100 + 1 * 20
    assert acc.depot['BTC'] == 99
    acc.tick({('EUR', 'USD'): 1.7, ('BTC', 'ETH'): 17}, clock=14)
    assert acc.depot['EUR'] == 99
    assert acc.depot['USD'] == 100 + 1 * 1.7
    assert acc.depot['ETH'] == 100 + 1 * 20 + 1 * 17
    assert acc.depot['BTC'] == 98


# noinspection PyUnresolvedReferences
def test_swapped_base_quote_pair():
    # swapped base quote pair
    acc = FXAccount('EUR')
    monkey_patch(acc)
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'USD'] = 100

    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 3)
    acc.tick({('USD', 'EUR'): 0.7})
    assert acc.depot['EUR'] == 99
    assert round(acc.depot['USD'], 6) == round(100 + 1 / 0.7, 6)

    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 3)
    acc.stop_loss(2, 1, 1/2, 'USD', 'EUR', 3)
    try:
        acc.tick({('USD', 'EUR'): 0.7, ('EUR', 'USD'): 0.7})
        assert False
    except ValueError:
        pass
    assert acc.depot['EUR'] == 99
    assert round(acc.depot['USD'], 6) == round(100 + 1 / 0.7, 6)


# noinspection PyUnresolvedReferences,PyArgumentList
def test_sell_duration_propagated_from_order():
    # def stop_loss(self, current_rate, amount, ask_stop_price, base, quote, order_lifetime_duration, **kwargs)
    # def sell(self, amount, ask_price, base, quote, fee=None, processing_duration=None,
    #              coverage='except', instant_withdrawal=False, instant_float_fee=False,
    #              float_fee_currency=None):
    acc = FXAccount('EUR')
    acc._c_depot[b'EUR'] = 10
    monkey_patch(acc)

    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 10, fee=1, instant_float_fee=True, float_fee_currency='EUR',
                  processing_duration=12)
    acc.tick({('EUR', 'USD'): 1.9}, clock=8)
    assert acc.depot['EUR'] == 9
    assert 'USD' not in list(acc.depot.keys())

    acc.tick({('EUR', 'USD'): 5.8}, clock=11)
    assert acc.depot['EUR'] == 9
    assert 'USD' not in list(acc.depot.keys())

    acc.tick({('EUR', 'USD'): 2.5}, clock=13)
    assert acc.depot['EUR'] == 9
    assert 'USD' not in list(acc.depot.keys())

    acc.tick({('EUR', 'USD'): 100}, clock=8+12)
    assert acc.depot['EUR'] == 8
    assert acc.depot['USD'] == 1.9

    # multiple currencies
    acc = FXAccount('EUR')
    monkey_patch(acc)
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'USD'] = 100
    acc._c_depot[b'ETH'] = 100
    acc._c_depot[b'BTC'] = 100
    acc.stop_loss(3, 1, 1.8, 'EUR', 'USD', 5, fee=1, instant_float_fee=True, float_fee_currency='EUR',
                  processing_duration=12)   # executed
    acc.stop_loss(35, 1, 18, 'BTC', 'ETH', 3, fee=1, instant_float_fee=True, float_fee_currency='EUR',
                  processing_duration=12)   # expired
    acc.tick({('EUR', 'USD'): 1.7, ('BTC', 'ETH'): 17})
    assert acc.depot['EUR'] == 98
    assert acc.depot['ETH'] == 100
    assert acc.depot['USD'] == 100
    assert acc.depot['BTC'] == 100

    acc.tick({('EUR', 'USD'): 1.7, ('BTC', 'ETH'): 17}, clock=acc.clock+12)
    assert acc.depot['EUR'] == 97
    assert acc.depot['BTC'] == 99
    assert acc.depot['ETH'] == 100 + 17
    assert acc.depot['USD'] == 100 + 1.7


# noinspection PyUnresolvedReferences,PyArgumentList
def test_patch():
    acc = FXAccount('EUR')
    acc._c_depot[b'EUR'] = 10
    monkey_patch(acc)

    def patch_function(self, current_rate, duration, base, quote):
        _ = self.setup_order_method(patch_function, 'duration', duration=duration, base=base, quote=quote)
        if current_rate > 1:
            acc._c_depot[b'EUR'] -= 1
            confirmation = 1
        else:
            confirmation = 0
        return self.tear_down_order_method(patch_function, confirmation)

    acc.patch([patch_function])

    acc.patch_function(0.1, 3, 'EUR', 'USD')
    assert acc.depot['EUR'] == 10

    acc.tick({('EUR', 'USD'): 2})
    assert acc.depot['EUR'] == 9

    acc.patch_function(0.1, 3, 'EUR', 'USD')
    acc.tick({('EUR', 'USD'): 0.1}, clock=20)
    assert acc.depot['EUR'] == 9
    assert len(acc._order_heap['EUR', 'USD']) == 0
    assert 'patch_function' in acc._internal_acc_methods

    def patch_function_2(self, current_rate, duration, base, quote):
        _ = self.setup_order_method(patch_function_2, 'duration', duration=duration, base=base, quote=quote)
        if current_rate > 1:
            acc._c_depot[b'EUR'] -= 2
            confirmation = 1
        else:
            confirmation = 0
        return self.tear_down_order_method(patch_function_2, confirmation)

    acc.patch([patch_function_2])
    assert 'patch_function_2' in acc._internal_acc_methods
    acc.patch_function_2(0.1, 3, 'EUR', 'USD')
    assert acc.depot['EUR'] == 9
    acc.tick({('EUR', 'USD'): 2})
    assert acc.depot['EUR'] == 7

    def patch_function_3(self, current_rate, duration, base, quote):
        _ = self.setup_order_method(patch_function_3, 'duration', duration=duration, base=base, quote=quote)
        if current_rate > 1:
            acc._c_depot[b'EUR'] -= 3
            confirmation = 1
        else:
            confirmation = 0
        return self.tear_down_order_method(patch_function_3, confirmation)

    acc.patch([patch_function_3])
    assert 'patch_function_3' in acc._internal_acc_methods
    acc.patch_function_3(0.1, 3, 'EUR', 'USD')
    assert acc.depot['EUR'] == 7
    acc.tick({('EUR', 'USD'): 2})
    assert acc.depot['EUR'] == 4


def test_exceptions_at_monkey_patch():
    acc = FXAccount('EUR')
    monkey_patch(acc)
    try:
        monkey_patch(acc)
        assert False
    except AccountError:
        pass

    acc = FXAccount('EUR')
    acc._order_heap = None
    try:
        monkey_patch(acc)
        assert False
    except AccountError:
        pass


# noinspection PyArgumentList
def test_exceptions_at_tick():
    acc = FXAccount('EUR')
    monkey_patch(acc)

    try:
        acc.tick(clock=-1)
        assert False
    except TypeError:
        pass

    try:
        acc.tick(clock=2.1)
        assert False
    except TypeError:
        pass

    try:
        acc.tick({'EUR': 3}, clock=2)
        assert False
    except KeyError:
        pass

    try:
        acc.tick({('EUR', 'BTC', 'ETH'): 3}, clock=2)
        assert False
    except KeyError:
        pass

    try:
        acc.tick({('EUR', 'BTC'): 'a'}, clock=2)
        assert False
    except TypeError:
        pass

    try:
        acc.tick({(1, 2): 'a'}, clock=2)
        assert False
    except TypeError:
        pass

    try:
        acc.tick({(1, 'BTC'): 'a'}, clock=2)
        assert False
    except TypeError:
        pass

    try:
        acc.tick('something', clock=2)
        assert False
    except TypeError:
        pass


# noinspection PyUnresolvedReferences
def test_propagate_exceptions_from_native_account_exceptions():
    acc = FXAccount('EUR')
    monkey_patch(acc)
    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 10, processing_duration='something')
    try:
        acc.stop_loss(1, 1, 2, 'EUR', 'USD', 10, processing_duration='something')
        assert False
    except OperatingError:
        pass

    try:
        acc.tick({('EUR', 'USD'): 1})
        assert False
    except OperatingError:
        pass


# noinspection PyUnresolvedReferences, DuplicatedCode
def test_exception_at_patch():
    acc = FXAccount('EUR')
    acc._c_depot[b'EUR'] = 10
    monkey_patch(acc)

    # noinspection PyUnusedLocal
    def patch_function(self, current_rate, duration, base, quote):
        _ = self.setup_order_method(patch_function, 'duration', duration=duration, base=base)
        if current_rate > 1:
            acc._c_depot[b'EUR'] -= 1
            confirmation = 1
        else:
            confirmation = 0
        return self.tear_down_order_method(patch_function, confirmation)

    acc.patch([patch_function])

    try:
        acc.patch([patch_function])
        assert False
    except AccountError:
        pass

    # noinspection PyUnusedLocal
    def patch_function(self, current_rate, duration, base, quote):
        _ = self.setup_order_method(patch_function, 'duration', base=base, quote=quote)
        if current_rate > 1:
            acc._c_depot[b'EUR'] -= 1
            confirmation = 1
        else:
            confirmation = 0
        return self.tear_down_order_method(patch_function, confirmation)

    acc.patch([patch_function], False)

    try:
        acc.patch_function(0.1, 3, 'EUR', 'USD')
        assert False
    except NameError:
        pass

    def patch_function(self, current_rate, duration, base, quote):
        _ = self.setup_order_method(patch_function, 'duration', duration=duration, base=base, quote=quote)
        if current_rate > 1:
            acc._c_depot[b'EUR'] -= 1
            confirmation = 1
        else:
            confirmation = 0
        return self.tear_down_order_method(patch_function, confirmation)

    acc.patch([patch_function], False)

    try:
        acc.patch_function(0.1, -1, 'EUR', 'USD')
        assert False
    except ValueError:
        pass

    # noinspection PyUnusedLocal
    def patch_function(self, current_rate, duration, test_1, test_2):
        _ = self.setup_order_method(patch_function, 'duration', duration=duration, test_1=test_1, test_2=test_2)
        if current_rate > 1:
            acc._c_depot[b'EUR'] -= 1
            confirmation = 1
        else:
            confirmation = 0
        return self.tear_down_order_method(patch_function, confirmation)

    acc.patch([patch_function], False)

    try:
        acc.patch_function(0.1, 2, 'EUR', 'USD')
        assert False
    except KeyError:
        pass

    def patch_function(self, current_rate, duration, base, quote):
        _ = self.setup_order_method(patch_function, 'duration', current_rate=current_rate, duration=duration, base=base,
                                    quote=quote)
        if current_rate > 1:
            acc._c_depot[b'EUR'] -= 1
            confirmation = 1
        else:
            confirmation = 0
        return self.tear_down_order_method(patch_function, confirmation)

    acc.patch([patch_function], False)

    acc.patch_function(0.1, 2, 'EUR', 'USD')

    def patch_function(self, current_rate, duration, base, quote):
        _ = self.setup_order_method(patch_function, duration, duration=duration, base=base,
                                    quote=quote)
        if current_rate > 1:
            acc._c_depot[b'EUR'] -= 1
            confirmation = 1
        else:
            confirmation = 0
        return self.tear_down_order_method(patch_function, confirmation)

    acc.patch([patch_function], False)

    try:
        acc.patch_function(0.1, 2, 'EUR', 'USD')
        assert False
    except TypeError:
        pass

    def patch_function(self, current_rate, duration, base, quote):
        _ = self.setup_order_method(patch_function, 'something', duration=duration, base=base,
                                    quote=quote)
        if current_rate > 1:
            acc._c_depot[b'EUR'] -= 1
            confirmation = 1
        else:
            confirmation = 0
        return self.tear_down_order_method(patch_function, confirmation)

    acc.patch([patch_function], False)

    try:
        acc.patch_function(0.1, 2, 'EUR', 'USD')
        assert False
    except NameError:
        pass

    def patch_function(self, current_rate, duration, base, quote, test_var):
        _ = self.setup_order_method(patch_function, 'something', duration=duration, base=base,
                                    quote=quote, test_var=test_var)
        if current_rate > 1:
            acc._c_depot[b'EUR'] -= 1
            confirmation = 1
        else:
            confirmation = 0
        return self.tear_down_order_method(patch_function, confirmation)

    acc.patch([patch_function], False)

    try:
        acc.patch_function(0.1, 2, 'EUR', 'USD', 3)
        assert False
    except NameError:
        pass

    def patch_function_something():
        pass

    def patch_function(self, current_rate, duration, base, quote, test_var):
        _ = self.setup_order_method(patch_function_something, 'duration', duration=duration, base=base,
                                    quote=quote, test_var=test_var)
        if current_rate > 1:
            acc._c_depot[b'EUR'] -= 1
            confirmation = 1
        else:
            confirmation = 0
        return self.tear_down_order_method(patch_function_something, confirmation)

    acc.patch([patch_function], False)

    try:
        acc.patch_function(0.1, 2, 'EUR', 'USD', 3)
        assert False
    except OperatingError:
        pass


# noinspection PyPep8Naming,PyUnresolvedReferences,DuplicatedCode
def test_two_similar_orders():
    acc = FXAccount('EUR')
    acc._c_depot[b'EUR'] = 10
    depot_EUR = acc.depot['EUR']
    monkey_patch(acc)

    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 10)
    acc.stop_loss(3, 1, 2, 'EUR', 'USD', 10)

    acc.stop_loss(3, 1, 1, 'EUR', 'USD', 10)
    assert depot_EUR == acc.depot['EUR']

    acc.tick({('EUR', 'USD'): 2.1})
    assert depot_EUR == acc.depot['EUR']

    acc.tick({('EUR', 'USD'): 1.9})
    assert acc.depot['EUR'] == 8
    assert acc.depot['USD'] == 1.9 * 2

    acc.tick({('EUR', 'USD'): 1.9})
    assert acc.depot['EUR'] == 8
    assert acc.depot['USD'] == 1.9 * 2


# noinspection PyUnresolvedReferences
def test_trailing_stop_loss():
    acc = FXAccount('EUR')
    acc._c_depot[b'EUR'] = 10
    monkey_patch(acc)

    # trailing_stop_loss(self, current_bid_rate, amount, trailing_stop_bid_price, base, quote,
    #       order_lifetime_duration, **kwargs)
    acc.trailing_stop_loss(1.2, 1, 1, 'EUR', 'USD', 10)

    acc.tick({('EUR', 'USD'): 1.4})
    assert acc._order_heap['EUR', 'USD'][0][1]['trailing_stop_bid_price'] == (1.4 / 1.2) * 1

    acc.tick({('EUR', 'USD'): 1.15})
    assert acc.depot['EUR'] == 10 - 1
    assert acc.depot['USD'] == 1.15
    assert len(acc._order_heap['EUR', 'USD']) == 0

    acc.trailing_stop_loss(1.2, 1, 1, 'EUR', 'USD', 1)     # expired before first trigger
    acc.trailing_stop_loss(1.2, 1, 1.19, 'EUR', 'USD', 10)     # triggered in step 2
    acc.trailing_stop_loss(1.2, 1, 1, 'EUR', 'USD', 3)     # expired after trigger
    acc.trailing_stop_loss(1.2, 1, 1, 'EUR', 'USD', 10)     # not triggered
    acc.tick({('EUR', 'USD'): 1.21})
    acc.tick({('EUR', 'USD'): 1.21})
    assert len(acc._order_heap['EUR', 'USD']) == 3      # expired
    acc.tick({('EUR', 'USD'): 1.15})
    assert acc.depot['EUR'] == 10 - 2
    assert acc.depot['USD'] == 1.15 * 2
    assert len(acc._order_heap['EUR', 'USD']) == 2      # triggered
    acc.tick({('EUR', 'USD'): 1.4})
    assert acc.depot['EUR'] == 10 - 2
    assert acc.depot['USD'] == 1.15 * 2
    assert len(acc._order_heap['EUR', 'USD']) == 1      # expired
    acc.tick({('EUR', 'USD'): 1.4})
    assert acc.depot['EUR'] == 10 - 2
    assert acc.depot['USD'] == 1.15 * 2
    assert len(acc._order_heap['EUR', 'USD']) == 1

    acc = FXAccount('EUR')
    acc._c_depot[b'EUR'] = 10
    monkey_patch(acc)
    acc.trailing_stop_loss(1.2, 1, 1, 'EUR', 'USD', 10)
    acc.trailing_stop_loss(1.2, 1, 1, 'EUR', 'USD', 10)

    acc.tick({('EUR', 'USD'): 0.8})
    assert acc.depot['EUR'] == 8
    assert acc.depot['USD'] == 2 * 0.8

    acc = FXAccount('EUR')
    acc._c_depot[b'EUR'] = 10
    monkey_patch(acc)
    acc.trailing_stop_loss(1.2, 1, 1, 'EUR', 'USD', 10)
    acc.tick({('EUR', 'USD'): 1.32})
    assert acc._order_heap['EUR', 'USD'][0][1]['trailing_stop_bid_price'] == 1.1
    acc.tick({('EUR', 'USD'): 1.2})
    assert acc._order_heap['EUR', 'USD'][0][1]['trailing_stop_bid_price'] == 1.1
    acc.tick({('EUR', 'USD'): 1.12})
    assert acc._order_heap['EUR', 'USD'][0][1]['trailing_stop_bid_price'] == 1.1
    acc.tick({('EUR', 'USD'): 1.32})
    assert acc._order_heap['EUR', 'USD'][0][1]['trailing_stop_bid_price'] == 1.1
    acc.tick({('EUR', 'USD'): 1.452})
    assert acc._order_heap['EUR', 'USD'][0][1]['trailing_stop_bid_price'] == 1.21


# noinspection PyUnresolvedReferences
def test_buy_limit():
    # buy_limit() is very similar to stop_loss() except underlying base transaction, such as it is sufficient to
    # use a shorter test sequence because stop_loss() is already well tested
    acc = FXAccount('EUR')
    acc._c_depot[b'EUR'] = 100
    monkey_patch(acc)

    # def buy_limit(self, current_ask_rate, volume, limit_ask_price, base, quote, order_lifetime_duration, **kwargs)
    acc.buy_limit(12, 10, 5, 'BTC', 'EUR', 12, fee=1, float_fee_currency='EUR', instant_float_fee=True,
                  processing_duration=1)
    acc.tick({('BTC', 'EUR'): 5.5})

    assert acc.depot['EUR'] == 100

    acc.tick({('BTC', 'EUR'): 4})
    assert acc.depot['EUR'] == 100 - 1

    acc.tick()
    assert acc.depot['EUR'] == 100 - 1 - 10 * 4
    assert acc.depot['BTC'] == 10


# noinspection PyUnresolvedReferences
def test_sell_limit():
    # sell_limit() is very similar to stop_loss() except underlying base transaction, such as it is sufficient to
    # use a shorter test sequence because stop_loss() is already well tested
    acc = FXAccount('EUR')
    acc._c_depot[b'EUR'] = 100
    monkey_patch(acc)

    # def buy_limit(self, current_ask_rate, volume, limit_ask_price, base, quote, order_lifetime_duration, **kwargs)
    acc.sell_limit(2, 10, 5, 'EUR', 'BTC', 12, fee=1, float_fee_currency='EUR', instant_float_fee=True,
                   processing_duration=1)
    acc.tick({('EUR', 'BTC'): 4.5})

    assert acc.depot['EUR'] == 100

    acc.tick({('EUR', 'BTC'): 5})
    assert acc.depot['EUR'] == 100 - 1

    acc.tick()
    assert acc.depot['EUR'] == 100 - 1 - 10
    assert acc.depot['BTC'] == 10 * 5


def test_start_buy():
    acc = FXAccount('EUR')
    acc._c_depot[b'EUR'] = 100
    monkey_patch(acc)

    acc.start_buy(2, 10, 3, 'BTC', 'EUR', 12)
    acc.tick({('BTC', 'EUR'): 2.5})

    assert acc.depot['EUR'] == 100

    acc.tick({('BTC', 'EUR'): 3})

    assert acc.depot['BTC'] == 10
    assert acc.depot['EUR'] == 100 - (10 * 3)
