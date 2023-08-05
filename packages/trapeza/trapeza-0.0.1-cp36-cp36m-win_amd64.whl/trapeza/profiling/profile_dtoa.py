"""
Elapsed time - dtoa_emyg: 0.3218841
Elapsed time - dtoa_ryu: 0.27834670000000006
Elapsed time - dtoa cpython: 1.4363251
Elapsed time - python str(): 1.3757834  # out-performance over cpython might be misleading due to conversion advantage
"""

import time

from trapeza.arithmetics import dtoa


if __name__ == "__main__":
    x = [1.11111 * i for i in range(1, 1000000)]
    x.extend(x)

    start_time = time.perf_counter()
    for x_i in x:
        dtoa.py_dtoa_emyg(x_i)
    end_time = time.perf_counter()
    print('Elapsed time - dtoa_emyg: {}'.format(end_time - start_time))

    start_time = time.perf_counter()
    for x_i in x:
        dtoa.py_dtoa_ryu(x_i)
    end_time = time.perf_counter()
    print('Elapsed time - dtoa_ryu: {}'.format(end_time - start_time))

    start_time = time.perf_counter()
    for x_i in x:
        dtoa.py_dtoa_cpython(x_i)
    end_time = time.perf_counter()
    print('Elapsed time - dtoa cpython: {}'.format(end_time - start_time))

    start_time = time.perf_counter()
    for x_i in x:
        str(x_i)
    end_time = time.perf_counter()
    print('Elapsed time - python str(): {}'.format(end_time - start_time))
