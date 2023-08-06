import inspect
import itertools

import cython

from trapeza.account.base_account import BaseAccount
from trapeza.strategy.base_strategy import BaseStrategy
from trapeza.utils import check_types, ProtectedDict, ProtectedList
from trapeza import exception as tpz_exception

from trapeza.arithmetics.arithmetics cimport c_precision_add

# noinspection PyProtectedMember,PyUnresolvedReferences
cpdef short _c_tick_method(self, dict data) except -1:
    """
    Default tick method. Ticks all contained FXAccounts (or derived BaseAccounts)
    :param self: class object, placeholder
    :param data: dict (see param:price_data at FXStrategy.run())
                 keys: currency pair as tuple of strings: (currency_0, currency_1)
                 values: list of floats as exchange rates per time step t or array of floats

                 {(base, quote): [rate_0, rate_1, ..., rate_t],
                  (base, quote): [rate_0, rate_1, ..., rate_t],
                  ...}

                 All values (list or array of floats) of all keys (currency pairs) have to be of same length.
    :return: 1
    """
    cdef long i = 0
    data_single_point = {k: data[k][-1] for k in data.keys()}
    for i in range(len(self.c_accounts)):
        if hasattr(self.c_accounts[i], '_is_order_manager_monkey_patch'):
            self.c_accounts[i].tick(data_single_point)
        else:
            try:
                self.c_accounts[i].c_tick(self.c_accounts[i]._c_clock + 1)
            except AttributeError:
                self.c_accounts[i].tick()
    return 1


# noinspection PyUnresolvedReferences,PyPep8Naming,PyAttributeOutsideInit,PyProtectedMember,PyTypeChecker
cdef class cFXStrategy:
    """
    This as a C++ implementation via cython and gets wrapped by FXStrategy class. This class tries to stay in C++ space
    as long as possible to avoid unnecessary type casting to Python data types. Internal class storage is implemented
    via C++ vectors and C++ unordered_map (comparable to Python's dict) and is only casted to Python data types when
    calling class attributes of FXStrategy.
    Please refer to the docstring of FXStrategy for detailed descriptions. Details might differ slightly, but the
    overall logic idea is the same and this class gets wrapped by FXStrategy anyhow. This class should never be called
    directly by the user.
    """
    def __init__(self, string name, list accounts, object strategy_func, long lookback, object tick_func,
                 suppress_ticking, ignore_type_checking, dict strategy_kwargs, dict tick_kwargs, suppress_evaluation):
        """
        Calls self.c_init. See self.c_init for further docstring information.
        :param name: std:string
        :param accounts: list of FXAccount (or any other class derived from BaseAccount) class objects
        :param strategy_func: Python function
        :param lookback: long
        :param tick_func: Python function, see FXStrategy docstring regarding call signature
        :param suppress_ticking: py_bool
        :param ignore_type_checking: py_bool
        :param strategy_kwargs: dict for additional kwargs for param:strategy_func
        :param tick_kwargs: dict for additional kwargs for param:tick_func
        :param: suppress_evaluation: py_bool
        """
        self.c_init(name, accounts, strategy_func, lookback, tick_func, suppress_ticking, ignore_type_checking,
                    strategy_kwargs, tick_kwargs, suppress_evaluation)

    # noinspection PyAttributeOutsideInit
    @cython.wraparound(False)
    cpdef short c_init(self, string name, list accounts, object strategy_func, long lookback, object tick_func,
                       bool_t suppress_ticking, bool_t ignore_type_checking, dict strategy_kwargs,
                       dict tick_kwargs, bool_t suppress_evaluation) except -1:
        """
        This method gets wrapped by __init__, which is useful when __init__ gets overwritten during subclassing.
        :param name: std:string
        :param accounts: list of FXAccount (or any other class derived from BaseAccount) class objects
        :param strategy_func: Python function containing the trading strategy
        :param lookback: long
        :param tick_func: Python function containing alternative tick method for FXAccount (or any other class derived 
                                 from BaseAccount), see FXStrategy docstring regarding call signature
        :param suppress_ticking: std:bool, see docstring of FXStrategy
        :param ignore_type_checking: std:bool, whether to ignore type checks (more performance, less safe)
        :param strategy_kwargs: dict for additional kwargs for param:strategy_func
        :param tick_kwargs: dict for additional kwargs for param:tick_func
        :param suppress_evaluation: std:bool, see docstring of FXStrategy
        :return: 1
        """
        self.c_name = name
        self._c_ignore_type_checking = ignore_type_checking
        self.c_accounts = accounts
        cdef str k
        cdef double v
        self._c_init_accs_depots = [{k: v for k, v in acc.depot.items()} for acc in self.c_accounts]    # python only
        self._c_accs_clocks = [acc.clock for acc in self.accounts]  # python only content
        self.c_strategy_func = strategy_func
        self.c_tick_method = tick_func
        self.c_lookback = lookback
        self.c_suppress_ticking = suppress_ticking
        self.c_suppress_evaluation = suppress_evaluation
        self.c_strategy_kwargs = strategy_kwargs    # python only content
        self.c_tick_kwargs = tick_kwargs            # python only content
        # c_signals, c_positions, c_merged_positions, c_total_balances, c_merged_total_balances and
        # _c_signals_at_step_t should be initialized empty by default in cython
        return 1

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef short _c_init_all_positions(self, list all_keys) except -1:
        """
        Set internal storage of self.c_positions and self.c_merged_positions to empty vectors.
        :param all_keys: list (or generator) of of all tuple keys contained in exchange_rates'/ price_data's dictionary
                         tuple keys: (py_str:base, py_str:quote)
        :return: 1
        """
        cdef str key
        cdef vector[double] vec
        cdef vector[vector[double]] vec_vec
        for key in set(itertools.chain(*all_keys)):
            self.c_positions[key.encode()] = vec_vec
            self.c_merged_positions[key.encode()] = vec
        return 1

    cpdef short _c_reset_storage(self) except -1:
        """
        Clears all internal storages (vectors and unordered_maps), which keep track of strategy results.
        :return: 1
        """
        self.c_signals.clear()
        self.c_positions.clear()
        self.c_merged_positions.clear()
        self.c_total_balances.clear()
        self.c_merged_total_balances.clear()
        self._c_signals_at_step_t.clear()
        return 1

    # noinspection PyProtectedMember
    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef short c_reset(self) except -1:
        """
        Resets internal storage and depots as well as clocks of all contained FXAccounts (or derived BaseAccounts).
        :return: 1 
        """
        self._c_reset_storage()
        cdef long i = 0
        for i in range(len(self.c_accounts)):
            self.c_accounts[i]._reset()

            # avoid copying just object ref
            self.c_accounts[i].depot = {k: float(v) for k, v in self._init_accs_depots[i].items()}

            self.c_accounts[i].clock = <long>self._c_accs_clocks[i]
        return 1

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef dict parse_positions(self, unordered_map[string, vector[vector[double]]] positions):
        """
        Parses input (positions) to Python dict.
        :param positions: unordered_map[string, vector[vector[double]]]
        :return: dict, see docstring of FXStrategy class regarding self.positions for further details
                 keys: py_str: currency/ asset
                 value: list of floats representing position sizes at every time step which FXStrategy has run through
        """
        cdef dict ret_positions = {}
        cdef list ret_outer_pos, ret_inner_pos
        for elem in positions:
            ret_outer_pos = []
            for outer_pos in elem.second:
                ret_inner_pos = []
                for inner_pos in outer_pos:
                    ret_inner_pos.append(inner_pos)
                ret_outer_pos.append(ret_inner_pos)
            ret_positions[elem.first.decode()] = ret_outer_pos
        return ret_positions

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef list parse_signals(self, vector[vector[vector[string]]] signals):
        """
        Parses input (signals) to Python list.
        :param signals: vector[vector[vector[string]]]
        :return: list, see docstring of FXStrategy class regarding self.signals for further details
        """
        cdef list ret_signals = []
        cdef list ret_middle_signals, ret_inner_signals
        for outer_signal in signals:
            ret_middle_signals = []
            for middle_signal in outer_signal:
                ret_inner_signals = []
                for inner_signal in middle_signal:
                    ret_inner_signals.append(inner_signal.decode())
                ret_middle_signals.append(ret_inner_signals)
            ret_signals.append(ret_middle_signals)
        return ret_signals

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef dict parse_merged_positions(self, unordered_map[string, vector[double]] merged_positions):
        """
        Parses input (merged_positions) to Python dict.
        :param merged_positions: unordered_map[string, vector[double]]
        :return: dict, see docstring of FXStrategy class regarding self.merged_positions for further details
        """
        cdef dict ret_merged_positions = {}
        cdef list ret_inner_mp
        for elem_mp in merged_positions:
            ret_inner_mp = []
            for db in elem_mp.second:
                ret_inner_mp.append(db)
            ret_merged_positions[elem_mp.first.decode()] = ret_inner_mp
        return ret_merged_positions

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef list parse_total_balances(self, vector[vector[double]] total_balances):
        """
        Parses input (total_balances) to Python list.
        :param total_balances: vector[vector[double]]
        :return: list, see docstring of FXStrategy class regarding self.total_balances for further details
        """
        cdef list ret_total_balances = []
        cdef list ret_inner_tb
        cdef list exp
        exp = total_balances
        for outer_tb in total_balances:
            ret_inner_tb = []
            for inner_tb in outer_tb:
                ret_inner_tb.append(inner_tb)
            ret_total_balances.append(ret_inner_tb)
        return ret_total_balances

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cdef list parse_merged_total_balances(self, vector[double] merged_total_balances):
        """
        Parses input (merged_total_balances) to Python list.
        :param merged_total_balances: vector[double]
        :return: list, see docstring of FXStrategy class regarding self.merged_total_balances for further details
        """
        cdef list ret_merged_total_balances = []
        for outer_mtb in merged_total_balances:
            ret_merged_total_balances.append(outer_mtb)
        return ret_merged_total_balances

    cpdef dict self_parse_positions(self):
        """
        Parses self.c_positions and returns a Python dict.
        :return: dict, see docstring of FXStrategy class for further details
        """
        return self.parse_positions(self.c_positions)

    cpdef list self_parse_signals(self):
        """
        Parses self.c_signals and returns Python list.
        :return: list, see docstring of FXStrategy class for further details
        """
        return self.parse_signals(self.c_signals)

    cpdef dict self_parse_merged_positions(self):
        """
        Parses self.c_merged_positions and returns Python dict.
        :return: dict, see docstring of FXStrategy class for further details
        """
        return self.parse_merged_positions(self.c_merged_positions)

    cpdef list self_parse_total_balances(self):
        """
        Parses self.c_total_balances and returns Python list.
        :return: list, see docstring of FXStrategy class for further details
        """
        return self.parse_total_balances(self.c_total_balances)

    cpdef list self_parse_merged_total_balances(self):
        """
        Parses self.c_merged_total_balances and returns Python list.
        :return: list, see docstring of FXStrategy class for further details
        """
        return self.parse_merged_total_balances(self.c_merged_total_balances)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef dict self_parse_signals_at_step_t(self):
        """
        Parses self._c_signals_at_step_t and returns Python dict.
        self._c_signals_at_step_t is just an intermediate and auxiliary storage.
        :return: dict,
                 key: index position within self.c_accounts
                 value: list of Python strings representing signals emitted at current time step
        """
        # unordered_map[long,vector[string]] _c_signals_at_step_t
        cdef dict ret_signals_at_step_t = {}
        cdef list inner_signals_at_step_t

        for elem in self._c_signals_at_step_t:
            inner_signals_at_step_t = elem.second
            inner_signals_at_step_t = [v.decode() for v in inner_signals_at_step_t]
            ret_signals_at_step_t[elem.first] = inner_signals_at_step_t
        return ret_signals_at_step_t

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef short positions_from_py(self, dict positions) except -1:
        """
        Parses Python dict of positions and sets self.c_positions.
        :param positions: dict, see docstring of FXStrategy class regarding self.positions for further details
        :return: 1
        """
        # unordered_map[string, vector[vector[double]]] c_positions
        self.c_positions.clear()

        cdef str k
        cdef list v, t
        cdef vector[double] inner_pos
        cdef vector[vector[double]] outer_pos
        inner_pos.reserve(len(self.c_accounts))
        outer_pos.reserve(len(positions[list(positions.keys())][0]))
        for k, v in positions.items():
            outer_pos.clear()
            for t in v:
                inner_pos.clear()
                inner_pos = t
                outer_pos.push_back(inner_pos)
            self.c_positions[k.encode()] = outer_pos
        return 1

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef short signals_from_py(self, list signals) except -1:
        """
        Parses Python list of signals and sets self.c_signals.
        :param signals: list, see docstring of FXStrategy class regarding self.signals for further details
        :return: 1
        """
        # vector[vector[vector[string]]] c_signals
        self.c_signals.clear()

        cdef list t, acc, list_sig
        cdef str sig
        cdef vector[string] inner_signals
        cdef vector[vector[string]] outer_signals
        outer_signals.reserve(len(self.c_accounts))
        for t in signals:
            outer_signals.clear()
            for acc in t:
                inner_signals.clear()
                list_sig = [sig.encode() for sig in acc]
                inner_signals = list_sig
                outer_signals.push_back(inner_signals)
            self.c_signals.push_back(outer_signals)
        return 1

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef short merged_positions_from_py(self, dict merged_positions) except -1:
        """
        Parses Python dict of merged_positions and sets self.c_merged_positions.
        :param merged_positions: dict, see docstring of FXStrategy class regarding self.merged_positions for 
                                 further details
        :return: 1
        """
        # unordered_map[string, vector[double]] c_merged_positions
        self.c_merged_positions.clear()

        cdef list v
        cdef str k
        cdef vector[double] inner_mp
        inner_mp.reserve(merged_positions[list(merged_positions.keys())][0])
        for k, v in merged_positions.items():
            inner_mp.clear()
            inner_mp = v
            self.c_merged_positions[k.encode()] = inner_mp
        return 1

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef short total_balances_from_py(self, list total_balances) except -1:
        """
        Parses list of total_balances and sets self.c_total_balances.
        :param total_balances: list, see docstring of FXStrategy class regarding self.total_balances for further details
        :return: 1
        """
        # vector[vector[double]] c_total_balances
        self.c_total_balances.clear()

        cdef list l
        cdef vector[double] inner_total_balances
        inner_total_balances.reserve(len(self.c_accounts))
        for l in total_balances:
            inner_total_balances.clear()
            inner_total_balances = l
            self.c_total_balances.push_back(inner_total_balances)

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef short merged_total_balances_from_py(self, list merged_total_balances) except -1:
        """
        Parses list of merged_total_balances and sets self.c_merged_total_balances
        :param merged_total_balances: list, see docstring of FXStrategy class regarding self.merged_total_balances 
                                      for further details
        :return: 1
        """
        # vector[double] c_merged_total_balances
        self.c_merged_total_balances.clear()
        self.c_merged_total_balances = merged_total_balances
        return 1

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef short _signals_at_step_t_from_py(self, dict _signals_at_step_t) except -1:
        """
        Parses Python dict of _signals_at_step_t and sets self._c_signals_at_step_t.
        :param _signals_at_step_t: dict, see self.self_parse_signals_at_step_t or FXStrategy for further details
                                   key: index positions of respective account in self.c_accounts
                                   value: list of Python strings representing signals emitted at current time step
        :return: 1
        """
        # unordered_map[long,vector[string]] _c_signals_at_step_t
        cdef long k
        cdef list l, parsed_list
        cdef str s
        cdef vector[string] inner
        # we cannot reserve vector as lists in _signals_at_step_t might have varying lengths
        for k, l in _signals_at_step_t.items():
            inner.clear()
            if len(l) > 0:
                parsed_list = [s.encode() for s in l]
                inner = parsed_list
            self._c_signals_at_step_t[k] = inner
        return 1

    cdef short c_evaluate(self, dict data_frame, string reference_currency, bool_t append_to_results,
                          vector[vector[string]] *ret_signals, vector[unordered_map[string, double]] *ret_positions,
                          vector[double] *ret_total_balances) except -1:
        """
        Evaluates accounts and appends to cFXStrategy's internal storage if append_to_results is set to True.
        See FXStrategy.evaluate for further details.
        :param data_frame: dict, see FXStrategy.evaluate for further details.
        :param reference_currency: std:string
        :param append_to_results: std:bool, appends result to internal storage if True
        :param ret_signals: vector[vector[string]]*, pointer to where results to copy to
        :param ret_positions: vector[unordered_map[string, double]]*, pointer to where results to copy to
        :param ret_total_balances: vector[double]*, pointer to where results to copy to
        :return: 1
        """
        cdef vector[vector[string]] signals
        cdef vector[string] inner_signals
        cdef vector[long] signals_at_step_t_keys
        cdef long acc_index = 0
        cdef long comp_val
        signals.reserve(len(self.c_accounts))
        signals_at_step_t_keys.reserve(len(self.c_accounts))
        for n in self._c_signals_at_step_t:
            signals_at_step_t_keys.push_back(n.first)
        # signals_at_step_t_keys = list(self._c_signals_at_step_t)
        for acc_index in range(len(self.c_accounts)):
            inner_signals.clear()
            # if acc_index in signals_at_step_t_keys:
            for comp_val in signals_at_step_t_keys:
                if comp_val == acc_index:
                    inner_signals = self._c_signals_at_step_t[acc_index]
            signals.push_back(inner_signals)

        cdef vector[unordered_map[string, double]] positions
        positions.reserve(len(self.c_accounts))
        cdef str u
        cdef vector[string] all_currencies = [u.encode() for u in set(itertools.chain(*data_frame.keys()))]
        cdef long i = 0
        cdef unordered_map[string, double] dict_positions
        cdef string currency
        for i in range(len(self.c_accounts)):
            dict_positions.clear()
            for currency in all_currencies:
                try:
                    dict_positions[currency] = self.c_accounts[i].c_position(currency)
                except AttributeError:
                    dict_positions[currency] = self.c_accounts[i].position(currency.decode())
            positions.push_back(dict_positions)

        cdef vector[double] total_balances
        total_balances.reserve(len(self.c_accounts))
        cdef dict data_current_step
        cdef double v
        cdef tuple k
        cdef dict parsed_data_current_step
        try:
            data_current_step = {k: data_frame[k][-1] for k in data_frame.keys()}
        except (TypeError, IndexError):
            data_current_step = {k: data_frame[k] for k in data_frame.keys()}
        for i in range(len(self.c_accounts)):
            try:
                parsed_data_current_step ={(k[0].encode(), k[1].encode()): v for k, v in data_current_step.items()}
                total_balances.push_back(self.c_accounts[i].c_total_balance(exchange_rates=parsed_data_current_step,
                                                                            reference_currency=reference_currency))
            except AttributeError:
                total_balances.push_back(self.c_accounts[i].total_balance(exchange_rates=data_current_step,
                                                                          reference_currency=reference_currency.decode()))

        cdef double sum_total_balances = 0
        cdef double sum_positions
        cdef vector[double] vec_sum_positions
        cdef vector[double] pos
        cdef vector[vector[double]] vec_pos
        pos.reserve(positions.size())
        vec_pos.reserve(1)
        vec_sum_positions.reserve(1)
        if append_to_results:
            self._c_signals_at_step_t.clear()
            # self._c_signals_at_step_t = dict()
            self.c_signals.push_back(signals)
            self.c_total_balances.push_back(total_balances)

            for i in range(total_balances.size()):
                sum_total_balances = c_precision_add(sum_total_balances, total_balances[i])
            self.c_merged_total_balances.push_back(sum_total_balances)
            for currency in all_currencies:
                pos.clear()
                # pos = [dict_acc[currency] for dict_acc in positions]
                for dict_acc in positions:
                    pos.push_back(dict_acc[currency])
                try:
                    self.c_positions[currency].push_back(pos)
                except KeyError:
                    vec_pos.clear()
                    vec_pos.push_back(pos)
                    self.c_positions[currency] = vec_pos

                sum_positions = 0
                for i in range(pos.size()):
                    sum_positions = c_precision_add(sum_positions, pos[i])
                try:
                    self.c_merged_positions[currency].push_back(sum_positions)
                except KeyError:
                    vec_sum_positions.clear()
                    vec_sum_positions.push_back(sum_positions)
                    self.c_merged_positions[currency] = vec_sum_positions

        # vector[vector[string]], vector[unordered_map[string, double]], vector[double]
        ret_signals[0] = signals
        ret_positions[0] = positions
        ret_total_balances[0] = total_balances
        return 1

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef tuple c_wrap_evaluate(self, dict data_frame, string reference_currency, append_to_results):
        """
        Serves as wrapper between self.c_evaluate and FXStrategy.evaluate.
        See docstrings of self.c_evaluate and FXStrategy.evaluate for further details.
        :param data_frame: dict, see FXStrategy.evaluate for further details
        :param reference_currency: std:string
        :param append_to_results: std:bool, appends results to internal storage if True
        :return: 
        """
        cdef vector[vector[string]] signals
        cdef vector[unordered_map[string, double]] positions
        cdef vector[double] total_balances
        signals.reserve(len(self.c_accounts))
        positions.reserve(len(self.c_accounts))
        total_balances.reserve(len(self.c_accounts))

        self.c_evaluate(data_frame, reference_currency, append_to_results, &signals, &positions, &total_balances)

        cdef list ret_signals = []
        cdef list ret_inner_signals
        for outer_signal in signals:
            ret_inner_signals = []
            for inner_signal in outer_signal:
                ret_inner_signals.append(inner_signal.decode())
            ret_signals.append(ret_inner_signals)

        cdef list ret_positions = []
        cdef dict ret_inner_positions
        for outer_position in positions:
            ret_inner_positions = {}
            for inner_position in outer_position:
                ret_inner_positions[inner_position.first.decode()] = inner_position.second
            ret_positions.append(ret_inner_positions)

        cdef list ret_total_balances = []
        for tb in total_balances:
            ret_total_balances.append(tb)

        return ret_signals, ret_positions, ret_total_balances

    @cython.wraparound(False)
    cpdef short c_add_signal(self, long i, string signal) except -1:
        """
        Add signals to temporary container self._c_signals_at_step_t.
        Gets wrapped by FXStrategy.
        :param i: index position of account in self.c_accounts
        :param signal: std:string, signals of account i emitted at current time step
        :return: 1
        """
        cdef vector[string] vec
        vec.reserve(1)
        if self._c_signals_at_step_t.count(i) == 1:
            self._c_signals_at_step_t[i].push_back(signal)
        else:
            vec.push_back(signal)
            self._c_signals_at_step_t[i] = vec
            # self._signals_at_step_t[i] = []
            # self._signals_at_step_t[i].append(signal)
        return 1

    @cython.wraparound(False)
    cdef short c_run(self, dict price_data, string reference_currency, dict volume_data, long len_data,
                     vector[vector[vector[string]]] *ret_signals,
                     unordered_map[string, vector[vector[double]]] *ret_positions,
                     unordered_map[string, vector[double]] *ret_merged_positions,
                     vector[vector[double]] *ret_total_balances , vector[double] *ret_merged_total_balances) except -1:
        """
        Runs complete strategy by looping through price_data and evaluating at every time step. 
        See FXStrategy.run for further details. 
        :param price_data: dict,
                           keys: tuple of py_strings (base, quote)
                           value: list of floats representing exchange_rates at every time_step (including 
                                  historic lookback portion), all lists must have same length
                           see FXStrategy.run for further details 
        :param reference_currency: std:string
        :param volume_data: dict, same structure as param:price_data, but with volumes instead of exchange_rates,
                            see FXStrategy.run for further details
        :param len_data: long, length of lists contained in price_data (including historic lookback portion)
        :param ret_signals: vector[vector[vector[string]]]*, pointer to where results to copy to
        :param ret_positions: unordered_map[string, vector[vector[double]]]*, pointer to where results to copy to
        :param ret_merged_positions: unordered_map[string, vector[double]]*, pointer to where results to copy to
        :param ret_total_balances: vector[vector[double]]*, pointer to where results to copy to
        :param ret_merged_total_balances: vector[double]*, pointer to where results to copy to
        :return: 1
        """
        # >>>setup: get all currencies within data
        cdef list all_price_pairs
        cdef list all_volume_pairs
        all_price_pairs = list(price_data.keys())
        if len(volume_data) > 0:
            all_volume_pairs = list(volume_data.keys())
        else:
            all_volume_pairs = []

        # >>>reset account and storage
        self.c_reset()

        # prepare storage
        self._c_init_all_positions(list(price_data.keys()))

        # >>>execute strategy
        cdef vector[vector[string]] signals
        cdef vector[unordered_map[string, double]] positions
        cdef vector[double] total_balances
        cdef vector[long] current_clocks
        cdef vector[long] new_clocks
        signals.reserve(len(self.c_accounts))
        positions.reserve(len(self.c_accounts))
        total_balances.reserve(len(self.c_accounts))
        current_clocks.reserve(len(self.c_accounts))
        new_clocks.reserve(len(self.c_accounts))
        cdef long i = 0
        cdef dict price_data_point
        cdef dict volume_data_point
        cdef tuple k
        try:
            current_clocks = [acc._c_clock for acc in self.c_accounts]
        except AttributeError:
            current_clocks = [acc.clock for acc in self.c_accounts]

        for i in range(self.c_lookback, len_data):
            # >>>get current clock to determine if ticking is done within strategy_func
            current_clocks.clear()
            if not self.c_suppress_ticking:
                try:
                    current_clocks = [acc._c_clock for acc in self.c_accounts]
                except AttributeError:
                    current_clocks = [acc.clock for acc in self.c_accounts]

            # >>>get data for time step i with lookback
            price_data_point = {k: price_data[k][i - self.c_lookback: i + 1] for k in all_price_pairs}
            if len(volume_data) > 0:
                # noinspection PyUnboundLocalVariable
                volume_data_point = {k: volume_data[k][i - self.c_lookback: i + 1] for k in all_volume_pairs}

                # >>action, go!
                self.c_strategy_func(self.c_accounts, price_data_point, reference_currency.decode(), volume_data_point,
                                   self, **self.c_strategy_kwargs)
            else:
                volume_data_point = {}

                # >>action, go!
                self.c_strategy_func(self.c_accounts, price_data_point, reference_currency.decode(), None, self,
                                     **self.c_strategy_kwargs)

            # >>>tick, if needed
            new_clocks.clear()
            try:
                new_clocks = [acc._c_clock for acc in self.c_accounts]
            except AttributeError:
                new_clocks = [acc.clock for acc in self.c_accounts]
            # lazy evaluation
            if not self.c_suppress_ticking and current_clocks == new_clocks:
            # if not self.c_suppress_ticking and set_previous == set_current:
                if len(self.c_tick_kwargs) > 0:
                    self.c_tick_method(self, price_data_point, **self.c_tick_kwargs)
                else:
                    self.c_tick_method(self, price_data_point)

            # >>>evaluate results and simultaneously append to final internally stored results
            # only evaluate if not suppress_evaluation is set
            if not self.c_suppress_evaluation:
                self.c_evaluate(price_data_point, reference_currency, True, &signals, &positions, &total_balances)

        # >>>check if ticked
        new_clocks.clear()
        try:
            new_clocks = [acc._c_clock for acc in self.c_accounts]
        except AttributeError:
            new_clocks = [acc.clock for acc in self.c_accounts]
        if not self.c_suppress_ticking and current_clocks == new_clocks:
            raise tpz_exception.OperatingError('Account clocks have not been ticked although '
                                               'param:suppress_ticking=False specifies ticking behavior.')

        ret_signals[0] = self.c_signals
        ret_positions[0] = self.c_positions
        ret_merged_positions[0] = self.c_merged_positions
        ret_total_balances[0] = self.c_total_balances
        ret_merged_total_balances[0] = self.c_merged_total_balances
        return 1

    @cython.boundscheck(False)
    @cython.wraparound(False)
    cpdef list c_wrap_run(self, dict price_data, string reference_currency, dict volume_data, long len_data):
        """
        Serves as wrapper between self.c_run and FXStrategy.run.
        See docstrings of self.c_run and FXStrategy.run for further details.
        :param price_data: dict,
                           keys: tuple of py_strings (base, quote)
                           value: list of floats representing exchange_rates at every time_step (including 
                                  historic lookback portion), all lists must have same length
                           see FXStrategy.run for further details 
        :param reference_currency: std:string
        :param volume_data: dict, same structure as param:price_data, but with volumes instead of exchange_rates,
                            see FXStrategy.run for further details
        :param len_data: long, length of lists contained in price_data (including historic lookback portion)
        :return: list[reference_currency, ret_signals, ret_positions, ret_merged_positions,
                      ret_total_balances, ret_merged_total_balances]
                          reference_currency: py_str
                          ret_signals: list of lists of lists, see FXStrategy.signals
                          ret_positions: dict, see FXStrategy.positions
                          ret_merged_positions: dict, see FXStrategy.merged_positions
                          ret_total_balances: list of lists, see FXStrategy.total_balances
                          ret_merged_total_balances: list, see FXStrategy.merged_total_balances
        """
        cdef vector[vector[vector[string]]] signals
        cdef unordered_map[string, vector[vector[double]]] positions
        cdef unordered_map[string, vector[double]] merged_positions
        cdef vector[vector[double]] total_balances
        cdef vector[double] merged_total_balances

        self.c_run(price_data, reference_currency, volume_data, len_data,
                   &signals, &positions, &merged_positions, &total_balances, &merged_total_balances)

        # cdef vector[vector[vector[string]]] signals
        cdef list ret_signals = self.parse_signals(signals)

        # cdef unordered_map[string, vector[vector[double]]] positions
        cdef dict ret_positions = self.parse_positions(positions)

        # cdef unordered_map[string, vector[double]] merged_positions
        cdef dict ret_merged_positions = self.parse_merged_positions(merged_positions)

        # cdef vector[vector[double]] total_balances
        cdef list ret_total_balances = self.parse_total_balances(total_balances)

        # cdef vector[double] merged_total_balances
        cdef list ret_merged_total_balances = self.parse_merged_total_balances(merged_total_balances)

        return [reference_currency.decode(), ret_signals, ret_positions, ret_merged_positions,
                ret_total_balances, ret_merged_total_balances]


# noinspection PyAbstractClass,PyAttributeOutsideInit,PyUnresolvedReferences,PyTypeChecker
class FXStrategy(cFXStrategy, BaseStrategy):
    """
    Derived from BaseStrategy class. This implementation is meant to be used with FXAccount (patched by
    trapeza.account.order_management.monkey_patch() and unpatched version), but in principal can be used with any
    class derived from BaseAccount.

    Ties (multiple) accounts and a strategy decision function to one logical unit, such that strategy decision function
    only has to implement trading logic without caring about e.g. tick handling (cf. time discrete state machine/
    stacked automaton logic implementation by FXAccount) or evaluation of trades and result parsing.

    FXStrategy tries to tick (cf. time discrete state machine/ stack automaton logic implementation by FXAccount)
    FXAccount, if FXAccount.clock is not already ticked within strategy decision function separately (auto-detection
    whether accounts have been ticked within strategy decision function)
    and self.suppress_ticking=False, which controls if ticking is conducted within FXStrategy.

    Data supplied to FXStrategy.run() is looped through time step by time step. Thereby, parameter lookback controls
    how much historic data is supplied to the strategy decision function at each time step (e.g. how many previous
    time steps are passed to strategy decision function in addition to current time step).
    At each time step during looping through supplied data, strategy function is called once, all accounts are ticked
    (auto-detection whether ticking has already been done within strategy function) and evaluated repeatedly.
    As the parameter lookback controls the size of historic data, the start time step is located at index=lookback
    (zero-based indexing) within data supplied to FXStrategy.run(), every data located before the index=lookback is
    treated as historic data (therefore trading strategy starts at index=lookback as first 'current' time step and
    then continuously loops through every remaining time step in data).
    Nonetheless, input data has to be prepended/ padded manually with historic data (this is not done automatically)
    before FXStrategy.run() method is called.

    A separate tick function can be supplied, otherwise tick method (call signature) of FXAccount (respective
    monkey patched account by order_management) will be applied, provided that self.suppress_ticking=False.
    Auto-detects if account was patched by trapeza.account.order_management.monkey_patch() and then applies
    appropriate tick method. If self.suppress_ticking=True, ticking is suppressed (at least FXStrategy.run() does
    not try to tick accounts, accounts still can be ticked from within strategy decision function).
    Custom tick function must follow call signature:

        tick_func(self, data_point_t, **kwargs)

        self: placeholder in function signature in order to access self of this class
        data_point: dict with key:tuple(str, str) and value: float,
                    {(base, quote): current_rate,
                     (base, quote): current_rate,
                      ...}
                    dictionary of base and quote currency pair and their respective exchange rate
                    in FX direct notation base|quote (see docstring of FXAccount class for notation convention).
                    This argument is auto-generated within FXStrategy.run() (in the sense, that data supplied to
                    FXStrategy.run() is parsed to only containing current time step before passing to tick method) and
                    passed to tick_func automatically within method call.
                    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    Make sure custom tick_func accepts this data format
                    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        kwargs: additionally kwargs arguments,
                kwargs of tick_func can be passed to param:kwargs of FXStrategy.__init__(). parm:kwargs must be
                contained with identical names in param:kwargs, which are passed to FXStrategy.__init__(),
                see param:kwargs of FXStrategy.__init__().
                Similar names to kwargs of strategy_func are not allowed.

    Separate kwargs for tick function and strategy function can be supplied to FXStrategy.__init__() as one kwarg,
    as long as both do not share similar named kwarg arguments.

    self.reset() is called during backtesting and resets accounts (make sure, accounts implemented a reset method
    similar to FXAccount) as well as stored results (see below).

    self.run() is called during backtesting and in turn calls strategy decision functions. Handles setup (resetting
    stored results as well as accounts), data feed to strategy decision function (see above) and parsing of results
    (see below). Data has to be supplied as dict:
    {(base, quote): [val_0, val_1, ..., val_t], (base, quote): [val_0, val_1, ..., val_t]}, where val_t is the
    exchange rate at time step t in FX notation (direct notation as quote-base-pair, see FXAccount).
    Same logic applies to volume data passed into self.run() (if volume data is not None, see parameter description for
    more information, how volume data is handled and processed).
    If lookback is used, then prepend/ pad historic data of lookback to data dict manually as this is not handled
    automatically (price data as well as volume data passed into self.run()).

    Exchange rate is expressed in FX direct notation convention (direct notation, not volume notation):
    1.2 EUR|USD --> 1.2 USD for 1 EUR (see docstring of FXAccount class for further information on notation convention)

    In order to evaluate trade signals, FXStrategy class object has to be used by strategy decision function in order to
    'transmit' trade signals emitted by strategy logic: call FXStrategy.add_signal(acc, signal_str) within strategy
    decision function (pass FXStrategy object as function argument to externally defined strategy decision function).
    Signals can be any string, e.g. 'sell', 'buy', 'short', 'long'. Multiple signals can be
    'transmitted' by repeatedly calling FXStrategy.add_signal() method. Signals are only evaluable if strategy decision
    function calls FXStrategy.add_signal(acc, signal_str).
    Additionally, if signals contain the name of the currency (which are used within tuple of strings as key of price
    data), then signals will be visualized more concise within dashboard (see FXDashboard). Furthermore, see
    FXDashboard for how to construct strings for signals in order to extend visualization capabilities of analysis
    dashboard (e.g. formatting of signals dependent whether they contain certain key words such as 'sell' or 'buy').


    Input data to FXStrategy.run() is given as:
        {(base, quote): [rate_0, rate_1, ..., rate_t],
         (base, quote): [rate_0, rate_1, ..., rate_t],
         ...}
        All values (list or array of floats) of all keys (currency pairs) have to be of same length.
        If historic data shall be used by strategy_func (cf. lookback), historic data has to be prepended
        manually to param:data, e.g.:
            lookback = 3
            {(base, quote): [rate_-3, rate_-2, rate_-1, rate_0, rate_1, ... rate_t],
             (base, quote): [rate_-3, rate_-2, rate_-1, rate_0, rate_1, ... rate_t],
             ...}
        Data will be looped through one by one (time frame specified by lookback and current time step t
        [window size: lookback + 1]). Start time step is at index=lookback. Applies for price data and volume data as
        well. Exchange rate is expressed in FX notation convention (direct notation, not volume notation)
        1.2 EUR|USD --> 1.2 USD for 1 EUR

    Strategy decision function does not need to return anything as FXStrategy.evaluate() takes care of results
    (as long as strategy decision function internally calls methods of FXAccount object).
    Strategy decision function must take on following call signature:

        strategy_func(accounts, price_data_point, reference_currency, volume_data_point, fxstrategy, **strategy_kwargs):
            accounts: list (!) of account objects (inherited from BaseAccount)
            price_data_point: dict with key:tuple(str, str) and value:float or value:list of floats
                              or value:array of floats,
                              {(base, quote): current_rate,
                              (base, quote): current_rate,
                               ...}
                               or
                              {(base, quote): [rate_-2, rate_-1, current_rate],
                               (base, quote): [rate_-2, rate_-1, current_rate],
                               ...}
                              --> dependent on size of parameter lookback (whether to prepend historic data to each call
                                  to strategy decision function for each loop within FXStrategy.run())
                             dictionary of base and quote currency pair and their respective exchange
                             rate in FX direct Notation base|quote (or volume data in case of volume_data,
                             see self.run()).
                             Whether floats or list/ array of floats are used as dict values, is dependent on the
                             parameter lookback.
            reference_currency: str,
                                reference currency in which results shall be quoted
            volume_data_point: None or dict,
                               If None (passed in at self.run()), None will be passed into strategy_func at each call
                               (see self.run()).
                               If dict, then same format (and logic) as price_data_point.
            fxstrategy: initiated FXStrategy class object used for adding signals within strategy_func via
                        fxstrategy.add_signal(acc, signal_str)
            strategy_kwargs: dict,
                             additional custom key word arguments
                             kwargs of strategy_func can be passed to param:kwargs of FXStrategy.__init__().
                             param:strategy_kwargs must be contained with identical names in param:kwargs, which are
                             passed to FXStrategy.__init__(), see param:kwargs of FXStrategy.__init__().
                             Similar names to kwargs of tick_func are not allowed (name mangling).

    Results are stored within class object in the following format:
    self.signals: list of lists,
                  gives all signals per account and per time step, which are generated by strategy decision function

                     | signals of account 0               | signals of account 1               |...
                     V                                    V                                    V
                  [[[acc_0_sig_t_0, acc_0_sig_t_0, ...], [acc_1_sig_t_0, acc_1_sig_t_0, ...], [...]],   <-- time step 0
                   [[acc_0_sig_t_1, acc_0_sig_t_1, ...], [acc_1_sig_t_1, acc_1_sig_t_1, ...], [...]],   <-- time step 1
                   ...]

                   access data via: time_step, acc, signal_nr

    self.positions: dict: currency (str) as key, list of lists as values of position of account n at time step t
                    gives all positions (currencies) and their value (size, amount, volume) per account and
                    per time step

                                 | account 0  | account 1  ...  | account n
                                 V            V                 V
                    {currency: [[acc_0_val_0, acc_1_val_0, ..., acc_n_val_0],    <-- time step 0
                                [acc_0_val_1, acc_1_val_1, ..., acc_n_val_1],    <-- time step 1
                                 ... ... ...
                                [acc_0_val_t, acc_1_val_t, ..., acc_n_val_t]],   <-- time step n
                     currency: ...}

                     access data via: position, time_step, acc_nr

    self.merged_positions: dict: currency (str) as key, list as values per time step
                           sums up all similar positions across all accounts to one
                           composite position (currency) per time step

                           {currency: [val_0, ..., val_t],
                            currency: [val_0, ..., val_t]}

                           access data via: position, time_step

    self.total_balances: list of lists,
                         gives total account value (over all positions) in specified reference currency per each
                         account and time step

                             | account 0        | account 1        | ...
                             V                  V                  V
                           [[balance_acc_0_t_0, balance_acc_1_t_0, ...],    <-- time step 0
                            [balance_acc_0_t_1, balance_acc_1_t_1, ...],    <-- time step 1
                            ...]

                         access data via: time_step, acc_nr

    self.merged_total_balances: list,
                                sums up total balances of all accounts per each time step; total balances are
                                all set to same reference currency; resembles total value of strategy with
                                respect to all used accounts per time step

                                  |time step 0 |time step 1 |...
                                  V            V            V
                                 [balance_t_0, balance_t_1, ....]

                                access data via: time_step
    Internally stored results will be accessed by backtesting engine, therefore do not disturb or manipulate
    those values manually. Furthermore, retrieving class attributes via e.g. self.signals returns a ProtectedDict (or
    ProtectedList, see implementation in trapeza.utils). Those ProtectedDicts are immutable. This is because FXStrategy
    wraps an underlying C++ implementation, and manipulating single indices/ elements of e.g. self.signals directly
    would not take effects on the underlying C++ implementation. Instead, users have to set a whole list (or dict)
    directly, if class attributes shall be manipulated, e.g. self.signals = some_list (see setter methods
    of FXStrategy).

    At each call to run, FXStrategy internal storage (which holds final results) and accounts are reset.
    Additionally depots of accounts are reset to the same depot status as when FXStrategy.__init__() was called (this
    is stored in self._init_accs_depots, see notes above on ProtectedDicts/ ProtectedLists).
    This also applies to clocks of accounts at time of initialization of FXStrategy as they are restored as well after
    each run (see self._acc_clocks). This means, FXStrategy.run() can be called repeatedly in such a way, that each call
    simulates an independent simulation run starting from the same account status as at time of FXStrategy.__init__() at
    every run. Calling FXStrategy.run() repeatedly is therefore safe and every time just simulates starting as if
    accounts have been freshly initialized with their initial account.depot and account.clock status as well as a fresh
    internal storage of FXStrategy. Internal reset is done BEFORE each run, but not after!

    Quick Start:
        >>  # define custom strategy decision function, make sure it follows call signature defined above
        >>  def awesome_strategy(accounts, price, reference_currency, volume, fxstrat):
        >>      # implement custom decision logic for one time step
        >>      [custom trade logic, which only can operate on current time step + historic lookback of
        >>       price and volume data]
        >>
        >>      # add signal called whatever you want, which is executed by certain account; use FXStrategy object
        >>      fxstrat.add_signal(accounts[0], 'awesome_transaction')  # str: signal name
        >>
        >>      # add signal called whatever you want, which is executed by another account; use FXStrategy object
        >>      fxstrat.add_signal(accounts[1], 'great_transaction')    # str: signal name
        >>
        >>      # execute trades with both accounts
        >>      accounts[0].awesome_transaction(...)    # some arbitrary transaction conducted by account 0
        >>      accounts[1].great_transaction(...)      # some arbitrary transaction conducted by account 1
        >>
        >>  # open up (init) two accounts
        >>  accs = [FXAccount(...) for _ in range(2)]
        >>
        >>  # init FXStrategy class object
        >>  strat = FXStrategy('genesis', accs, awesome_strategy, lookback=0)
        >>
        >>  # accounts and decision function are now registered as one logical unit and are ready for backtesting
        >>  strat.run(all_price_data, 'USD', all_volume_data)
        >>  # alternatively if awesome_strategy() does not need any volume data for its trade logic:
        >>  # strat.run(all_price_data, 'USD', None)

    Customization of iteration/ looping logic:
    If a more granular control of account behavior is needed within the strategy decision function, iteration/ looping
    logic of FXStrategy.run() can be suppressed by setting the parameter lookback to
    'lookback = length of data (number of max. time steps) - 1'. This limits the number of calls to the strategy
    decision function effectively to only once within FXStrategy.run() method, such that looping and ticking can be
    done entirely within strategy decision function without outside interference of FXStrategy.run().
    Nonetheless, ticking and evaluation have to been done manually then within strategy decision function.
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    Therefore first add all signals and tick all account clocks before calling FXStrategy.evaluate().
    Make sure, append_to_results is set to True when calling FXStrategy.evaluate().
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    FXStrategy.evaluate(): when append_to_results is set to False, accounts will be evaluated (but not internally
    altered, so repeated call to evaluate is safe in the sense of not changing internal states of accounts and
    retrieving same results after each call), but evaluation results will not be written to internal storage of results
    within FXStrategy. Results are therefore not accessible for backtest evaluation. Repeated call to
    FXStrategy.evaluate is safe not to alter any data and delivers same results after each call if append_to_results
    is set to False.
    If append_to_results is set to True, evaluation results will be written to internal storage of results within
    FXStrategy and are accessible for backtest analysis. Every call to FXStrategy.evaluate() resembles the evaluation
    at one sequential time step t+1 if append_to_results is set to True. So whenever a time step is passed, make a
    call to FXStrategy.evaluate(). This has only to be done, if ticking and evaluation is done manually in
    strategy decision function. If the users relays on the auto-ticking during FXStrategy.run(), FXStrategy.evaluate()
    does not need to be called separately.
    !!! In order to retrieve correct results, first tick all account clocks (cf. internal time discrete state machine
        within FXAccount) to make sure, all transactions take place at evaluation !!!
    !!! FXStrategy.evaluate() cleans internal short term storage of signals (if append_to_results=True).
        This means, after calling FXStrategy.evaluate(), all signals which are appended via FXStrategy.add_signal()
        afterwards are assigned to the next time step/ until next call to FXStrategy.evaluate(). All signals, which are
        added before call to FXStrategy.evaluate(), will be assigned to the same time step as FXStrategy.evaluate()
        (internal storage will be cleaned after method call such that adding new signals will not interfere with
        previously added signals)
        (keep in mind to first tick all accounts before calling FXStrategy.evaluate(), otherwise accounts will not
        perform desired transactions within strategy decision function, especially when processing durations are
        involved) !!!
    When calling FXStrategy.evaluate() manually and accounts are patched by
    trapeza.account.order_management.monkey_patch(), then account.tick(data_point_t_including_lookback) must be
    assembled manually whenever accounts are ticked from inside strategy decision function. This means, data passed to
    account.tick() has to include current time step (set manually) including all historic data according to lookback
    (as mentioned earlier, volume data is only used for trading logic, but not for ticking accounts or evaluating
    strategy).
    Example:
        >>  # define custom strategy decision function, make sure it follows call signature defined above
        >>  def awesome_strategy(accounts, price, reference_currency, volume, fxstrat):
        >>      # implement custom decision logic, which only gets called once but has the entire data set available
        >>      # for calculations, which was passed to fxstrat.run()
        >>      [custom trade logic, which can operate on the whole data set for prices and volumes]
        >>
        >>      # add signal called whatever you want, which is executed by certain account; use FXStrategy object
        >>      fxstrat.add_signal(accounts[0], 'awesome_transaction')  # str: signal name
        >>
        >>      # add signal called whatever you want, which is executed by an other account; use FXStrategy object
        >>      fxstrat.add_signal(accounts[1], 'great_transaction')    # str: signal name
        >>
        >>      # execute trades with both accounts
        >>      accounts[0].awesome_transaction(...)
        >>      accounts[1].great_transaction(...)
        >>
        >>      # tick accounts: data_point is all data at corresponding time step t plus historic lookback as dict
        >>      _ = [acc.tick() for acc in accounts]    # alternatively: acc.tick(data_point_t_including_lookback)
        >>
        >>      # evaluate and store results: pass data argument as same variable from strategy function argument
        >>      # argument data is the same variable for awesome_strategy() as well as fxstrat.evaluate
        >>      fxstrat.evaluate(data, reference_currency, append_to_results=True)
        >>
        >>      # from here on a new time step starts:
        >>      [custom trade logic, which can operate on the whole data set for prices and volumes]
        >>      [add signals]
        >>      [make transactions]
        >>      [tick accounts with data_point_t+1_including_lookback]
        >>      [evaluate]
        >>
        >>      # and so on and so forth
        >>      # volume data is not needed for ticking or evaluating, but solely for custom trade logic
        >>
        >>  # init FXStrategy class object, force run() to only run once by setting appropriate lookback
        >>  strat = FXStrategy('genesis', accs, awesome_strategy, lookback=length_of_data - 1)
        >>
        >>  # accounts and decision function are now registered as one logical unit and are ready for backtesting
        >>  strat.run(all_price_data, 'USD', all_volume_data)
        >>  # alternatively if awesome_strategy() does not need any volume data for its trade logic:
        >>  # strat.run(all_price_data, 'USD', None)

    Results of the run simulation of FXStrategy can be accessed by the class object attributes:
        'FXStrategy.positions', 'FXStrategy.merged_positions', 'FXStrategy.total_balances',
        'FXStrategy.merged_total_balances', 'FXStrategy.signals'
        (ProtectedDicts/ ProtectedLists will be returned, single indices/ elements are immutable and can not be
        manipulated directly. Cast to dict/ list via new variable if single elements shall be manipulated.)
    Those results can be plotted easily via:
        >>  from matplotlib import pyplot as plt
        >>
        >>  # plot time series of the total strategy balance across all accounts referenced in 'USD' after running
        >>  # strategy simulation via fxstrat.run(...)
        >>  plt.figure()
        >>  plt.plot(range(len_data), fxstrat.merged_total_balances)

    Regarding the strategy decision function parameter 'accounts', a list of accounts is always passed to strategy
    decision function during self.run().
    Even if a single account is passed to FXStrategy.__init__, strategy decision function will receive a list of
    account(s), e.g. in this case [acc_0] if FXStrategy('genesis', acc_0, awesome_strategy, lookback=42).

    For adding signals, FXStrategy.add_signal() will automatically assign signal string to the right account, which
    is passed as argument to FXStrategy.add_signal(account, signal). Signals in FXStrategy.signals (internal storage
    holding final results after FXStrategy.run()) are in the same order as the list of accounts passed
    to FXStrategy.__init__().

    !!! kwargs of tick_func and kwargs of strategy_func must not share same argument names (name conflicts) !!!

    If FXDashboard shall be used for visualization:
            if signal string contains currency (or whatever is defined by data dict, see FXStrategy.run()) as substring,
            signal will be appropriately visualized on the same line chart as currency. If signal string contains
            one of the keys of param:signal_symbols dict at FXDashboard.__init__ as substring, signal will be
            appropriately visualized with therein defined symbol shape and color.
            signal string therefore must not contain multiple currencies as substring, nor multiple keys of
            param:signal_symbols dict at FXDashboard.__init__, but only one currency and only one key of
            param:signal_symbols as substring.
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            !!! signal names, which are appended with FXStrategy.add_signal(), should not contain multiple substrings
                of either currencies (or assets or whatever defines keys of FXEngine.price_data dictionary) nor keys
                of shape defining dictionary (param:signal_symbols at FXDashboard.__init__) !!!
                Recommendation: signal names should be mutual free of substring parts to each other,
                otherwise they might be visualized multiple times at FXDashboard !!!
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """

    @property
    def name(self):
        """
        Return FXStrategy.name
        :return: str
        """
        return self.c_name.decode()
    @name.setter
    def name(self, inp):
        """
        Set FXStrategy.name
        :param inp: str
        :return: None
        """
        check_types([inp], [str], ['name setter'], self._c_ignore_type_checking)
        self.c_name = inp.encode()
    @name.deleter
    def name(self):
        del self.name

    @property
    def accounts(self):
        """
        Return list of accounts contained in FXStrategy.
        :return: ProtectedList, immutable
        """
        return ProtectedList(self.c_accounts)
    @accounts.setter
    def accounts(self, inp):
        """
        Set list of accounts (use is not recommended, instead set proper list of accounts at __init__).
        :param inp: list of FXAccount (or derived from BaseAccount) objects
        :return: None
        """
        check_types([inp], [list], ['account setter'], self._c_ignore_type_checking)
        if not self._c_ignore_type_checking:
            inp = self._check_parse_accounts(inp)
        self.c_accounts = inp
    @accounts.deleter
    def accounts(self):
        del self.accounts

    @property
    def lookback(self):
        """
        Returns FXStrategy.lookback. This denotes the historic lookback data, which is available at time step 0.
        See docstring of FXStrategy class.
        :return: int
        """
        return self.c_lookback
    @lookback.setter
    def lookback(self, inp):
        """
        Set new lookback
        :param inp: int
        :return: None
        """
        check_types([inp], [int], ['lookback setter'], self._c_ignore_type_checking)
        self.c_lookback = inp
    @lookback.deleter
    def lookback(self):
        del self.lookback

    @property
    def suppress_ticking(self):
        """
        Returns status if ticking of accounts is suppressed (=True) or if accounts are automatically ticked during
        FXStrategy.run (=False)
        :return: bool
        """
        return self.c_suppress_ticking
    @suppress_ticking.setter
    def suppress_ticking(self, inp):
        """
        Set new status whether to suppress automatic ticking (=True).
        :param inp: bool
        :return: None
        """
        check_types([inp], [bool], ['suppress_ticking setter'], self._c_ignore_type_checking)
        self.c_suppress_ticking = inp
    @suppress_ticking.deleter
    def suppress_ticking(self):
        del self.suppress_ticking

    @property
    def suppress_evaluation(self):
        """
        Returns status if evaluation of accounts is suppressed (=True) at every time step (iteration) of FXStrategy.run.
        :return: bool
        """
        return self.c_suppress_evaluation
    @suppress_evaluation.setter
    def suppress_evaluation(self, inp):
        """
        Set new status whether to suppress evaluation at every time step (iteration) during FXStrategy.run.
        :param inp: bool
        :return: None
        """
        check_types([inp], [bool], ['suppress_evaluation', self._c_ignore_type_checking])
        self.c_suppress_evaluation = inp
    @suppress_evaluation.deleter
    def suppress_evaluation(self):
        del self.suppress_evaluation

    @property
    def strategy_kwargs(self):
        """
        Returns kwargs for strategy decision function. See docstring of FXStrategy class for further details.
        :return: Protected dict, immutable
        """
        return ProtectedDict(self.c_strategy_kwargs)
    @strategy_kwargs.setter
    def strategy_kwargs(self, inp):
        """
        Set a new kwargs dict for strategy decision function. See docstring of FXStrategy class for further details.
        :param inp: dict
        :return: None
        """
        check_types([inp], [dict], ['strategy_kwargs setter'], self._c_ignore_type_checking)
        self.c_strategy_kwargs = inp
    @strategy_kwargs.deleter
    def strategy_kwargs(self):
        del self.c_strategy_kwargs

    @property
    def tick_kwargs(self):
        """
        Returns kwargs for (alternative) ticking method. See docstring of FXStrategy class for further details.
        :return: Protected dict, immutable
        """
        return ProtectedDict(self.c_tick_kwargs)
    @tick_kwargs.setter
    def tick_kwargs(self, inp):
        """
        Set a new kwargs dict for (alternative) ticking method. See docstring of FXStrategy class for further details.
        :param inp: dict
        :return: None
        """
        check_types([inp], [dict], ['tick_kwargs setter'], self._c_ignore_type_checking)
        self.c_tick_kwargs = inp
    @tick_kwargs.deleter
    def tick_kwargs(self):
        del self.c_tick_kwargs

    @property
    def strategy_func(self):
        """
        Returns strategy decision function (as object).
        :return: callable function object
        """
        return self.c_strategy_func
    @strategy_func.setter
    def strategy_func(self, inp):
        """
        Set new strategy decision function.
        :param inp: callable function object
        :return: None
        """
        check_types([inp], [callable], ['strategy_func setter'], self._c_ignore_type_checking)
        self.c_strategy_func = inp
    @strategy_func.deleter
    def strategy_func(self):
        del self.strategy_func

    @property
    def tick_method(self):
        """
        Returns (alternative) ticking method for accounts.
        :return: callable function object
        """
        return self.c_tick_method
    @tick_method.setter
    def tick_method(self, inp):
        """
        Set new (alternative) ticking method for accounts.
        :param inp: callable function object
        :return: None
        """
        check_types([inp], [callable], ['tick_func setter'], self._c_ignore_type_checking)
        self.c_tick_method = inp
    @tick_method.deleter
    def tick_method(self):
        del self.tick_method

    @property
    def _init_accs_depots(self):
        """
        Return initial depot states of all accounts contained in FXStrategy.
        :return: ProtectedList of dicts, immutable
        """
        return ProtectedList(self._c_init_accs_depots)
    @_init_accs_depots.setter
    def _init_accs_depots(self, inp):
        """
        Set new initial depot states of all accounts contained in FXStrategy.
        :param inp: list of dicts, see FXAccount for further information on dict structure for account's depot
                    dict with str:currency (or asset) as key and float (position size) as value
        :return: None
        """
        check_types([inp], [list], ['_init_accs_depots setter'], self._c_ignore_type_checking)
        if not self._c_ignore_type_checking:
            for i in inp:
                check_types([i], [dict], ['_init_accs_depots setter list must contain dicts'],
                            self._c_ignore_type_checking)
        self._c_init_accs_depots = inp
    @_init_accs_depots.deleter
    def _init_accs_depots(self):
        del self._init_accs_depots

    @property
    def _accs_clocks(self):
        """
        Return list of all accounts' clocks (current time steps per account).
        :return: ProtectedList, immutable
        """
        return ProtectedList(self._c_accs_clocks)
    @_accs_clocks.setter
    def _accs_clocks(self, inp):
        """
        Set new list of all accounts' clocks (current time step per account)
        :param inp: list of ints
        :return: None
        """
        check_types([inp], [list], ['_accs_clocks setter'], self._c_ignore_type_checking)
        if not self._c_ignore_type_checking:
            for i in inp:
                check_types([i], [int], ['_accs_clocks setter list must contain floats'],
                            self._c_ignore_type_checking)
        self._c_accs_clocks = inp
    @_accs_clocks.deleter
    def _accs_clocks(self):
        del self._accs_clocks

    # protected
    @property
    def positions(self):
        """
        Returns dict of self.positions. See docstring of FXStrategy class for further information.
        :return: ProtectedDict, immutable
        """
        return ProtectedDict(self.self_parse_positions())
    @positions.setter
    def positions(self, inp):
        """
        Set new dict of positions to self.positions. See docstring of FXStrategy class for further information.
        :param inp: dict,
                    key: str (currency or asset)
                    value: list of lists floats (list at every time step consisting of lists of position sizes for
                           each account)
                    See docstring of FXStrategy class for further information.
        :return: None
        """
        check_types([inp], [dict], ['position setter'], self._c_ignore_type_checking)
        if not self._c_ignore_type_checking:
            for k, v in inp:
                check_types([k, v], [str, list], ['key in position setter dict', 'value in position setter dict'],
                            self._c_ignore_type_checking)
                # sample checks
                check_types([v[0]], [list], ['time step list in value of position setter dict'],
                            self._c_ignore_type_checking)
                check_types([v[0][0]], [float], ['float value in time step list as value of position setter dict'],
                            self._c_ignore_type_checking)
        self.position_from_py(inp)
    @positions.deleter
    def positions(self):
        del self.positions

    @property
    def merged_positions(self):
        """
        Returns dict of self.merged_positions. See docstring of FXStrategy class for further information.
        :return: ProtectedDict, immutable
        """
        return ProtectedDict(self.self_parse_merged_positions())
    @merged_positions.setter
    def merged_positions(self, inp):
        """
        Set new dict of merged_positions to self.merged_positions. See docstring of FXStrategy class for
        further information.
        :param inp: dict,
                    key: str (currency or asset)
                    value: list of floats (position size over all accounts at every time step)
                    See docstring of FXStrategy class for further information.
        :return: None
        """
        check_types([inp], [dict], ['merged_positions setter'], self._c_ignore_type_checking)
        if not self._c_ignore_type_checking:
            for k, v in inp:
                check_types([k, v], [str, list],
                            ['key in merged_positions setter dict', 'value in merged_positions setter dict'],
                            self._c_ignore_type_checking)
                # sample check
                check_types([v[0]], [float], ['float value in value list of merged_positions setter dict'],
                            self._c_ignore_type_checking)
        self.merged_positions_from_py(inp)
    @merged_positions.deleter
    def merged_positions(self):
        del self.merged_positions

    @property
    def total_balances(self):
        """
        Returns list of self.total_balances. See docstring of FXStrategy class for further information.
        :return: ProtectedList, immutable
        """
        return ProtectedList(self.self_parse_total_balances())
    @total_balances.setter
    def total_balances(self, inp):
        """
        Set new list of total_balances to self.total_balances. See docstring of FXStrategy class for further information.
        :param inp: list of list of floats, lists at every time step of lists of total_balances for each account.
                    See docstring of FXStrategy class for further information.
        :return: None
        """
        check_types([inp], [list], ['total_balances setter'], self._c_ignore_type_checking)
        # sample checks
        check_types([inp[0], inp[0][0]], [list, float],
                    ['time step list of total_balances setter',
                     'float value in time step list of total_balances setter'],
                    self._c_ignore_type_checking)
        self.total_balances_from_py(inp)
    @total_balances.deleter
    def total_balances(self):
        del self.total_balances

    @property
    def merged_total_balances(self):
        """
        Returns list of self.merged_total_balances. See docstring of FXStrategy class for further information.
        :return: ProtectedList, immutable
        """
        return ProtectedList(self.self_parse_merged_total_balances())
    @merged_total_balances.setter
    def merged_total_balances(self, inp):
        """
        Set new list of merged_total_balances to self.merged_total_balances. See docstring of FXStrategy class for
        further information.
        :param inp: list of floats, merged_total_balances over all accounts at each time step
        :return: None
        """
        check_types([inp], [list], ['merged_total_balances setter'], self._c_ignore_type_checking)
        # sample check
        check_types([inp[0]], [float], ['float value in list of merged_total_balances setter'],
                    self._c_ignore_type_checking)
        self.merged_total_balances_from_py(inp)
    @merged_total_balances.deleter
    def merged_total_balances(self):
        del self.merged_total_balances

    @property
    def signals(self):
        """
        Returns list of self.signals. See docstring of FXStrategy class for further information.
        :return: ProtectedList, immutable
        """
        return ProtectedList(self.self_parse_signals())
    @signals.setter
    def signals(self, inp):
        """
        Set new list of signals to self.signals. See docstring of FXStrategy class for further information.
        :param inp: list of list of list of strings, list for each time step of lists of emitted signals for
                    each account.
                    See docstring of FXStrategy class for further information.
        :return: None
        """
        check_types([inp], [list], ['signals setter'], self._c_ignore_type_checking)
        # sample checks
        check_types([inp[0], inp[0][0]], [list, list],
                    ['time step list of signals setter', 'account list in time step list of signals setter'],
                    self._c_ignore_type_checking)
        if len(inp[0][0]) > 0:
            check_types([inp[0][0][0]], [str], ['signal of account in signals setter'], self._c_ignore_type_checking)
        self.signals_from_py(inp)
    @signals.deleter
    def signals(self):
        del self.signals

    @property
    def _signals_at_step_t(self):
        """
        Returns dict of self._signals_at_step_t.
        This as an intermediate and temporary container, which stores signals emitted at the current time step.
        :return: ProtectedDict, immutable,
                 keys: int, index position of account in self.accounts
                 value: list of strings representing signals emitted by account i at current time step
        """
        # readonly access (cython extension type)
        return ProtectedDict(self.self_parse_signals_at_step_t())
    @_signals_at_step_t.setter
    def _signals_at_step_t(self, inp):
        """
        Sets new dict of _signals_at_step_t to self._signals_at_step_t.
        This as an intermediate and temporary container, which stores signals emitted at the current time step.
        :param inp: dict,
                    keys: int, index position of account in self.accounts
                    value: list of strings representing signals emitted by account i at current time step
        :return: None
        """
        check_types([inp], [dict], ['_signals_at_step_t setter'],  self._c_ignore_type_checking)
        # sample check
        if len(inp) > 0:
            check_types([list(inp.keys())[0]], [int], ['key in _signals_at_step_t setter dict'],
                        self._c_ignore_type_checking)
            check_types([inp[list(inp.keys())[0]]], [list], ['list as value in _signals_at_step_t setter dict'],
                        self._c_ignore_type_checking)
        if len(inp[list(inp.keys())[0]]) > 0:
            check_types([inp[list(inp.keys())[0]][0]], [str],
                        ['value in list as value in _signals_at_step_t setter dict'], self._c_ignore_type_checking)

        self._signals_at_step_t_from_py(inp)
    @_signals_at_step_t.deleter
    def _signals_at_step_t(self):
        del self._signals_at_step_t

    @property
    def _ignore_type_checking(self):
        """
        Returns current status whether types are checked (=False) at every method call or if checks are ignored (=True).
        See docstring of FXStrategy class for further information.
        :return: bool
        """
        # readonly access (cython extension type)
        return self._c_ignore_type_checking


    def __init__(self, str name, accounts, strategy_func, long lookback, tick_func=None, suppress_ticking=False,
                 suppress_evaluation=False, ignore_type_checking=False, **kwargs):
        """
        Initializes FXStrategy class object to tie strategy decision function and accounts to one logical unit, which
        then can be passed to backtest analysis engine. Make sure to use this class object within strategy decision
        function to add signals (e.g. fxstrat.add_signal called inside externally defined strategy decision function).

        FXStrategy object shall also be used within strategy_func for adding signals.

        FXStrategy.run() handles ticking and parses output in the appropriate format for subsequent analysis during call
        within FXStrategy.run(). Internal reset is done BEFORE each run, but not after!

        !!! kwargs of tick_func and kwargs of strategy_func must not share same argument names (name conflict) !!!

        :type name: str
        :param name: str,
                     name of this strategy & accounts combination, unique name used for visualization and identification
                     purposes
        :param accounts: list of FXAccounts (or other objects derived from BaseAccount) or
                         single FXAccount (or other object derived from BaseAccount)
        :param strategy_func: function with call signature:
                                  strategy_func(accounts, price_data_point, reference_currency, volume_data_point,
                                                fxstrategy, **strategy_kwargs)

                                  accounts: list of account objects (inherited from BaseAccount)
                                  price_data_point: dict with key:tuple(str, str) and value:float
                                                    or value:list of floats or value:array of floats
                                                    dictionary of base and quote currency pair and their respective
                                                    exchange rate in FX Notation base|quote
                                                    {(base, quote): [current_rate],
                                                     (base, quote): [current_rate],
                                                      ...}
                                                     or
                                                    {(base, quote): [rate_-2, rate_-1, current_rate],
                                                     (base, quote): [rate_-2, rate_-1, current_rate],
                                                     ...}
                                                    --> dependent on size of parameter lookback (whether to prepend
                                                        historic data to each call to strategy decision function for
                                                        each loop within FXStrategy.run())
                                                    If floats or list or array of floats are used as dict values is
                                                    dependent on the parameter lookback.
                                  reference_currency: str,
                                                      reference currency in which results shall be quoted
                                  volume_data_point: None or dict,
                                                     if dict, then in the same format as price_data_point (e.g. with
                                                     volume data instead of exchange rate data)
                                  fxstrategy: initiated FXStrategy class object used for adding signals within
                                              strategy_func via fxstrategy.add_signal(signal_str)
                                  strategy_kwargs: dict,
                                                   additional custom key word arguments.
                                                   kwargs of strategy_func can be passed to param:kwargs. Must be
                                                   contained with identical names in param:kwargs, which are passed to
                                                   FXStrategy.__init__(), see param:kwargs.
                                                   Similar names to kwargs of tick_func are not allowed.

                            Ticking can either be done within strategy_func or otherwise is done in self.run()
                            (auto-detection, also refer to param:suppress_ticking; auto-detection if accounts have
                            been patched by trapeza.account.order_management.monkey_patch()).
                            Strategy_func does not have to return any values, values are fetched by
                            FXStrategy.evaluate(). Just make sure, ticking of accounts happens before
                            FXStrategy.evaluate() such that effect of transactions on accounts has taken place

                            Regarding the strategy decision function parameter 'accounts', a list of accounts is always
                            passed to strategy decision function during self.run(). Even if a single account is passed
                            to FXStrategy.__init__, strategy decision function will receive a list of account(s),
                            e.g. in this case [acc_0] if FXStrategy('genesis', acc_0, awesome_strategy, lookback=42).
        :param lookback: int,
                         number of time steps which are treated as historic data when data is supplied to self.run().
                         Historic data has to be prepended to data manually. Start time step is located at
                         index=lookback (zero-based indexing). See docstring of class.
        :param tick_func: func, default=None
                          custom function for ticking accounts.

                          Default=None, which means internal default function is applied: account.tick() or
                          account.tick(data) of FXAccount (handles both cases automatically, cf. patch by
                          trapeza.account.order_management.monkey_patch()).

                          Ignored if param:suppress_ticking is set to True.

                          Must have following call signature:
                            tick_func(self, data_point, **kwargs)

                            self: placeholder in function signature to access self of this class
                            data_point: same as price_data_point in param:strategy_func
                                        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                        Make sure custom tick_func accepts this data format
                                        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                            kwargs: additionally kwargs arguments,
                                    kwargs of tick_func can be passed to param:kwargs. Must be contained with identical
                                    names in param:kwargs, which are passed to FXStrategy.__init__(), see param:kwargs.
                                    Similar names to kwargs of strategy_func are not allowed.

                          Volume data is not needed within ticking. Sell and buy volumes are set by account.sell() and
                          account.buy(). To calculate order size, only price data is needed. Therefore tick_func does
                          not need to be supplied with (market/ trading) volume data.
        :param suppress_ticking: bool, default=False,
                                 If set to True, ticking of accounts (internal time-state machine) is ignored (at least
                                 self.run() does not try to tick accounts, accounts still can be ticked from inside
                                 param:strategy_func),
                                 If set to False, accounts will be ticked according to param:tick_func
        :param suppress_evaluation: bool, default=False
                                    If set to False, accounts will be evaluated via FXStrategy.evaluate at every time
                                    step (iteration) during FXStrategy.run.
                                    If set to True, accounts will not be automatically evaluated at each time step
                                    (iteration) of FXStrategy.run, but the user has to do this manually, which is
                                    especially handy when implementing custom looping behaviour (see documentation
                                    'strategy.md').
        :param kwargs: additional key word arguments,
                       kwargs can be supplied for param:tick_func (if function is passed as argument to
                       FXStrategy.__init__() method, respectively param:tick_func is not None) and for
                       param:strategy_func all in one.
                       Auto-splits kwargs into kwargs of param:tick_func and param:strategy_func as long as both do
                       not use same argument names!
        :param ignore_type_checking: bool,
                                     if True, type checking is omitted, which increases performance but is less safe
        :return: None
        :raises: trapeza.OperatingError: if kwargs of strategy_func and tick_func have identically named arguments
                 TypeError: if types do not match up,
                            only thrown if ignore_type_checking is False (type_checking enabled at __init__)
        """
        check_types([name], [str], ['name'], ignore_type_checking)
        # >>>check if account inherits from trapeza.account.base_account.BaseAccount and assign to self.accounts
        accounts = self._check_parse_accounts(accounts)

        # >>>check types and store attributes
        check_types([strategy_func, kwargs, lookback, suppress_ticking, suppress_evaluation],
                    [callable, dict, int, bool, bool],
                    ['strategy_func', '**kwargs', 'lookback', 'suppress_ticking', 'suppress_evaluation'],
                    ignore_type_checking)

        if tick_func is None:
            tick_method = _c_tick_method
        else:
            tick_method = tick_func

        # >>>split kwargs into strategy_func and tick_func
        if tick_func is None:
            strategy_kwargs = kwargs
            tick_kwargs = dict()
        else:
            # first check if any of the strategy decision function's and any of the tick function's arguments are named
            # the same
            strategy_param_names = [k for k, _ in inspect.signature(strategy_func).parameters.items()]
            tick_param_names = [k for k, _ in inspect.signature(tick_func).parameters.items()]
            intersection_param_names = set(strategy_param_names).intersection(set(tick_param_names))
            if len(intersection_param_names):
                raise tpz_exception.OperatingError('param:strategy_func and param:tick_func have identically named'
                                                   'parameters/ kwargs, which makes it impossible to evaluate'
                                                   'param:**kwargs during class initialization. '
                                                   '\n Identically named params: {}'.format(intersection_param_names))
            # the first five arguments of strategy decision function are positional and therefore irrelevant
            # the first two arguments of tick function are positional and therefore irrelevant
            # positional arguments are passed as positional arguments in the main c_run() function, only the rest is
            # passed as kwargs and are therefore relevant in the following
            strategy_param_names = [k for k, _ in list(inspect.signature(strategy_func).parameters.items())[5:]]
            tick_param_names = [k for k, _ in list(inspect.signature(tick_func).parameters.items())[2:]]
            strategy_kwargs = {k: kwargs[k] for k in kwargs if k in strategy_param_names}
            tick_kwargs = {k: kwargs[k] for k in kwargs if k in tick_param_names}

        super().__init__(name.encode(), accounts, strategy_func, lookback, tick_method, suppress_ticking,
                         ignore_type_checking, strategy_kwargs, tick_kwargs, suppress_evaluation)

    def _check_parse_accounts(self, accounts):
        """
        Checks if accounts (or account) are derived from trapeza.account.base_account.BaseAccount and
        assigns them internally
        to self.accounts (or [account])

        :param accounts: list of FXAccount objects
        :return: None
        :raises: trapeza.exceptions.AccountError, if accounts not derived from trapeza.account.base_account.BaseAccount
        """
        try:
            for acc in accounts:
                if not issubclass(acc.__class__, BaseAccount):
                    raise tpz_exception.AccountError(acc, 'Account has to inherit from '
                                                          'trapeza.account.base_account.BaseAccount.')
            return accounts
        except TypeError:
            if not issubclass(accounts.__class__, BaseAccount):
                raise tpz_exception.AccountError(accounts, 'Account has to inherit from '
                                                           'trapeza.account.base_account.BaseAccount.')
            return [accounts]
        except tpz_exception.AccountError as e:
            # re-raise
            raise e

    def _init_all_positions(self, all_keys):
        """
        Initializes positions (self.depot_position and self.depot_composite_positions)

        :param all_keys: list of keys,
                         all keys (currency pairs) of data supplied to self.run()
        :return: None
        """
        self._c_init_accs_depots(list(all_keys))

    def _reset_storage(self):
        """
        Resets internal storage (before self.run() is called):
            self.signals, self.positions, self.merged_positions, self.total_balances
            and self.merged_total_balances and internal self._signals_at_step_t
        :return: None
        """
        self._c_reset_storage()

    def reset(self):
        """
        Resets internal storage of FXStrategy and storage of accounts. Restores account depot status to the same
        status as of time of calling FXStrategy.__init__(), keeps kwargs saved. Same applies to account.clock as they
        are restored to the same status as of the time of initialization of FXStrategy.
        Total reset as if FXStrategy was freshly initialized.
        Internal reset is done BEFORE each run, but not after!
        :return: None
        """
        self.c_reset()

    def _tick_method(self, dict data):
        """
        Default ticking method if self.suppress_ticking=False and None passed to self.tick_func at
        FXStrategy.__init__(). Implementation is based on FXAccount as well as patched version via
        trapeza.account.order_management.monkey_patch().

        :param data: dict with key:(base, quote) and value:current_exchange_rate or value:list of exchange_rates,
                     {(base, quote): current_rate,
                     (base, quote): current_rate,
                      ...}
                     or
                     {(base, quote): [rate_-2, rate_-1, current_rate],
                     (base, quote): [rate_-2, rate_-1, current_rate],
                      ...}
                     (dependent on size of parameter lookback)

                     if dict value: list of exchange_rates:
                        Only last value will be taken into account such that, if historic data has been prepended to
                        the data frame according to param:lookback, no changes to the data frame are needed; just pass
                        current data frame in without worrying about lookback.

                     if accounts are patched with trapeza.account.order_management:
                        if None, order management is not executed (orders may expire at next tick) but only
                        _exec_heap, which manages processing of delayed transaction (e.g. due to processing time
                        of broker). Keys of param:data, that are not listed within account._order_heap
                        (list of all open orders annotated with base|quote pair), are ignored.

                     Exchange rate is expressed in FX notation convention (direct notation, not volume notation)
                     1.2 EUR|USD --> 1.2 USD for 1 EUR
        :return: None
        """
        _c_tick_method(self, data)

    def evaluate(self, dict data_frame, str reference_currency, append_to_results):
        """
        Evaluates accounts regarding position sizes and total balances (expressed in reference currency), as well as
        all signals, which have been appended via FXStrategy.add_signal() method beforehand calling self.evaluate().

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        Ticking and adding signals have to be done before evaluation! Ticking is not included in evaluate!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        Cleans signals, which are temporarily appended via FXStrategy.add_signal for time step t, so be careful when
        manually calling this method (when append_to_results=True).
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        This method gets called at every iteration during looping through data supplied to FXStrategy.run().

        If append_to_results=True, results from evaluation of current time step t will be appended to internal storage
        of self.signals, self.depot_positions, self.depot_composite_positions, self.depot_total_balances
        and self.depot_composite_total_balances, which hold final results for subsequent analysis via backtesting
        engine. self._signals_at_step_t gets cleaned if append_to_results_True (which temporarily holds added signals).
        If append_to_results=False, results will not be appended and self.evaluate() will not have any internal
        effects (only returning raw evaluation of current time step t, does not clean anything).

        Recommendation: use FXStrategy.positions, FXStrategy.total_balances etc. instead of returned values from
                        FXStrategy.evaluate() in order to retrieve results.

        :param data_frame: dict with key:(base, quote) and value:exchange_rate or
                           value:[exchange_rate_-2, exchange_rate_-1, exchange_rate_0] depending
                           on value of self.lookback.
                           If called from self.run(), this is handled automatically.
                           If called manually, make sure data_frame is consistent in size (time steps) regarding
                           lookback + 1

                           e.g.:
                           dict with key:tuple(str, str) and value: float or value:list of floats or
                           value: array of floats,
                           {(base, quote): current_rate,
                            (base, quote): current_rate,
                             ...}
                           or
                           {(base, quote): [rate_-2, rate_-1, current_rate],
                            (base, quote): [rate_-2, rate_-1, current_rate],
                             ...}
                           --> dependent on size of parameter lookback (whether to prepend historic data to each call
                               to strategy decision function for each loop within FXStrategy.run())
        :param reference_currency: str,
                                   reference currency to bill total balances in
        :param append_to_results: bool,
                                  if True: appends results to self.signals, self.positions, self.merged_positions,
                                   self.total_balances and self.merged_total_balances such that backtesting engine can
                                   use results for subsequent analysis
                                  if False: does not append results to internal storage, self.evaluate() method does
                                  not take any effects on internal/ final results
        :return: signals: list of lists,
                          [[sig_acc_0, sig_acc_0, ...],
                           [sig_acc_1, sig_acc_1, ...], ...]
                          each list contains signals of each account at time step t
                 positions: list of dicts per account with key:str and value:amount
                            key: currency, value: exchange rate
                            [dict_acc_0, dict_acc_1, ...]
                            with dict_acc_x = {currency: amount, currency: amount, ...}
                            each dict contains all positions and corresponding volume per account
                            positions and corresponding amount/ volume per account at time step t
                 total_balances: list of floats,
                                 [tot_bal_acc_0, tot_bal_acc_1, ...]
                                 total balance of each account in param:reference_currency at time step t
        :raises: KeyError: if exchange_rates do not include all currencies listed in account depots or if reference
                           currency is not listed in data_frame
        """
        return self.c_wrap_evaluate(data_frame, reference_currency.encode(), append_to_results)

    def add_signal(self, acc, str signal):
        """
        Adds signal of specific account for current time step t, which is then automatically processed and appended to
        overall result when self.evaluate() is called with append_to_results=True.
        Handles format parsing of results automatically.
        Gets cleaned for next time step every time FXStrategy.evaluate() is called, which happens at every iteration
        through data supplied to FXStrategy.run() method.
        Just call add_signal within strategy_func every time a new signal is generated at specific time step t
        (be cautious when calling evaluate() method manually, as this cleans all current signals without evaluating/
        appending them to results!).

        If FXDashboard shall be used for visualization:
            if signal string contains currency (or whatever is defined by data dict, see FXStrategy.run()) as substring,
            signal will be appropriately visualized on the same line chart as currency. If signal string contains
            one of the keys of param:signal_symbols dict at FXDashboard.__init__ as substring, signal will be
            appropriately visualized with therein defined symbol shape and color.
            signal string therefore must not contain multiple currencies as substring, nor multiple keys of
            param:signal_symbols dict at FXDashboard.__init__, but only one currency and only one key of
            param:signal_symbols as substring.
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            !!! signal names, which are appended with FXStrategy.add_signal(), should not contain multiple substrings
                of either currencies (or assets or whatever defines keys of FXEngine.price_data dictionary) nor keys
                of shape defining dictionary (param:signal_symbols at FXDashboard.__init__) !!!
                Recommendation: signal names should be mutual free of substring parts to each other,
                otherwise they might be visualized multiple times at FXDashboard !!!
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        :param acc: FXAccount object (or other Account object inherited from BaseAccount) which to add signal for
        :param signal: str,
                       unique string describing trading signal, such as 'buy', 'sell', 'short', 'long'. Signals are
                       used for visualization in subsequent backtesting analysis.
        :return: None
        :raises: ValueError, if param:acc not in self.accounts
                 TypeError, if signal not str, only thrown if ignore_type_checking is False
                            (type_checking enabled at __init__)
        """
        check_types([signal], [str], ['signal'], self._c_ignore_type_checking)
        try:
            i = self.accounts.index(acc)
        except ValueError:
            i = self.accounts.index(acc[0])

        self.c_add_signal(i, signal.encode())

    def run(self, dict price_data, str reference_currency, volume_data=None):
        """
        Runs strategy_func with supplied data. Data is fed in via looping through every time step of data.
        At each loop, lookback defines number of previous time steps, which are prepended to current time step t and
        which are then fed into decision function (strategy decision function receives lookback + current time steps as
        data time frame of currency pairs (base|quote) and their exchange rate/ volumes at those time steps all at
        once).
        Historic data for using lookback parameter has to be prepended manually to data before passing to this method.
        Start time step is therefore at index=lookback with respect to data, which passed into this method.
        If 'lookback = length_of_data (all time steps) -1', then run is only called once internally (for loop reduced
        to one single iteration, which is useful if strategy decision function shall only be called once, e.g. when
        strategy decision function is heavily vectorized for performance reasons, even though ticking and adding
        signals have to be handled manually within strategy_func).
        If 'lookback = 0', only one (current) time step will be fed to strategy decision function at each loop
        (number of loops equals number of time steps contained in data). See param:price_data for data format and how
        time steps are arranged.

        Reference currency is used to calculate total balances of accounts after executing
        strategy_func.

        If ticking is not done within strategy decision function, then this method attempts to tick all accounts, as
        long as param:suppress_ticking at FXStrategy.__init__() is not set to True. If set to True, FXStrategy.run()
        will not attempt to tick accounts, but accounts can still be ticked from inside the strategy decision function.
        Raises exception, if ticking is not possible (detected via account.clocks) and suppress_ticking=False.

        At each call to run, FXStrategy internal storage (which hold final results) and accounts are reset.
        Additionally depots and clocks of accounts are reset to the same depot and clock status as when
        FXStrategy.__init__() was called.
        This means, FXStrategy.run() can be called repeatedly in such a way, that each call simulates an independent
        simulation run starting from the same account status as at time of FXStrategy.__init__() at every run. Calling
        FXStrategy.run() repeatedly is therefore safe and just simulates every time starting as if accounts have been
        freshly initialized with their initial account.depot and account.clock status as well as a fresh internal
        storage of FXStrategy.

        Additionally, volume data can be passed to strategy decision function. If volume data is None, then None value
        will be passed to strategy_func. If volume data is a dict in the same format as price data, then same logic as
        for price data is applied regarding lookback handling and iterating over volume data. Volume data is then
        iterated over for each time step with respective lookback portion. Volume data only has to comply to price
        data as it has to take the same data format. Keys of volume data can be chosen independently from price
        data (but have to be tuples of strings). No further checks (e.g. if ('BTC', 'EUR') key is inverse to
        ('EUR', 'BTC')) are applied to volume data.

        Results can be accessed via 'self.positions', 'self.merged_positions', 'self.total_balances',
        'self.merged_total_balances', 'self.signals'. See docstring class description for more information.

        Internal reset is done BEFORE each run, but not after!

        :param price_data: dict with:
                     keys: currency pair as tuple of strings: (currency_0, currency_1)
                     values: list of floats as exchange rates per time step t or array of floats

                     {(base, quote): [rate_0, rate_1, ..., rate_t],
                      (base, quote): [rate_0, rate_1, ..., rate_t],
                      ...}

                     All values (list or array of floats) of all keys (currency pairs) have to be of same length.

                     If historic data shall be used by strategy_func (cf. lookback), historic data has to be prepended
                     manually to param:data, e.g.:
                         lookback = 3

                         {(base, quote): [rate_-3, rate_-2, rate_-1, rate_0, rate_1, ... rate_t],
                          (base, quote): [rate_-3, rate_-2, rate_-1, rate_0, rate_1, ... rate_t],
                          ...}

                     Data will be looped through one by one (time frame specified by lookback and current time step t
                     [size: lookback + 1]). Start time step is at index=lookback.

                     Exchange rate is expressed in FX notation convention (direct notation, not volume notation)
                     1.2 EUR|USD --> 1.2 USD for 1 EUR

                     None values allowed (if handling via accounts during account.tick(data_point_t) is ensured.
                     data_point_t is a data dict only containing time steps which are fed to strategy decision function
                     at each loop).

                     if accounts are patched with trapeza.account.order_management:
                        if None value occurs, order management is not executed (orders may expire at next tick) but only
                        _exec_heap, which manages processing of delayed transaction (e.g. due to processing time
                        of broker). Keys of param:data, that are not listed within account._order_heap
                        (list of all open orders annotated with base|quote pair), are ignored.
        :param reference_currency: str,
                                   reference currency in which to bill total balances of all accounts
        :param volume_data: None or dict,
                            If None, then None value is also passed to strategy decision function.
                            If dict, then dict must be in the same format as param:price_data. Instead of price data,
                                place volume data (or whatever data shall be used within strategy decision function) as
                                values. Keys (tuple of strings, which annotate e.g. currencies) do not have to be
                                identical to keys of param:price_data. No cross volume checking applied, which means
                                that e.g. ('BTC', 'EUR') does not have to match up against ('EUR', 'BTC'). Data input
                                at one's own caution. Lookbacks are handled in the same manner as in param:price_data.
        :return: reference_currency: str,
                                     see param:reference_currency
                 self.signals: list of lists,
                               see Class Docstring
                 self.positions: dict,
                                 see Class Docstring
                 self.merged_positions: dict,
                                        see Class Docstring
                 self.total_balances: list of lists,
                                      see Class Docstring
                 self.merged_total_balances: list,
                                             see Class Docstring
        :raises: IndexError: if dict values (list or array of floats) of param:data do not have same length,
                             only thrown if ignore_type_checking is False (type_checking enabled at __init__)
                 ValueError: if length dict values (list or array of floats) is less than lookback + 1
                 TypeError: if types do not match up,
                            only thrown if ignore_type_checking is False (type_checking enabled at __init__)
                 trapeza.OperatingError: if accounts have not been ticked (when suppress ticking=True)

        # TODO: return special value if transactions have been ignored during run (e.g. coverage exception at account)
        """
        # data:
        # dict = {(base, quote): [val_0, val_1, ..., val_t], (base, quote): [val_0, val_1, ..., val_t]}

        len_data = len(price_data[list(price_data.keys())[0]])

        # >>>type checking
        if not self._c_ignore_type_checking:
            # >>price data
            check_types([price_data], [dict], ['price_data'], self._c_ignore_type_checking)
            for k in price_data.keys():
                check_types([k], [tuple], ['price_data_key'], self._c_ignore_type_checking)
                check_types([k[0], k[1]], [str, str], ['price_data_key_tuple_0', 'price_data_key_tuple_1'],
                            self._c_ignore_type_checking)
                # sample check
                check_types([price_data[k][0]], [float], ['price_data_value'], self._c_ignore_type_checking)
                if len(price_data[k]) != len_data:
                    raise IndexError('Not all time series of all tuple keys within supplied price data dict have the '
                                     'same length.')
            # >>volume data
            if volume_data is not None:
                check_types([volume_data], [dict], ['volume_data'], self._c_ignore_type_checking)
                for k in volume_data.keys():
                    check_types([k], [tuple], ['volume_data_key'], self._c_ignore_type_checking)
                    check_types([k[0], k[1]], [str, str], ['volume_data_key_tuple_0', 'volume_data_key_tuple_1'],
                                self._c_ignore_type_checking)
                    # sample check
                    check_types([volume_data[k][0]], [float], ['volume_data_value'], self._c_ignore_type_checking)
                    if len(volume_data[k]) != len_data:
                        raise IndexError

        if len_data <= self.lookback:
            raise ValueError('Data does not contain enough time steps: {}. '
                             'Data has to contain more time steps than '
                             'specified by lookback: {}.'.format(len_data, self.lookback))

        if volume_data is None:
            volume_data = {}

        return self.c_wrap_run(price_data, reference_currency.encode(), volume_data, len_data)
