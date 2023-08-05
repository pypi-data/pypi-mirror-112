# noinspection PyUnresolvedReferences,PyPackageRequirements
import pytest
import numpy as np
import math
import pathlib
import os
import pickle
import tempfile

from trapeza.strategy import FXStrategy
from trapeza.engine import FXEngine
from trapeza.account import FXAccount
from trapeza.exception import StrategyError
from trapeza import utils
from trapeza.tests.setup_test import setup_strategies, setup_data, setup_strategies_alt, \
    setup_volume_data, strategy_func_single_w_ticking_kwargs, strategy_func_single_volume_wo_ticking


# noinspection DuplicatedCode
def assert_run_multi(data, signals, positions, total_balances, merged_total_balances,
                     start_index, win_size, lookback):
    data = {k: data[k][start_index:start_index + lookback + win_size] for k in data.keys()}
    np_data = np.array(data['BTC', 'EUR'])[lookback:]

    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    np_data_ltc = np.array(data['LTC', 'EUR'])[lookback:]
    buy_0_1_n_ltc = ((np_data_ltc < 1) & (0 < np_data_ltc)).sum()
    buy_0_1_ltc = np_data_ltc[((np_data_ltc < 1) & (0 < np_data_ltc))]
    sell_1_2_n_ltc = ((np_data_ltc < 2) & (1 <= np_data_ltc)).sum()
    sell_1_2_ltc = np_data_ltc[(np_data_ltc < 2) & (1 <= np_data_ltc)]
    buy_2_3_n_ltc = ((np_data_ltc < 3) & (2 <= np_data_ltc)).sum()
    buy_2_3_ltc = np_data_ltc[(np_data_ltc < 3) & (2 <= np_data_ltc)]
    sell_3_4_n_ltc = ((np_data_ltc < 4) & (3 <= np_data_ltc)).sum()
    sell_3_4_ltc = np_data_ltc[(np_data_ltc < 4) & (3 <= np_data_ltc)]
    hold_n_ltc = len(np_data_ltc) - buy_0_1_n_ltc - buy_2_3_n_ltc - sell_1_2_n_ltc - sell_3_4_n_ltc

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

    assert (np.char.find(signals, 'buy') == 0).sum() == (buy_0_1_n + buy_2_3_n + buy_0_1_n_ltc + buy_2_3_n_ltc
                                                         + sell_1_2_n + sell_3_4_n)
    assert (np.char.find(signals, 'sell') == 0).sum() == (sell_1_2_n + sell_3_4_n + sell_1_2_n_ltc + sell_3_4_n_ltc
                                                          + buy_0_1_n + buy_2_3_n)
    assert (np.char.find(signals, 'hold') == 0).sum() == 2 * hold_n + hold_n_ltc
    assert (np.char.find(signals[:, 0, :], 'buy') == 0).sum() == buy_0_1_n + buy_2_3_n
    assert (np.char.find(signals[:, 1, :], 'sell') == 0).sum() == buy_0_1_n + buy_2_3_n
    assert (signals[:, 2, :] == 'sell').sum() == sell_1_2_n_ltc + sell_3_4_n_ltc
    assert math.isclose(merged_total_balances[-1], (btc_acc + btc_inv_acc + ltc_acc))
    assert math.isclose(total_balances[-1][0], btc_acc)
    assert math.isclose(total_balances[-1][1], btc_inv_acc)
    assert math.isclose(total_balances[-1][2], ltc_acc)
    assert math.isclose(positions['BTC'][-1][0],
                        (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())))
    assert math.isclose(positions['BTC'][-1][1],
                        (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum())))
    assert math.isclose(positions['BTC'][-1][2], 500)

    if len(merged_total_balances) > 0:
        return True
    else:
        return False


# noinspection DuplicatedCode
def assert_run_single(data, signals, merged_total_balances, start_index, win_size, lookback):
    data = {k: data[k][start_index:start_index + lookback + win_size] for k in data.keys()}
    np_data = np.array(data['BTC', 'EUR'])[lookback:]

    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    signals = np.array(signals)
    merged_total_balances = np.array(merged_total_balances)

    assert (np.char.find(signals, 'buy') == 0).sum() == buy_0_1_n + buy_2_3_n
    assert (np.char.find(signals, 'sell') == 0).sum() == sell_1_2_n + sell_3_4_n
    assert (np.char.find(signals, 'hold') == 0).sum() == hold_n
    assert math.isclose(merged_total_balances[-1],
                        (500 + (sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n)
                         + (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum()))
                         * data['BTC', 'EUR'][-1] + 500 * data['LTC', 'EUR'][-1]))

    if len(merged_total_balances) > 0:
        return True
    else:
        return False


def test_init():
    strats = setup_strategies()
    engine = FXEngine('genesis', strats, '__test_cache__', False)

    assert engine.name == 'genesis'
    assert len(engine.strategies) == len(strats)
    assert '__test_cache__' in engine._tmp_dir
    assert pathlib.Path(engine._tmp_dir).is_dir()
    assert engine.lookbacks[strats[0].name] == strats[0].lookback

    engine.close()
    assert not pathlib.Path(engine._tmp_dir).is_dir()


@pytest.mark.filterwarnings('ignore::UserWarning')
def test_build_partitioning_indices():
    strats = setup_strategies()
    engine = FXEngine('genesis', strats, '__test_cache__')

    dict_indices = engine._build_partitioning_indices(10, 5, 2, 3)
    assert len(dict_indices.keys()) == 2
    assert len(dict_indices[2]) == 4
    for i in dict_indices[2]:
        assert i < 4
    assert len(dict_indices[3]) == 3
    for i in dict_indices[3]:
        assert i < 3

    dict_indices = engine._build_partitioning_indices(10, 5, 2, 3, 4)
    assert len(dict_indices.keys()) == 2
    assert len(dict_indices[2]) == 2
    for i in dict_indices[2]:
        assert i < 4
    assert len(dict_indices[3]) == 2
    for i in dict_indices[3]:
        assert i < 3

    dict_indices = engine._build_partitioning_indices(10, 5, 2, 3, 'all_once')
    assert len(dict_indices) == 2
    assert len(dict_indices[2]) == 1
    for i in dict_indices[2]:
        assert i < 4
    assert len(dict_indices[3]) == 1
    for i in dict_indices[3]:
        assert i < 3

    dict_indices = engine._build_partitioning_indices(10, 5, 2, 4, 2)
    assert len(dict_indices) <= 2
    if 2 in dict_indices.keys():
        assert len(dict_indices[2]) == 1
        for i in dict_indices[2]:
            assert i < 4
    if 3 in dict_indices.keys():
        assert len(dict_indices[3]) == 1
        for i in dict_indices[3]:
            assert i < 3
    if 4 in dict_indices.keys():
        assert len(dict_indices[4]) == 1
        for i in dict_indices[4]:
            assert i < 2


def test_iter_data_partitions():
    strats = setup_strategies()
    engine = FXEngine('genesis', strats, '__test_cache__')
    data = {('LTC', 'EUR'): [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ('BTC', 'EUR'): [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]}

    lens_data = [10, 10, 10]
    lookbacks = [5, 7, 2]
    n_runs = [4, 3, 4]
    for k in range(len(lens_data)):
        len_data = lens_data[k]
        lookback = lookbacks[k]
        dict_indices = engine._build_partitioning_indices(len_data, lookback, 2, 3, 4)
        window_sizes = [2, 2, 3, 3]
        for i, sample in enumerate(engine._iter_partition_indices(dict_indices)):
            win_size = sample[0]
            start_index = sample[1]

            if start_index == 'runthrough':
                s_ind = 0
            else:
                s_ind = start_index

            sample_data = {k: data[k][s_ind: s_ind + win_size + lookback]
                           for k in data.keys()}

            assert len(sample_data.keys()) == 2
            assert len(sample_data['LTC', 'EUR']) == len(sample_data['BTC', 'EUR']) == win_size + lookback
            assert data['LTC', 'EUR'][start_index] in sample_data['LTC', 'EUR']
            assert data['BTC', 'EUR'][start_index] in sample_data['BTC', 'EUR']
            assert win_size == window_sizes[i]
            assert start_index < len_data - lookback - 1
            assert data['LTC', 'EUR'][start_index: start_index + win_size + lookback] == sample_data['LTC', 'EUR']
            assert data['BTC', 'EUR'][start_index: start_index + win_size + lookback] == sample_data['BTC', 'EUR']
        # noinspection PyUnboundLocalVariable
        assert i == n_runs[k] - 1


# noinspection DuplicatedCode
def test_run_strategy():
    strats = setup_strategies()
    engine = FXEngine('genesis', strats, '__test_cache__')
    prices = setup_data()
    volumes = setup_volume_data()

    engine.price_data = prices
    engine.volume_data = volumes
    engine.run_strategy(0, 'EUR', 100, 0)
    tmp_files = []
    for file in os.listdir(engine._tmp_dir):
        f_name = os.path.join(engine._tmp_dir, os.fsdecode(file))
        if 'lookbacks' in f_name:
            continue
        else:
            tmp_files.append(f_name)
    assert len(tmp_files) == 1
    assert '100' in tmp_files[0]
    assert '0' in tmp_files[0]
    with open(tmp_files[0], 'rb') as js_inp:
        # ret_val = json.load(js_inp)
        ret_val = pickle.load(js_inp)
    signals = np.array(ret_val['signals'])
    merged_total_balances = np.array(ret_val['merged_total_balances'])
    total_balances = ret_val['total_balances']
    positions = ret_val['positions']

    np_data = np.array(prices['BTC', 'EUR'])[10:]
    buy_0_1_n = ((np_data < 1) & (0 < np_data)).sum()
    buy_0_1 = np_data[((np_data < 1) & (0 < np_data))]
    sell_1_2_n = ((np_data < 2) & (1 <= np_data)).sum()
    sell_1_2 = np_data[(np_data < 2) & (1 <= np_data)]
    buy_2_3_n = ((np_data < 3) & (2 <= np_data)).sum()
    buy_2_3 = np_data[(np_data < 3) & (2 <= np_data)]
    sell_3_4_n = ((np_data < 4) & (3 <= np_data)).sum()
    sell_3_4 = np_data[(np_data < 4) & (3 <= np_data)]
    hold_n = len(np_data) - buy_0_1_n - buy_2_3_n - sell_1_2_n - sell_3_4_n

    np_data_ltc = np.array(prices['LTC', 'EUR'])[10:]
    buy_0_1_n_ltc = ((np_data_ltc < 1) & (0 < np_data_ltc)).sum()
    buy_0_1_ltc = np_data_ltc[((np_data_ltc < 1) & (0 < np_data_ltc))]
    sell_1_2_n_ltc = ((np_data_ltc < 2) & (1 <= np_data_ltc)).sum()
    sell_1_2_ltc = np_data_ltc[(np_data_ltc < 2) & (1 <= np_data_ltc)]
    buy_2_3_n_ltc = ((np_data_ltc < 3) & (2 <= np_data_ltc)).sum()
    buy_2_3_ltc = np_data_ltc[(np_data_ltc < 3) & (2 <= np_data_ltc)]
    sell_3_4_n_ltc = ((np_data_ltc < 4) & (3 <= np_data_ltc)).sum()
    sell_3_4_ltc = np_data_ltc[(np_data_ltc < 4) & (3 <= np_data_ltc)]
    hold_n_ltc = len(np_data_ltc) - buy_0_1_n_ltc - buy_2_3_n_ltc - sell_1_2_n_ltc - sell_3_4_n_ltc

    btc_eur = ((sell_3_4.sum() + sell_1_2.sum() - buy_0_1_n - buy_2_3_n) +
               (500 +
                (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())) * prices['BTC', 'EUR'][-1])
    btc_eur_inv = ((buy_0_1.sum() + buy_2_3.sum() - sell_1_2_n - sell_3_4_n) +
                   (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum()))
                   * prices['BTC', 'EUR'][-1])
    ltc_eur = ((sell_3_4_ltc.sum() + sell_1_2_ltc.sum() - buy_0_1_n_ltc - buy_2_3_n_ltc) +
               (500 + (-sell_3_4_n_ltc - sell_1_2_n_ltc +
                       (1 / buy_0_1_ltc).sum() + (1 / buy_2_3_ltc).sum())) * prices['LTC', 'EUR'][-1])
    btc_acc = 500 + btc_eur + 500 * prices['LTC', 'EUR'][-1]
    btc_inv_acc = 500 + btc_eur_inv + 500 * prices['LTC', 'EUR'][-1]
    ltc_acc = 500 + ltc_eur + 500 * prices['BTC', 'EUR'][-1]

    for acc in engine.strategies[0].accounts:
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
    assert math.isclose(engine.strategies[0].total_balances[-1][0], btc_acc)
    assert math.isclose(total_balances[-1][0], btc_acc)
    assert math.isclose(engine.strategies[0].total_balances[-1][1], btc_inv_acc)
    assert math.isclose(total_balances[-1][1], btc_inv_acc)
    assert math.isclose(engine.strategies[0].total_balances[-1][2], ltc_acc)
    assert math.isclose(total_balances[-1][2], ltc_acc)
    assert math.isclose(engine.strategies[0].positions['BTC'][-1][0],
                        (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())))
    assert math.isclose(positions['BTC'][-1][0],
                        (500 + (-sell_3_4_n - sell_1_2_n + (1 / buy_0_1).sum() + (1 / buy_2_3).sum())))
    assert math.isclose(engine.strategies[0].positions['BTC'][-1][1],
                        (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum())))
    assert math.isclose(positions['BTC'][-1][1],
                        (500 + (-buy_2_3_n - buy_0_1_n + (1 / sell_1_2).sum() + (1 / sell_3_4).sum())))
    assert math.isclose(engine.strategies[0].positions['BTC'][-1][2], 500)
    assert math.isclose(positions['BTC'][-1][2], 500)

    engine._reset_tmp_dir()
    tmp_files = []
    for file in os.listdir(engine._tmp_dir):
        f_name = os.path.join(engine._tmp_dir, os.fsdecode(file))
        if 'lookbacks' in f_name:
            continue
        else:
            tmp_files.append(f_name)
    assert len(tmp_files) == 0


# noinspection DuplicatedCode
def test_run():
    strats = setup_strategies()

    for strategy in strats:
        if '_' in strategy.name:
            raise Exception('Underscore "_" character in strategy name not allowed for testing. '
                            'Nevertheless, underscore "_" character is allowed in production code, but just not during'
                            'testing! So besides for testing purposes never mind this restriction')

    engine = FXEngine('genesis', strats, '__test_cache__')
    data = setup_data()
    len_data = len(data[list(data.keys())[0]])

    win_diff = 5

    engine.run(data, 'EUR', None, len_data - win_diff - 10, len_data - 10, 10, True)

    tmp_files = dict()
    run_balances = None
    for file in os.listdir(engine._tmp_dir):
        f_name = os.path.join(engine._tmp_dir, os.fsdecode(file))
        if 'lookbacks' in f_name:
            continue
        elif 'runs-total-balances-start-end_' in f_name:
            with open(f_name, 'rb') as js_inp:
                run_balances = pickle.load(js_inp)
        else:
            with open(f_name, 'rb') as js_inp:
                ret_val = pickle.load(js_inp)
                split_name = f_name.split('\\')[-1].split('_')
                tmp_files[split_name[0], split_name[1], split_name[2]] = ret_val

    is_checked_runthrough = False
    is_checked_single = False
    is_checked_multi = False

    for key in tmp_files.keys():
        strat_name = key[0]
        win_size = key[1]
        start_ind = key[2]

        signals = np.array(tmp_files[tuple(key)]['signals'])
        positions = tmp_files[key]['positions']
        merged_positions = tmp_files[key]['merged_positions']
        total_balances = np.array(tmp_files[key]['total_balances'])
        merged_total_balances = np.array(tmp_files[key]['merged_total_balances'])

        if 'runthrough' in key:
            start_ind = 0
            assert len(merged_total_balances) == len_data - engine.lookbacks[strat_name] == int(win_size)
            is_checked_runthrough = True
            start_ind_read = 'runthrough'
        else:
            start_ind = int(start_ind)
            start_ind_read = start_ind
            win_size = int(win_size)

        start_balance = run_balances[(strat_name, int(win_size), start_ind_read)][0]
        end_balance = run_balances[(strat_name, int(win_size), start_ind_read)][1]

        if strat_name == 'genesis':
            is_checked_multi = assert_run_multi(data, signals, positions, total_balances, merged_total_balances,
                                                int(start_ind), int(win_size), engine.lookbacks[strat_name])
        elif strat_name == 'benchmark':
            is_checked_single = assert_run_single(data, signals, merged_total_balances, int(start_ind), int(win_size),
                                                  engine.lookbacks[strat_name])

        assert start_balance == merged_total_balances[0]
        assert end_balance == merged_total_balances[-1]
        assert len(merged_total_balances) == int(win_size)
        assert utils.precision_add(*total_balances[-1]) == merged_total_balances[-1]
        half_len_total_balances = len(merged_total_balances) // 2
        assert (utils.precision_add(*total_balances[half_len_total_balances])
                == merged_total_balances[half_len_total_balances])

        assert (np.round(utils.precision_add(merged_positions['EUR'][half_len_total_balances],
                                             merged_positions['BTC'][half_len_total_balances] * data['BTC', 'EUR']
                                             [start_ind + engine.lookbacks[strat_name] + half_len_total_balances],
                                             merged_positions['LTC'][half_len_total_balances] * data['LTC', 'EUR']
                                             [start_ind + engine.lookbacks[strat_name] + half_len_total_balances]), 8)
                == np.round(merged_total_balances[half_len_total_balances], 8))

        total_positions = 0
        for pos in ['BTC', 'LTC']:
            t_p = (data[pos, 'EUR'][start_ind + engine.lookbacks[strat_name] + half_len_total_balances]
                   * np.array(positions[pos][half_len_total_balances]))
            t_p_s = utils.precision_add(*t_p)
            total_positions = utils.precision_add(t_p_s, total_positions)
        t_p_s_e = utils.precision_add(*positions['EUR'][half_len_total_balances])
        total_positions = utils.precision_add(t_p_s_e, total_positions)
        assert np.round(total_positions, 8) == np.round(merged_total_balances[half_len_total_balances], 8)

    assert is_checked_runthrough
    assert is_checked_single
    assert is_checked_multi


# noinspection DuplicatedCode
def test_load_result():
    strats = setup_strategies()

    for strategy in strats:
        if '_' in strategy.name:
            raise Exception('Underscore "_" character in strategy name not allowed for testing. '
                            'Nevertheless, underscore "_" character is allowed in production code, but just not during'
                            'testing! So besides for testing purposes never mind this restriction')

    engine = FXEngine('genesis', strats, '__test_cache__')
    data = setup_data()
    len_data = len(data[list(data.keys())[0]])

    win_diff = 5

    engine.run(data, 'EUR', None, len_data - win_diff - 10, len_data - 10, 10, True)

    results = engine.load_result(strats[0].name, len_data-strats[0].lookback, 'runthrough')
    assert assert_run_multi(data, np.array(results['signals']), results['positions'],
                            np.array(results['total_balances']), np.array(results['merged_total_balances']),
                            0, len_data-strats[0].lookback, strats[0].lookback,)

    results_default = engine.load_result(strats[0].name)
    assert np.array_equal(np.array(results['merged_total_balances']),
                          np.array(results_default['merged_total_balances']))


def test_strategy_reset_after_engine_run():
    strats = setup_strategies_alt()
    engine = FXEngine('genesis', strats, '__test_cache__')
    engine.strategies[0].accounts[0].clock = 100
    data = setup_data()

    engine.run(data, 'EUR', None, 10, 50, 50)

    assert engine.strategies[0].accounts[1].clock == 100
    assert engine.strategies[0].accounts[0].clock == 0
    assert engine.strategies[1].accounts[0].clock == 0

    assert engine.strategies[0].accounts[0].depot['BTC'] == 500
    assert engine.strategies[0].accounts[0].depot['LTC'] == 500
    assert engine.strategies[0].accounts[0].depot['EUR'] == 500
    assert engine.strategies[0].accounts[1].depot['BTC'] == 500
    assert engine.strategies[0].accounts[1].depot['LTC'] == 500
    assert engine.strategies[0].accounts[1].depot['EUR'] == 500
    assert engine.strategies[1].accounts[0].depot['BTC'] == 500
    assert engine.strategies[1].accounts[0].depot['LTC'] == 500
    assert engine.strategies[1].accounts[0].depot['EUR'] == 500

    assert len(list(engine.strategies[0].positions.keys())) == 0
    assert len(list(engine.strategies[0].merged_positions.keys())) == 0
    assert utils.is_empty_list(engine.strategies[0].signals)
    assert utils.is_empty_list(engine.strategies[0].total_balances)
    assert utils.is_empty_list(engine.strategies[0].merged_total_balances)
    assert len(list(engine.strategies[1].positions.keys())) == 0
    assert len(list(engine.strategies[1].merged_positions.keys())) == 0
    assert utils.is_empty_list(engine.strategies[1].signals)
    assert utils.is_empty_list(engine.strategies[1].total_balances)
    assert utils.is_empty_list(engine.strategies[1].merged_total_balances)


# noinspection DuplicatedCode
def test_analyze():
    strats = setup_strategies()
    engine = FXEngine('genesis', strats, '__test_cache__')
    data = setup_data()
    len_data = len(data[list(data.keys())[0]])

    win_diff = 5

    engine.run(data, 'EUR', None, len_data - win_diff - 10, len_data - 10, 10, True)
    engine.analyze()
    eval_results = engine.analysis_results

    assert type(eval_results) == dict
    assert set(list(eval_results.keys())) == set([strategy.name for strategy in engine.strategies])
    metrics_keys = list(eval_results[engine.strategies[0].name]
                        [list(eval_results[engine.strategies[0].name].keys())[0]].keys())
    assert set(metrics_keys) == {'total_rate_of_return', 'volatility', 'downside_risk', 'value_at_risk',
                                 'expected_rate_of_return', 'sharpe_ratio', 'sortino_ratio', 'max_drawdown'}
    sharpe_ratio_sample = (eval_results[engine.strategies[0].name]
                           [list(eval_results[engine.strategies[0].name].keys())[0]]['sharpe_ratio'])
    assert isinstance(sharpe_ratio_sample, int) or isinstance(sharpe_ratio_sample, float)


# noinspection DuplicatedCode
def test_save():
    strats = setup_strategies()
    engine = FXEngine('genesis', strats, '__test_cache__')
    data = setup_data()
    len_data = len(data[list(data.keys())[0]])

    win_diff = 5

    engine.run(data, 'EUR', None, len_data - win_diff - 10, len_data - 10, 10, True)
    engine.analyze()

    engine.save('test_save_dir')

    assert os.path.isdir('test_save_dir/genesis_temp')
    assert os.path.exists(os.path.join(os.getcwd(), 'test_save_dir', 'object.pkl'))


def test_load():
    strats = setup_strategies()
    engine = FXEngine('genesis', strats, '__test_cache__')

    engine.load('test_save_dir')

    assert engine.has_run is True
    assert engine.is_analyzed is True
    for fn in os.listdir(os.path.join(os.getcwd(), engine._tmp_dir)):
        fn_path = os.path.join(engine._tmp_dir, fn)
        with open(fn_path, 'rb') as fn_inp:
            results = pickle.load(fn_inp)
        assert 'merged_total_balances' in list(results.keys())
        break

    try:
        engine.is_analyzed = False
        engine.analyze()
        assert True
    except Exception as e:
        raise e

    assert os.path.isdir('test_save_dir/genesis_temp')
    assert os.path.exists(os.path.join(os.getcwd(), 'test_save_dir', 'object.pkl'))


# noinspection PyUnresolvedReferences
def test_clean_artifacts():
    strats = setup_strategies()

    if len([f.path for f in os.scandir(os.path.join(os.getcwd(), '__test_cache__')) if f.is_dir()]) == 0:
        os.makedirs(os.path.join(os.getcwd(), '__test_cache__', 'something'))

    assert len([f.path for f in os.scandir(os.path.join(os.getcwd(), '__test_cache__')) if f.is_dir()]) > 0

    engine = FXEngine('genesis', strats, '__test_cache__', clean_cache_artifacts=True)
    engine.close()
    engine.__del__()

    assert len([f.path for f in os.scandir(os.path.join(os.getcwd(), '__test_cache__')) if f.is_dir()]) == 0


def test_cache_dir_system():
    strats = setup_strategies()

    for strategy in strats:
        if '_' in strategy.name:
            raise Exception('Underscore "_" character in strategy name not allowed for testing. '
                            'Nevertheless, underscore "_" character is allowed in production code, but just not during'
                            'testing! So besides for testing purposes never mind this restriction')

    engine = FXEngine('genesis', strats)

    pth = engine._tmp_dir
    temp_dir_name = pth.split('\\')[-1]
    sys_pth = tempfile.gettempdir()

    assert os.path.join(sys_pth, 'trapeza', 'FXEngine', temp_dir_name) == pth
    assert os.path.isdir(sys_pth)
    assert os.path.isdir(pth)


# noinspection DuplicatedCode
def test_register():
    strats = setup_strategies()
    engine = FXEngine('genesis', strats, '__test_cache__')
    data = setup_data()
    len_data = len(data[list(data.keys())[0]])

    win_diff = 5

    engine.run(data, 'EUR', None, len_data - win_diff - 10, len_data - 10, 10, True)
    engine.analyze()

    assert engine.is_analyzed is True
    assert engine.has_run is True
    assert engine.strategies[0].name == 'genesis'
    assert engine.strategies[1].name == 'benchmark'
    assert engine.strategies[0]._init_accs_depots[0]['LTC'] == 500
    assert engine.lookbacks['genesis'] == 10

    acc = FXAccount('EUR')
    strat = FXStrategy('something', acc, strategy_func_single_w_ticking_kwargs, 5)
    engine.register_strategies(strat)

    assert engine.is_analyzed is False
    assert engine.has_run is False
    assert engine.strategies[0].name == 'something'
    assert engine.lookbacks['something'] == 5
    assert len(engine.strategies) == 1

    engine.register_strategies([strat, strats[1]])

    assert engine.is_analyzed is False
    assert engine.has_run is False
    assert engine.strategies[0].name == 'something'
    assert engine.lookbacks['something'] == 5
    assert engine.lookbacks['benchmark'] == 2
    assert len(engine.strategies) == 2


def test_close():
    strats = setup_strategies()
    engine = FXEngine('genesis', strats, '__test_cache__')

    engine.close()


# noinspection DuplicatedCode
def test_single_process_run():
    strats = setup_strategies()

    for strategy in strats:
        if '_' in strategy.name:
            raise Exception('Underscore "_" character in strategy name not allowed for testing. '
                            'Nevertheless, underscore "_" character is allowed in production code, but just not during'
                            'testing! So besides for testing purposes never mind this restriction')

    engine = FXEngine('genesis', strats, '__test_cache__', n_jobs=0)
    data = setup_data()
    len_data = len(data[list(data.keys())[0]])

    win_diff = 5

    engine.run(data, 'EUR', None, len_data - win_diff - 10, len_data - 10, 10, True)

    tmp_files = dict()
    run_balances = None
    for file in os.listdir(engine._tmp_dir):
        f_name = os.path.join(engine._tmp_dir, os.fsdecode(file))
        if 'lookbacks' in f_name:
            continue
        elif 'runs-total-balances-start-end_' in f_name:
            with open(f_name, 'rb') as js_inp:
                run_balances = pickle.load(js_inp)
        else:
            with open(f_name, 'rb') as js_inp:
                ret_val = pickle.load(js_inp)
                split_name = f_name.split('\\')[-1].split('_')
                tmp_files[split_name[0], split_name[1], split_name[2]] = ret_val

    is_checked_runthrough = False
    is_checked_single = False
    is_checked_multi = False

    for key in tmp_files.keys():
        strat_name = key[0]
        win_size = key[1]
        start_ind = key[2]

        signals = np.array(tmp_files[tuple(key)]['signals'])
        positions = tmp_files[key]['positions']
        merged_positions = tmp_files[key]['merged_positions']
        total_balances = np.array(tmp_files[key]['total_balances'])
        merged_total_balances = np.array(tmp_files[key]['merged_total_balances'])

        if 'runthrough' in key:
            start_ind = 0
            assert len(merged_total_balances) == len_data - engine.lookbacks[strat_name] == int(win_size)
            is_checked_runthrough = True
            start_ind_read = 'runthrough'
        else:
            start_ind = int(start_ind)
            start_ind_read = start_ind
            win_size = int(win_size)

        start_balance = run_balances[(strat_name, int(win_size), start_ind_read)][0]
        end_balance = run_balances[(strat_name, int(win_size), start_ind_read)][1]

        if strat_name == 'genesis':
            is_checked_multi = assert_run_multi(data, signals, positions, total_balances, merged_total_balances,
                                                int(start_ind), int(win_size), engine.lookbacks[strat_name])
        elif strat_name == 'benchmark':
            is_checked_single = assert_run_single(data, signals, merged_total_balances, int(start_ind), int(win_size),
                                                  engine.lookbacks[strat_name])

        assert start_balance == merged_total_balances[0]
        assert end_balance == merged_total_balances[-1]
        assert len(merged_total_balances) == int(win_size)
        assert utils.precision_add(*total_balances[-1]) == merged_total_balances[-1]
        half_len_total_balances = len(merged_total_balances) // 2
        assert (utils.precision_add(*total_balances[half_len_total_balances])
                == merged_total_balances[half_len_total_balances])

        assert (np.round(utils.precision_add(merged_positions['EUR'][half_len_total_balances],
                                             merged_positions['BTC'][half_len_total_balances] * data['BTC', 'EUR']
                                             [start_ind + engine.lookbacks[strat_name] + half_len_total_balances],
                                             merged_positions['LTC'][half_len_total_balances] * data['LTC', 'EUR']
                                             [start_ind + engine.lookbacks[strat_name] + half_len_total_balances]), 8)
                == np.round(merged_total_balances[half_len_total_balances], 8))

        total_positions = 0
        for pos in ['BTC', 'LTC']:
            t_p = (data[pos, 'EUR'][start_ind + engine.lookbacks[strat_name] + half_len_total_balances]
                   * np.array(positions[pos][half_len_total_balances]))
            t_p_s = utils.precision_add(*t_p)
            total_positions = utils.precision_add(t_p_s, total_positions)
        t_p_s_e = utils.precision_add(*positions['EUR'][half_len_total_balances])
        total_positions = utils.precision_add(t_p_s_e, total_positions)
        assert np.round(total_positions, 8) == np.round(merged_total_balances[half_len_total_balances], 8)

    assert is_checked_runthrough
    assert is_checked_single
    assert is_checked_multi


# noinspection DuplicatedCode
def test_distinct_number_of_cores_run():
    strats = setup_strategies()

    for strategy in strats:
        if '_' in strategy.name:
            raise Exception('Underscore "_" character in strategy name not allowed for testing. '
                            'Nevertheless, underscore "_" character is allowed in production code, but just not during'
                            'testing! So besides for testing purposes never mind this restriction')

    engine = FXEngine('genesis', strats, '__test_cache__', n_jobs=5)
    data = setup_data()
    len_data = len(data[list(data.keys())[0]])

    win_diff = 5

    engine.run(data, 'EUR', None, len_data - win_diff - 10, len_data - 10, 10, True)

    tmp_files = dict()
    run_balances = None
    for file in os.listdir(engine._tmp_dir):
        f_name = os.path.join(engine._tmp_dir, os.fsdecode(file))
        if 'lookbacks' in f_name:
            continue
        elif 'runs-total-balances-start-end_' in f_name:
            with open(f_name, 'rb') as js_inp:
                run_balances = pickle.load(js_inp)
        else:
            with open(f_name, 'rb') as js_inp:
                ret_val = pickle.load(js_inp)
                split_name = f_name.split('\\')[-1].split('_')
                tmp_files[split_name[0], split_name[1], split_name[2]] = ret_val

    is_checked_runthrough = False
    is_checked_single = False
    is_checked_multi = False

    for key in tmp_files.keys():
        strat_name = key[0]
        win_size = key[1]
        start_ind = key[2]

        signals = np.array(tmp_files[tuple(key)]['signals'])
        positions = tmp_files[key]['positions']
        merged_positions = tmp_files[key]['merged_positions']
        total_balances = np.array(tmp_files[key]['total_balances'])
        merged_total_balances = np.array(tmp_files[key]['merged_total_balances'])

        if 'runthrough' in key:
            start_ind = 0
            assert len(merged_total_balances) == len_data - engine.lookbacks[strat_name] == int(win_size)
            is_checked_runthrough = True
            start_ind_read = 'runthrough'
        else:
            start_ind = int(start_ind)
            start_ind_read = start_ind
            win_size = int(win_size)

        start_balance = run_balances[(strat_name, int(win_size), start_ind_read)][0]
        end_balance = run_balances[(strat_name, int(win_size), start_ind_read)][1]

        if strat_name == 'genesis':
            is_checked_multi = assert_run_multi(data, signals, positions, total_balances, merged_total_balances,
                                                int(start_ind), int(win_size), engine.lookbacks[strat_name])
        elif strat_name == 'benchmark':
            is_checked_single = assert_run_single(data, signals, merged_total_balances, int(start_ind), int(win_size),
                                                  engine.lookbacks[strat_name])

        assert start_balance == merged_total_balances[0]
        assert end_balance == merged_total_balances[-1]
        assert len(merged_total_balances) == int(win_size)
        assert utils.precision_add(*total_balances[-1]) == merged_total_balances[-1]
        half_len_total_balances = len(merged_total_balances) // 2
        assert (utils.precision_add(*total_balances[half_len_total_balances])
                == merged_total_balances[half_len_total_balances])

        assert (np.round(utils.precision_add(merged_positions['EUR'][half_len_total_balances],
                                             merged_positions['BTC'][half_len_total_balances] * data['BTC', 'EUR']
                                             [start_ind + engine.lookbacks[strat_name] + half_len_total_balances],
                                             merged_positions['LTC'][half_len_total_balances] * data['LTC', 'EUR']
                                             [start_ind + engine.lookbacks[strat_name] + half_len_total_balances]), 8)
                == np.round(merged_total_balances[half_len_total_balances], 8))

        total_positions = 0
        for pos in ['BTC', 'LTC']:
            t_p = (data[pos, 'EUR'][start_ind + engine.lookbacks[strat_name] + half_len_total_balances]
                   * np.array(positions[pos][half_len_total_balances]))
            t_p_s = utils.precision_add(*t_p)
            total_positions = utils.precision_add(t_p_s, total_positions)
        t_p_s_e = utils.precision_add(*positions['EUR'][half_len_total_balances])
        total_positions = utils.precision_add(t_p_s_e, total_positions)
        assert np.round(total_positions, 8) == np.round(merged_total_balances[half_len_total_balances], 8)

    assert is_checked_runthrough
    assert is_checked_single
    assert is_checked_multi


# noinspection DuplicatedCode
@pytest.mark.filterwarnings('ignore::UserWarning')
def test_partial_max_total_runs():
    strats = setup_strategies()[0]

    for strategy in [strats]:
        if '_' in strategy.name:
            raise Exception('Underscore "_" character in strategy name not allowed for testing. '
                            'Nevertheless, underscore "_" character is allowed in production code, but just not during'
                            'testing! So besides for testing purposes never mind this restriction')

    engine = FXEngine('genesis', strats, '__test_cache__')
    data = setup_data()
    len_data = len(data[list(data.keys())[0]])

    engine.run(data, 'EUR', None, None, 50, 30, True)

    tmp_files = dict()
    run_balances = None
    for file in os.listdir(engine._tmp_dir):
        f_name = os.path.join(engine._tmp_dir, os.fsdecode(file))
        if 'lookbacks' in f_name:
            continue
        elif 'runs-total-balances-start-end_' in f_name:
            with open(f_name, 'rb') as js_inp:
                run_balances = pickle.load(js_inp)
        else:
            with open(f_name, 'rb') as js_inp:
                ret_val = pickle.load(js_inp)
                split_name = f_name.split('\\')[-1].split('_')
                tmp_files[split_name[0], split_name[1], split_name[2]] = ret_val

    is_checked_runthrough = False
    is_checked_multi = False

    assert len(tmp_files) == 30

    for key in tmp_files.keys():
        strat_name = key[0]
        win_size = key[1]
        start_ind = key[2]

        signals = np.array(tmp_files[tuple(key)]['signals'])
        positions = tmp_files[key]['positions']
        merged_positions = tmp_files[key]['merged_positions']
        total_balances = np.array(tmp_files[key]['total_balances'])
        merged_total_balances = np.array(tmp_files[key]['merged_total_balances'])

        if 'runthrough' in key:
            start_ind = 0
            assert len(merged_total_balances) == len_data - engine.lookbacks[strat_name] == int(win_size)
            is_checked_runthrough = True
            start_ind_read = 'runthrough'
        else:
            start_ind = int(start_ind)
            start_ind_read = start_ind
            win_size = int(win_size)

        start_balance = run_balances[(strat_name, int(win_size), start_ind_read)][0]
        end_balance = run_balances[(strat_name, int(win_size), start_ind_read)][1]

        if strat_name == 'genesis':
            is_checked_multi = assert_run_multi(data, signals, positions, total_balances, merged_total_balances,
                                                int(start_ind), int(win_size), engine.lookbacks[strat_name])

        assert start_balance == merged_total_balances[0]
        assert end_balance == merged_total_balances[-1]
        assert len(merged_total_balances) == int(win_size)
        assert utils.precision_add(*total_balances[-1]) == merged_total_balances[-1]
        half_len_total_balances = len(merged_total_balances) // 2
        assert (utils.precision_add(*total_balances[half_len_total_balances])
                == merged_total_balances[half_len_total_balances])

        assert (np.round(utils.precision_add(merged_positions['EUR'][half_len_total_balances],
                                             merged_positions['BTC'][half_len_total_balances] * data['BTC', 'EUR']
                                             [start_ind + engine.lookbacks[strat_name] + half_len_total_balances],
                                             merged_positions['LTC'][half_len_total_balances] * data['LTC', 'EUR']
                                             [start_ind + engine.lookbacks[strat_name] + half_len_total_balances]), 6)
                == np.round(merged_total_balances[half_len_total_balances], 6))

        total_positions = 0
        for pos in ['BTC', 'LTC']:
            t_p = (data[pos, 'EUR'][start_ind + engine.lookbacks[strat_name] + half_len_total_balances]
                   * np.array(positions[pos][half_len_total_balances]))
            t_p_s = utils.precision_add(*t_p)
            total_positions = utils.precision_add(t_p_s, total_positions)
        t_p_s_e = utils.precision_add(*positions['EUR'][half_len_total_balances])
        total_positions = utils.precision_add(t_p_s_e, total_positions)
        assert np.round(total_positions, 7) == np.round(merged_total_balances[half_len_total_balances], 7)

    assert is_checked_runthrough
    assert is_checked_multi


def test_run_once():
    strats = setup_strategies()[0]

    for strategy in [strats]:
        if '_' in strategy.name:
            raise Exception('Underscore "_" character in strategy name not allowed for testing. '
                            'Nevertheless, underscore "_" character is allowed in production code, but just not during'
                            'testing! So besides for testing purposes never mind this restriction')

    engine = FXEngine('genesis', strats, '__test_cache__')
    data = setup_data()

    engine.run(data, 'EUR', None, None, 50, 'all_once', False)

    tmp_files = dict()
    for file in os.listdir(engine._tmp_dir):
        f_name = os.path.join(engine._tmp_dir, os.fsdecode(file))
        if 'lookbacks' in f_name:
            continue
        elif 'runs-total-balances-start-end_' in f_name:
            continue
        else:
            with open(f_name, 'rb') as js_inp:
                ret_val = pickle.load(js_inp)
                split_name = f_name.split('\\')[-1].split('_')
                tmp_files[split_name[0], split_name[1], split_name[2]] = ret_val

    assert len(tmp_files) == 50


def test_multiple_engines():
    acc_0 = FXAccount('EUR')
    acc_1 = FXAccount('USD')

    for cur in ['EUR', 'LTC', 'BTC']:
        acc_0._c_depot[cur.encode()] = 500

    strat_0 = FXStrategy('0', acc_0, strategy_func_single_w_ticking_kwargs, 10)
    strat_1 = FXStrategy('1', acc_1, strategy_func_single_volume_wo_ticking, 5)

    for strategy in [strat_0, strat_1]:
        if '_' in strategy.name:
            raise Exception('Underscore "_" character in strategy name not allowed for testing. '
                            'Nevertheless, underscore "_" character is allowed in production code, but just not during'
                            'testing! So besides for testing purposes never mind this restriction')

    engine_price = FXEngine('price', strat_0, '__test_cache__')
    engine_vol = FXEngine('vol', strat_1, '__test_cache__')

    prices = setup_data()
    vols = setup_volume_data()

    engine_price.run(prices, 'EUR', volume_data=vols, min_run_length=1, max_run_length=50, max_total_runs=50,
                     run_through=False)
    engine_vol.run(prices, 'BTC', volume_data=vols, min_run_length=1, max_run_length=50, max_total_runs=50,
                   run_through=False)

    for file in os.listdir(engine_price._tmp_dir):
        f_name = os.path.join(engine_price._tmp_dir, os.fsdecode(file))
        if 'lookbacks' in f_name:
            continue
        elif 'runs-total-balances-start-end_' in f_name:
            continue
        elif f_name.split('\\')[-1].split('_')[0] == '1':
            continue
        else:
            with open(f_name, 'rb') as js_inp:
                ret_val = pickle.load(js_inp)
                merged_total_balances = ret_val['merged_total_balances']
                signals = ret_val['signals']
                split_name = f_name.split('\\')[-1].split('_')
                win_size, start_ind = int(split_name[1]), int(split_name[2])
                assert assert_run_single(prices, signals, merged_total_balances, start_ind, win_size, strat_0.lookback)

    for file in os.listdir(engine_price._tmp_dir):
        f_name = os.path.join(engine_price._tmp_dir, os.fsdecode(file))
        if 'lookbacks' in f_name:
            continue
        elif 'runs-total-balances-start-end_' in f_name:
            continue
        elif f_name.split('\\')[-1].split('_')[0] == '0':
            continue
        else:
            with open(f_name, 'rb') as js_inp:
                ret_val = pickle.load(js_inp)
                merged_total_balances = ret_val['merged_total_balances']
                split_name = f_name.split('\\')[-1].split('_')
                win_size, start_ind = int(split_name[1]), int(split_name[2])
                btc_vol = np.array(vols['BTC', 'EUR'])[strat_1.lookback + start_ind:
                                                       strat_1.lookback + start_ind + win_size]
                assert np.allclose(btc_vol, merged_total_balances)
                assert len(btc_vol) == len(merged_total_balances)


# noinspection DuplicatedCode
def test_volume_data():
    acc = FXAccount('EUR')
    strat = FXStrategy('genesis', acc, strategy_func_single_volume_wo_ticking, 10)

    for strategy in [strat]:
        if '_' in strategy.name:
            raise Exception('Underscore "_" character in strategy name not allowed for testing. '
                            'Nevertheless, underscore "_" character is allowed in production code, but just not during'
                            'testing! So besides for testing purposes never mind this restriction')

    engine = FXEngine('genesis', strat, '__test_cache__')

    vol_data = setup_volume_data()
    price_data = setup_data()
    len_data = len(vol_data[list(vol_data.keys())[0]])
    win_diff = 5

    engine.run(price_data, 'BTC', vol_data, len_data - win_diff - 10, len_data - 10, 10, True)

    tmp_files = dict()
    run_balances = None
    for file in os.listdir(engine._tmp_dir):
        f_name = os.path.join(engine._tmp_dir, os.fsdecode(file))
        if 'lookbacks' in f_name:
            continue
        elif 'runs-total-balances-start-end_' in f_name:
            with open(f_name, 'rb') as js_inp:
                run_balances = pickle.load(js_inp)
        else:
            with open(f_name, 'rb') as js_inp:
                ret_val = pickle.load(js_inp)
                split_name = f_name.split('\\')[-1].split('_')
                tmp_files[split_name[0], split_name[1], split_name[2]] = ret_val

    for key in tmp_files.keys():
        strat_name = key[0]
        win_size = key[1]
        start_ind = key[2]

        merged_total_balances = np.array(tmp_files[key]['merged_total_balances'])

        if 'runthrough' in key:
            start_ind = 0
            assert len(merged_total_balances) == len_data - engine.lookbacks[strat_name] == int(win_size)
            start_ind_read = 'runthrough'
        else:
            start_ind = int(start_ind)
            start_ind_read = start_ind
        win_size = int(win_size)

        start_balance = run_balances[(strat_name, int(win_size), start_ind_read)][0]
        end_balance = run_balances[(strat_name, int(win_size), start_ind_read)][1]

        btc_vol = np.array(vol_data['BTC', 'EUR'])[strat.lookback+start_ind:strat.lookback+start_ind+win_size]

        assert np.allclose(btc_vol, merged_total_balances)
        assert start_balance == merged_total_balances[0]
        assert end_balance == merged_total_balances[-1]
        assert len(btc_vol) == len(merged_total_balances)


def test_exception_unique_names():
    acc = FXAccount('EUR')
    strat_1 = FXStrategy('something', acc, strategy_func_single_w_ticking_kwargs, 5)
    strat_2 = FXStrategy('something', acc, strategy_func_single_w_ticking_kwargs, 10)

    try:
        _ = FXEngine('genesis', [strat_1, strat_2], '__test_cache__')
        assert False
    except StrategyError:
        assert True


def test_exception_not_account():
    try:
        _ = FXEngine('genesis', 'something', '__test_cache__')
        assert False
    except StrategyError:
        assert True

    try:
        _ = FXEngine('genesis', 1, '__test_cache__')
        assert False
    except StrategyError:
        assert True


def test_exception_window_specification():
    acc = FXAccount('EUR')
    strat_1 = FXStrategy('something', acc, strategy_func_single_w_ticking_kwargs, 5)
    engine = FXEngine('genesis', strat_1, '__test_cache__')
    prices = setup_data()

    try:
        _ = engine.run(prices, 'EUR', min_run_length=-1)
        assert False
    except ValueError:
        assert True

    try:
        _ = engine.run(prices, 'EUR', min_run_length=20, max_run_length=19)
        assert False
    except ValueError:
        assert True

    try:
        strat_1.lookback = len(prices['BTC', 'EUR'])
        _ = engine.run(prices, 'EUR')
        assert False
    except ValueError:
        assert True

    try:
        _ = engine.run(prices, 'EUR', max_total_runs='something')
        assert False
    except TypeError:
        assert True


def test_exception_none_prices():
    acc = FXAccount('EUR')
    strat_1 = FXStrategy('something', acc, strategy_func_single_w_ticking_kwargs, 5)
    engine = FXEngine('genesis', strat_1, '__test_cache__')

    try:
        _ = engine.run(None, 'EUR', min_run_length=1)
        assert False
    except TypeError:
        assert True


def test_exception_different_length_data():
    acc = FXAccount('EUR')
    strat_1 = FXStrategy('something', acc, strategy_func_single_w_ticking_kwargs, 5)
    engine = FXEngine('genesis', strat_1, '__test_cache__')

    data = setup_data()
    data['BTC', 'EUR'] = data['BTC', 'EUR'][:-2]

    try:
        _ = engine.run(data, 'EUR')
        assert False
    except IndexError:
        assert True


def test_exception_max_total_runs():
    acc = FXAccount('EUR')
    strat_1 = FXStrategy('something', acc, strategy_func_single_w_ticking_kwargs, 5)
    engine = FXEngine('genesis', strat_1, '__test_cache__')

    data = setup_data()

    try:
        _ = engine.run(data, 'EUR', max_total_runs='something')
        assert False
    except TypeError:
        assert True


def test_exception_save_load():
    acc = FXAccount('EUR')
    strat_1 = FXStrategy('something', acc, strategy_func_single_w_ticking_kwargs, 5)
    engine = FXEngine('genesis', strat_1, '__test_cache__')

    try:
        engine.save('some_path.file_extension')
        assert False
    except TypeError:
        assert True

    try:
        engine.load('some_path.file_extension')
        assert False
    except TypeError:
        assert True


def test_exception_analyze():
    acc = FXAccount('EUR')

    for cur in ['EUR', 'LTC', 'BTC']:
        acc._c_depot[cur.encode()] = 500

    strat_1 = FXStrategy('something', acc, strategy_func_single_w_ticking_kwargs, 5)
    engine = FXEngine('genesis', strat_1, '__test_cache__')

    data = setup_data()

    engine.run(data, 'EUR')

    try:
        engine.analyze('something')
        assert False
    except TypeError:
        assert True


def test_exception_mutual_substring_naming():
    strats = setup_strategies()

    for strategy in strats:
        if '_' in strategy.name:
            raise Exception('Underscore "_" character in strategy name not allowed for testing. '
                            'Nevertheless, underscore "_" character is allowed in production code, but just not during'
                            'testing! So besides for testing purposes never mind this restriction')

    strats[0].name = strats[1].name

    try:
        _ = FXEngine('genesis', strats, '__test_cache__')
        assert False
    except StrategyError:
        assert True


def test_run_with_fee_func():
    # noinspection PyUnusedLocal
    def fee_sell(amount, price, base, quote, execution_time):
        return 1, base, 1

    # noinspection PyUnusedLocal
    def fee_buy(amount, price, base, quote, execution_time):
        return 1, base, 1

    acc_0 = FXAccount('EUR', fee_buy=fee_buy, fee_sell=fee_sell)

    for cur in ['EUR', 'LTC', 'BTC']:
        acc_0._c_depot[cur.encode()] = 500

    strat_0 = FXStrategy('0', acc_0, strategy_func_single_w_ticking_kwargs, 10)

    engine = FXEngine('genesis', strat_0, '__test_cache__')
    data = setup_data()

    engine.run(data, 'EUR', None, None, 50, 'all_once', False)
