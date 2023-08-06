from functools import reduce
import operator
from sklearn.neighbors import KernelDensity
import numpy as np
from scipy.integrate import quad
from trapeza.arithmetics import py_dtoa_ryu
from decimal import Decimal


class ProtectedDict(dict):
    def __setitem__(self, key, value):
        raise AttributeError('Dictionary is protected from direct manipulation via key access. Proper methods of '
                             'respective class (e.g. see FXAccount or FXStrategy) or assignment of complete dictionary '
                             'instance (self.attr = {...}) must be used. Direct element access via key is only '
                             'supported for getter but not setter of dictionary. Alternatively, manipulate underlying '
                             'c-implemented (cython) class (e.g. cFXAccount or cFXStrategy) dictionary, '
                             'whose class attributes are wrapped by corresponding Python class (nonetheless it is '
                             'highly recommended to not manipulate c-implemented (cython) class attributes, but use '
                             'respective class methods).')


class ProtectedExecHeap(list):
    def __setitem__(self, key, value):
        raise AttributeError('List self.exec_heap is protected from direct manipulation via index access. '
                             'Proper methods of FXAccount or assignment of complete list instance (self.attr = [...]) '
                             'must be used. Direct element access via index is only supported for getter but not '
                             'setter of self.exec_heap. Alternatively, manipulate underlying c-implemented (cython) '
                             'cFXAccount vector minHeap (self.vec_heap), which is wrapped by FXAccount @property.')


class ProtectedList(list):
    def __setitem__(self, key, value):
        raise AttributeError('List is protected from direct manipulation via index access. Proper methods of '
                             'respective class (e.g. see FXAccount or FXStrategy) or assignment of complete list '
                             'instance (self.attr = [...]) must be used. Direct element access via index is only '
                             'supported for getter but not setter of list. Alternatively, manipulate underlying '
                             'c-implemented (cython) class (e.g. cFXAccount or cFXStrategy) list, '
                             'whose class attributes are wrapped by corresponding Python class (nonetheless it is '
                             'highly recommended to not manipulate c-implemented (cython) class attributes, but use '
                             'respective class methods).')


class StringTupleKeyDict(dict):
    def __getitem__(self, key):
        return dict.__getitem__(self, (str(key[0]), str(key[1])))

    def __setitem__(self, key, value):
        dict.__setitem__(self, (str(key[0]), str(key[1])), value)


def _convert_args_to_decimal(*args):
    """
    Turns ints and floats into list of decimal.Decimal
    :param args: ints or floats
    :return: list of decimal.Decimal
    """
    args = map(Decimal, map(py_dtoa_ryu, args))
    return args


def precision_add(*args):
    """
    Addition operation with minimized floating point error. Implementation based on standard decimal module.
    :param args: number/ floats to be summed up
    :return: float
    """
    args = _convert_args_to_decimal(*args)
    return float(sum(args))


def precision_subtract(minuend, subtrahend):
    """
    Subtraction operation with minimized floating point error. Implementation based on standard decimal module.
    :param minuend: int or float
    :param subtrahend: int or float
    :return: float
    """
    args = list(_convert_args_to_decimal(minuend, subtrahend))
    return float(args[0]-args[1])


def precision_multiply(*args):
    """
    Multiplication operation with minimized floating point error. Implementation based on standard decimal module.
    :param args: number/ floats to be multiplied
    :return: float
    """
    args = _convert_args_to_decimal(*args)
    return float(reduce(operator.mul, args, 1))


def precision_divide(dividend, divisor):
    """
    Division operation with minimized floating point error. Implementation based on standard decimal module.
    :param dividend: int or float
    :param divisor: int or float
    :return: float
    """
    args = list(_convert_args_to_decimal(dividend, divisor))
    return float(args[0] / args[1])


def check_types(var_list, type_list, name_list, ignore=False):
    """
    Checks if var_list[i] is of type_list[i]. Raises TypeError, which mentions name_list[i] in error message
    :param var_list: list of vars,
                     vars to check
    :param type_list: list of types,
                      types to check against
    :param name_list: list of str,
                      names of var_list
    :param ignore: bool,
                   if True, type checking is omitted
    :return: None
    :raises: TypeError: if types do not match up
             IndexError: if input lists are not of same length
    """
    if ignore is True:
        return None

    if not (len(var_list) == len(type_list) == len(name_list)):
        raise IndexError('Lists do not have same length.')

    try:
        for i in range(len(var_list)):
            if type_list[i] == callable:
                if not type_list[i](var_list[i]):
                    raise TypeError('{} must be {}.'.format(name_list[i], type_list[i]))
            else:
                if not type_list[i](var_list[i]) == var_list[i]:
                    raise TypeError('{} must be {}.'.format(name_list[i], type_list[i]))
    except Exception as e:
        # noinspection PyUnboundLocalVariable
        raise TypeError('{} must be {}. Original exception raised as: {}'.format(name_list[i], type_list[i], e))


def find_prefix(prefix_set, target_string):
    """
    Takes a list or set of possible prefixes and checks whether one of them is a valid prefix of target_string.
    Returns the first (!) index of prefix in prefix_set if prefix is a valid prefix of target_string (only on index
    is returned even though multiple prefixes in prefix_set might match, which is the case e.g. for
    ['pre', 'pre_a', 'pre_ab'] as prefix_set and 'pre_abcde' as target_string).
    Returns -1 if no prefix matches.
    :param prefix_set: set or list of strings
    :param target_string: string
    :return: index of first prefix match, otherwise -1
    """
    for i, prefix in enumerate(prefix_set):
        if prefix == target_string[:len(prefix)]:
            return i
    return -1


def is_empty_list(_list):
    """
    Checks if list is empty, also applicable for nested lists
    :param _list: list, nested list
    :return: bool,
             True if list is empty, else False
    """
    if isinstance(_list, list):  # Is a list
        return all(map(is_empty_list, _list))
    return False


def scipy_dist_fit_std(data, scipy_dist):
    """
    Fits a scipy distribution from scipy.stats (only pass in class) and calculates standard deviation
    :param data: 1D list or array
    :param scipy_dist: scipy.stats.distribution_model e.g. scipy.stats.norm (class)
    :return: float
    """
    shape_params = scipy_dist.fit(data, loc=0, scale=1)     # [:-2]
    return scipy_dist.std(*shape_params)


def scipy_dist_fit_ppf(data, alpha, scipy_dist):
    """
    Fits a scipy distribution from scipy.stats (only pass in class) and calculates
    percent point function/ quantile function (inverse of cumulative distribution function) at param:alpha.
    :param data: 1D list or array
    :param alpha: int or float,
                  alpha/ quantile value
    :param scipy_dist: scipy.stats.distribution_model e.g. scipy.stats.norm (class)
    :return: float
    """
    shape_params = scipy_dist.fit(data, loc=0, scale=1)[:-2]
    return scipy_dist.ppf(alpha, *shape_params)


def scipy_dist_fit_mean(data, scipy_dist):
    """
    Fits a scipy distribution from scipy.stats (only pass in class) and calculates mean.
    :param data: 1D list or array
    :param scipy_dist: scipy.stats.distribution_model e.g. scipy.stats.norm (class)
    :return: float
    """
    shape_params = scipy_dist.fit(data, loc=0, scale=1)     # [:-2]
    return scipy_dist.mean(*shape_params)


def kde_pdf(data, x, kernel, bandwidth):
    """
    Fits a kernel density function and calculates probability density function value (relative likelihood/ density)
    at point x (value of random variable)
    :param data: 1D list or array
    :param x: int or float
    :param kernel: str, {‘gaussian’, ‘tophat’, ‘epanechnikov’, ‘exponential’, ‘linear’, ‘cosine’}
                   see sklearn.neighbors.KernelDensity
    :param bandwidth: float,
                      the bandwidth of the kernel
    :return: float
    """
    if type(data) is list:
        data = np.asarray(data)
    if data.ndim < 2:
        data = np.expand_dims(data, 1)

    kde = KernelDensity(kernel=kernel, bandwidth=bandwidth).fit(data)
    return np.exp(kde.score_samples(x))[0]


def kde_ppf(data, alpha, kernel, bandwidth):
    """
    Fits a kernel density function and calculates
    percent point function/ quantile function (inverse of cumulative distribution function) at param:alpha.
    :param data: 1D list or array
    :param alpha: int or float,
                  alpha/ quantile value
    :param kernel: str, {‘gaussian’, ‘tophat’, ‘epanechnikov’, ‘exponential’, ‘linear’, ‘cosine’}
                   see sklearn.neighbors.KernelDensity
    :param bandwidth: float,
                      the bandwidth of the kernel
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
        return np.exp(kde.score_samples(x))[0]

    # noinspection PyTypeChecker
    return quad(integrand, -np.inf, alpha)[0]
