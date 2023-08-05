"""
No memory leak detected: see mem_profile_py_dtoa_ryu.jpg

Use https://pypi.org/project/memory-profiler/
"""

from trapeza.arithmetics.dtoa import py_dtoa_ryu
import time
import gc


if __name__ == "__main__":
    a = list()
    for i in range(1_000_000):
        a.append(i + i/5 + 0.00001)

    gc.collect()
    time.sleep(5)

    for n in a:
        c = py_dtoa_ryu(n)
