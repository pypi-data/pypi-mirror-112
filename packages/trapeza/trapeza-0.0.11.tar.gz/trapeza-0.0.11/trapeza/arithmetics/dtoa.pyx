####################################################################
# Wraps ryu C implementation and Cpython double_to_string function #
# emyg_dtoa is not used any more!                                  #
####################################################################

from libc.string cimport strcpy
from cpython.mem cimport PyMem_Free

cdef extern from "emyg_dtoa.c":
    void emyg_dtoa(double value, char*buffer)

cdef extern from "ryu.h":
    void d2s_buffered(double f, char* result)

cdef extern from "Python.h":
    # noinspection PyPep8Naming
    char* PyOS_double_to_string(double val, char format_code, int precision, int flags, int *_type)


cdef void dtoa_emyg(double d, char* buffer):
    """
    THIS IMPLEMENTATION IS NOT USED ANYMORE!
    Converts double to string using the very efficient emyg dtoa algorithm. Wrapper around emyg_dtoa.c.
    :param d: double
    :param buffer: char*
    :return: void
    """
    # todo: documentation: at max 15 to 17 decimal places, when 0.x then 17 decimal places
    if d == 0:
        buffer[0] = b'0'
        return
    emyg_dtoa(d, buffer)


cdef void dtoa_ryu(double d, char* buffer):
    """
    Converts double to string using the RYU algorithm, which is currently one of the fastest dtoa algorithms.
    Wrapper around ryu.h.
    :param d: double
    :param buffer: char*
    :return: void
    """
    d2s_buffered(d, buffer)


# noinspection PyTypeChecker
cdef void dtoa_cpython(double d, char* buffer):
    """
    Converts double to string using the same methods as Python does.
    Frees intermediate char* via PyMem_Free() internally as the Python Docs recommend this regarding 
    PyOS_double_to_string().
    :param d: double
    :param buffer: char*
    :return: void
    """
    cdef char* s = PyOS_double_to_string(d, b'r', 0, 0, NULL)
    strcpy(buffer, s)
    PyMem_Free(s)


# noinspection PyTypeChecker
cpdef py_dtoa_cpython(double d):
    """
    Potential memory leak! Not profiled yet.
    Only for testing.
    :param d: double
    :return: str
    """
    cdef char[255] buffer
    dtoa_cpython(d, buffer)
    return buffer.decode()


# noinspection PyTypeChecker
cpdef py_dtoa_ryu(double d):
    """
    Used as str() replacement in trapeza.utils. Previous frepr package was used. But frepr is broken for Python 3.9.
    :param d: double
    :return: str
    """
    cdef char[255] buffer
    dtoa_ryu(d, buffer)
    return buffer.decode()


# noinspection PyTypeChecker
cpdef py_dtoa_emyg(double d):
    """
    Potential memory leak! Not profiled yet.
    Only for testing.
    :param d: double
    :return: str
    """
    cdef char[255] buffer
    dtoa_emyg(d, buffer)
    return buffer.decode()
