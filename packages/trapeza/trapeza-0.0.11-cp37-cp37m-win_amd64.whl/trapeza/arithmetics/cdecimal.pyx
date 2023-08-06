#################################################################################
# thin wrapper for Python's decimal.Decimal such that it's callable from cython #
#################################################################################
# - we use Python's double-to-string conversion routine to be sure that double
#   gets converted exactly as we intended
# - decimal.Decimal takes in a Python str object, so it makes no sense to pass
#   a pure C char string, as this would be converted to a Python object anyway

from libc.stdlib cimport strtod
import decimal
from trapeza import context as tpz_ctx
from trapeza.arithmetics.cdecimal cimport c_op


# set rounding method of global context
cdef RND_METHOD = None
if tpz_ctx.ROUNDING == 'ROUND_CEILING':
    RND_METHOD = decimal.ROUND_CEILING
elif tpz_ctx.ROUNDING == 'ROUND_FLOOR':
    RND_METHOD = decimal.ROUND_FLOOR
elif tpz_ctx.ROUNDING == 'ROUND_HALF_EVEN':
    RND_METHOD = decimal.ROUND_HALF_EVEN
elif tpz_ctx.ROUNDING == 'ROUND_HALF_TOWARDS_ZERO':
    RND_METHOD = decimal.ROUND_HALF_DOWN
elif tpz_ctx.ROUNDING == 'ROUND_HALF_AWAY_FROM_ZERO':
    RND_METHOD = decimal.ROUND_HALF_UP
elif tpz_ctx.ROUNDING == 'ROUND_UP':
    RND_METHOD = decimal.ROUND_UP
elif tpz_ctx.ROUNDING == 'ROUND_DOWN':
    RND_METHOD = decimal.ROUND_DOWN
elif tpz_ctx.ROUNDING == 'ROUND_05UP':
    RND_METHOD = decimal.ROUND_05UP
else:
    # default: round half even
    RND_METHOD = decimal.ROUND_HALF_EVEN


# init and set context to specific precision and rounding method
cdef ctx = decimal.Context(prec=tpz_ctx.ARBITRARY_DECIMAL_PRECISION, rounding=RND_METHOD)
decimal.setcontext(ctx)

# get quantization
cdef QUANT_SIZE
if tpz_ctx.ARBITRARY_QUANTIZE_SIZE is not None:
    QUANT_SIZE = decimal.Decimal('0.{}1'.format('0' * (tpz_ctx.ARBITRARY_QUANTIZE_SIZE -1)), ctx)


# noinspection PyTypeChecker,PyPep8Naming
cdef double c_add(double d_1, double d_2):
    """
    Arbitrary precision addition using Python's decimal module
    :param d_1: double
    :param d_2: double
    :return: double
    """
    cdef D_1 = decimal.Decimal(str(d_1), ctx)
    cdef D_2 = decimal.Decimal(str(d_2), ctx)
    D_2 = D_1 + D_2
    cdef double ret = strtod(D_2.to_eng_string().encode(), NULL)
    return ret


# noinspection PyTypeChecker,PyPep8Naming
cdef double c_sub(double d_1, double d_2):
    """
    Arbitrary precision subtraction using Python's decimal module
    :param d_1: double
    :param d_2: double
    :return: double
    """
    cdef D_1 = decimal.Decimal(str(d_1), ctx)
    cdef D_2 = decimal.Decimal(str(d_2), ctx)
    D_2 = D_1 - D_2
    cdef double ret = strtod(D_2.to_eng_string().encode(), NULL)
    return ret


# noinspection PyTypeChecker,PyPep8Naming
cdef double c_i_mul(double d_1, double d_2):
    """
    Arbitrary precision multiplication using Python's decimal module
    :param d_1: double
    :param d_2: double
    :return: double 
    """
    cdef D_1 = decimal.Decimal(str(d_1), ctx)
    cdef D_2 = decimal.Decimal(str(d_2), ctx)
    D_2 = D_1 * D_2
    cdef double ret = strtod(D_2.to_eng_string().encode(), NULL)
    return ret


# noinspection PyTypeChecker,PyPep8Naming
cdef double c_q_mul(double d_1, double d_2):
    """
    Arbitrary precision multiplication using Python's decimal module. Additionally, result is quantized to 
    trapeza.context.ARBITRARY_QUANTIZE_SIZE which prevents precision inflation during multiplication.
    :param d_1: double
    :param d_2: double
    :return: double 
    """
    cdef D_1 = decimal.Decimal(str(d_1), ctx)
    cdef D_2 = decimal.Decimal(str(d_2), ctx)
    D_2 = D_1 * D_2
    D_2 = D_2.quantize(QUANT_SIZE, rounding=RND_METHOD, context=ctx)
    cdef double ret = strtod(D_2.to_eng_string().encode(), NULL)
    return ret


# noinspection PyTypeChecker,PyPep8Naming
cdef double c_i_div(double d_1, double d_2):
    """
    Arbitrary precision division using Python's decimal module
    :param d_1: double
    :param d_2: double
    :return: double 
    """
    cdef D_1 = decimal.Decimal(str(d_1), ctx)
    cdef D_2 = decimal.Decimal(str(d_2), ctx)
    D_2 = D_1 / D_2
    cdef double ret = strtod(D_2.to_eng_string().encode(), NULL)
    return ret


# noinspection PyTypeChecker,PyPep8Naming
cdef double c_q_div(double d_1, double d_2):
    """
    Arbitrary precision division using Python's decimal module. Additionally, result is quantized to 
    trapeza.context.ARBITRARY_QUANTIZE_SIZE which prevents precision inflation during division.
    :param d_1: double
    :param d_2: double
    :return: double  
    """
    cdef D_1 = decimal.Decimal(str(d_1), ctx)
    cdef D_2 = decimal.Decimal(str(d_2), ctx)
    D_2 = D_1 / D_2
    D_2 = D_2.quantize(QUANT_SIZE, rounding=RND_METHOD, context=ctx)
    cdef double ret = strtod(D_2.to_eng_string().encode(), NULL)
    return ret


# assign proper mul and div operation in accordance to quantization scheme
cdef c_op c_mul, c_div
if isinstance(tpz_ctx.ARBITRARY_QUANTIZE_SIZE, int):
    c_mul = c_q_mul
    c_div = c_q_div
elif tpz_ctx.ARBITRARY_QUANTIZE_SIZE is None:
    c_mul = c_i_mul
    c_div = c_i_div
else:
    raise NotImplementedError('trapeza.context.ARBITRARY_QUANTIZE_SIZE must be None or int.')
