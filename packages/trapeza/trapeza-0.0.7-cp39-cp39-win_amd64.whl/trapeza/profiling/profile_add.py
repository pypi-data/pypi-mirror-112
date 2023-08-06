"""
LIBMPDEC_FAST:
    number of additions: 100000
    Elapsed time - python addition:     0.010552899999999976
    Elapsed time - cfloat_add:          0.030007000000000006
    Elapsed time - python Decimal:      0.13471529999999998
    Elapsed time - libmpdec_fast_add:   0.1364198
    Elapsed time - cdecimal_add:        0.21239

LIBMPDEC:
    number of additions: 100000
    Elapsed time - python addition:     0.010946000000000011
    Elapsed time - cfloat_add:          0.03174890000000008
    Elapsed time - python Decimal:      0.1376526
    Elapsed time - cdecimal_add:        0.23626409999999998
    Elapsed time - libmpdec_add:        0.4931805


Results might be misleading because cython implementations have conversion overhead from C data type to Python object.
"""

from trapeza import context as tpz_cxt
tpz_cxt.ARITHMETICS = 'LIBMPDEC'    # LIBMPDEC or LIBMPDEC_FAST
import time
import math
from decimal import Decimal, ROUND_HALF_UP
import numpy as np

from trapeza.arithmetics import arithmetics as arm


if __name__ == "__main__":
    nr_digits_input = 4
    scaling = math.pow(10, nr_digits_input)
    adds = []
    for _ in range(100000):
        rand = math.trunc(np.random.random_sample() * scaling) / scaling
        rand = rand + np.random.randint(0, 100, 1)[0]
        rand *= np.random.choice([1, -1], 1, p=[0.7, 0.3])[0]
        rand = Decimal(str(rand)).quantize(Decimal('1.{}'.format('0' * nr_digits_input)), ROUND_HALF_UP)
        adds.append(rand)
    print('number of additions: {}'.format(len(adds)))

    a = 0
    start_time = time.perf_counter()
    for i in adds:
        a = arm.py_libmpdec_add(a, i)
    end_time = time.perf_counter()
    print('Elapsed time - libmpdec_add: {}'.format(end_time-start_time))

    a = 0
    start_time = time.perf_counter()
    for i in adds:
        a = arm.py_cdecimal_add(a, i)
    end_time = time.perf_counter()
    print('Elapsed time - cdecimal_add: {}'.format(end_time - start_time))

    a = 0
    start_time = time.perf_counter()
    for i in adds:
        a = arm.py_cfloat_add(a, i)
    end_time = time.perf_counter()
    print('Elapsed time - cfloat_add: {}'.format(end_time - start_time))

    a = 0
    start_time = time.perf_counter()
    for i in adds:
        a += i
    end_time = time.perf_counter()
    print('Elapsed time - python addition: {}'.format(end_time - start_time))

    a = Decimal('0')
    start_time = time.perf_counter()
    for i in adds:
        _ = Decimal(str(1000.1))
        a += Decimal(str(i))
        _ = float(a)
    end_time = time.perf_counter()
    print('Elapsed time - python Decimal: {}'.format(end_time - start_time))
