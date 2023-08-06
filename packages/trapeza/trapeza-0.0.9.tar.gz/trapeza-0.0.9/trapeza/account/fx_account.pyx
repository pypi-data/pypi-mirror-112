# distutils: language=c++

import heapq
import warnings

import cython

from libc.math cimport INFINITY

from trapeza.account.execution_heap cimport fx_heap_element_struct, cFXWrapperVectorHeap, bool_t, string, DictKeysToVec
from trapeza.arithmetics.arithmetics cimport c_precision_add, c_precision_subtract, c_precision_multiply, c_precision_divide

from trapeza.account.base_account import BaseAccount
from trapeza.utils import check_types, ProtectedDict, ProtectedExecHeap
from trapeza import exception as tpz_exception


cpdef tuple fx_null_fee(double volume, double price, base, quote, long processing_duration):
    """
    Standard fee rule for FXAccount, equal to not applying any fees.

    :param volume: double, transaction volume in base currency
    :param price: double, price in base|quote FX direct notation
    :param base: python str, base currency in FX direct notation (see docstring of class description FXAccount)
    :param quote: python str, quote currency in FX direct notation (see docstring of class description FXAccount)
    :param processing_duration: long, processing time of FXAccount transaction (e.g. sell() or buy())
    :return: 0, base, 0
    """
    return 0, base, 0

# noinspection PyAbstractClass,PyPep8Naming,PyUnresolvedReferences,PyAttributeOutsideInit,PyTypeChecker
cdef class cFXAccount:
    """
    This is a C++ implementation via cython and gets wrapped by FXAccount class. This class tries to stay in C++ space
    as long as possible to avoid unnecessary type casting to Python data types. The internal heap (cf. stack automaton
    logic) is implemented via a C++ heap vector.
    Please refer to the docstrings of FXAccount for detailed descriptions. Details might differ slightly, but the
    overall logic idea is the same and this class gets wrapped by FXAccount anyhow. This class is never called directly
    by the user, so detailed docstrings do not make that much sense here.

    TODO: map instead of dict (not really an advantage as Python's dict is already well optimized)
    TODO: check if turning string to char* makes sense
    """

    def __init__(self, string reference_currency, dict depot, dict fee_dict, list exec_heap, long clock,
                 dict exchange_rates, short check_marked_coverage, bool_t prohibit_debiting,
                 bool_t ignore_type_checking):
        """
        Calls self._c__init__. See self._c__init__ for further docstring information.
        :param reference_currency: std:string
        :param depot: dict
        :param fee_dict: dict
        :param exec_heap: list of lists
        :param clock: long
        :param exchange_rates: dict
        :param check_marked_coverage: short
        :param prohibit_debiting: std:bool
        :param ignore_type_checking: std:bool
        :return None
        """
        self._c__init__(reference_currency, depot, fee_dict, exec_heap, clock,exchange_rates, check_marked_coverage,
                     prohibit_debiting, ignore_type_checking)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef void _c__init__(self, string reference_currency, dict depot, dict fee_dict, list exec_heap, long clock,
                 dict exchange_rates, short check_marked_coverage, bool_t prohibit_debiting,
                 bool_t ignore_type_checking) except*:
        """
        This methods gets wrapped by __init__ and serves as method to be called from _c_reset() and _c_full_reset(), 
        which is useful when __init__ gets overwritten during subclassing.
        :param reference_currency: std:string, reference currency for account
        :param depot: dict, {b'currency': double:current_position_size}
        :param fee_dict: dict, {b'buy': func, b'sell': func, b'withdraw': func, b'deposit': func}
        :param exec_heap: list os lists, list of [int:time, py_str:action_func, float:volume, py_str:currency,
                                                  py_str:coverage]
                          this gets translated to self.vec_heap (C++ heap vector)
                          action_func: {'c_withdraw', 'c_deposit'} ('withdraw' and 'deposit' are not auto-parsed at 
                                       this point)
                          coverage: see FXAccount docstring regarding sell, buy, withdraw and deposit
        :param clock: long, internal clock
        :param exchange_rates: dict, {(b'currency', b'currency'): double:current_exchange_rate}
        :param check_marked_coverage: short, 0: False/ None, 1: min_backward, 2: max_forward
                                      see FXAccount for further details
        :param prohibit_debiting: std:bool
                                  see FXAccount for further details
        :param ignore_type_checking: std:bool
                                     see FXAccount for further details
        :return: None
        """
        # >>>set whether internal type checking is omitted (performance increase vs. safer code)
        self._c_ignore_type_checking = ignore_type_checking

        # >>>base_currency
        self._c_reference_currency = reference_currency

        # >>>depot: key: currency, value: volume
        self._c_depot = depot

        # >>>switch checking of coverage of marked transaction on or off
        # 0: False/ None, 1: min_backward, 2: max_forward
        self._c_check_marked_coverage = check_marked_coverage

        # >>>internal state which checks if self.update_exchange_rate() or self.batch_update_exchange_rates() was called
        #    before calling self.total_balance()
        self._c_is_exchange_rate_updated = False

        # >>>internal state for processing marked transactions within coverage checking (recursion handling)
        self._c_is_heap = False

        # >>>heap: (time, action_func, volume, currency, **kwargs)
        self.vec_heap = cFXWrapperVectorHeap(exec_heap)

        # >>>parse fees
        self._c_fee = fee_dict

        # >>>exchange rates
        self._c_exchange_rates = exchange_rates

        # >>>allow debiting
        self._c_prohibit_debiting = prohibit_debiting

        # >>>clock
        self._c_clock = clock  # internal clock in time base units for oder execution

        #>>>init depot in reference currency
        # self._c_depot[reference_currency] = 0

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef short _c_reset(self) except -1:
        """
        See FXAccount for docstring information.
        :return: 1
        """
        self._c__init__(self._c_reference_currency, dict(), self._c_fee, [], 0, dict(), self._c_check_marked_coverage,
                        self._c_prohibit_debiting, self._c_ignore_type_checking)
        return 1

    @cython.wraparound(False)
    cpdef double _c_check_coverage(self, double debit_amount, string currency, long time_step,
                                   double virtual_deposit=0) except -1:
        """
        See FXAccount for docstring information.
        
        virtual_deposit is used for intermediary calculations of fictive (what-if) funds which have not been executed
        or marked on heap yet.
        
        :param debit_amount: double
        :param currency: std:string
        :param time_step: long
        :param virtual_deposit: double, virtual but not effectively executed/ billed fund, which is added on top for
                                coverage calculation (but not billed at depot or internal heap, so takes no real effect)
        :return: coverage (i.e. cum_sum_funds - cum_sum_debits - debit_amount) in given currency up to given time step, 
                 double or math.inf (if self.check_marked_coverage=False)
        """
        if self._c_check_marked_coverage == 0:
            return INFINITY

        if self._c_check_marked_coverage == 2 and  self.vec_heap.size() != 0:
                time_step = self.vec_heap.max_time_step()

        # >>>avoid double accounting when debit volume is already in heap
        if self._c_is_heap:
            debit_amount = 0

        self._c_isin_depot(currency)

        cdef double marked_debit_amount
        cdef double marked_funds
        cdef double coverage
        cdef double currency_position
        marked_debit_amount = self.vec_heap.cum_sum_marked_debit(currency, time_step, self._c_clock)
        if virtual_deposit != 0:
            marked_funds = c_precision_add(self.vec_heap.cum_sum_marked_fund(currency, time_step, self._c_clock),
                                           virtual_deposit)
        else:
            marked_funds = self.vec_heap.cum_sum_marked_fund(currency, time_step, self._c_clock)

        # noinspection PyUnresolvedReferences
        currency_position = self._c_depot[currency]
        coverage = c_precision_add(currency_position,
                                   c_precision_add(marked_funds,
                                                   c_precision_add(-marked_debit_amount, -debit_amount)))

        if coverage < 0:
            raise tpz_exception.CoverageError(coverage, currency.decode())
        return coverage

    # noinspection PyUnresolvedReferences
    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef short _c_check_debiting(self) except -1:
        """
        Checks if any positions in self.depot are negative, given that self._c_prohibit_debiting is True (else this
        function just passes through without doing anything). If negative positions are detected, CoverageError
        is thrown.
        :return: 1
        :raises: warning.warn and 
                 trapeza.exception.CoverageError: if any position in self._c_depot is negative and 
                                                  self._c_prohibit_debiting is True
        """
        cdef string key
        if self._c_prohibit_debiting is False:
            return 1
        else:
            for key in self._c_depot.keys():
                if self._c_depot[key] < 0:
                    warnings.warn('Negative depot position detected, even though debiting was not allowed. '
                                  'Account depot as well as internal execution heap of delayed/ future transactions '
                                  'may be irrecoverably corrupted. CoverageError.')
                    self._c_issue_corruption_warning()
                    raise tpz_exception.CoverageError(self._c_depot[key], key.decode(),
                                                     'Debiting into negative positions not allowed by '
                                                     'parameter "prohibit_debiting" at init.')
        return 1

    @cython.wraparound(False)
    cpdef short _c_isin_depot(self, string currency) except -1:
        """
        Checks if param:currency is in self.depot.keys()
        :param currency: std:string
        :return: 1
        :raises: trapeza.exception.PositionNAError: if currency not in self.depot
        """
        try:
            # noinspection PyUnresolvedReferences
            _ = self._c_depot[currency]
        except KeyError:
            raise tpz_exception.PositionNAError(currency.decode())
        return 1

    @cython.wraparound(False)
    cdef short _c_isin_depot_quiet(self, string currency) except -1:
        """
        Does exactly the same as self._c_isin_depot() but instead of throwing an exception, this function returns
        1 for 'is in depot' and 0 if not: without throwing any exception.
        :param currency: std:string
        :return: 1: if currency in depot
                 0: else
        """
        try:
            # noinspection PyUnresolvedReferences
            _ = self._c_depot[currency]
        except KeyError:
            return 0
        return 1

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef short _c_issue_corruption_warning(self) except -1:
        """
        Issues warning about corrupted heap and corrupted account depot if checking of marked but not yet booked 
        transactions is inactive and corruption is detected.

        If CoverageError occurs, account depot gets unusable: e.g. sell transaction is split into deposit and
        withdrawal and if some other withdrawal causes CoverageException in between those two split transactions,
        then transactions cannot be booked back - because there's no identifier, if withdrawal is an actual withdrawal
        or part of a composed transaction like buy() or sell() - which means, last depot status before
        CoverageException occurs is not re-constructable! This is especially the case of marked but not yet booked 
        coverages.

        When CoverageException occurs during 'coverage' of transaction's method (this independent from marked coverage, 
        i.e checking if transaction can be executed right now with current depot status without regarding
        marked transactions), then there haven't been any bookings/ filling and no heap actions, such that depot status
        is recoverable. This is because, if CoverageException during 'coverage' of transaction's method occurs, it 
        prevents pushing things to heap or booking any transactions. So if no checking of marked coverage and if 
        transactions are delayed, then this transaction already got pushed to the heap, such that, even when 
        CoverageError is thrown at execution, heap might be already corrupted due to the fact, that there's no 
        distinguishing of split transactions (sell and buy into withdraw and deposit).
        --> if CoverageException at 'coverage' of transaction's method and when marked coverage is active:
              nothing happened, no bookings, no pushing to heap, so no need to do anything, because execution was
              prevented by CoverageException...
              deleting heap not necessary, reverting transaction not necessary
        --> if CoverageException during checking marked coverage (but not yet booked transactions):
              nothing happened, no bookings, no pushing to heap, so no need to do anything, because execution was
              prevented by CoverageException...
              deleting heap not necessary, reverting transaction not necessary
        --> if CoverageException at 'coverage' of transaction's method when marked coverage is inactive:
              everything lost, nothing recoverable
              heap is corrupted due to splitting sell and buy transactions, reverting transaction is not sufficient to
              catch split transactions of buy and sell and to reconstruct depot status accordingly (as order of
              ordinary withdrawals and withdrawals from splitting e.g. sell() or buy() might got mixed up)
              deleting heap doesn't make sense as heap and depot status are corrupted and irrecoverable,
              depot status is not recoverable
              only thing to do: issue warning!
        :return: 1
        :raises: warning
        """
        if self._c_check_marked_coverage == 0:
            warnings.warn('Checking of marked but not yet billed transactions was turned off. Account depot as '
                          'well as internal execution heap of delayed/ future transactions may be '
                          'irrecoverably corrupted. CoverageError.')
        return 1

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef short _c_confirmation(self, long processing_duration) except -1:
        """
        Return confirmation status depending on value of processing_duration
        
        :param processing_duration: long
        :return: 1 if no processing_duration (no delay in processing transaction, instant execution/ billing), else 0
        """
        # if processing_duration is None or processing_duration <= 0:   # None not possible
        if processing_duration <= 0:
            return 1
        else:
            return 0

    @cython.wraparound(False)
    cdef short _c_fill_fee(self, double fee_volume, string fee_currency, long fee_exec_duration,
                           string forward_coverage=b'except') except -1:
        """
        See FXAccount for docstring information.
        
        Handles fee internally and calls self.c_withdraw(), which takes processing_duration into account to process
        fees.
        
        :param fee_volume: double, volume in param:fee_currency
        :param fee_currency: std:string, currency
        :param fee_exec_duration: long
        :param forward_coverage: std:string,
                                 propagates coverage from method, from which
                                 self._fill_fee() was called, to self.withdraw()
        :return: 1
        """
        if fee_volume > 0:
            self.c_withdraw(fee_volume, fee_currency, fee_exec_duration, coverage=forward_coverage)
        return 1

    @cython.wraparound(False)
    cdef short _execute_heap(self) except -1:
        """
        Processes and executes self.exec_heap (if transactions are delayed due to processing duration of fulfillment).
        Heap structure (stack automaton logic) is implemented via C++ vector, see trapeza.account.execution_heap.pyx
        for implementation details.
        :return: 1
        """
        # heap: (time, action_func, volume, currency, **kwargs)

        # >>>avoid double accounting when processing heap
        self._c_is_heap = True

        # >>>loop through heap, which is sorted in ascending timestamps
        cdef fx_heap_element_struct process
        while True:
            # get first element with lowest timestamp
            if self.vec_heap.size() > 0:
                process = self.vec_heap.heappop()
            else:
                self._c_is_heap = False
                break

            # check if internal clock already reached execution time
            if self._c_clock >= process.time:
                # execute
                if len(process) == 5:
                    # noinspection PyUnresolvedReferences
                    getattr(self, process.action_func.decode())\
                        (process.volume, process.currency, 0,
                         coverage=process.coverage)
                else:
                    # noinspection PyUnresolvedReferences
                    getattr(self, process.action_func.decode())(process.volume, process.currency.decode(), 0)
            else:
                # internal clock did not reach execution time yet, so push back and exit
                self.vec_heap.heappush_struct(process)
                self._c_is_heap = False
                break
        self._c_check_debiting()
        return 1

    # noinspection DuplicatedCode,PyUnresolvedReferences
    @cython.wraparound(False)
    cpdef short c_sell(self, double volume, double bid_price, string base, string quote, double fee_volume=0,
                   string fee_currency=b'default', long fee_exec_duration=0, long processing_duration=0,
                   string coverage=b'except', bool_t instant_withdrawal=False,
                   bool_t instant_float_fee=False) except -9999:
        """
        C++ implementation via cython. Is wrapped by FXAccount. See FXAccount.sell for further information.
        
        :param volume: double, in BASE currency
        :param bid_price: double, current bid rate in base|quote notation
        :param base: std:string, currency
        :param quote: std:string, currency
        :param fee_volume: double, volume in param:fee_currency
        :param fee_currency: std:string, if b'default', then param:fee_currency defaults to param:base
        :param fee_exec_duration: long, processing time (delay) in time base units of internal clock
        :param processing_duration: long, processing time (delay) in time base units of internal clock
        :param coverage: std:string {b'partial', b'except', b'ignore', b'debit'}, 
                         default=b'except'
                         see FXAccount.sell for details
        :param instant_withdrawal: std:bool, 
                                   see FXAccount.sell for details
        :param instant_float_fee: std:bool, 
                                  see FXAccount.sell for details
        :return: confirmation: short, 
                               confirmation states --> -1: ignored, 0: processing (processing_duration), 1: executed
        """
        # >>>parse fee_currency if necessary: not the most elegant job, but this way heap execution logic does not brake
        if fee_currency == b'default':
            fee_currency = base

        # >>>store value for later restoring
        cdef short current_check_marked_coverage
        current_check_marked_coverage = self._c_check_marked_coverage
        # >>>get fulfillment method depending on account coverage and fee structure
        if self._c_depot[base] < c_precision_add(volume, fee_volume * (fee_currency == base)):
            if coverage == b'except':
                raise tpz_exception.CoverageError(c_precision_add(volume, fee_volume * (fee_currency == base)),
                                                  base.decode())
            elif coverage == b'partial':
                volume = c_precision_subtract(self._c_depot[base], fee_volume * (fee_currency == base))
                if volume < 0:
                    raise tpz_exception.CoverageError(fee_volume, fee_currency.decode(),
                                                     'Transaction not feasible even though coverage set '
                                                     'to partial. Fees not covered.')
            elif coverage == b'ignore':
                return -1
            elif coverage == b'debit':
                self._c_check_marked_coverage = 0

        # >>>check coverage before proceeding
        self._c_check_coverage(c_precision_add(volume, fee_volume * (fee_currency == base)), base,
                               self._c_clock + processing_duration * (1 - instant_withdrawal))
        if fee_volume > 0:
            # if fee_volume is in base (or generally speaking not in quote),
            # we have to check that enough money is on depot
            if fee_currency != quote:
                self._c_check_coverage(fee_volume, fee_currency,
                                       self._c_clock + fee_exec_duration * (1 - instant_float_fee))
            # if fee_volume is in quote, we have to take processing times into account
            #   - instant processing of fee and depositing: we can emulate this behavior by virtually depositing
            #       the sell volume when checking coverage
            #   - depositing before fee: we can emulate this behavior by virtually depositing the sell volume
            #       when checking coverage
            #   - fee before depositing: check that enough money in fee_currency is on depot
            elif fee_exec_duration * (1 - instant_float_fee) < processing_duration:
                self._c_check_coverage(fee_volume, fee_currency,
                                       self._c_clock + fee_exec_duration * (1 - instant_float_fee))
            else:
                if self._c_isin_depot_quiet(fee_currency) == 0:
                    # this is done to prevent an exception if there is not yet an open position in fee_currency on
                    # account's depot
                    self._c_depot[fee_currency] = 0
                # volume given in base, bid_price in base|quote notation (unit: [quote/base])
                # volume for offsetting fees must be in quote, so we have to multiply with bid_price
                self._c_check_coverage(fee_volume, fee_currency,
                                       self._c_clock + fee_exec_duration * (1 - instant_float_fee),
                                       c_precision_multiply(volume, bid_price))

        # >>>process transactions according to withdrawal execution duration
        self.c_withdraw(volume, base, processing_duration=processing_duration * (1 - instant_withdrawal),
                        coverage=coverage)

        # >>>deposit quote currency
        self.c_deposit(volume=c_precision_multiply(volume, bid_price), currency=quote,
                       processing_duration=processing_duration, coverage=coverage)

        # >>>handle fees
        cdef string propagate_coverage
        if coverage == b'partial':
            propagate_coverage = b'except'
        else:
            propagate_coverage = coverage
        self._c_fill_fee(fee_volume=fee_volume, fee_currency=fee_currency,
                         fee_exec_duration=fee_exec_duration * (1 - instant_float_fee),
                         forward_coverage=propagate_coverage)

        # >>>restore
        self._c_check_marked_coverage = current_check_marked_coverage

        # >>> return confirmation
        return self._c_confirmation(processing_duration)

    # noinspection DuplicatedCode,PyUnresolvedReferences
    @cython.wraparound(False)
    cpdef short c_buy(self, double volume, double ask_price, string base, string quote, double fee_volume=0,
                      string fee_currency=b'default', long fee_exec_duration=0, long processing_duration=0,
                      string coverage=b'except', bool_t instant_withdrawal=False,
                      bool_t instant_float_fee=False) except -9999:
        """
        C++ implementation via cython. Is wrapped by FXAccount. See FXAccount.buy for further information.
        
        :param volume: double, in BASE currency
        :param ask_price: double, current ask rate (base|quote notation)
        :param base: std:string, currency
        :param quote: std:string, currency
        :param fee_volume: double, volume in param:fee_currency
        :param fee_currency: std:string, if b'default', then param:fee_currency defaults to param:base
        :param fee_exec_duration: long, processing time (delay) in time base units of internal clock
        :param processing_duration: long, processing time (delay) in time base units of internal clock
        :param coverage: std:string {b'partial', b'except', b'ignore', b'debit'},
                         default=b'except'
                         see FXAccount.buy for details
        :param instant_withdrawal: std:bool, 
                                   see FXAccount.buy for details
        :param instant_float_fee: std:bool, 
                                  see FXAccount.buy for details
        :return: confirmation: short,
                               confirmation states --> -1: ignored, 0: processing (processing_duration), 1: executed
        """
        # Volume is currently given in base. At buy transaction, we receive base and give quote currency. So it's
        # easier to handle volume in quote currency.
        # >>>convert volume from base into quote
        cdef double volume_quote = c_precision_multiply(volume, ask_price)

        # >>>parse fee_currency if necessary: not the most elegant job, but this way heap execution logic does not brake
        if fee_currency == b'default':
            fee_currency = base

        # >>>store value for later restoring
        cdef short curr_check_marked_coverage
        curr_check_marked_coverage = self._c_check_marked_coverage
        # >>>get fulfillment method depending on account coverage and fee structure
        # volume is in quote currency
        if self._c_depot[quote] < c_precision_add(volume_quote, fee_volume * (fee_currency == quote)):
            if coverage == b'except':
                raise tpz_exception.CoverageError(c_precision_add(volume_quote, fee_volume * (fee_currency == quote)),
                                                  quote.decode())
            elif coverage == b'partial':
                volume_quote = c_precision_subtract(self._c_depot[quote], fee_volume * (fee_currency == quote))  # in quote currency
                if volume_quote < 0:
                    raise tpz_exception.CoverageError(fee_volume, fee_currency.decode(),
                                                     'Transaction not feasible even though coverage set '
                                                     'to partial. Fees not covered.')
            elif coverage == b'ignore':
                return -1
            elif coverage == b'debit':
                self._c_check_marked_coverage = 0

        # >>>check coverage before proceeding
        self._c_check_coverage(c_precision_add(volume_quote, fee_volume * (fee_currency == quote)), quote,
                             self._c_clock + processing_duration * (1 - instant_withdrawal))
        if fee_volume > 0:
            # if fee_volume is in quote (or generally speaking not in base),
            # we have to check that enough money is on depot
            if fee_currency != base:
                self._c_check_coverage(fee_volume, fee_currency,
                                       self._c_clock + fee_exec_duration * (1 - instant_float_fee))
            # if fee_volume is in base, we have to take processing times into account
            #   - instant processing of fee and depositing: we can emulate this behavior by virtually depositing
            #       the buy volume when checking coverage
            #   - depositing before fee: we can emulate this behavior by virtually depositing the buy volume
            #       when checking coverage
            #   - fee before depositing: check that enough money in fee_currency is on depot
            elif fee_exec_duration * (1 - instant_float_fee) < processing_duration:
                self._c_check_coverage(fee_volume, fee_currency,
                                       self._c_clock + fee_exec_duration * (1 - instant_float_fee))
            else:
                if self._c_isin_depot_quiet(fee_currency) == 0:
                    # this is done to prevent an exception if there is not yet an open position in fee_currency on
                    # account's depot (quote currency in particular)
                    self._c_depot[fee_currency] = 0
                self._c_check_coverage(fee_volume, fee_currency,
                                       self._c_clock + fee_exec_duration * (1 - instant_float_fee), volume)

        # >>>process transactions according to withdrawal execution duration
        self.c_withdraw(volume_quote, quote, processing_duration=processing_duration * (1 - instant_withdrawal),
                        coverage=coverage)

        # >>>deposit base currency
        self.c_deposit(volume, base, processing_duration=processing_duration, coverage=coverage)

        # >>>handle fees
        cdef string propagate_coverage
        if coverage == b'partial':
            propagate_coverage = b'except'
        else:
            propagate_coverage = coverage
        self._c_fill_fee(fee_volume=fee_volume, fee_currency=fee_currency,
                         fee_exec_duration=fee_exec_duration * (1 - instant_float_fee),
                         forward_coverage=propagate_coverage)

        # >>>restore
        self._c_check_marked_coverage = curr_check_marked_coverage

        # >>> return confirmation
        return self._c_confirmation(processing_duration)

    # noinspection DuplicatedCode
    @cython.wraparound(False)
    cpdef short c_transfer(self, double volume, string currency,
                         double payer_fee_volume=0, string payer_fee_currency=b'default',
                         long payer_fee_exec_duration=0, long payer_processing_duration=0) except -9999:
        """
        C++ implementation via cython. Is wrapped by FXAccount. See FXAccount.transfer for further information.
        
        Same coverage as self.c_withdraw will be used (default=b'except').
        
        :param volume: double, volume in param:currency
        :param currency: std:string
        :param payer_fee_volume: double, volume in param:payer_fee_currency
        :param payer_fee_currency: std:string, if b'default' then param:payer_fee_currency is used
        :param payer_fee_exec_duration: long, processing time (delay) in time base units of internal clock
        :param payer_processing_duration: long, processing time (delay) in time base units of internal clock
        :return: confirmation: short, confirmation states --> 0: processing (processing_duration), 1: executed
        """
        if payer_fee_currency == b'default':
            payer_fee_currency = currency

        # >>>withdraw from own account
        self.c_withdraw(volume, currency, payer_processing_duration, payer_fee_volume, payer_fee_currency,
                        payer_fee_exec_duration)

        return self._c_confirmation(payer_processing_duration)

    # noinspection DuplicatedCode
    @cython.wraparound(False)
    cpdef short c_collect(self, double volume, string currency,
                        double payee_fee_volume=0, string payee_fee_currency=b'default', long payee_fee_exec_duration=0,
                        long payee_processing_duration=0) except -9999:
        """
        C++ implementation via cython. Is wrapped by FXAccount. See FXAccount.collect for further information.
        
        Same coverage as self.c_deposit will be used (default=b'except').
        
        :param volume: double, volume in param:currency
        :param currency: std:string
        :param payee_fee_volume: double, volume in param:payee_fee_currency
        :param payee_fee_currency: std:string, if b'default' then param:payee_fee_currency is used
        :param payee_fee_exec_duration: long, processing time (delay) in time base units of internal clock
        :param payee_processing_duration: long, processing time (delay) in time base units of internal clock
        :return: confirmation: short, confirmation states --> 0: processing (processing_duration), 1: executed
        """
        # >>>parse fee_currency if necessary: not the most elegant job, but this way heap execution logic does not brake
        if payee_fee_currency == b'default':
            payee_fee_currency = currency

        # >>>deposit at own account
        self.c_deposit(volume, currency, payee_processing_duration, payee_fee_volume, payee_fee_currency,
                       payee_fee_exec_duration)

        return self._c_confirmation(payee_processing_duration)

    # noinspection PyUnresolvedReferences
    @cython.wraparound(False)
    cpdef short c_deposit(self, double volume, string currency, long processing_duration, double fee_volume=0,
                        string fee_currency=b'default', long fee_exec_duration=0,
                        string coverage=b'except', bool_t instant_float_fee=False) except -9999:
        """
        C++ implementation via cython. Is wrapped by FXAccount. See FXAccount.deposit for further information.
        
        THIS METHOD IMPLEMENTS A SLIGHTLY DIFFERENT ORDER OF ARGUMENTS THAN FXAccount!
        
        :param volume: double, volume given in currency
        :param currency: std:string
        :param processing_duration: long, processing time (delay) in time base units of internal clock
        :param fee_volume: double, volume given in fee_currency
        :param fee_currency: std:string, if b'default' then param:currency is used
        :param fee_exec_duration: long, processing time (delay) in time base units of internal clock
        :param coverage: std:string {b'except', b'debit'}, default=b'except'
                         see FXAccount.deposit for details
                         b'partial' not available for this function (makes no sense, see comments
                         in source code of this method)
                         b'ignore' not available on purpose
        :param instant_float_fee: std:bool, 
                                  see FXAccount.deposit for details
        :return: confirmation: short, confirmation states --> 0: processing (processing_duration), 1: executed
        :TODO: optimize performance
        """
        # >>>parse fee_currency if necessary: not the most elegant job, but this way heap execution logic does not brake
        if fee_currency == b'default':
            fee_currency = currency

        # >>>store value for later restoring
        cdef short curr_check_marked_coverage
        cdef double remaining_fees
        cdef double current_depot_fee_currency = 0
        curr_check_marked_coverage = self._c_check_marked_coverage

        # >>>prevent KeyError if fee_currency is in currency as fees can be offset by incoming depositing volume
        if currency == fee_currency and self._c_isin_depot_quiet(fee_currency) == 0:
            current_depot_fee_currency = 0
        else:
            self._c_isin_depot(fee_currency)
            current_depot_fee_currency = self._c_depot[fee_currency]

        # when depositing, the only transaction, which might cause coverage violation, is the withdrawal of fees
        # so basically there are three possible scenarios:
        #   1. fees < deposit volume
        #   2. fees = deposit volume
        #   3. fees > deposit volume: depot positions have to cover the remainder
        # fee can either be payed by deposit volume or by depot positions
        # paying by depositing volume is only possible, if fees and depositing volume are in the same currency and
        # if processing times comply
        # if fees and depositing volume are not in the same currency, fees have to be payed by depot position
        # we do not have any possibility to scale down fees if coverage violation occurs, because it is not clear
        # if fees are calculated as fix or variable fees --> therefore partial depositing makes no sense!
        # >>>handle coverage exception induced by fees
        # fee coverage is checked at code block below, so we just have to set debiting mode if necessary
        if (fee_volume > 0 and coverage == b'except'
                and current_depot_fee_currency + (volume * (currency==fee_currency)) < fee_volume):
            # this is rather a weak check as processing times of depositing and fee billing might cause
            #   coverage violation
            # Checking only against depot position would be to restrictive as fees also might be payed from depositing
            #   volume. Taking processing times into account is done later on, so we stick to this weaker check here
            # we do a re-check with precision arithmetics to avoid error caused by floating point errors
            if c_precision_add(current_depot_fee_currency, volume * (currency==fee_currency)) < fee_volume:
                # multiplication is either with 1 or 0 so need for precision
                if self._c_is_heap:
                    self._c_issue_corruption_warning()
                raise tpz_exception.CoverageError(fee_volume, currency.decode())
        elif coverage == b'debit':
            self._c_check_marked_coverage = 0

        # >>>check coverage of fees
        if fee_volume > 0:
            # if fee is billed in the same currency as deposit amount, then we have to take processing times into account:
            #   - fee and deposit at same time: we can emulate this by virtually depositing as fee is effectively subtracted
            #       from the deposit amount in the end
            #   - deposit before fee: we can emulate this by virtually depositing as first deposit will arrive on
            #       account and then fee will be billed from this later on
            #   - fee before depositing: we have to check if enough money is on the account
            #   - instant fee: we have to check current position and take depositing volume into account if also instant
            # >>different currencies, fees cannot be offset by incoming depositing amount
            if fee_currency != currency:
                self._c_check_coverage(fee_volume, fee_currency,
                                       self._c_clock + fee_exec_duration * (1 - instant_float_fee))
            # from here on it's fee_currency == currency
            # >>instant fee
            elif fee_exec_duration * (1 - instant_float_fee) == 0:
                # we have to implement a hard check here because self._c_check_coverage does not throw an exception
                # if coverage checking is deactivated
                # we're doing this explicitly to be consistent with behavior of other transactions
                # this check must not be applied if debiting is allowed explicitly
                if (coverage != b'debit'
                        and current_depot_fee_currency + volume*(processing_duration==0) < fee_volume):
                    # we do re-check to avoid floating point errors
                    if c_precision_add(current_depot_fee_currency, volume*(processing_duration==0)) < fee_volume:
                        # multiplication either with 1 or 0 so no need for precision
                        if self._c_is_heap:
                            self._c_issue_corruption_warning()
                        raise tpz_exception.CoverageError(fee_volume, fee_currency.decode())
            # >>fee before depositing
            elif fee_exec_duration * (1 - instant_float_fee) < processing_duration:
                self._c_check_coverage(fee_volume, fee_currency,
                                       self._c_clock + fee_exec_duration * (1 - instant_float_fee))
            # >>fee after or at the same time of depositing
            else:
                if current_depot_fee_currency == 0:
                    # this is done to prevent an exception if there is not yet an open position in fee_currency on
                    # account's depot (and if it's 0 even though position exists, then we can set it to 0 again
                    # without any side effects)
                    self._c_depot[fee_currency] = 0
                self._c_check_coverage(fee_volume, fee_currency,
                                       self._c_clock + fee_exec_duration * (1 - instant_float_fee), volume)

        # >>>instant execution
        if processing_duration <= 0:
            try:  # if currency is already in depot
                self._c_depot[currency] = c_precision_add(self._c_depot[currency], volume)
            except KeyError:  # else we open a new position in depot
                self._c_depot[currency] = volume
        # >>>delayed transaction caused by necessary execution duration
        else:
            # push to exec_heap: (time, action_func, volume, currency, **kwargs)
            # only push coverage with 'except' or 'debit': if we push 'partial', then volume gets recursively
            # reduced, which does not follow the principle of least surprise. Instead turn 'partial' to except, which
            # is a more conservative guess (therefore just don't provide **kwargs, as 'except' is default value)
            if coverage == b'debit':
                self.vec_heap.heappush([self._c_clock + processing_duration, b'c_deposit', volume, currency,
                                        coverage])
            else:
                self.vec_heap.heappush([self._c_clock + processing_duration, b'c_deposit', volume, currency])

        # >>>handle fees
        if fee_volume > 0:
            self._c_fill_fee(fee_volume=fee_volume, fee_currency=fee_currency,
                             fee_exec_duration=fee_exec_duration * (1 - instant_float_fee),
                             forward_coverage=b'debit')

        # >>>restore
        self._c_check_marked_coverage = curr_check_marked_coverage

        # >>>return confirmation
        return self._c_confirmation(processing_duration)

    @cython.wraparound(False)
    cpdef short c_withdraw(self, double volume, string currency, long processing_duration=0, double fee_volume=0,
                         string fee_currency=b'default', long fee_exec_duration=0,
                         string coverage=b'except', bool_t instant_float_fee=False) except -9999:
        """
        C++ implementation via cython. Is wrapped by FXAccount. See FXAccount.withdraw for further information.
        
        THIS METHOD IMPLEMENTS A SLIGHTLY DIFFERENT ORDER OF ARGUMENTS THAN FXAccount!
        
        :param volume: double, volume given in currency
        :param currency: std:string
        :param processing_duration: long, processing time (delay) in time base units of internal clock
        :param fee_volume: double, volume given in fee_currency
        :param fee_currency: std:string, if b'default' then param:currency is used
        :param fee_exec_duration: long, processing time (delay) in time base units of internal clock
        :param coverage: std:string {b'partial', b'except', b'debit'}, default=b'except'
                         see FXAccount.withdraw for details
                         b'ignore' not available on purpose
        :param instant_float_fee: std:bool, 
                                  see FXAccount.withdraw for details
        :return: confirmation: short, confirmation states --> 0: processing (processing_duration), 1: executed
        """
        # >>>parse fee_currency if necessary: not the most elegant job, but this way heap execution logic does not brake
        if fee_currency == b'default':
            fee_currency = currency

        # >>>store for later restoring
        cdef short curr_check_marked_coverage
        curr_check_marked_coverage = self._c_check_marked_coverage

        # >>>handle coverage exception
        # volume is in currency
        cdef double currency_position = self._c_depot[currency]
        if currency_position < c_precision_add(volume, fee_volume * (fee_currency == currency)):
            if coverage == b'except':
                if self._c_is_heap:
                    self._c_issue_corruption_warning()
                raise tpz_exception.CoverageError(c_precision_add(volume, fee_volume * (fee_currency == currency)),
                                                  currency.decode())
            elif coverage == b'partial':
                volume = c_precision_subtract(currency_position, fee_volume * (fee_currency == currency))
                # in currency
                if volume < 0:
                    if self._c_is_heap:
                        self._c_issue_corruption_warning()
                    raise tpz_exception.CoverageError(fee_volume * (fee_currency == currency), currency.decode(),
                                                     'Transaction not feasible even though coverage set '
                                                     'to partial. Fees not covered')
            elif coverage == b'debit':
                self._c_check_marked_coverage = 0

        # >>>check coverage
        self._c_check_coverage(c_precision_add(volume, fee_volume * (fee_currency == currency)), currency,
                               self._c_clock + processing_duration)
        if fee_volume > 0:
            # when withdrawing, there is no depositing transaction onto the account
            # so we do not have to take different processing duration of withdrawal and fee billing into account as
            # billed fees cannot be offset by any incoming deposits within this code block
            self._c_check_coverage(fee_volume, fee_currency,
                                   self._c_clock + fee_exec_duration * (1 - instant_float_fee))

        # >>>instant execution
        if processing_duration <= 0:
            # execute
            self._c_depot[currency] = c_precision_subtract(currency_position, volume)
        # >>>delayed transaction caused by necessary execution duration
        else:
            # push to exec_heap: (time, action_func, volume, currency, **kwargs)
            # only push coverage with 'except' or 'debit': if we push 'partial', then volume gets recursively
            # reduced, which does not follow the principle of least surprise. Instead turn 'partial' to except, which
            # is a more conservative guess (therefore just don't provide **kwargs, as 'except' is default value)
            if coverage == b'debit':
                self.vec_heap.heappush([self._c_clock + processing_duration, b'c_withdraw', volume, currency,
                                        coverage])
            else:
                self.vec_heap.heappush([self._c_clock + processing_duration, b'c_withdraw', volume, currency])

        # >>>handle fees
        cdef string propagate_coverage
        if coverage == b'partial':
            propagate_coverage = b'except'
        else:
            propagate_coverage = coverage
        if fee_volume > 0:
            self._c_fill_fee(fee_volume=fee_volume, fee_currency=fee_currency,
                             fee_exec_duration=fee_exec_duration * (1 - instant_float_fee),
                             forward_coverage=propagate_coverage)

        # >>>restore
        self._c_check_marked_coverage = curr_check_marked_coverage

        # >>>return confirmation
        return self._c_confirmation(processing_duration)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef long c_tick(self, long clock) except? -9999:
        """
        C++ implementation via cython. Is wrapped by FXAccount. See FXAccount.tick for further information.
        
        Executes exec_heap after new clock time is set.
        
        :param clock: long >= 0
        :return: long, current (freshly set) clock time
        """
        self._c_clock = clock

        self._execute_heap()
        return self._c_clock

    @cython.wraparound(False)
    cpdef short c_update_exchange_rate(self, double rate, string base, string quote) except -1:
        """
        C++ implementation via cython. Is wrapped by FXAccount. See FXAccount.update_exchange_rate for 
        further information.
        
        Updates internal dict structure, which is needed during calculation of self.c_total_balance().
        It's sufficient enough, to just provide base|quote ratio. quote|base ratio does not have to be added separately
        and will be calculated automatically.

        :param rate: double,
                     use FX direct notation of base|quote pair (see docstring of class FXAccount for further information
                     on notation conventions)
        :param base: std:string
        :param quote: std:string
        :return: 1
        """
        # >>>update
        self._c_exchange_rates[base, quote] = rate
        self._c_is_exchange_rate_updated = True
        return 1

    @cython.wraparound(False)
    cpdef short c_batch_update_exchange_rates(self, list list_rates, list list_base_quote_pair) except -1:
        """
        C++ implementation via cython. Is wrapped by FXAccount. See FXAccount.batch_update_exchange_rates 
        for further information.
        
        Updates internal dict structure all at once, which is needed during calculation of self.c_total_balance().
        Updates are done all at once in contrast to self.c_update_exchange_rate, which only updates a single 
        base|quote pair.
        It's sufficient enough, to just provide base|quote ratio. quote|base ratio does not have to be added separately
        and will be calculated automatically.

        :param list_rates: list of floats,
                           exchange rate of base|quote pair in FX direct notation (see docstring of class FXAccount for 
                           further information on notation conventions)
        :param list_base_quote_pair: list of tuples(base, quote),
                                     base|quote pair notation
                                     base: std:string
                                     quote: std:string
        :return: 1
        """
        cdef int i
        for i in range(len(list_rates)):
            # noinspection PyUnresolvedReferences
            self.update_exchange_rate(list_rates[i], list_base_quote_pair[i][0], list_base_quote_pair[i][1])
        return 1

    # noinspection PyUnresolvedReferences
    @cython.wraparound(False)
    cpdef double c_total_balance(self, dict exchange_rates, string reference_currency) except? -1.7e+250:
        """
        C++ implementation via cython. Is wrapped by FXAccount. See FXAccount.total_balance for further information.
        
        Calculates current value of all assets within self.depot in reference currency.
        
        DOES NOT CHECK IF self.exchange_rates HAS BEEN UPDATED (in contrast to FXAccount.total_balance)!
        
        :param exchange_rates: dict with tuple of bytes (encoded python strings) as keys

                               key: (base, quote) as bytes (encoded python string) denoting currencies (or assets),
                                    in FX direct notation  (see docstring of class FXAccount for further information
                                    on notation conventions)
                               value: float,
                                      exchange_rate of base|quote pair in FX direct notation  
                                      (see docstring of class FXAccount for further information on notation conventions)

                               It's sufficient enough, to just provide base|quote ratio.
                               quote|base ratio does not have to be added separately and will be calculated
                               automatically (see self.c_batch_update_exchange_rates).
                               
                               see FXAccount.total_balance for details
        :param reference_currency: std:string
                                   reference_currency
        :return: total_balance: double
        :raises: KeyError: if exchange_rates does not include all currencies listed in account depot
                 ValueError: if exchange rates of base|quote and 1/quote|base do not match up
        """
        # >>>check if all currencies are contained in exchange_rates
        # unpack tuple list to normal list of single currencies
        cdef set ext_currencies
        cdef set int_currencies
        cdef bytes cur_i
        cdef tuple pair_i
        ext_currencies = {cur_i for pair_i in exchange_rates.keys() for cur_i in pair_i}
        # get currencies which are currently in self.depot
        int_currencies = set(self._c_depot.keys())
        # check if int_currencies is a subset of ext_currencies
        if not int_currencies.issubset(ext_currencies):
            raise KeyError('exchange_rates does not include all currencies listed in account depot. '
                           'Currencies in current depot: {}. '
                           'Currencies given by exchange_rates: {}'.format(int_currencies, ext_currencies))

        # >>>calculate total balance
        cdef double balance
        cdef bool_t is_base_quote_notation
        cdef bool_t is_quote_base_notation
        cdef string currency
        cdef double currency_position
        cdef double ex_rate
        cdef double inv_ex_rate

        cdef DictKeysToVec currency_pairs = DictKeysToVec(exchange_rates)

        for currency, currency_position in self._c_depot.items():
            if currency != reference_currency:
                # not in reference currency, so we have to convert
                # only base|quote, but not quote|base
                (is_base_quote_notation, is_quote_base_notation,
                 ex_rate, inv_ex_rate) = currency_pairs.is_tuple_key_in_tuple_vec(currency, reference_currency)
                if is_base_quote_notation:
                    balance = c_precision_add(balance, c_precision_multiply(ex_rate, currency_position))
                elif is_quote_base_notation:
                    balance = c_precision_add(balance, c_precision_divide(currency_position, inv_ex_rate))
                else:
                    # this theoretically should never happen
                    # noinspection PyUnresolvedReferences
                    raise KeyError('{}|{} or {}|{} are not included in '
                                   'exchange_rates.'.format(currency.decode(), reference_currency.decode(),
                                                            reference_currency.decode(), currency.decode()))
                # if both notation variants are present in exchange_rate, then we have to check, if both rates are
                # equivalent (respectively, one of them is inverted to check equality)
                if is_base_quote_notation and is_quote_base_notation:
                    if ex_rate != c_precision_divide(1, inv_ex_rate):
                        raise ValueError('Exchange rates of base|quote and 1/quote|base do not match up.')
            else:
                # already in reference currency, so just add
                balance = c_precision_add(balance, currency_position)

        self._c_is_exchange_rate_updated = False

        return balance

    @cython.wraparound(False)
    cpdef double c_position(self, string currency) except? -1.7e+250:
        """
        C++ implementation via cython. Is wrapped by FXAccount. See FXAccount.position for further information.
        
        Returns current position size.
        
        :param currency: std:string
        :return: position: double, volume of currency
        """
        cdef double pos

        try:
            return self._c_depot[currency]
        except KeyError:
            return 0


# noinspection PyAbstractClass,PyAttributeOutsideInit,PyTypeChecker
class FXAccount(cFXAccount, BaseAccount):
    """
    Derived from BaseAccount. This implementation is meant to model transactions and mechanisms specific to the
    foreign exchange market. Nevertheless the implementation can also be used to model e.g. transactions of stocks
    (with minor adaption such as rounding stocks down to whole).
    Special emphasis is placed on providing a flexible interface to model a variety of situations.

    The package 'trapeza' uses the following FX specific notation for currency pairs (direct quotation notation):
        A currency pair is denoted by base|quote, e.g. €|$.
        The exchange rate of the base|quote pair defines that x volume in quote currency is exchanged for one unit of
        base currency.
        In mathematical terms, the exchange rate of base|quote has the unit of [quote/base], e.g. the exchange rate
        of the €|$-pair has the mathematical unit of [$/€].
        Multiplying the exchange rate by a volume in base currency is equivalent to the exchange direction 'from base
        to quote'. Dividing a volume in quote currency by the exchange rate is equivalent to 'from quote to base'.
        We use 'w' as symbol for the exchange rate of base|quote pair, v_base and v_quote for volumes in base and
        quote currencies.

        Multiplication: v_base * w = v_quote -> [base] * [quote/base] = [quote]  (from base to quote)
        Division:       v_quote / w = v_base -> [quote] * [base/quote] = [base]  (from quote to base)

        This also referred to as 'direct quotation' (versus volume quotation)

    In context of the above defined notation, sell and buy transactions are defined as follows:
        Buy: Buy the base currency and sell the quote currency.
             (in other words: receive units in base currency in exchange for quote currency)
             In market context, buy transactions are performed at the ask price
        Sell: Sell the base currency and buy the quote currency.
              (in other words: receive units in quote currency in exchange for base currency)
              Sell transactions are performed at the bid price
        Ask price: price offered to buyer side (from seller)
        Bid price: price offered to seller side (from buyer)
        Normally following relation holds true: aks price > bid price

    FXAccount class tries to model a normal bank depot/ account with all its transaction types. Following transaction
    types are implemented:
        - deposit: deposit money (or assets) onto the account's depot
        - withdraw: withdraw money (or assets) from the account's depot
        - buy: buy a base|quote currency; base can either be an other currency or any asset (e.g. stock)
        - sell: sell a base|quote currency; base can either be an other currency or any asset (e.g. stock)
        - transfer: transfer money (or assets) from own account onto an other account (which at least must be derived
                    from trapeza.account.base_account.BaseAccount abstract class)
        - collect: collect money (or assets) from an other account (which at least must be derived
                   from trapeza.account.base_account.BaseAccount abstract class) onto own account
    For sell and buy transactions you have to supply the respective market data, e.g. the current exchange rate.
    Thereby it does not matter if the user is selling/buying a currency pair or stocks (which is just
    a stock|currency pair) or anything else like options. Goal of this library is not simulate market data e.g. option
    prices, but to model transaction types. By supplying appropriate market data, the user is free to model transactions
    regarding currency pairs, stocks, options, etc.

    FXAccount is also able to model processing times of a transaction's fulfillment, e.g. if a transaction is not
    executed immediately but needs some time to be filled (transmission time of message, broker execution, etc.).
    This is achieved by implementing a stack automaton alike logic which executes at discrete time steps.
    FXAccount contains an internal clock, which is counted up by calling FXAccount.tick() by  one time step.
    If processing duration of a transaction is set to 0 (default), the respective transaction is filled immediately.
    If processing duration is set to something else than 0, then the respective transaction is filled when the internal
    clock of FXAccount reaches the time step of 'processing duration + time at instructing transaction', e.g.:
        time step 0: instruct sell transaction with processing duration of 2
        time step 1: nothing happens
        time step 2: sell transaction is/ will be conducted
    The time unit can be anything the user wants to choose, e.g. seconds, working days etc.
    Internally, this structure is represented by a stack, which in this case is a heap data structure (we'll call it
    heap from here on). Transactions with larger processing times than 0 will be put onto the heap. At each call to
    FXAccount.tick() the heap will be checked if any delayed transactions are due.

    FXAccount also performs a coverage check, e.g. if a withdraw transaction would lead to a negative account balance.
    This check is also applied to transactions delayed by processing durations at the time of instructing them in order
    to ensure that transactions filled at future time steps will not lead to coverage violations.
    For this kind of coverage check, three possible checks are available:
        1. False or None: omits coverage analysis
        2. 'min_backward': Current clock time and processing duration are added up to the execution time step of
                           respective order. Coverage is checked up to this execution time step. This ensures, that
                           the transaction is conductible at the time due, but does not ensure, that transaction
                           might lead to coverage violations beyond the execution time step.
        3. 'max_forward': The maximum execution time step on the internal heap is taken as reference time step
                          (therefore called max forward). Coverage check is performed up to this reference time step.
                          This ensures, that coverage is given at any time in the future.
    A coverage violation throws an trapeza.exception.CoverageException. See docstring of transaction types on how to
    control exception behavior.
    If checking of marked but not yet billed transactions (self.check_marked_coverage set at __init__) is turned off
    (set to False), then unexpected behavior raises in case a coverage exception occurs (either when trying to perform
    a transaction or during execution of transactions stacked on internal heap (delayed transactions by processing
    times)).

    Furthermore, FXAccount can define transaction fees. Those transaction fees can either be defined by arguments
    passed to the different transaction calls, or can be defined globally, e.g. at __init__ as functions which are then
    automatically applied to the different transactions. Globally defined fees must be functions.
    If fees are defined as functions, they must implement the following call signature:
        (fee_amount, fee_currency, fee_exec_time) = fee(volume, price, base, quote, processing_duration)
            volume: float, given in base (see parameter:base)
            price: float, given in base|quote direct notation (see above for notation convention)
            base: python string, base currency
            quote: python string, quote currency
            processing_duration: int, processing time needed to fill transaction/ until transaction takes effect
                                 on account
    The arguments volume, price, base, quote and processing_duration are the same arguments as used in the call to
    the transaction, e.g. FXAccount.sell(...). They are just passed through to the fee function.
    See docstring of class methods for further details.
    Fee functions can also be set via overwriting class attributes. FXAccount._fee contains a dict:
        FXAccount._fee = {'sell': func, 'buy': func, 'withdraw': func, 'deposit': func}
    If the user wants to overwrite the fee functions, an entire dict has to be provided! Single key-values can not be
    overwritten separately (e.g. FXAccount._fee['sell'] = ... will throw an exception)!
    Collect() and transfer() do not have dedicated fee functions, but invoke those of withdrawal and depositing. Extra
    fees can be submitted via the argument list (in this case fees of depositing and withdrawal are temporarily
    suspended once for this transaction). In general, passing fees via argument list of method calls will take those
    fees into consideration and will temporarily suspend global fees once for the respective transaction.
    Default is not applying any fees.
    The above defined function signature for defining custom fees always takes volume referenced in base currency
    (both are arguments of custom defined fee function) and always takes python strings as inputs (no encoding etc.
    needed).

    FXAccount keeps track of all positions in its depot. FXAccount.position(currency) returns the current position size
    of currency (or any other asset).
    FXAccount.total_balance returns the total value of the account's depot expressed in the reference currency
    (set at __init__).
    FXAccount.total_balance can be called directly when passing exchange rates to it (keys: tuple of strings
    expressing base and quote, value: float). Otherwise self.batch_update_exchange_rates (or self.update_exchange_rate,
    which is not recommended) has to be called beforehand (if self.total_balance shall be called without any
    arguments).
    FXAccount.position does not need any updating beforehand.
    .update_exchange_rate and .batch_update_exchange_rates do not affect internal heap of delayed transactions or the
    internal clock.
    FXAccount.position and FXAccount.total_balance are just (so to speak) snapshots at the current internal clock time.
    Do not forget to call FXAccount.tick() to proceed in time and to execute transactions delayed by processing times.

    FXAccount also has the option of type checking, which can be set at __init__. If set to False, each class method
    checks if the arguments passed to it are of the right data type. This adds some safety by additional checks but
    costs performance. If set to True, type checking will be ignored. Default is type checking being active.

    Quickstart:
    >> acc = FXAccount('EUR')   # reference currency is in EUR
    >> acc.deposit(100, 'EUR')  # deposit 100 EUR onto account
    >> acc.tick()               # proceed one time step, nothing's gonna happen here...
    >> acc.sell(10, 1, 'EUR', 'TPZ')    # exchange 10 EUR against fictive currency TPZ
    >> print(acc.total_balance({('EUR', 'TPZ'): 1}
    >> >> 100
    >> acc.sell(10, 1, 'EUR', 'TPZ', fee= 1, processing_duration=1)     # transaction is delayed, fee in base
    >> print(acc.total_balance({('EUR', 'TPZ'): 1}
    >> >> 100
    >> acc.tick()       # this will lead to filling delayed transaction
    >> print(acc.depot)
    >> >> {'EUR': 79, 'TPZ': 20}    # 1 EUR fee is subtracted
    """

    @property
    def exec_heap(self):
        """
        Returns internal heap of delayed transactions. Internally the heap is implemented as C++ vector int the
        cFXAccount class.
        :return: (heap) list of lists,
                 each sub-list is structured as follows:
                    [int:execution_time, str:transaction_type, float:volume, str:currency, str:coverage]
                 transaction_type is {'c_deposit', 'c_withdraw'} (or {'deposit', 'withdraw'}, gets automatically parsed
                    to 'c_withdraw' and 'c_deposit')
                 coverage: see docstring of FXAccount.deposit() or .withdraw()
                 str denotes normal python string type
        """
        return ProtectedExecHeap(self.vec_heap.tolist())
    @exec_heap.setter
    def exec_heap(self, inp):
        """
        Set internal heap (and underlying C++ vector implementation). See getter method for further information.
        :param inp: list of lists (see getter) or None
        :return: None
        """
        inp = self._parse_exec_heap(inp, self._c_ignore_type_checking)
        self.vec_heap = cFXWrapperVectorHeap(inp)
    @exec_heap.deleter
    def exec_heap(self):
        del self.exec_heap

    @property
    def check_marked_coverage(self):
        """
        Returns status of self.check_marked_coverage which denotes how coverage analysis is conducted for marked but
        not yet booked delayed transactions.
        :return: {False, 'min_backward', 'max_forward'}
        """
        if self._c_check_marked_coverage == 0:
            return False
        elif self._c_check_marked_coverage == 1:
            return 'min_backward'
        elif self._c_check_marked_coverage == 2:
            return 'max_forward'
        else:
            raise tpz_exception.OperatingError('Internal logic error. Value in underlying c-implementation (cython) is '
                                              'set to an invalid value.')
    @check_marked_coverage.setter
    def check_marked_coverage(self, inp):
        """
        Set type of coverage analysis.
        :param inp: {None, False, 'min_backward', 'max_forward'}
                    or 0 (None/ False), 1 ('min_forward'), 2 ('max_forward')
        :return: None
        :raises: TypeError
        """
        if inp is None or inp is False:
            self._c_check_marked_coverage = 0
        elif inp == 'min_backward':
            self._c_check_marked_coverage = 1
        elif inp == 'max_forward':
            self._c_check_marked_coverage = 2
        elif inp in [0, 1, 2]:
            self._c_check_marked_coverage = inp
        else:
            raise TypeError('check_marked_coverage must be in {None, False, "max_forward", "min_backward"}.')
    @check_marked_coverage.deleter
    def check_marked_coverage(self):
        del self.check_marked_coverage

    @property
    def clock(self):
        """
        Return current internal clock.
        :return: int
        """
        return self._c_clock
    @clock.setter
    def clock(self, inp):
        """
        Set current internal clock. It is not recommended to manually set internal clock, but use self.tick() instead.
        :param inp: int >= 0
        :return: None
        :raises: ValueError (inp < 0) or TypeError (inp not int)
        """
        try:
            if inp < 0:
                raise ValueError('Internal clock must be set to >=0.')
            elif not int(inp) == inp:
                raise TypeError('Only integers for setting internal clock.')
            else:
                self._c_clock = inp
        except Exception as e:
            raise e
    @clock.deleter
    def clock(self):
        del self.clock

    @property
    def _ignore_type_checking(self):
        """
        Returns whether type checking is ignored or not.
        :return: bool
        """
        # readonly access (cython extension type)
        return self._c_ignore_type_checking

    @property
    def depot(self):
        """
        Return current depot and it's positions. Returned dict is not manipulable/ mutable. Use setter method instead.
        :return: dict, keys: str:currency, value: float:position_size
        """
        return ProtectedDict((k.decode(), v) for k, v in self._c_depot.items())
    @depot.setter
    def depot(self, inp):
        """
        Set depot by providing a complete dict of all new positions
        :param inp: dict with key str:currency, value: float
        :return: None
        :raises: TypeError
        """
        check_types([inp], [dict], ['depot_setter'], self._c_ignore_type_checking)
        self._c_depot = self._parse_depot(inp, self._c_ignore_type_checking)
    @depot.deleter
    def depot(self):
        del self.depot

    @property
    def _fee(self):
        """
        Return current set fees. Returned dict is not manipulable/ mutable. Use setter method instead.
        :return: dict, keys:{'sell', 'buy', 'withdraw', 'deposit'}, values: function
        """
        return ProtectedDict((k.decode(), v) for k, v in self._c_fee.items())
    @_fee.setter
    def _fee(self, inp):
        """
        Set new fees by providing a dict. Dict can contain keys:{'sell', 'buy', 'withdraw', 'deposit'}. If one of the
        keys is missing in inp, then the current internal setting for this key will be taken over and re-used.
        :param inp: dict, keys:{'sell', 'buy', 'withdraw', 'deposit'}, values: function
        :return: None
        :raises: TypeError
        """
        try:
            if type(inp) != dict:
                raise TypeError
            _fee_tmp_dict = {}
            _fee_keys = ['buy', 'sell', 'deposit', 'withdraw']
            for _f_key in _fee_keys:
                if _f_key in inp.keys():
                    _fee_tmp_dict[_f_key] = inp[_f_key]
                else:
                    _fee_tmp_dict[_f_key] = self._c_fee[_f_key.encode()]
            if len(set(list(inp.keys())) - set(_fee_keys)) > 0:
                raise KeyError
            self._c_fee = self._parse_fees(_fee_tmp_dict['buy'], _fee_tmp_dict['sell'],
                                           _fee_tmp_dict['deposit'], _fee_tmp_dict['withdraw'],
                                           self._c_ignore_type_checking)
        except TypeError:
            raise TypeError('_fee setter argument must be dict with fee["buy"], fee["sell"], fee["deposit"] '
                            'and fee["withdraw"]. See docstring of FXAccount for further information about fee '
                            'handling.')
        except KeyError:
            raise KeyError('_fee setter argument must be dict with fee["buy"], fee["sell"], fee["deposit"] '
                            'and fee["withdraw"]. See docstring of FXAccount for further information about fee '
                            'handling.')
    @_fee.deleter
    def _fee(self):
        del self._fee

    @property
    def exchange_rates(self):
        """
        Returns current exchange rates (which was previously provided by self.tick(...), self.update_exchange_rate(...)
        or self.batch_update_exchange_rates(...)) as dict which is not manipulable/ mutable. Use setter method instead.
        :return: dict with keys:tuple of str:currency (currency pair) and values:float
        """
        return ProtectedDict(((k[0].decode(), k[1].decode()), v) for k, v in self._c_exchange_rates.items())
    @exchange_rates.setter
    def exchange_rates(self, inp):
        """
        Set new exchange rates as complete dict of all currency pairs. Must contain all currency pairs which are also
        contained in self.depot, otherwise self.total_balance will throw an exception. Doesn't matter if keys are
        noted as base|quote or quote|base as rates are automatically inverted to base|self.reference_currency (when
        calling FXAccount.total_balance).
        :param inp: dict with keys:tuple of str:currency (currency pair) and values:float
        :return: None
        :raises: TypeError
        """
        check_types([inp], [dict], ['exchange_rates_setter'], self._c_ignore_type_checking)
        self._c_exchange_rates = self._parse_exchange_rates(inp, self._c_ignore_type_checking)
    @exchange_rates.deleter
    def exchange_rates(self):
        del self.exchange_rates

    @property
    def reference_currency(self):
        """
        Return reference currency used for calculating total balance/ value of depot and fees.
        :return: str
        """
        return self._c_reference_currency.decode()
    @reference_currency.setter
    def reference_currency(self, inp):
        """
        Set new reference currency.
        :param inp: str
        :return: None
        :raises: TypeError
        """
        check_types([inp], [str], ['inp'])
        self._c_reference_currency = inp.encode()
    @reference_currency.deleter
    def reference_currency(self):
        del self.reference_currency

    @property
    def is_exchange_rate_updated(self):
        """
        Returns whether internal exchange rates have been updated and self.total_balance() is ready to be called.
        :return: bool
        """
        return self._c_is_exchange_rate_updated
    @is_exchange_rate_updated.setter
    def is_exchange_rate_updated(self, inp):
        """
        Set internal status whether exchange rates have been updated and self.total_balance() is
        ready to be called. It is not recommended to set this value manually.
        :param inp: bool
        :return: None
        :raises: TypeError
        """
        check_types([inp], [bool], ['is_exchange_rate_updated_setter'])
        self._c_is_exchange_rate_updated = inp
    @is_exchange_rate_updated.deleter
    def is_exchange_rate_updated(self):
        del self.is_exchange_rate_updated

    @property
    def prohibit_debiting(self):
        """
        Return whether debiting of account is allowed or not.
        :return: bool
        """
        return self._c_prohibit_debiting
    @prohibit_debiting.setter
    def prohibit_debiting(self, inp):
        """
        Set internally whether debiting of account is allowed. It is not recommended to set this value manually as it
        might mess up internal heap execution.
        :param inp: bool
        :return: None
        :raises: TypeError
        """
        check_types([inp], [bool], ['prohibit_debiting_setter'])
        self._c_prohibit_debiting = inp
    @prohibit_debiting.deleter
    def prohibit_debiting(self):
        del self.prohibit_debiting

    def __init__(self, reference_currency, depot=None,
                 fee_buy=False, fee_sell=False, fee_deposit=False, fee_withdraw=False,
                 exec_heap=None, long clock=0, exchange_rates=None, marked_coverage='min_backward',
                 prohibit_debiting=False, ignore_type_checking=False):
        """
        Inherits from base class account of trapeza.account.base_account.BaseAccount.
        Account for managing buy, sell, withdrawal, deposit,
        transfer (between accounts derived from trapeza.account.base_account.BaseAccount) and
        collect (between accounts derived from trapeza.account.base_account.BaseAccount) of FX trading transactions.
        Customizable fee structure. Accounts for transaction processing durations by implementing time-state-logic
        (comparable to stack automaton).
        Call self.tick() for proceeding one time unit and to make transactions take effect if they incur transaction
        processing duration.
        This class is mainly a wrapper around cFXAccount, which is a more efficient C++ implementation.

        :param reference_currency: str
                                   reference currency for calculating fees, total balance, etc.
        :param depot: {dict(currency: volume), None}, default=None
                      Dictionary which keeps track of depot assets.
                      depot=None initializes empty dictionary.

                      currency: str (key)
                      volume: float (value)
        :param exec_heap: heapq (list) of lists: [time, action_func, volume, currency, coverage], default=None
                          Heap that stores transactions which take place at future time steps (e.g. due to processing
                          duration) and is executed at each clock cycle (self.tick()).
                          Exec_heap=None initializes an empty heap.

                          time: int, in clock cycles/ time base units (starting from 0)
                          action_func: {'c_withdraw', 'c_deposit'} (or {'withdraw', 'deposit'}: gets parsed to
                                        'c_withdraw' and 'c_deposit')
                          volume: float
                          currency: str
                          coverage: str (see docstring FXAccount.deposit() or .withdraw().
                          str as python strings
        :param clock: int, default=0
                      internal clock in time base units (or any units the user wishes to define) for event handling
                      such as transactions delayed by a certain transaction time for filling/ fulfillment.
                      Increased by one unit when self.tick() is called.
        :param fee_buy: {func, False}, default=False
                        False: no fee applied
                        func: function describing fee structure with signature as follows
                              (fee_amount,
                               fee_currency,
                               fee_exec_time) = fee(volume, price, base, quote, processing_duration)
                              func must follow above signature
                              volume, price, base, quote, processing_duration are the same as used within respective
                              transaction call (in this case FXAccount.buy()). Those arguments are just passed through
                              from there.
        :param fee_sell: see fee_buy
        :param fee_withdraw: see fee_buy,
                             if func: fee_amount, fee_currency, fee_exec_time
                                        = fee(volume, price, base, quote, processing_duration)
                                        = fee(volume, None, currency, currency, processing_duration)
                                      base input is pre-set to/ called with hardcoded param:currency
                                      price input is pre-set to/ called with hardcoded None
                                      quote input is pre-set to/ called with hardcoded param:currency
                             also applied at transfer
        :param fee_deposit: see fee_buy
                             if func: fee_amount, fee_currency, fee_exec_time
                                        = fee(volume, price, base, quote, processing_duration)
                                        = fee(volume, None, currency, currency, processing_duration)
                                      base input is pre-set to/ called with hardcoded param:currency
                                      price input is pre-set to/ called with hardcoded None
                                      quote input is pre-set to/ called with hardcoded param:currency
                             also applied at collect
        :param exchange_rates: {dict, None}, default=None
                               if None, self.exchange_rates is initialized as empty dict

                               key: (base, quote) --> (from_currency, to_currency) see docstring of class for a
                                    description of the notation convention in use.
                                    Should contain all currency pairs of depot positions w.r.t. reference currency
                                    (otherwise there might be a risk that other functions of FXAccount might throw an
                                    exception due to data corruption. Data corruption might or might not occur, but
                                    if it occurs, it will definitely throw an exception).
                                    Doesn't matter if keys are supplied as base|quote or quote|base as rates will be
                                    inverted automatically to match currency|reference_currency.
                                    base: str
                                    quote: str
                               value: float,
                                      exchange_rate of base|quote FX pair

                               (!!!) use FX notation described in docstring of class (!!!)
                               1.2 USD|EUR (FX) --> 1.2 EUR/USD (mathematical unit)
                               --> 1 USD * 1.2 EUR/USD == 1.2 EUR --> exchange_rate['USD', 'EUR']=1.2

                               It's sufficient enough, to just provide base|quote ratio or quote|base ratio (just one
                               of them, the inverse is calculated automatically).
        :param marked_coverage: {False, None, 'max_forward', 'min_backward'}, default = 'min_backward'
                                      whether to check if marked but not yet booked transactions might lead to future
                                      coverage violation.

                                      None or False: No coverage checking
                                      'max_forward': Get the maximum time_step in current heap and check if insertion
                                                     of transaction into internal heap leads to coverage violation
                                                     at any time_step (therefore called max_forward, as we look
                                                     forward into future up to max time horizon within heap).
                                                     This checks, if any insertion of transaction might lead to a
                                                     coverage exception at any given time_step.
                                      'min_backward': Take time_step given by processing_duration of transaction method
                                                      call, and check if coverage
                                                      is given up to this time_step. Therefore coverage is only checked
                                                      whether specific transaction can be filled without coverage
                                                      violation, but does not check, if transaction might lead to
                                                      future coverage violations.

                                      - if {'max_forward', 'min_backward'}: throws trapeza.exception.CoverageError if
                                        future coverage is violated
                                      - if None or False: no coverage check of marked but not yet booked transactions.
                                        This is independent from the 'coverage' of a transaction's method argument of
                                        transaction methods which only checks coverage at the time of calling the
                                        transaction method (e.g. whether depot is covered just at the moment).
        :param prohibit_debiting: {False, True}, default=False
                                  if True: no negative positions allowed at time of a transaction's execution
                                           !!! CoverageError is only thrown at _exec_heap(). This is not a good and
                                           proper warning, but just a safety backup !!!
                                  if False: negative positions are allowed. If self.check_marked_coverage is set to
                                            None, then debiting might really occur.
        :param ignore_type_checking: bool,
                                     if True, type checking is omitted, which increases performance but is less safe
        :raises: TypeError: if argument types are not of specified types

        :TODO: integrate Futures, Options and other Derivatives? (add function which executes derivative; treat
               derivatives as currency strings regarding sell(), buy() and push to exec_heap)
        :TODO: reduce complexity in deposit(), withdraw(), transfer(), collect() and total_balance()
        :TODO: implement rollover
        :TODO: remove empty positions/ positions equal to zero from self.depot dict (?)
        :TODO: insert additional abstraction layer to define persistent fee models in order to avoid specifying
               fee terms separately every time when calling transactions methods, implementation similar to
               order_management.monkey_patch()
        :TODO: [prevent setting underlying c_attributes directly (e.g. _fee, see unit tests for examples): not sure
                if this really possible or necessary as those attributes are not exposed to the user anyway...]
        """
        check_types([ignore_type_checking], [bool], ['ignore_type_checking'], False)

        # >>>type checking
        check_types([reference_currency, clock, prohibit_debiting],
                    [str, int, bool],
                    ['base_currency', 'clock', 'prohibit_debiting'], ignore_type_checking)
        if marked_coverage is None or marked_coverage is False:
            marked_coverage = 0
        elif marked_coverage == 'min_backward':
            marked_coverage = 1
        elif marked_coverage == 'max_forward':
            marked_coverage = 2
        if marked_coverage not in [0, 1, 2]:
            raise TypeError('check_marked_coverage must be in {None, False, "max_forward", "min_backward"}.')
        if not ignore_type_checking:
            if fee_buy is not False:
                check_types([fee_buy], [callable], ['fee_buy'], False)
            if fee_sell is not False:
                check_types([fee_sell], [callable], ['fee_sell'], False)
            if fee_deposit is not False:
                check_types([fee_deposit], [callable], ['fee_deposit'], False)
            if fee_withdraw is not False:
                check_types([fee_withdraw], [callable], ['fee_withdraw'], False)

        # >>>depot: key: currency, value: volume -> parse str keys to bytes keys to be compatible with C implementation
        #    of cFXAccount
        depot = self._parse_depot(depot, ignore_type_checking)

        # >>>heap: (time, action_func, volume, currency, **kwargs)
        exec_heap = self._parse_exec_heap(exec_heap, ignore_type_checking)

        # >>>parse fees: parse str keys to bytes keys to be compatible with C implementation of cFXAccount
        fee_dict = self._parse_fees(fee_buy, fee_sell, fee_deposit, fee_withdraw, ignore_type_checking)

        # >>>exchange rates: parse str keys to bytes keys to be compatible with C implementation of cFXAccount
        exchange_rates =self._parse_exchange_rates(exchange_rates, ignore_type_checking)
        # >>>parse str keys to bytes keys to be compatible with C implementation of cFXAccount

        if not ignore_type_checking:
            check_types([depot, exec_heap, fee_dict, exchange_rates],
                        [dict, list, dict, dict],
                        ['depot', 'exec_heap', 'fee_dict', 'exchange_rates'], False)

        super().__init__(reference_currency.encode(), depot, fee_dict, exec_heap, clock, exchange_rates,
                         marked_coverage, prohibit_debiting, ignore_type_checking)

    def _full_reset(self):
        """
        Resets account with depot=None, fee_x=False (e.g. fee_buy), check_marked_coverage='min_backward', empty heap,
        clock=0 and empty exchange_rate dict. Only initial reference_currency is retained. See docstring of __init__
        for further information.
        :return: None
        """
        self.__init__(self._c_reference_currency.decode())

    def _reset(self):
        """
        Resets account but retains reference_currency, check_marked_coverage, prohibit_debiting, ignore_type_checking
        and fee_x (e.g. fee_buy). Depot, heap and exchange_rate dict are set to empty, clock is set to 0. See docstring
        of __init__ for further information.
        :return: None
        """
        self._c_reset()

    def _check_is_valid_fee_func(self, func):
        """
        Checks if function is a valid function for fees and complies with following signature
        fee_amount, fee_currency, fee_exec_time = fee(volume, price, base, quote, processing_duration)
        :param func: func
        :return: None
        :raises: TypeError
        """
        result = func(1, 1, 'X', 'Y', 1)
        if len(result) != 3:
            raise TypeError
        check_types([result[0], result[1], result[2]], [float, str, float],
                    ['fee_amount', 'fee_currency', 'fee_processing_duration'], self._c_ignore_type_checking)

    @staticmethod
    def _parse_depot(depot, ignore_type_checking):
        """
        Parses and checks init arguments
        :param depot: dict(currency: volume) with currency as string and volume as float or None
        :param ignore_type_checking: bool,
                                     if True, type checking is omitted, which increases performance but is less safe
        :return: dict (currency: volume) with currency as string and volume as float encoded for passing to underlying
                 C++ implementation
        :raises: TypeError
        """
        if depot is None:
            depot = dict()
        else:
            check_types([depot], [dict], ['depot'], ignore_type_checking)
            for currency, volume in depot.items():
                check_types([currency, volume], [str, float], ['currency in depot', 'currency volume in depot'],
                            ignore_type_checking)
            depot = {k.encode(): v for k, v in depot.items()}
        return depot

    @staticmethod
    def _parse_exec_heap(exec_heap, ignore_type_checking):
        """
        Parses and checks if provided (heap) list is valid as internal execution heap
        :param exec_heap: heapq (list) of lists: [int:time, str:action_func, float:volume, str:currency, str:coverage]
                          or None
                          if None: empty heap
        :return: parsed input as list of lists
        :raises: TypeError
        """
        has_warn = False
        has_risen = False

        # heap: [time:int, action_func:str, volume:float, currency:str, coverage:str]
        if exec_heap is None:
            exec_heap = []
        elif type(exec_heap) in [tuple, list] and len(exec_heap) == 0:
            exec_heap = []
        else:
            try:
                _ = len(exec_heap[0])  # this will throw an exception if 1D list
                # if no exception, exec_heap is list of tuples or list of list
                if tuple(exec_heap) == exec_heap:
                    # convert 2D tuple such that at leas outer container is list
                    exec_heap = list(exec_heap)
                elif not list(exec_heap) == exec_heap:
                    has_risen = True
                    raise TypeError('exec_heap must be either list of list, tuples of lists, tuple of a single entry'
                                    'to exec_heap or list of single entry to exec_heap. Single entry to exec_heap'
                                    'consists of: [int:time, str:action_func, float:volume, str:currency, '
                                    'str:coverage]')
            except KeyError:
                raise TypeError('exec_heap must be either list of list, tuples of lists, tuple of a single entry'
                                'to exec_heap or list of single entry to exec_heap. Single entry to exec_heap'
                                'consists of: [int:time, str:action_func, float:volume, str:currency, str:coverage]')
            except (TypeError, IndexError):
                if has_risen:
                    raise TypeError('exec_heap must be either list of list, tuples of lists, tuple of a single entry'
                                    'to exec_heap or list of single entry to exec_heap. Single entry to exec_heap'
                                    'consists of: [int:time, str:action_func, float:volume, str:currency, '
                                    'str:coverage]')
                else:
                    # exception indicates, that exec heap is 1D -> turn it into 2D array for heapify
                    exec_heap = [exec_heap]

            # turn list into heap
            heapq.heapify(exec_heap)

            # do type checking
            for i, element in enumerate(exec_heap):
                # [time:int, action_func:str, volume:float, currency:str, coverage:str]
                if type(element) is tuple:
                    exec_heap[i] = list(element)
                    element = exec_heap[i]

                if len(element) < 5:
                    raise TypeError('Single entry to exec_heap consists of: [int:time, str:action_func, float:volume, '
                                    'str:currency, str:coverage]. Only {} elements were given '
                                    'as single entry to exec_heap. Either a single entry or a list of single entries '
                                    'can be used to set exec_heap manually.'.format(len(element)))

                if element[1] in ['withdraw', 'deposit']:
                    exec_heap[i][1] = ''.join(['c_', element[1]])
                    if has_warn is False:
                        warnings.warn('Auto-converting "withdraw" and "deposit" to "c_withdraw" and "c_deposit" (to '
                                      'match up cython-implemented exec_heap of cFXAccount, which wrapped is by '
                                      'FXAccount).')
                        has_warn = True
                elif element[1] in ['c_withdraw', 'c_deposit']:
                    pass
                else:
                    raise TypeError('When setting exec_heap manually, method argument must either be a list or tuple '
                                    'of single entries or a single entry itself as list or tuple of the following '
                                    'elements: [int:time, str:action_func, float:volume, str:currency, '
                                    'str:coverage]. action_func must be either "withdraw" or '
                                    '"deposit", got {}'.format(element[1]))
                if element[4] not in ['except', 'partial', 'debit', 'ignore']:
                    raise ValueError('coverage must be in ["except", "partial", "debit", "ignore"]')
                check_types([element[0], element[1], element[2], element[3], element[4]],
                            [int, str, float, str, str],
                            ['heap_time', 'heap_action_type', 'heap_volume', 'heap_currency', 'heap_coverage'],
                            ignore_type_checking)
        return exec_heap

    def _parse_fees(self, fee_buy, fee_sell, fee_deposit, fee_withdraw, ignore_type_checking):
        """
        Parses and checks fees. Uses standard fee function (equivalent to not applying any fees) if argument is set
        to False.
        :param fee_buy: {False, func}
        :param fee_sell: {False, func}
        :param fee_deposit: {False, func}
        :param fee_withdraw: {False, func}
        :return: dict with {'sell': func, 'buy': func, 'deposit': func, 'withdraw': func}
        :raises: TypeError
        """
        _fee = dict()

        if fee_buy is False:
            _fee[b'buy'] = fx_null_fee
        else:
            check_types([fee_buy], [callable], ['fee_buy'], ignore_type_checking)
            self._check_is_valid_fee_func(fee_buy)
            _fee[b'buy'] = fee_buy
        if fee_sell is False:
            _fee[b'sell'] = fx_null_fee
        else:
            check_types([fee_sell], [callable], ['fee_sell'], ignore_type_checking)
            self._check_is_valid_fee_func(fee_sell)
            _fee[b'sell'] = fee_sell
        if fee_deposit is False:
            _fee[b'deposit'] = fx_null_fee
        else:
            check_types([fee_deposit], [callable], ['fee_deposit'], ignore_type_checking)
            self._check_is_valid_fee_func(fee_deposit)
            _fee[b'deposit'] = fee_deposit
        if fee_withdraw is False:
            _fee[b'withdraw'] = fx_null_fee
        else:
            check_types([fee_withdraw], [callable], ['fee_withdraw'], ignore_type_checking)
            self._check_is_valid_fee_func(fee_withdraw)
            _fee[b'withdraw'] = fee_withdraw

        return _fee

    @staticmethod
    def _parse_exchange_rates(exchange_rates, ignore_type_checking):
        """
        Parses and checks exchange rates.
        :param exchange_rates: dict with keys:tuple(str:currency, str:currency) and value as float or None
        :return: dict encoded for passing to underlying C++ implementation
        :raises: TypeError
        """
        if exchange_rates is None:
            exchange_rates = dict()
        else:
            if not ignore_type_checking:
                check_types([exchange_rates], [dict], ['exchange_rates'], ignore_type_checking)
                # sample check types within dict
                sample_key = list(exchange_rates.keys())[0]
                check_types([sample_key], [tuple], ['exchange_rate_key_tuple'], ignore_type_checking)
                check_types([sample_key[0], sample_key[1]],
                            [str, str],
                            ['exchange_rate_currency', 'exchange_rate_currency'], ignore_type_checking)
                check_types([exchange_rates[sample_key]], [float], ['exchange_rate_value'], ignore_type_checking)
            exchange_rates = {(k[0].encode(), k[1].encode()): v for k, v in exchange_rates.items()}
        return exchange_rates

    @staticmethod
    def _check_alt_fee(alt_fee, str alt_fee_error_msg):
        """
        Checks if param:alt_fee is of type {None, False, callable, float}. If alt_fee is callable method, method
        signature is not checked in detail !!! (see param:fee_buy func definition/ signature at self.__init__())
        :param alt_fee: alternative fee, {None, False, callable, float}
        :param alt_fee_error_msg: str,
                                  for error message when NotImplementedError is raised:
                                  '{} must be of type None, bool, '
                                  'float or func and not of type {}'.format(alt_fee_error_msg, type(alt_fee))
        :return: None
        :raises: NotImplementedError
        """
        try:
            if alt_fee is None or alt_fee is False or callable(alt_fee):
                pass
            elif float(alt_fee) == alt_fee:
                pass
            else:
                raise NotImplementedError('{} must be of type None, bool, '
                                          'float or func and not of type {}'.format(alt_fee_error_msg, type(alt_fee)))
        except (ValueError, TypeError):
            raise NotImplementedError('{} must be of type None, bool, '
                                      'float or func and not of type {}'.format(alt_fee_error_msg, type(alt_fee)))
        except NotImplementedError:
            raise NotImplementedError('{} must be of type None, bool, '
                                      'float or func and not of type {}'.format(alt_fee_error_msg, type(alt_fee)))

    @staticmethod
    def _parse_fee_and_transaction_params(float_fee_currency,
                                          str default_float_currency,
                                          alt_fee, str alt_fee_error_msg, instant_float_fee,
                                          processing_duration):
        """
        Parses parameters regarding fees and transaction. Called by transactions methods.
        :param float_fee_currency: {None, str}, parsed to default_currency if None
        :param default_float_currency: str
        :param alt_fee: alternative fee, {None, False, callable, float}, else raise NotImplementedError
        :param alt_fee_error_msg: str, error message when NotImplementedError is raised:
                                  '{} must be of type None, bool, float or func and not '
                                  'of type {}'.format(alt_fee_error_msg, type(alt_fee)))
        :param instant_float_fee: bool, parsed to False if alt_fee is {None, alt_fee, callable}
        :param processing_duration: {None, int}, parsed to 0 if None
        :return: float_fee_currency: str
                 instant_float_fee: bool
                 processing_duration: int
        :raises: NotImplementedError
        """
        try:
            if alt_fee is None or alt_fee is False or callable(alt_fee):
                instant_float_fee = False
                float_fee_currency = default_float_currency
            elif float(alt_fee) == alt_fee:  # if float, than just pass
                if float_fee_currency is None:
                    float_fee_currency = default_float_currency
            else:
                # alt_fee must be in [func, None, bool, float]
                raise NotImplementedError('{} must be of type None, bool, '
                                          'float or func and not of type {}'.format(alt_fee_error_msg, type(alt_fee)))
        except (TypeError, ValueError):
            raise NotImplementedError('{} must be of type None, bool, '
                                      'float or func and not of type {}'.format(alt_fee_error_msg, type(alt_fee)))
        except NotImplementedError:
            raise NotImplementedError('{} must be of type None, bool, '
                                      'float or func and not of type {}'.format(alt_fee_error_msg, type(alt_fee)))

        if float_fee_currency is None:
            raise NotImplementedError('alt_fee must be in {None, False, func, Float')

        if processing_duration is None:
            processing_duration = 0
        return float_fee_currency, instant_float_fee, processing_duration

    def _check_coverage(self, debit_amount, currency, time_step):
        """
        Only used for unit testing. Thin wrapper for underlying C++ implementation.
        Checks coverage if param:debit_amount is withdrawn including marked withdrawals up to param:time_step in
        param:currency

        DO NOT USE -1 as return value. This is reserved to indicate exception (cython specifics).

        :param debit_amount: float
        :param currency: str
        :param time_step: int
        :return: float or math.inf (if self.check_marked_coverage=False or self.check_marked_coverage=None)
        """
        return self._c_check_coverage(debit_amount, currency.encode(), time_step)

    def _eval_fee(self, str action_type, alt_fee, double volume, double current_rate, str base, str quote,
                  processing_duration):
        """
        Evaluates fee without processing any transaction. Takes processing_duration into account. Used to predict
        fee costs.
        :param action_type: {'buy', 'sell', 'deposit', 'withdraw'},
                            ignored if alt_fee != None
        :param alt_fee: alternative fee, {func, False, None, float}
        :param volume: float
        :param base: str
        :param current_rate: float
        :param quote: str
        :param processing_duration: int
        :return: fee_amount: float
                 fee_currency: str
                 fee_exec_duration: int
        :raises: NotImplementedError if alt_fee is not in {func, False, None, float}
                 ValueError if volume < 0
                 TypeError if volume and price are not float/int or if processing duration is not int
        """
        # >>>sanity check
        if volume < 0:
            raise ValueError

        try:
            if alt_fee is None:  # apply self.fee
                (fee_amount,
                 fee_currency,
                 fee_exec_duration) = self._c_fee[action_type.encode()](volume, current_rate, base, quote,
                                                                        processing_duration)
            elif alt_fee is False:  # no fee
                fee_amount, fee_currency, fee_exec_duration = 0, base, 0
            elif callable(alt_fee):
                try:
                    fee_amount, fee_currency, fee_exec_duration = alt_fee(volume, current_rate, base, quote,
                                                                          processing_duration)
                except (NameError, TypeError):
                    raise NotImplementedError
            elif float(alt_fee) == alt_fee:
                fee_amount, fee_currency, fee_exec_duration = alt_fee, base, processing_duration
            else:
                raise NotImplementedError
        except ValueError:
            raise NotImplementedError
        except NotImplementedError:
            raise NotImplementedError

        # noinspection PyUnboundLocalVariable
        return fee_amount, fee_currency, fee_exec_duration

    def _cum_sum_heap(self, currency, action_func_type, long time_step):
        """
        Only used for unit testing. Thin wrapper for underlying C++ implementation.

        Cumulative sum of all transactions in the defined currency, which are located on the internal heap, up to the
        defined time_step. Internal heap consists entries which are defined by execution time, transaction, etc., see
        docstring of property exec_heap for further details.
        :param currency: str
        :param action_func_type: str
        :param time_step: int
        :return: float
        """
        if action_func_type in ['withdraw', 'deposit']:
            action_func_type = ''.join(['c_', action_func_type])
            warnings.warn('Auto-converting "withdraw" and "deposit" to "c_withdraw" and "c_deposit" (to '
                          'match up cython-implemented exec_heap of cFXAccount, which wrapped is by '
                          'FXAccount).')
        elif action_func_type in ['c_withdraw', 'c_deposit']:
            pass
        else:
            raise TypeError('action_func_type must be "c_withdraw", "c_deposit". "withdraw", "deposit" (auto-'
                            'converting to "withdraw" and "deposit" to "c_..."), got {}'.format(action_func_type))
        return self.vec_heap.cum_sum_heap(currency.encode(), action_func_type.encode(), time_step, self._c_clock)

    def _cum_sum_marked_fund(self, currency, long time_step):
        """
        Only used for unit testing. Thin wrapper for underlying C++ implementation.

        Cumulative sum of depositing orders in heap up to time_step in given currency.
        :param currency: str
        :param time_step: int
        :return: float
        """
        return self.vec_heap.cum_sum_marked_fund(currency.encode(), time_step, self._c_clock)

    def _cum_sum_marked_debit(self, currency, time_step):
        """
        Only used for unit testing. Thin wrapper for underlying C++ implementation.

        Cumulative sum of withdrawal orders in heap up to time_step in given currency.
        :param currency: str
        :param time_step: int
        :return: float
        """
        return self.vec_heap.cum_sum_marked_debit(currency.encode(), time_step, self._c_clock)

    def _fill_fee(self, action_type, alt_fee, volume, price, base, quote, processing_duration,
                  forward_coverage='except'):
        """
        Only used for unit testing.

        Handles fee internally (parsing of arguments and evaluation of fee amount, currency and processing duration)
        and calls self.withdraw(), which takes processing_duration, etc. into account to process fees.
        :param action_type: {'buy', 'sell', 'deposit', 'withdraw'},
                            ignored if alt_fee != None
        :param alt_fee: alternative fee, {func, False, None, float}
        :param volume: float
        :param base: str
        :param price: float
        :param quote: str
        :param processing_duration: int
        :param forward_coverage: str,
                                 propagates coverage from method, from which
                                 self._fill_fee() was called, to self.withdraw()
        :return: fee_volume: float
                 fee_currency: str
                 fee_exec_duration: int
        :raises: NotImplementedError if alt_fee is not in {func, False, None, float}
                 ValueError if volume < 0
        """
        (fee_volume,
         fee_currency,
         fee_exec_duration) = self._eval_fee(action_type=action_type, alt_fee=alt_fee, volume=volume, current_rate=price,
                                             base=base, quote=quote, processing_duration=processing_duration)

        # noinspection PyUnboundLocalVariable
        if fee_volume > 0:
            # noinspection PyUnboundLocalVariable
            self.withdraw(volume=fee_volume, currency=fee_currency, processing_duration=fee_exec_duration,
                          coverage=forward_coverage)
        return fee_volume, fee_currency, fee_exec_duration

    def withdraw(self, volume, currency, fee=None, processing_duration=None, coverage='except', instant_float_fee=False,
                 float_fee_currency=None):
        """
        Withdraws volume given in currency from account.
        Furthermore, processing duration (e.g. transmission time of messages in real-life systems, broker execution,
        etc.) can be modelled.
        Fees can be defined either as function or float. If fee is float, then a separate currency in which to bill fees
        can be defined. Additionally, if fees are float, fees can be withdrawn immediately even though withdrawal of
        transaction volume might take some processing duration. This is controlled via instant_float_fee (bool).

        This is a wrapper around the underlying C++ implementation.

        :param volume: float, >= 0
                       volume given in currency
        :param currency: str
        :param processing_duration: int or None, default=None
                                    processing time (delay) in time base units of internal clock until transaction takes
                                    effect on account's depot
                                    time of execution/ billing = self.clock + processing_duration
                                    None is equivalent to 0 in behavior
        :param fee: {func, False, None, float}, default=None
                               fee setting for withdrawal

                               None: self._fee['withdraw'] is applied which is set at __init__. Default at __init__ is
                                     not applying any fees. See docstring of self.__init__ and docstring of class for
                                     further information about globally applied fees and how to set
                                     self._fee['withdraw']
                               False: no fees at all applied, even if self._fee['withdraw'] is set (overrides globally
                                      set fees: self._fee['withdraw'] will be temporarily ignored for this one
                                      transaction)
                               func: alternative function to self._fee is applied (self._fee['withdraw'] will be
                                     ignored for this one transaction and func will be applied instead)
                                     Must follow call signature:
                                         fee_volume, fee_currency, fee_exec_time
                                              = fee(volume, price, base, quote, processing_duration)
                                              = fee(volume, 1, currency, currency, processing_duration)
                                     base input is pre-set to/ called with hardcoded param:currency
                                     price input is pre-set to/ called with hardcoded 1
                                     quote input is pre-set to/ called with hardcoded param:currency
                               float: constant fee is applied and billed in param:float_fee_currency
                                      if instant_float_fee = False: fee is billed at the same time as set by
                                                                    param:processing_duration (same time step when
                                                                    transaction takes effect on account's depot)
                                      if instant_float_fee = True: fee is billed instantly independent from
                                                                   param:processing_duration of transaction
        :param coverage: {'partial', 'except', 'debit'}, default='except'
                                   Controls exception behavior in case of coverage violation.
                                   This coverage analysis checks whether transaction is conductible in principal (e.g.
                                   if currently account's depot position is sufficient right now) but does not check
                                   against marked but not yet billed transactions.

                                   'partial': partial fulfilment as far as possible (including fees).
                                              Withdrawal volume will be reduced s.t. that coverage conditions are met.
                                              This means, if withdrawal volume + fees is greater than current depot
                                              position, then withdrawal volume will be reduced, such that no debiting
                                              in account's depot positions occurs. If volume and fees are not in the
                                              same currency, this reduction is only performed on the volume (fees might
                                              still cause a coverage violation), amount of fees stays untouched then.
                                              volume is reduced to meet initially calculated fees, fees are not
                                              adapted to reduced volume (guessing interdependency would be hard), s.t.
                                              more fees might be payed than according to reduced volume.
                                              This does not guarantee transaction fulfillment, as this just checks
                                              current depot but does not check against marked but not yet billed
                                              (delayed) transactions, which is done independently of this coverage check
                                   'except': raises trapeza.exception.CoverageError if coverage is violated, which is
                                             the case if withdrawal (including fees) is
                                             greater than current depot position (in same currency as volume)
                                   'debit': temporarily deactivates coverage check of current depot position as well as
                                            coverage check of marked but not yet booked transactions.
                                            If prohibit_debiting is set to False at __init__(), then negative (debt)
                                            positions are possible, else a trapeza.exception.CoverageError will be
                                            thrown at time of execution.

                                    Coverage checking of current depot position is done independently of
                                    self.check_marked_coverage, which additionally checks against marked but not yet
                                    filled future transactions (e.g. if self.check_marked_coverage is set to
                                    'min_backward' or 'max_forward).
                                    'debit' deactivates coverage check regarding future marked, not yet filled
                                    transactions as well as coverage check of current depot positions for this one
                                    transaction (see above).
        :param instant_float_fee: bool, default=False
                                  ONLY APPLIES if fee = float, else ignored
                                  if True, fees are withdrawn instantly independent of processing_duration. This does
                                    not affect processing duration of withdrawing param:volume.
                                  if False, fees are billed at the same time as withdrawing param:volume given by the
                                    processing duration.
        :param float_fee_currency: {str, None}, default=None
                                   currency type to bill fee if fee=float, else ignored
                                   if None or ignored, float_fee_currency is set to param:currency
        :return: int
                 confirmation states --> 0: processing (processing_duration greater 0), 1: executed/ billed
        :raises: TypeError: if parameters do not match specified types
                 NotImplementedError: if coverage not in {'partial', 'except', 'debit'} or fee not
                                      in {None, False, func, float}
                 trapeza.exception.CoverageError: if coverage not sufficient (transaction or fee) depending on
                                                  coverage and if checking of marked transaction is
                                                  switched on
                 trapeza.exception.PositionNAError: if currency (str) or float_fee_currency (str) is not
                                                    in self.depot.keys()
                 ValueError: if volume < 0
        :TODO: when coverage='partial', than recalculate fees according to reducing volume to meet coverage
        :TODO:  volume-depot + f(volume-x) -x = 0 --> min
        """
        # >>>parsing inputs
        (parsed_fee_currency,
         instant_float_fee,
         processing_duration) = self._parse_fee_and_transaction_params(float_fee_currency, currency,
                                                                       fee, 'withdrawal_fee',
                                                                       instant_float_fee, processing_duration)

        # >>>sanity and type checking
        if volume < 0:
            raise ValueError('volume must be grater than 0.')

        check_types([volume, currency, processing_duration, parsed_fee_currency, instant_float_fee, coverage],
                    [float, str, int, str, bool, str],
                    ['volume', 'currency', 'processing_duration', 'float_fee_currency', 'instant_float_fee',
                     'coverage'], self._c_ignore_type_checking)
        self._c_isin_depot(currency.encode())

        # >>>evaluate fees
        (fee_volume,
         fee_currency,
         fee_exec_duration) = self._eval_fee(action_type='withdraw', alt_fee=fee, volume=volume,
                                             current_rate=1, base=parsed_fee_currency, quote=currency,
                                             processing_duration=processing_duration * (1 - instant_float_fee))

        # >>>handle coverage exception
        if coverage not in ['except', 'partial', 'debit']:
            raise NotImplementedError('coverage must be {"except", "partial", "debit"}.')

        return self.c_withdraw(volume, currency.encode(), processing_duration, fee_volume, fee_currency.encode(),
                               fee_exec_duration, coverage.encode(), instant_float_fee)

    def deposit(self, volume, currency, fee=None, processing_duration=None, coverage='except', instant_float_fee=False,
                float_fee_currency=None):
        """
        Deposits volume given in currency onto account.
        Furthermore, processing duration (e.g. transmission time of messages in real-life systems, broker execution,
        etc.) can be modelled.
        Fees can be defined either as function or float. If fee is float, then a separate currency in which to bill fees
        can be defined. Additionally, if fees are float, fees can be withdrawn immediately even though depositing of
        transaction volume might take some processing duration. This is controlled via instant_float_fee (bool).

        This is a wrapper around the underlying C++ implementation.

        :param volume: float, >= 0
                       volume given in currency
        :param currency: str
        :param processing_duration: int or None, default=None
                                    processing time (delay) in time base units of internal clock until transaction takes
                                    effect on account's depot
                                    time of execution/ billing = self.clock + processing_duration
                                    None is equivalent to 0 in behavior
        :param fee: {func, False, None, float}, default=None
                            fee setting for depositing

                            None: self._fee['deposit'] is applied which is set at __init__. Default at __init__ is
                                  not applying any fees. See docstring of self.__init__ and docstring of class for
                                  further information about globally applied fees and how to set self._fee['deposit']
                            False: no fees at all applied, even if self._fee['deposit'] is set (overrides globally
                                   set fees: self._fee['deposit'] will be temporarily ignored for this one
                                   transaction)
                            func: alternative function to self._fee is applied (self._fee['deposit'] will be ignored
                                  for this one transaction and func will be applied instead)
                                  Must follow call signature:
                                      fee_volume, fee_currency, fee_exec_time
                                           = fee(volume, price, base, quote, processing_duration)
                                           = fee(volume, 1, currency, currency, processing_duration)
                                  base input is pre-set to/ called with hardcoded param:currency
                                  price input is pre-set to/ called with hardcoded 1
                                  quote input is pre-set to/ called with hardcoded param:currency
                            float: constant fee is applied and billed in param:float_fee_currency
                                   if instant_float_fee = False: fee is billed at the same time as set by
                                                                 param:processing_duration (same time step when
                                                                 transaction takes effect on account's depot)
                                   if instant_float_fee = True: fee is billed instantly independent from
                                                                param:processing_duration of transaction
        :param coverage: {'except', 'debit'}, default='except'
                                   Controls exception behavior in case of coverage violation.
                                   This coverage analysis checks whether transaction is conductible in principal (e.g.
                                   if currently account's depot position is sufficient right now) but does not check
                                   against marked but not yet billed transactions.

                                   'except': raises trapeza.exception.CoverageError if coverage is violated, which is
                                             the case if fee is greater than current depot position (in same currency
                                             as fee)
                                   'debit': temporarily deactivates coverage check of current depot position as well as
                                            coverage check of marked but not yet booked transactions. If
                                            prohibit_debiting is set to False at __init__(), then negative (debt)
                                            positions are possible, else a trapeza.exception.CoverageError will be
                                            thrown at time of execution.

                                   Coverage checking of current depot position is done independently of
                                   self.check_marked_coverage, which additionally checks against marked but not yet
                                   filled future transactions (e.g. if self.check_marked_coverage is set to
                                   'min_backward' or 'max_forward).
                                   'debit' deactivates coverage check regarding future marked, not yet filled
                                   transactions as well as coverage check of current depot positions (see above).

                                   'partial' makes no sense in this context. See comments in source code of
                                   cFXAccount.c_deposit for further information.
        :param instant_float_fee: bool, default=False
                                  ONLY APPLIES if fee = float, else ignored
                                  if True, fees are withdrawn instantly independent of processing_duration. This does
                                    not affect processing duration of withdrawing param:volume.
                                  if False, fees are billed at the same time as withdrawing param:volume given by the
                                    processing duration.
        :param float_fee_currency: {str, None}, default=None
                                   currency type to bill fee if fee=float, else ignored
                                   if None or ignored, float_fee_currency is set to param:currency
        :return: int
                 confirmation states --> 0: processing (processing_duration greater 0), 1: executed/ billed
        :raises: TypeError if parameters do not match specified types
                 NotImplementedError: if coverage not in {'partial', 'except', 'debit'} or fee not
                                      in {None, False, func, float}
                 trapeza.exception.CoverageError: if coverage not sufficient (transaction or fee) depending on
                                                  coverage and if checking of marked transaction is
                                                  switched on
                 trapeza.exception.PositionNAError: if currency (str) or float_fee_currency (str) is not
                                                    in self.depot.keys()
                 ValueError: if volume < 0
        :TODO: when coverage='partial', than recalculate fees according to reducing volume to meet coverage
        :TODO:  volume-depot + f(volume-x) -x = 0 --> min
        :TODO: optimize performance of underlying cython implementation
        """
        # >>>parsing inputs
        (parsed_fee_currency,
         instant_float_fee,
         processing_duration) = self._parse_fee_and_transaction_params(float_fee_currency, currency,
                                                                       fee, 'deposit_fee', instant_float_fee,
                                                                       processing_duration)

        # >>>sanity and type checking
        if volume < 0:
            raise ValueError('volume must be grater than 0.')

        check_types([volume, currency, processing_duration, parsed_fee_currency, instant_float_fee, coverage],
                    [float, str, int, str, bool, str],
                    ['volume', 'currency', 'processing_duration', 'float_fee_currency', 'instant_float_fee',
                     'coverage'], self._c_ignore_type_checking)

        # >>>evaluate fees
        (fee_volume,
         fee_currency,
         fee_exec_duration) = self._eval_fee(action_type='deposit', alt_fee=fee, volume=volume, current_rate=1,
                                             base=parsed_fee_currency, quote=currency,
                                             processing_duration=processing_duration * (1 - instant_float_fee))

        # >>>handle coverage exception induced by fees
        if coverage not in ['except', 'debit']:
            raise NotImplementedError('coverage must be {"except", "debit"}.')

        return self.c_deposit(volume, currency.encode(), processing_duration, fee_volume, fee_currency.encode(),
                              fee_exec_duration, coverage.encode(), instant_float_fee)

    def collect(self, payer_account, double volume, str currency, payee_fee=False, payer_fee=False,
                payee_processing_duration=None, payer_processing_duration=None):
        """
        Collects payment volume in given currency from payer account to this:account.
        Furthermore, processing duration (e.g. transmission time of messages in real-life systems, broker execution,
        etc.) can be modelled.
        Fees can be defined either as function or float for payer and payee. If payee_fee=None and payer_fee=None, then
        the standard and globally set fees of self._fee['deposit'] and self._fee['withdraw'] (which are set at __init__)
        will be applied. If None (default), no fees will be applied

        If payer_fee or payer_processing_duration shall be applied, then payer class must implement
        payer_account.withdraw(volume, currency, payer_fee, payer_processing_duration)

        Coverage analysis is conducted with default arguments of withdraw() and deposit()
        (e.g. coverage='except', instant_float_fee=False)

        !!! If execution is not instant (e.g. processing_duration is not None), both accounts have to call .tick() to
            make transaction take effect on both accounts. It is not sufficient to just only .tick() one account !!!

        This is a wrapper around the underlying C++ implementation.

        :param payer_account: class trapeza.account.base_account.BaseAccount (or derived class) object
        :param volume: float, >= 0
                       volume of currency
        :param currency: str
        :param payee_fee: {None, False, func, float}, default=False
                          fee setting for payee account

                          None: self._fee['deposit'] is applied which is set at __init__. Default at __init__ is
                                not applying any fees. See docstring of self.__init__ and docstring of class for
                                further information about globally applied fees and how to set self._fee['deposit'].
                                Call signature will be parsed to:
                                    fee(volume, 1, currency, currency, processing_duration)
                          False: no fees at all applied, even if self._fee['deposit'] is set (overrides globally
                                 set fees: self._fee['deposit'] will be temporarily ignored for this one transaction)
                          func: alternative function to calculate fees is applied with signature (self._fee['deposit']
                                will be ignored for this one transaction and func will be applied instead)
                                fee_volume, fee_currency, fee_exec_time
                                     = fee(volume, price, base, quote, processing_duration)
                                     = fee(volume, 1, currency, currency, processing_duration)
                                price is set/ hard coded to 1 (induced by withdraw()/ deposit())
                                base and quote are set/ hard coded to param:currency (induced by withdraw()/ deposit())
                          float: constant fee is applied and billed in param:currency at the same time as the collect
                                 transaction takes effect (e.g. when payee_processing_duration is not 0)
        :param payer_fee: dependent on payer class implementation of payer_account.withdraw()
                          default=False

                          (!) if not {None, False, 0}:
                            payer_account.withdraw(volume, currency, payer_fee, payer_processing_duration) is called
                            to withdraw transaction volume and fees
        :param payee_processing_duration: int or None, default=None
                                          processing time (delay) in time base units of internal clock until transaction
                                          takes effect on account's depot
                                          time of execution/ billing = self.clock + processing_duration
                                          None is equivalent to 0 in behavior
        :param payer_processing_duration: int or None, default=None
                                          processing time (delay) in time base units of internal clock until transaction
                                          takes effect on account's depot
                                          time of execution/ billing = self.clock + processing_duration
                                          None is equivalent to 0 in behavior

                                         (!) if not {None, 0}:
                                            payer_account.withdraw(volume, currency, payer_fee,
                                                                   payer_processing_duration)
                                            is called (make sure, this method is implemented at payer_account)
                                         else:
                                            payer_account.withdraw(volume, currency) is called
        :return: confirmation states --> 0: processing (processing_duration), 1: executed/ billed
        :raises: TypeError: if volume, currency, processing_duration not of specified type
                 trapeza.exception.CoverageError: if coverage not sufficient (transaction or fee).
                                                  Coverage analysis is set to 'except' (see docstring of self.deposit()
                                                  or self.withdraw()).
                                                  Coverage is only checked at payee account.
                 NotImplementedError: if payee_fee not in {None, False, func, float}
                 trapeza.exception.PositionNAError: if currency (str) or fee_currency (str) from payee_fee is not
                                                    in self.depot.keys()
                 trapeza.exception.AccountError: if payer_account is not derived
                                                 from trapeza.account.base_account.BaseAccount
                 ValueError: if volume < 0
                 if exception raised, then no transactions have been billed (no change in heap or depot,
                 nothing happened)
                 additional exceptions may be risen by payer_account
        """
        # >>>sanity check
        try:
            if not issubclass(payer_account.__class__, BaseAccount):
                raise tpz_exception.AccountError(payer_account)
        except TypeError:
            raise tpz_exception.AccountError(payer_account)
        except tpz_exception.AccountError:
            raise tpz_exception.AccountError(payer_account)

        try:
            if payer_account == self:
                raise tpz_exception.AccountError(payer_account)
        except TypeError:
            raise tpz_exception.AccountError(payer_account)
        except tpz_exception.AccountError:
            raise tpz_exception.AccountError(payer_account)

        # >>>parsing
        if payer_processing_duration is None:
            payer_processing_duration = 0
        if payee_processing_duration is None:
            payee_processing_duration = 0

        # >>>type checking
        check_types([volume, currency, payer_processing_duration, payee_processing_duration],
                    [float, str, int, int],
                    ['volume', 'currency', 'payer_processing_duration', 'payee_processing_duration'],
                    self._c_ignore_type_checking)
        self._check_alt_fee(payee_fee, 'payer_fee')  # only check payee fee structure, payer fee structure unknown

        if volume < 0:
            raise ValueError

        # >>>check coverage deposit, which is only checking if fees are covered as we do not withdraw anything
        # only check payee
        (fee_volume,
         fee_currency,
         fee_exec_duration) = self._eval_fee(action_type='deposit', alt_fee=payee_fee, volume=volume, current_rate=1,
                                             base=currency, quote=currency,
                                             processing_duration=payee_processing_duration)

        if fee_volume > 0:
            self._c_check_coverage(fee_volume, fee_currency.encode(), self._c_clock + fee_exec_duration)

        # >>>withdraw from payer account
        # if payer account is not covered, then this line will (hopefully) throw an error, such that the next line
        # won't proceed and no false transaction at the own account will be incurred
        if payer_processing_duration == 0 and (payer_fee is False or payer_fee is None or payer_fee == 0):
            payer_account.withdraw(volume, currency)
        else:
            try:
                payer_account.withdraw(volume, currency, payer_fee, payer_processing_duration)
            except TypeError:
                raise tpz_exception.AccountError('payer_account has no implementation '
                                                 'payer_account.withdraw(volume, currency, payer_fee, '
                                                 'payer_processing_duration)')

        return self.c_collect(volume, currency.encode(), fee_volume, fee_currency.encode(), fee_exec_duration,
                              payee_processing_duration)

    def transfer(self, payee_account, double volume, str currency, payee_fee=False, payer_fee=False,
                 payee_processing_duration=None, payer_processing_duration=None):
        """
        Transfers payment volume in given currency from this:account to payee account.
        Furthermore, processing duration (e.g. transmission time of messages in real-life systems, broker execution,
        etc.) can be modelled.
        Fees can be defined either as function or float for payer and payee. If payee_fee=None and payer_fee=None, then
        the standard and globally set fees of self._fee['deposit'] and self._fee['withdraw'] (which are set at __init__)
        will be applied. If None (default), no fees will be applied

        If payee_fee or payee_processing_duration shall be applied, then payee class must implement
        payee_account.deposit(volume, currency, payee_fee, payee_processing_duration)

        Coverage analysis is conducted with default arguments of withdraw() and deposit()
        (e.g. coverage='except', instant_float_fee=False)

        !!! If execution is not instant (e.g. processing_duration is not None), both accounts have to call .tick() to
            make transaction take effect on both accounts. It is not sufficient to just only .tick() one account !!!

        This is a wrapper around the underlying C++ implementation.

        :param payee_account: class trapeza.account.base_account.BaseAccount (or derived class) object
        :param volume: float, >= 0
                       volume of currency
        :param currency: str
        :param payee_fee: dependent on payee class implementation of payee_account.deposit()
                          default=False

                          (!) if not {None, False, 0}:
                            payee_account.deposit(volume, currency, payee_fee, payee_processing_duration) is called
                            to deposit transaction volume (and to bill fees if necessary)
        :param payer_fee: {None, False, func, float}, default=False
                          fee setting for payer account

                          None: self._fee['withdraw'] is applied which is set at __init__. Default at __init__ is
                                not applying any fees. See docstring of self.__init__ and docstring of class for
                                further information about globally applied fees and how to set self._fee['withdraw'].
                                Call signature will be parsed to:
                                    fee(volume, 1, currency, currency, processing_duration)
                          False: no fees at all applied, even if self._fee['withdraw'] is set (overrides globally
                                 set fees: self._fee['withdraw'] will be temporarily ignored for this one transaction)
                          func: alternative function to calculate fees is applied with signature (self._fee['withdraw']
                                will be ignored for this one transaction and func will be applied instead)
                                fee_volume, fee_currency, fee_exec_time
                                     = fee(volume, price, base, quote, processing_duration)
                                     = fee(volume, 1, currency, currency, processing_duration)
                                price is set/ hard coded to 1 (induced by withdraw()/ deposit())
                                base and quote are set/ hard coded to param:currency (induced by withdraw()/ deposit())
                          float: constant fee is applied and billed in param:currency at the same time as the transfer
                                 transaction takes effect (e.g. when payer_processing_duration is not 0)
        :param payee_processing_duration: int or None, default=None
                                          processing time (delay) in time base units of internal clock until transaction
                                          takes effect on account's depot
                                          time of execution/ billing = self.clock + processing_duration
                                          None is equivalent to 0 in behavior

                                         (!) if not {None, 0}:
                                            payee_account.deposit(volume, currency, payee_fee,
                                                                  payee_processing_duration)
                                            is called (make sure, this method is implemented at payee_account)
                                         else:
                                            payee_account.deposit(volume, currency) is called
        :param payer_processing_duration: int or None, default=None
                                          processing time (delay) in time base units of internal clock until transaction
                                          takes effect on account's depot
                                          time of execution/ billing = self.clock + processing_duration
                                          None is equivalent to 0 in behavior
        :return: confirmation states --> 0: processing (processing_duration), 1: executed/ billed
        :raises: TypeError: if volume, currency, processing_duration not of specified type
                 trapeza.exception.CoverageError: if coverage not sufficient (transaction or fee).
                                                  Coverage analysis is set to 'except' (see docstring of self.deposit()
                                                  or self.withdraw()).
                                                  Coverage is only checked at payer account.
                 NotImplementedError: if payer_fee not in {None, False, func, float}
                 trapeza.exception.PositionNAError: if currency (str) or fee_currency (str) from payer_fee is not
                                                    in self.depot.keys()
                 trapeza.exception.AccountError: if payee_account is not derived
                                                 from trapeza.account.base_account.BaseAccount
                 ValueError: if volume < 0
                 if exception raised, then no transactions have been billed (no change in heap or depot,
                 nothing happened)
                 additional exceptions may be risen by payee_account
        """
        # >>>sanity check
        try:
            if not issubclass(payee_account.__class__, BaseAccount):
                raise tpz_exception.AccountError(payee_account)
        except TypeError:
            raise tpz_exception.AccountError(payee_account)
        except tpz_exception.AccountError:
            raise tpz_exception.AccountError(payee_account)

        try:
            if payee_account == self:
                raise tpz_exception.AccountError(payee_account)
        except TypeError:
            raise tpz_exception.AccountError(payee_account)
        except tpz_exception.AccountError:
            raise tpz_exception.AccountError(payee_account)

        # >>>parsing
        if payer_processing_duration is None:
            payer_processing_duration = 0
        if payee_processing_duration is None:
            payee_processing_duration = 0

        # >>>type checking
        check_types([volume, currency, payer_processing_duration, payee_processing_duration],
                    [float, str, int, int],
                    ['volume', 'currency', 'payer_processing_duration', 'payee_processing_duration'],
                    self._c_ignore_type_checking)
        self._check_alt_fee(payer_fee, 'payer_fee')  # only check payer fee structure, payee fee structure unknown

        if volume < 0:
            raise ValueError

        # >>>coverage check withdrawal and fees
        # only check payer
        (fee_volume,
         fee_currency,
         fee_exec_duration) = self._eval_fee(action_type='withdraw', alt_fee=payer_fee, volume=volume, current_rate=1,
                                             base=currency, quote=currency,
                                             processing_duration=payer_processing_duration)
        self._c_check_coverage(c_precision_add(volume, fee_volume * (fee_currency == currency)), currency.encode(),
                               self._c_clock + max(fee_exec_duration, payer_processing_duration))
        if fee_volume > 0:
            self._c_check_coverage(fee_volume, fee_currency.encode(), self._c_clock + fee_exec_duration)

        # >>>deposit at payee account
        # if payee cannot cover deposit fee, then this line will (hopefully) throw an error, such that the next line
        # won't proceed and no false transaction at the own account will be incurred
        if payee_processing_duration == 0 and (payee_fee is False or payee_fee is None or payee_fee == 0):
            payee_account.deposit(volume, currency)
        else:
            try:
                payee_account.deposit(volume, currency, payee_fee, payee_processing_duration)
            except TypeError:
                tpz_exception.AccountError('payee_account has no implementation '
                                           'payee_account.deposit(volume, currency, payee_fee, '
                                           'payee_processing_duration)')

        return self.c_transfer(volume, currency.encode(), fee_volume, fee_currency.encode(), fee_exec_duration,
                               payer_processing_duration)

    def buy(self, double volume_base, double ask_price, str base, str quote, fee=None, processing_duration=None,
            str coverage='except', instant_withdrawal=False, instant_float_fee=False, float_fee_currency=None):
        """
        Buy base|quote pair at ask_price. Give quote and receive base: quote->base, see docstring of class for further
        information about notation convention.

        Volume is given in BASE currency.

        Furthermore, processing duration (e.g. transmission time of messages in real-life systems, broker execution,
        etc.) can be modelled.
        Fees can be defined either as function or float. If fee is float, then a separate currency in which to bill fees
        can be defined. Additionally, if fees are float, fees can be withdrawn immediately even though transaction
        might take some processing duration. This is controlled via instant_float_fee (bool).
        If fee=float and float_fee_currency=None, then fees are applied in BASE currency.
        Additionally, the withdrawal part of the buy transaction can be conducted instantly independent of the
        processing_duration, which can be controlled via instant_withdrawal.

        Buy transaction is split into a withdrawal of volume in quote currency and a deposit of volume in base currency.

        This is a wrapper around the underlying C++ implementation.

        :param volume_base: float, >= 0
                            volume of BASE currency
        :param base: str,
                     base currency
        :param ask_price: float
                          current base|quote bid (FX notation, see docstring of class regarding notation conventions)
        :param quote: str,
                      quote currency
        :param fee: {func, False, None, float}, default=None
                        fee setting for buy transaction

                        None: self._fee['buy'] is applied which is set at __init__. Default at __init__ is
                              not applying any fees. See docstring of self.__init__ and docstring of class for
                              further information about globally applied fees and how to set self._fee['buy']
                        False: no fees at all applied, even if self._fee['buy'] is set (overrides globally set fees:
                               self._fee['buy'] will be temporarily ignored for this one transaction)
                        func: alternative function to self._fee is applied (self._fee['buy'] will be ignored
                              for this one transaction and func will be applied instead)
                              Must follow call signature:
                                  fee_volume, fee_currency, fee_exec_time
                                       = fee(volume, price, base, quote, processing_duration)
                        float: constant fee is applied and billed in param:float_fee_currency
                               if instant_float_fee = False: fee is billed at the same time as set by
                                                             param:processing_duration (same time step when
                                                             transaction takes effect on account's depot)
                               if instant_float_fee = True: fee is billed instantly independent from
                                                            param:processing_duration of transaction
        :param processing_duration: int or None, default=None
                                    processing time (delay) in time base units of internal clock until transaction takes
                                    effect on account's depot
                                    time of execution/ billing = self.clock + processing_duration
                                    None is equivalent to 0 in behavior
        :param coverage: {'partial', 'except', 'ignore', 'debit'}, default='except'
                                   Controls exception behavior in case of coverage violation.
                                   This coverage analysis checks whether transaction is conductible in principal (e.g.
                                   if currently account's depot position is sufficient right now) but does not check
                                   against marked but not yet billed transactions.

                                   'partial': partial fulfilment as far as possible (including fees).
                                              Withdrawal volume of buying transaction will be reduced s.t. that coverage
                                              conditions are met.
                                              This means, if withdrawal volume + fees is greater than current depot
                                              position, then withdrawal volume will be reduced, such that no debiting
                                              in account's depot positions occurs. If volume and fees are not in the
                                              same currency, this reduction is only performed on the volume (fees might
                                              still cause a coverage violation), amount of fees stays untouched then.
                                              volume is reduced to meet initially calculated fees, fees are not
                                              adapted to reduced volume (guessing interdependency would be hard), s.t.
                                              more fees might be payed than according to reduced volume.
                                              This does not guarantee transaction fulfillment, as this just checks
                                              current depot but does not check against marked but not yet billed
                                              (delayed) transactions, which is done independently of this
                                              coverage check.
                                              If withdrawal volume has to be reduced, then depositing volume is adapted
                                              accordingly.
                                   'except': raises trapeza.exception.CoverageError if coverage is violated, which is
                                             the case if withdrawal (including fees) is
                                             greater than current depot position (in same currency as volume)
                                   'debit': temporarily deactivates coverage check of current depot position as well as
                                            coverage check of marked but not yet booked transactions. If
                                            prohibit_debiting is set to False at __init__(), then negative (debt)
                                            positions are possible, else a trapeza.exception.CoverageError will be
                                            thrown at time of execution.
                                   'ignore': buy order is not fulfilled but ignored instead if coverage violation occurs

                                    Coverage checking of current depot position is done independently of
                                    self.check_marked_coverage, which additionally checks against marked but not yet
                                    filled future transactions (e.g. if self.check_marked_coverage is set to
                                    'min_backward' or 'max_forward).
                                    'debit' deactivates coverage check regarding future marked, not yet filled
                                    transactions as well as coverage check of current depot positions for this one
                                    transaction (see above).
        :param instant_withdrawal: bool, default=False
                                   if True, volume in quote currency is withdrawn instantly,
                                        but depositing volume in base currency is done after processing_duration.
                                        This argument does not affect at which time step fees will be billed (which
                                        is only affected via processing_time (when fee is a func or self._fee['buy']
                                        is applied), fee and instant_float_fee).
                                   if False, processing_time is applied to both withdrawal and depositing
        :param instant_float_fee: bool, default=False
                                  ONLY APPLIES if fee = float, else ignored
                                  if True, fees are withdrawn instantly independent of processing_duration. This does
                                    not affect processing duration of withdrawing param:volume.
                                  if False, fees are billed at the same time as withdrawing param:volume given by the
                                    processing duration.
        :param float_fee_currency: {str, None}, default=None
                                   currency type to bill fee if fee=float, else ignored
                                   if None or ignored, float_fee_currency is set to param:base,
                                   else float_fee_currency is set to param:base if fee is False, None or func
        :return: int
                 confirmation states --> -1: ignored, 0: processing (processing_duration), 1: executed/ billed
        :raises: trapeza.exception.PositionNAError: if quote (str) or float_fee_currency (str) is
                                                    not in self.depot.keys()
                 TypeError: if base, quote, volume, float_fee_currency or ask_price not of specified type
                 NotImplementedError: if coverage not in {'partial', 'except', 'ignore', 'debit'} or
                                      fee not in {func, False, None, float}
                 trapeza.exception.CoverageError: if coverage not sufficient (transaction or fee) depending on
                                                  coverage and if checking of marked transaction
                                                  (self.check_marked_coverage) is switched on
                 ValueError: if volume < 0
        :TODO: when coverage='partial', than recalculate fees according to reducing volume to meet coverage
        :TODO:  volume-depot + f(volume-x) -x = 0 --> min
        """
        # >>>parsing inputs
        (parsed_fee_currency,
         instant_float_fee,
         processing_duration) = self._parse_fee_and_transaction_params(float_fee_currency, base, fee,
                                                                       'buy_fee', instant_float_fee,
                                                                       processing_duration)

        # >>>sanity and type checking
        if volume_base < 0:
            raise ValueError('Buy volume in {} is < 0.'.format(quote))

        check_types([base, quote, volume_base, ask_price, parsed_fee_currency, processing_duration,
                     instant_withdrawal, instant_float_fee, coverage],
                    [str, str, float, float, str, int, bool, bool, str],
                    ['base', 'quote', 'volume', 'ask_price', 'float_fee_currency', 'processing_duration',
                     'instant_withdrawal', 'instant_float_fee', 'coverage'], self._c_ignore_type_checking)
        self._c_isin_depot(quote.encode())

        # >>>evaluate fees
        # volume is in quote currency
        (fee_volume,
         fee_currency,
         fee_exec_duration) = self._eval_fee(action_type='buy', alt_fee=fee, volume=volume_base,
                                             current_rate=ask_price, base=parsed_fee_currency, quote=quote,
                                             processing_duration=processing_duration * (1 - instant_float_fee))

        # >>>handle coverage exception induced by fees
        if coverage not in ['except', 'partial', 'debit', 'ignore']:
            raise NotImplementedError('coverage must be {"except", "partial", "debit"}.')

        return self.c_buy(volume_base, ask_price, base.encode(), quote.encode(), fee_volume, fee_currency.encode(),
                          fee_exec_duration, processing_duration, coverage.encode(),
                          instant_withdrawal, instant_float_fee)

    def sell(self, double volume_base, double bid_price, str base, str quote, fee=None, processing_duration=None,
             str coverage='except', instant_withdrawal=False, instant_float_fee=False, float_fee_currency=None):
        """
        Sell base|quote pair at bid_price. Give base and receive quote: base->quote, see docstring of class for further
        information about notation convention.

        Volume is given in BASE currency.

        Furthermore, processing duration (e.g. transmission time of messages in real-life systems, broker execution,
        etc.) can be modelled.
        Fees can be defined either as function or float. If fee is float, then a separate currency in which to bill fees
        can be defined. Additionally, if fees are float, fees can be withdrawn immediately even though transaction
        might take some processing duration. This is controlled via instant_float_fee (bool).
        If fee=float and float_fee_currency=None, then fees are applied in BASE currency.
        Additionally, the withdrawal part of the sell transaction can be conducted instantly independent of the
        processing_duration, which can be controlled via instant_withdrawal.

        Sell transaction is split into a withdrawal of volume in base currency and a deposit of volume in
        quote currency.

        This is a wrapper around the underlying C++ implementation.

        :param volume_base: float, >= 0
                            volume of BASE currency
        :param base: str,
                     base currency
        :param bid_price: float
                          current base|quote ask (FX notation, see docstring of class regarding notation conventions)
        :param quote: str,
                      quote currency
        :param fee: {func, False, None, float}, default=None
                        fee setting for sell transaction

                        None: self._fee['sell'] is applied which is set at __init__. Default at __init__ is
                              not applying any fees. See docstring of self.__init__ and docstring of class for
                              further information about globally applied fees and how to set self._fee['sell']
                        False: no fees at all applied, even if self._fee['sell'] is set (overrides globally set fees:
                               self._fee['sell'] will be temporarily ignored for this one transaction)
                        func: alternative function to self._fee is applied (self._fee['sell'] will be ignored
                              for this one transaction and func will be applied instead)
                              Must follow call signature:
                                  fee_volume, fee_currency, fee_exec_time
                                       = fee(volume, price, base, quote, processing_duration)
                        float: constant fee is applied and billed in param:float_fee_currency
                               if instant_float_fee = False: fee is billed at the same time as set by
                                                             param:processing_duration (same time step when
                                                             transaction takes effect on account's depot)
                               if instant_float_fee = True: fee is billed instantly independent from
                                                            param:processing_duration of transaction
        :param processing_duration: int or None, default=None
                                    processing time (delay) in time base units of internal clock until transaction takes
                                    effect on account's depot
                                    time of execution/ billing = self.clock + processing_duration
                                    None is equivalent to 0 in behavior
        :param coverage: {'partial', 'except', 'ignore', 'debit'}, default='except'
                                   Controls exception behavior in case of coverage violation.
                                   This coverage analysis checks whether transaction is conductible in principal (e.g.
                                   if currently account's depot position is sufficient right now) but does not check
                                   against marked but not yet billed transactions.

                                   'partial': partial fulfilment as far as possible (including fees).
                                              Withdrawal volume of sell transaction will be reduced s.t. that coverage
                                              conditions are met.
                                              This means, if withdrawal volume + fees is greater than current depot
                                              position, then withdrawal volume will be reduced, such that no debiting
                                              in account's depot positions occurs. If volume and fees are not in the
                                              same currency, this reduction is only performed on the volume (fees might
                                              still cause a coverage violation), amount of fees stays untouched then.
                                              volume is reduced to meet initially calculated fees, fees are not
                                              adapted to reduced volume (guessing interdependency would be hard), s.t.
                                              more fees might be payed than according to reduced volume.
                                              This does not guarantee transaction fulfillment, as this just checks
                                              current depot but does not check against marked but not yet billed
                                              (delayed) transactions, which is done independently of this
                                              coverage check.
                                              If withdrawal volume has to be reduced, then depositing volume is adapted
                                              accordingly.
                                   'except': raises trapeza.exception.CoverageError if coverage is violated, which is
                                             the case if withdrawal (including fees) is
                                             greater than current depot position (in same currency as volume)
                                   'debit': temporarily deactivates coverage check of current depot position as well as
                                            coverage check of marked but not yet booked transactions. If
                                            prohibit_debiting is set to False at __init__(), then negative (debt)
                                            positions are possible, else a trapeza.exception.CoverageError will be
                                            thrown at time of execution.
                                   'ignore': sell order is not fulfilled but ignored instead if coverage
                                             violation occurs

                                    Coverage checking of current depot position is done independently of
                                    self.check_marked_coverage, which additionally checks against marked but not yet
                                    filled future transactions (e.g. if self.check_marked_coverage is set to
                                    'min_backward' or 'max_forward).
                                    'debit' deactivates coverage check regarding future marked, not yet filled
                                    transactions as well as coverage check of current depot positions for this one
                                    transaction (see above).
        :param instant_withdrawal: bool, default=False
                                   if True, volume in base currency is withdrawn instantly,
                                        but depositing volume in quote currency is done after processing_duration.
                                        This argument does not affect at which time step fees will be billed (which
                                        is only affected via processing_time (when fee is a func or
                                        self._fee['sell'] is applied), fee and instant_float_fee).
                                   if False, processing_time is applied to both withdrawal and depositing
        :param instant_float_fee: bool, default=False
                                  ONLY APPLIES if fee = float, else ignored
                                  if True, fees are withdrawn instantly independent of processing_duration. This does
                                    not affect processing duration of withdrawing param:volume.
                                  if False, fees are billed at the same time as withdrawing param:volume given by the
                                    processing duration.
        :param float_fee_currency: {str, None}, default=None
                                   currency type to bill fee if fee=float, else ignored
                                   if None or ignored, float_fee_currency is set to param:base,
                                   else float_fee_currency is set to param:base if fee is False, None or func
        :return: int
                 confirmation states --> -1: ignored, 0: processing (processing_duration), 1: executed/ billed
        :raises: trapeza.exception.PositionNAError: if base (str) or float_fee_currency (str) is
                                                    not in self.depot.keys()
                 TypeError: if base, quote, volume, float_fee_currency or bid_price not of specified type
                 NotImplementedError: if coverage not in {'partial', 'except', 'ignore', 'debit'} or
                                      fee not in {func, False, None, float}
                 trapeza.exception.CoverageError: if coverage not sufficient (transaction or fee) depending on
                                                  coverage and if checking of marked transaction
                                                  (self.check_marked_coverage) is switched on
                 ValueError: if volume < 0
        :TODO: when coverage='partial', than recalculate fees according to reducing volume to meet coverage
        :TODO:  volume-depot + f(volume-x) -x = 0 --> min
        """
        # catch cases: x) currency not in depot, x) not sufficient coverage, x) fee structure, x) return confirmation

        # >>>parsing inputs
        (parsed_fee_currency,
         instant_float_fee,
         processing_duration) = self._parse_fee_and_transaction_params(float_fee_currency, base, fee,
                                                                       'sell_fee', instant_float_fee,
                                                                       processing_duration)

        # >>>sanity and type checking
        if volume_base < 0:
            raise ValueError('Sell volume in {} is < 0.'.format(base))

        check_types([base, quote, volume_base, bid_price, parsed_fee_currency, processing_duration,
                     instant_withdrawal, instant_float_fee, coverage],
                    [str, str, float, float, str, int, bool, bool, str],
                    ['base', 'quote', 'volume', 'bid_price', 'float_fee_currency', 'processing_duration',
                     'instant_withdrawal', 'instant_float_fee', 'coverage'], self._c_ignore_type_checking)
        self._c_isin_depot(base.encode())

        # >>>evaluate fees
        (fee_volume,
         fee_currency,
         fee_exec_duration) = self._eval_fee(action_type='sell', alt_fee=fee, volume=volume_base, current_rate=bid_price,
                                             base=parsed_fee_currency, quote=quote,
                                             processing_duration=processing_duration * (1 - instant_float_fee))

        # >>>handle coverage exception induced by fees
        if coverage not in ['except', 'partial', 'debit', 'ignore']:
            raise NotImplementedError('coverage must be {"except", "partial", "debit"}.')

        return self.c_sell(volume_base, bid_price, base.encode(), quote.encode(), fee_volume, fee_currency.encode(),
                           fee_exec_duration, processing_duration, coverage.encode(),
                           instant_withdrawal, instant_float_fee)

    def tick(self, clock=None):
        """
        If clock=None, then counts internal clock up by one time base unit.
        Else internal clock is set to param:clock as new internal time step.
        Executes exec_heap (see stack automaton logic implemented as heap data structure described in docstring of
        class) after new clock time is set, e.g. executing all due transactions, which were delayed due to processing
        times. All transactions on heap, whose execution times (defined as time step of instructing transaction +
        processing duration) are less than the new clock time, will be executed from oldest to newest up to the new
        clock time. Transactions allocated in the future w.r.t. the new clock time will of course not be executed but
        remain on the heap until they are due (w.r.t internal clock).

        This is a wrapper around the underlying C++ implementation.

        :param clock: {int >= 0, None}, default=None
                      if clock=None, then count up by one. If clock is integer, set internal clock to param:clock.
        :return: int, current (freshly set) clock time
        :raises: TypeError: if clock is not int or clock < 0
        """
        if clock is None:
            clock = self._c_clock + 1
        elif not self._c_ignore_type_checking:
            try:
                if 0 <= clock == int(clock):
                    pass
                else:
                    raise TypeError('clock has to be int >= 0.')
            except Exception as e:
                raise e

        return self.c_tick(clock)

    def update_exchange_rate(self, double rate, str base, str quote):
        """
        It is highly recommended not to use this class method, but use self.batch_update_exchange_rates instead!


        Update and/ or add exchange rate (within self.exchange_rates dictionary) for base|quote pair in
        self.exchange_rates dictionary.
        Use FX direct notation, see docstring of class for further information on notation convention.

        It's sufficient enough, to just provide base|quote ratio. quote|base ratio does not have to be added separately
        and will be calculated automatically.

        This method updates the class attribute self.exchange_rates (just one entry at a time).

        This is a wrapper around the underlying C++ implementation.

        :param rate: float,
                     use FX direct notation of base|quote pair, see docstring of class for further information
        :param base: str
        :param quote: str
        :return: None
        :raises: TypeError if parameters do not match specified types
        """
        # >>>type check
        check_types([rate, base, quote], [float, str, str], ['rate', 'base', 'quote'], self._c_ignore_type_checking)

        self.c_update_exchange_rate(rate, base.encode(), quote.encode())

    def batch_update_exchange_rates(self, list_rates, list_base_quote_pairs):
        """
        Performs batch update of exchange rates of multiple currency pairs (or assets), whereas
        self.update_exchange_rate() only updates one exchange rate pair at once.
        It's sufficient enough, to just provide base|quote ratio. quote|base ratio does not have to be added separately
        and will be calculated automatically.

        If one wants to call self.total_balance() without arguments, then this method has to be called beforehand.

        It is highly recommended, that all pairs, which are also present within depot (as single positions not as pairs
        directly), are present in the update arguments of this method. Otherwise self.total_balance() might throw an
        exception in certain circumstances! The safest way is to not use this method at all but call
        self.total_balance() with appropriate input data argument!

        This method updates the class attribute self.exchange_rates.

        This is a wrapper around the underlying C++ implementation.

        :param list_rates: list of floats,
                           exchange rate of base|quote pair
                           Rate is given in FX direct notation of base|quote, see docstring of class for further
                           information on notation convention (simply speaking: just plug in official exchange rates
                           from base|quote pair which one can find on any website providing financial data)
        :param list_base_quote_pairs: list of tuples(base, quote),
                                     base|quote pair in FX direct notation, see docstring of class
                                     base: str
                                     quote: str
        :return: None
        :raises: TypeError if parameters do not match specified types
                 IndexError: if lists don't have same length
        """
        if not (len(list_rates) == len(list_base_quote_pairs)):
            raise IndexError('Lists must have same length.')

        for i in range(len(list_rates)):
            # noinspection PyUnresolvedReferences
            check_types([list_rates[i], list_base_quote_pairs[i]], [float, tuple],
                        ['list_rates must contain floats or ints', 'list_base_quote_pairs must contain tuples'],
                        self._c_ignore_type_checking)
        return self.c_batch_update_exchange_rates(list_rates, list_base_quote_pairs)

    def total_balance(self, exchange_rates=None, reference_currency=None):
        """
        Calculates current value of all assets within self.depot in reference currency.

        If exchange_rate=None, then self.batch_update_exchange_rates() has to be called beforehand.

        This is a wrapper around the underlying C++ implementation.

        :param exchange_rates: {dict, None}, default=None
                               if None, self.exchange_rates will be used (if set at initialization)

                               !!! call self.batch_update_exchange_rate before calling this
                                   function if param:exchange_rate=None !!!

                               exchange_rates are given in base|quote FX direct notation, see docstring of class for
                               further information on notation convention (simply speaking: just plug in official
                               exchange rates from base|quote pair which one can find on any website providing
                               financial data)

                               key: tuple of (str, str)
                                    (base, quote) --> (from_currency, to_currency)
                                    All currencies contained in self.depot can be interpreted as base.
                                    reference currency (or self.reference_currency if reference_currency=None) can be
                                    interpreted as quote.

                                    base: str
                                    quote: str

                                    Furthermore, it does not matter if data is provided as (base, quote) or
                                    (quote, base), inverting is done automatically internally.
                                    Supplying exchange rate data as one of the two tuple variants is sufficient (user
                                    does not have to supply base|quote and quote|base, but just one of them).
                               value: float,
                                      exchange_rate of base|quote pair

                               It's sufficient enough, to just provide base|quote ratio.
                               quote|base ratio does not have to be added separately and is calculated automatically.
        :param reference_currency: {str, None}, default=None
                                   if None, reference_currency is set to self.reference_currency
        :return: float
        :raises: KeyError: if exchange_rates does not include all currencies listed in account depot
                 TypeError: if parameters do not match specified types
                 ValueError: if exchange rates of base|quote and 1/quote|base do not match up
                 trapeza.exception.OperatingError: if this method is called with exchange_rate=None and exchange rates
                                                   have not been updated otherwise beforehand
                                                   (e.g. self.batch_update_exchange_rates)
                                                   or
                                                   if somehow else both exchange_rate=None and self.exchange_rates=None
        TODO: assume exchange_rate=0 if currency not in data (?) -> safer not to implement this convention
        """
        # >>>check if exchange rates have been updated if internal exchange rates are taken for calculations
        if not self._c_is_exchange_rate_updated and exchange_rates is None:
            raise tpz_exception.OperatingError('Exchange rates have not been updated before calling. Please call '
                                               'self.batch_update_exchange_rates beforehand.')

        # >>>parsing
        if reference_currency is None:
            reference_currency = self._c_reference_currency.decode()    # self.reference_currency

        if exchange_rates is None:
            exchange_rates = self._c_exchange_rates
        else:
            # >>>type check
            if len(exchange_rates) == 0:
                raise tpz_exception.OperatingError('Exchange rates contain empty dict.')

            exchange_rates = self._parse_exchange_rates(exchange_rates, self._c_ignore_type_checking)

        check_types([reference_currency, exchange_rates], [str, dict],
                    ['reference_currency', 'exchange_rates dict'], self._c_ignore_type_checking)

        return self.c_total_balance(exchange_rates, reference_currency.encode())

    def position(self, str currency):
        """
        Returns position size of given currency.
        (Does not need any update of exchange rate previous to calling this method)

        This is a wrapper around the underlying C++ implementation.

        :param currency: str
        :return: position: float, volume of currency
        :raises: TypeError: if parameters do not match specified types
        """
        check_types([currency], [str], ['currency'], self._c_ignore_type_checking)

        return self.c_position(currency.encode())

