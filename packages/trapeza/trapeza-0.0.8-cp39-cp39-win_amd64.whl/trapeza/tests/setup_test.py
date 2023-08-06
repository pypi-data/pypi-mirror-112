import math
from decimal import Decimal
import numpy as np

from trapeza.account import FXAccount
from trapeza.strategy import FXStrategy
from trapeza.arithmetics.arithmetics import py_libmpdec_div


def setup_accs(ref_currencies=('EUR', 'LTC', 'BTC')):
    accs = [FXAccount(ref_cur, ignore_type_checking=True) for ref_cur in ref_currencies]
    for acc in accs:
        for cur in ref_currencies:
            acc._c_depot[cur.encode()] = 500
    return accs


def setup_large_accs(ref_currencies=('EUR', 'LTC', 'BTC')):
    accs = [FXAccount(ref_cur, ignore_type_checking=True) for ref_cur in ref_currencies]
    for acc in accs:
        for cur in ref_currencies:
            acc._c_depot[cur.encode()] = 5000000
    return accs


# noinspection PyTypeChecker
def setup_strategies(ref_currencies=('EUR', 'LTC', 'BTC')):
    accs = setup_accs(ref_currencies)
    strat_1 = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking, 10)
    strat_2 = FXStrategy('benchmark', [accs[0]], strategy_func_single_w_ticking_kwargs, 2)
    return [strat_1, strat_2]


# noinspection PyTypeChecker
def setup_large_strategies(ref_currencies=('EUR', 'LTC', 'BTC')):
    accs = setup_large_accs(ref_currencies)
    strat_1 = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking, 10, ignore_type_checking=True)
    strat_2 = FXStrategy('benchmark', [accs[0]], strategy_func_single_w_ticking_kwargs, 2, ignore_type_checking=True)
    return [strat_1, strat_2]


# noinspection PyTypeChecker
def setup_strategies_alt(ref_currencies=('EUR', 'LTC', 'BTC')):
    accs = setup_accs(ref_currencies)
    accs[1].clock = 100
    strat_1 = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking, 10)
    strat_2 = FXStrategy('benchmark', [accs[0]], strategy_func_single_w_ticking_kwargs, 2)
    return [strat_1, strat_2]


def setup_data():
    np.random.seed(42)

    data = dict()
    data[('BTC', 'EUR')] = np.linspace(0.1, 5, 100) + np.random.normal(0, 0.1, 100)
    data[('LTC', 'EUR')] = np.linspace(6, 3, 100) + np.random.normal(0, 0.1, 100)
    data[('BTC', 'LTC')] = data[('BTC', 'EUR')] / data[('LTC', 'EUR')]

    return data


def setup_large_data():
    np.random.seed(42)

    data = dict()
    data[('BTC', 'EUR')] = np.linspace(0.1, 5, 1000) + np.random.normal(0, 0.1, 1000)
    data[('LTC', 'EUR')] = np.linspace(6, 3, 1000) + np.random.normal(0, 0.1, 1000)
    data[('BTC', 'LTC')] = data[('BTC', 'EUR')] / data[('LTC', 'EUR')]

    return data


def setup_volume_data():
    np.random.seed(42)

    data = dict()
    data[('BTC', 'EUR')] = np.linspace(10, 50, 100) + np.random.normal(0, 1, 100)
    data[('LTC', 'EUR')] = np.linspace(60, 300, 100) + np.random.normal(0, 1, 100)
    data[('BTC', 'LTC')] = np.linspace(8, 100, 100) + np.random.normal(0, 1, 100)

    return data


# noinspection DuplicatedCode
# noinspection PyUnusedLocal
def strategy_func_single_wo_ticking(accs, data, ref_currency, volume, fxstrat):
    acc = accs[0]
    if 0 < data['BTC', 'EUR'][-1] < 1:
        acc.buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(acc, 'buy')

    elif 1 <= data['BTC', 'EUR'][-1] < 2:
        acc.sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(acc, 'sell')

    elif 2 <= data['BTC', 'EUR'][-1] < 3:
        acc.buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(acc, 'buy')

    elif 3 <= data['BTC', 'EUR'][-1] < 4:
        acc.sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(acc, 'sell')

    else:
        fxstrat.add_signal(acc, 'hold')


# noinspection DuplicatedCode
# noinspection PyUnusedLocal
def strategy_func_single_wo_ticking_kwargs(accs, data, ref_currency, volume, fxstrat, strat_quack=3):
    acc = accs[0]
    if strat_quack != 3:
        raise ValueError

    if 0 < data['BTC', 'EUR'][-1] < 1:
        acc.buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(acc, 'buy')

    elif 1 <= data['BTC', 'EUR'][-1] < 2:
        acc.sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(acc, 'sell')

    elif 2 <= data['BTC', 'EUR'][-1] < 3:
        acc.buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(acc, 'buy')

    elif 3 <= data['BTC', 'EUR'][-1] < 4:
        acc.sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(acc, 'sell')

    else:
        fxstrat.add_signal(acc, 'hold')


# noinspection DuplicatedCode
# noinspection PyUnusedLocal
def strategy_func_single_w_ticking_kwargs(accs, data, ref_currency, volume, fxstrat, strat_quack=3):
    acc = accs[0]

    if strat_quack != 3:
        raise ValueError

    if 0 < data['BTC', 'EUR'][-1] < 1:
        acc.buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(acc, 'buy')

    elif 1 <= data['BTC', 'EUR'][-1] < 2:
        acc.sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(acc, 'sell')

    elif 2 <= data['BTC', 'EUR'][-1] < 3:
        acc.buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(acc, 'buy')

    elif 3 <= data['BTC', 'EUR'][-1] < 4:
        acc.sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(acc, 'sell')

    else:
        fxstrat.add_signal(acc, 'hold')

    if hasattr(acc, '_order_heap'):
        data_single_point = {k: data[k][-1] for k in data.keys()}
        acc.tick(data_single_point)
    else:
        acc.tick()


# noinspection DuplicatedCode
# noinspection PyUnusedLocal
def strategy_func_multi_wo_ticking(accs, data, ref_currency, volume, fxstrat):
    if 0 < data['BTC', 'EUR'][-1] < 1:
        accs[0].buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[0], 'buy_BTC_EUR')

        accs[1].sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[1], 'sell_BTC_EUR')

    elif 1 <= data['BTC', 'EUR'][-1] < 2:
        accs[0].sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[0], 'sell_BTC_EUR')

        accs[1].buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[1], 'buy_BTC_EUR')

    elif 2 <= data['BTC', 'EUR'][-1] < 3:
        accs[0].buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[0], 'buy_BTC_EUR')

        accs[1].sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[1], 'sell_BTC_EUR')

    elif 3 <= data['BTC', 'EUR'][-1] < 4:
        accs[0].sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[0], 'sell_BTC_EUR')

        accs[1].buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[1], 'buy_BTC_EUR')

    else:
        fxstrat.add_signal(accs[0], 'hold_BTC_EUR')
        fxstrat.add_signal(accs[1], 'hold_BTC_EUR')

    # ----------------------------------------------------
    # LTC
    # ----------------------------------------------------
    if 0 < data['LTC', 'EUR'][-1] < 1:
        accs[2].buy(py_libmpdec_div(1, data['LTC', 'EUR'][-1]), data['LTC', 'EUR'][-1], 'LTC', 'EUR')
        fxstrat.add_signal(accs[2], 'buy')

    elif 1 <= data['LTC', 'EUR'][-1] < 2:
        accs[2].sell(1, data['LTC', 'EUR'][-1], 'LTC', 'EUR')
        fxstrat.add_signal(accs[2], 'sell')

    elif 2 <= data['LTC', 'EUR'][-1] < 3:
        accs[2].buy(py_libmpdec_div(1, data['LTC', 'EUR'][-1]), data['LTC', 'EUR'][-1], 'LTC', 'EUR')
        fxstrat.add_signal(accs[2], 'buy')

    elif 3 <= data['LTC', 'EUR'][-1] < 4:
        accs[2].sell(1, data['LTC', 'EUR'][-1], 'LTC', 'EUR')
        fxstrat.add_signal(accs[2], 'sell')

    else:
        fxstrat.add_signal(accs[2], 'hold')


# noinspection DuplicatedCode
# noinspection PyUnusedLocal
def strategy_func_multi_wo_ticking_kwargs(accs, data, ref_currency, volume, fxstrat, strat_quack=3):
    if strat_quack != 3:
        raise ValueError

    if 0 < data['BTC', 'EUR'][-1] < 1:
        accs[0].buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[0], 'buy')

        accs[1].sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[1], 'sell')

    elif 1 <= data['BTC', 'EUR'][-1] < 2:
        accs[0].sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[0], 'sell')

        accs[1].buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[1], 'buy')

    elif 2 <= data['BTC', 'EUR'][-1] < 3:
        accs[0].buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[0], 'buy')

        accs[1].sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[1], 'sell')

    elif 3 <= data['BTC', 'EUR'][-1] < 4:
        accs[0].sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[0], 'sell')

        accs[1].buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[1], 'buy')

    else:
        fxstrat.add_signal(accs[0], 'hold')
        fxstrat.add_signal(accs[1], 'hold')

    # ----------------------------------------------------
    # LTC
    # ----------------------------------------------------
    if 0 < data['LTC', 'EUR'][-1] < 1:
        accs[2].buy(py_libmpdec_div(1, data['LTC', 'EUR'][-1]), data['LTC', 'EUR'][-1], 'LTC', 'EUR')
        fxstrat.add_signal(accs[2], 'buy')

    elif 1 <= data['LTC', 'EUR'][-1] < 2:
        accs[2].sell(1, data['LTC', 'EUR'][-1], 'LTC', 'EUR')
        fxstrat.add_signal(accs[2], 'sell')

    elif 2 <= data['LTC', 'EUR'][-1] < 3:
        accs[2].buy(py_libmpdec_div(1, data['LTC', 'EUR'][-1]), data['LTC', 'EUR'][-1], 'LTC', 'EUR')
        fxstrat.add_signal(accs[2], 'buy')

    elif 3 <= data['LTC', 'EUR'][-1] < 4:
        accs[2].sell(1, data['LTC', 'EUR'][-1], 'LTC', 'EUR')
        fxstrat.add_signal(accs[2], 'sell')

    else:
        fxstrat.add_signal(accs[2], 'hold')


# noinspection DuplicatedCode
# noinspection PyUnusedLocal
def strategy_func_multi_w_ticking_kwargs(accs, data, ref_currency, volume, fxstrat, strat_quack=3):
    if strat_quack != 3:
        raise ValueError

    if 0 < data['BTC', 'EUR'][-1] < 1:
        accs[0].buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[0], 'buy')

        accs[1].sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[1], 'sell')

    elif 1 <= data['BTC', 'EUR'][-1] < 2:
        accs[0].sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[0], 'sell')

        accs[1].buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[1], 'buy')

    elif 2 <= data['BTC', 'EUR'][-1] < 3:
        accs[0].buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[0], 'buy')

        accs[1].sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[1], 'sell')

    elif 3 <= data['BTC', 'EUR'][-1] < 4:
        accs[0].sell(1, data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[0], 'sell')

        accs[1].buy(py_libmpdec_div(1, data['BTC', 'EUR'][-1]), data['BTC', 'EUR'][-1], 'BTC', 'EUR')
        fxstrat.add_signal(accs[1], 'buy')

    else:
        fxstrat.add_signal(accs[0], 'hold')
        fxstrat.add_signal(accs[1], 'hold')

    # ----------------------------------------------------
    # LTC
    # ----------------------------------------------------
    if 0 < data['LTC', 'EUR'][-1] < 1:
        accs[2].buy(py_libmpdec_div(1, data['LTC', 'EUR'][-1]), data['LTC', 'EUR'][-1], 'LTC', 'EUR')
        fxstrat.add_signal(accs[2], 'buy')

    elif 1 <= data['LTC', 'EUR'][-1] < 2:
        accs[2].sell(1, data['LTC', 'EUR'][-1], 'LTC', 'EUR')
        fxstrat.add_signal(accs[2], 'sell')

    elif 2 <= data['LTC', 'EUR'][-1] < 3:
        accs[2].buy(py_libmpdec_div(1, data['LTC', 'EUR'][-1]), data['LTC', 'EUR'][-1], 'LTC', 'EUR')
        fxstrat.add_signal(accs[2], 'buy')

    elif 3 <= data['LTC', 'EUR'][-1] < 4:
        accs[2].sell(1, data['LTC', 'EUR'][-1], 'LTC', 'EUR')
        fxstrat.add_signal(accs[2], 'sell')

    else:
        fxstrat.add_signal(accs[2], 'hold')

    # ----------------------------------------------------
    # ticking
    # ----------------------------------------------------
    for acc in accs:
        if hasattr(acc, '_order_heap'):
            data_single_point = {k: data[k][-1] for k in data.keys()}
            acc.tick(data_single_point)
        else:
            acc.tick()


# noinspection PyUnusedLocal,PyProtectedMember
def strategy_func_single_volume_wo_ticking(accs, data, ref_currency, volume, fxstrat):
    acc = accs[0]
    acc._c_depot[b'BTC'] = volume['BTC', 'EUR'][-1]


# noinspection DuplicatedCode
def subroutine_add_accum(add_method, dec_cxt, iterations=1000):
    """
    Routine for testing arbitrary precision arithmetics
    :param add_method: method
    :param dec_cxt: decimal.Context
    :param iterations: int
    :return: None
    """
    a = 0
    b = Decimal('0', dec_cxt)
    for _ in range(iterations):
        rand = np.random.random_sample()
        rand = rand + np.random.randint(0, 100, 1)[0]
        rand *= np.random.choice([1, -1], 1, p=[0.7, 0.3])[0]
        rand = math.trunc(rand * 1000000) / 1000000

        a = add_method(a, rand)
        b = b + Decimal(str(rand), dec_cxt)
        assert float(a) == float(b)


# noinspection DuplicatedCode
def subroutine_sub_accum(sub_method, dec_cxt, iterations=1000):
    """
    Routine for testing arbitrary precision arithmetics
    :param sub_method: method
    :param dec_cxt: decimal.Context
    :param iterations: int
    :return: None
    """
    a = 10000
    b = Decimal('10000', dec_cxt)
    for _ in range(iterations):
        rand = np.random.random_sample()
        rand = rand + np.random.randint(0, 100, 1)[0]
        rand *= np.random.choice([1, -1], 1, p=[0.7, 0.3])[0]
        rand = math.trunc(rand * 1000000) / 1000000

        a = sub_method(a, rand)
        b = b - Decimal(str(rand), dec_cxt)
        assert float(a) == float(b)


def subroutine_mul_accum(mul_method, dec_cxt, quant_size, iterations=1000):
    """
    Routine for testing arbitrary precision arithmetics
    :param mul_method: method
    :param dec_cxt: decimal.Context
    :param quant_size: int
    :param iterations: int
    :return: None
    """
    a = 1
    b = Decimal('1', dec_cxt)
    quantizer = Decimal('0.{}1'.format('0' * (quant_size - 1)))
    for _ in range(iterations):
        rand = np.random.random_sample()
        rand = rand + np.random.randint(0, 2, 1)[0]
        rand += 0.1
        rand *= np.random.choice([1, -1], 1, p=[0.7, 0.3])[0]
        rand = math.trunc(rand * 10) / 10

        a = mul_method(a, rand)
        b = b * Decimal(str(rand), dec_cxt)
        b = b.quantize(quantizer, context=dec_cxt)
        assert float(a) == float(b)


def subroutine_div_accum(div_method, dec_cxt, quant_size, iterations=1000):
    """
    Routine for testing arbitrary precision arithmetics
    :param div_method: method
    :param dec_cxt: decimal.Context
    :param quant_size: int
    :param iterations: int
    :return: None
    """
    a = 100000
    b = Decimal('100000', dec_cxt)
    quantizer = Decimal('0.{}1'.format('0' * (quant_size - 1)))
    for _ in range(iterations):
        rand = np.random.random_sample()
        rand = rand + np.random.randint(1, 2, 1)[0]
        rand *= np.random.choice([1, -1], 1, p=[0.7, 0.3])[0]
        rand = math.trunc(rand * 10) / 10

        a = div_method(a, rand)
        b = b / Decimal(str(rand), dec_cxt)
        b = b.quantize(quantizer, context=dec_cxt)
        assert float(a) == float(b)
