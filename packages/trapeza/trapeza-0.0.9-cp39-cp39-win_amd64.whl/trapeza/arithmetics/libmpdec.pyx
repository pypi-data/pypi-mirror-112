##################################
# wrapper for libmpdec C-library #
##################################
# references:
#   https://github.com/python/cpython/blob/63298930fb531ba2bb4f23bc3b915dbf1e17e9e1/Modules/_decimal/_decimal.c
#   https://www.bytereef.org/mpdecimal/doc/libmpdec/index.html
from libc.stdint cimport int64_t, uint32_t
from libc.stdlib cimport strtod
from trapeza import context as tpz_ctx
from trapeza.arithmetics.dtoa cimport dtoa_ryu, dtoa_cpython, dtoa_t
from trapeza.arithmetics.libmpdec cimport c_op

cdef extern from "mpdecimal.h":
    ctypedef int64_t mpd_ssize_t

    ctypedef struct mpd_context_t:
        mpd_ssize_t prec
        int round
        uint32_t traps      # status events that should be trapped

    ctypedef struct mpd_t:
        pass

    cdef enum:
        MPD_ROUND_UP,  # /* round away from 0               */
        MPD_ROUND_DOWN,  # /* round toward 0 (truncate)       */
        MPD_ROUND_CEILING,  # /* round toward +infinity          */
        MPD_ROUND_FLOOR,  # /* round toward -infinity          */
        MPD_ROUND_HALF_UP,  # /* 0.5 is rounded up               */
        MPD_ROUND_HALF_DOWN,  # /* 0.5 is rounded down             */
        MPD_ROUND_HALF_EVEN,  # /* 0.5 is rounded to even          */
        MPD_ROUND_05UP,  # /* round zero or five away from 0  */
        MPD_ROUND_TRUNC,  # /* truncate, but set infinity      */

    cdef enum:
        MPD_Conversion_syntax = 0x00000002U
        MPD_Division_impossible = 0x00000008U
        MPD_Division_undefined = 0x00000010U
        MPD_Fpu_error = 0x00000020U
        MPD_Invalid_context = 0x00000080U
        MPD_Invalid_operation = 0x00000100U
        MPD_Malloc_error = 0x00000200U
        MPD_Division_by_zero = 0x00000004U
        MPD_Overflow = 0x00000800U
        MPD_Underflow = 0x00004000U

        MPD_IEEE_Invalid_operation = (MPD_Conversion_syntax | MPD_Division_impossible | MPD_Division_undefined |
                                      MPD_Fpu_error | MPD_Invalid_context | MPD_Invalid_operation | MPD_Malloc_error)

        MPD_Traps = (MPD_IEEE_Invalid_operation | MPD_Division_by_zero | MPD_Overflow | MPD_Underflow)

    void mpd_init(mpd_context_t *ctx, mpd_ssize_t prec)
    mpd_t *mpd_new(mpd_context_t *ctx)
    void mpd_set_string(mpd_t *result, const char *s, mpd_context_t *ctx)
    char *mpd_to_sci(const mpd_t *dec, int fmt)
    void mpd_del(mpd_t *dec)
    void *mpd_free(void *ptr)

    void mpd_add(mpd_t *result, const mpd_t *a, const mpd_t *b, mpd_context_t *ctx)
    void mpd_sub(mpd_t *result, const mpd_t *a, const mpd_t *b, mpd_context_t *ctx)
    void mpd_mul(mpd_t *result, const mpd_t *a, const mpd_t *b, mpd_context_t *ctx)
    void mpd_div(mpd_t *q, const mpd_t *a, const mpd_t *b, mpd_context_t *ctx)

    void mpd_quantize(mpd_t *result, const mpd_t *a, const mpd_t *b, mpd_context_t *ctx)


# define context
cdef mpd_context_t ctx


# define precision of global context
cdef mpd_ssize_t PREC = tpz_ctx.ARBITRARY_DECIMAL_PRECISION


# init global context
mpd_init(&ctx, PREC)


# set precision of global context, total number of digits in decimal representation (total number including integral
# and fractional part, this is different then the decimal places after the radix point!)
ctx.prec = PREC


# set rounding method of global context
if tpz_ctx.ROUNDING == 'ROUND_CEILING':
    ctx.round = MPD_ROUND_CEILING
elif tpz_ctx.ROUNDING == 'ROUND_FLOOR':
    ctx.round = MPD_ROUND_FLOOR
elif tpz_ctx.ROUNDING == 'ROUND_HALF_EVEN':
    ctx.round = MPD_ROUND_HALF_EVEN
elif tpz_ctx.ROUNDING == 'ROUND_HALF_TOWARDS_ZERO':
    ctx.round = MPD_ROUND_HALF_DOWN
elif tpz_ctx.ROUNDING == 'ROUND_HALF_AWAY_FROM_ZERO':
    ctx.round = MPD_ROUND_HALF_UP
elif tpz_ctx.ROUNDING == 'ROUND_UP':
    ctx.round = MPD_ROUND_UP
elif tpz_ctx.ROUNDING == 'ROUND_DOWN':
    ctx.round = MPD_ROUND_DOWN
elif tpz_ctx.ROUNDING == 'ROUND_05UP':
    ctx.round = MPD_ROUND_05UP
else:
    # default: round half even
    ctx.round = MPD_ROUND_HALF_EVEN


# use traps for global context
ctx.traps = MPD_Traps


# set dtoa method
cdef dtoa_t dtoa
if tpz_ctx.ARITHMETICS == 'LIBMPDEC_FAST':
    dtoa = dtoa_ryu
elif tpz_ctx.ARITHMETICS == 'LIBMPDEC':
    dtoa = dtoa_cpython
else:
    # default: dtoa method of Cpython which is slower but more precise
    dtoa = dtoa_cpython


# get quantization
cdef mpd_t* QUANT_SIZE
if tpz_ctx.ARBITRARY_QUANTIZE_SIZE is not None:
    QUANT_SIZE = mpd_new(&ctx)
    # noinspection PyTypeChecker
    mpd_set_string(QUANT_SIZE, '0.{}1'.format('0' * (tpz_ctx.ARBITRARY_QUANTIZE_SIZE-1)).encode(), &ctx)


cdef mpd_t* strtodec(const char *s):
    """
    Convert string to mpd_t pointer
    :param s: string
    :return: mpd_t* dec
    """
    cdef mpd_t* dec
    dec = mpd_new(&ctx)
    mpd_set_string(dec, s, &ctx)
    return dec


# noinspection PyTypeChecker
cdef mpd_t* dtodec(double d):
    """
    Convert double to mpd_t pointer:
        First convert double to string
        Second convert string to mpd_t via strtodec
    :param d: double
    :return: mpd_t* dec
    """
    cdef char[255] s
    dtoa(d, s)  # potential memory leak? couldn't find any so far
    cdef mpd_t* dec = strtodec(s)
    return dec


cdef double dectod(mpd_t* dec):
    """
    Converts mpd_t pointer to double and frees memory
    :param dec: mpd_t* dec (pointer)
    :return: double
    """
    cdef char* s = mpd_to_sci(dec, 1)
    cdef double ret = strtod(s, NULL)
    mpd_del(dec)
    mpd_free(s)
    return ret


cdef double c_add(double d_1, double d_2):
    """
    Arbitrary precision add using libmpdec internally.
    :param d_1: double
    :param d_2: double
    :return: double
    """
    cdef mpd_t* dec_1 = dtodec(d_1)
    cdef mpd_t* dec_2 = dtodec(d_2)

    cdef mpd_t* res
    res = mpd_new(&ctx)
    mpd_add(res, dec_1, dec_2, &ctx)

    mpd_del(dec_1)
    mpd_del(dec_2)

    return dectod(res)


cdef double c_sub(double d_1, double d_2):
    """
    Arbitrary precision subtract using libmpdec internally.
    :param d_1: double
    :param d_2: double
    :return: double
    """
    cdef mpd_t* dec_1 = dtodec(d_1)
    cdef mpd_t* dec_2 = dtodec(d_2)

    cdef mpd_t* res
    res = mpd_new(&ctx)
    mpd_sub(res, dec_1, dec_2, &ctx)

    mpd_del(dec_1)
    mpd_del(dec_2)

    return dectod(res)


cdef double c_i_mul(double d_1, double d_2):
    """
    Arbitrary precision multiply using libmpdec internally.
    :param d_1: double
    :param d_2: double
    :return: double
    """
    cdef mpd_t*dec_1 = dtodec(d_1)
    cdef mpd_t*dec_2 = dtodec(d_2)

    cdef mpd_t*res
    res = mpd_new(&ctx)
    mpd_mul(res, dec_1, dec_2, &ctx)

    mpd_del(dec_1)
    mpd_del(dec_2)

    return dectod(res)


cdef double c_q_mul(double d_1, double d_2):
    """
    Arbitrary precision multiply using libmpdec internally. Additionally, result is quantized to 
    trapeza.context.ARBITRARY_QUANTIZE_SIZE which prevents precision inflation during multiplication.
    :param d_1: double
    :param d_2: double
    :return: double
    """
    cdef mpd_t*dec_1 = dtodec(d_1)
    cdef mpd_t*dec_2 = dtodec(d_2)

    cdef mpd_t*res
    res = mpd_new(&ctx)
    mpd_mul(res, dec_1, dec_2, &ctx)
    mpd_quantize(res, res, QUANT_SIZE, &ctx)

    mpd_del(dec_1)
    mpd_del(dec_2)

    return dectod(res)


cdef double c_i_div(double d_1, double d_2):
    """
    Arbitrary precision division using libmpdec internally.
    :param d_1: double
    :param d_2: double
    :return: double
    """
    cdef mpd_t*dec_1 = dtodec(d_1)
    cdef mpd_t*dec_2 = dtodec(d_2)

    cdef mpd_t*res
    res = mpd_new(&ctx)
    mpd_div(res, dec_1, dec_2, &ctx)

    mpd_del(dec_1)
    mpd_del(dec_2)

    return dectod(res)


cdef double c_q_div(double d_1, double d_2):
    """
    Arbitrary precision division using libmpdec internally. Additionally, result is quantized to 
    trapeza.context.ARBITRARY_QUANTIZE_SIZE which prevents precision inflation during division.
    :param d_1: double
    :param d_2: double
    :return: double
    """
    cdef mpd_t*dec_1 = dtodec(d_1)
    cdef mpd_t*dec_2 = dtodec(d_2)

    cdef mpd_t*res
    res = mpd_new(&ctx)
    mpd_div(res, dec_1, dec_2, &ctx)
    mpd_quantize(res, res, QUANT_SIZE, &ctx)

    mpd_del(dec_1)
    mpd_del(dec_2)

    return dectod(res)


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


cpdef py_c_add(double d_1, double d_2):
    """
    For profiling purpose only.
    :param d_1: double
    :param d_2: double
    :return: double
    """
    return c_add(d_1, d_2)


cpdef mem_test_add():
    cdef int i
    for i in range(100000):
        c_add(1.1, 2.2)
