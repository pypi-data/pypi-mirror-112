import numpy as np
from scipy import stats
from scipy.stats.mstats import gmean
from scipy.integrate import quad
from sklearn.neighbors import KernelDensity

from trapeza import utils

# todo: implement more metrics
# todo: https://en.wikipedia.org/wiki/List_of_financial_performance_measures
# todo: https://en.wikipedia.org/wiki/Tail_value_at_risk
# todo: https://en.wikipedia.org/wiki/Bias_ratio
# todo: https://en.wikipedia.org/wiki/Average_absolute_deviation
# todo: https://blog.quantinsti.com/volatility-and-measures-of-risk-adjusted-return-based-on-volatility/
# todo: https://en.wikipedia.org/wiki/Calmar_ratio
# todo: volatility (own idea): fit linear regression line and calculate volatility of error terms (distance to
#                              regression line)
# todo: long short exposure, sector exposure, etc.


def _returns(data, reference):
    """
    Calculates returns based on the same frequency as data (e.g. if data is on daily basis, than returned returns are
    on daily basis as well)
    :param data: 1D list or array shape(n,)
    :param reference: str, {log_return, pct_return, abs_return}
    :return: 1D array, shape(n-1,)
    """
    if reference == 'log_return':
        ref = np.diff(np.log(data))
    elif reference == 'pct_return':
        ref = np.diff(data) / data[:-1]
    elif reference == 'abs_return':
        ref = np.diff(data)
    else:
        raise NotImplementedError('Currently only {log_return, pct_return, abs_return} are implemented.')
    return ref


def total_rate_of_return(data, reference='pct_return', period_length=None, reference_period_length=252):
    """
    Calculates overall historic rate of return over given period and applies annualization if period_length is not None.
    Does not apply any probability modelling approach. Does not return expected rate of return per time step.
    :param data: 1D list or array
    :param reference: str, {'log_return', 'pct_return', 'abs_return'},
                      type of rate of return, calculation of rate of return:
                        log_return: logarithmic return (base e) for final and initial value
                        pct_return: percentage return for final and initial value
                        abs_return: absolute differences for final and initial value
    :param period_length: int, float or None,
                          annualization parameter
                            None: no annualization applied
                            int or float: period which is spanned by param:data
                                          e.g., if daily data, period_length represents number of days described
                                          by param:data,
                                          typically period_length=len(data)
                                log_return: log_return * (reference_period_length / period_length)
                                pct_return: np.power(1 + pct_return, reference_period_length / period_length) - 1
                                abs_return: abs_return * (reference_period_length / period_length)
    :param reference_period_length: int or float,
                                    ignored if period_length=None
                                    total length spanned by reference period in relation to param:period_length,
                                    e.g. if daily data, reference_period_length=252 (or 365) if rate of return is to be
                                    annualized (provided that period_length is not None)
    :return: float
             result is returned as the same type as param:reference (e.g. log returns are not converted back)
    :TODO: factor in inflation
    :TODO: factor in time value of money
    """
    if reference == 'pct_return':
        ret = (data[-1] / data[0]) - 1
        if period_length is not None:
            ret = np.power(1 + ret, reference_period_length / period_length) - 1
    elif reference == 'log_return':
        ret = np.log(data[-1] / data[0])
        if period_length is not None:
            ret = ret * (reference_period_length / period_length)
    elif reference == 'abs_return':
        ret = data[-1] - data[0]
        if period_length is not None:
            ret = ret * (reference_period_length / period_length)
    else:
        raise NotImplementedError('Currently only {pct_return, log_return, abs_return} are implemented.')

    return ret


def volatility(data, reference='log_return', prob_model='norm', ddof=0, annualization_factor=1, alpha=2.0):
    """
    Calculates volatility (either as standard deviation or defined by prob_model)
    :param data: 1D list or array
    :param reference: str, {'log_return', 'pct_return', 'abs_return', 'abs_value', 'indexed_value'},
                      reference values used as underlying to calculate standard deviation (or similar concepts defined
                      by prob_model):
                        log_return: daily (or respective frequency of param:data) logarithmic returns (base e)
                        pct_return: daily (or respective frequency of param:data) percentage return
                        abs_return: daily (or respective frequency of param:data) absolute differences to previous day
                        abs_value: absolute (price) values without pre-processing or any return calculations (plain
                                   raw input)
                        indexed_value: (price) values are indexed to 100 with respect to first data point
    :param prob_model: str, {'norm', '68_percentile', 'pareto', 'log_norm', 'chebyshev'}
                       probability model to calculate standard deviation or similar concepts:
                        norm: normal distribution, uses conventional standard deviation
                        68_percentile: calculates symmetric percentile limits, in which 68% of all values lie within,
                                       and return half of the limits' width. Therefore this method follows roughly the
                                       same concept as the standard deviation of normal distributions
                        pareto: pareto distribution based on scipy implementation
                        log_norm: log normal distribution based on scipy implementation
                        chebyshev: use Chebyshev's inequality, NOT IMPLEMENTED
                                   https://en.wikipedia.org/wiki/Chebyshev's_inequality
                                   https://stats.stackexchange.com/questions/82419/does-a-sample-version-of-the-one-sided-chebyshev-inequality-exist
                                   https://stats.stackexchange.com/questions/108578/what-does-standard-deviation-tell-us-in-non-normal-distribution
    :param ddof: int, delta degree of freedom,
                 use ddof=1 for sample standard deviation
                 use ddof=0 for population standard deviation
                 currently only implemented, if prob_model='norm'
    :param annualization_factor: int or float,
                                 annualization: volatility * sqrt(annualization_factor)
                                 provided that data is daily:
                                     use annualization_factor=1 for daily standard deviation,
                                     annualization_factor=252 for yearly (if no trading at weekends etc.,
                                     cf. 365 for cryptos),
                                     and annualization_factor=252/12 for monthly
    :param alpha: float,
                  scaling factor for calculating annualization factor according to Levy stability exponent
                  annualized_volatility = np.power(annualization_factor, 1/alpha) * volatility
                  alpha=2.0 equals sqrt(annualization_factor)
    :return: float
             result is returned as the same type as param:reference (e.g. log returns are not converted back)
    :TODO: implement prob_model='chebyshev' and different probability distributions and auto select
    :TODO: check if kde is feasible
    """
    # cast to array
    if type(data) is list:
        data = np.array(data)

    # calculate reference for taking standard deviation
    if reference in ['log_return', 'pct_return', 'abs_return']:
        ref = _returns(data, reference)
    elif reference == 'abs_value':
        ref = data
    elif reference == 'indexed_value':
        ref = (data / data[-1]) * 100
    else:
        raise NotImplementedError('Currently only {log_return, pct_return, abs_return, abs_value, '
                                  'indexed_price} are implemented.')

    # take standard deviation according to probability model
    if prob_model == 'norm':
        vola = np.nanstd(ref, ddof=ddof, dtype=np.float64)
    elif prob_model == '68_percentile':
        # vola = (np.percentile(data, 84.13447) - np.percentile(data, 15.86553)) * 0.5
        vola = (np.percentile(ref, 84.13447) - np.percentile(ref, 15.86553)) * 0.5
    elif prob_model == 'pareto':
        vola = utils.scipy_dist_fit_std(ref, stats.pareto)
    elif prob_model == 'log_norm':
        vola = utils.scipy_dist_fit_std(ref, stats.lognorm)
    else:
        raise NotImplementedError('Currently only {norm, 68_percentile, pareto} are implemented.')

    # annualize standard deviation
    return np.power(annualization_factor, 1/alpha) * vola
    # return np.sqrt(annualization_factor) * vola


def continuous_lower_partial_moment(data, target, order, scipy_distribution):
    """
    Calculates the lower partial moment based on supplied distribution (param:scipy_distribution), which only factor in
    values below target with respect to the whole distribution estimated by param:data
    :param data: 1D list or array
    :param target: int or float
    :param order: int
    :param scipy_distribution: scipy distribution class,
                               e.g. scipy.stats.pareto
    :return: float
    """
    shape_params = scipy_distribution.fit(data, loc=0, scale=1)

    def integrand(x):
        return scipy_distribution.pdf(x, *shape_params) * np.power(target - x, order)

    return quad(integrand, -1 * np.inf, target)[0]


def kde_lower_partial_moment(data, target, order, kernel='gaussian', bandwidth=0.75):
    """
    Calculates the lower partial moment based on kernel density estimation, which only factor in values below target
    with respect to the whole distribution estimated by param:data
    :param data: 1D list or array
    :param target: int or float
    :param order: int
    :param kernel: str,
                   see sklearn.neighbors.KernelDensity
    :param bandwidth: str,
                      see sklearn.neighbors.KernelDensity
    :return: float
    """
    if type(data) is list:
        data = np.asarray(data)
    if data.ndim < 2:
        data = np.expand_dims(data, 1)

    kde = KernelDensity(kernel=kernel, bandwidth=bandwidth).fit(data)

    def integrand(x):
        if type(x) is not np.ndarray:
            x = np.array([[x]])
        if x.ndim < 1:
            x = np.expand_dims(x, 1)
        return np.exp(kde.score_samples(x)) * np.power(target-x, order)[0]

    return quad(integrand, -1 * np.inf, target)[0]


def downside_risk(data, target, reference='log_return', prob_model='norm', kde_kernel='gaussian', kde_bandwidth=0.75):
    """
    Calculates downside risk defined as the downside deviation (target semi-deviation, 'standard deviation of only
    negative values', also defined as probability-weighted squared below-target values),
    square root of downside variance.

    :param data: 1D list or array
    :param target: int or float,
                   if param:reference is in log_return, then use log_risk_free_rate,
                   if param:reference is in pct_return, then use pct_risk_free_rate
                   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                   !!! basically, must be in the same scale/ unit as param:reference !!!
                   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    :param reference: str, {'log_return', 'pct_return', 'abs_return', 'abs_value', 'indexed_value'},
                      reference values used as underlying to calculate lower partial moment (or similar concepts defined
                      by prob_model):
                        log_return: daily (or respective frequency of param:data) logarithmic returns (base e)
                        pct_return: daily (or respective frequency of param:data) percentage return
                        abs_return: daily (or respective frequency of param:data) absolute differences to previous day
                        abs_value: absolute (price) values without pre-processing or any return calculations (plain
                                   raw input)
    :param prob_model: str, {'norm', 'pareto', 'log_norm', 'kde', '68_percentile'}
                       probability model to calculate lower partial moment or similar concepts:
                        norm: normal distribution, uses conventional standard deviation
                        pareto: pareto distribution based on scipy implementation
                        log_norm: log normal distribution based on scipy implementation
                        kde: kernel density estimation based on sklearn.neighbors.KernelDensity
                        68_percentile: calculates symmetric percentile limits, in which 68% of all values lie within,
                                       and return half of the limits' width. Therefore this method follows roughly the
                                       same concept as the standard deviation of normal distributions
    :param kde_kernel: str,
                       see sklearn.neighbors.KernelDensity
                       ignored if param:prob_model is not 'kde'
    :param kde_bandwidth: str,
                          see sklearn.neighbors.KernelDensity
                          ignored if param:prob_model is not 'kde'
    :return: float,
             result is returned as the same type as param:reference (e.g. log returns are not converted back)
    """
    # cast to array
    if type(data) is list:
        data = np.array(data)

    # calculate reference for taking standard deviation
    if reference in ['log_return', 'pct_return', 'abs_return']:
        ref = _returns(data, reference)
    elif reference == 'abs_value':
        ref = data
    else:
        raise NotImplementedError('Currently only {log_return, pct_return, abs_return, abs_value} are implemented.')

    if prob_model == 'norm':
        adj_ref = ref - target
        neg_ref_sum = np.sum(np.power(np.clip(adj_ref, a_min=None, a_max=0), 2))
        downside_dev = np.sqrt(neg_ref_sum / len(ref))
    elif prob_model == '68_percentile':
        adj_ref = ref - target
        neg_ref_sum = np.sum(np.power(np.clip(adj_ref, a_min=None, a_max=0), 2))
        downside_dev = (np.percentile(neg_ref_sum, 84.13447) - np.percentile(neg_ref_sum, 15.86553)) * 0.5
    elif prob_model == 'pareto':
        downside_dev = np.sqrt(continuous_lower_partial_moment(ref, target, 2, stats.pareto))
    elif prob_model == 'log_norm':
        downside_dev = np.sqrt(continuous_lower_partial_moment(ref, target, 2, stats.lognorm))
    elif prob_model == 'kde':
        downside_dev = np.sqrt(kde_lower_partial_moment(ref, target, 2, kernel=kde_kernel, bandwidth=kde_bandwidth))
    else:
        raise NotImplementedError('Currently only {norm, pareto, log_norm, kde} are implemented.')

    return downside_dev


def value_at_risk(data, confidence=0.95, reference='log_return', prob_model='norm', ddof=0,
                  method='historic_simulation', annualization_factor=1, alpha=2.0,
                  kde_kernel='gaussian', kde_bandwidth=0.75):
    """
    Calculate value at risk metric. Gives lowest return rate, which is to be expected in [confidence]% of all cases.
    :param data: 1D array or list
    :param confidence: float, (0, 1),
                       confidence level to calculate value at risk,
                       takes 1-confidence as percentile for calculations
    :param reference: str, {'log_return', 'pct_return', 'abs_return', abs_value', 'indexed_value'},
                      reference values used as underlying to calculate standard deviation (or similar concepts defined
                      by prob_model):
                        log_return: daily (or respective frequency of param:data) logarithmic returns (base e)
                        pct_return: daily (or respective frequency of param:data) percentage return
                        abs_return: daily (or respective frequency of param:data) absolute differences to previous day
                        abs_value: absolute (price) values without pre-processing or any return calculations (plain
                                   raw input)
                        indexed_value: (price) values are indexed to 100 with respect to first data point
    :param prob_model: str, {norm, log_norm, pareto, kde},
                       ignored if method='historic_simulation', only in use if method='var_cov'
                       probability models:
                        norm: normal distribution
                        log_norm: log normal distribution based on scipy implementation
                        pareto: pareto distribution based on scipy implementation
                        kde: kernel_density_distribution

                        CURRENTLY ONLY NORM AND PARETO ARE IMPLEMENTED
    :param ddof: int, delta degree of freedom,
                 use ddof=1 for sample standard deviation
                 use ddof=0 for population standard deviation
                 currently only implemented, if prob_model='norm'
    :param method: str, {'historic_simulation', 'var_cov'},
                   historic_simulation: calculation based on (1-confidence)-percentile of historic data
                   var_cov: fit probability model and calculate value at 1-confidence% of inverse cumulative
                            distribution function (1-confidence% of all values of probability function are less or
                            equal to calculated value)
    :param annualization_factor: int or float,
                                 annualization: volatility * sqrt(annualization_factor)
                                 provided that data is daily:
                                     use annualization_factor=1 for daily,
                                     annualization_factor=252 for yearly (if no trading at weekends etc.,
                                     cf. 365 for cryptos),
                                     and annualization_factor=252/12 for monthly
    :param alpha: float,
                  scaling factor for calculating annualization factor according to Levy stability exponent
                  annualized_volatility = np.power(annualization_factor, 1/alpha) * volatility
                  alpha=2.0 equals sqrt(annualization_factor)
    :param kde_kernel: str,
                       see sklearn.neighbors.KernelDensity
                       ignored if param:prob_model is not 'kde'
    :param kde_bandwidth: str,
                          see sklearn.neighbors.KernelDensity
                          ignored if param:prob_model is not 'kde'
    :return: float,
             result is returned as the same type as param:reference (e.g. log returns are not converted back)
    :TODO: implement different probability models (e.g. pareto) and auto select
    :TODO: Monte Carlo https://s3.amazonaws.com/assets.datacamp.com/production/course_5612/slides/chapter4.pdf
    """
    # cast to array
    if type(data) is list:
        data = np.array(data)

    # calculate reference for taking standard deviation
    if reference in ['log_return', 'pct_return', 'abs_return']:
        ref = _returns(data, reference)
    elif reference == 'abs_value':
        ref = data
    elif reference == 'indexed_value':
        ref = (data / data[-1]) * 100
    else:
        raise NotImplementedError('Currently only {log_return, pct_return, abs_return, abs_value, '
                                  'indexed_value} are implemented.')

    if method == 'historic_simulation':
        v_a_r = np.quantile(ref, 1-confidence)
    elif method == 'var_cov':
        if prob_model == 'norm':
            v_a_r = stats.norm.ppf(1-confidence, np.mean(ref), np.std(ref, ddof=ddof))
        elif prob_model == 'log_norm':
            v_a_r = utils.scipy_dist_fit_ppf(ref, 1-confidence, stats.lognorm)
        elif prob_model == 'pareto':
            v_a_r = utils.scipy_dist_fit_ppf(ref, 1-confidence, stats.pareto)
        elif prob_model == 'kde':
            v_a_r = utils.kde_ppf(ref, 1-confidence, kernel=kde_kernel, bandwidth=kde_bandwidth)
        else:
            raise NotImplementedError('Currently only {norm, pareto, kde} is implemented.')
    else:
        raise NotImplementedError('Currently only {historic_simulation, var_cov} are implemented.')

    # annualize
    return np.power(annualization_factor, 1/alpha) * v_a_r
    # return np.sqrt(annualization_factor) * v_a_r


def expected_rate_of_return(ret, reference_rate, prob_model_exp_ror, kde_kernel, kde_bandwidth):
    """
    Calculates expected rate of (excess) return based on a data series of returns.
    Returns are not scaled or manipulated in any way (so if log returns shall be used, returns have to be converted
    to log returns before calling this function).
    Reference rate is used to calculate excess rate of return: rate - reference rate, from which expected value is
    calculated and returned.
    :param ret: 1D list or array,
                returns, not raw data, no further data manipulation applied
    :param reference_rate: int or float,
                           reference rate to calculate excess rate: ret - reference_rate
    :param prob_model_exp_ror: str, {'norm', 'log_norm', '50_percentile', 'pareto', 'kde', 'geometric'},
                               probability model to calculate expected rate of return per time step (frequency given
                               in param:data):
                                norm: normal distribution, mean as estimator
                                log_norm: log normal distribution, mean defined on log normal distribution as estimator,
                                        scipy implementation
                                50_percentile: median as estimator
                                pareto: pareto distribution, mean defined on pareto distribution as estimator,
                                        scipy implementation
                                kde: kernel density estimation
                                geometric: geometric mean as compound rate of return,
                                           this does not apply any probability distribution but calculates mean
                                           compound excess rate of return based on historic data
    :param kde_kernel: str,
                       see sklearn.neighbors.KernelDensity
                       ignored if param:prob_model_exp_ror is not 'kde'
    :param kde_bandwidth: str,
                          see sklearn.neighbors.KernelDensity
                          ignored if param:prob_model_exp_ror is not 'kde'
    :return: float,
             expected rate of return
    """
    # cast to numpy array
    if type(ret) is list:
        ret = np.array(ret)

    if prob_model_exp_ror == 'norm':
        exp_ret = np.mean(ret - reference_rate)
    elif prob_model_exp_ror == 'log_norm':
        exp_ret = utils.scipy_dist_fit_mean(ret - reference_rate, stats.lognorm)
    elif prob_model_exp_ror == '50_percentile':
        exp_ret = np.percentile(ret - reference_rate, 50)
    elif prob_model_exp_ror == 'pareto':
        exp_ret = utils.scipy_dist_fit_mean(ret - reference_rate, stats.pareto)
    elif prob_model_exp_ror == 'kde':
        exp_ret = utils.kde_ppf(ret - reference_rate, 0.5, kernel=kde_kernel, bandwidth=kde_bandwidth)
    elif prob_model_exp_ror == 'geometric':
        exp_ret = gmean(ret - reference_rate)
    else:
        raise NotImplementedError('Currently only {norm, 50_percentile, pareto, kde, geometric} are implemented.')

    return exp_ret


def sharpe_ratio(data, risk_free_rate=0.0001173037, reference='pct_return', prob_model_exp_ror='norm',
                 prob_model_vola='norm', ddof_vola=0, revised_denominator=True, annualization_factor=1, alpha=2.0,
                 kde_kernel='gaussian', kde_bandwidth=0.75):
    # target -> 3% in absolute percent --> daily percent: 0.00011730371383444904
    # log(1.00011730371383444904) = 0.0001172968
    """
    Calculates Sharpe ratio
    :param data: 1D list or array
    :param risk_free_rate: int, float or 1D array
                           risk free rate to calculate sharpe ratio
                           if param:reference is in log_return, then use log_risk_free_rate,
                           if param:reference is in pct_return, then use pct_risk_free_rate
                           !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                           !!! basically, must be in the same scale/ unit as param:reference !!!
                           !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                           e.g. if param:data is daily, then risk_free_rate must be daily as well
                              target -> 3% in absolute percent per year --> daily percent: 0.00011730371383444904
                              log(1.00011730371383444904) = 0.0001172968 for log daily percent
    :param reference: str, {'log_return', 'pct_return'},
                      reference values used as underlying to calculate standard deviation (or similar concepts defined
                      by prob_model_exp_ror and prob_model_vola) and expected
                      rate of return (in same frequency as param:data):
                        log_return: daily logarithmic returns (base e)
                        pct_return: daily percentage return
    :param prob_model_exp_ror: str, {'norm', 'log_norm', '50_percentile', 'pareto', 'kde', 'geometric'},
                               probability model to calculate expected rate of return per time step (frequency given
                               in param:data):
                                norm: normal distribution, mean as estimator
                                log_norm: log normal distribution, mean defined on log normal distribution as estimator,
                                        scipy implementation
                                50_percentile: median as estimator
                                pareto: pareto distribution, mean defined on pareto distribution as estimator,
                                        scipy implementation
                                kde: kernel density estimation
                                geometric: geometric mean as compound rate of return,
                                           this does not apply any probability distribution but calculates mean
                                           compound excess rate of return based on historic data
    :param prob_model_vola: str, {'norm', '68_percentile', 'pareto', 'log_norm', 'chebyshev'}
                            probability model to calculate volatility, see metrics.volatility()
    :param ddof_vola: int, delta degree of freedom,
                      used for metrics.volatility()
                      use ddof=1 for sample standard deviation
                      use ddof=0 for population standard deviation
    :param revised_denominator: bool,
                                whether to use original or revised definition of the sharpe ratio
                                    revised=True: std(total_rate_of_return - risk_free_rate)
                                    revised=False: std(total_rate_of_return)
                                ignored, if param:risk_free_rate is int, as std(a-b)==std(a) if b is constant
    :param annualization_factor: int or float,
                                 annualization: volatility * sqrt(annualization_factor)
                                 provided that data is daily:
                                     use annualization_factor=1 for daily,
                                     annualization_factor=252 for yearly (if no trading at weekends etc.,
                                     cf. 365 for cryptos),
                                     and annualization_factor=252/12 for monthly
    :param alpha: float,
                  scaling factor for calculating annualization factor according to Levy stability exponent
                  annualized_volatility = np.power(annualization_factor, 1/alpha) * volatility
                  alpha=2.0 equals sqrt(annualization_factor)
    :param kde_kernel: str,
                       see sklearn.neighbors.KernelDensity
                       ignored if param:prob_model_exp_ror is not 'kde'
    :param kde_bandwidth: str,
                          see sklearn.neighbors.KernelDensity
                          ignored if param:prob_model_exp_ror is not 'kde'
    :return: float,
             result is returned as the same type as param:reference (e.g. log returns are not converted back)
    """
    if type(risk_free_rate) is list:
        risk_free_rate = np.array(risk_free_rate)

    if reference in ['log_return', 'pct_return']:
        ret = _returns(data, reference)
    else:
        raise NotImplementedError('Currently only {log_return, pct_return} are implemented.')

    # do not annualize expected returns at this point
    exp_ret = expected_rate_of_return(ret, risk_free_rate, prob_model_exp_ror, kde_kernel, kde_bandwidth)

    # do not annualize volatility at this point
    if isinstance(risk_free_rate, int) or revised_denominator is False:
        # first case: std(a-b) == std(a) if b is constant
        # second case: std(a) is old sharpe ratio definition
        sharpe = exp_ret / volatility(data, reference=reference, prob_model=prob_model_vola, ddof=ddof_vola,
                                      annualization_factor=1)
    elif revised_denominator is True:
        sharpe = exp_ret / volatility(ret - risk_free_rate, reference='abs_value', prob_model=prob_model_vola,
                                      ddof=ddof_vola, annualization_factor=1)
    else:
        raise TypeError('revised_denominator must be boolean.')

    # annualize
    return np.power(annualization_factor, 1/alpha) * sharpe
    # return np.sqrt(annualization_factor) * sharpe


def sortino_ratio(data, target_rate=0.0001173037, reference='pct_return', prob_model_exp_ror='norm',
                  prob_model_dr='norm', annualization_factor=1, alpha=2.0, kde_kernel='gaussian', kde_bandwidth=0.75):
    """
    Calculates Sortino ratio
    :param data: 1D list or array
    :param target_rate: int, float or 1D array
                        target rate to calculate sortino ratio
                        if param:reference is in log_return, then use log_target_rate,
                        if param:reference is in pct_return, then use pct_target_rate
                        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        !!! basically, must be in the same scale/ unit as param:reference !!!
                        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        e.g. if param:data is daily, then target_rate must be daily as well
                              target -> 3% in absolute percent per year --> daily percent: 0.00011730371383444904
                              log(1.00011730371383444904) = 0.0001172968 for log daily percent
    :param reference: str, {'log_return', 'pct_return'},
                      reference values used as underlying to calculate standard deviation (or similar concepts defined
                      by prob_model_exp_ror and prob_model_vola) and expected
                      rate of return (in same frequency as param:data):
                        log_return: daily logarithmic returns (base e)
                        pct_return: daily percentage return
    :param prob_model_exp_ror: str, {'norm', 'log_norm' '50_percentile', 'pareto', 'kde', 'geometric'},
                               probability model to calculate expected rate of return per time step (frequency given
                               in param:data):
                                norm: normal distribution, mean as estimator
                                log_norm: log normal distribution, mean defined on log normal distribution as estimator,
                                        scipy implementation
                                50_percentile: median as estimator
                                pareto: pareto distribution, mean defined on pareto distribution as estimator,
                                        scipy implementation
                                kde: kernel density estimation
                                geometric: geometric mean as compound rate of return,
                                           this does not apply any probability distribution but calculates mean
                                           compound excess rate of return based on historic data
    :param prob_model_dr: str, {'norm', 'log_normal', 'pareto', 'log_norm', 'kde', '68_percentile'}
                          probability model to calculate downside risk, see metrics.downside_risk()
    :param annualization_factor: int or float,
                                 annualization: volatility * sqrt(annualization_factor)
                                 provided that data is daily:
                                     use annualization_factor=1 for daily,
                                     annualization_factor=252 for yearly (if no trading at weekends etc.,
                                     cf. 365 for cryptos),
                                     and annualization_factor=252/12 for monthly
    :param alpha: float,
                  scaling factor for calculating annualization factor according to Levy stability exponent
                  annualized_volatility = np.power(annualization_factor, 1/alpha) * volatility
                  alpha=2.0 equals sqrt(annualization_factor)
    :param kde_kernel: str,
                       see sklearn.neighbors.KernelDensity
                       only used if one (or both) of the probability models uses 'kde'
    :param kde_bandwidth: str,
                          see sklearn.neighbors.KernelDensity
                          only used if one (or both) of the probability models uses 'kde'
    :return: float,
             result is returned as the same type as param:reference (e.g. log returns are not converted back)
    """
    if type(target_rate) is list:
        target_rate = np.array(target_rate)

    if reference in ['log_return', 'pct_return']:
        ret = _returns(data, reference)
    else:
        raise NotImplementedError('Currently only {log_return, pct_return} are implemented.')

    # do not annualize expected returns at this point
    exp_ret = expected_rate_of_return(ret, target_rate, prob_model_exp_ror, kde_kernel, kde_bandwidth)

    down_risk = downside_risk(ret, target_rate, reference='abs_value', prob_model=prob_model_dr,
                              kde_kernel=kde_kernel, kde_bandwidth=kde_bandwidth)
    if down_risk > 0.0001:
        sortino = exp_ret / down_risk
    else:
        sortino = 0

    return np.power(annualization_factor, 1/alpha) * sortino
    # return np.sqrt(annualization_factor) * sortino


# noinspection PyUnusedLocal
def win_loss_ratio(data):
    """
    The win/loss ratio is the ratio of the total number of winning trades to the number of losing trades. It does not
    take into account how much was won or lost, but simply if they were winners or losers.
    Source: https://www.investopedia.com/terms/w/win-loss-ratio.asp

    Also known as success ratio.

    TODO: implement
    """
    raise NotImplementedError


def max_drawdown(data, mode='relative'):
    """
    Maximum drawdown is a specific measure of drawdown that looks for the greatest movement from a high point to a low
    point, before a new peak is achieved. However, it's important to note that it only measures the size of the largest
    loss, without taking into consideration the frequency of large losses. Because it measures only the largest
    drawdown, MDD does not indicate how long it took an investor to recover from the loss, or if the investment even
    recovered at all.
    Source: https://www.investopedia.com/terms/m/maximum-drawdown-mdd.asp

    :param data: 1D list or 1D array
    :param mode: str, {'relative', 'absolute'}
                 relative: drawdown is calculated based on relative values, which means dividing nominal drawdown value
                           by accumulated amount to find peak and through values
                           !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                           !!! max relative drop, not referenced to total invested capital but peak to total !!!
                           !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                           no logs applied
                 absolute: drawdown is calculated based on absolute values

                 e.g. S&P500:
                    2007-2008: drawdown =    888 points --> 57%
                         2020: drawdown = 11,150 points --> 34%
                    --> absolute and relative drawdown differ significantly
                 if drawdown analysis comprises a longer period, relative numbers might make more sense
    :return: depth: int,
                    absolute max drawdown value, see param:mode
                    NOT referenced to total invested capital but peak to through
                    depth=0, if only ascending values in data
             peak_index: int or None,
                         index of peak value in data
                         None if only ascending values in data
             through_index: int or None,
                            index of through value in data
                            None if only ascending values in data
    """
    # index indicating through point
    if mode == 'relative':
        through_index = np.argmax((np.maximum.accumulate(data) - data)
                                  / np.maximum.accumulate(data))
    elif mode == 'absolute':
        through_index = np.argmax(np.maximum.accumulate(data) - data)
    else:
        raise NotImplementedError('Parameter mode only implements {relative, absolute}.')

    # if no through value was found, then only ascending values contained in data
    if through_index == 0:
        return 0, None, None

    peak_index = np.argmax(data[:through_index])  # index indicating peak point

    through_value = data[through_index]
    peak_value = data[peak_index]

    depth = peak_value - through_value

    return depth, peak_index, through_index


def high_water_marks(data):
    """
    Calculate high water marks. A high water mark is reached, if current value exceeds all past values. Every time a new
    high/ maximum is reached, it is called a high water mark
    :param data: 1D list or 1D array
    :return: water_mark_values: 1D array of floats,
                                values of high water marks (shape does not match data, but just lists all high water
                                marks that have been reached)
             water_mark_indices: 1D array of floats,
                                 indices in param:data, where high water marks are located within
    """
    water_marks = np.maximum.accumulate(data)
    water_marks_values, water_marks_indices = np.unique(water_marks, return_index=True)
    return water_marks_values, water_marks_indices


def drawdown(data, mode='relative'):
    """
    Calculates drawdown over the entire data frame. Drawdown is defined as peak-to-through. Peaks are values, which
    are larger than all previous values. Through values are minimum between two peaks. In contrast to maximum drawdown,
    this function returns all (local) drawdowns over the entire data frame.
    :param data: 1D list or 1D array
    :param mode: str, {'relative', 'absolute'}
                 relative: drawdown is calculated based on relative values, which means dividing nominal drawdown value
                           by accumulated amount to find peak and through values
                           no logs applied
                 absolute: drawdown is calculated based on absolute values

                 e.g. S&P500:
                    2007-2008: drawdown =    888 points --> 57%
                         2020: drawdown = 11,150 points --> 34%
                    --> absolute and relative drawdown differ significantly
                 if drawdown analysis comprises a longer period, relative numbers might make more sense
    :return: draw: 1D array, same length as param:data,
                   running drawdown at each point in data frame, which resembles drawdown from previous peak,
                   used to plot drawdown/ under water chart
             depth: 1D array,
                    depth between peak and through values,
                    depth between peak_indices[c] and through_indices[c]
             peak_indices: 1D array,
                           index of peak values within param:data,
                           peak_indices[c] is related to through_indices[c]
             through_indices: 1D array,
                              index of through values within param:data
                              peak_indices[c] is related to through_indices[c]
    """

    if mode == 'relative':
        draw = (data - np.maximum.accumulate(data)) / np.maximum.accumulate(data)
    elif mode == 'absolute':
        draw = data - np.maximum.accumulate(data)
    else:
        raise NotImplementedError('Parameter mode only implements {relative, absolute}.')

    peak_indices = np.where((draw[:-1] == 0) & (draw[:-1] > draw[1:]))[0]

    through_indices = []

    if len(peak_indices) > 1:
        for i in range(len(peak_indices)-1):
            through_indices.append(np.argmin(data[peak_indices[i]:peak_indices[i+1]]) + peak_indices[i])
    through_indices.append(np.argmin(data[peak_indices[-1]:]) + peak_indices[-1])

    depth = data[peak_indices] - data[through_indices]
    return draw, depth, peak_indices, through_indices
