# noinspection PyUnresolvedReferences,PyPackageRequirements
import pytest
import numpy as np
import math

from trapeza.account.order_management import monkey_patch
from trapeza.strategy import FXStrategy
from trapeza.exception import AccountError, OperatingError
from trapeza import utils
import trapeza

from trapeza.tests.setup_test import setup_accs, setup_data, setup_volume_data, \
    strategy_func_single_wo_ticking, strategy_func_single_wo_ticking_kwargs, strategy_func_single_w_ticking_kwargs, \
    strategy_func_multi_wo_ticking, strategy_func_multi_wo_ticking_kwargs, strategy_func_multi_w_ticking_kwargs, \
    strategy_func_single_volume_wo_ticking


def test_add_signal():
    acc = setup_accs()[0]
    strat = FXStrategy('genesis', acc, strategy_func_single_wo_ticking, 0)

    strat.add_signal([acc], 'something')

    assert len(strat._signals_at_step_t) != 0


def test_init_single_acc():
    acc = setup_accs()[0]

    # without kwargs
    strat = FXStrategy('genesis', acc, strategy_func_single_wo_ticking, 10)
    assert strat.name == 'genesis'
    assert strat.lookback == 10
    assert strat.accounts[0] == acc
    assert strat.suppress_ticking is False
    assert strat.tick_method.__name__ == trapeza.strategy.fx_strategy._c_tick_method.__name__
    assert len(strat.strategy_kwargs) == 0
    assert len(strat.tick_kwargs) == 0

    # with kwargs
    # noinspection PyUnusedLocal
    def some_ticking(self, tick_quack, some_quack):
        return

    strat = FXStrategy('genesis', [acc], strategy_func_single_wo_ticking_kwargs, 10, tick_func=some_ticking,
                       strat_quack=3, some_quack=10, suppress_ticking=True)
    assert strat.lookback == 10
    assert strat.accounts[0] == acc
    assert strat.suppress_ticking is True
    assert strat.tick_method.__name__ == some_ticking.__name__
    assert strat.strategy_kwargs['strat_quack'] == 3
    assert strat.tick_kwargs['some_quack'] == 10

    strat = FXStrategy('genesis', [acc], strategy_func_single_wo_ticking_kwargs, 10, strat_quack=3,
                       suppress_ticking=True)
    assert strat.lookback == 10
    assert strat.accounts[0] == acc
    assert strat.suppress_ticking is True
    assert strat.tick_method.__name__ == trapeza.strategy.fx_strategy._c_tick_method.__name__
    assert strat.strategy_kwargs['strat_quack'] == 3
    assert len(strat.tick_kwargs) == 0

    # with patched: shouldn't make any difference


def test_init_multi_acc():
    accs = setup_accs()

    # without kwargs
    strat = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking, 10)
    assert strat.lookback == 10
    assert len(strat.accounts) == len(accs)
    assert strat.suppress_ticking is False
    assert strat.tick_method.__name__ == trapeza.strategy.fx_strategy._c_tick_method.__name__
    assert len(strat.strategy_kwargs) == 0
    assert len(strat.tick_kwargs) == 0

    # with kwargs
    # noinspection PyUnusedLocal
    def some_ticking(self, tick_quack, some_quack):
        return

    strat = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking_kwargs, 10, tick_func=some_ticking,
                       strat_quack=3, some_quack=10, suppress_ticking=True)
    assert strat.lookback == 10
    assert len(strat.accounts) == len(accs)
    assert strat.suppress_ticking is True
    assert strat.tick_method.__name__ == some_ticking.__name__
    assert strat.strategy_kwargs['strat_quack'] == 3
    assert strat.tick_kwargs['some_quack'] == 10

    strat = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking_kwargs, 10, strat_quack=3, suppress_ticking=True)
    assert strat.lookback == 10
    assert len(strat.accounts) == len(accs)
    assert strat.suppress_ticking is True
    assert strat.tick_method.__name__ == trapeza.strategy.fx_strategy._c_tick_method.__name__
    assert strat.strategy_kwargs['strat_quack'] == 3
    assert len(strat.tick_kwargs) == 0

    # with patched: shouldn't make any difference


def test_reset_single_acc():
    acc = setup_accs()[0]
    strat = FXStrategy('genesis', acc, strategy_func_single_wo_ticking, 10)

    acc.sell(1, 1, 'BTC', 'LTC', processing_duration=100)
    strat._signals_at_step_t = {0: ['test']}
    assert len(acc.exec_heap) != 0
    assert len(strat._signals_at_step_t) != 0

    strat.reset()
    assert len(acc.exec_heap) == 0
    assert len(strat._signals_at_step_t) == 0


def test_reset_multi_acc():
    accs = setup_accs()
    strat = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking, 10)

    for acc in accs:
        acc.sell(1, 1, 'BTC', 'LTC', processing_duration=100)
    for acc in accs:
        assert len(acc.exec_heap) != 0
    try:
        strat._signals_at_step_t = [5]
        assert False
    except TypeError:
        pass
    strat._signals_at_step_t = {0: ['test']}
    assert len(strat._signals_at_step_t) != 0

    strat.reset()
    for acc in accs:
        assert len(acc.exec_heap) == 0
    assert len(strat._signals_at_step_t) == 0


# noinspection DuplicatedCode
def test_evaluate_single_acc():
    acc = setup_accs()[0]
    strat = FXStrategy('genesis', acc, strategy_func_single_wo_ticking, 10)
    data_frame = {('BTC', 'EUR'): 2, ('LTC', 'BTC'): 500, ('LTC', 'EUR'): 0}

    # no append_to_results
    acc.buy(1, 1, 'BTC', 'EUR')
    strat.add_signal(acc, 'buy')

    signals, positions, total_balances = strat.evaluate(data_frame, 'EUR', False)
    signals_copy = signals[:]
    assert signals[0][0] == 'buy'
    assert positions[0]['BTC'] == 501
    assert positions[0]['EUR'] == 499
    assert float(total_balances[0]) == float(499 + 501 * 2)
    assert len(strat._signals_at_step_t) != 0
    assert (len(strat.positions) == len(strat.merged_positions) == len(strat.total_balances)
            == len(strat.merged_total_balances) == len(strat.signals) == 0)
    assert acc.position('BTC') == 501
    assert acc.position('EUR') == 499
    assert acc.clock == 0

    # test re-call
    signals, positions, total_balances = strat.evaluate(data_frame, 'EUR', False)
    assert utils.is_empty_list(signals) is False
    assert signals == signals_copy
    assert positions[0]['BTC'] == 501
    assert positions[0]['EUR'] == 499
    assert total_balances[0] == 499 + 501 * 2
    assert len(strat._signals_at_step_t) != 0
    assert (len(strat.positions) == len(strat.merged_positions) == len(strat.total_balances)
            == len(strat.merged_total_balances) == len(strat.signals) == 0)
    assert acc.position('BTC') == 501
    assert acc.position('EUR') == 499
    assert acc.clock == 0

    # append_to_results
    strat.add_signal(acc, 'buy')
    signals, positions, total_balances = strat.evaluate(data_frame, 'EUR', True)
    assert signals[0][0] == 'buy' == strat.signals[0][0][0]
    assert positions[0]['BTC'] == 501 == strat.positions['BTC'][0][0] == strat.merged_positions['BTC'][0]
    assert positions[0]['EUR'] == 499 == strat.positions['EUR'][0][0] == strat.merged_positions['EUR'][0]
    assert total_balances[0] == 499 + 501 * 2 == strat.total_balances[0][0] == strat.merged_total_balances[0]
    assert len(strat._signals_at_step_t) == 0
    assert acc.position('BTC') == 501
    assert acc.position('EUR') == 499
    assert acc.clock == 0

    acc.tick()
    acc.buy(1, 1, 'BTC', 'EUR')
    strat.add_signal(acc, 'buy')
    signals, positions, total_balances = strat.evaluate(data_frame, 'EUR', True)
    assert signals[0][0] == 'buy' == strat.signals[1][0][0]
    assert positions[0]['BTC'] == 502 == strat.positions['BTC'][1][0] == strat.merged_positions['BTC'][1]
    assert positions[0]['EUR'] == 498 == strat.positions['EUR'][1][0] == strat.merged_positions['EUR'][1]
    assert total_balances[0] == 498 + 502 * 2 == strat.total_balances[1][0] == strat.merged_total_balances[1]
    assert len(strat._signals_at_step_t) == 0
    assert acc.position('BTC') == 502
    assert acc.position('EUR') == 498
    assert acc.clock == 1


# noinspection DuplicatedCode
def test_evaluate_multi_acc():
    accs = setup_accs()
    strat = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking, 10)
    data_frame = {('BTC', 'EUR'): 2, ('LTC', 'BTC'): 500, ('LTC', 'EUR'): 0}

    # no append_to_results
    for acc in accs:
        acc.buy(1, 1, 'BTC', 'EUR')
        strat.add_signal(acc, 'buy')
    signals, positions, total_balances = strat.evaluate(data_frame, 'EUR', False)
    signals_copy = signals[:]
    for i, acc in enumerate(accs):
        assert signals[i][0] == 'buy'
        assert positions[i]['BTC'] == 501
        assert positions[i]['EUR'] == 499
        assert total_balances[i] == 499 + 501 * 2
        assert len(strat._signals_at_step_t) != 0
        assert (len(strat.positions) == len(strat.merged_positions) == len(strat.total_balances)
                == len(strat.merged_total_balances) == len(strat.signals) == 0)
        assert acc.position('BTC') == 501
        assert acc.position('EUR') == 499
        assert acc.clock == 0

    # test re-call
    signals, positions, total_balances = strat.evaluate(data_frame, 'EUR', False)
    assert utils.is_empty_list(signals) is False
    assert signals == signals_copy
    for i, acc in enumerate(accs):
        assert positions[i]['BTC'] == 501
        assert positions[i]['EUR'] == 499
        assert total_balances[i] == 499 + 501 * 2
        assert len(strat._signals_at_step_t) != 0
        assert (len(strat.positions) == len(strat.merged_positions) == len(strat.total_balances)
                == len(strat.merged_total_balances) == len(strat.signals) == 0)
        assert acc.position('BTC') == 501
        assert acc.position('EUR') == 499
        assert acc.clock == 0

    # append_to_results
    for acc in accs:
        strat.add_signal(acc, 'buy')
    signals, positions, total_balances = strat.evaluate(data_frame, 'EUR', True)
    for i, acc in enumerate(accs):
        assert signals[i][0] == 'buy' == strat.signals[0][i][0]
        assert positions[i]['BTC'] == 501 == strat.positions['BTC'][0][i]
        assert positions[i]['EUR'] == 499 == strat.positions['EUR'][0][i]
        assert total_balances[i] == 499 + 501 * 2 == strat.total_balances[0][i]
        assert len(strat._signals_at_step_t) == 0
        assert acc.position('BTC') == 501
        assert acc.position('EUR') == 499
        assert acc.clock == 0
    assert strat.merged_positions['BTC'][0] == 3 * 501
    assert strat.merged_positions['EUR'][0] == 3 * 499
    assert strat.merged_total_balances[0] == 3 * (499 + 501 * 2)

    for i, acc in enumerate(accs):
        acc.tick()
        if i == 0:
            acc.buy(2, 1, 'BTC', 'EUR')
        else:
            acc.buy(1, 1, 'BTC', 'EUR')
        strat.add_signal(acc, 'buy')
    signals, positions, total_balances = strat.evaluate(data_frame, 'EUR', True)
    for i, acc in enumerate(accs):
        assert signals[i][0] == 'buy' == strat.signals[1][i][0]
        if i == 0:
            btc = 503
            eur = 497
        else:
            btc = 502
            eur = 498
        assert positions[i]['BTC'] == btc == strat.positions['BTC'][1][i]
        assert positions[i]['EUR'] == eur == strat.positions['EUR'][1][i]
        assert total_balances[i] == eur + btc * 2 == strat.total_balances[1][i]
        assert len(strat._signals_at_step_t) == 0
        assert acc.position('BTC') == btc
        assert acc.position('EUR') == eur
        assert acc.clock == 1
    assert strat.merged_positions['BTC'][1] == 3 * 502 + 1
    assert strat.merged_positions['EUR'][1] == 3 * 498 - 1
    assert strat.merged_total_balances[1] == 3 * (498 + 502 * 2) - 1 + 1 * 2


# noinspection DuplicatedCode
def test_run_single_acc_wo_ticking():
    # unpatched
    acc = setup_accs()[0]
    strat = FXStrategy('genesis', acc, strategy_func_single_wo_ticking, 10, ignore_type_checking=True)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    assert acc.clock == len(np_data)
    assert math.isclose(merged_total_balances[-1],
                        (500 + (sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n)
                         + (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum()))
                         * data['BTC', 'EUR'][-1] + 500 * data['LTC', 'EUR'][-1]))
    assert (signals == 'buy').sum() == buy_0_1_n + buy_2_3_n
    assert (signals == 'sell').sum() == sell_1_2_n + sell_3_4_n
    assert (signals == 'hold').sum() == hold_n

    # without lookback
    acc = setup_accs()[0]
    strat = FXStrategy('genesis', acc, strategy_func_single_wo_ticking, 0, ignore_type_checking=True)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[0:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    assert acc.clock == len(np_data)
    assert math.isclose(merged_total_balances[-1],
                        (500 + (sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n)
                         + (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum()))
                         * data['BTC', 'EUR'][-1] + 500 * data['LTC', 'EUR'][-1]))
    assert (signals == 'buy').sum() == buy_0_1_n + buy_2_3_n
    assert (signals == 'sell').sum() == sell_1_2_n + sell_3_4_n
    assert (signals == 'hold').sum() == hold_n

    # patched
    acc = setup_accs()[0]
    monkey_patch(acc)
    strat = FXStrategy('genesis', acc, strategy_func_single_wo_ticking, 10, ignore_type_checking=True)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    assert acc.clock == len(np_data)
    assert math.isclose(merged_total_balances[-1],
                        (500 + (sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n)
                         + (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum()))
                         * data['BTC', 'EUR'][-1] + 500 * data['LTC', 'EUR'][-1]))
    assert (signals == 'buy').sum() == buy_0_1_n + buy_2_3_n
    assert (signals == 'sell').sum() == sell_1_2_n + sell_3_4_n
    assert (signals == 'hold').sum() == hold_n


# noinspection DuplicatedCode
def test_run_single_acc_wo_ticking_kwargs():
    # unpatched
    acc = setup_accs()[0]
    strat = FXStrategy('genesis', acc, strategy_func_single_wo_ticking_kwargs, 10, strat_quack=3)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    assert acc.clock == len(np_data)
    assert math.isclose(merged_total_balances[-1],
                        (500 + (sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n)
                         + (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum()))
                         * data['BTC', 'EUR'][-1] + 500 * data['LTC', 'EUR'][-1]))
    assert (signals == 'buy').sum() == buy_0_1_n + buy_2_3_n
    assert (signals == 'sell').sum() == sell_1_2_n + sell_3_4_n
    assert (signals == 'hold').sum() == hold_n

    # patched
    acc = setup_accs()[0]
    monkey_patch(acc)
    strat = FXStrategy('genesis', acc, strategy_func_single_wo_ticking_kwargs, 10, strat_quack=3)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    assert acc.clock == len(np_data)
    assert math.isclose(merged_total_balances[-1],
                        (500 + (sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n)
                         + (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum()))
                         * data['BTC', 'EUR'][-1] + 500 * data['LTC', 'EUR'][-1]))
    assert (signals == 'buy').sum() == buy_0_1_n + buy_2_3_n
    assert (signals == 'sell').sum() == sell_1_2_n + sell_3_4_n
    assert (signals == 'hold').sum() == hold_n

    # with custom tick
    # patched with custom tick
    def some_tick(self, data_point, acc_tick):
        data_single_point = {k: data_point[k][-1] for k in data_point.keys()}
        for _acc in acc_tick:
            _acc.tick(data_single_point)

    acc = setup_accs()[0]
    monkey_patch(acc)
    strat = FXStrategy('genesis', acc, strategy_func_single_wo_ticking_kwargs, 10, tick_func=some_tick, acc_tick=[acc],
                       strat_quack=3)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    assert acc.clock == len(np_data)
    assert math.isclose(merged_total_balances[-1],
                        (500 + (sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n)
                         + (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum()))
                         * data['BTC', 'EUR'][-1] + 500 * data['LTC', 'EUR'][-1]))
    assert (signals == 'buy').sum() == buy_0_1_n + buy_2_3_n
    assert (signals == 'sell').sum() == sell_1_2_n + sell_3_4_n
    assert (signals == 'hold').sum() == hold_n


# noinspection DuplicatedCode
def test_run_single_acc_w_ticking_kwargs():
    # unpatched
    acc = setup_accs()[0]
    strat = FXStrategy('genesis', acc, strategy_func_single_w_ticking_kwargs, 10, strat_quack=3)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    assert acc.clock == len(np_data)
    assert math.isclose(merged_total_balances[-1],
                        (500 + (sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n)
                         + (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum()))
                         * data['BTC', 'EUR'][-1] + 500 * data['LTC', 'EUR'][-1]))
    assert (signals == 'buy').sum() == buy_0_1_n + buy_2_3_n
    assert (signals == 'sell').sum() == sell_1_2_n + sell_3_4_n
    assert (signals == 'hold').sum() == hold_n

    # patched
    acc = setup_accs()[0]
    monkey_patch(acc)
    strat = FXStrategy('genesis', acc, strategy_func_single_w_ticking_kwargs, 10, strat_quack=3, suppress_ticking=True)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    assert acc.clock == len(np_data)
    assert math.isclose(merged_total_balances[-1],
                        (500 + (sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n)
                         + (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum()))
                         * data['BTC', 'EUR'][-1] + 500 * data['LTC', 'EUR'][-1]))
    assert (signals == 'buy').sum() == buy_0_1_n + buy_2_3_n
    assert (signals == 'sell').sum() == sell_1_2_n + sell_3_4_n
    assert (signals == 'hold').sum() == hold_n


# noinspection DuplicatedCode
def test_run_multi_acc_wo_ticking():
    # unpatched
    accs = setup_accs()
    strat = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking, 10)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    np_data_ltc = np.array(data['LTC', 'EUR'])[10:]
    buy_0_1_n_ltc = ((np_data_ltc < 1) & (0 < np_data_ltc)).sum()
    buy_0_1_ltc = np_data_ltc[((np_data_ltc < 1) & (0 < np_data_ltc))]
    sell_1_2_n_ltc = ((np_data_ltc < 2) & (1 <= np_data_ltc)).sum()
    sell_1_2_ltc = np_data_ltc[(np_data_ltc < 2) & (1 <= np_data_ltc)]
    buy_2_3_n_ltc = ((np_data_ltc < 3) & (2 <= np_data_ltc)).sum()
    buy_2_3_ltc = np_data_ltc[(np_data_ltc < 3) & (2 <= np_data_ltc)]
    sell_3_4_n_ltc = ((np_data_ltc < 4) & (3 <= np_data_ltc)).sum()
    sell_3_4_ltc = np_data_ltc[(np_data_ltc < 4) & (3 <= np_data_ltc)]
    hold_n_ltc = len(np_data_ltc) - buy_0_1_n_ltc - buy_2_3_n_ltc - sell_1_2_n_ltc - sell_3_4_n_ltc

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    btc_eur = ((sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n) +
               (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())) * data['BTC', 'EUR'][-1])
    btc_eur_inv = ((buy_0_1.sum() + buy_2_3.sum() - sell_1_2_n - sell_3_4_n) +
                   (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum()))
                   * data['BTC', 'EUR'][-1])
    ltc_eur = ((sell_3_4_ltc.sum() + sell_1_2_ltc.sum() - buy_0_1_n_ltc - buy_2_3_n_ltc) +
               (500 + (-sell_3_4_n_ltc - sell_1_2_n_ltc +
                       (1 / buy_0_1_ltc).sum() + (1 / buy_2_3_ltc).sum())) * data['LTC', 'EUR'][-1])
    btc_acc = 500 + btc_eur + 500 * data['LTC', 'EUR'][-1]
    btc_inv_acc = 500 + btc_eur_inv + 500 * data['LTC', 'EUR'][-1]
    ltc_acc = 500 + ltc_eur + 500 * data['BTC', 'EUR'][-1]

    for acc in accs:
        assert acc.clock == len(np_data)
    assert (np.char.find(signals, 'buy') == 0).sum() == (buy_0_1_n + buy_2_3_n + buy_0_1_n_ltc + buy_2_3_n_ltc
                                                         + sell_1_2_n + sell_3_4_n)
    assert (np.char.find(signals, 'sell') == 0).sum() == (sell_1_2_n + sell_3_4_n + sell_1_2_n_ltc + sell_3_4_n_ltc
                                                          + buy_0_1_n + buy_2_3_n)
    assert (np.char.find(signals, 'hold') == 0).sum() == 2 * hold_n + hold_n_ltc
    assert (np.char.find(signals[:, 0, :], 'buy') == 0).sum() == buy_0_1_n + buy_2_3_n
    assert (np.char.find(signals[:, 1, :], 'sell') == 0).sum() == buy_0_1_n + buy_2_3_n
    assert (signals[:, 2, :] == 'sell').sum() == sell_1_2_n_ltc + sell_3_4_n_ltc
    assert math.isclose(merged_total_balances[-1], (btc_acc + btc_inv_acc + ltc_acc))
    assert math.isclose(strat.total_balances[-1][0], btc_acc)
    assert math.isclose(strat.total_balances[-1][1], btc_inv_acc)
    assert math.isclose(strat.total_balances[-1][2], ltc_acc)
    assert math.isclose(strat.positions['BTC'][-1][0],
                        (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())))
    assert math.isclose(strat.positions['BTC'][-1][1],
                        (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum())))
    assert math.isclose(strat.positions['BTC'][-1][2], 500)

    # without lookback
    accs = setup_accs()
    strat = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking, 0)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[0:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    np_data_ltc = np.array(data['LTC', 'EUR'])[0:]
    buy_0_1_n_ltc = ((np_data_ltc < 1) & (0 < np_data_ltc)).sum()
    buy_0_1_ltc = np_data_ltc[((np_data_ltc < 1) & (0 < np_data_ltc))]
    sell_1_2_n_ltc = ((np_data_ltc < 2) & (1 <= np_data_ltc)).sum()
    sell_1_2_ltc = np_data_ltc[(np_data_ltc < 2) & (1 <= np_data_ltc)]
    buy_2_3_n_ltc = ((np_data_ltc < 3) & (2 <= np_data_ltc)).sum()
    buy_2_3_ltc = np_data_ltc[(np_data_ltc < 3) & (2 <= np_data_ltc)]
    sell_3_4_n_ltc = ((np_data_ltc < 4) & (3 <= np_data_ltc)).sum()
    sell_3_4_ltc = np_data_ltc[(np_data_ltc < 4) & (3 <= np_data_ltc)]
    hold_n_ltc = len(np_data_ltc) - buy_0_1_n_ltc - buy_2_3_n_ltc - sell_1_2_n_ltc - sell_3_4_n_ltc

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    btc_eur = ((sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n) +
               (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())) * data['BTC', 'EUR'][-1])
    btc_eur_inv = ((buy_0_1.sum() + buy_2_3.sum() - sell_1_2_n - sell_3_4_n) +
                   (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum()))
                   * data['BTC', 'EUR'][-1])
    ltc_eur = ((sell_3_4_ltc.sum() + sell_1_2_ltc.sum() - buy_0_1_n_ltc - buy_2_3_n_ltc) +
               (500 + (-sell_3_4_n_ltc - sell_1_2_n_ltc +
                       (1 / buy_0_1_ltc).sum() + (1 / buy_2_3_ltc).sum())) * data['LTC', 'EUR'][-1])
    btc_acc = 500 + btc_eur + 500 * data['LTC', 'EUR'][-1]
    btc_inv_acc = 500 + btc_eur_inv + 500 * data['LTC', 'EUR'][-1]
    ltc_acc = 500 + ltc_eur + 500 * data['BTC', 'EUR'][-1]

    for acc in accs:
        assert acc.clock == len(np_data)
    assert (np.char.find(signals, 'buy') == 0).sum() == (buy_0_1_n + buy_2_3_n + buy_0_1_n_ltc + buy_2_3_n_ltc
                                                         + sell_1_2_n + sell_3_4_n)
    assert (np.char.find(signals, 'sell') == 0).sum() == (sell_1_2_n + sell_3_4_n + sell_1_2_n_ltc + sell_3_4_n_ltc
                                                          + buy_0_1_n + buy_2_3_n)
    assert (np.char.find(signals, 'hold') == 0).sum() == 2 * hold_n + hold_n_ltc
    assert (np.char.find(signals[:, 0, :], 'buy') == 0).sum() == buy_0_1_n + buy_2_3_n
    assert (np.char.find(signals[:, 1, :], 'sell') == 0).sum() == buy_0_1_n + buy_2_3_n
    assert (np.char.find(signals[:, 2, :], 'sell') == 0).sum() == sell_1_2_n_ltc + sell_3_4_n_ltc
    assert math.isclose(merged_total_balances[-1], (btc_acc + btc_inv_acc + ltc_acc))
    assert math.isclose(strat.total_balances[-1][0], btc_acc)
    assert math.isclose(strat.total_balances[-1][1], btc_inv_acc)
    assert math.isclose(strat.total_balances[-1][2], ltc_acc)
    assert math.isclose(strat.positions['BTC'][-1][0],
                        (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())))
    assert math.isclose(strat.positions['BTC'][-1][1],
                        (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum())))
    assert math.isclose(strat.positions['BTC'][-1][2], 500)

    # patched
    accs = setup_accs()
    for acc in accs:
        monkey_patch(acc)
    strat = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking, 10)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    np_data_ltc = np.array(data['LTC', 'EUR'])[10:]
    buy_0_1_n_ltc = ((np_data_ltc < 1) & (0 < np_data_ltc)).sum()
    buy_0_1_ltc = np_data_ltc[((np_data_ltc < 1) & (0 < np_data_ltc))]
    sell_1_2_n_ltc = ((np_data_ltc < 2) & (1 <= np_data_ltc)).sum()
    sell_1_2_ltc = np_data_ltc[(np_data_ltc < 2) & (1 <= np_data_ltc)]
    buy_2_3_n_ltc = ((np_data_ltc < 3) & (2 <= np_data_ltc)).sum()
    buy_2_3_ltc = np_data_ltc[(np_data_ltc < 3) & (2 <= np_data_ltc)]
    sell_3_4_n_ltc = ((np_data_ltc < 4) & (3 <= np_data_ltc)).sum()
    sell_3_4_ltc = np_data_ltc[(np_data_ltc < 4) & (3 <= np_data_ltc)]
    hold_n_ltc = len(np_data_ltc) - buy_0_1_n_ltc - buy_2_3_n_ltc - sell_1_2_n_ltc - sell_3_4_n_ltc

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    btc_eur = ((sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n) +
               (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())) * data['BTC', 'EUR'][-1])
    btc_eur_inv = ((buy_0_1.sum() + buy_2_3.sum() - sell_1_2_n - sell_3_4_n) +
                   (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum()))
                   * data['BTC', 'EUR'][-1])
    ltc_eur = ((sell_3_4_ltc.sum() + sell_1_2_ltc.sum() - buy_0_1_n_ltc - buy_2_3_n_ltc) +
               (500 + (-sell_3_4_n_ltc - sell_1_2_n_ltc +
                       (1 / buy_0_1_ltc).sum() + (1 / buy_2_3_ltc).sum())) * data['LTC', 'EUR'][-1])
    btc_acc = 500 + btc_eur + 500 * data['LTC', 'EUR'][-1]
    btc_inv_acc = 500 + btc_eur_inv + 500 * data['LTC', 'EUR'][-1]
    ltc_acc = 500 + ltc_eur + 500 * data['BTC', 'EUR'][-1]

    for acc in accs:
        assert acc.clock == len(np_data)
    assert (np.char.find(signals, 'buy') == 0).sum() == (buy_0_1_n + buy_2_3_n + buy_0_1_n_ltc + buy_2_3_n_ltc
                                                         + sell_1_2_n + sell_3_4_n)
    assert (np.char.find(signals, 'sell') == 0).sum() == (sell_1_2_n + sell_3_4_n + sell_1_2_n_ltc + sell_3_4_n_ltc
                                                          + buy_0_1_n + buy_2_3_n)
    assert (np.char.find(signals, 'hold') == 0).sum() == 2 * hold_n + hold_n_ltc
    assert (np.char.find(signals[:, 0, :], 'buy') == 0).sum() == buy_0_1_n + buy_2_3_n
    assert (np.char.find(signals[:, 1, :], 'sell') == 0).sum() == buy_0_1_n + buy_2_3_n
    assert (np.char.find(signals[:, 2, :], 'sell') == 0).sum() == sell_1_2_n_ltc + sell_3_4_n_ltc
    assert math.isclose(merged_total_balances[-1], (btc_acc + btc_inv_acc + ltc_acc))
    assert math.isclose(strat.total_balances[-1][0], btc_acc)
    assert math.isclose(strat.total_balances[-1][1], btc_inv_acc)
    assert math.isclose(strat.total_balances[-1][2], ltc_acc)
    assert math.isclose(strat.positions['BTC'][-1][0],
                        (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())))
    assert math.isclose(strat.positions['BTC'][-1][1],
                        (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum())))
    assert math.isclose(strat.positions['BTC'][-1][2], 500)


# noinspection DuplicatedCode
def test_run_multi_acc_wo_ticking_kwargs():
    # unpatched
    accs = setup_accs()
    strat = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking_kwargs, 10, strat_quack=3)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    np_data_ltc = np.array(data['LTC', 'EUR'])[10:]
    buy_0_1_n_ltc = ((np_data_ltc < 1) & (0 < np_data_ltc)).sum()
    buy_0_1_ltc = np_data_ltc[((np_data_ltc < 1) & (0 < np_data_ltc))]
    sell_1_2_n_ltc = ((np_data_ltc < 2) & (1 <= np_data_ltc)).sum()
    sell_1_2_ltc = np_data_ltc[(np_data_ltc < 2) & (1 <= np_data_ltc)]
    buy_2_3_n_ltc = ((np_data_ltc < 3) & (2 <= np_data_ltc)).sum()
    buy_2_3_ltc = np_data_ltc[(np_data_ltc < 3) & (2 <= np_data_ltc)]
    sell_3_4_n_ltc = ((np_data_ltc < 4) & (3 <= np_data_ltc)).sum()
    sell_3_4_ltc = np_data_ltc[(np_data_ltc < 4) & (3 <= np_data_ltc)]
    hold_n_ltc = len(np_data_ltc) - buy_0_1_n_ltc - buy_2_3_n_ltc - sell_1_2_n_ltc - sell_3_4_n_ltc

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    btc_eur = ((sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n) +
               (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())) * data['BTC', 'EUR'][-1])
    btc_eur_inv = ((buy_0_1.sum() + buy_2_3.sum() - sell_1_2_n - sell_3_4_n) +
                   (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum()))
                   * data['BTC', 'EUR'][-1])
    ltc_eur = ((sell_3_4_ltc.sum() + sell_1_2_ltc.sum() - buy_0_1_n_ltc - buy_2_3_n_ltc) +
               (500 + (-sell_3_4_n_ltc - sell_1_2_n_ltc +
                       (1 / buy_0_1_ltc).sum() + (1 / buy_2_3_ltc).sum())) * data['LTC', 'EUR'][-1])
    btc_acc = 500 + btc_eur + 500 * data['LTC', 'EUR'][-1]
    btc_inv_acc = 500 + btc_eur_inv + 500 * data['LTC', 'EUR'][-1]
    ltc_acc = 500 + ltc_eur + 500 * data['BTC', 'EUR'][-1]

    for acc in accs:
        assert acc.clock == len(np_data)
    assert (signals == 'buy').sum() == buy_0_1_n + buy_2_3_n + buy_0_1_n_ltc + buy_2_3_n_ltc + sell_1_2_n + sell_3_4_n
    assert (signals == 'sell').sum() == (sell_1_2_n + sell_3_4_n + sell_1_2_n_ltc + sell_3_4_n_ltc
                                         + buy_0_1_n + buy_2_3_n)
    assert (signals == 'hold').sum() == 2 * hold_n + hold_n_ltc
    assert (signals[:, 0, :] == 'buy').sum() == buy_0_1_n + buy_2_3_n
    assert (signals[:, 1, :] == 'sell').sum() == buy_0_1_n + buy_2_3_n
    assert (signals[:, 2, :] == 'sell').sum() == sell_1_2_n_ltc + sell_3_4_n_ltc
    assert math.isclose(merged_total_balances[-1], (btc_acc + btc_inv_acc + ltc_acc))
    assert math.isclose(strat.total_balances[-1][0], btc_acc)
    assert math.isclose(strat.total_balances[-1][1], btc_inv_acc)
    assert math.isclose(strat.total_balances[-1][2], ltc_acc)
    assert math.isclose(strat.positions['BTC'][-1][0],
                        (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())))
    assert math.isclose(strat.positions['BTC'][-1][1],
                        (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum())))
    assert math.isclose(strat.positions['BTC'][-1][2], 500)

    # patched
    accs = setup_accs()
    for acc in accs:
        monkey_patch(acc)
    strat = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking_kwargs, 10, strat_quack=3)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    np_data_ltc = np.array(data['LTC', 'EUR'])[10:]
    buy_0_1_n_ltc = ((np_data_ltc < 1) & (0 < np_data_ltc)).sum()
    buy_0_1_ltc = np_data_ltc[((np_data_ltc < 1) & (0 < np_data_ltc))]
    sell_1_2_n_ltc = ((np_data_ltc < 2) & (1 <= np_data_ltc)).sum()
    sell_1_2_ltc = np_data_ltc[(np_data_ltc < 2) & (1 <= np_data_ltc)]
    buy_2_3_n_ltc = ((np_data_ltc < 3) & (2 <= np_data_ltc)).sum()
    buy_2_3_ltc = np_data_ltc[(np_data_ltc < 3) & (2 <= np_data_ltc)]
    sell_3_4_n_ltc = ((np_data_ltc < 4) & (3 <= np_data_ltc)).sum()
    sell_3_4_ltc = np_data_ltc[(np_data_ltc < 4) & (3 <= np_data_ltc)]
    hold_n_ltc = len(np_data_ltc) - buy_0_1_n_ltc - buy_2_3_n_ltc - sell_1_2_n_ltc - sell_3_4_n_ltc

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    btc_eur = ((sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n) +
               (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())) * data['BTC', 'EUR'][-1])
    btc_eur_inv = ((buy_0_1.sum() + buy_2_3.sum() - sell_1_2_n - sell_3_4_n) +
                   (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum()))
                   * data['BTC', 'EUR'][-1])
    ltc_eur = ((sell_3_4_ltc.sum() + sell_1_2_ltc.sum() - buy_0_1_n_ltc - buy_2_3_n_ltc) +
               (500 + (-sell_3_4_n_ltc - sell_1_2_n_ltc +
                       (1 / buy_0_1_ltc).sum() + (1 / buy_2_3_ltc).sum())) * data['LTC', 'EUR'][-1])
    btc_acc = 500 + btc_eur + 500 * data['LTC', 'EUR'][-1]
    btc_inv_acc = 500 + btc_eur_inv + 500 * data['LTC', 'EUR'][-1]
    ltc_acc = 500 + ltc_eur + 500 * data['BTC', 'EUR'][-1]

    for acc in accs:
        assert acc.clock == len(np_data)
    assert (signals == 'buy').sum() == buy_0_1_n + buy_2_3_n + buy_0_1_n_ltc + buy_2_3_n_ltc + sell_1_2_n + sell_3_4_n
    assert (signals == 'sell').sum() == (sell_1_2_n + sell_3_4_n + sell_1_2_n_ltc + sell_3_4_n_ltc
                                         + buy_0_1_n + buy_2_3_n)
    assert (signals == 'hold').sum() == 2 * hold_n + hold_n_ltc
    assert (signals[:, 0, :] == 'buy').sum() == buy_0_1_n + buy_2_3_n
    assert (signals[:, 1, :] == 'sell').sum() == buy_0_1_n + buy_2_3_n
    assert (signals[:, 2, :] == 'sell').sum() == sell_1_2_n_ltc + sell_3_4_n_ltc
    assert math.isclose(merged_total_balances[-1], (btc_acc + btc_inv_acc + ltc_acc))
    assert math.isclose(strat.total_balances[-1][0], btc_acc)
    assert math.isclose(strat.total_balances[-1][1], btc_inv_acc)
    assert math.isclose(strat.total_balances[-1][2], ltc_acc)
    assert math.isclose(strat.positions['BTC'][-1][0],
                        (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())))
    assert math.isclose(strat.positions['BTC'][-1][1],
                        (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum())))
    assert math.isclose(strat.positions['BTC'][-1][2], 500)

    # with custom tick
    # patched with custom tick
    def some_tick(self, data_point, acc_tick):
        data_single_point = {k: data_point[k][-1] for k in data_point.keys()}
        for _acc in acc_tick:
            _acc.tick(data_single_point)

    accs = setup_accs()
    for acc in accs:
        monkey_patch(acc)
    strat = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking_kwargs, 10, tick_func=some_tick,
                       acc_tick=accs, strat_quack=3)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    np_data_ltc = np.array(data['LTC', 'EUR'])[10:]
    buy_0_1_n_ltc = ((np_data_ltc < 1) & (0 < np_data_ltc)).sum()
    buy_0_1_ltc = np_data_ltc[((np_data_ltc < 1) & (0 < np_data_ltc))]
    sell_1_2_n_ltc = ((np_data_ltc < 2) & (1 <= np_data_ltc)).sum()
    sell_1_2_ltc = np_data_ltc[(np_data_ltc < 2) & (1 <= np_data_ltc)]
    buy_2_3_n_ltc = ((np_data_ltc < 3) & (2 <= np_data_ltc)).sum()
    buy_2_3_ltc = np_data_ltc[(np_data_ltc < 3) & (2 <= np_data_ltc)]
    sell_3_4_n_ltc = ((np_data_ltc < 4) & (3 <= np_data_ltc)).sum()
    sell_3_4_ltc = np_data_ltc[(np_data_ltc < 4) & (3 <= np_data_ltc)]
    hold_n_ltc = len(np_data_ltc) - buy_0_1_n_ltc - buy_2_3_n_ltc - sell_1_2_n_ltc - sell_3_4_n_ltc

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    btc_eur = ((sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n) +
               (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())) * data['BTC', 'EUR'][-1])
    btc_eur_inv = ((buy_0_1.sum() + buy_2_3.sum() - sell_1_2_n - sell_3_4_n) +
                   (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum()))
                   * data['BTC', 'EUR'][-1])
    ltc_eur = ((sell_3_4_ltc.sum() + sell_1_2_ltc.sum() - buy_0_1_n_ltc - buy_2_3_n_ltc) +
               (500 + (-sell_3_4_n_ltc - sell_1_2_n_ltc +
                       (1 / buy_0_1_ltc).sum() + (1 / buy_2_3_ltc).sum())) * data['LTC', 'EUR'][-1])
    btc_acc = 500 + btc_eur + 500 * data['LTC', 'EUR'][-1]
    btc_inv_acc = 500 + btc_eur_inv + 500 * data['LTC', 'EUR'][-1]
    ltc_acc = 500 + ltc_eur + 500 * data['BTC', 'EUR'][-1]

    for acc in accs:
        assert acc.clock == len(np_data)
    assert (signals == 'buy').sum() == buy_0_1_n + buy_2_3_n + buy_0_1_n_ltc + buy_2_3_n_ltc + sell_1_2_n + sell_3_4_n
    assert (signals == 'sell').sum() == (sell_1_2_n + sell_3_4_n + sell_1_2_n_ltc + sell_3_4_n_ltc
                                         + buy_0_1_n + buy_2_3_n)
    assert (signals == 'hold').sum() == 2 * hold_n + hold_n_ltc
    assert (signals[:, 0, :] == 'buy').sum() == buy_0_1_n + buy_2_3_n
    assert (signals[:, 1, :] == 'sell').sum() == buy_0_1_n + buy_2_3_n
    assert (signals[:, 2, :] == 'sell').sum() == sell_1_2_n_ltc + sell_3_4_n_ltc
    assert math.isclose(merged_total_balances[-1], (btc_acc + btc_inv_acc + ltc_acc))
    assert math.isclose(strat.total_balances[-1][0], btc_acc)
    assert math.isclose(strat.total_balances[-1][1], btc_inv_acc)
    assert math.isclose(strat.total_balances[-1][2], ltc_acc)
    assert math.isclose(strat.positions['BTC'][-1][0],
                        (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())))
    assert math.isclose(strat.positions['BTC'][-1][1],
                        (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum())))
    assert math.isclose(strat.positions['BTC'][-1][2], 500)


def test_run_multi_acc_wo_ticking_kwargs_self():
    # with custom tick
    # patched with custom tick
    def some_tick(self, data_point):
        data_single_point = {k: data_point[k][-1] for k in data_point.keys()}
        for _acc in self.accounts:
            _acc.tick(data_single_point)

    accs = setup_accs()
    for acc in accs:
        monkey_patch(acc)
    strat = FXStrategy('genesis', accs, strategy_func_multi_wo_ticking_kwargs, 10, tick_func=some_tick,
                       acc_tick=accs, strat_quack=3)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    np_data_ltc = np.array(data['LTC', 'EUR'])[10:]
    buy_0_1_n_ltc = ((np_data_ltc < 1) & (0 < np_data_ltc)).sum()
    buy_0_1_ltc = np_data_ltc[((np_data_ltc < 1) & (0 < np_data_ltc))]
    sell_1_2_n_ltc = ((np_data_ltc < 2) & (1 <= np_data_ltc)).sum()
    sell_1_2_ltc = np_data_ltc[(np_data_ltc < 2) & (1 <= np_data_ltc)]
    buy_2_3_n_ltc = ((np_data_ltc < 3) & (2 <= np_data_ltc)).sum()
    buy_2_3_ltc = np_data_ltc[(np_data_ltc < 3) & (2 <= np_data_ltc)]
    sell_3_4_n_ltc = ((np_data_ltc < 4) & (3 <= np_data_ltc)).sum()
    sell_3_4_ltc = np_data_ltc[(np_data_ltc < 4) & (3 <= np_data_ltc)]
    hold_n_ltc = len(np_data_ltc) - buy_0_1_n_ltc - buy_2_3_n_ltc - sell_1_2_n_ltc - sell_3_4_n_ltc

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    btc_eur = ((sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n) +
               (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())) * data['BTC', 'EUR'][-1])
    btc_eur_inv = ((buy_0_1.sum() + buy_2_3.sum() - sell_1_2_n - sell_3_4_n) +
                   (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum()))
                   * data['BTC', 'EUR'][-1])
    ltc_eur = ((sell_3_4_ltc.sum() + sell_1_2_ltc.sum() - buy_0_1_n_ltc - buy_2_3_n_ltc) +
               (500 + (-sell_3_4_n_ltc - sell_1_2_n_ltc +
                       (1 / buy_0_1_ltc).sum() + (1 / buy_2_3_ltc).sum())) * data['LTC', 'EUR'][-1])
    btc_acc = 500 + btc_eur + 500 * data['LTC', 'EUR'][-1]
    btc_inv_acc = 500 + btc_eur_inv + 500 * data['LTC', 'EUR'][-1]
    ltc_acc = 500 + ltc_eur + 500 * data['BTC', 'EUR'][-1]

    for acc in accs:
        assert acc.clock == len(np_data)
    assert (signals == 'buy').sum() == buy_0_1_n + buy_2_3_n + buy_0_1_n_ltc + buy_2_3_n_ltc + sell_1_2_n + sell_3_4_n
    assert (signals == 'sell').sum() == (sell_1_2_n + sell_3_4_n + sell_1_2_n_ltc + sell_3_4_n_ltc
                                         + buy_0_1_n + buy_2_3_n)
    assert (signals == 'hold').sum() == 2 * hold_n + hold_n_ltc
    assert (signals[:, 0, :] == 'buy').sum() == buy_0_1_n + buy_2_3_n
    assert (signals[:, 1, :] == 'sell').sum() == buy_0_1_n + buy_2_3_n
    assert (signals[:, 2, :] == 'sell').sum() == sell_1_2_n_ltc + sell_3_4_n_ltc
    assert math.isclose(merged_total_balances[-1], (btc_acc + btc_inv_acc + ltc_acc))
    assert math.isclose(strat.total_balances[-1][0], btc_acc)
    assert math.isclose(strat.total_balances[-1][1], btc_inv_acc)
    assert math.isclose(strat.total_balances[-1][2], ltc_acc)
    assert math.isclose(strat.positions['BTC'][-1][0],
                        (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())))
    assert math.isclose(strat.positions['BTC'][-1][1],
                        (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum())))
    assert math.isclose(strat.positions['BTC'][-1][2], 500)


# noinspection DuplicatedCode
def test_run_multi_acc_w_ticking_kwargs():
    # unpatched
    accs = setup_accs()
    strat = FXStrategy('genesis', accs, strategy_func_multi_w_ticking_kwargs, 10, strat_quack=3)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    np_data_ltc = np.array(data['LTC', 'EUR'])[10:]
    buy_0_1_n_ltc = ((np_data_ltc < 1) & (0 < np_data_ltc)).sum()
    buy_0_1_ltc = np_data_ltc[((np_data_ltc < 1) & (0 < np_data_ltc))]
    sell_1_2_n_ltc = ((np_data_ltc < 2) & (1 <= np_data_ltc)).sum()
    sell_1_2_ltc = np_data_ltc[(np_data_ltc < 2) & (1 <= np_data_ltc)]
    buy_2_3_n_ltc = ((np_data_ltc < 3) & (2 <= np_data_ltc)).sum()
    buy_2_3_ltc = np_data_ltc[(np_data_ltc < 3) & (2 <= np_data_ltc)]
    sell_3_4_n_ltc = ((np_data_ltc < 4) & (3 <= np_data_ltc)).sum()
    sell_3_4_ltc = np_data_ltc[(np_data_ltc < 4) & (3 <= np_data_ltc)]
    hold_n_ltc = len(np_data_ltc) - buy_0_1_n_ltc - buy_2_3_n_ltc - sell_1_2_n_ltc - sell_3_4_n_ltc

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    btc_eur = ((sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n) +
               (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())) * data['BTC', 'EUR'][-1])
    btc_eur_inv = ((buy_0_1.sum() + buy_2_3.sum() - sell_1_2_n - sell_3_4_n) +
                   (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum()))
                   * data['BTC', 'EUR'][-1])
    ltc_eur = ((sell_3_4_ltc.sum() + sell_1_2_ltc.sum() - buy_0_1_n_ltc - buy_2_3_n_ltc) +
               (500 + (-sell_3_4_n_ltc - sell_1_2_n_ltc +
                       (1 / buy_0_1_ltc).sum() + (1 / buy_2_3_ltc).sum())) * data['LTC', 'EUR'][-1])
    btc_acc = 500 + btc_eur + 500 * data['LTC', 'EUR'][-1]
    btc_inv_acc = 500 + btc_eur_inv + 500 * data['LTC', 'EUR'][-1]
    ltc_acc = 500 + ltc_eur + 500 * data['BTC', 'EUR'][-1]

    for acc in accs:
        assert acc.clock == len(np_data)
    assert (signals == 'buy').sum() == buy_0_1_n + buy_2_3_n + buy_0_1_n_ltc + buy_2_3_n_ltc + sell_1_2_n + sell_3_4_n
    assert (signals == 'sell').sum() == (sell_1_2_n + sell_3_4_n + sell_1_2_n_ltc + sell_3_4_n_ltc
                                         + buy_0_1_n + buy_2_3_n)
    assert (signals == 'hold').sum() == 2 * hold_n + hold_n_ltc
    assert (signals[:, 0, :] == 'buy').sum() == buy_0_1_n + buy_2_3_n
    assert (signals[:, 1, :] == 'sell').sum() == buy_0_1_n + buy_2_3_n
    assert (signals[:, 2, :] == 'sell').sum() == sell_1_2_n_ltc + sell_3_4_n_ltc
    assert math.isclose(merged_total_balances[-1], (btc_acc + btc_inv_acc + ltc_acc))
    assert math.isclose(strat.total_balances[-1][0], btc_acc)
    assert math.isclose(strat.total_balances[-1][1], btc_inv_acc)
    assert math.isclose(strat.total_balances[-1][2], ltc_acc)
    assert math.isclose(strat.positions['BTC'][-1][0],
                        (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())))
    assert math.isclose(strat.positions['BTC'][-1][1],
                        (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum())))
    assert math.isclose(strat.positions['BTC'][-1][2], 500)

    # patched
    accs = setup_accs()
    for acc in accs:
        monkey_patch(acc)
    strat = FXStrategy('genesis', accs, strategy_func_multi_w_ticking_kwargs, 10, strat_quack=3, suppress_ticking=True)
    data = setup_data()

    strat.run(data, 'EUR')

    np_data = np.array(data['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    np_data_ltc = np.array(data['LTC', 'EUR'])[10:]
    buy_0_1_n_ltc = ((np_data_ltc < 1) & (0 < np_data_ltc)).sum()
    buy_0_1_ltc = np_data_ltc[((np_data_ltc < 1) & (0 < np_data_ltc))]
    sell_1_2_n_ltc = ((np_data_ltc < 2) & (1 <= np_data_ltc)).sum()
    sell_1_2_ltc = np_data_ltc[(np_data_ltc < 2) & (1 <= np_data_ltc)]
    buy_2_3_n_ltc = ((np_data_ltc < 3) & (2 <= np_data_ltc)).sum()
    buy_2_3_ltc = np_data_ltc[(np_data_ltc < 3) & (2 <= np_data_ltc)]
    sell_3_4_n_ltc = ((np_data_ltc < 4) & (3 <= np_data_ltc)).sum()
    sell_3_4_ltc = np_data_ltc[(np_data_ltc < 4) & (3 <= np_data_ltc)]
    hold_n_ltc = len(np_data_ltc) - buy_0_1_n_ltc - buy_2_3_n_ltc - sell_1_2_n_ltc - sell_3_4_n_ltc

    signals = np.array(strat.signals)
    merged_total_balances = np.array(strat.merged_total_balances)

    btc_eur = ((sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n) +
               (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())) * data['BTC', 'EUR'][-1])
    btc_eur_inv = ((buy_0_1.sum() + buy_2_3.sum() - sell_1_2_n - sell_3_4_n) +
                   (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum()))
                   * data['BTC', 'EUR'][-1])
    ltc_eur = ((sell_3_4_ltc.sum() + sell_1_2_ltc.sum() - buy_0_1_n_ltc - buy_2_3_n_ltc) +
               (500 + (-sell_3_4_n_ltc - sell_1_2_n_ltc +
                       (1 / buy_0_1_ltc).sum() + (1 / buy_2_3_ltc).sum())) * data['LTC', 'EUR'][-1])
    btc_acc = 500 + btc_eur + 500 * data['LTC', 'EUR'][-1]
    btc_inv_acc = 500 + btc_eur_inv + 500 * data['LTC', 'EUR'][-1]
    ltc_acc = 500 + ltc_eur + 500 * data['BTC', 'EUR'][-1]

    for acc in accs:
        assert acc.clock == len(np_data)
    assert (signals == 'buy').sum() == buy_0_1_n + buy_2_3_n + buy_0_1_n_ltc + buy_2_3_n_ltc + sell_1_2_n + sell_3_4_n
    assert (signals == 'sell').sum() == (sell_1_2_n + sell_3_4_n + sell_1_2_n_ltc + sell_3_4_n_ltc
                                         + buy_0_1_n + buy_2_3_n)
    assert (signals == 'hold').sum() == 2 * hold_n + hold_n_ltc
    assert (signals[:, 0, :] == 'buy').sum() == buy_0_1_n + buy_2_3_n
    assert (signals[:, 1, :] == 'sell').sum() == buy_0_1_n + buy_2_3_n
    assert (signals[:, 2, :] == 'sell').sum() == sell_1_2_n_ltc + sell_3_4_n_ltc
    assert math.isclose(merged_total_balances[-1], (btc_acc + btc_inv_acc + ltc_acc))
    assert math.isclose(strat.total_balances[-1][0], btc_acc)
    assert math.isclose(strat.total_balances[-1][1], btc_inv_acc)
    assert math.isclose(strat.total_balances[-1][2], ltc_acc)
    assert math.isclose(strat.positions['BTC'][-1][0],
                        (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())))
    assert math.isclose(strat.positions['BTC'][-1][1],
                        (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum())))
    assert math.isclose(strat.positions['BTC'][-1][2], 500)


def test_exceptions_add_signal():
    acc = setup_accs()[0]
    acc_alt = setup_accs()[0]
    strat = FXStrategy('genesis', acc, strategy_func_single_wo_ticking, 10)

    try:
        strat.add_signal([acc_alt], 'something')
        assert False
    except ValueError:
        pass


def test_exceptions_init():
    acc = setup_accs()[0]

    # noinspection PyShadowingNames,PyUnusedLocal
    def some_ticking(self, strat_quack, accs=3):
        return accs

    try:
        _ = FXStrategy('genesis', acc, strategy_func_single_wo_ticking_kwargs, 10, strat_quack=3, time_quack=3,
                       tick_func=some_ticking)
        assert False
    except OperatingError:
        pass

    acc = 3
    try:
        _ = FXStrategy('genesis', acc, strategy_func_single_wo_ticking_kwargs, 10)
        assert False
    except AccountError:
        pass

    accs = [3, 3, 3]
    try:
        _ = FXStrategy('genesis', accs, strategy_func_single_wo_ticking_kwargs, 10)
        assert False
    except AccountError:
        pass

    try:
        _ = FXStrategy(1, accs, strategy_func_single_wo_ticking_kwargs, 10)
        assert False
    except TypeError:
        pass


def test_exceptions_run():
    acc = setup_accs()[0]
    data = setup_data()

    # noinspection PyUnusedLocal
    def some_ticking(self, data_frame):
        return

    strat = FXStrategy('genesis', acc, strategy_func_single_wo_ticking, 10, tick_func=some_ticking)

    try:
        strat.run(data, 'EUR')
        assert False
    except OperatingError:
        pass

    strat = FXStrategy('genesis', acc, strategy_func_single_wo_ticking, 100)

    try:
        strat.run(data, 'EUR')
        assert False
    except ValueError:
        pass

    data = {k: data[k][i:-1] for i, k in enumerate(data.keys())}
    try:
        strat.run(data, 'EUR')
        assert False
    except IndexError:
        pass


# noinspection DuplicatedCode
def test_volume_data():
    acc = setup_accs()[0]
    acc._c_depot[b'BTC'] = 0
    acc._c_depot[b'LTC'] = 0
    acc._c_depot[b'EUR'] = 0
    strat = FXStrategy('genesis', acc, strategy_func_single_volume_wo_ticking, 10)
    prices = setup_data()
    volumes = setup_volume_data()

    strat.run(prices, 'BTC', volumes)

    btc_vol = np.array(volumes['BTC', 'EUR'])[10:]
    result = np.array(strat.merged_total_balances)

    assert np.allclose(btc_vol, result)


# noinspection DuplicatedCode
def test_return_types_run():
    acc = setup_accs()[0]
    acc._c_depot[b'BTC'] = 0
    acc._c_depot[b'LTC'] = 0
    acc._c_depot[b'EUR'] = 0
    strat = FXStrategy('genesis', acc, strategy_func_single_volume_wo_ticking, 10)
    prices = setup_data()
    volumes = setup_volume_data()

    results = strat.run(prices, 'BTC', volumes)

    assert type(results[0]) == str
    assert type(results[1]) == list
    assert type(results[2]) == dict
    assert type(results[3]) == dict
    assert type(results[4]) == list
    assert type(results[5]) == list
