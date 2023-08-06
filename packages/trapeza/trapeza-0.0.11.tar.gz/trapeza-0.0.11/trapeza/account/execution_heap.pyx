# noinspection PyUnresolvedReferences
from trapeza.account.execution_heap cimport fx_heap_element_struct, vector, bool_t, string, currency_pair_struct
from trapeza.arithmetics.arithmetics cimport c_precision_add


cdef inline bool_t fx_heap_comparator (const fx_heap_element_struct &u, const fx_heap_element_struct &v):
    return u.time > v.time


# noinspection PyPep8Naming,PyUnresolvedReferences
cdef class cFXWrapperVectorHeap:
    """
    This is a C++ implementation via cython for a heapyfied list used in cFXAccount class.
    """
    # noinspection PyTypeChecker
    def __init__(self, list exec_heap):
        """
        Turns a list of lists into vector of structs.
        See trapeza.account.FXAccount for further details regarding param:exec_heap.
        :param exec_heap: list of lists: [time, action_func, volume, currency, coverage]
                          time: int, in clock cycles/ time base units (starting from 0)
                          action_func: {'c_withdraw', 'c_deposit'} (or {'withdraw', 'deposit'}: gets parsed to
                                        'c_withdraw' and 'c_deposit')
                          volume: float
                          currency: str
                          coverage: str (see docstring FXAccount.deposit() or .withdraw().
        """
        cdef fx_heap_element_struct struct_element

        self.std_cover_at_exec_exception = 'except'.encode()

        for process in exec_heap:
            struct_element = self.encode_tostruct(process)

            self.vector_heap.push_back(struct_element)

        make_heap(self.vector_heap.begin(), self.vector_heap.end(), &fx_heap_comparator)

    cdef long size(self):
        """
        Returns length of heap.
        :return: long
        """
        return self.vector_heap.size()

    cpdef double cum_sum_heap(self, string currency, string action_func_type, long time_step, long current_clock):
        """
        Calculates cumulative sum over heap for given currency, action_func_type, between current_clock and time_step.
        :param currency: std:string
        :param action_func_type: std:string, {b'c_withdraw', b'c_deposit'}
        :param time_step: long
        :param current_clock: long
        :return: double
        """
        if self.vector_heap.size() == 0:
            return 0

        cdef double cum_sum = 0
        cdef long i
        cdef vector[fx_heap_element_struct] copy_heap

        copy_heap.reserve(self.vector_heap.size())
        copy_heap = self.vector_heap
        sort_heap(copy_heap.begin(), copy_heap.end(), &fx_heap_comparator)

        i = copy_heap.size() - 1
        while i >= 0:
            process = copy_heap[i]

            if (current_clock <= process.time <= time_step and process.action_func == action_func_type
                    and process.currency == currency):
                cum_sum = c_precision_add(cum_sum, process.volume)
            elif process.time > time_step:
                break

            i -= 1

        return cum_sum

    # noinspection PyTypeChecker
    cpdef double cum_sum_marked_fund(self, string currency, long time_step, long current_clock):
        """
        Returns cumulative sum of depositing transaction, which are on heap. See self.cum_sum_heap for further 
        information.
        :param currency: std:string
        :param time_step: long
        :param current_clock: long
        :return: double
        """
        return self.cum_sum_heap(currency, b'c_deposit', time_step, current_clock)

    # noinspection PyTypeChecker
    cpdef double cum_sum_marked_debit(self, string currency, long time_step, long current_clock):
        """
        Returns cumulative sum of withdrawal transaction, which are on heap. See self.cum_sum_heap for further 
        information.
        :param currency: std:string
        :param time_step: long
        :param current_clock: long
        :return: double
        """
        return self.cum_sum_heap(currency, b'c_withdraw', time_step, current_clock)

    cdef fx_heap_element_struct heappop(self):
        """
        Pops smallest element from vector. Smallest element is defined by struct.time.
        :return: fx_heap_element_struct struct
        """
        cdef fx_heap_element_struct struct_element

        if self.vector_heap.size() <= 0:
            raise IndexError('Cannot heappop from empty heap.')

        pop_heap(self.vector_heap.begin(), self.vector_heap.end(), &fx_heap_comparator)
        # noinspection PyAttributeOutsideInit
        struct_element = self.vector_heap.back()
        self.vector_heap.pop_back()

        return struct_element

    cpdef fx_heap_element_struct encode_tostruct(self, list element):
        """
        Encodes sub-list of exec_heap to fx_heap_element_struct struct.
        :param element: list: [time, action_func, volume, currency, coverage]
                          time: int, in clock cycles/ time base units (starting from 0)
                          action_func: py_str, {'c_withdraw', 'c_deposit'}
                          volume: float
                          currency: py_str
                          coverage: py_str (see docstring FXAccount.deposit() or .withdraw().
        :return: fx_heap_element_struct struct
        """
        cdef fx_heap_element_struct struct_element

        struct_element.time = element[0]
        struct_element.action_func = element[1].encode()
        struct_element.volume = element[2]
        struct_element.currency = element[3].encode()
        if len(element) == 4:
            struct_element.coverage = self.std_cover_at_exec_exception
        else:
            struct_element.coverage = element[4].encode()

        return struct_element

    cpdef fx_heap_element_struct tostruct(self, list element):
        """
        Turns list of exec_heap to fx_heap_element_struct struct without calling encode() on string (e.g. strings
        are already encoded).
        :param element: list: [time, action_func, volume, currency, coverage]
                          time: int, in clock cycles/ time base units (starting from 0)
                          action_func: std:string, {b'c_withdraw', b'c_deposit'}
                          volume: float
                          currency: std:string
                          coverage: std:string (see docstring FXAccount.deposit() or .withdraw().
        :return: fx_heap_element_struct struct
        """
        cdef fx_heap_element_struct struct_element

        struct_element.time = element[0]
        struct_element.action_func = element[1]
        struct_element.volume = element[2]
        struct_element.currency = element[3]
        if len(element) == 4:
            struct_element.coverage = self.std_cover_at_exec_exception
        else:
            struct_element.coverage = element[4]

        return struct_element

    cdef void heappush_struct(self, fx_heap_element_struct element):
        """
        Pushes fx_heap_element_struct struct onto heap
        :param element: fx_heap_element_struct
        :return: None
        """
        self.vector_heap.push_back(element)
        push_heap(self.vector_heap.begin(), self.vector_heap.end(), &fx_heap_comparator)

    cdef void heappush(self, list element):
        """
        Pushes list element onto heap.
        :param element: list: [time, action_func, volume, currency, coverage]
                          time: int, in clock cycles/ time base units (starting from 0)
                          action_func: py_str, {'c_withdraw', 'c_deposit'}
                          volume: float
                          currency: py_str
                          coverage: py_str (see docstring FXAccount.deposit() or .withdraw().
        :return: None
        """
        cdef fx_heap_element_struct struct_element

        struct_element = self.tostruct(element)
        self.heappush_struct(struct_element)

    cpdef list tolist(self):
        """
        Converts vector of structs to list of lists
        :return: list of lists
        """
        cdef list exec_heap = []
        cdef long i

        sort_heap(self.vector_heap.begin(), self.vector_heap.end(), &fx_heap_comparator)

        i = self.vector_heap.size() - 1
        # for i in range(self.vector_heap.size()):
        while i >= 0:
            element = self.vector_heap[i]
            exec_heap.append([element.time, element.action_func.decode(), element.volume, element.currency.decode(),
                              element.coverage.decode()])
            i -= 1

        make_heap(self.vector_heap.begin(), self.vector_heap.end(), &fx_heap_comparator)

        return exec_heap

    cdef long max_time_step(self) except? -9223372036854775807:
        """
        Returns max time step, which is currently located on heap.
        :return: long
        """
        if self.vector_heap.size() == 1:
            return self.vector_heap[0].time
        elif self.vector_heap.size() == 0:
            raise IndexError('Empty heap has no maximum element.')

        cdef int max_element = self.vector_heap[<long>(self.vector_heap.size() / 2)].time
        cdef int i

        for i in range(<long>(1 + self.vector_heap.size() / 2), self.vector_heap.size()):
            max_element = max(max_element, self.vector_heap[i].time)

        return max_element

    cpdef long py_max_time_step(self) except? -9223372036854775807:
        """Python wrapper"""
        return self.max_time_step()


cdef class DictKeysToVec:
    """
    Turns keys of python dictionary to a vector structs (which emulates a tuple pair).
    C++ implementation via cython.
    """
    # noinspection PyUnresolvedReferences
    def __init__(self, dict tuple_dict):
        """
        Turns keys into vector of structs
        :param tuple_dict: dict, with tuple pairs as keys and floats as values
        """
        cdef tuple key
        cdef double current_rate
        cdef currency_pair_struct currency_pair

        self.currency_pairs.reserve(len(tuple_dict))

        for key, current_rate in tuple_dict.items():
            currency_pair.currency_a = key[0]
            currency_pair.currency_b = key[1]
            currency_pair.rate = current_rate
            self.currency_pairs.push_back(currency_pair)

    # noinspection PyUnresolvedReferences,PyTypeChecker
    cdef (bool_t, bool_t, double, double) is_tuple_key_in_tuple_vec(self, string key_a, string key_b):
        """
        Checks if tuple of keys is in vector of structs (which is built from dict).
        :param key_a: std:string
        :param key_b: std:string
        :return: (is_key, is_inv_key, key_rate, inv_key_rate)
                 is_key: std:bool, whether (key_a, key_b) is in vector (respective in dict)
                 is_inv_key: std:bool, whether (key_b, key_a) is in vector (respective in dict)
                 key_rate: float value (exchange_rate) of vector/dict for (key_a, key_b)
                 inv_key_rate: float value (exchange_rate) of vector/dict for (key_b, key_a)
        """
        cdef currency_pair_struct element
        cdef bool_t is_key = False
        cdef bool_t is_inv_key = False
        cdef double key_rate
        cdef double inv_key_rate

        for element in self.currency_pairs:
            if key_a == element.currency_a:
                if key_b == element.currency_b:
                    is_key = True
                    key_rate = element.rate
            elif key_a == element.currency_b:
                if key_b == element.currency_a:
                    is_inv_key = True
                    inv_key_rate =element.rate
            if is_key and is_inv_key:
                break

        return is_key, is_inv_key, key_rate, inv_key_rate
