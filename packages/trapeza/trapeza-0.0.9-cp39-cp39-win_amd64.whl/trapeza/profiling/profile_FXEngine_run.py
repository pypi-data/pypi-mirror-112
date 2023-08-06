"""
Timing: ca. 4.84
"""
import timeit

from trapeza import context as tpz_cxt
tpz_cxt.ARITHMETICS = 'LIBMPDEC_FAST'    # LIBMPDEC or LIBMPDEC_FAST

from trapeza.engine import FXEngine
from trapeza.tests.setup_test import setup_large_strategies, setup_large_data


# noinspection DuplicatedCode
if __name__ == '__main__':
    strats = setup_large_strategies()
    engine = FXEngine('genesis', strats, '../tests/__test_cache__', ignore_type_checking=True, n_jobs=-1)
    data = setup_large_data()
    len_data = len(data[list(data.keys())[0]])

    win_diff = 5

    t_start = timeit.default_timer()
    for _ in range(10):
        # timings before any optimization 24.1903497, 23.073752000000002, 21.776832499999998
        engine.run(data, 'EUR', None, len_data - win_diff - 10, len_data - 10, 10, True)
    t_end = timeit.default_timer()
    print(t_end - t_start)
