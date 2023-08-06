"""
No memory leak detected: see mem_profile_libmpdec.jpg

Use https://pypi.org/project/memory-profiler/
"""

from trapeza import context as tpz_cxt
tpz_cxt.ARITHMETICS = 'LIBMPDEC'    # 'LIBMPDEC_FAST' (uses ryu dtoa), 'LIBMPDEC' (uses dtoa of Cpython)
from trapeza.arithmetics import arithmetics as arm
from trapeza.arithmetics import libmpdec
import time
import gc


if __name__ == "__main__":
    for i in range(1000000):
        a = arm.py_libmpdec_add(1.1, 2.2)

    gc.collect()
    time.sleep(5)

    libmpdec.mem_test_add()
