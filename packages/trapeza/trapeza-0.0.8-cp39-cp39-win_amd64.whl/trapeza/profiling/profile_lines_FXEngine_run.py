"""
There doesn't seem to be much of a further optimization potential except a complete re-design of the entire internal
logic, which doesn't seem to make much sense.

fx_strategy.pyx must be compiled with compiler directive:
# cython: profile=True
# cython: linetrace=True
# cython: binding=True
# distutils: define_macros=CYTHON_TRACE_NOGIL=1
"""
import cProfile
import pstats

from trapeza import context as tpz_cxt
tpz_cxt.ARITHMETICS = 'LIBMPDEC_FAST'    # LIBMPDEC or LIBMPDEC_FAST

from trapeza.engine import FXEngine
from trapeza.tests.setup_test import setup_large_strategies, setup_large_data


def profiling_func():
    strats = setup_large_strategies()
    engine = FXEngine('genesis', strats, '../tests/__test_cache__', ignore_type_checking=True, n_jobs=1)
    data = setup_large_data()
    len_data = len(data[list(data.keys())[0]])

    win_diff = 5

    for _ in range(10):
        engine.run(data, 'EUR', None, len_data - win_diff - 10, len_data - 10, 10, True)


if __name__ == '__main__':
    cProfile.runctx('profiling_func()', globals(), locals(), 'Profile.prof')    # 24.022
    s = pstats.Stats('Profile.prof')
    s.strip_dirs().sort_stats('time').print_stats()
