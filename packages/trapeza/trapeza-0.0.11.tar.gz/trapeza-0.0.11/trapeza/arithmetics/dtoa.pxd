cdef void dtoa_emyg(double d, char* buffer)
cdef void dtoa_ryu(double d, char* buffer)
cdef void dtoa_cpython(double d, char* buffer)

ctypedef void (*dtoa_t)(double d, char* buffer)

cpdef py_dtoa_ryu(double d)
