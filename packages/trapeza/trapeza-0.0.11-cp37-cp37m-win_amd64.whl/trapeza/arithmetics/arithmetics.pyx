###########################################################################
# Wraps cdecimal.pyx, cfloat.pyx and libmpdec.pys into a common interface #
###########################################################################

# arithmetic methods:
#   Python native float arithmetics & PyOS_double_to_string                 (FLOAT)
#   Python decimal.Decimal arbitrary arithmetics & PyOS_double_to_string    (DECIMAL)
#   libmpdec arbitrary precision arithmetics & ryu dtoa                     (LIBMPDEC_FAST)
#   libmpdec arbitrary precision arithmetics & PyOS_double_to_string        (LIBMPDEC)
# todo: implement further arithmetic methods (e.g. own fixed point implementation cfpm, work in progress)

# rounding methods:
#   ceiling
#   floor
#   half even
#   half away from zero
#   half towards zero
# additionally and only for libmpdec and Decimal
#   down
#   up
#   half up
#   05up

import warnings

IF USE_LIBMPDEC:
    from trapeza.arithmetics cimport libmpdec as _libmpdec
ELSE:
    from trapeza.arithmetics cimport cdecimal as _libmpdec
    warnings.warn('LIBMPDEC and LIBMPDEC_FAST not available. Falling back to DECIMAL. '
                  'Consider compiling package from source.')
from trapeza.arithmetics cimport cdecimal
from trapeza.arithmetics cimport cfloat
from trapeza import context as tpz_ctx


cdef c_precision_t c_precision_add
cdef c_precision_t c_precision_subtract
cdef c_precision_t c_precision_multiply
cdef c_precision_t c_precision_divide


# read in arithmetics method
if tpz_ctx.ARITHMETICS == 'FLOAT':
    c_precision_add = cfloat.c_add
    c_precision_subtract = cfloat.c_sub
    c_precision_multiply = cfloat.c_mul
    c_precision_divide = cfloat.c_div
elif tpz_ctx.ARITHMETICS == 'DECIMAL':
    c_precision_add = cdecimal.c_add
    c_precision_subtract = cdecimal.c_sub
    c_precision_multiply = cdecimal.c_mul
    c_precision_divide = cdecimal.c_div
elif tpz_ctx.ARITHMETICS == 'LIBMPDEC' or tpz_ctx.ARITHMETICS == 'LIBMPDEC_FAST':
    # distinguishing between LIBMPDEC and LIBMPDEC_FAST is done in libmpdec.pyx
    c_precision_add = _libmpdec.c_add
    c_precision_subtract = _libmpdec.c_sub
    c_precision_multiply = _libmpdec.c_mul
    c_precision_divide = _libmpdec.c_div
else:
    raise NotImplementedError('Currently only the following arithmetic modes for trapeza.context.ARITHMETICS are '
                              'supported: {"FLOAT", "DECIMAL", "LIBMPDEC", "LIBMPDEC_FAST"}.')


# check rounding method
# todo: Currently we only have decimal.Decimal and libmpdec, which both support all rounding methods such that we do
#   do not have to distinguish between backends if we check rounding method.
#   If we add more backends, we might have to change this part to be more specific for each backend
if tpz_ctx.ROUNDING not in {'ROUND_CEILING', 'ROUND_FLOOR', 'ROUND_HALF_EVEN', 'ROUND_HALF_TOWARDS_ZERO',
                                      'ROUND_HALF_AWAY_FROM_ZERO', 'ROUND_UP', 'ROUND_DOWN', 'ROUND_05UP'}:
    raise NotImplementedError('Currently only the following rounding methods are supported for '
                              'ARITHMETICS={"DECIMAL", "LIBMPDEC", "LIBMPDEC_FAST"}: '
                              '{"ROUND_CEILING", "ROUND_FLOOR", "ROUND_HALF_EVEN", "ROUND_HALF_TOWARDS_ZERO",'
                              ' "ROUND_HALF_AWAY_FROM_ZERO", "ROUND_UP", "ROUND_DOWN", "ROUND_05UP"}')

# precision does not need to be checked separately

# todo: fixed point size checking not implemented yet because fixed point arithmetic is not implemented yet

# expose interface for unit testing
cpdef py_libmpdec_add(double d_1, double d_2):
    """Interface for unit testing"""
    return _libmpdec.c_add(d_1, d_2)

cpdef py_libmpdec_sub(double d_1, double d_2):
    """Interface for unit testing"""
    return _libmpdec.c_sub(d_1, d_2)

cpdef py_libmpdec_mul(double d_1, double d_2):
    """Interface for unit testing"""
    return _libmpdec.c_mul(d_1, d_2)

cpdef py_libmpdec_div(double d_1, double d_2):
    """Interface for unit testing"""
    return _libmpdec.c_div(d_1, d_2)


cpdef py_cfloat_add(double d_1, double d_2):
    """Interface for unit testing"""
    return cfloat.c_add(d_1, d_2)

cpdef py_cfloat_sub(double d_1, double d_2):
    """Interface for unit testing"""
    return cfloat.c_sub(d_1, d_2)

cpdef py_cfloat_mul(double d_1, double d_2):
    """Interface for unit testing"""
    return cfloat.c_mul(d_1, d_2)

cpdef py_cfloat_div(double d_1, double d_2):
    """Interface for unit testing"""
    return cfloat.c_div(d_1, d_2)


cpdef py_cdecimal_add(double d_1, double d_2):
    """Interface for unit testing"""
    return cdecimal.c_add(d_1, d_2)

cpdef py_cdecimal_sub(double d_1, double d_2):
    """Interface for unit testing"""
    return cdecimal.c_sub(d_1, d_2)

cpdef py_cdecimal_mul(double d_1, double d_2):
    """Interface for unit testing"""
    return cdecimal.c_mul(d_1, d_2)

cpdef py_cdecimal_div(double d_1, double d_2):
    """Interface for unit testing"""
    return cdecimal.c_div(d_1, d_2)
