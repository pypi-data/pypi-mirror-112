from trapeza.account.execution_heap cimport cFXWrapperVectorHeap, bool_t, string


cpdef tuple fx_null_fee(double volume, double price, base, quote, long processing_duration)


# noinspection PyPep8Naming
cdef class cFXAccount:
    # class attributes
    cdef public bool_t _c_is_heap
    cdef public bool_t _c_is_exchange_rate_updated
    cdef public bool_t _c_prohibit_debiting
    cdef public string _c_reference_currency
    cdef public dict _c_depot
    cdef public dict _c_fee
    cdef public dict _c_exchange_rates
    cdef readonly bool_t _c_ignore_type_checking
    cdef public long _c_clock
    cdef public short _c_check_marked_coverage    # 0: False/ None, 1: min_backward, 2: max_forward
    cdef public cFXWrapperVectorHeap vec_heap

    # C-only interface
    cdef short _c_check_debiting(self) except -1
    cdef short _c_issue_corruption_warning(self) except -1
    cdef short _c_confirmation(self, long processing_duration) except -1
    cdef short _c_fill_fee(self, double fee_volume, string fee_currency, long fee_exec_duration,
                           string forward_coverage=*) except -1
    cdef short _execute_heap(self) except -1
    cdef short _c_isin_depot_quiet(self, string currency) except -1

    # C and Python interface
    cpdef void _c__init__(self, string reference_currency, dict depot, dict fee_dict, list exec_heap, long clock,
                          dict exchange_rates, short check_marked_coverage, bool_t prohibit_debiting,
                          bool_t ignore_type_checking) except *
    cpdef short _c_reset(self) except -1
    cpdef double _c_check_coverage(self, double debit_amount, string currency, long time_step,
                                   double virtual_deposit=*) except -1
    cpdef short _c_isin_depot(self, string currency) except -1
    cpdef short c_sell(self, double volume, double bid_price, string base, string quote, double fee_volume=*,
                     string fee_currency=*, long fee_exec_duration=*, long processing_duration=*,
                     string coverage=*, bool_t instant_withdrawal=*,
                     bool_t instant_float_fee=*) except -9999
    cpdef short c_buy(self, double volume, double ask_price, string base, string quote, double fee_volume=*,
                    string fee_currency=*, long fee_exec_duration=*, long processing_duration=*,
                    string coverage=*, bool_t instant_withdrawal=*,
                    bool_t instant_float_fee=*) except -9999
    cpdef short c_transfer(self, double volume, string currency,
                         double payer_fee_volume=*, string payer_fee_currency=*,
                         long payer_fee_exec_duration=*, long payer_processing_duration=*) except -9999
    cpdef short c_collect(self, double volume, string currency,
                        double payee_fee_volume=*, string payee_fee_currency=*, long payee_fee_exec_duration=*,
                        long payee_processing_duration=*) except -9999
    cpdef short c_deposit(self, double volume, string currency, long processing_duration, double fee_volume=*,
                        string fee_currency=*, long fee_exec_duration=*,
                        string coverage=*, bool_t instant_float_fee=*) except -9999
    cpdef short c_withdraw(self, double volume, string currency, long processing_duration=*, double fee_volume=*,
                         string fee_currency=*, long fee_exec_duration=*,
                         string coverage=*, bool_t instant_float_fee=*) except -9999
    cpdef long c_tick(self, long clock) except? -9999
    cpdef short c_update_exchange_rate(self, double rate, string base, string quote) except -1
    cpdef short c_batch_update_exchange_rates(self, list list_rates, list list_base_quote_pair) except -1
    cpdef double c_total_balance(self, dict exchange_rates, string reference_currency) except? -1.7e+250
    cpdef double c_position(self, string currency) except? -1.7e+250
