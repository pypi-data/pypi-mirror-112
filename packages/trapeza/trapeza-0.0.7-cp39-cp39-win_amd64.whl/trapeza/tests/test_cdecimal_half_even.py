from decimal import ROUND_HALF_EVEN, Context, setcontext

from trapeza import context as tpz_cxt
tpz_cxt.ARITHMETICS = 'DECIMAL'
tpz_cxt.ROUNDING = 'ROUND_HALF_EVEN'
tpz_cxt.ARBITRARY_DECIMAL_PRECISION = 28    # set to same as Python's decimal default precision
tpz_cxt.ARBITRARY_QUANTIZE_SIZE = 10    # we do not test against None, because even Python's decimal is bogus then
from trapeza.arithmetics import arithmetics as arm
# IT'S IMPORTANT TO IMPORT CONTEXT FIRST
from trapeza.tests.setup_test import subroutine_add_accum, subroutine_sub_accum, \
    subroutine_mul_accum, subroutine_div_accum


dec_cxt = Context(prec=28, rounding=ROUND_HALF_EVEN)
setcontext(dec_cxt)


def test_libmpdec_add():
    assert arm.py_libmpdec_add(1.000001, 2.000002) == 3.000003
    assert arm.py_libmpdec_add(1.11111, 2.22222) == 3.33333
    assert arm.py_libmpdec_add(1, 2) == 3
    assert arm.py_libmpdec_add(1.111111, 2.22222) == 3.333331
    assert arm.py_libmpdec_add(1.0000001, 2.0000002) == 3.0000003
    assert arm.py_libmpdec_add(1.0000111, 2.000022) == 3.0000331
    assert arm.py_libmpdec_add(1.0000001, 2.2) == 3.2000001

    # prone to false rounding
    assert arm.py_libmpdec_add(0.56, 0.45) == 1.01

    # check for error accumulation
    subroutine_add_accum(arm.py_libmpdec_add, dec_cxt)


def test_libmpdec_sub():
    assert arm.py_libmpdec_sub(3.000003, 2.000002) == 1.000001
    assert arm.py_libmpdec_sub(3.00003, 2.00002) == 1.00001
    assert arm.py_libmpdec_sub(3, 2) == 1
    assert arm.py_libmpdec_sub(3.000031, 2.00002) == 1.000011
    assert arm.py_libmpdec_sub(3.0000003, 2.0000002) == 1.0000001
    assert arm.py_libmpdec_sub(3.0000031, 2.000002) == 1.0000011
    assert arm.py_libmpdec_sub(3.0000001, 2.2) == 0.8000001

    # prone to false rounding
    assert arm.py_libmpdec_sub(1.01, 0.45) == 0.56

    # check for error accumulation
    subroutine_sub_accum(arm.py_libmpdec_sub, dec_cxt)


def test_libmpdec_mul():
    assert arm.py_libmpdec_mul(1.011007, 2.021107) == 2.0433533247
    # todo: documentation of compliant bogus behavior when QUANT set to None
    assert arm.py_libmpdec_mul(1.00001, 3.00001) == 3.0000400001    # this is bogus but conforms with decimal.Decimal
    assert arm.py_libmpdec_mul(1, 2) == 2
    assert arm.py_libmpdec_mul(1.111171, 2.22231) == 2.469366425
    assert arm.py_libmpdec_mul(1.0000001, 2.0000002) == 2.0000004
    assert arm.py_libmpdec_mul(1.0000007, 2.000007) == 2.0000084
    assert arm.py_libmpdec_mul(1.0071373, 2.07137) == 2.0861539891

    # prone to false rounding
    assert arm.py_libmpdec_mul(0.56, 0.45) == 0.252

    # check for error accumulation - we assume inputs have at max same precision as fixed point
    subroutine_mul_accum(arm.py_libmpdec_mul, dec_cxt, tpz_cxt.ARBITRARY_QUANTIZE_SIZE)


def test_libmpdec_div():
    assert arm.py_libmpdec_div(2.043353324749, 2.021107) == 1.011007
    # todo: documentation of compliant bogus behavior when QUANT set to None
    assert arm.py_libmpdec_div(3.0000400001, 3.00001) == 1.00001  # this is bogus but conforms with decimal.Decimal
    assert arm.py_libmpdec_div(2, 1) == 2
    assert arm.py_libmpdec_div(2.46936642501, 2.22231) == 1.111171
    assert arm.py_libmpdec_div(2.0000004, 2.0000002) == 1.0000001
    assert arm.py_libmpdec_div(2.000008400005, 2.000007) == 1.0000007
    assert arm.py_libmpdec_div(2.086153989101, 2.07137) == 1.0071373

    # prone to false rounding
    assert arm.py_libmpdec_div(0.252, 0.45) == 0.56

    # check for error accumulation - we assume inputs have at max same precision as fixed point
    subroutine_div_accum(arm.py_libmpdec_div, dec_cxt, tpz_cxt.ARBITRARY_QUANTIZE_SIZE)
