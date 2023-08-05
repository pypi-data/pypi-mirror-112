"""
Only testing against round trip condition when converting float/ double to string and back.
The actual string representation might differ from the float input, which is especially the case for emyg_dtoa.
For using Python's decimal module, this test is not sufficient, because emyg_dtoa always gets interpreted as exact,
which might lead to numerical errors.
"""
import math
from trapeza.arithmetics.dtoa import py_dtoa_emyg, py_dtoa_cpython, py_dtoa_ryu


def test_dtoa_emyg():
    assert type(py_dtoa_emyg(1.2)) == str

    assert float(py_dtoa_emyg(1.2)) == 1.2
    assert float(py_dtoa_emyg(-1.2)) == -1.2
    assert float(py_dtoa_emyg(10)) == 10
    assert float(py_dtoa_emyg(-10)) == -10
    assert float(py_dtoa_emyg(-1000.123)) == -1000.123
    assert float(py_dtoa_emyg(1000000000000.123)) == 1000000000000.123
    assert float(py_dtoa_emyg(1000.12345678)) == 1000.12345678
    assert float(py_dtoa_emyg(0.56)) == 0.56
    assert float(py_dtoa_emyg(-0.56)) == -0.56

    x = [1.11111 * i for i in range(1, 1000000)]
    x.extend(x)
    for x_i in x:
        assert float(str(x_i)) == float(py_dtoa_emyg(x_i))


def test_dtoa_cpython():
    assert type(py_dtoa_cpython(1.2)) == str

    assert float(py_dtoa_cpython(1.2)) == 1.2
    assert float(py_dtoa_cpython(-1.2)) == -1.2
    assert float(py_dtoa_cpython(10)) == 10
    assert float(py_dtoa_cpython(-10)) == -10
    assert float(py_dtoa_cpython(-1000.123)) == -1000.123
    assert float(py_dtoa_cpython(1000000000000.123)) == 1000000000000.123
    assert float(py_dtoa_cpython(1000.12345678)) == 1000.12345678
    assert float(py_dtoa_cpython(0.56)) == 0.56
    assert float(py_dtoa_cpython(-0.56)) == -0.56

    x = [1.11111 * i for i in range(1, 1000000)]
    x.extend(x)
    for x_i in x:
        x_i = math.trunc(x_i * 1000000) / 1000000
        assert float(str(x_i)) == float(py_dtoa_cpython(x_i))


def test_dtoa_ryu():
    assert type(py_dtoa_ryu(1.2)) == str

    assert float(py_dtoa_ryu(1.2)) == 1.2
    assert float(py_dtoa_ryu(-1.2)) == -1.2
    assert float(py_dtoa_ryu(10)) == 10
    assert float(py_dtoa_ryu(-10)) == -10
    assert float(py_dtoa_ryu(-1000.123)) == -1000.123
    assert float(py_dtoa_ryu(1000000000000.123)) == 1000000000000.123
    assert float(py_dtoa_ryu(1000.12345678)) == 1000.12345678
    assert float(py_dtoa_ryu(0.56)) == 0.56
    assert float(py_dtoa_ryu(-0.56)) == -0.56

    x = [1.11111 * i for i in range(1, 1000000)]
    x.extend(x)
    for x_i in x:
        x_i = math.trunc(x_i * 1000000) / 1000000
        assert float(str(x_i)) == float(py_dtoa_ryu(x_i))
