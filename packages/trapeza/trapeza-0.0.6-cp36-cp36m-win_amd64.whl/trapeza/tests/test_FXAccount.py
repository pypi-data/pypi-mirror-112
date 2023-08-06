# noinspection PyPackageRequirements
import pytest
import heapq
import numpy as np

from trapeza import account
from trapeza.utils import check_types, ProtectedDict, ProtectedExecHeap
from trapeza.exception import CoverageError, PositionNAError, AccountError, OperatingError
from trapeza.account.execution_heap import cFXWrapperVectorHeap

# FXAccount was changed in its .buy() interface: volume argument is now given in BASE and not in QUOTE anymore.
# Therefore arguments passed to FXAccount.buy() had to be adapted, which explains apparently strange multiplication of
# arguments (multiplication with inverse exchange rate to convert quote currency notation into base currency notation)
# and the excess use of the parameter float_fee_currency.
# This avoids to change all asserts.


def test_standard_init():
    try:
        _ = account.FXAccount(3)
        assert False
    except TypeError:
        pass

    acc = account.FXAccount('EUR')
    assert acc.clock == 0, 'Clock must be initialized with 0'
    assert len(acc.depot) == 0, 'Depot must be initialized empty'
    assert type(acc.depot) == ProtectedDict, 'Depot must be dict'
    assert acc.reference_currency == 'EUR', 'Reference currency bad initialization'
    assert len(acc.exec_heap) == 0, 'Heap must be initialized empty'
    fee_amount, fee_currency, fee_exec_dur = acc._fee['sell'](0, 0, 'EUR', 'EUR', 0)
    assert fee_amount == 0, 'Fee amount must be initialized to 0'
    assert fee_currency == 'EUR', 'Fee currency must be EUR'
    assert fee_exec_dur == 0, 'Execution duration of fees must be initialized 0'
    assert type(acc._fee) == ProtectedDict
    assert len(acc.exchange_rates) == 0, 'Exchange rates must be initialized empty'
    assert type(acc.exchange_rates) == ProtectedDict, 'Exchange rates must be dict'
    assert acc.check_marked_coverage == 'min_backward'

    try:
        _ = account.FXAccount('EUR', marked_coverage='something')
        assert False
    except TypeError:
        pass
    try:
        _ = account.FXAccount('EUR', exec_heap='something')
        assert False
    except TypeError:
        pass
    try:
        _ = account.FXAccount('EUR', exec_heap=[('test', 2)])
        assert False
    except TypeError:
        pass
    try:
        _ = account.FXAccount('EUR', exec_heap=[('test', 2, 'test', 'USD')])
        assert False
    except TypeError:
        pass
    try:
        _ = account.FXAccount('EUR', fee_sell=2)
        assert False
    except TypeError:
        pass
    try:
        _ = account.FXAccount('EUR', fee_buy=2)
        assert False
    except TypeError:
        pass
    try:
        _ = account.FXAccount('EUR', fee_deposit=2)
        assert False
    except TypeError:
        pass
    try:
        _ = account.FXAccount('EUR', fee_withdraw=2)
        assert False
    except TypeError:
        pass

    # noinspection PyUnusedLocal
    def _fee(amount, price, base, quote, dur):
        return 0, 'EUR', 0

    _ = account.FXAccount('EUR', fee_sell=_fee)
    _ = account.FXAccount('EUR', fee_buy=_fee)
    _ = account.FXAccount('EUR', fee_withdraw=_fee)
    _ = account.FXAccount('EUR', fee_deposit=_fee)


def test_set_exec_heap():
    acc = account.FXAccount('EUR')

    heap = acc._parse_exec_heap([10, 'withdraw', 10, 'EUR', 'except'], False)
    assert heap == [[10, 'c_withdraw', 10, 'EUR', 'except']]

    heap = acc._parse_exec_heap((11, 'c_withdraw', 11, 'EUR', 'except'), False)
    assert heap == [[11, 'c_withdraw', 11, 'EUR', 'except']]

    heap = acc._parse_exec_heap([[12, 'deposit', 12, 'EUR', 'except']], False)
    assert heap == [[12, 'c_deposit', 12, 'EUR', 'except']]

    heap = acc._parse_exec_heap([(13, 'c_deposit', 13, 'BTC', 'except')], False)
    assert heap == [[13, 'c_deposit', 13, 'BTC', 'except']]

    # noinspection PyRedundantParentheses
    heap = acc._parse_exec_heap(((14, 'deposit', 14, 'EUR', 'except')), False)
    assert heap == [[14, 'c_deposit', 14, 'EUR', 'except']]

    heap = acc._parse_exec_heap(([15, 'c_deposit', 15, 'EUR', 'except']), False)
    assert heap == [[15, 'c_deposit', 15, 'EUR', 'except']]

    try:
        acc._parse_exec_heap([10, 'something', 10, 'EUR', 'except'], False)
        assert False
    except TypeError:
        pass

    try:
        acc._parse_exec_heap([10, 'withdraw', 'something', 'EUR', 'except'], False)
        assert False
    except TypeError:
        pass
    try:
        acc._parse_exec_heap([(13, 'c_deposit', 13, 3, 'except')], False)
        assert False
    except TypeError:
        pass


# todo: this test is damn broken! (in terms of clean and good code design...)
# noinspection PyTypeChecker
@pytest.mark.parametrize(
    'reference_currency, depot, exec_heap, clock, fee_sell, fee_buy, fee_deposit, '
    'fee_withdraw, exchange_rates, check_marked_coverage',
    [['EUR', {'EUR': 1}, (1, 'withdraw', 1, 'EUR', 'except'), 1, False, False, False, False, {('EUR', 'USD'): 0.5},
      'min_backward'],
     ['USD', {'BTC': 1}, [(1, 'deposit', 1, 'EUR', 'except')], 3, False, False, False, False, {('EUR', 'USD'): 1.2},
      None]])
def test_init_arguments(reference_currency, depot, exec_heap, clock, fee_sell, fee_buy,
                        fee_deposit, fee_withdraw, exchange_rates, check_marked_coverage):
    acc = account.FXAccount(reference_currency, depot, fee_sell, fee_buy,
                            fee_deposit, fee_withdraw, exec_heap, clock, exchange_rates, check_marked_coverage)

    assert acc.reference_currency == reference_currency
    assert type(acc.depot) == ProtectedDict
    assert len(acc.depot) == len(depot)
    assert type(acc.exec_heap) == ProtectedExecHeap
    assert acc.clock == clock
    assert type(acc._fee) == ProtectedDict
    assert type(acc.exchange_rates) == ProtectedDict

    if type(depot) == dict:
        assert acc.depot == depot
    if exec_heap is None or (type(exec_heap) in [tuple, list] and len(exec_heap) == 0):
        exec_heap = []
    else:
        try:
            _ = len(exec_heap[0])

            # if no exception, then 2D input
            if tuple(exec_heap) == exec_heap:
                exec_heap = list(exec_heap)
            for i in range(len(exec_heap)):
                if 'c_' not in exec_heap[i][1]:
                    # noinspection PyTypeChecker
                    exec_heap[i][1] = ''.join(['c_', exec_heap[i][1]])
                if len(exec_heap[i]) != 5:
                    # noinspection PyTypeChecker
                    exec_heap[i] = [exec_heap[i][0], exec_heap[i][1], exec_heap[i][2], exec_heap[i][3], 'except']
        except (TypeError, IndexError, KeyError, ValueError):
            # 1D input
            action_type = exec_heap[1]
            if 'c_' not in action_type:
                action_type = ''.join(['c_', action_type])
            exec_heap = [[exec_heap[0], action_type, exec_heap[2], exec_heap[3], 'except']]
    assert acc.exec_heap == exec_heap

    if fee_sell is False:
        assert acc._fee['sell'].__name__ == 'fx_null_fee'
    else:
        assert acc._fee['sell'] == fee_sell

    if fee_buy is False:
        assert acc._fee['buy'].__name__ == 'fx_null_fee'
    else:
        assert acc._fee['buy'] == fee_buy

    if fee_deposit is False:
        assert acc._fee['deposit'].__name__ == 'fx_null_fee'
    else:
        assert acc._fee['deposit'] == fee_deposit

    if fee_withdraw is False:
        assert acc._fee['withdraw'].__name__ == 'fx_null_fee'
    else:
        assert acc._fee['withdraw'] == fee_withdraw

    assert type(acc.exchange_rates) == ProtectedDict
    if type(exchange_rates) == dict:
        assert acc.exchange_rates == exchange_rates


def test_clock():
    acc = account.FXAccount('EUR')
    try:
        acc.tick('something')
        assert False
    except TypeError:
        pass
    try:
        acc.tick(-1)
        assert False
    except TypeError:
        pass
    acc.tick(None)
    assert acc.clock == 1
    acc.tick(100)
    assert acc.clock == 100
    try:
        acc.clock = -1
        assert False
    except ValueError:
        pass


def test_check_types():
    w = False
    x = 'x'
    y = 1
    z = 2.0

    check_types([w, x, y, z], [bool, str, int, float], ['w', 'x', 'y', 'z'])
    try:
        check_types([w, x, y, z], [float, bool, int, str], ['w', 'x', 'y', 'z'])
        assert False
    except TypeError:
        pass


# noinspection PyUnusedLocal
def test_fill_fee():
    acc = account.FXAccount('EUR', depot={'EUR': 100})

    # check depot and execution handler

    # --- delayed execution
    fee_amount, fee_currency, fee_exec_duration = acc._fill_fee('sell', False, 100, 1, 'EUR', 'BTC', 10)
    assert fee_amount == 0
    assert fee_currency == 'EUR'
    assert fee_exec_duration == 0 or fee_exec_duration is None

    fee_amount, fee_currency, fee_exec_duration = acc._fill_fee('buy', None, 100, 1, 'EUR', 'BTC', 20)
    assert fee_amount == 0
    assert fee_currency == 'EUR'
    assert fee_exec_duration == 0 or fee_exec_duration is None

    fee_amount, fee_currency, fee_exec_duration = acc._fill_fee('transfer', 50, 100, 1, 'EUR', 'BTC', 30)
    assert fee_amount == 50
    assert fee_currency == 'EUR'
    assert fee_exec_duration == 30

    # noinspection PyUnusedLocal
    def _fee(amount, price, base, quote, execution_time):
        return amount * price, quote, execution_time * 0.5

    try:
        fee_amount, fee_currency, fee_exec_duration = acc._fill_fee('sell', _fee, 100, 1, 'EUR', 'BTC', 40)
        assert False
    except PositionNAError:
        pass
    save_depot = acc.depot.copy()
    acc._c_depot[b'BTC'] = 100
    fee_amount, fee_currency, fee_exec_duration = acc._fill_fee('buy', _fee, 100, 1, 'EUR', 'BTC', 40)
    assert fee_amount == 100 * 1
    assert fee_currency == 'BTC'
    assert fee_exec_duration == 20
    acc.depot = save_depot

    heap = acc.exec_heap
    assert heap[0][0] == 20
    assert type(heap[0][1]) == str
    assert heap[0][2] == 100
    assert heap[0][3] == 'BTC'

    # --- instant execution
    fee_amount, fee_currency, fee_exec_duration = acc._fill_fee('withdraw', False, 100, 1, 'EUR', 'BTC', 0)
    assert acc.depot['EUR'] == 100

    fee_amount, fee_currency, fee_exec_duration = acc._fill_fee('deposit', None, 100, 1, 'EUR', 'BTC', 0)
    assert acc.depot['EUR'] == 100

    fee_amount, fee_currency, fee_exec_duration = acc._fill_fee('withdraw', 50, 100, 1, 'EUR', 'BTC', 0)
    assert acc.depot['EUR'] == 50

    # noinspection PyUnusedLocal
    def _fee(amount, price, base, quote, execution_time):
        return amount * price, quote, execution_time * 3

    try:
        fee_amount, fee_currency, fee_exec_duration = acc._fill_fee('buy', _fee, 100, 1, 'EUR', 'BTC', 0)
        assert False
    except PositionNAError:
        pass
    try:
        fee_amount, fee_currency, fee_exec_duration = acc._fill_fee('sell', _fee, 100, 1, 'EUR', 'EUR', 0)
        assert False
    except CoverageError:
        pass
    fee_amount, fee_currency, fee_exec_duration = acc._fill_fee('withdraw', _fee, 50, 1, 'EUR', 'EUR', 0)
    assert acc.depot['EUR'] == 0

    # no ticks performed, so exec_heap should be unchanged
    heap = acc.exec_heap
    assert heap[0][0] == 20
    assert type(heap[0][1]) == str
    assert heap[0][2] == 100
    assert heap[0][3] == 'BTC'

    # assign internal fee function
    acc._c_fee[b'sell'] = _fee
    acc._c_depot[b'EUR'] = 100000
    acc._c_depot[b'BTC'] = 1000
    fee_amount, fee_currency, fee_exec_duration = acc._fill_fee('sell', None, 10, 2, 'EUR', 'EUR', 1)
    assert [acc.clock + 3, 'c_withdraw', 20, 'EUR', 'except'] in acc.exec_heap
    fee_amount, fee_currency, fee_exec_duration = acc._fill_fee('sell', None, 10, 2, 'EUR', 'EUR', 0)
    acc._c_depot[b'BTC'] = 1000 - 20

    # --- check exceptions
    try:
        acc._fill_fee('sell', None, -2, 'EUR', 1, 'EUR', 0)
        assert False
    except (ValueError, TypeError) as e:
        pass
    try:
        acc._fill_fee('buy', None, 'test', 'EUR', 1, 'EUR', 0)
        assert False
    except TypeError:
        pass

    try:
        acc._fee['sell'] = _fee
        assert False
    except AttributeError:
        pass
    try:
        acc.depot['EUR'] = 1000
        assert False
    except AttributeError:
        pass


# noinspection PyUnusedLocal,PyTypeChecker
def test_exceptions_with_input_types_to_sell():
    acc = account.FXAccount('EUR', depot={'EUR': 31, 'BTC': 139.0},
                            exec_heap=[(22, 'deposit', 66, 'BTC', 'except'),
                                       (22, 'withdraw', 33, 'EUR', 'except')])

    # --- check exceptions
    try:
        acc.sell(100, 2, 'EUR', 'BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.sell(100, 2, 'EUR', 'BTC', coverage='something')
        assert False
    except NotImplementedError:
        pass
    try:
        acc.sell(100, 2, 'EUR', 'BTC', processing_duration=10)
        assert False
    except CoverageError:
        pass
    try:
        acc.sell(100, 2, 'EUR', 'BTC', coverage='something', processing_duration=10)
        assert False
    except NotImplementedError:
        pass
    try:
        acc.sell(100, 2, 'EUR', 'BTC', fee=100, processing_duration=10)
        assert False
    except CoverageError:
        pass
    try:
        acc.sell(100, 2, 'EUR', 'BTC', fee=100, processing_duration=10, coverage='partial')
        assert False
    except CoverageError:
        pass
    try:
        acc.sell(1, 2, 'EUR', 'BTC', fee=100, processing_duration=10)
        assert False
    except CoverageError:
        pass
    try:
        acc.sell(100, 2, 'EUR', 'BTC', coverage='something', processing_duration=10, fee=100)
        assert False
    except NotImplementedError:
        pass
    try:
        acc.sell('test', 1, 'EUR', 'BTC')
        assert False
    except TypeError:
        pass
    try:
        acc.sell(-1, 1, 'EUR', 'BTC')
        assert False
    except ValueError:
        pass
    try:
        acc.sell(1, 1, 3, 'BTC')
        assert False
    except TypeError:
        pass
    try:
        acc.sell(1, 1, 'EUR', 'BTC', fee='something')
        assert False
    except NotImplementedError:
        pass
    try:
        acc.sell(1, 1, 'EUR', 'BTC', processing_duration='something')
        assert False
    except TypeError:
        pass
    try:
        acc.sell(1, 1, 'EUR', 'BTC', coverage='something', fee=100)
        assert False
    except NotImplementedError:
        pass
    try:
        acc.sell(100, 1, 'EUR', 'BTC', coverage='something')
        assert False
    except NotImplementedError:
        pass
    try:
        acc.sell(1, 1, 'EUR', 'BTC', coverage='except', fee=100000,
                 float_fee_currency='quote')
        assert False
    except PositionNAError:
        pass
    try:
        acc.sell(1, 1, 'EUR', 'BTC', coverage='except', fee=100000,
                 float_fee_currency='something')
        assert False
    except PositionNAError:
        pass
    try:
        acc.sell(1, 1, 'EUR', 'BTC', coverage='except', fee=1,
                 float_fee_currency='something')
        assert False
    except PositionNAError:
        pass

    try:
        acc.sell(1, 1, 'EUR', 'BTC', coverage='except', fee=1, float_fee_currency=3)
        assert False
    except TypeError:
        pass


# noinspection PyUnusedLocal,PyTypeChecker
def test_continuous_sell_series_hardcoded():
    # fixed coverage: exception
    # base|quote: not swapped
    # Perform a series of buy orders with different settings regarding fees, execution duration,
    # withdrawal duration (nominal value of buy order) and fee withdrawal duration. Then check account depot and clock.
    # Clock ticking is performed continuous to simulate live behavior

    base = 'EUR'
    quote = 'BTC'

    # noinspection PyUnusedLocal
    def _fee(_amount, _price, _base, _quote, execution_time):
        return 0.5 * _amount, _quote, 2

    acc = account.FXAccount('EUR')
    acc._c_depot[base.encode()] = 60
    acc._c_depot[quote.encode()] = 20

    # 1 transaction
    acc.sell(5, 2, base, quote, fee=_fee, processing_duration=3, instant_withdrawal=True)
    assert acc.clock == 0
    assert acc.depot[base] == 55
    assert acc.depot[quote] == 20

    acc.tick()  # 1
    # 2 transaction
    acc.sell(20, 2, base, quote)
    assert acc.clock == 1
    assert acc.depot[base] == 35
    assert acc.depot[quote] == 60

    acc.tick()  # 2
    # 3 transaction
    acc.sell(10, 2, base, quote, fee=10, processing_duration=3)
    assert acc.clock == 2
    assert acc.depot[base] == 35
    assert acc.depot[quote] == 57.5

    acc.tick()  # 3
    assert acc.clock == 3
    assert acc.depot[base] == 35
    assert acc.depot[quote] == 67.5

    acc.tick()  # 4
    # 4 transaction
    acc.sell(5, 2, base, quote, fee=_fee)
    assert acc.clock == 4
    assert acc.depot[base] == 30
    assert acc.depot[quote] == 77.5

    acc.tick()  # 5
    assert acc.clock == 5
    assert acc.depot[base] == 10
    assert acc.depot[quote] == 97.5

    acc.tick()  # 6
    # 5 transaction
    acc.sell(10, 2, base, quote, fee=_fee, processing_duration=3)
    assert acc.clock == 6
    assert acc.depot[base] == 10
    assert acc.depot[quote] == 95

    acc.tick()  # 7
    acc._c_depot[base.encode()] += 50
    assert acc.clock == 7
    assert acc.depot[base] == 60
    assert acc.depot[quote] == 95

    acc.tick()  # 8
    # 6 transaction
    acc.sell(10, 2, base, quote, fee=_fee, processing_duration=1, instant_withdrawal=True)
    assert acc.clock == 8
    assert acc.depot[base] == 50
    assert acc.depot[quote] == 90

    acc.tick()  # 9
    # 7 transaction
    acc.sell(5, 2, base, quote, processing_duration=1, instant_withdrawal=True)
    assert acc.clock == 9
    assert acc.depot[base] == 35
    assert acc.depot[quote] == 130

    acc.tick()  # 10
    assert acc.clock == 10
    assert acc.depot[base] == 35
    assert acc.depot[quote] == 135

    acc.tick()  # 11
    # 8 transaction
    acc.sell(1, 2, base, quote, fee=1, instant_withdrawal=True)
    assert acc.clock == 11
    assert acc.depot[base] == 33
    assert acc.depot[quote] == 137

    acc.tick()  # 12
    assert acc.clock == 12
    assert acc.depot[base] == 33
    assert acc.depot[quote] == 137

    acc.tick()  # 13
    acc.sell(1, 2, base, quote, fee=1, instant_float_fee=True, processing_duration=2)
    assert acc.clock == 13
    assert acc.depot[base] == 32
    assert acc.depot[quote] == 137

    acc.tick()  # 14
    acc._c_fee[b'sell'] = _fee
    acc.sell(2, 4, base, quote, fee=None)
    assert acc.clock == 14
    assert acc.depot[base] == 30
    assert acc.depot[quote] == 145

    acc.tick()  # 15
    assert acc.clock == 15
    assert acc.depot[base] == 29
    assert acc.depot[quote] == 147

    acc.tick()  # 16
    assert acc.clock == 16
    assert acc.depot[base] == 29
    assert acc.depot[quote] == 146

    acc.tick()  # 17
    acc.sell(1, 2, base, quote, fee=False)
    assert acc.clock == 17
    assert acc.depot[base] == 28
    assert acc.depot[quote] == 148

    acc.tick()  # 18
    acc.sell(1, 2, base, quote, fee=1, processing_duration=2, instant_withdrawal=True, instant_float_fee=True)
    assert acc.clock == 18
    assert [acc.clock + 2, 'c_deposit', 2.0, quote, 'except'] in acc.exec_heap
    assert acc.depot[base] == 26
    assert acc.depot[quote] == 148

    acc.tick()  # 19
    acc.sell(1, 2, base, quote, fee=1, processing_duration=2, instant_withdrawal=True, instant_float_fee=True,
             float_fee_currency=quote)
    assert acc.clock == 19
    assert [acc.clock + 2, 'c_deposit', 2.0, quote, 'except'] in acc.exec_heap
    assert acc.depot[base] == 25
    assert acc.depot[quote] == 147


# noinspection PyUnusedLocal,PyTypeChecker
def test_float_fee_currency_sell():
    base = 'EUR'
    quote = 'BTC'

    # noinspection PyUnusedLocal
    def _fee(_amount, _price, _base, _quote, execution_time):
        return 0.5 * _amount, _quote, 2

    acc = account.FXAccount('EUR')
    acc._c_depot[base.encode()] = 60
    acc._c_depot[quote.encode()] = 20

    # set float_fee_currency to quote, as float_fee_currency='base' by default and tested
    # in test_continuous_sell_series_hardcoded:
    #   instant exchange
    acc.sell(5, 2, base, quote, fee=5, float_fee_currency=quote)
    assert acc.depot[base] == 55
    assert acc.depot[quote] == 25
    #   delayed exchange
    acc.sell(5, 2, base, quote, fee=5, processing_duration=10, float_fee_currency=quote)
    assert acc.depot[base] == 55
    assert acc.depot[quote] == 25
    try:
        acc.sell(5, 2, base, quote, fee=500, processing_duration=10, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    acc.tick(5)
    assert acc.depot[base] == 55
    assert acc.depot[quote] == 25
    acc.tick(10)
    assert acc.depot[base] == 50
    assert acc.depot[quote] == 30

    #   delayed exchange, instant withdrawal
    acc.sell(5, 2, base, quote, fee=5, processing_duration=10, float_fee_currency=quote, instant_withdrawal=True)
    assert acc.depot[base] == 45
    assert acc.depot[quote] == 30
    try:
        acc.sell(5, 2, base, quote, fee=500, processing_duration=10, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    acc.tick(15)
    assert acc.depot[base] == 45
    assert acc.depot[quote] == 30
    acc.tick(20)
    assert acc.depot[base] == 45
    assert acc.depot[quote] == 35

    #   delayed exchange, instant fee
    acc.sell(5, 2, base, quote, fee=5, processing_duration=10, float_fee_currency=quote, instant_float_fee=True)
    acc.tick(25)
    assert acc.depot[base] == 45
    assert acc.depot[quote] == 30
    acc.tick(30)
    assert acc.depot[base] == 40
    assert acc.depot[quote] == 40
    acc.tick(40)

    # no effect if: alt_fee not float
    # instant
    acc.sell(5, 2, base, quote, fee=_fee, float_fee_currency=quote)  # fee: return 0.5 * _amount, _quote, 2
    assert acc.depot[base] == 35
    assert acc.depot[quote] == 50
    acc.tick(42)
    assert acc.depot[quote] == 47.5

    acc.sell(5, 2, base, quote, fee=_fee, float_fee_currency=quote, instant_float_fee=True)
    assert acc.depot[base] == 30
    assert acc.depot[quote] == 57.5
    acc.tick(44)
    assert acc.depot[quote] == 55

    # delayed
    acc.sell(5, 2, base, quote, fee=_fee, processing_duration=5, float_fee_currency=quote, instant_float_fee=True)
    assert acc.depot[base] == 30
    assert acc.depot[quote] == 55
    acc.tick(46)
    assert acc.depot[base] == 30
    assert acc.depot[quote] == 52.5
    acc.tick(49)
    assert acc.depot[base] == 25
    assert acc.depot[quote] == 62.5
    acc.sell(5, 2, base, quote, fee=_fee, processing_duration=5, float_fee_currency=quote, instant_float_fee=True,
             instant_withdrawal=True)
    assert acc.depot[base] == 20
    assert acc.depot[quote] == 62.5
    acc.tick(54)
    assert acc.depot[base] == 20
    assert acc.depot[quote] == 70

    # third float fee currency
    acc._c_depot[b'YEN'] = 200
    acc.sell(5, 2, base, quote, fee=5, float_fee_currency='YEN')
    assert acc.depot[base] == 15
    assert acc.depot[quote] == 80
    assert acc.depot['YEN'] == 195


# noinspection PyUnusedLocal,PyTypeChecker
def test_swapped_base_quote_order_in_continuous_sell_series_hardcoded():
    # fixed coverage: exception
    # base|quote: swapped
    # Perform a series of buy orders with different settings regarding fees, execution duration,
    # withdrawal duration (nominal value of buy order) and fee withdrawal duration. Then check account depot and clock.
    # Clock ticking is performed continuous to simulate live behavior

    base = 'BTC'
    quote = 'EUR'

    # noinspection PyUnusedLocal
    def _fee(_amount, _price, _base, _quote, execution_time):
        return 0.5 * _amount, _quote, 2

    acc = account.FXAccount('EUR')
    acc._c_depot[base.encode()] = 60
    acc._c_depot[quote.encode()] = 20

    # 1 transaction
    acc.sell(5, 2, base, quote, fee=_fee, processing_duration=3, instant_withdrawal=True)
    assert acc.clock == 0
    assert acc.depot[base] == 55
    assert acc.depot[quote] == 20

    acc.tick()  # 1
    # 2 transaction
    acc.sell(20, 2, base, quote)
    assert acc.clock == 1
    assert acc.depot[base] == 35
    assert acc.depot[quote] == 60

    acc.tick()  # 2
    # 3 transaction
    acc.sell(10, 2, base, quote, fee=10, processing_duration=3)
    assert acc.clock == 2
    assert acc.depot[base] == 35
    assert acc.depot[quote] == 57.5

    acc.tick()  # 3
    assert acc.clock == 3
    assert acc.depot[base] == 35
    assert acc.depot[quote] == 67.5

    acc.tick()  # 4
    # 4 transaction
    acc.sell(5, 2, base, quote, fee=_fee)
    assert acc.clock == 4
    assert acc.depot[base] == 30
    assert acc.depot[quote] == 77.5

    acc.tick()  # 5
    assert acc.clock == 5
    assert acc.depot[base] == 10
    assert acc.depot[quote] == 97.5

    acc.tick()  # 6
    # 5 transaction
    acc.sell(10, 2, base, quote, fee=_fee, processing_duration=3)
    assert acc.clock == 6
    assert acc.depot[base] == 10
    assert acc.depot[quote] == 95

    acc.tick()  # 7
    acc._c_depot[base.encode()] += 50
    assert acc.clock == 7
    assert acc.depot[base] == 60
    assert acc.depot[quote] == 95

    acc.tick()  # 8
    # 6 transaction
    acc.sell(10, 2, base, quote, fee=_fee, processing_duration=1, instant_withdrawal=True)
    assert acc.clock == 8
    assert acc.depot[base] == 50
    assert acc.depot[quote] == 90

    acc.tick()  # 9
    # 7 transaction
    acc.sell(5, 2, base, quote, processing_duration=1, instant_withdrawal=True)
    assert acc.clock == 9
    assert acc.depot[base] == 35
    assert acc.depot[quote] == 130

    acc.tick()  # 10
    assert acc.clock == 10
    assert acc.depot[base] == 35
    assert acc.depot[quote] == 135

    acc.tick()  # 11
    # 8 transaction
    acc.sell(1, 2, base, quote, fee=1, instant_withdrawal=True)
    assert acc.clock == 11
    assert acc.depot[base] == 33
    assert acc.depot[quote] == 137

    acc.tick()  # 12
    assert acc.clock == 12
    assert acc.depot[base] == 33
    assert acc.depot[quote] == 137

    acc.tick()  # 13
    acc.sell(1, 2, base, quote, fee=1, instant_float_fee=True, processing_duration=2)
    assert acc.clock == 13
    assert acc.depot[base] == 32
    assert acc.depot[quote] == 137

    acc.tick()  # 14
    acc._c_fee[b'sell'] = _fee
    acc.sell(2, 4, base, quote, fee=None)
    assert acc.clock == 14
    assert acc.depot[base] == 30
    assert acc.depot[quote] == 145

    acc.tick()  # 15
    assert acc.clock == 15
    assert acc.depot[base] == 29
    assert acc.depot[quote] == 147

    acc.tick()  # 16
    assert acc.clock == 16
    assert acc.depot[base] == 29
    assert acc.depot[quote] == 146

    acc.tick()  # 17
    acc.sell(1, 2, base, quote, fee=False)
    assert acc.clock == 17
    assert acc.depot[base] == 28
    assert acc.depot[quote] == 148

    acc.tick()  # 18
    acc.sell(1, 2, base, quote, fee=1, processing_duration=2, instant_withdrawal=True, instant_float_fee=True)
    assert acc.clock == 18
    assert [acc.clock + 2, 'c_deposit', 2, quote, 'except'] in acc.exec_heap
    assert acc.depot[base] == 26
    assert acc.depot[quote] == 148

    acc.tick()  # 19
    acc.sell(1, 2, base, quote, fee=1, processing_duration=2, instant_withdrawal=True, instant_float_fee=True,
             float_fee_currency=quote)
    assert acc.clock == 19
    assert [acc.clock + 2, 'c_deposit', 2, quote, 'except'] in acc.exec_heap
    assert acc.depot[base] == 25
    assert acc.depot[quote] == 147


# noinspection PyUnusedLocal,PyTypeChecker
def test_tick_once_sell():
    base = 'EUR'
    quote = 'BTC'

    # noinspection PyUnusedLocal
    def _fee(_amount, _price, _base, _quote, execution_time):
        return 0.5 * _amount, _quote, 2

    # noinspection PyUnusedLocal,PyTypeChecker
    def setup_up():
        _acc = account.FXAccount('EUR')
        _acc._c_depot[base.encode()] = 60
        _acc._c_depot[quote.encode()] = 20

        _acc.sell(5, 2, base, quote)
        _acc.sell(10, 2, base, quote, fee=10, processing_duration=5, instant_withdrawal=True)
        _acc.sell(5, 3, base, quote, fee=5, processing_duration=5)
        _acc.sell(15, 2, base, quote, processing_duration=10)
        return _acc

    acc = setup_up()
    acc.tick(3)
    assert acc.clock == 3
    assert acc.depot[base] == 45
    assert acc.depot[quote] == 30
    acc.tick(6)
    assert acc.clock == 6
    assert acc.depot[base] == 25
    assert acc.depot[quote] == 65
    acc.tick(12)
    assert acc.clock == 12
    assert acc.depot[base] == 10
    assert acc.depot[quote] == 95

    acc = setup_up()
    acc.tick(8)
    assert acc.clock == 8
    assert acc.depot[base] == 25
    assert acc.depot[quote] == 65

    acc = setup_up()
    acc.tick(14)
    assert acc.clock == 14
    assert acc.depot[base] == 10
    assert acc.depot[quote] == 95

    acc = setup_up()
    acc.sell(1, 2, base, quote, processing_duration=8)
    acc.tick(6)
    assert acc.clock == 6
    assert acc.depot[base] == 25
    assert acc.depot[quote] == 65
    acc.tick(7)
    assert acc.clock == 7
    assert acc.depot[base] == 25
    assert acc.depot[quote] == 65
    acc.tick(9)
    assert acc.clock == 9
    assert acc.depot[base] == 24
    assert acc.depot[quote] == 67
    acc.tick(14)
    assert acc.clock == 14
    assert acc.depot[base] == 9
    assert acc.depot[quote] == 97


# noinspection PyUnusedLocal,PyTypeChecker
def test_exceptions_with_input_types_to_buy():
    acc = account.FXAccount('EUR', depot={'EUR': 139, 'BTC': 31},
                            exec_heap=[(22, 'deposit', 66, 'BTC', 'except'), (22, 'withdraw', 33, 'EUR', 'except')])

    # --- check exceptions
    try:
        acc.buy(100, 2, 'EUR', 'BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(100, 2, 'EUR', 'BTC', coverage='something')
        assert False
    except NotImplementedError:
        pass
    try:
        acc.buy(100, 2, 'EUR', 'BTC', processing_duration=10)
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(100, 2, 'EUR', 'BTC', coverage='something', processing_duration=10)
        assert False
    except NotImplementedError:
        pass
    try:
        acc.buy(100, 2, 'EUR', 'BTC', fee=100, processing_duration=10)
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(100, 2, 'EUR', 'BTC', fee=100, processing_duration=10, coverage='partial',
                float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(1, 2, 'EUR', 'BTC', fee=100, processing_duration=10, float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(100, 2, 'EUR', 'BTC', coverage='something', processing_duration=10, fee=100)
        assert False
    except NotImplementedError:
        pass
    try:
        acc.buy('test', 1, 'EUR', 'BTC')
        assert False
    except TypeError:
        pass
    try:
        acc.buy(-1, 1, 'EUR', 'BTC')
        assert False
    except ValueError:
        pass
    try:
        acc.buy(1, 1, 3, 'BTC')
        assert False
    except TypeError:
        pass
    try:
        acc.buy(1, 1, 'EUR', 'BTC', fee='something')
        assert False
    except NotImplementedError:
        pass
    try:
        acc.buy(1, 1, 'EUR', 'BTC', processing_duration='something')
        assert False
    except TypeError:
        pass
    try:
        acc.buy(1, 1, 'EUR', 'BTC', coverage='something', fee=100)
        assert False
    except NotImplementedError:
        pass
    try:
        acc.buy(100, 1, 'EUR', 'BTC', coverage='something')
        assert False
    except NotImplementedError:
        pass
    try:
        acc.buy(1, 1, 'EUR', 'BTC', coverage='except', fee=100000,
                float_fee_currency='quote')
        assert False
    except PositionNAError:
        pass
    try:
        acc.buy(1, 1, 'EUR', 'BTC', coverage='except', fee=100000,
                float_fee_currency='something')
        assert False
    except PositionNAError:
        pass
    try:
        acc.buy(1, 1, 'EUR', 'BTC', coverage='except', fee=1,
                float_fee_currency='something')
        assert False
    except PositionNAError:
        pass
    try:
        acc.buy(1, 1, 'EUR', 'BTC', coverage='except', fee=1, float_fee_currency=3)
        assert False
    except TypeError:
        pass


# noinspection PyUnusedLocal,PyTypeChecker
def test_continuous_buy_series_hardcoded():
    # fixed coverage: exception
    # base|quote: not swapped
    # Perform a series of sell orders with different settings regarding fees, execution duration,
    # withdrawal duration (nominal value of sell order) and fee withdrawal duration. Then check account depot and clock.
    # Clock ticking is performed continuous to simulate live behavior

    base = 'EUR'
    quote = 'BTC'

    # noinspection PyUnusedLocal
    def _fee(_amount, _price, _base, _quote, execution_time):
        return 0.5 * _amount * _price, _base, 2

    acc = account.FXAccount('EUR')
    acc._c_depot[quote.encode()] = 60
    acc._c_depot[base.encode()] = 20

    # 1 transaction
    acc.buy(2 * 5, 0.5, base, quote, fee=_fee, processing_duration=3, instant_withdrawal=True)
    assert acc.clock == 0
    assert acc.depot[quote] == 55
    assert acc.depot[base] == 20

    acc.tick()  # 1
    # 2 transaction
    acc.buy(2*20, 0.5, base, quote)
    assert acc.clock == 1
    assert acc.depot[quote] == 35
    assert acc.depot[base] == 60

    acc.tick()  # 2
    # 3 transaction
    acc.buy(2 * 10, 0.5, base, quote, fee=10, processing_duration=3, float_fee_currency=quote)
    assert acc.clock == 2
    assert acc.depot[quote] == 35
    assert acc.depot[base] == 57.5

    acc.tick()  # 3
    assert acc.clock == 3
    assert acc.depot[quote] == 35
    assert acc.depot[base] == 67.5

    acc.tick()  # 4
    # 4 transaction
    acc.buy(2 * 5, 0.5, base, quote, fee=_fee)
    assert acc.clock == 4
    assert acc.depot[quote] == 30
    assert acc.depot[base] == 77.5

    acc.tick()  # 5
    assert acc.clock == 5
    assert acc.depot[quote] == 10
    assert acc.depot[base] == 97.5

    acc.tick()  # 6
    # 5 transaction
    acc.buy(2 * 10, 0.5, base, quote, fee=_fee, processing_duration=3)
    assert acc.clock == 6
    assert acc.depot[quote] == 10
    assert acc.depot[base] == 95

    acc.tick()  # 7
    acc._c_depot[quote.encode()] += 50
    assert acc.clock == 7
    assert acc.depot[quote] == 60
    assert acc.depot[base] == 95

    acc.tick()  # 8
    # 6 transaction
    acc.buy(2 * 10, 0.5, base, quote, fee=_fee, processing_duration=1, instant_withdrawal=True)
    assert acc.clock == 8
    assert acc.depot[quote] == 50
    assert acc.depot[base] == 90

    acc.tick()  # 9
    # 7 transaction
    acc.buy(2*5, 0.5, base, quote, processing_duration=1, instant_withdrawal=True)
    assert acc.clock == 9
    assert acc.depot[quote] == 35
    assert acc.depot[base] == 130

    acc.tick()  # 10
    assert acc.clock == 10
    assert acc.depot[quote] == 35
    assert acc.depot[base] == 135

    acc.tick()  # 11
    # 8 transaction
    acc.buy(2 * 1, 0.5, base, quote, fee=1, instant_withdrawal=True, float_fee_currency=quote)
    assert acc.clock == 11
    assert acc.depot[quote] == 33
    assert acc.depot[base] == 137

    acc.tick()  # 12
    assert acc.clock == 12
    assert acc.depot[quote] == 33
    assert acc.depot[base] == 137

    acc.tick()  # 13
    acc.buy(2 * 1, 0.5, base, quote, fee=1, instant_float_fee=True, processing_duration=2, float_fee_currency=quote)
    assert acc.clock == 13
    assert acc.depot[quote] == 32
    assert acc.depot[base] == 137

    acc.tick()  # 14
    acc._c_fee[b'buy'] = _fee
    acc.buy(4 * 2, 0.25, base, quote, fee=None)
    assert acc.clock == 14
    assert acc.depot[quote] == 30
    assert acc.depot[base] == 145

    acc.tick()  # 15
    assert acc.clock == 15
    assert acc.depot[quote] == 29
    assert acc.depot[base] == 147

    acc.tick()  # 16
    assert acc.clock == 16
    assert acc.depot[quote] == 29
    assert acc.depot[base] == 146

    acc.tick()  # 17
    acc.buy(2 * 1, 0.5, base, quote, fee=False)
    assert acc.clock == 17
    assert acc.depot[quote] == 28
    assert acc.depot[base] == 148

    acc.tick()  # 18
    acc.buy(2 * 1, 0.5, base, quote, fee=1, processing_duration=2, instant_withdrawal=True, instant_float_fee=True,
            float_fee_currency=quote)
    assert acc.clock == 18
    assert [acc.clock + 2, 'c_deposit', 2, base, 'except'] in acc.exec_heap
    assert acc.depot[quote] == 26
    assert acc.depot[base] == 148

    acc.tick()  # 19
    acc.buy(2 * 1, 0.5, base, quote, fee=1, processing_duration=2, instant_withdrawal=True, instant_float_fee=True,
            float_fee_currency=quote)
    assert acc.clock == 19
    assert [acc.clock + 2, 'c_deposit', 2, base, 'except'] in acc.exec_heap
    assert acc.depot[quote] == 24
    assert acc.depot[base] == 148

    acc.tick(200)
    pos_base = acc.depot[base]
    pos_quote = acc.depot[quote]
    acc.buy(1, 1, base, quote, fee=1)
    assert acc.depot[base] == pos_base + 1 - 1
    assert acc.depot[quote] == pos_quote - 1


# noinspection PyUnusedLocal,PyTypeChecker
def test_swapped_base_quote_order_in_continuous_buy_series_hardcoded():
    # fixed coverage: exception
    # base|quote: swapped
    # Perform a series of sell orders with different settings regarding fees, execution duration,
    # withdrawal duration (nominal value of sell order) and fee withdrawal duration. Then check account depot and clock.
    # Clock ticking is performed continuous to simulate live behavior

    base = 'BTC'
    quote = 'EUR'

    # noinspection PyUnusedLocal
    def _fee(_amount, _price, _base, _quote, execution_time):
        return 0.5 * _amount * _price, _base, 2

    acc = account.FXAccount('EUR')
    acc._c_depot[quote.encode()] = 60
    acc._c_depot[base.encode()] = 20

    # 1 transaction
    acc.buy(2 * 5, 0.5, base, quote, fee=_fee, processing_duration=3, instant_withdrawal=True)
    assert acc.clock == 0
    assert acc.depot[quote] == 55
    assert acc.depot[base] == 20

    acc.tick()  # 1
    # 2 transaction
    acc.buy(2*20, 0.5, base, quote)
    assert acc.clock == 1
    assert acc.depot[quote] == 35
    assert acc.depot[base] == 60

    acc.tick()  # 2
    # 3 transaction
    acc.buy(2 * 10, 0.5, base, quote, fee=10, processing_duration=3, float_fee_currency=quote)
    assert acc.clock == 2
    assert acc.depot[quote] == 35
    assert acc.depot[base] == 57.5

    acc.tick()  # 3
    assert acc.clock == 3
    assert acc.depot[quote] == 35
    assert acc.depot[base] == 67.5

    acc.tick()  # 4
    # 4 transaction
    acc.buy(2 * 5, 0.5, base, quote, fee=_fee)
    assert acc.clock == 4
    assert acc.depot[quote] == 30
    assert acc.depot[base] == 77.5

    acc.tick()  # 5
    assert acc.clock == 5
    assert acc.depot[quote] == 10
    assert acc.depot[base] == 97.5

    acc.tick()  # 6
    # 5 transaction
    acc.buy(2 * 10, 0.5, base, quote, fee=_fee, processing_duration=3)
    assert acc.clock == 6
    assert acc.depot[quote] == 10
    assert acc.depot[base] == 95

    acc.tick()  # 7
    acc._c_depot[quote.encode()] += 50
    assert acc.clock == 7
    assert acc.depot[quote] == 60
    assert acc.depot[base] == 95

    acc.tick()  # 8
    # 6 transaction
    acc.buy(2 * 10, 0.5, base, quote, fee=_fee, processing_duration=1, instant_withdrawal=True)
    assert acc.clock == 8
    assert acc.depot[quote] == 50
    assert acc.depot[base] == 90

    acc.tick()  # 9
    # 7 transaction
    acc.buy(2*5, 0.5, base, quote, processing_duration=1, instant_withdrawal=True)
    assert acc.clock == 9
    assert acc.depot[quote] == 35
    assert acc.depot[base] == 130

    acc.tick()  # 10
    assert acc.clock == 10
    assert acc.depot[quote] == 35
    assert acc.depot[base] == 135

    acc.tick()  # 11
    # 8 transaction
    acc.buy(2 * 1, 0.5, base, quote, fee=1, instant_withdrawal=True, float_fee_currency=quote)
    assert acc.clock == 11
    assert acc.depot[quote] == 33
    assert acc.depot[base] == 137

    acc.tick()  # 12
    assert acc.clock == 12
    assert acc.depot[quote] == 33
    assert acc.depot[base] == 137

    acc.tick()  # 13
    acc.buy(2 * 1, 0.5, base, quote, fee=1, instant_float_fee=True, processing_duration=2, float_fee_currency=quote)
    assert acc.clock == 13
    assert acc.depot[quote] == 32
    assert acc.depot[base] == 137

    acc.tick()  # 14
    acc._c_fee[b'buy'] = _fee
    acc.buy(4 * 2, 0.25, base, quote, fee=None)
    assert acc.clock == 14
    assert acc.depot[quote] == 30
    assert acc.depot[base] == 145

    acc.tick()  # 15
    assert acc.clock == 15
    assert acc.depot[quote] == 29
    assert acc.depot[base] == 147

    acc.tick()  # 16
    assert acc.clock == 16
    assert acc.depot[quote] == 29
    assert acc.depot[base] == 146

    acc.tick()  # 17
    acc.buy(2 * 1, 0.5, base, quote, fee=False)
    assert acc.clock == 17
    assert acc.depot[quote] == 28
    assert acc.depot[base] == 148

    acc.tick()  # 18
    acc.buy(2 * 1, 0.5, base, quote, fee=1, processing_duration=2, instant_withdrawal=True, instant_float_fee=True,
            float_fee_currency=quote)
    assert acc.clock == 18
    assert [acc.clock + 2, 'c_deposit', 2, base, 'except'] in acc.exec_heap
    assert acc.depot[quote] == 26
    assert acc.depot[base] == 148

    acc.tick()  # 19
    acc.buy(2 * 1, 0.5, base, quote, fee=1, processing_duration=2, instant_withdrawal=True, instant_float_fee=True,
            float_fee_currency=quote)
    assert acc.clock == 19
    assert [acc.clock + 2, 'c_deposit', 2, base, 'except'] in acc.exec_heap
    assert acc.depot[quote] == 24
    assert acc.depot[base] == 148

    acc.tick(200)
    pos_base = acc.depot[base]
    pos_quote = acc.depot[quote]
    acc.buy(1, 1, base, quote, fee=1)
    assert acc.depot[base] == pos_base + 1 - 1
    assert acc.depot[quote] == pos_quote - 1


# noinspection PyUnusedLocal,PyTypeChecker
def test_coverage_sell_buy_series_min_backward():
    acc = account.FXAccount('EUR')

    base = 'EUR'
    quote = 'BTC'

    acc.depot = {base: 100, quote: 100}

    # time 0
    acc.sell(10, 1, base, quote, fee=False, processing_duration=10)
    assert acc.depot[base] == 100
    assert acc.depot[quote] == 100

    acc.sell(10, 1, base, quote, fee=False, processing_duration=5)
    assert acc.depot[base] == 100
    assert acc.depot[quote] == 100

    acc.sell(90, 1, base, quote, fee=False, processing_duration=8)

    try:
        acc.sell(10, 1, base, quote, fee=False, processing_duration=12)
        assert False
    except CoverageError:
        pass

    acc.sell(90, 1, base, quote, fee=False, processing_duration=2)

    acc.buy(100, 1, base, quote, fee=False, processing_duration=3)

    acc.buy(100, 1, base, quote, fee=False, processing_duration=11)

    acc.sell(10, 1, base, quote, fee=False, processing_duration=12)

    acc.tick(12)
    assert acc.depot[base] == 90
    assert acc.depot[quote] == 110

    acc.sell(90, 1, base, quote, fee=False, processing_duration=3)
    acc.sell(10, 1, base, quote, fee=False, processing_duration=2)

    try:
        acc.tick(15)
        assert False
    except CoverageError:
        pass


# noinspection PyUnusedLocal,PyTypeChecker
def test_coverage_sell_buy_series_max_forward():
    acc = account.FXAccount('EUR', marked_coverage='max_forward')

    base = 'EUR'
    quote = 'BTC'

    acc.depot = {base: 100, quote: 100}

    # time 0
    acc.sell(10, 1, base, quote, fee=False, processing_duration=10)
    assert acc.depot[base] == 100
    assert acc.depot[quote] == 100

    acc.sell(10, 1, base, quote, fee=False, processing_duration=5)
    assert acc.depot[base] == 100
    assert acc.depot[quote] == 100

    try:
        acc.sell(90, 1, base, quote, fee=False, processing_duration=8)
        assert False
    except CoverageError:
        pass

    acc.sell(10, 1, base, quote, fee=False, processing_duration=12)

    try:
        acc.sell(90, 1, base, quote, fee=False, processing_duration=12)
        assert False
    except CoverageError:
        pass

    acc.buy(100, 1, base, quote, fee=False, processing_duration=3)

    try:
        acc.buy(100, 1, base, quote, fee=False, processing_duration=11)
        assert False
    except CoverageError:
        pass

    acc.sell(10, 1, base, quote, fee=False, processing_duration=12)

    acc.tick(12)
    assert acc.depot[base] == 160
    assert acc.depot[quote] == 40


# noinspection PyUnusedLocal,PyTypeChecker
def test_no_marked_coverage_sell_buy_series_with_coverage_debit():
    acc = account.FXAccount('EUR', marked_coverage=False)

    base = 'EUR'
    quote = 'BTC'

    check_marked_coverage = acc.check_marked_coverage

    acc.depot = {base: 100, quote: 100}

    # time 0
    acc.sell(10, 1, base, quote, fee=False, processing_duration=10, coverage='debit')
    assert acc.depot[base] == 100
    assert acc.depot[quote] == 100

    acc.sell(10, 1, base, quote, fee=False, processing_duration=5, coverage='debit')
    assert acc.depot[base] == 100
    assert acc.depot[quote] == 100

    acc.sell(90, 1, base, quote, fee=False, processing_duration=8, coverage='debit')
    assert acc.depot[base] == 100
    assert acc.depot[quote] == 100

    acc.sell(10, 1, base, quote, fee=False, processing_duration=12, coverage='debit')

    acc.sell(90, 1, base, quote, fee=False, processing_duration=12, coverage='debit')
    assert acc.depot[base] == 100
    assert acc.depot[quote] == 100

    acc.buy(100, 1, base, quote, fee=False, processing_duration=3, coverage='debit')

    acc.buy(100, 1, base, quote, fee=False, processing_duration=11, coverage='debit')
    assert acc.depot[base] == 100
    assert acc.depot[quote] == 100

    acc.sell(100, 1, base, quote, fee=False, processing_duration=12, coverage='debit')
    acc.buy(100, 1, base, quote, fee=False, processing_duration=20, coverage='debit')

    acc.tick(12)
    assert acc.depot[base] == -10
    assert acc.depot[quote] == 210

    acc.sell(100, 1, base, quote, fee=100, processing_duration=12, coverage='debit',
             instant_float_fee=True, float_fee_currency=base)
    assert acc.depot[base] == -110
    assert acc.depot[quote] == 210

    assert check_marked_coverage == acc.check_marked_coverage


# noinspection PyUnusedLocal,PyTypeChecker
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_no_marked_coverage_sell_buy_series_with_coverage_except():
    acc = account.FXAccount('EUR', marked_coverage=False)

    base = 'EUR'
    quote = 'BTC'

    acc.depot = {base: 100, quote: 100}

    # time 0
    acc.sell(10, 1, base, quote, fee=False, processing_duration=10, coverage='except')
    # 90, 110
    assert acc.depot[base] == 100
    assert acc.depot[quote] == 100

    acc.sell(10, 1, base, quote, fee=False, processing_duration=5, coverage='except')
    # 190, 10
    assert acc.depot[base] == 100
    assert acc.depot[quote] == 100

    acc.sell(90, 1, base, quote, fee=False, processing_duration=8, coverage='except')
    # 100, 100
    assert acc.depot[base] == 100
    assert acc.depot[quote] == 100

    acc.sell(10, 1, base, quote, fee=False, processing_duration=12, coverage='except')

    acc.sell(90, 1, base, quote, fee=False, processing_duration=12, coverage='except')
    assert acc.depot[base] == 100
    assert acc.depot[quote] == 100

    acc.buy(100, 1, base, quote, fee=False, processing_duration=3, coverage='except')
    # 200, 100

    acc.buy(100, 1, base, quote, fee=False, processing_duration=11, coverage='except')
    # except
    assert acc.depot[base] == 100
    assert acc.depot[quote] == 100

    acc.sell(100, 1, base, quote, fee=False, processing_duration=12, coverage='except')
    acc.buy(100, 1, base, quote, fee=False, processing_duration=20, coverage='except')

    try:
        acc.tick(12)
        assert False
    except CoverageError:
        pass
    assert acc.depot[base] < 100
    assert acc.depot[quote] == 210


# noinspection PyUnusedLocal,PyTypeChecker
def test_instant_float_fee_ignored_when_alt_fee_is_func():
    acc = account.FXAccount('EUR')

    # noinspection PyUnusedLocal
    def _fee(amount, price, base, quote, processing_duration):
        return amount * price, base, 10

    acc._c_depot[b'EUR'] = 100
    acc.sell(10, 1, 'EUR', 'BTC', fee=_fee, instant_float_fee=True)
    assert acc.depot['EUR'] == 90
    assert acc.depot['BTC'] == 10

    acc.tick(10)
    assert acc.depot['EUR'] == 80

    acc.buy(10, 1, 'EUR', 'BTC', fee=_fee, instant_float_fee=True)
    assert acc.depot['EUR'] == 90
    assert acc.depot['BTC'] == 0

    acc.tick(20)
    assert acc.depot['EUR'] == 80


# noinspection PyUnusedLocal,PyTypeChecker
def test_ignored_transaction_confirmation():
    # noinspection PyUnusedLocal
    def _fee(amount, price, base, quote, processing_duration):
        return amount, base, 10

    acc = account.FXAccount('EUR', marked_coverage='min_backward')
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100

    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore')
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=False)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', processing_duration=10)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', instant_withdrawal=True)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=10,
                            instant_float_fee=True)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=10,
                            instant_float_fee=True, float_fee_currency='BTC')
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=_fee)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=_fee,
                            instant_withdrawal=True, instant_float_fee=True, float_fee_currency='BTC')
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100

    acc = account.FXAccount('EUR', marked_coverage='max_forward')
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100

    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore')
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=False)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', processing_duration=10)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', instant_withdrawal=True)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=10,
                            instant_float_fee=True)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=10,
                            instant_float_fee=True, float_fee_currency='BTC')
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=_fee)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=_fee,
                            instant_withdrawal=True, instant_float_fee=True, float_fee_currency='BTC')
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100

    acc = account.FXAccount('EUR', marked_coverage=None)
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100

    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore')
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=False)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', processing_duration=10)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', instant_withdrawal=True)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=10,
                            instant_float_fee=True)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=10,
                            instant_float_fee=True, float_fee_currency='BTC')
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=_fee)
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore', fee=_fee,
                            instant_withdrawal=True, instant_float_fee=True, float_fee_currency='BTC')
    assert confirmation == -1
    assert len(acc.exec_heap) == 0
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100


def test_cum_sum_heap():
    acc = account.FXAccount('EUR')
    acc.tick(10)
    # (time, action_func, amount, currency, **kwargs)
    new_heap = [(5, 'withdraw', 10, 'EUR', 'except'),
                (10, 'withdraw', 10, 'BTC', 'except'),
                (10, 'deposit', 10, 'EUR', 'except'),
                (15, 'withdraw', 15, 'EUR', 'except'),
                (15, 'deposit', 15, 'BTC', 'except'),
                (15, 'deposit', 15, 'EUR', 'except')]
    heapq.heapify(new_heap)
    acc.exec_heap = new_heap

    assert acc._cum_sum_heap('EUR', 'withdraw', 16) == 15
    assert acc._cum_sum_heap('EUR', 'withdraw', 12) == 0
    assert acc._cum_sum_heap('EUR', 'deposit', 16) == 25
    assert acc._cum_sum_heap('EUR', 'deposit', 12) == 10


# noinspection PyUnusedLocal,PyTypeChecker
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_coverage_partial_exception_sell_buy():
    cov_exp = 'partial'
    base = 'EUR'
    quote = 'BTC'

    def _fee(_amount, _price, _base, _quote, _dur):
        return 1000, _base, 10

    def _fee_buy(_amount, _price, _base, _quote, _dur):
        return 1000, _quote, 10

    acc = account.FXAccount('EUR', marked_coverage='min_backward')
    acc._c_depot[base.encode()] = 100
    acc._c_depot[quote.encode()] = 100
    try:
        acc.sell(1000, 1, base, quote, coverage=cov_exp, fee=200)
        assert False
    except CoverageError:
        pass
    try:
        acc.sell(1000, 1, base, quote, coverage=cov_exp, fee=201, instant_float_fee=True,
                 instant_withdrawal=True, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(1000, 1, base, quote, coverage=cov_exp, fee=200, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(1000, 1, base, quote, coverage=cov_exp, fee=200, instant_float_fee=True,
                instant_withdrawal=True, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass

    try:
        acc.sell(1000, 1, base, quote, coverage=cov_exp, fee=_fee)
        assert False
    except CoverageError:
        pass
    try:
        acc.sell(1000, 1, base, quote, coverage=cov_exp, fee=_fee, instant_float_fee=True,
                 instant_withdrawal=True, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(1000, 1, base, quote, coverage=cov_exp, fee=_fee_buy)
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(1000, 1, base, quote, coverage=cov_exp, fee=_fee_buy, instant_float_fee=True,
                instant_withdrawal=True, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass

    acc = account.FXAccount('EUR', marked_coverage='max_forward')
    acc._c_depot[base.encode()] = 100
    acc._c_depot[quote.encode()] = 100
    try:
        acc.sell(1000, 1, base, quote, coverage=cov_exp, fee=200)
        assert False
    except CoverageError:
        pass
    try:
        acc.sell(1000, 1, base, quote, coverage=cov_exp, fee=200.1, instant_float_fee=True,
                 instant_withdrawal=True, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(1000, 1, base, quote, coverage=cov_exp, fee=200, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(1000, 1, base, quote, coverage=cov_exp, fee=200, instant_float_fee=True,
                instant_withdrawal=True, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass

    try:
        acc.sell(1000, 1, base, quote, coverage=cov_exp, fee=_fee)
        assert False
    except CoverageError:
        pass
    try:
        acc.sell(1000, 1, base, quote, coverage=cov_exp, fee=_fee, instant_float_fee=True,
                 instant_withdrawal=True, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(1000, 1, base, quote, coverage=cov_exp, fee=_fee_buy)
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(1000, 1, base, quote, coverage=cov_exp, fee=_fee_buy, instant_float_fee=True,
                instant_withdrawal=True, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass

    acc = account.FXAccount('EUR', marked_coverage=None)
    acc._c_depot[base.encode()] = 100
    acc._c_depot[quote.encode()] = 100
    try:
        acc.sell(1000, 1, base, quote, coverage=cov_exp, fee=200)
        assert False
    except CoverageError:
        pass
    try:
        acc.sell(1000, 1, base, quote, coverage=cov_exp, fee=200, instant_float_fee=True,
                 instant_withdrawal=True, float_fee_currency=base)
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(1000, 1, base, quote, coverage=cov_exp, fee=200, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(1000, 1, base, quote, coverage=cov_exp, fee=150, instant_float_fee=True,
                instant_withdrawal=True, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass

    try:
        acc.sell(1000, 1, base, quote, coverage=cov_exp, fee=_fee)
        assert False
    except CoverageError:
        pass
    try:
        acc.sell(1000, 1, base, quote, coverage=cov_exp, fee=_fee, instant_float_fee=True,
                 instant_withdrawal=True, float_fee_currency=base)
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(1000, 1, base, quote, coverage=cov_exp, fee=_fee_buy)
        assert False
    except CoverageError:
        pass
    try:
        acc.buy(1000, 1, base, quote, coverage=cov_exp, fee=_fee_buy, instant_float_fee=True,
                instant_withdrawal=True, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass


# noinspection PyUnusedLocal,PyTypeChecker
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_coverage_partial_exception_withdraw_deposit():
    cov_exp = 'partial'
    base = 'EUR'
    quote = 'BTC'

    def _fee(_amount, _price, _base, _quote, _dur):
        return 100000, _base, 10

    acc = account.FXAccount('EUR', marked_coverage='min_backward')
    acc._c_depot[base.encode()] = 100
    acc._c_depot[quote.encode()] = 100
    try:
        acc.deposit(1000, base, fee=2000)
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1000, base, fee=200,
                    instant_float_fee=True, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, base, coverage=cov_exp, fee=200)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, base, coverage=cov_exp, fee=200, instant_float_fee=True,
                     float_fee_currency=quote)
        assert False
    except CoverageError:
        pass

    try:
        acc.deposit(1000, base, fee=_fee)
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1000, base, fee=_fee, instant_float_fee=True,
                    float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, base, coverage=cov_exp, fee=_fee)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, base, coverage=cov_exp, fee=_fee,
                     instant_float_fee=True, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass

    acc = account.FXAccount('EUR', marked_coverage='max_forward')
    acc._c_depot[base.encode()] = 100
    acc._c_depot[quote.encode()] = 100
    try:
        acc.deposit(1000, base, fee=2000)
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1000, base, fee=200, instant_float_fee=True,
                    float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, base, coverage=cov_exp, fee=200)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, base, coverage=cov_exp, fee=200, instant_float_fee=True,
                     float_fee_currency=quote)
        assert False
    except CoverageError:
        pass

    try:
        acc.deposit(1000, base, fee=_fee)
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1000, base, fee=_fee, instant_float_fee=True,
                    float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, base, coverage=cov_exp, fee=_fee)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, base, coverage=cov_exp, fee=_fee,
                     instant_float_fee=True, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass

    acc = account.FXAccount('EUR', marked_coverage=None)
    acc._c_depot[base.encode()] = 100
    acc._c_depot[quote.encode()] = 100
    try:
        acc.deposit(1000, base, fee=2000)
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1000, base, fee=200, instant_float_fee=True,
                    float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, base, coverage=cov_exp, fee=2000)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, base, coverage=cov_exp, fee=150, instant_float_fee=True,
                     float_fee_currency=quote)
        assert False
    except CoverageError:
        pass

    try:
        acc.deposit(1000, base, fee=_fee)
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1000, base, fee=_fee, instant_float_fee=True,
                    float_fee_currency=quote)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, base, coverage=cov_exp, fee=_fee)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, base, coverage=cov_exp, fee=_fee,
                     instant_float_fee=True, float_fee_currency=quote)
        assert False
    except CoverageError:
        pass


# noinspection PyUnusedLocal
def test_withdraw_check_marked_min_backward():
    # def withdraw(self, amount, currency, processing_duration=None, fee=False,
    #              coverage='except', instant_float_fee=False, float_fee_currency=None)

    # 0) check_marked_coverage
    #
    # 1) instant
    #   a) coverage
    #   b) withdrawal fee (x float_fee_currency)
    # 2) delayed
    #   a) delayed everything
    #   b) instant float fee x fee_currency
    #   c) coverage
    #
    # 3) exceptions

    acc = account.FXAccount('EUR')
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100
    check_marked_coverage = acc.check_marked_coverage

    # noinspection PyUnusedLocal
    def _fee(amount, price, _base, _quote, exc_dur):
        return amount, _quote, 0

    # 1) instant
    acc.withdraw(1, 'EUR')
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 100

    acc.withdraw(1, 'EUR', fee=1, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 98
    assert acc.depot['BTC'] == 99

    acc.withdraw(1, 'EUR', instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 97
    assert acc.depot['BTC'] == 99

    acc.withdraw(1, 'EUR', fee=_fee, instant_float_fee=True, float_fee_currency='USD')
    assert acc.depot['EUR'] == 95
    assert acc.depot['BTC'] == 99

    try:
        acc.withdraw(1000, 'EUR')
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', fee=10000, float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', fee=10000, float_fee_currency='EUR',
                     coverage='partial')
        assert False
    except CoverageError:
        pass

    acc.withdraw(1000, 'EUR', coverage='partial')
    assert acc.depot['EUR'] == 0
    assert acc.depot['BTC'] == 99

    acc.withdraw(100, 'EUR', coverage='debit')
    assert acc.depot['EUR'] == -100
    assert acc.depot['BTC'] == 99

    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100
    acc.withdraw(1, 'EUR', coverage='debit', fee=100)
    assert acc.depot['EUR'] == -1
    assert acc.depot['BTC'] == 100

    # 2) delayed transaction
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100
    exc_t = 2

    acc.withdraw(1, 'EUR', processing_duration=exc_t)
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1)
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1, instant_float_fee=True)
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 100

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1, instant_float_fee=True,
                 float_fee_currency='BTC')
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 99

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee, instant_float_fee=False,
                 float_fee_currency='BTC')
    assert acc.depot['EUR'] == 98
    assert acc.depot['BTC'] == 99

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee, instant_float_fee=True,
                 float_fee_currency='EUR')
    assert acc.depot['EUR'] == 97
    assert acc.depot['BTC'] == 99

    # coverage
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100

    try:
        acc.withdraw(1000, 'EUR', processing_duration=exc_t)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1000)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1000, instant_float_fee=True,
                     float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, 'EUR', processing_duration=exc_t, fee=_fee)
        assert False
    except CoverageError:
        pass

    # noinspection PyUnusedLocal
    def _fee_2(amount, price, base, quote, dur):
        return 10000, 'EUR', 2

    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee_2)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee_2, instant_float_fee=True,
                     float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    # partial
    acc.exec_heap = []
    acc.withdraw(1000, 'EUR', processing_duration=exc_t, coverage='partial')
    assert acc.depot['EUR'] == 100

    acc.exec_heap = []
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=10000,
                     coverage='partial')
        assert False
    except CoverageError:
        pass
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1000,
                     coverage='partial',
                     instant_float_fee=True, float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee_2,
                     coverage='partial', instant_float_fee=True, float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee_2,
                     coverage='partial', instant_float_fee=True, float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass

    # debit
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100

    acc.withdraw(200, 'EUR', processing_duration=exc_t, coverage='debit')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=_fee_2, coverage='debit')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=_fee_2, coverage='debit',
                 instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                 instant_float_fee=False, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                 instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == -100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                 instant_float_fee=True, float_fee_currency='EUR')
    assert acc.depot['EUR'] == -100
    assert acc.depot['BTC'] == -100

    assert check_marked_coverage == acc.check_marked_coverage


# noinspection PyUnusedLocal
def test_withdraw_check_marked_max_forward():
    acc = account.FXAccount('EUR', marked_coverage='max_forward')
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100
    check_marked_coverage = acc.check_marked_coverage

    # noinspection PyUnusedLocal
    def _fee(amount, price, _base, _quote, exc_dur):
        return amount, _quote, 0

    # 1) instant
    acc.withdraw(1, 'EUR')
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 100

    acc.withdraw(1, 'EUR', fee=1, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 98
    assert acc.depot['BTC'] == 99

    acc.withdraw(1, 'EUR', instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 97
    assert acc.depot['BTC'] == 99

    acc.withdraw(1, 'EUR', fee=_fee, instant_float_fee=True, float_fee_currency='USD')
    assert acc.depot['EUR'] == 95
    assert acc.depot['BTC'] == 99

    try:
        acc.withdraw(1000, 'EUR')
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', fee=10000, float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', fee=10000, float_fee_currency='EUR',
                     coverage='partial')
        assert False
    except CoverageError:
        pass

    acc.withdraw(1000, 'EUR', coverage='partial')
    assert acc.depot['EUR'] == 0
    assert acc.depot['BTC'] == 99

    acc.withdraw(100, 'EUR', coverage='debit')
    assert acc.depot['EUR'] == -100
    assert acc.depot['BTC'] == 99

    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100
    acc.withdraw(1, 'EUR', coverage='debit', fee=100)
    assert acc.depot['EUR'] == -1
    assert acc.depot['BTC'] == 100

    # 2) delayed transaction
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100
    exc_t = 2

    acc.withdraw(1, 'EUR', processing_duration=exc_t)
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1)
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1, instant_float_fee=True)
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 100

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1, instant_float_fee=True,
                 float_fee_currency='BTC')
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 99

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee, instant_float_fee=False,
                 float_fee_currency='BTC')
    assert acc.depot['EUR'] == 98
    assert acc.depot['BTC'] == 99

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee, instant_float_fee=True,
                 float_fee_currency='EUR')
    assert acc.depot['EUR'] == 97
    assert acc.depot['BTC'] == 99

    # coverage
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100

    try:
        acc.withdraw(1000, 'EUR', processing_duration=exc_t)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1000)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1000, instant_float_fee=True,
                     float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, 'EUR', processing_duration=exc_t, fee=_fee)
        assert False
    except CoverageError:
        pass

    # noinspection PyUnusedLocal
    def _fee_2(amount, price, base, quote, dur):
        return 10000, 'EUR', 2

    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee_2)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee_2, instant_float_fee=True,
                     float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    # partial
    acc.exec_heap = []
    acc.withdraw(1000, 'EUR', processing_duration=exc_t, coverage='partial')
    assert acc.depot['EUR'] == 100

    acc.exec_heap = []
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=10000,
                     coverage='partial')
        assert False
    except CoverageError:
        pass
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1000,
                     coverage='partial',
                     instant_float_fee=True, float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee_2,
                     coverage='partial', instant_float_fee=True, float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee_2,
                     coverage='partial', instant_float_fee=True, float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass

    # debit
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100

    acc.withdraw(200, 'EUR', processing_duration=exc_t, coverage='debit')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=_fee_2, coverage='debit')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=_fee_2, coverage='debit',
                 instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                 instant_float_fee=False, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                 instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == -100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                 instant_float_fee=True, float_fee_currency='EUR')
    assert acc.depot['EUR'] == -100
    assert acc.depot['BTC'] == -100

    assert check_marked_coverage == acc.check_marked_coverage


# noinspection PyUnusedLocal
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_withdraw_check_marked_none():
    acc = account.FXAccount('EUR', marked_coverage=None)
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100
    check_marked_coverage = acc.check_marked_coverage

    # noinspection PyUnusedLocal
    def _fee(amount, price, _base, _quote, exc_dur):
        return amount, _quote, 0

    # 1) instant
    acc.withdraw(1, 'EUR')
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 100

    acc.withdraw(1, 'EUR', fee=1, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 98
    assert acc.depot['BTC'] == 99

    acc.withdraw(1, 'EUR', instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 97
    assert acc.depot['BTC'] == 99

    acc.withdraw(1, 'EUR', fee=_fee, instant_float_fee=True, float_fee_currency='USD')
    assert acc.depot['EUR'] == 95
    assert acc.depot['BTC'] == 99

    try:
        acc.withdraw(1000, 'EUR')
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', fee=10000, float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', fee=10000, float_fee_currency='EUR',
                     coverage='partial')
        assert False
    except CoverageError:
        pass

    acc.withdraw(1000, 'EUR', coverage='partial')
    assert acc.depot['EUR'] == 0
    assert acc.depot['BTC'] == 99

    acc.withdraw(100, 'EUR', coverage='debit')
    assert acc.depot['EUR'] == -100
    assert acc.depot['BTC'] == 99

    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100
    acc.withdraw(1, 'EUR', coverage='debit', fee=100)
    assert acc.depot['EUR'] == -1
    assert acc.depot['BTC'] == 100

    # 2) delayed transaction
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100
    exc_t = 2

    acc.withdraw(1, 'EUR', processing_duration=exc_t)
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1)
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1, instant_float_fee=True)
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 100

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1, instant_float_fee=True,
                 float_fee_currency='BTC')
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 99

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee, instant_float_fee=False,
                 float_fee_currency='BTC')
    assert acc.depot['EUR'] == 98
    assert acc.depot['BTC'] == 99

    acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee, instant_float_fee=True,
                 float_fee_currency='EUR')
    assert acc.depot['EUR'] == 97
    assert acc.depot['BTC'] == 99

    # coverage
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100

    try:
        acc.withdraw(1000, 'EUR', processing_duration=exc_t)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1000)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1000, instant_float_fee=True,
                     float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1000, 'EUR', processing_duration=exc_t, fee=_fee)
        assert False
    except CoverageError:
        pass

    # noinspection PyUnusedLocal
    def _fee_2(amount, price, base, quote, dur):
        return 10000, 'EUR', 2

    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee_2)
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee_2, instant_float_fee=True,
                     float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    # partial
    acc.exec_heap = []
    acc.withdraw(1000, 'EUR', processing_duration=exc_t, coverage='partial')
    assert acc.depot['EUR'] == 100

    acc.exec_heap = []
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=10000,
                     coverage='partial')
        assert False
    except CoverageError:
        pass
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=1000,
                     coverage='partial',
                     instant_float_fee=True, float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee_2,
                     coverage='partial', instant_float_fee=True, float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.withdraw(1, 'EUR', processing_duration=exc_t, fee=_fee_2,
                     coverage='partial', instant_float_fee=True, float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass

    # debit
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100

    acc.withdraw(200, 'EUR', processing_duration=exc_t, coverage='debit')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=_fee_2, coverage='debit')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=_fee_2, coverage='debit',
                 instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                 instant_float_fee=False, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                 instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == -100
    acc.withdraw(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                 instant_float_fee=True, float_fee_currency='EUR')
    assert acc.depot['EUR'] == -100
    assert acc.depot['BTC'] == -100

    assert check_marked_coverage == acc.check_marked_coverage


# noinspection PyUnusedLocal
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_withdraw_debit_heap_depot():
    acc = account.FXAccount('EUR', marked_coverage='min_backward')
    check_marked_coverage = acc.check_marked_coverage
    acc.depot = {'EUR': -100, 'BTC': -100}
    acc.exec_heap = [(5, 'withdraw', 100, 'EUR', 'except')]
    acc.withdraw(100, 'EUR', coverage='debit')
    acc.withdraw(100, 'EUR', coverage='debit', processing_duration=6)
    acc.withdraw(100, 'EUR', coverage='debit', fee=100, float_fee_currency='EUR')
    try:
        acc.withdraw(100, 'EUR')
        assert False
    except CoverageError:
        pass
    assert check_marked_coverage == acc.check_marked_coverage

    acc = account.FXAccount('EUR', marked_coverage='max_forward')
    check_marked_coverage = acc.check_marked_coverage
    acc.depot = {'EUR': -100, 'BTC': -100}
    acc.exec_heap = [(5, 'withdraw', 100, 'EUR', 'except')]
    acc.withdraw(100, 'EUR', coverage='debit')
    acc.withdraw(100, 'EUR', coverage='debit', processing_duration=6)
    acc.withdraw(100, 'EUR', coverage='debit', fee=100, float_fee_currency='EUR')
    try:
        acc.withdraw(100, 'EUR')
        assert False
    except CoverageError:
        pass
    assert check_marked_coverage == acc.check_marked_coverage

    acc = account.FXAccount('EUR', marked_coverage=None)
    check_marked_coverage = acc.check_marked_coverage
    acc.depot = {'EUR': -100, 'BTC': -100}
    acc.exec_heap = [(5, 'withdraw', 100, 'EUR', 'except')]
    acc.withdraw(100, 'EUR', coverage='debit')
    acc.withdraw(100, 'EUR', coverage='debit', processing_duration=6)
    acc.withdraw(100, 'EUR', coverage='debit', fee=100, float_fee_currency='EUR')
    try:
        acc.withdraw(100, 'EUR')
        assert False
    except CoverageError:
        pass
    assert check_marked_coverage == acc.check_marked_coverage


# noinspection PyUnusedLocal
def test_withdraw_input_exceptions():
    acc = account.FXAccount('EUR')
    acc.depot = {'EUR': 100, 'BTC': 100}

    try:
        acc.withdraw(-100, 'EUR')
        assert False
    except ValueError:
        pass
    try:
        acc.withdraw(100, 'something')
        assert False
    except PositionNAError:
        pass
    try:
        acc.withdraw(100, 'EUR', processing_duration='something')
        assert False
    except TypeError:
        pass
    try:
        acc.withdraw(100, 'EUR', fee='something')
        assert False
    except NotImplementedError:
        pass
    try:
        acc.withdraw(100, 'EUR', fee=100, float_fee_currency='something')
        assert False
    except PositionNAError:
        pass
    try:
        acc.withdraw(100, 'EUR', fee=100, coverage='something')
        assert False
    except NotImplementedError:
        pass
    try:
        acc.withdraw(100, 'EUR', instant_float_fee='something', fee=100)
        assert False
    except TypeError:
        pass
    acc.withdraw(100, 'EUR', instant_float_fee='something')


# noinspection PyUnusedLocal
def test_deposit_check_marked_min_backward():
    # deposit(self, amount, currency, processing_duration=None, fee=False,
    #                 coverage='except', instant_float_fee=False, float_fee_currency=None)

    # 0) check_marked_coverage
    #
    # 1) instant
    #   a) coverage
    #   b) deposit_fee (x float_fee_currency)
    # 2) delayed
    #   a) delayed everything
    #   b) instant float fee x fee_currency
    #   c) coverage
    #
    # 3) exceptions

    acc = account.FXAccount('EUR')
    acc.depot = {'EUR': 100, 'BTC': 100}
    check_marked_coverage = acc.check_marked_coverage

    # noinspection PyUnusedLocal
    def _fee(amount, price, _base, _quote, exc_dur):
        return amount, _quote, 0

    # 1) instant
    acc.deposit(1, 'EUR')
    assert acc.depot['EUR'] == 101
    assert acc.depot['BTC'] == 100

    acc.deposit(1, 'EUR', fee=1, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 102
    assert acc.depot['BTC'] == 99

    acc.deposit(1, 'EUR', instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 103
    assert acc.depot['BTC'] == 99

    acc.deposit(1, 'EUR', fee=_fee, instant_float_fee=True, float_fee_currency='USD')
    assert acc.depot['EUR'] == 103
    assert acc.depot['BTC'] == 99

    try:
        acc.deposit(1, 'EUR', fee=10000, float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1, 'EUR', fee=10000, float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass

    acc.deposit(1000, 'EUR')
    assert acc.depot['EUR'] == 1103
    assert acc.depot['BTC'] == 99

    acc.deposit(100, 'EUR', coverage='debit')
    assert acc.depot['EUR'] == 1203
    assert acc.depot['BTC'] == 99

    acc.exec_heap = []
    acc.depot = {'EUR': 100, 'BTC': 100}
    acc.deposit(1, 'EUR', coverage='debit', fee=200)
    assert acc.depot['EUR'] == -99
    assert acc.depot['BTC'] == 100

    # 2) delayed transaction
    acc.depot = {'EUR': 100, 'BTC': 100}
    exc_t = 2

    acc.deposit(1, 'EUR', processing_duration=exc_t)
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1)
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1, instant_float_fee=True)
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 100

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1, instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 99

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee, instant_float_fee=False,
                float_fee_currency='BTC')
    assert acc.depot['EUR'] == 98
    assert acc.depot['BTC'] == 99

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee, instant_float_fee=True,
                float_fee_currency='EUR')
    assert acc.depot['EUR'] == 97
    assert acc.depot['BTC'] == 99

    # coverage
    acc.depot = {'EUR': 100, 'BTC': 100}

    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1000)
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1000, instant_float_fee=True,
                    float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1000, 'EUR', processing_duration=exc_t, fee=_fee)
        assert False
    except CoverageError:
        pass

    # noinspection PyUnusedLocal
    def _fee_2(amount, price, base, quote, dur):
        return 10000, 'EUR', 2

    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee_2)
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee_2, instant_float_fee=True,
                    float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    # partial
    acc.exec_heap = []
    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=101)
    assert acc.depot['EUR'] == 100

    acc.exec_heap = []
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=10000)
        assert False
    except CoverageError:
        pass
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1000, instant_float_fee=True,
                    float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee_2, instant_float_fee=True,
                    float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee_2, instant_float_fee=True,
                    float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass

    # debit
    acc.exec_heap = []
    acc.depot = {'EUR': 100, 'BTC': 100}

    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=_fee_2, coverage='debit')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=_fee_2, coverage='debit',
                instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                instant_float_fee=False, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == -100
    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                instant_float_fee=True, float_fee_currency='EUR')
    assert acc.depot['EUR'] == -100
    assert acc.depot['BTC'] == -100

    assert check_marked_coverage == acc.check_marked_coverage


# noinspection PyUnusedLocal
def test_deposit_check_marked_max_forward():
    acc = account.FXAccount('EUR', marked_coverage='max_forward')
    acc.depot = {'EUR': 100, 'BTC': 100}
    check_marked_coverage = acc.check_marked_coverage

    # noinspection PyUnusedLocal
    def _fee(amount, price, _base, _quote, exc_dur):
        return amount, _quote, 0

    # 1) instant
    acc.deposit(1, 'EUR')
    assert acc.depot['EUR'] == 101
    assert acc.depot['BTC'] == 100

    acc.deposit(1, 'EUR', fee=1, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 102
    assert acc.depot['BTC'] == 99

    acc.deposit(1, 'EUR', instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 103
    assert acc.depot['BTC'] == 99

    acc.deposit(1, 'EUR', fee=_fee, instant_float_fee=True, float_fee_currency='USD')
    assert acc.depot['EUR'] == 103
    assert acc.depot['BTC'] == 99

    try:
        acc.deposit(1, 'EUR', fee=10000, float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1, 'EUR', fee=10000, float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass

    acc.deposit(1000, 'EUR')
    assert acc.depot['EUR'] == 1103
    assert acc.depot['BTC'] == 99

    acc.deposit(100, 'EUR', coverage='debit')
    assert acc.depot['EUR'] == 1203
    assert acc.depot['BTC'] == 99

    acc.exec_heap = []
    acc.depot = {'EUR': 100, 'BTC': 100}
    acc.deposit(1, 'EUR', coverage='debit', fee=200)
    assert acc.depot['EUR'] == -99
    assert acc.depot['BTC'] == 100

    # 2) delayed transaction
    acc.depot = {'EUR': 100, 'BTC': 100}
    exc_t = 2

    acc.deposit(1, 'EUR', processing_duration=exc_t)
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1)
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1, instant_float_fee=True)
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 100

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1, instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 99

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee, instant_float_fee=False,
                float_fee_currency='BTC')
    assert acc.depot['EUR'] == 98
    assert acc.depot['BTC'] == 99

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee, instant_float_fee=True,
                float_fee_currency='EUR')
    assert acc.depot['EUR'] == 97
    assert acc.depot['BTC'] == 99

    # coverage
    acc.depot = {'EUR': 100, 'BTC': 100}

    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1000)
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1000, instant_float_fee=True,
                    float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1000, 'EUR', processing_duration=exc_t, fee=_fee)
        assert False
    except CoverageError:
        pass

    # noinspection PyUnusedLocal
    def _fee_2(amount, price, base, quote, dur):
        return 10000, 'EUR', 2

    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee_2)
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee_2, instant_float_fee=True,
                    float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    # partial
    acc.exec_heap = []
    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=101)
    assert acc.depot['EUR'] == 100

    acc.exec_heap = []
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=10000)
        assert False
    except CoverageError:
        pass
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1000, instant_float_fee=True,
                    float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee_2, instant_float_fee=True,
                    float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee_2, instant_float_fee=True,
                    float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass

    # debit
    acc.exec_heap = []
    acc.depot = {'EUR': 100, 'BTC': 100}

    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=_fee_2, coverage='debit')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=_fee_2, coverage='debit',
                instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                instant_float_fee=False, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == -100
    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                instant_float_fee=True, float_fee_currency='EUR')
    assert acc.depot['EUR'] == -100
    assert acc.depot['BTC'] == -100

    assert check_marked_coverage == acc.check_marked_coverage


# noinspection PyUnusedLocal
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_deposit_check_marked_none():
    acc = account.FXAccount('EUR', marked_coverage=None)
    acc.depot = {'EUR': 100, 'BTC': 100}
    check_marked_coverage = acc.check_marked_coverage

    # noinspection PyUnusedLocal
    def _fee(amount, price, _base, _quote, exc_dur):
        return amount, _quote, 0

    # 1) instant
    acc.deposit(1, 'EUR')
    assert acc.depot['EUR'] == 101
    assert acc.depot['BTC'] == 100

    acc.deposit(1, 'EUR', fee=1, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 102
    assert acc.depot['BTC'] == 99

    acc.deposit(1, 'EUR', instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 103
    assert acc.depot['BTC'] == 99

    acc.deposit(1, 'EUR', fee=_fee, instant_float_fee=True, float_fee_currency='USD')
    assert acc.depot['EUR'] == 103
    assert acc.depot['BTC'] == 99

    try:
        acc.deposit(1, 'EUR', fee=10000, float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1, 'EUR', fee=10000, float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass

    acc.deposit(1000, 'EUR')
    assert acc.depot['EUR'] == 1103
    assert acc.depot['BTC'] == 99

    acc.deposit(100, 'EUR', coverage='debit')
    assert acc.depot['EUR'] == 1203
    assert acc.depot['BTC'] == 99

    acc.exec_heap = []
    acc.depot = {'EUR': 100, 'BTC': 100}
    acc.deposit(1, 'EUR', coverage='debit', fee=200)
    assert acc.depot['EUR'] == -99
    assert acc.depot['BTC'] == 100

    # 2) delayed transaction
    acc.depot = {'EUR': 100, 'BTC': 100}
    exc_t = 2

    acc.deposit(1, 'EUR', processing_duration=exc_t)
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1)
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1, instant_float_fee=True)
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 100

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1, instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 99
    assert acc.depot['BTC'] == 99

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee, instant_float_fee=False,
                float_fee_currency='BTC')
    assert acc.depot['EUR'] == 98
    assert acc.depot['BTC'] == 99

    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee, instant_float_fee=True,
                float_fee_currency='EUR')
    assert acc.depot['EUR'] == 97
    assert acc.depot['BTC'] == 99

    # coverage
    acc.depot = {'EUR': 100, 'BTC': 100}

    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1000)
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1000, instant_float_fee=True,
                    float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1000, 'EUR', processing_duration=exc_t, fee=_fee)
        assert False
    except CoverageError:
        pass

    # noinspection PyUnusedLocal
    def _fee_2(amount, price, base, quote, dur):
        return 10000, 'EUR', 2

    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee_2)
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee_2, instant_float_fee=True,
                    float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    # partial
    acc.exec_heap = []
    acc.deposit(1, 'EUR', processing_duration=exc_t, fee=101)
    assert acc.depot['EUR'] == 100

    acc.exec_heap = []
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=10000)
        assert False
    except CoverageError:
        pass
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=1000, instant_float_fee=True,
                    float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    acc.exec_heap = []
    acc._c_depot[b'EUR'] = 100
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee_2, instant_float_fee=True,
                    float_fee_currency='BTC')
        assert False
    except CoverageError:
        pass
    try:
        acc.deposit(1, 'EUR', processing_duration=exc_t, fee=_fee_2, instant_float_fee=True,
                    float_fee_currency='EUR')
        assert False
    except CoverageError:
        pass

    # debit
    acc.exec_heap = []
    acc.depot = {'EUR': 100, 'BTC': 100}

    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=_fee_2, coverage='debit')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=_fee_2, coverage='debit',
                instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                instant_float_fee=False, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == 100
    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                instant_float_fee=True, float_fee_currency='BTC')
    assert acc.depot['EUR'] == 100
    assert acc.depot['BTC'] == -100
    acc.deposit(200, 'EUR', processing_duration=exc_t, fee=200, coverage='debit',
                instant_float_fee=True, float_fee_currency='EUR')
    assert acc.depot['EUR'] == -100
    assert acc.depot['BTC'] == -100

    assert check_marked_coverage == acc.check_marked_coverage


# noinspection PyUnusedLocal
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_deposit_debit_heap_depot():
    acc = account.FXAccount('EUR', marked_coverage='min_backward')
    check_marked_coverage = acc.check_marked_coverage
    acc.depot = {'EUR': -100, 'BTC': -100}
    acc.exec_heap = [(5, 'withdraw', 100, 'EUR', 'except')]
    acc.deposit(100, 'EUR', coverage='debit')
    acc.deposit(100, 'EUR', coverage='debit', processing_duration=6)
    acc.deposit(100, 'EUR', coverage='debit', fee=100, float_fee_currency='EUR')
    try:
        acc.deposit(100, 'EUR', fee=1000000)
        assert False
    except CoverageError:
        pass
    assert check_marked_coverage == acc.check_marked_coverage

    acc = account.FXAccount('EUR', marked_coverage='max_forward')
    check_marked_coverage = acc.check_marked_coverage
    acc.depot = {'EUR': -100, 'BTC': -100}
    acc.exec_heap = [(5, 'withdraw', 100, 'EUR', 'except')]
    acc.deposit(100, 'EUR', coverage='debit')
    acc.deposit(100, 'EUR', coverage='debit', processing_duration=6)
    acc.deposit(100, 'EUR', coverage='debit', fee=100, float_fee_currency='EUR')
    try:
        acc.deposit(100, 'EUR', fee=1000000)
        assert False
    except CoverageError:
        pass
    assert check_marked_coverage == acc.check_marked_coverage

    acc = account.FXAccount('EUR', marked_coverage=None)
    check_marked_coverage = acc.check_marked_coverage
    acc.depot = {'EUR': -100, 'BTC': -100}
    acc.exec_heap = [(5, 'withdraw', 100, 'EUR', 'except')]
    acc.deposit(100, 'EUR', coverage='debit')
    acc.deposit(100, 'EUR', coverage='debit', processing_duration=6)
    acc.deposit(100, 'EUR', coverage='debit', fee=100, float_fee_currency='EUR')
    try:
        acc.deposit(100, 'EUR', fee=1000000)
        assert False
    except CoverageError:
        pass
    assert check_marked_coverage == acc.check_marked_coverage


# noinspection PyUnusedLocal
def test_deposit_input_exceptions():
    acc = account.FXAccount('EUR')
    acc.depot = {'EUR': 100, 'BTC': 100}

    try:
        acc.deposit(-100, 'EUR')
        assert False
    except ValueError:
        pass
    try:
        acc.deposit(100, 'EUR', processing_duration='something')
        assert False
    except TypeError:
        pass
    try:
        acc.deposit(100, 'EUR', fee='something')
        assert False
    except NotImplementedError:
        pass
    try:
        acc.deposit(100, 'EUR', fee=100, float_fee_currency='something')
        assert False
    except PositionNAError:
        pass
    try:
        acc.deposit(100, 'EUR', fee=100, coverage='something')
        assert False
    except NotImplementedError:
        pass
    try:
        acc.deposit(100, 'EUR', instant_float_fee='something', fee=100)
        assert False
    except TypeError:
        pass

    try:
        acc.deposit(1, 'EUR', fee=1, float_fee_currency='something')
        assert False
    except PositionNAError:
        pass

    acc.deposit(100, 'EUR', instant_float_fee='something')


# noinspection PyTypeChecker
def test_transfer():
    # def transfer(self, payee_account, amount, currency,
    #              payee_fee=False, payer_fee=False,
    #              payee_processing_duration=None, payer_processing_duration=None)

    acc_payer = account.FXAccount('EUR')
    acc_payee = account.FXAccount('EUR')

    acc_payer._c_depot[b'EUR'] = 100

    acc_payer.transfer(acc_payee, 50, 'EUR')
    assert acc_payer.depot['EUR'] == 50
    assert acc_payee.depot['EUR'] == 50

    acc_payer.transfer(acc_payee, 10, 'EUR', payee_fee=10, payer_fee=10)
    assert acc_payer.depot['EUR'] == 30
    assert acc_payee.depot['EUR'] == 50

    acc_payer.transfer(acc_payee, 10, 'EUR', payee_fee=5, payer_fee=5, payer_processing_duration=1,
                       payee_processing_duration=2)
    assert acc_payer.depot['EUR'] == 30
    assert acc_payee.depot['EUR'] == 50
    acc_payer.tick()
    acc_payee.tick()
    assert acc_payer.depot['EUR'] == 15
    assert acc_payee.depot['EUR'] == 50
    acc_payer.tick()
    acc_payee.tick()
    assert acc_payer.depot['EUR'] == 15
    assert acc_payee.depot['EUR'] == 55

    # noinspection PyUnusedLocal
    def _fee(amount, price, base, quote, dur):
        return 1, base, 1

    acc_payer.transfer(acc_payee, 1, 'EUR', payer_fee=_fee, payee_fee=5, payer_processing_duration=2,
                       payee_processing_duration=2)
    assert acc_payer.depot['EUR'] == 15
    assert acc_payee.depot['EUR'] == 55
    acc_payer.tick()
    acc_payee.tick()
    assert acc_payer.depot['EUR'] == 14
    assert acc_payee.depot['EUR'] == 55
    acc_payer.tick()
    acc_payee.tick()
    assert acc_payer.depot['EUR'] == 13
    assert acc_payee.depot['EUR'] == 51

    acc_payer.transfer(acc_payee, 1, 'EUR', payee_fee=_fee, payer_fee=5, payer_processing_duration=2,
                       payee_processing_duration=2)
    assert acc_payer.depot['EUR'] == 13
    assert acc_payee.depot['EUR'] == 51
    acc_payer.tick()
    acc_payee.tick()
    assert acc_payer.depot['EUR'] == 13
    assert acc_payee.depot['EUR'] == 50
    acc_payer.tick()
    acc_payee.tick()
    assert acc_payer.depot['EUR'] == 7
    assert acc_payee.depot['EUR'] == 51

    acc_payer._c_fee[b'withdraw'] = _fee
    acc_payee._c_fee[b'deposit'] = _fee

    acc_payer.transfer(acc_payee, 1, 'EUR', payee_fee=None, payer_fee=None, payer_processing_duration=2,
                       payee_processing_duration=2)
    assert acc_payer.depot['EUR'] == 7
    assert acc_payee.depot['EUR'] == 51
    acc_payer.tick()
    acc_payee.tick()
    assert acc_payer.depot['EUR'] == 6
    assert acc_payee.depot['EUR'] == 50
    acc_payer.tick()
    acc_payee.tick()
    assert acc_payer.depot['EUR'] == 5
    assert acc_payee.depot['EUR'] == 51

    # coverage
    try:
        acc_payer.transfer(acc_payee, 100, 'EUR', payee_fee=None, payer_fee=None, payer_processing_duration=2,
                           payee_processing_duration=2)
        assert False
    except CoverageError:
        pass
    try:
        acc_payer.transfer(acc_payee, 1, 'EUR', payee_fee=None, payer_fee=100, payer_processing_duration=2,
                           payee_processing_duration=2)
        assert False
    except CoverageError:
        pass
    acc_payer.exec_heap = [(acc_payer.clock + 1, 'withdraw', 100, 'EUR', 'except')]
    try:
        acc_payer.transfer(acc_payee, 100, 'EUR', payee_fee=False, payer_fee=False)
        assert False
    except CoverageError:
        pass
    acc_payer.exec_heap = []
    d = 0
    try:
        d = acc_payer.depot['EUR']
        acc_payer.transfer(acc_payee, 1, 'EUR', payee_fee=10000, payer_fee=None, payer_processing_duration=2,
                           payee_processing_duration=2)
        assert False
    except CoverageError:
        assert acc_payer.depot['EUR'] == d

    # exceptions
    acc_payer._c_depot[b'EUR'] = 100
    acc_payee._c_depot[b'EUR'] = 100
    try:
        acc_payer.transfer(acc_payer, 1, 'EUR')
        assert False
    except AccountError:
        pass
    try:
        acc_payer.transfer(3, 1, 'EUR')
        assert False
    except AccountError:
        pass
    try:
        acc_payer.transfer(acc_payee, -1, 'EUR')
        assert False
    except ValueError:
        pass
    try:
        acc_payer.transfer(acc_payee, 1, 'something')
        assert False
    except PositionNAError:
        pass
    try:
        acc_payer.transfer(acc_payee, 1, 'EUR', payer_processing_duration='something')
        assert False
    except TypeError:
        pass
    try:
        acc_payer.transfer(acc_payee, 1, 'EUR', payer_fee='something')
        assert False
    except NotImplementedError:
        pass


# noinspection PyTypeChecker
def test_collect():
    # def transfer(self, payee_account, amount, currency,
    #              payee_fee=False, payer_fee=False,
    #              payee_processing_duration=None, payer_processing_duration=None)

    acc_one = account.FXAccount('EUR')
    acc_two = account.FXAccount('EUR')

    acc_two._c_depot[b'EUR'] = 100

    acc_one.collect(acc_two, 50, 'EUR')
    assert acc_two.depot['EUR'] == 50
    assert acc_one.depot['EUR'] == 50

    acc_one.collect(acc_two, 10, 'EUR', payee_fee=10, payer_fee=10)
    assert acc_two.depot['EUR'] == 30
    assert acc_one.depot['EUR'] == 50

    acc_one.collect(acc_two, 10, 'EUR', payee_fee=5, payer_fee=5, payer_processing_duration=1,
                    payee_processing_duration=2)
    assert acc_two.depot['EUR'] == 30
    assert acc_one.depot['EUR'] == 50
    acc_two.tick()
    acc_one.tick()
    assert acc_two.depot['EUR'] == 15
    assert acc_one.depot['EUR'] == 50
    acc_two.tick()
    acc_one.tick()
    assert acc_two.depot['EUR'] == 15
    assert acc_one.depot['EUR'] == 55

    # noinspection PyUnusedLocal
    def _fee(amount, price, base, quote, dur):
        return 1, base, 1

    acc_one.collect(acc_two, 1, 'EUR', payer_fee=_fee, payee_fee=5, payer_processing_duration=2,
                    payee_processing_duration=2)
    assert acc_two.depot['EUR'] == 15
    assert acc_one.depot['EUR'] == 55
    acc_two.tick()
    acc_one.tick()
    assert acc_two.depot['EUR'] == 14
    assert acc_one.depot['EUR'] == 55
    acc_two.tick()
    acc_one.tick()
    assert acc_two.depot['EUR'] == 13
    assert acc_one.depot['EUR'] == 51

    acc_one.collect(acc_two, 1, 'EUR', payee_fee=_fee, payer_fee=5, payer_processing_duration=2,
                    payee_processing_duration=2)
    assert acc_two.depot['EUR'] == 13
    assert acc_one.depot['EUR'] == 51
    acc_two.tick()
    acc_one.tick()
    assert acc_two.depot['EUR'] == 13
    assert acc_one.depot['EUR'] == 50
    acc_two.tick()
    acc_one.tick()
    assert acc_two.depot['EUR'] == 7
    assert acc_one.depot['EUR'] == 51

    acc_two._c_fee[b'withdraw'] = _fee
    acc_one._c_fee[b'deposit'] = _fee

    acc_one.collect(acc_two, 1, 'EUR', payee_fee=None, payer_fee=None, payer_processing_duration=2,
                    payee_processing_duration=2)
    assert acc_two.depot['EUR'] == 7
    assert acc_one.depot['EUR'] == 51
    acc_two.tick()
    acc_one.tick()
    assert acc_two.depot['EUR'] == 6
    assert acc_one.depot['EUR'] == 50
    acc_two.tick()
    acc_one.tick()
    assert acc_two.depot['EUR'] == 5
    assert acc_one.depot['EUR'] == 51

    # coverage
    try:
        acc_one.collect(acc_two, 100, 'EUR', payee_fee=None, payer_fee=None, payer_processing_duration=2,
                        payee_processing_duration=2)
        assert False
    except CoverageError:
        pass
    try:
        acc_one.collect(acc_two, 1, 'EUR', payee_fee=None, payer_fee=100, payer_processing_duration=2,
                        payee_processing_duration=2)
        assert False
    except CoverageError:
        pass
    acc_one.exec_heap = [(acc_two.clock + 1, 'withdraw', 100, 'EUR', 'except')]
    try:
        acc_one.collect(acc_two, 100, 'EUR', payee_fee=False, payer_fee=False)
        assert False
    except CoverageError:
        pass
    acc_one.exec_heap = []
    d = 0
    try:
        d = acc_two.depot['EUR']
        acc_one.collect(acc_two, 1, 'EUR', payee_fee=10000, payer_fee=None, payer_processing_duration=2,
                        payee_processing_duration=2)
        assert False
    except CoverageError:
        assert acc_two.depot['EUR'] == d

    # exceptions
    acc_two._c_depot[b'EUR'] = 100
    acc_one._c_depot[b'EUR'] = 100
    try:
        acc_one.collect(acc_one, 1, 'EUR')
        assert False
    except AccountError:
        pass
    try:
        acc_one.collect(3, 1, 'EUR')
        assert False
    except AccountError:
        pass
    try:
        acc_one.collect(acc_two, -1, 'EUR')
        assert False
    except ValueError:
        pass
    try:
        acc_one.collect(acc_two, 1, 'something')
        assert False
    except PositionNAError:
        pass
    try:
        acc_one.collect(acc_two, 1, 'EUR', payer_processing_duration='something')
        assert False
    except TypeError:
        pass
    try:
        acc_one.collect(acc_two, 1, 'EUR', payer_fee='something')
        assert False
    except NotImplementedError:
        pass


# noinspection PyTypeChecker
def test_position():
    acc = account.FXAccount('EUR')
    acc._c_depot[b'BTC'] = 100

    assert acc.position('BTC') == 100
    assert acc.position('EUR') == 0

    acc.exec_heap = [(10, 'withdraw', 10, 'BTC', 'except'),
                     (12, 'withdraw', 10, 'EUR', 'except'),
                     (12, 'deposit', 12, 'BTC', 'except')]

    assert acc.position('BTC') == 100

    try:
        _ = acc.position(2)
        assert False
    except TypeError:
        pass


# noinspection PyTypeChecker
def test_total_balance():
    acc = account.FXAccount('EUR')
    acc._c_depot[b'BTC'] = 100
    acc._c_depot[b'ETH'] = 100
    acc._c_depot[b'EUR'] = 50

    def assert_depot():
        assert acc._c_depot[b'BTC'] == 100
        assert acc._c_depot[b'ETH'] == 100
        assert acc._c_depot[b'EUR'] == 50

    assert acc.total_balance({('BTC', 'EUR'): 2, ('ETH', 'EUR'): 1}) == 350
    assert_depot()
    assert acc.total_balance({('BTC', 'EUR'): 2, ('ETH', 'EUR'): 1, ('BTC', 'EUR'): 2}) == 350
    assert_depot()
    assert acc.total_balance({('BTC', 'USD'): 2, ('ETH', 'USD'): 1, ('EUR', 'USD'): 1}, 'USD') == 350
    assert_depot()
    assert acc.total_balance({('BTC', 'EUR'): 2, ('ETH', 'EUR'): 1, ('EUR', 'USD'): 100}) == 350
    assert_depot()
    assert acc.total_balance({('EUR', 'BTC'): 0.5, ('ETH', 'EUR'): 1, ('EUR', 'USD'): 100}) == 350
    assert_depot()
    assert acc.total_balance({('BTC', 'EUR'): 2, ('EUR', 'BTC'): 0.5, ('ETH', 'EUR'): 1, ('EUR', 'USD'): 100}) == 350
    assert_depot()
    assert acc.total_balance({('BTC', 'EUR'): 2, ('ETH', 'EUR'): 1, ('EUR', 'USD'): 100, ('ETH', 'USD'): 100}) == 350
    assert_depot()
    assert acc.total_balance({('BTC', 'EUR'): 2, ('ETH', 'EUR'): 1, ('EUR', 'USD'): 100,
                              ('ETH', 'USD'): 100, ('USD', 'USD'): 2000}) == 350
    assert_depot()
    assert acc.total_balance({('BTC', 'EUR'): 2, ('ETH', 'EUR'): 1, ('EUR', 'USD'): 100, ('USD', 'ETH'): 0.01}) == 350
    assert_depot()
    assert acc.total_balance({('BTC', 'EUR'): 2, ('ETH', 'EUR'): 1, ('EUR', 'ETH'): 1}) == 350
    assert_depot()
    try:
        assert acc.total_balance({('BTC', 'EUR'): 2, ('ETH', 'EUR'): 1, ('EUR', 'ETH'): 2}) == 350
        assert False
    except ValueError:
        assert_depot()
        pass

    # assigned
    acc.exchange_rates = {('BTC', 'EUR'): 2, ('ETH', 'EUR'): 1, ('EUR', 'USD'): 100, ('ETH', 'USD'): 100}
    try:
        _ = acc.total_balance()
        assert False
    except OperatingError:
        assert_depot()
        pass
    acc.update_exchange_rate(2, 'BTC', 'EUR')
    assert acc.total_balance() == 350
    assert_depot()
    try:
        _ = acc.total_balance()
        assert False
    except OperatingError:
        assert_depot()
        pass
    acc.update_exchange_rate(2, 'BTC', 'EUR')
    try:
        _ = acc.total_balance(reference_currency='USD')
        assert False
    except KeyError:
        assert_depot()
        pass
    acc.update_exchange_rate(2, 'BTC', 'USD')
    acc.update_exchange_rate(1, 'ETH', 'USD')
    acc.update_exchange_rate(1, 'EUR', 'USD')
    assert acc.total_balance(reference_currency='USD') == 350
    assert_depot()
    assert acc.total_balance({('BTC', 'EUR'): 2, ('ETH', 'EUR'): 1, ('EUR', 'USD'): 100}) == 350
    assert_depot()

    # input exceptions
    try:
        _ = acc.total_balance({('BTC', 'EUR'): 2})
        assert False
    except KeyError:
        assert_depot()
        pass
    try:
        _ = acc.total_balance(2)
        assert False
    except TypeError:
        assert_depot()
        pass
    try:
        _ = acc.total_balance({('BTC', 'EUR'): 2}, reference_currency=2)
        assert False
    except TypeError:
        assert_depot()
        pass
    try:
        _ = acc.total_balance({('BTC', 'EUR'): 2, ('ETH', 'EUR'): 1, ('EUR', 'USD'): 100, ('ETH', 'USD'): 100},
                              'something')
        assert False
    except KeyError:
        assert_depot()
        pass
    try:
        acc = account.FXAccount('EUR')
        acc.total_balance(exchange_rates=None)
        assert False
    except OperatingError:
        pass
    try:
        acc = account.FXAccount('EUR')
        acc.total_balance(exchange_rates=dict())
        assert False
    except OperatingError:
        pass


# noinspection PyTypeChecker
def test_update_exchange_rates():
    acc = account.FXAccount('EUR')

    assert len(acc.exchange_rates) == 0

    acc.update_exchange_rate(2, 'BTC', 'EUR')
    assert acc.exchange_rates['BTC', 'EUR'] == 2

    try:
        acc.update_exchange_rate('something', 'B', 'E')
        assert False
    except TypeError:
        pass
    try:
        acc.update_exchange_rate(2, 2, 'B')
        assert False
    except TypeError:
        pass
    try:
        acc.update_exchange_rate(2, 'B', 2)
        assert False
    except TypeError:
        pass


def test_batch_update_exchange_rates():
    acc = account.FXAccount('EUR')

    assert len(acc.exchange_rates) == 0

    acc.batch_update_exchange_rates([1, 2, 3], [('EUR', 'BTC'), ('EUR', 'ETC'), ('EUR', 'USD')])
    assert acc.exchange_rates['EUR', 'BTC'] == 1
    assert acc.exchange_rates['EUR', 'ETC'] == 2
    assert acc.exchange_rates['EUR', 'USD'] == 3
    assert acc.is_exchange_rate_updated is True

    try:
        acc.batch_update_exchange_rates([1, 2, None], [('EUR', 'BTC'), ('EUR', 'ETC'), ('EUR', 'USD')])
        assert False
    except TypeError:
        pass
    try:
        acc.batch_update_exchange_rates([1, 2, 'something'], [('EUR', 'BTC'), ('EUR', 'ETC'), ('EUR', 'USD')])
        assert False
    except TypeError:
        pass
    try:
        acc.batch_update_exchange_rates([1, 2, 3], [('EUR', 4), ('EUR', 'ETC'), ('EUR', 'USD')])
        assert False
    except TypeError:
        pass
    try:
        acc.batch_update_exchange_rates([], [('EUR', 'BTC'), ('EUR', 'ETC'), ('EUR', 'USD')])
        assert False
    except IndexError:
        pass
    try:
        acc.batch_update_exchange_rates([1, 2, 3], [])
        assert False
    except IndexError:
        pass
    try:
        acc.batch_update_exchange_rates([1, 2, 3], [('EUR', None), ('EUR', 'ETC'), ('EUR', 'USD')])
        assert False
    except TypeError:
        pass
    try:
        acc.batch_update_exchange_rates([1, 2, None], [None, None, None])
        assert False
    except TypeError:
        pass
    try:
        acc.batch_update_exchange_rates([1, 2, 3], [(None, None), ('EUR', 'ETC'), ('EUR', 'USD')])
        assert False
    except TypeError:
        pass
    try:
        acc.batch_update_exchange_rates([1, 2, 3], ['EUR', ('EUR', 'ETC'), ('EUR', 'USD')])
        assert False
    except TypeError:
        pass
    try:
        acc.batch_update_exchange_rates([1, 2, 3], [None, ('EUR', 'ETC'), ('EUR', 'USD')])
        assert False
    except TypeError:
        pass
    try:
        acc.batch_update_exchange_rates([1, 2, 3], [1, ('EUR', 'ETC'), ('EUR', 'USD')])
        assert False
    except TypeError:
        pass
    try:
        acc.batch_update_exchange_rates([1, 2, (3, 2)], [None, ('EUR', 'ETC'), ('EUR', 'USD')])
        assert False
    except TypeError:
        pass
    try:
        acc.batch_update_exchange_rates([1, 2, [3, 2]], [None, ('EUR', 'ETC'), ('EUR', 'USD')])
        assert False
    except TypeError:
        pass


# noinspection PyUnusedLocal,PyTypeChecker
def test_ignored_and_debit_buy():
    acc = account.FXAccount('EUR')
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100
    confirmation = acc.buy(1000, 1, 'EUR', 'BTC', coverage='ignore')
    assert confirmation == -1

    acc.buy(1000, 1, 'EUR', 'BTC', coverage='debit')
    assert acc.depot['BTC'] == -900


# noinspection PyUnusedLocal,PyTypeChecker
def test_ignored_and_debit_sell():
    acc = account.FXAccount('EUR')
    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100
    confirmation = acc.sell(1000, 1, 'EUR', 'BTC', coverage='ignore')
    assert confirmation == -1

    acc.sell(1000, 1, 'EUR', 'BTC', coverage='debit')
    assert acc.depot['EUR'] == -900


# noinspection PyUnusedLocal
def test_coverage_exception_deposit():
    acc = account.FXAccount('EUR')
    acc.deposit(5, 'EUR')

    try:
        acc.deposit(100, 'EUR', coverage='somethings', fee=10)
        assert False
    except NotImplementedError:
        pass
    try:
        acc.deposit(100, 'EUR', fee=10, float_fee_currency='BTC')
        assert False
    except PositionNAError:
        pass


# noinspection PyUnusedLocal
def test_full_reset():
    acc = account.FXAccount('EUR')
    acc.check_marked_coverage = None
    acc.tick(12)

    ref_acc = account.FXAccount('EUR')

    check_keys = ['check_marked_coverage', 'depot', 'exchange_rates', 'exec_heap', 'is_exchange_rate_updated',
                  '_c_is_heap']

    count = 0
    for key in check_keys:
        if getattr(acc, key) == getattr(ref_acc, key):
            count += 1
    assert len(check_keys) != count
    assert ref_acc.clock != acc.clock
    assert ref_acc.reference_currency == acc.reference_currency

    acc._full_reset()
    count = 0
    for key in check_keys:
        if getattr(acc, key) == getattr(ref_acc, key):
            count += 1
    assert len(check_keys) == count
    assert ref_acc.clock == acc.clock == 0
    assert ref_acc.reference_currency == acc.reference_currency

    acc.reference_currency = 'USD'
    acc._full_reset()
    assert acc.reference_currency == 'USD'


def test_reset():
    acc = account.FXAccount('USD')

    # noinspection PyUnusedLocal
    def _f(amount, price, base, quote, dur):
        return 1, 'EUR', 1

    # noinspection PyUnusedLocal
    def _false_fee(amount, price, base):
        return 1, 'EUR', 1

    # noinspection PyUnusedLocal
    def _false_fee_2(amount, price, base, quote, duration, volatility):
        return 2, 'EUR', 1

    # noinspection PyUnusedLocal
    def _false_fee_3(amount, price, base, quote, duration):
        return 2, 1, 1

    # noinspection PyUnusedLocal
    def _false_fee_4(amount, price, base, quote, duration):
        return 2, 1

    acc.check_marked_coverage = None
    acc.tick(12)
    try:
        acc._fee = {'sell': _false_fee}
        assert False
    except TypeError:
        pass
    try:
        acc._fee = {'sell': _false_fee_2}
        assert False
    except TypeError:
        pass
    try:
        acc._fee = {'sell': _false_fee_3}
        assert False
    except TypeError:
        pass
    try:
        acc._fee = {'sell': _false_fee_4}
        assert False
    except TypeError:
        pass
    try:
        acc._fee = _false_fee
        assert False
    except (TypeError, KeyError):
        pass
    try:
        acc._fee = {'sell': _f, 'something': _f}
    except (TypeError, KeyError):
        pass

    acc._c_fee[b'sell'] = _f
    acc._c_depot[b'EUR'] = 2
    acc.exchange_rates = {('EUR', 'USD'): 2}
    acc.is_exchange_rate_updated = True
    acc.is_heap = True

    ref_acc = account.FXAccount('EUR')

    check_keys = ['exchange_rates', 'exec_heap', 'is_exchange_rate_updated',
                  '_c_is_heap']

    count = 0
    for key in check_keys:
        if getattr(acc, key) == getattr(ref_acc, key):
            count += 1
    assert len(check_keys) != count
    assert ref_acc.clock != acc.clock
    assert acc.check_marked_coverage != ref_acc.check_marked_coverage
    assert ref_acc.reference_currency != acc.reference_currency
    assert acc._fee['sell'] == _f
    assert acc.depot['EUR'] == 2

    acc._reset()
    count = 0
    for key in check_keys:
        if getattr(acc, key) == getattr(ref_acc, key):
            count += 1
    assert len(check_keys) == count
    assert ref_acc.clock == acc.clock == 0
    assert acc.check_marked_coverage != ref_acc.check_marked_coverage
    assert ref_acc.reference_currency != acc.reference_currency
    assert acc._fee['sell'] == _f
    assert len(acc.depot) == 0 == len(ref_acc.depot)

    acc.reference_currency = 'USD'
    acc._reset()
    assert acc.reference_currency == 'USD'


# noinspection PyTypeChecker
def test_eval_fee():
    acc = account.FXAccount('EUR')

    try:
        acc._eval_fee('withdraw', dict, 1, 1, 'EUR', 'USD', 1)
        assert False
    except NotImplementedError:
        pass

    try:
        acc._eval_fee('withdraw', 'test', 1, 2, 'EUR', 'USD', 1)
        assert False
    except NotImplementedError:
        pass


def test_check_types_exception():
    a = 1
    b = 2
    try:
        check_types([a, b], [int, float], ['a'])
        assert False
    except IndexError:
        pass


# noinspection PyTypeChecker
def test_check_alt_fee_exception():
    acc = account.FXAccount('EUR')
    try:
        acc._check_alt_fee('something', 'no')
        assert False
    except NotImplementedError:
        pass
    try:
        acc._check_alt_fee(dict(), 'no')
        assert False
    except NotImplementedError:
        pass
    try:
        acc._check_alt_fee('test', 'no')
        assert False
    except NotImplementedError:
        pass


# noinspection PyTypeChecker
def test_parse_fee_and_transaction_params():
    acc = account.FXAccount('EUR')
    try:
        _ = acc._parse_fee_and_transaction_params(None, 'test', dict(), 'no', False, 3)
        assert False
    except NotImplementedError:
        pass
    try:
        _ = acc._parse_fee_and_transaction_params(None, None, None, 'no', False, 3)
        assert False
    except NotImplementedError:
        pass
    try:
        _ = acc._parse_fee_and_transaction_params('EUR', 'EUR', dict(), 'no', False, 3)
        assert False
    except NotImplementedError:
        pass
    try:
        _ = acc._parse_fee_and_transaction_params('EUR', 'EUR', 'test', 'no', False, 3)
        assert False
    except NotImplementedError:
        pass


# noinspection PyUnusedLocal,PyTypeChecker
def test_debit_series():
    acc = account.FXAccount('EUR')

    acc._c_depot[b'EUR'] = 100
    acc._c_depot[b'BTC'] = 100

    acc.withdraw(200, 'BTC', processing_duration=2, coverage='debit')
    assert acc.depot['BTC'] == 100
    acc.tick()

    acc.buy(10, 1, 'EUR', 'BTC')
    acc.sell(5, 1, 'EUR', 'BTC', fee=5, float_fee_currency='BTC')
    try:
        acc.buy(10, 1, 'EUR', 'BTC', processing_duration=2)
        assert False
    except CoverageError:
        pass
    assert acc.depot['BTC'] == 90
    acc.tick()
    assert acc.depot['BTC'] == -110

    acc.sell(100, 2, 'EUR', 'BTC')
    assert acc.depot['BTC'] == 90


def test_check_is_valid_fee_func():
    # noinspection PyUnusedLocal
    def _fee(amount, price, base, quote, duration):
        return 1, 2

    # noinspection PyUnusedLocal
    def _fee_2(amount, price, base, quote, duration):
        return 1, 2, 3, 4

    acc = account.FXAccount('EUR')

    try:
        acc._check_is_valid_fee_func(_fee)
        assert False
    except TypeError:
        pass

    try:
        acc._check_is_valid_fee_func(_fee_2)
        assert False
    except TypeError:
        pass


def test_abstract_base_class():
    try:
        # noinspection PyUnusedLocal
        base = account.BaseAccount()
        assert False
    except TypeError:
        pass


# noinspection PyUnusedLocal
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_avoid_debiting():
    acc = account.FXAccount('EUR', prohibit_debiting=True)
    acc._c_depot[b'EUR'] = 100
    try:
        acc.withdraw(1000, 'EUR')
        acc.tick(1)
        assert False
    except CoverageError:
        pass

    acc._c_depot[b'EUR'] = 100
    try:
        acc.withdraw(1000, 'EUR', coverage='debit')
        acc.tick(1)
        assert False
    except CoverageError:
        pass

    acc._c_depot[b'EUR'] = 100
    acc.prohibit_debiting = False
    acc.tick(1)
    acc.withdraw(200, 'EUR', coverage='debit')
    acc.tick(1)
    assert acc.depot['EUR'] == -100


# noinspection PyTypeChecker
def test_c_heap_implementation_max_element():
    # (time, action_func, volume, currency, coverage)
    exec_heap = [[5, 'sell', 10, 'EUR', 'except'],
                 [10, 'buy', 1, 'BTC', 'except'],
                 [3, 'sell', 100, 'EUR', 'except'],
                 [8, 'buy', 15, 'BTC', 'except']]
    vec_heap = cFXWrapperVectorHeap(exec_heap)
    assert vec_heap.py_max_time_step() == 10


def test_direct_key_index_access_exception():
    acc = account.FXAccount('EUR', prohibit_debiting=True)

    # noinspection PyUnusedLocal
    def _fee(amount, price, base, quote, dur):
        return 0, 'EUR', 0

    try:
        acc.depot['BTC'] = 100
        assert False
    except AttributeError:
        pass

    try:
        acc._fee['sell'] = _fee
        assert False
    except AttributeError:
        pass

    try:
        acc.exchange_rates['EUR', 'BTC'] = 1
        assert False
    except AttributeError:
        pass

    try:
        acc.exec_heap[0] = [1, 'sell', 10, 'EUR', 'except']
        assert False
    except AttributeError:
        pass


def test_fee_setter_exception():
    acc = account.FXAccount('EUR')

    # noinspection PyUnusedLocal
    def _fee(amount, price, base, quote, dur):
        return 0, 'EUR', 0

    try:
        acc._fee = ['something']
        assert False
    except (TypeError, KeyError):
        pass

    try:
        acc._fee = {'something': 2}
        assert False
    except (TypeError, KeyError):
        pass

    # this is now expected behavior
    # try:
    #     acc._fee = {'sell': _fee, 'buy': _fee}
    #     assert False
    # except (TypeError, KeyError):
    #     pass

    try:
        acc._fee = {'sell': 1, 'buy': 3, 'withdraw': 2, 'deposit': 6}
        assert False
    except (TypeError, KeyError):
        pass

    acc._fee = {'sell': _fee, 'buy': _fee, 'withdraw': _fee, 'deposit': _fee}


def test_parse_exec_heap_exception():
    acc = account.FXAccount('EUR')

    try:
        acc.exec_heap = [[0, 'c_withdraw', 10, 'EUR', 'something']]
        assert False
    except ValueError:
        pass

    try:
        acc.exec_heap = {'a': 2, 'b': 3, 'c': 4}
        assert False
    except (TypeError, ValueError):
        pass

    try:
        acc.exec_heap = np.array([1, 2, 3, 4])
        assert False
    except (TypeError, ValueError):
        pass


# noinspection PyArgumentList,PyTypeChecker
def test_buy_fee_func():
    # base|quote price: quote/base in mathematical terms
    # we suppose price is given as base|quote and volume is given in base volume

    # fees in quote
    # noinspection PyUnusedLocal
    def buy_fee(volume, price, base, quote, processing_duration):
        # return fee_amount, fee_currency, fee_exec_time
        # we want to bill fees in quote currency: volume given in base currency so we have to convert
        return volume * 0.1 * price, quote, 0

    acc = account.FXAccount('EUR', fee_buy=buy_fee)
    acc.deposit(100, 'EUR')
    acc.buy(5, 2, 'BTC', 'EUR')

    assert acc.depot['EUR'] == 100 - 10 - 1
    assert acc.depot['BTC'] == 5

    # fees in base
    # noinspection PyUnusedLocal
    def buy_fee(volume, price, base, quote, processing_duration):
        # return fee_amount, fee_currency, fee_exec_time
        # we want to bill in base currency
        # volume is given in base currency
        return volume * 0.1, base, 0

    acc = account.FXAccount('EUR', fee_buy=buy_fee)
    acc.deposit(100, 'EUR')
    acc.buy(5, 2, 'BTC', 'EUR')

    assert acc.depot['EUR'] == 100 - 10
    assert acc.depot['BTC'] == 5 - 5*0.1

    # fees in arbitrary currency
    # noinspection PyUnusedLocal
    def buy_fee(volume, price, base, quote, processing_duration):
        # return fee_amount, fee_currency, fee_exec_time
        return 1, 'ETH', 0

    acc = account.FXAccount('EUR', fee_buy=buy_fee)
    acc.deposit(100, 'EUR')
    acc.deposit(100, 'ETH')
    acc.buy(5, 2, 'BTC', 'EUR')

    assert acc.depot['EUR'] == 100 - 10
    assert acc.depot['ETH'] == 100 - 1
    assert acc.depot['BTC'] == 5


# noinspection PyArgumentList,PyTypeChecker
def test_sell_fee_func():
    # base|quote price: quote/base in mathematical terms
    # we suppose price is given as base|quote and volume is given in base volume

    # fees in base
    # noinspection PyUnusedLocal
    def sell_fee(volume, price, base, quote, processing_duration):
        # volume is already in base
        return volume * 0.1, base, 0

    acc = account.FXAccount('EUR', fee_sell=sell_fee)
    acc.deposit(100, 'BTC')
    acc.sell(10, 2, 'BTC', 'EUR')

    assert acc.depot['EUR'] == 20
    assert acc.depot['BTC'] == 100 - 10 - 1

    # fees in quote
    # noinspection PyUnusedLocal
    def sell_fee(volume, price, base, quote, processing_duration):
        # we want to bill in quote
        # volume is given in base, price is given in base|quote notation, so we have to convert
        fee_amount = volume * 0.1 * price
        return fee_amount, quote, 0

    acc = account.FXAccount('EUR', fee_sell=sell_fee)
    acc.deposit(100, 'BTC')
    acc.sell(10, 2, 'BTC', 'EUR')

    assert acc.depot['EUR'] == 20 - 2
    assert acc.depot['BTC'] == 100 - 10

    # fees in arbitrary currency
    # noinspection PyUnusedLocal
    def sell_fee(volume, price, base, quote, processing_duration):
        # return fee_amount, fee_currency, fee_exec_time
        return 1, 'ETH', 0

    acc = account.FXAccount('EUR', fee_sell=sell_fee)
    acc.deposit(100, 'BTC')
    acc.deposit(100, 'ETH')
    acc.sell(10, 2, 'BTC', 'EUR')

    assert acc.depot['EUR'] == 20
    assert acc.depot['BTC'] == 100 - 10
    assert acc.depot['ETH'] == 100 - 1


def test_deposit_fee_func():
    # base|quote price: quote/base in mathematical terms
    # we suppose volume is given in base volume (there's no currency pair within this transaction type, so we just call
    # the currency base anyways)

    # fees in base
    # noinspection PyUnusedLocal
    def deposit_fee(volume, price, base, quote, processing_duration):
        # function arguments pre-set to:
        # deposit_fee((volume, 1, currency, currency, processing_duration)
        # returns fee_amount, fee_currency, fee_exec_time
        return volume * 0.1, base, 0

    acc = account.FXAccount('EUR', fee_deposit=deposit_fee)
    acc.deposit(100, 'EUR')
    acc.deposit(100, 'BTC')

    assert acc.depot['EUR'] == 100 - 10
    assert acc.depot['BTC'] == 100 - 10

    # there's no quote currency, so the only option is to test against arbitrary currency
    # fees in arbitrary currency
    # noinspection PyUnusedLocal
    def deposit_fee(volume, price, base, quote, processing_duration):
        # return fee_amount, fee_currency, fee_exec_time
        return 1, 'ETH', 0

    acc = account.FXAccount('EUR', fee_deposit=deposit_fee)
    acc.deposit(101, 'ETH')
    acc.deposit(100, 'EUR')

    assert acc.depot['ETH'] == 101 - 1 - 1
    assert acc.depot['EUR'] == 100

    # fees exceeding deposit amount
    # noinspection PyUnusedLocal
    def deposit_fee(volume, price, base, quote, processing_duration):
        return volume * 1.1, base, 0

    acc = account.FXAccount('EUR', fee_deposit=deposit_fee)
    acc._c_depot[b'EUR'] = 100
    acc.deposit(100, 'EUR')

    assert acc.depot['EUR'] == 100 - (100 * 1.1) + 100


def test_withdraw_fee_func():
    # base|quote price: quote/base in mathematical terms
    # we suppose volume is given in base volume (there's no currency pair within this transaction type, so we just call
    # the currency base anyways)

    # fees in base
    # noinspection PyUnusedLocal
    def withdraw_fee(volume, price, base, quote, processing_duration):
        # function arguments pre-set to:
        # deposit_fee((volume, 1, currency, currency, processing_duration)
        # returns fee_amount, fee_currency, fee_exec_time
        return volume * 0.1, base, 0

    acc = account.FXAccount('EUR', fee_withdraw=withdraw_fee)
    acc.deposit(100, 'EUR')
    acc.withdraw(10, 'EUR')

    assert acc.depot['EUR'] == 100 - 10 - 1

    # there's no quote currency, so the only option is to test against arbitrary currency
    # fees in arbitrary currency
    # noinspection PyUnusedLocal
    def withdraw_fee(volume, price, base, quote, processing_duration):
        # return fee_amount, fee_currency, fee_exec_time
        return 1, 'ETH', 0

    acc = account.FXAccount('EUR', fee_withdraw=withdraw_fee)
    acc.deposit(100, 'EUR')
    acc.deposit(100, 'ETH')
    acc.withdraw(10, 'EUR')

    assert acc.depot['EUR'] == 100 - 10
    assert acc.depot['ETH'] == 100 - 1

    # fees exceeding withdrawal amount
    # noinspection PyUnusedLocal
    def withdraw_fee(volume, price, base, quote, processing_duration):
        return volume * 1.1, base, 0

    acc = account.FXAccount('EUR', fee_withdraw=withdraw_fee)
    acc.deposit(100, 'EUR')
    acc.withdraw(10, 'EUR')

    assert acc.depot['EUR'] == 100 - 10 - 10*1.1

    acc = account.FXAccount('EUR', fee_withdraw=withdraw_fee)
    acc.deposit(100, 'EUR')
    acc.withdraw(50, 'EUR', coverage='partial')

    assert acc.depot['EUR'] == 0
