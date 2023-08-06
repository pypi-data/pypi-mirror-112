ctypedef double (*c_op)(double d_1, double d_2)

cdef double c_add(double d_1, double d_2)
cdef double c_sub(double d_1, double d_2)
cdef c_op c_mul
cdef c_op c_div
