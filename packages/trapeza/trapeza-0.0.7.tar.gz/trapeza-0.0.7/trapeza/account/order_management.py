import warnings
import inspect

from trapeza.account.base_account import BaseAccount
from trapeza.utils import check_types, precision_add, precision_divide, precision_subtract, precision_multiply
from trapeza import exception as tpz_exception


# TODO: Cythonizing this module would need to handle a lot of Python objects like list and dicts
#   even tough there might be a slight performance increase due to e.g. list.append actions, the effort currently
#   wouldn't worth it as there are enough other low hanging optimization fruits


def monkey_patch(account, only_basic=False):
    """
    Monkey patch account of BaseAccount or derived subclass with methods for implementing order management (additional
    data structure and methods), such as stop loss.
    Patched methods are then accessible by class instance directly, e.g. account.stop_loss().
    Be aware of possible side effects.
    Only patches single instance, not entire classes.
    Patches standard order types such as stop loss by default.
    Additionally custom methods can be patched onto account instance via patch() method.

    Overwrites tick() method of account instance of BaseAccount/ derived subclass in order to perform heap execution
    of transactions (implemented in BaseAccount/ derived subclass) as well as heap execution of order management
    (implemented via patch), and then ticks up account.clock.

    Be cautious when multi-processing, internal states might get messed up, as internal states/ attributes
    store temporarily values, which are then used across different methods across patched structures.

    Checks and prohibits attributes or methods getting over-patched.

    Attributes and methods introduced from monkey_patch additionally to account instance attributes:
       _order_heap, _is_order_manager_heap, _is_setup_order_called, _is_tear_down_order_called, _tick, __reset,
       _temp_kwargs_order, _internal_acc_methods, patch, _check_is_patchable, _exec_order_manager_heap, 
       _push_order_to_order_heap, _remove_order_from_order_heap, setup_order_method, tear_down_order_method, tick,
       _check_inverted_dict_current_data, _reset, _is_order_manager_monkey_patch
       if only_basic=False:
            stop_loss, trailing_stop_loss, start_buy, buy_limit, sell_limit todo extend

    If only_basic=True, then only basic functionality without any order types will be patched. Otherwise order types
    i.e. stop_loss, sell_limit, etc. will be patched. Patched account must be of type trapeza.account.FXAccount or must
    at least have the same call signatures to account methods such as account.sell(...) as class
    trapeza.account.FXAccount.

    Methods of account instance, which are used within custom implemented order functions (e.g. account.sell() for
    stop_loss() method) must return a confirmation value:
    1: success, 0: in processing/ delayed due to broker, -1: ignored/ unsuccessful.

    Order heap gets garbage cleaned automatically from expired orders.

    Functions can be patched by calling patch() function.

    Public functions:
        setup_order_method, tear_down_order_method, tick, patch,
        if only_basic=False:
            stop_loss, trailing_stop_loss, start_buy, buy_limit, sell_limit todo extend

    :param account: account instance of trapeza.account.BaseAccount or derived subclass
    :param only_basic: bool, default=False
                       if True, then only basic functionality but no order types will be patched
                       if False, then additional order types are patched
                            --> !!! order types assume trapeza.account.FXAccount or at least same call signatures !!!
    :return: None
    :raises: trapeza.exception.AccountError: if overriding existing attributes or methods of account instance, e.g.
                                           methods, which already were implemented in BaseAccount/ derived subclass, or
                                           was already patched
    :TODO: add more order types (as additional static methods + at self.patch within __init__), e.g.:
            buy/ sell limit, buy/ sell stop, trailing, IOC, FOK, stop limit and liquid volumes
    :TODO: theoretically self._is_setup_order_called and self._is_tear_down_order_called can be removed by implementing
           checking for 'setup_order_method' and 'tear_down_order_method' during execution of heap by checking if
           those two strings occur within func.__code__.co_names, but this would decrease performance for larger
           custom implemented functions as there might be quite a lot of functions names to search through
           and it might decrease readability
    :TODO: use function in place of param:volume to simulate imperfect market liquidity
    """
    # >>>check if argument is patchable
    if not issubclass(account.__class__, BaseAccount):
        raise tpz_exception.AccountError(account,
                                         'Account has to inherit from trapeza.account.base_account.BaseAccount')

    _check_is_patchable(account)

    # >>>monkey patch attributes
    # order heap: {(base, quote): [[func, kwargs], [func, kwargs], ...], (base, quote): [[func, kwargs]], ...}
    account._order_heap = dict()
    account._is_order_manager_heap = False  # set True if called from self._exec_heap(), else false
    account._is_setup_order_called = False  # checks if setup routine is implemented at patch
    account._is_tear_down_order_called = False  # checks if teardown routine is implemented at patch
    account._temp_kwargs_order = dict()  # stores kwargs during heap execution
    account._internal_acc_methods = list()  # stores names of account methods
    account._is_order_manager_monkey_patch = True  # attribute which can be checked from outside

    # >>>monkey patch tick method separately
    setattr(account, '_tick', account.tick.__get__(account))
    # noinspection PyArgumentList
    setattr(account, 'tick', tick.__get__(account))

    # >>>monkey patch _reset method separately
    # noinspection PyProtectedMember
    setattr(account, '__reset', account._reset.__get__(account))
    # noinspection PyArgumentList
    setattr(account, '_reset', _reset.__get__(account))

    # >>>monkey patch rest of methods
    patchable_methods = [_exec_order_manager_heap, patch, _remove_order_from_order_heap,
                         _push_order_to_order_heap, setup_order_method, tear_down_order_method,
                         _check_inverted_dict_current_data]
    if not only_basic:
        patchable_methods.extend([stop_loss, trailing_stop_loss, start_buy, buy_limit, sell_limit])  # todo extend
    patch(account, patchable_methods, safe_patch=True)

    # >>>set internal states
    account._is_setup_order_called = False
    account._is_tear_down_order_called = False


# noinspection PyProtectedMember
def _check_is_patchable(account):
    """
    Checks if object (account instance of BaseAccount or respective Subclass) is patchable or was already patched before
    Does not get patched onto account of BaseAccount or derived subclass.
    :param account: instance of trapeza.account.base_account.BaseAccount or derived subclass
    :return: None
    :raises: trapeza.exception.AccountError: if overriding existing attributes or methods of account instance, which
                                           indicates, that account instance was already patched before
    """
    if hasattr(account, '_order_heap'):
        raise tpz_exception.AccountError(account, 'Cannot patch "_order_heap" variable. '
                                                  'account might have already been patched.')
    if hasattr(account, '_is_order_manager_heap'):
        raise tpz_exception.AccountError(account, 'Cannot patch "_is_order_manager_heap" variable. '
                                                  'account might have already been patched.')
    if hasattr(account, '_is_setup_order_called'):
        raise tpz_exception.AccountError(account, 'Cannot patch "_is_setup_order_called" variable. '
                                                  'account might have already been patched.')
    if hasattr(account, '_is_tear_down_order_called'):
        raise tpz_exception.AccountError(account, 'Cannot patch "_is_tear_down_order_called" variable. '
                                                  'account might have already been patched.')
    if hasattr(account, '_temp_kwargs_order'):
        raise tpz_exception.AccountError(account, 'Cannot patch "_temp_kwargs_order" variable. '
                                                  'account might have already been patched.')
    if hasattr(account, '_internal_acc_methods'):
        raise tpz_exception.AccountError(account, 'Cannot patch "_internal_acc_methods" variable. '
                                                  'account might have already been patched.')
    if hasattr(account, '_tick'):
        raise tpz_exception.AccountError(account, 'Cannot patch "_tick" method. '
                                                  'account might have already been patched.')
    if hasattr(account, '__reset'):
        raise tpz_exception.AccountError(account, 'Cannot patch "__reset" method. '
                                                  'account might have already been patched.')


def _exec_order_manager_heap(self, dict_current_data):
    """
    Executes order manager heap. Heap is cleaned automatically from expired orders.
    Gets patched onto account of BaseAccount or derived subclass.
    :param dict_current_data: {(base, quote): current_rate, (base, quote): current_rate, ...}
                              base: str
                              quote: str
                              rate: float
    :return: None
    :raises: trapeza.exception.OperatingError: if setup and teardown functions not implemented in order function,
                                             which was patched onto account of BaseAccount or derived class
    """
    # >>>trigger heap execution
    self._is_order_manager_heap = True

    # >>>check if dict_current_data has inverted base|quote pairs
    dict_current_data = self._check_inverted_dict_current_data(dict_current_data)

    # >>>checks if setup and tear down have been called from patched functions
    #    First set variables to False. When heap executes the very order, those variables will be set to True.
    #    If this doesn't happen, setup and teardown were not implemented in order function, which will throw an
    #    error. If heap has executed successfully, then those variables will be set to False and the whole thing
    #    continues accordingly.

    # >>>check every key = base|quote pair in data, if order can be filled
    for key in dict_current_data.keys():
        # >>>loop through all orders of specific base|quote pair
        for i, heap_entry in enumerate(self._order_heap[key]):
            # >>>pre-reset states after each order
            self._is_tear_down_order_called = False
            self._is_setup_order_called = False

            # >>>check if order is not already expired and try to execute order if not expired
            if heap_entry[1]['_internal_order_lifetime'] >= self.clock:
                # >>prepare arguments such that they match up with call signature of order function
                # 'internal_order_lifetime' doesn't match call signature and is therefore passed by account attribute
                # to setup_order_method and tear_down_order_method
                self._temp_kwargs_order = heap_entry[1]
                # self._temp_kwargs_order['_internal_order_lifetime'] = heap_entry[1]['_internal_order_lifetime']
                # We have to remove key '_internal_order_lifetime' to match call signature. We open up a new dict
                # as we don't want to alter heap entries directly
                _exec_order_kwargs = {k: heap_entry[1][k] for k in heap_entry[1] if k != '_internal_order_lifetime'}
                # >>execute heap
                _ = getattr(self, heap_entry[0])(dict_current_data[key], **_exec_order_kwargs)
                # >>check if function has called setup and tear down, both must be True
                #   if transaction is confirmed, order is removed from heap by tear_down_order_method: so no need
                #   to remove order separately here
                if not self._is_tear_down_order_called or not self._is_setup_order_called:
                    # theoretically this part of the code is not reachable: if setup_order_method is missing, than
                    # KeyError is thrown by _push_order_to_order_heap and if tear_down_order_method is missing,
                    # than order does not get pushed onto heap and is never listed as an open order
                    raise tpz_exception.OperatingError('Setup and/ or teardown have not been called. Make sure patched'
                                                       'methods include those methods.')
            # >>>order is expired, so remove from heap
            else:
                self._remove_order_from_order_heap(heap_entry[0], **heap_entry[1])

    # >>>trigger normal execution and reset internal states
    self._is_order_manager_heap = False
    self._is_tear_down_order_called = False
    self._is_setup_order_called = False


# noinspection PyIncorrectDocstring
def _check_inverted_dict_current_data(self, dict_current_data):
    """
    Checks if an inverted base|quote pair is within dict_current_data regarding self._order_heap and inverts
    them. Removes all keys from dict_current_data, which are not in self._order_heap, and replaces all
    inverted base|quote pairs, including exchange rate.
    Gets patched onto account of BaseAccount or derived subclass.
    :param dict_current_data: {(base, quote): current_rate, (base, quote): current_rate, ...}
                              base: str
                              quote: str
                              rate: float
    :return: altered dict_current_data
    :raises: ValueError: if base|quote pair and swapped base|quote pair in dict_current_data, which do not match up
                         in terms of exchange rate and inverted exchange rate
    """
    # >>>check if base|quote pair of dict_current_data is in self._order_heap keys and if not, then check
    #    if it may be within self._order_heap keys but swapped. If last case holds true, we have to invert
    #    current rate given by dict_current_data
    # >>get those keys of dict_current_data, which are not in self._order_heap
    possibly_inverted_keys = set(dict_current_data.keys()).difference(set(self._order_heap.keys()))
    for inversion_candidate in possibly_inverted_keys:
        # check if inverted base|quote pair is in self._order_heap
        if (inversion_candidate[1], inversion_candidate[0]) in self._order_heap.keys():
            # invert current rate given by dict_current_data and assign to dict_current_data
            dict_current_data[inversion_candidate[1],
                              inversion_candidate[0]] = 1 / dict_current_data[inversion_candidate]
        # remove either inverted base|quote pair or unlisted base|quote pair
        dict_current_data.pop(inversion_candidate)

    # >>>Check if dict_current_data simultaneously holds base|quote pair and inverted counterpart. This is okay as long
    #    as rates are inverted and equal as well
    candidate_keys = [key for key in dict_current_data.keys() if (key[1], key[0]) in dict_current_data.keys()]
    congruent_keys = list()
    for c_k in candidate_keys:
        if (c_k[1], c_k[0]) not in congruent_keys:
            congruent_keys.append(c_k)
    for c_key in congruent_keys:
        if dict_current_data[c_key] != (1 / dict_current_data[(c_key[1], c_key[0])]):
            raise ValueError('{} and {} are listed in dict_current_data but do not match up in terms of inverted '
                             'rates ({} vs. {}).'.format(c_key, (c_key[1], c_key[0]), dict_current_data[c_key],
                                                         dict_current_data[c_key[1], c_key[0]]))

    return dict_current_data


def _push_order_to_order_heap(self, func_name, **kwargs):
    """
    Pushes order to heap
    Gets patched onto account of BaseAccount or derived subclass.
    :param func_name: str,
                      name of order function, which is patched onto account of BaseAccount/ derived subclass
    :param kwargs: keywords of func specified by func_name
    :return: None
    :raises: KeyError: if 'base' or 'quote' not in **kwargs as keys
    """
    # >>>get current orders of base quote pair, which is specified in **kwargs
    try:
        active_orders = self._order_heap[kwargs['base'], kwargs['quote']]
    except KeyError:
        active_orders = []
    active_orders.append([func_name, kwargs])
    try:
        self._order_heap[kwargs['base'], kwargs['quote']] = active_orders
    except KeyError:
        raise KeyError('Patched function must have "base" and "quote" as arguments.')


def _remove_order_from_order_heap(self, func_name, **kwargs):
    """
    Removes order from heap
    Gets patched onto account of BaseAccount or derived subclass.
    :param func_name: str,
                      name of order function, which is patched onto account BaseAccount/ derived subclass
    :param kwargs: keywords of func specified by func_name
    :return: None
    :raises: KeyError: if 'base' or 'quote' not in **kwargs as keys
    """
    active_orders = self._order_heap[kwargs['base'], kwargs['quote']]
    # We can delete all orders of the same kind at once, even though when two identical orders were placed.
    # This is because during the for loop within _exec_order_manager_heap, a copy of the current heap is made, such that
    # even when we delete all orders of the same kind in this function at once, the heap is not touched during
    # _exec_order_manager_heap, which ensures, that the second order of the same kind will be executed as well and
    # is not accidentally deleted within this function call (when deleting the first order of the same kind)
    active_orders = [order for order in active_orders if not (order[0] == func_name and order[1] == kwargs)]
    self._order_heap[kwargs['base'], kwargs['quote']] = active_orders


# noinspection PyIncorrectDocstring
def setup_order_method(self, func, order_lifespan_arg_name, **kwargs):
    """
    This function has to be called at the very start of every custom implemented order function, which shall be
    patched onto account of BaseAccount or derived subclass. Does basic setup routines of internal variables (especially
    expiry date of order).
    !!! Make sure that custom order function takes 'current rate' as argument right after 'self', e.g.
        custom_function(self, current_rate, ....) !!!
    Gets patched onto account of BaseAccount or derived subclass.
    :param func: function object,
                 order function passed as object/ callable, which is patched
                 onto account of BaseAccount/ derived subclass
    :param order_lifespan_arg: str,
                               denoting variable name of custom order function which represents order lifespan duration,
                               pass str of variable which ever variable (argument used in order function) represents the
                               lifetime duration of the corresponding order. Suppose one has two variables denoting some
                               duration, e.g. lifespan of the order and processing duration of transaction due to
                               processing time of the broker. To avoid confusion about those durations, one has to pass
                               the name of the variable, that denotes the lifespan of the order,
                               to param:order_lifespan_arg_name.
                               This way, both durations can be distinguished and be processed the right way. Only pass
                               the str name of the variable to param:order_lifespan_arg, not the actual value or
                               reference/ object/ variable.
    :param kwargs: all arguments of func as kwargs
                   arguments of func can be passed as "arg_1=arg_1, arg_2=arg_2, ..." as param:kwargs, except
                   current_rate (which is always first argument after self within func signature;
                   even though this is theoretically caught, it's better to be safe than sorry....)
                   if func has **kwargs then use "arg_1=arg_1, arg_2=arg_2, ..., **kwargs" as param:kwargs

                   example:
                        func(self, current_rate , base, quote, duration, **kwargs)
                        --> param:kwargs = "base=base, quote=quote, **kwargs"
                        --> setup_order_method(func, 'duration', base=base, quote=quote, **kwargs)

                    current_rate (which is always first argument after self within func signature) must be excluded
                    from param:kwargs (this exception is caught within setup_order_method() but not ensured to be
                    fail safe... better safe than sorry)

                    !!! variable, which is denoted by param:order_lifespan_arg_name has to be included
                        in param:kwargs !!!
    :return: is_expired: bool,
                         True if order is expired (not due to processing, but due to
                         date limit of order), else False
    :raises: TypeError: if parameters not of specified type
             ValueError: if lifetime is less than 0
             NameError: if param:order_lifespan_arg not in keys of param:**kwargs
                        or if **kwargs does not include all arguments of func
             trapeza.exception.OperatingError: if func.__name__ not in internal list of available methods of account
             KeyError: thrown by _push_order_to_order_heap if base and quote not in keys of param: **kwargs
    """
    # >>>check if func_name is in internal list of available methods of account
    if func.__name__ not in self._internal_acc_methods:
        raise tpz_exception.OperatingError('{} is not listed as method of account and may '
                                           'not be patched yet.'.format(func.__name__))
    # >>>check if current rate (which is always the first argument after self) is within list_arg_names and throw
    #    exception if so: todo this might have to be optimized performance-wise
    func_sign = str(inspect.signature(func)).replace('(', '').replace(')', '').split(', ')
    if func_sign[1] in kwargs.keys():
        kwargs.pop(func_sign[1])
    # >>>check if kwargs contains at least all arguments of custom implemented order function
    func_sign.pop(0)  # pop self
    func_sign.pop(0)  # pop current rate
    func_sign = [i.partition('=')[0] for i in func_sign]  # handle default arguments
    func_sign = [i for i in func_sign if i != '**kwargs']
    if len(set(func_sign).difference(set(kwargs.keys()))) > 0:
        raise NameError('param:**kwargs does not include all arguments of func. \nParams of function signature: {}.'
                        '\nParams of received kwargs: {}.'
                        '\nMissed param in kwargs: {}'.format(func_sign, kwargs.keys(),
                                                              set(func_sign).difference(set(kwargs.keys()))))
    # >>>set internal variable to True to confirm, that this function has bee called
    self._is_setup_order_called = True

    # >>>set internal variable to make sure it is overwritten by tear_down_order_method() function
    self._is_tear_down_order_called = False

    # >>>if function is called the first time, then we have to do some basic setups and prepare it to be executable
    #    from heap
    if not self._is_order_manager_heap:
        # >>do some basic checks which only have to be done once as they are not changed afterwards
        # >>type check
        check_types([func, order_lifespan_arg_name], [callable, str], ['func', 'order_lifespan_arg_name'],
                    self._ignore_type_checking)
        if order_lifespan_arg_name not in kwargs.keys():
            raise NameError('param:order_lifespan_arg not found in param:**kwargs at function setup_order_method().')
        if kwargs[order_lifespan_arg_name] < 0:
            raise ValueError('order_lifespan_arg must be grater 0.')
        # other variables are hard to check

        # if called from outside and not heap, then duration is the absolute time span in which the order is valid
        kwargs['_internal_order_lifetime'] = self.clock + kwargs[order_lifespan_arg_name]
    else:
        kwargs['_internal_order_lifetime'] = self._temp_kwargs_order['_internal_order_lifetime']

    # >>>check if order may already have been expired and store kwarg internally
    if kwargs['_internal_order_lifetime'] < self.clock:
        # expiry date lies within past date and is no more valid
        # this part of the code is theoretically unreachable as expired orders are deleted during heap execution but
        # better safe than sorry...
        self._remove_order_from_order_heap(func.__name__, **kwargs)
        _is_expired_temp_order = True
    else:
        _is_expired_temp_order = False

    # >>>store kwarg internally
    self._temp_kwargs_order = kwargs

    return _is_expired_temp_order


# noinspection PyIncorrectDocstring
def tear_down_order_method(self, func, confirmation):
    """
    This function has to be called at the very end of every custom implemented order function, which shall be
    patched onto account of BaseAccount or derived subclass. Does basic teardown routines of internal variables
    (especially cleaning heap).
    Gets patched onto account of BaseAccount or derived subclass.
    :param func: function object,
                 order function passed as object/ callable, which is patched
                 onto account of BaseAccount/ derived subclass
    :param confirmation: int, {-1, 0, 1}
                         transaction confirmation implemented in BaseAccount/ derived subclass, e.g. if sell() was
                         successful. See trapeza.account.fx_account.FXAccount for further information.
                         Every class to be patched has to implement this confirmation for every transaction type.
                         -1: ignored, not successful, not yet executed
                          0: delayed due to execution/ transaction time (e.g. processing time of broker) but in
                             transaction/ filling
                          1: successful (it is absolutely important, to stick to at least this convention)
    :return: confirmation: int,
                           just passes param:confirmation through
    :raises: TypeError: if parameters not of specified type
    """
    # >>>check types
    check_types([func, confirmation], [callable, int], ['func', 'confirmation'], self._ignore_type_checking)

    # >>>set internal state for heap execution
    self._is_tear_down_order_called = True

    # >>>if executed, either remove from heap if called from heap, or do nothing if called from outside as order
    #    does not need to be pushed to heap because execution already happened
    if confirmation == 1 and self._is_order_manager_heap:
        self._remove_order_from_order_heap(func.__name__, **self._temp_kwargs_order)
    # >>>if not executed, either push to heap if called from outside, or do nothing if called from heap
    #    because order is still on heap when not executed
    elif confirmation != 1 and not self._is_order_manager_heap:
        self._push_order_to_order_heap(func.__name__, **self._temp_kwargs_order)

    # >>>tidy up internal states
    self._temp_kwargs_order = dict()
    if not self._is_order_manager_heap:
        self._is_setup_order_called = False
        self._is_tear_down_order_called = False

    return confirmation


# noinspection PyIncorrectDocstring
def patch(self, list_funcs, safe_patch=True):
    """
    Patches methods on to account of BaseAccount or derived subclass.
    Patched methods are then directly accessible from patched instance (e.g. account.stop_loss()).
    Functions must follow the same structure as:

        def sample_patch_func(self, current_rate, *args, **kwargs):
            is_expired = self.setup_order_method(sample_patch_func, 'order_lifetime_name', ...)   # see docstring of
                                                                                                    setup_order_method()
            # order_lifetime is contained in *args, but it's string name has to be explicitly passed to
            # setup_order_method as well
            ... custom_code ...
            confirmation = self.transaction(*args, *kwargs)     # see docstring of monkey_patch(), method of account
            return self.tear_down_order_method(sample_patch_func, confirmation)

        make sure, that function calls self.tear_down_order_method(func, confirmation) before exit and
        self.setup_order_method at entry
        furthermore, function must have base and quote as arguments, see pre-implemented order types

    !!! do not change position of param:current_rate !!!

    Gets patched onto account of BaseAccount or derived subclass and is directly accessible from account.
    :param safe_patch: bool, default = True
                       If set to True, method checks if method, which shall be patched, already exists in account of
                       BaseAccount or derived subclass which is about to be patched and throws AccountError. If False,
                       over-patching is possible
    :param list_funcs: list of methods
                       method function must follow signature:
                            confirmation = method(self, current_rate, *args, **kwargs)
                       see docstring above
                       see self.stop_loss(self, current_rate, volume, stop_bid_price, base, quote, **kwargs)
    :return: None
    :raises: trapeza.exception.AccountError: if method name from list_func is already in use
             TypeError: if parameters not of specified type
    """
    # >>>checking
    check_types([list_funcs, safe_patch], [list, bool],
                ['list_funcs', 'safe_patch'], self._ignore_type_checking)
    for i in range(len(list_funcs)):
        check_types([list_funcs[i]], [callable],
                    ['element_of_list_func'], self._ignore_type_checking)

    for i in range(len(list_funcs)):
        if safe_patch:
            try:
                _ = getattr(self, list_funcs[i].__name__)
                raise tpz_exception.AccountError(self,
                                                 'Method/ variable "{}" is already defined and '
                                                 'can not be patched.'.format(list_funcs[i].__name__))
            except AttributeError:
                pass
        setattr(self, list_funcs[i].__name__, list_funcs[i].__get__(self))

    # >>>update list of internal methods
    self._internal_acc_methods = [fn for fn in dir(self) if callable(getattr(self, fn)) and not fn.startswith("__")]


# noinspection PyIncorrectDocstring
def tick(self, dict_current_data=None, *args_base_tick, **kwargs_base_tick):
    """
    Counts internal clock up by one time base unit if clock=None. Else internal clock is set to param:clock.
    Executes oder heap and exec_heap of account instance after new clock time is set.

    Overrides account.tick(), see monkey_patch() function.

    Heap is cleaned automatically from expired orders during heap execution.

    Gets patched onto account of BaseAccount or derived subclass.
    :param dict_current_data: {(base, quote): current_rate, (base, quote): current_rate, ...} or None, default=None
                              if None, order management is not executed (orders may expire at next tick) but only
                              _exec_heap, which manages processing of delayed transaction (e.g. due to processing time
                              of broker).
                              Keys of param:dict_current_data, that are not listed within self._order_heap
                              (list of all open orders annotated with base|quote pair), are ignored.
    :param args_base_tick: args
                           args supplied to original unpatched account.tick() (respective account._tick())
                           original unpatched account.tick() (which is re-patched as account._tick(), see docstring
                           of monkey_patch()) is called first before order management is executed. During call to
                           original unpatched account.tick()/ respective account._tick() *args_base_tick is passed
                           through and supplied to account._tick().
                           args_base_tick is dependent on concrete implementation of original unpatched account.tick()
    :param kwargs_base_tick: kwargs dict
                             kwargs dict supplied to original unpatched account.tick() (respective account._tick()),
                             e.g. clock=...
                             original unpatched account.tick() (which is re-patched as account._tick(), see docstring
                             of monkey_patch()) is called first before order management is executed. During call to
                             original unpatched account.tick()/ respective account._tick() **kwargs_base_tick is passed
                             through and supplied to account._tick().
                             kwargs_base_tick is dependent on concrete implementation of
                             original unpatched account.tick()
    :return: current (freshly set) clock time
    :raises: TypeError: if clock is not int or clock < 0, current exchange rate stored in dict_current_data
                        is not float/ int, key of dict_current_data is not string or dict_current_data is not dict
             KeyError: if keys of param:dict_current_data are not tuple of length two
    """
    # >>>tick account
    self._tick(*args_base_tick, **kwargs_base_tick)

    # >>>execute heap
    if dict_current_data is not None:
        # >>check types
        check_types([dict_current_data], [dict], ['dict_current_data'], self._ignore_type_checking)

        # current_data_copy = copy.deepcopy(dict_current_data)
        current_data_copy = {k: dict_current_data[k] for k in dict_current_data.keys()}

        # >>sample check dict_current_data
        key_0 = list(current_data_copy.keys())[0]
        if len(key_0) != 2:
            raise KeyError('Key for dict_current_data has to be a tuple of strings.')
        check_types([current_data_copy[key_0]], [float], ['value_dict_current_data'], self._ignore_type_checking)
        check_types([key_0[0], key_0[1]], [str, str], ['key_dict_current_data', 'key_dict_current_data'],
                    self._ignore_type_checking)
        # >>>execute order heap
        self._exec_order_manager_heap(current_data_copy)
    else:
        warnings.warn('tick() (patched) was called without param:dict_current_data. Orders are not checked or '
                      'executed for this time step.')

    return self.clock


def _reset(self):
    self.__reset()

    self._order_heap = dict()
    self._is_order_manager_heap = False  # set True if called from self._exec_heap(), else false
    self._is_setup_order_called = False  # checks if setup routine is implemented at patch
    self._is_tear_down_order_called = False  # checks if teardown routine is implemented at patch
    self._temp_kwargs_order = dict()  # stores kwargs during heap execution
    self._is_order_manager_monkey_patch = True  # attribute which can be checked from outside


# noinspection PyIncorrectDocstring
def stop_loss(self, current_bid_rate, volume, stop_bid_price, base, quote, order_lifetime_duration, **kwargs):
    """
    Assumes account is of type trapeza.account.FXAccount or at least same call signature to functions
    like account.sell().

    Places a normal stop_loss order. Sells base volume, when current rate falls below stop_bid_price.
    This protects a position from losses or at least limits losses, as position is sold at stop limit which prevents
    further downturn of position if prices keep declining.

    This is a very simplified order model and does not account for lack of liquidity or FOK/ IOC.

    This implementation is more like a sell stop order.

    :param current_bid_rate: float,
                         e.g. current exchange rate of base|quote pair. Use FX notation of base|quote pair as rate
                         independent if its a sell or buy order
    :param volume: float,
                   volume in BASE currency
    :param stop_bid_price: float,
                           stop limit when to sell
    :param base: str,
                 currency
    :param quote: str,
                  currency
    :param order_lifetime_duration: int,
                                    how long order shall be active in time steps before expiration
    :param kwargs: dict
                   passed to kwargs of account.sell() besides volume, current_rate, base, quote
    :return: confirmation: int,
                           -1: sell transaction ignored/ not filled/ not yed executed,
                           0: sell transaction delayed due to processing time, e.g. at broker, but successfully placed,
                           1: sell transaction filled
    :raises: TypeError: if parameters not of specified type thrown by setup_order_method() function
             trapeza.exception.OperatingError: if exception occurs during calling account.sell(), e.g. incorrectly
                                             specified arguments for account.sell()

    :TODO: integrate liquid volume and FOK vs. IOC into user code logic (either distinct arguments or use **kwargs)
    :TODO:  currently this order is more like a sell stop order
    """
    # >>>get expiry date and do basic setup
    _ = self.setup_order_method(stop_loss, 'order_lifetime_duration', volume=volume, stop_bid_price=stop_bid_price,
                                base=base, quote=quote, order_lifetime_duration=order_lifetime_duration,
                                **kwargs)

    # #########################
    # # # start user code # # #
    # #########################
    try:  # try except is just an extra bonus and not a must have for custom implementation
        # >>>execute sell order if price drops below (or equal) stop price
        if current_bid_rate <= stop_bid_price:
            confirmation = self.sell(volume, current_bid_rate, base, quote, **kwargs)
        else:
            confirmation = 0
    except Exception as e:
        raise tpz_exception.OperatingError(e)
    # ########################
    # # # end user code # # #
    # ########################

    # >>>handle heap depending on execution status and return confirmation status
    return self.tear_down_order_method(stop_loss, confirmation)


# noinspection PyIncorrectDocstring
def trailing_stop_loss(self, current_bid_rate, volume, trailing_stop_bid_price, base, quote,
                       order_lifetime_duration, percent=True, **kwargs):
    """
    Assumes account is of type trapeza.account.FXAccount or at least same call signature to functions
    like account.sell().

    Places a trailing stop_loss order. Sells base volume, when current rate falls below trailing_stop_bid_price.
    Trigger stop limit is adjusted such that the percent distance or absolute distance (depending on param:percent)
    between current_bid_rate and initial trailing_stop_bid_price remains the same whenever current_bid_rate raises.
    This protects the position by limiting losses while simultaneously gives the possibility of letting profits move
    according to rising rates. Trigger stop does not move when rates decrease
    This protects a position from losses or at least limits losses, as position is sold at stop limit which prevents
    further downturn of position if prices keep declining.

    This is a very simplified order model and does not account for lack of liquidity or FOK/ IOC.

    This implementation is more like a sell stop order with trailing limits.

    :param current_bid_rate: float,
                         e.g. current exchange rate of base|quote pair. Use FX notation of base|quote pair as rate
                         independent if its a sell or buy order
    :param volume: float,
                   volume in BASE currency
    :param trailing_stop_bid_price: float,
                               stop limit when to sell, will be adjusted if rates increase such that percent distance or
                               absolute distance keeps the same depending on param:percent
    :param base: str,
                 currency
    :param quote: str,
                  currency
    :param order_lifetime_duration: int,
                                    how long order shall be active in time steps before expiration
    :param percent: bool, default=True
                    if True, trigger stop limit will be adjusted, such that percent distance will be adjusted upwards,
                    else absolute distance will be adjusted upwards
    :param kwargs: dict,
                   passed to kwargs of account.sell() besides volume, current_rate, base, quote
    :return: confirmation: int,
                           -1: sell transaction ignored/ not filled/ not yed executed,
                           0: sell transaction delayed due to processing time, e.g. at broker, but successfully placed,
                           1: sell transaction filled
    :raises: TypeError: if parameters not of specified type thrown by setup_order_method() function
             trapeza.exception.OperatingError: if exception occurs during calling account.sell(), e.g. incorrectly
                                             specified arguments for account.sell()

    :TODO: integrate liquid volume and FOK vs. IOC into user code logic (either distinct arguments or use **kwargs)
    :TODO:  currently this order is more like a sell stop order with trailing limit
    """
    # >>>if called from heap (order execution) get old order data, delete old order and re-push new order
    if self._is_order_manager_heap:
        old_rate = self._temp_kwargs_order['old_bid_rate']
        # >>>delete old order
        self._remove_order_from_order_heap('trailing_stop_loss', **self._temp_kwargs_order)
        # >>>re-calculate trailing stop
        dist_percentage = precision_divide(current_bid_rate, old_rate)
        # >>>if new trailing stop, then re-set internal kwargs of order heap
        if dist_percentage > 1:
            if percent:
                trailing_stop_bid_price = precision_multiply(dist_percentage, trailing_stop_bid_price)
            else:
                trailing_stop_bid_price = precision_add(trailing_stop_bid_price,
                                                        precision_subtract(current_bid_rate, old_rate))
            # >>>set new order data
            self._temp_kwargs_order['trailing_stop_bid_price'] = trailing_stop_bid_price
            # >>>update new rate
            self._temp_kwargs_order['old_bid_rate'] = current_bid_rate
            bid_rate = current_bid_rate
        else:
            bid_rate = old_rate

        # >>>push new order to heap
        self._push_order_to_order_heap('trailing_stop_loss', **self._temp_kwargs_order)
        # >>>remove old_bid_rate from kwargs so that it gets overwritten with current_bid_rate during call of setup
        kwargs = {k: kwargs[k] for k in kwargs.keys() if k != 'old_bid_rate'}
    else:
        bid_rate = current_bid_rate

    # >>>basic setup
    self.setup_order_method(trailing_stop_loss, 'order_lifetime_duration', volume=volume,
                            trailing_stop_bid_price=trailing_stop_bid_price, base=base, quote=quote,
                            order_lifetime_duration=order_lifetime_duration,
                            old_bid_rate=bid_rate, percent=percent, **kwargs)

    # >>>cleanse kwargs
    kwargs = {k: kwargs[k] for k in kwargs.keys() if k != 'old_aks_rate'}

    try:  # try except is just an extra bonus and not a must have for custom implementation
        # >>>execute sell order if price drops below (or equal) stop price
        if current_bid_rate <= trailing_stop_bid_price:
            confirmation = self.sell(volume, current_bid_rate, base, quote, **kwargs)
        else:
            confirmation = 0
    except Exception as e:
        raise tpz_exception.OperatingError(e)

    # >>>handle heap depending on execution status and return confirmation status
    return self.tear_down_order_method(trailing_stop_loss, confirmation)


# noinspection PyIncorrectDocstring
def start_buy(self, current_ask_rate, volume, start_ask_price, base, quote, order_lifetime_duration, **kwargs):
    """
    Assumes account is of type trapeza.account.FXAccount or at least same call signature to functions
    like account.sell().

    Places a normal start_buy order. Buys base volume, when current rate raises above start_ask_price.
    This order type is used to buy a position as soon as the course exceeds a certain limit, which might indicate a
    sustainable recovery point and is used e.g. to take advantage of sustainable trends.

    This is a very simplified order model and does not account for lack of liquidity or FOK/ IOC.

    :param current_ask_rate: float,
                         e.g. current exchange rate of base|quote pair. Use FX notation of base|quote pair as rate
                         independent if its a sell or buy order
    :param volume: float,
                   volume in BASE currency
    :param start_ask_price: float,
                            start limit to buy
    :param base: str,
                 currency
    :param quote: str,
                  currency
    :param order_lifetime_duration: int,
                                    how long order shall be active in time steps before expiration
    :param kwargs: dict
                   passed to kwargs of account.buy() besides volume, current_rate, base, quote
    :return: confirmation: int,
                           -1: buy transaction ignored/ not filled/ not yed executed,
                           0: buy transaction delayed due to processing time, e.g. at broker, but successfully placed,
                           1: buy transaction filled
    :raises: TypeError: if parameters not of specified type thrown by setup_order_method() function
             trapeza.exception.OperatingError: if exception occurs during calling account.buy(), e.g. incorrectly
                                               specified arguments for account.buy()
    """
    # >>>get expiry date and do basic setup
    _ = self.setup_order_method(start_buy, 'order_lifetime_duration', volume=volume, start_ask_price=start_ask_price,
                                base=base, quote=quote, order_lifetime_duration=order_lifetime_duration,
                                **kwargs)

    # #########################
    # # # start user code # # #
    # #########################
    try:  # try except is just an extra bonus and not a must have for custom implementation
        # >>>execute sell order if price drops below (or equal) stop price
        if current_ask_rate >= start_ask_price:
            confirmation = self.buy(volume, current_ask_rate, base, quote, **kwargs)
        else:
            confirmation = 0
    except Exception as e:
        raise tpz_exception.OperatingError(e)
    # ########################
    # # # end user code # # #
    # ########################

    # >>>handle heap depending on execution status and return confirmation status
    return self.tear_down_order_method(start_buy, confirmation)


# noinspection PyIncorrectDocstring
def buy_limit(self, current_ask_rate, volume, limit_ask_price, base, quote, order_lifetime_duration, **kwargs):
    """
    Assumes account is of type trapeza.account.FXAccount or at least same call signature to functions
    like account.sell().

    Places a normal buy limit order. Buys base volume, when current rate falls below or equal to limit_ask_price.
    This ensures, that the buy transaction is fulfilled at or below limit price, which means, that we do not
    buy at a price worse/ higher than limit price as we aim to buy a lowest possible price in general.

    This is a very simplified order model and does not account for lack of liquidity or FOK/ IOC.

    :param current_ask_rate: float,
                         e.g. current exchange rate of base|quote pair. Use FX notation of base|quote pair as rate
                         independent if its a sell or buy order
    :param volume: float,
                   volume in BASE currency
    :param limit_ask_price: float,
                            when to buy, current rate has to be equal or fall bellow limit_ask_price in order to
                            place buy order
    :param base: str,
                 currency
    :param quote: str,
                  currency
    :param order_lifetime_duration: int,
                                    how long order shall be active in time steps before expiration
    :param kwargs: dict
    :return: confirmation: int,
                           -1: transaction ignored/ not filled, 0: transaction delayed due to processing
                           time, e.g. at broker, but successfully placed, 1:  transaction filled
    :raises: TypeError: if parameters not of specified type thrown by setup_order_method() function
             trapeza.exception.OperatingError: if exception occurs during calling account.buy(), e.g. incorrectly
                                             specified arguments for account.buy()

    :TODO: integrate liquid volume and FOK vs. IOC into user code logic (either distinct arguments or use **kwargs)
    """
    # >>>get expiry date and do basic setup
    _ = self.setup_order_method(buy_limit, 'order_lifetime_duration', volume=volume, limit_ask_price=limit_ask_price,
                                base=base, quote=quote, order_lifetime_duration=order_lifetime_duration,
                                **kwargs)

    # #########################
    # # # start user code # # #
    # #########################
    try:  # try except is just an extra bonus and not a must have for custom implementation
        # >>>execute buy order if price is above (or equal) stop price
        if current_ask_rate <= limit_ask_price:
            confirmation = self.buy(volume, current_ask_rate, base, quote, **kwargs)
        else:
            confirmation = 0
    except Exception as e:
        raise tpz_exception.OperatingError(e)
    # ########################
    # # # end user code # # #
    # ########################

    # >>>handle heap depending on execution status and return confirmation status
    return self.tear_down_order_method(buy_limit, confirmation)


# noinspection PyIncorrectDocstring
def sell_limit(self, current_bid_rate, volume, limit_bid_price, base, quote, order_lifetime_duration, **kwargs):
    """
    Assumes account is of type trapeza.account.FXAccount or at least same call signature to functions
    like account.sell().

    Places a normal sell limit order. Sells base volume, when current rate is above or equal limit_bid_price.
    This ensures, that we sell to price which is above or equal limit price and guarantees, that our sell transaction
    is not worse than expected by limit price, as our aim is to sell to the highest possible price. Therefore at
    least prices as high as limit price are guaranteed to guarantee respective minimal revenues.

    This is a very simplified order model and does not account for lack of liquidity or FOK/ IOC.

    :param current_bid_rate: float,
                         e.g. current exchange rate of base|quote pair. Use FX notation of base|quote pair as rate
                         independent if its a sell or buy order
    :param volume: float,
                   volume in BASE currency
    :param limit_bid_price: float,
                            when to buy, current rate has to be equal or fall bellow limit_ask_price in order to
                            place buy order
    :param base: str,
                 currency
    :param quote: str,
                  currency
    :param order_lifetime_duration: int,
                                    how long order shall be active in time steps before expiration
    :param kwargs: dict
    :return: confirmation: int,
                           -1: transaction ignored/ not filled, 0: transaction delayed due to processing
                           time, e.g. at broker, but successfully placed, 1:  transaction filled
    :raises: TypeError: if parameters not of specified type thrown by setup_order_method() function
             trapeza.exception.OperatingError: if exception occurs during calling account.buy(), e.g. incorrectly
                                             specified arguments for account.buy()

    :TODO: integrate liquid volume and FOK vs. IOC into user code logic (either distinct arguments or use **kwargs)
    """
    # >>>get expiry date and do basic setup
    _ = self.setup_order_method(sell_limit, 'order_lifetime_duration', volume=volume, limit_bid_price=limit_bid_price,
                                base=base, quote=quote, order_lifetime_duration=order_lifetime_duration,
                                **kwargs)

    # #########################
    # # # start user code # # #
    # #########################
    try:  # try except is just an extra bonus and not a must have for custom implementation
        # >>>execute buy order if price is above (or equal) stop price
        if current_bid_rate >= limit_bid_price:
            confirmation = self.sell(volume, current_bid_rate, base, quote, **kwargs)
        else:
            confirmation = 0
    except Exception as e:
        raise tpz_exception.OperatingError(e)
    # ########################
    # # # end user code # # #
    # ########################

    # >>>handle heap depending on execution status and return confirmation status
    return self.tear_down_order_method(sell_limit, confirmation)
