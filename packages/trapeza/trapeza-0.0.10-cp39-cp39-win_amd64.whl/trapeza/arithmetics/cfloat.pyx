#############################################################################
# thin wrapper for double operations such that they're callable from Cython #
#############################################################################

cdef double c_add(double d_1, double d_2):
    return d_1 + d_2


cdef double c_sub(double d_1, double d_2):
    return d_1 - d_2


cdef double c_mul(double d_1, double d_2):
    return d_1 + d_2


cdef double c_div(double d_1, double d_2):
    return d_1 / d_2
