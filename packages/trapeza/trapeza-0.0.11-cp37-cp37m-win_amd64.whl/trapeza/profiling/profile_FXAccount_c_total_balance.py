"""
Profiling of c_total_balance() method of cFXAccount in trapeza.account.fx_account, which is wrapped by FXAccount.
Due to the implementation via Cython, line_profile cannot display the source code of c_total_balance(), such that
one has to look it up manually in source file to compare timings to corresponding lines of code.

There doesn't seem to be much of a further optimization potential except a complete re-design of the entire internal
logic, which doesn't seem to make much sense.

fx_account.pyx must be compiled with compiler directive:
# cython: profile=True
# cython: linetrace=True
# cython: binding=True
# distutils: define_macros=CYTHON_TRACE_NOGIL=1
"""

import line_profiler

from trapeza.account import FXAccount


def profile_function(_acc):
    for _ in range(100000):
        _acc.c_total_balance({(b'EUR', b'BTC'): 1.2, (b'EUR', b'ETH'): 1.2, (b'EUR', b'ETC'): 1.2}, b'EUR')


if __name__ == '__main__':
    acc = FXAccount('EUR')
    acc._c_depot = {b'EUR': 100, b'BTC': 100, b'ETH': 100, b'ETC': 100}

    prof = line_profiler.LineProfiler(acc.c_total_balance)
    prof.runctx('profile_function(acc)', globals(), locals())
    prof.print_stats()
