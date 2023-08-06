# distutils: language=c++
from libcpp.string cimport string
from libcpp cimport bool as bool_t    # use in .pyx
from libcpp.vector cimport vector
# noinspection PyUnresolvedReferences
from libcpp.algorithm cimport make_heap, sort_heap, push_heap, pop_heap     # use in .pyx


cdef struct fx_heap_element_struct:
    long time
    string action_func
    double volume
    string currency
    string coverage


cdef struct currency_pair_struct:
    string currency_a
    string currency_b
    double rate

# noinspection PyPep8Naming
cdef class cFXWrapperVectorHeap:
    cdef vector[fx_heap_element_struct] vector_heap
    cdef string std_cover_at_exec_exception
    cdef long size(self)
    cpdef double cum_sum_heap(self, string currency, string action_func_type, long time_step, long current_clock)
    cpdef double cum_sum_marked_fund(self, string currency, long time_step, long current_clock)
    cpdef double cum_sum_marked_debit(self, string currency, long time_step, long current_clock)
    cdef fx_heap_element_struct heappop(self)
    cpdef fx_heap_element_struct encode_tostruct(self, list element)
    cpdef fx_heap_element_struct tostruct(self, list element)
    cdef void heappush_struct(self, fx_heap_element_struct element)
    cdef void heappush(self, list element)
    cpdef list tolist(self)
    cdef long max_time_step(self) except? -9223372036854775807
    cpdef long py_max_time_step(self) except? -9223372036854775807


cdef class DictKeysToVec:
    cdef vector[currency_pair_struct] currency_pairs
    cdef (bool_t, bool_t, double, double) is_tuple_key_in_tuple_vec(self, string key_a, string key_b)
