"""
No memory leak detected: see mem_profile_acc.jpg

Use https://pypi.org/project/memory-profiler/
"""
import time
import gc
from trapeza import context as tpz_cxt
tpz_cxt.ARITHMETICS = 'LIBMPDEC_FAST'    # 'LIBMPDEC_FAST' (uses ryu dtoa), 'LIBMPDEC' (uses dtoa of Cpython)
from trapeza.account import FXAccount


if __name__ == "__main__":
    acc = FXAccount('EUR')

    for _ in range(30):
        acc_alt = FXAccount('BTC')

    del acc_alt

    time.sleep(3)

    for _ in range(1000):
        acc.deposit(100, 'EUR')
        # noinspection PyTypeChecker
        acc.sell(100, 1, 'EUR', 'BTC')
        # noinspection PyTypeChecker
        acc.buy(100, 1, 'EUR', 'BTC')
        acc.withdraw(100, 'EUR')
        gc.collect()

    del acc
    gc.collect()

    for _ in range(5):
        time.sleep(0.5)

    gc.collect()
