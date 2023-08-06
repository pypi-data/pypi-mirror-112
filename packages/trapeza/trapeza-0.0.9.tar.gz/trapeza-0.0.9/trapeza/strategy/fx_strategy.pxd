# distutils: language=c++
from libcpp cimport bool as bool_t      # use in .pyx
from libcpp.string cimport string       # use in .pyx
from libcpp.unordered_map cimport unordered_map     # use in .pyx
from libcpp.vector cimport vector


cpdef short _c_tick_method(self, dict data) except -1


# noinspection PyPep8Naming
cdef class cFXStrategy:
    cdef vector[vector[vector[string]]] c_signals
    cdef unordered_map[string, vector[vector[double]]] c_positions
    cdef unordered_map[string, vector[double]] c_merged_positions
    cdef vector[vector[double]] c_total_balances
    cdef vector[double] c_merged_total_balances
    cdef unordered_map[long,vector[string]] _c_signals_at_step_t

    cdef public string c_name
    cdef readonly bool_t _c_ignore_type_checking
    cdef public list c_accounts
    cdef public long c_lookback
    cdef public bool_t c_suppress_ticking
    cdef public bool_t c_suppress_evaluation

    cdef public dict c_strategy_kwargs  # py_strings only
    cdef public dict c_tick_kwargs  # py_strings_only
    cdef public object c_strategy_func
    cdef public object c_tick_method
    cdef public list _c_init_accs_depots    # list of dicts of py_objects
    cdef public list _c_accs_clocks         # list of py_ints

    cpdef short c_init(self, string name, list accounts, object strategy_func, long lookback, object tick_func,
                       bool_t suppress_ticking, bool_t ignore_type_checking, dict strategy_kwargs,
                       dict tick_kwargs, bool_t suppress_evaluation) except -1
    cpdef short _c_init_all_positions(self, list all_keys) except -1
    cpdef short _c_reset_storage(self) except -1
    cpdef short c_reset(self) except -1
    cdef dict parse_positions(self, unordered_map[string, vector[vector[double]]] positions)
    cdef list parse_signals(self, vector[vector[vector[string]]] signals)
    cdef dict parse_merged_positions(self, unordered_map[string, vector[double]] merged_positions)
    cdef list parse_total_balances(self, vector[vector[double]] total_balances)
    cdef list parse_merged_total_balances(self, vector[double] merged_total_balances)
    cpdef dict self_parse_positions(self)
    cpdef list self_parse_signals(self)
    cpdef dict self_parse_merged_positions(self)
    cpdef list self_parse_total_balances(self)
    cpdef list self_parse_merged_total_balances(self)
    cpdef dict self_parse_signals_at_step_t(self)
    cpdef short positions_from_py(self, dict positions) except -1
    cpdef short signals_from_py(self, list signals) except -1
    cpdef short merged_positions_from_py(self, dict merged_positions) except -1
    cpdef short total_balances_from_py(self, list total_balances) except -1
    cpdef short merged_total_balances_from_py(self, list merged_total_balances) except -1
    cpdef short _signals_at_step_t_from_py(self, dict _signals_at_step_t) except -1
    cpdef tuple c_wrap_evaluate(self, dict data_frame, string reference_currency, append_to_results)
    cdef short c_evaluate(self, dict data_frame, string reference_currency, bool_t append_to_results,
                          vector[vector[string]] *ret_signals, vector[unordered_map[string, double]] *ret_positions,
                          vector[double] *ret_total_balances) except -1
    cpdef short c_add_signal(self, long i, string signal) except -1
    cdef short c_run(self, dict price_data, string reference_currency, dict volume_data, long len_data,
                     vector[vector[vector[string]]] *ret_signals,
                     unordered_map[string, vector[vector[double]]] * ret_positions,
                     unordered_map[string, vector[double]] * ret_merged_positions,
                     vector[vector[double]] *ret_total_balances, vector[double] *ret_merged_total_balances) except -1
    cpdef list c_wrap_run(self, dict price_data, string reference_currency, dict volume_data, long len_data)
