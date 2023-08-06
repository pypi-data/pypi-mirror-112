# noinspection PyUnresolvedReferences,PyPackageRequirements
import pytest
import numpy as np
import math
from scipy import stats

from trapeza import metric

data = np.array([1, 2, 3, 4, 5, 6, 3, 1, 3, 4, 5, 8, 9, 6, 5, 4, 3])
nd_data = np.array([[1, 2, 3, 4, 5, 6, 3, 2, 3, 4, 5, 8, 9, 6, 5, 4],
                    [4, 5, 6, 9, 8, 5, 4, 3, 2, 3, 6, 5, 4, 3, 2, 1]])


def test_max_draw_down():
    depth, peak_index, through_index = metric.max_drawdown(data, mode='absolute')
    assert depth == 6
    assert peak_index == 12
    assert through_index == 16

    depth, peak_index, through_index = metric.max_drawdown(data, mode='relative')
    assert depth == 5
    assert peak_index == 5
    assert through_index == 7


def test_high_water_marks():
    water_marks_values, water_marks_indices = metric.high_water_marks(data)

    assert np.array_equal(np.array([1, 2, 3, 4, 5, 6, 8, 9]), water_marks_values)
    assert np.array_equal(np.array([0, 1, 2, 3, 4, 5, 11, 12]), water_marks_indices)


def test_volatility():
    volatility = metric.volatility(data, reference='log_return', prob_model='norm')
    assert volatility == np.std(np.diff(np.log(data)))

    volatility = metric.volatility(data, reference='pct_return', prob_model='norm')
    assert volatility == np.std((data[1:] - data[:-1]) / data[:-1])

    volatility = metric.volatility(data, reference='abs_return', prob_model='norm')
    assert volatility == np.std(data[1:] - data[:-1])

    volatility = metric.volatility(data, reference='abs_value', prob_model='norm')
    assert volatility == np.std(data)

    volatility = metric.volatility(data, reference='indexed_value', prob_model='norm')
    assert (isinstance(volatility, float)) or (isinstance(volatility, int))

    volatility = metric.volatility(data, reference='log_return', prob_model='68_percentile')
    assert (isinstance(volatility, float)) or (isinstance(volatility, int))

    volatility = metric.volatility(data, reference='log_return', prob_model='log_norm')
    assert (isinstance(volatility, float)) or (isinstance(volatility, int))

    volatility = metric.volatility(data, reference='indexed_value', prob_model='norm', annualization_factor=252)
    assert (isinstance(volatility, float)) or (isinstance(volatility, int))

    volatility = metric.volatility(data, reference='indexed_value', prob_model='pareto', annualization_factor=252)
    assert (isinstance(volatility, float)) or (isinstance(volatility, int))


def test_value_at_risk():
    var = metric.value_at_risk(data, confidence=0.95, reference='log_return', method='historic_simulation')
    assert math.isclose(var, np.percentile(np.diff(np.log(data)), 5))

    var = metric.value_at_risk(data, confidence=0.99, reference='log_return', method='historic_simulation')
    assert math.isclose(var, np.percentile(np.diff(np.log(data)), 1))

    var = metric.value_at_risk(data, confidence=0.95, reference='pct_return', method='historic_simulation')
    assert math.isclose(var, np.percentile((data[1:] - data[:-1]) / data[:-1], 5))

    var = metric.value_at_risk(data, confidence=0.95, reference='pct_return', method='historic_simulation',
                               annualization_factor=252)
    assert math.isclose(var, np.percentile((data[1:] - data[:-1]) / data[:-1], 5) * np.sqrt(252))

    var = metric.value_at_risk(data, confidence=0.99, reference='log_return', method='var_cov', prob_model='norm')
    assert isinstance(var, float) or isinstance(var, int)

    var = metric.value_at_risk(data, confidence=0.95, reference='abs_return', method='var_cov', prob_model='norm')
    assert isinstance(var, float) or isinstance(var, int)

    var = metric.value_at_risk(data, confidence=0.99, reference='log_return', method='var_cov', prob_model='pareto')
    assert isinstance(var, float) or isinstance(var, int)

    var = metric.value_at_risk(data, confidence=0.99, reference='log_return', method='var_cov', prob_model='log_norm')
    assert isinstance(var, float) or isinstance(var, int)

    var = metric.value_at_risk(data, confidence=0.99, reference='log_return', method='var_cov', prob_model='kde',
                               kde_kernel='gaussian', kde_bandwidth=0.75)
    assert isinstance(var, float) or isinstance(var, int)


def test_rate_of_return():
    ror = metric.total_rate_of_return(data, reference='pct_return', period_length=None, reference_period_length=252)
    assert ror == (data[-1] / data[0]) - 1

    ror = metric.total_rate_of_return(data, reference='log_return', period_length=None, reference_period_length=252)
    assert ror == np.log(data[-1] / data[0])

    ror = metric.total_rate_of_return(data, reference='abs_return', period_length=None, reference_period_length=252)
    assert ror == data[-1] - data[0]

    ror = metric.total_rate_of_return(data, reference='pct_return',
                                      period_length=len(data), reference_period_length=252)
    assert ror == np.power((data[-1] / data[0]), 252 / len(data)) - 1

    ror = metric.total_rate_of_return(data, reference='log_return',
                                      period_length=len(data), reference_period_length=252)
    assert ror == np.log(data[-1] / data[0]) * (252 / len(data))

    ror = metric.total_rate_of_return(data, reference='abs_return',
                                      period_length=len(data), reference_period_length=252)
    assert ror == (data[-1] - data[0]) * (252 / len(data))


def test_sharpe_ratio():
    sr = metric.sharpe_ratio(data, risk_free_rate=0.01, reference='pct_return',
                             prob_model_exp_ror='norm', prob_model_vola='norm', ddof_vola=0,
                             revised_denominator=True, annualization_factor=1)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sharpe_ratio(data, risk_free_rate=0.01, reference='log_return',
                             prob_model_exp_ror='norm', prob_model_vola='norm', ddof_vola=0,
                             revised_denominator=True, annualization_factor=1)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sharpe_ratio(data, risk_free_rate=0, reference='pct_return',
                             prob_model_exp_ror='norm', prob_model_vola='norm', ddof_vola=0,
                             revised_denominator=True, annualization_factor=1)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sharpe_ratio(data, risk_free_rate=0.01, reference='pct_return',
                             prob_model_exp_ror='50_percentile', prob_model_vola='68_percentile', ddof_vola=0,
                             revised_denominator=True, annualization_factor=1)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sharpe_ratio(data, risk_free_rate=0.01, reference='pct_return',
                             prob_model_exp_ror='pareto', prob_model_vola='pareto', ddof_vola=0,
                             revised_denominator=True, annualization_factor=1)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sharpe_ratio(data, risk_free_rate=0.015, reference='log_return',
                             prob_model_exp_ror='pareto', prob_model_vola='pareto', ddof_vola=0,
                             revised_denominator=False, annualization_factor=1)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sharpe_ratio(data, risk_free_rate=0.015, reference='log_return',
                             prob_model_exp_ror='log_norm', prob_model_vola='log_norm', ddof_vola=0,
                             revised_denominator=False, annualization_factor=1)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sharpe_ratio(data, risk_free_rate=0.01, reference='pct_return',
                             prob_model_exp_ror='norm', prob_model_vola='norm', ddof_vola=0,
                             revised_denominator=True, annualization_factor=252)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sharpe_ratio(data, risk_free_rate=0.01, reference='pct_return',
                             prob_model_exp_ror='norm', prob_model_vola='norm', ddof_vola=0,
                             revised_denominator=False, annualization_factor=1)
    assert isinstance(sr, float) or isinstance(sr, int)

    risk_free = np.array([0.01 for _ in range(len(data) - 1)])

    sr = metric.sharpe_ratio(data, risk_free_rate=risk_free, reference='pct_return',
                             prob_model_exp_ror='norm', prob_model_vola='norm', ddof_vola=1,
                             revised_denominator=True, annualization_factor=1)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sharpe_ratio(data, risk_free_rate=np.log(1 + risk_free), reference='log_return',
                             prob_model_exp_ror='pareto', prob_model_vola='68_percentile', ddof_vola=1,
                             revised_denominator=False, annualization_factor=252)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sharpe_ratio(data, risk_free_rate=0.01, reference='pct_return',
                             prob_model_exp_ror='geometric', prob_model_vola='norm', ddof_vola=0,
                             revised_denominator=True, annualization_factor=1)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sharpe_ratio(data, risk_free_rate=0.01, reference='pct_return',
                             prob_model_exp_ror='kde', prob_model_vola='norm', ddof_vola=0,
                             revised_denominator=True, annualization_factor=1,
                             kde_kernel='gaussian', kde_bandwidth=0.75)
    assert isinstance(sr, float) or isinstance(sr, int)


def test_cont_lpm():
    # noinspection SpellCheckingInspection
    clpm = metric.continuous_lower_partial_moment(data, 2, 2, stats.lognorm)
    assert isinstance(clpm, float) or isinstance(clpm, int)


def test_kde_lpm():
    # noinspection SpellCheckingInspection
    kdelpm = metric.kde_lower_partial_moment(data, 2, 2)
    assert isinstance(kdelpm, float) or isinstance(kdelpm, int)


def test_downside_risk():
    dr = metric.downside_risk(data, 2, reference='log_return', prob_model='norm')
    assert isinstance(dr, float) or isinstance(dr, int)

    dr = metric.downside_risk(data, 2, reference='pct_return', prob_model='norm')
    assert isinstance(dr, float) or isinstance(dr, int)

    dr = metric.downside_risk(data, 2, reference='abs_return', prob_model='norm')
    assert isinstance(dr, float) or isinstance(dr, int)

    dr = metric.downside_risk(data, 2, reference='abs_value', prob_model='norm')
    assert isinstance(dr, float) or isinstance(dr, int)

    dr = metric.downside_risk(data, 2, reference='log_return', prob_model='log_norm')
    assert isinstance(dr, float) or isinstance(dr, int)

    dr = metric.downside_risk(data, 2, reference='log_return', prob_model='pareto')
    assert isinstance(dr, float) or isinstance(dr, int)

    dr = metric.downside_risk(data, 2, reference='log_return', prob_model='kde',
                              kde_kernel='gaussian', kde_bandwidth=0.75)
    assert isinstance(dr, float) or isinstance(dr, int)

    dr = metric.downside_risk(data, 2, reference='log_return', prob_model='68_percentile')
    assert isinstance(dr, float) or isinstance(dr, int)


def test_sortino_ratio():
    sr = metric.sortino_ratio(data, target_rate=0.03, reference='pct_return',
                              prob_model_exp_ror='norm', prob_model_dr='norm',
                              annualization_factor=1, alpha=2.0)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sortino_ratio(data, target_rate=0.03, reference='log_return',
                              prob_model_exp_ror='norm', prob_model_dr='norm',
                              annualization_factor=1, alpha=2.0)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sortino_ratio(data, target_rate=0.03, reference='pct_return',
                              prob_model_exp_ror='50_percentile', prob_model_dr='log_norm',
                              annualization_factor=1, alpha=2.0)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sortino_ratio(data, target_rate=0.03, reference='pct_return',
                              prob_model_exp_ror='log_norm', prob_model_dr='norm',
                              annualization_factor=1, alpha=2.0)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sortino_ratio(data, target_rate=0.03, reference='pct_return',
                              prob_model_exp_ror='pareto', prob_model_dr='pareto',
                              annualization_factor=1, alpha=2.0)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sortino_ratio(data, target_rate=0.03, reference='pct_return',
                              prob_model_exp_ror='50_percentile', prob_model_dr='kde',
                              annualization_factor=1, alpha=2.0,
                              kde_kernel='gaussian', kde_bandwidth=0.75)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sortino_ratio(data, target_rate=0.03, reference='pct_return',
                              prob_model_exp_ror='kde', prob_model_dr='kde',
                              annualization_factor=1, alpha=2.0,
                              kde_kernel='gaussian', kde_bandwidth=0.75)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sortino_ratio(data, target_rate=0.03, reference='pct_return',
                              prob_model_exp_ror='50_percentile', prob_model_dr='kde',
                              annualization_factor=252, alpha=2.0,
                              kde_kernel='gaussian', kde_bandwidth=0.75)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sortino_ratio(data, target_rate=0.03, reference='pct_return',
                              prob_model_exp_ror='50_percentile', prob_model_dr='kde',
                              annualization_factor=12, alpha=3.0,
                              kde_kernel='gaussian', kde_bandwidth=0.75)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sortino_ratio(data, target_rate=0.03, reference='pct_return',
                              prob_model_exp_ror='50_percentile', prob_model_dr='68_percentile',
                              annualization_factor=1, alpha=2.0)
    assert isinstance(sr, float) or isinstance(sr, int)

    sr = metric.sortino_ratio(data, target_rate=0.03, reference='pct_return',
                              prob_model_exp_ror='geometric', prob_model_dr='norm',
                              annualization_factor=1, alpha=2.0)
    assert isinstance(sr, float) or isinstance(sr, int)

    try:
        _ = metric.sortino_ratio(data, target_rate=0.03, reference='pct_return',
                                 prob_model_exp_ror='some', prob_model_dr='norm',
                                 annualization_factor=1, alpha=2.0)
    except NotImplementedError:
        pass

    try:
        _ = metric.sortino_ratio(data, target_rate=0.03, reference='pct_return',
                                 prob_model_exp_ror='norm', prob_model_dr='some',
                                 annualization_factor=1, alpha=2.0)
    except NotImplementedError:
        pass


def test_drawdowns():
    draw, depth, peak_indices, through_indices = metric.drawdown(data, mode='relative')
    assert np.array_equal(depth, np.array([5, 6]))
    assert np.array_equal(peak_indices, np.array([5, 12]))
    assert np.array_equal(through_indices, np.array([7, 16]))

    draw, depth, peak_indices, through_indices = metric.drawdown(data, mode='absolute')
    assert np.array_equal(depth, np.array([5, 6]))
    assert np.array_equal(peak_indices, np.array([5, 12]))
    assert np.array_equal(through_indices, np.array([7, 16]))
