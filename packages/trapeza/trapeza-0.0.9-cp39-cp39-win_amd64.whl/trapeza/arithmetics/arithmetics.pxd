ctypedef double (*c_precision_t)(double, double)
cdef c_precision_t c_precision_add
cdef c_precision_t c_precision_subtract
cdef c_precision_t c_precision_multiply
cdef c_precision_t c_precision_divide


# interface for unit testing
cpdef py_libmpdec_add(double d_1, double d_2)
cpdef py_libmpdec_sub(double d_1, double d_2)
cpdef py_libmpdec_mul(double d_1, double d_2)
cpdef py_libmpdec_div(double d_1, double d_2)

cpdef py_cfloat_add(double d_1, double d_2)
cpdef py_cfloat_sub(double d_1, double d_2)
cpdef py_cfloat_mul(double d_1, double d_2)
cpdef py_cfloat_div(double d_1, double d_2)

cpdef py_cdecimal_add(double d_1, double d_2)
cpdef py_cdecimal_sub(double d_1, double d_2)
cpdef py_cdecimal_mul(double d_1, double d_2)
cpdef py_cdecimal_div(double d_1, double d_2)
