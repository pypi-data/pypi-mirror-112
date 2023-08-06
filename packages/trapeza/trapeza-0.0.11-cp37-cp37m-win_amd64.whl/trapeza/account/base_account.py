from abc import ABCMeta, abstractmethod


class BaseAccount(metaclass=ABCMeta):
    """
    Base class for accounts. Provides a basic interface such that transactions between accounts are compatible.

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    Return of confirmation state must be implemented for all methods which shall be used for order management -
    such as buy and sell limits -  if class is going to be patched by trapeza.account.order_management.monkey_patch()
    (esp. such as sell() or buy())
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    """
    @property
    @abstractmethod
    def clock(self):
        """
        Class attribute that holds current clock time in time base units and is used for self.tick(). See self.tick()
        """

    @abstractmethod
    def sell(self, volume, price, from_unit, to_unit):
        """
        Implement selling transaction

        !!! Return of confirmation state must be implemented if class shall be patched
            by trapeza.account.order_management.monkey_patch() !!!

        :param volume: float in from_unit
        :param price: float
        :param from_unit: str
        :param to_unit: str
        :return: int
                 confirmation states --> -1: ignored, 0: processing (processing_duration), 1: executed
                 at least state 0 and 1 have to implemented
        """

    @abstractmethod
    def buy(self, volume, price, to_unit, from_unit):
        """
        Implement buying transaction. Compare swapped order of parameters compared to sell() !!! (e.g. when trading
        currencies)

        !!! Return of confirmation state must be implemented if class shall be patched
            by trapeza.account.order_management.monkey_patch() !!!

        :param volume: float in from_unit
        :param price: float
        :param from_unit: str
        :param to_unit: str
        :return: int
                 confirmation states --> -1: ignored, 0: processing (processing_duration), 1: executed
                 at least state 0 and 1 have to implemented
        """

    @abstractmethod
    def transfer(self, payee_account, volume, unit):
        """
        Implement transfer transaction from one account to other account.

        !!! Return of confirmation state must be implemented if class shall be patched
            by trapeza.account.order_management.monkey_patch() !!!

        :param payee_account: derived from trapeza.account.base_account_BaseAccount class
        :param volume: float
        :param unit: str
        :return: int
                 confirmation states --> -1: ignored, 0: processing (processing_duration), 1: executed
                 at least state 0 and 1 have to implemented
        """

    @abstractmethod
    def collect(self, payer_account, volume, unit):
        """
        Implement collect transaction from one account to other account.

        !!! Return of confirmation state must be implemented if class shall be patched
            by trapeza.account.order_management.monkey_patch() !!!

        :param payer_account: derived from trapeza.account.base_account_BaseAccount class
        :param volume: float
        :param unit: str
        :return: int
                 confirmation states --> -1: ignored, 0: processing (processing_duration), 1: executed
                 at least state 0 and 1 have to implemented
        """

    @abstractmethod
    def deposit(self, volume, unit):
        """
        Implement deposit transaction to deposit account funding.

        !!! Return of confirmation state must be implemented if class shall be patched
            by trapeza.account.order_management.monkey_patch() !!!

        :param volume: float
        :param unit: str
        :return: int
                 confirmation states --> -1: ignored, 0: processing (processing_duration), 1: executed
                 at least state 0 and 1 have to implemented
        """

    @abstractmethod
    def withdraw(self, volume, unit):
        """
        Implement withdraw transaction to withdraw debit volume from account.

        !!! Return of confirmation state must be implemented if class shall be patched
            by trapeza.account.order_management.monkey_patch() !!!

        :param volume: float
        :param unit: str
        :return: int
                 confirmation states --> -1: ignored, 0: processing (processing_duration), 1: executed
                 at least state 0 and 1 have to implemented
        """

    @abstractmethod
    def tick(self):
        """
        If internal time-state machine is implemented, then this methods increases time by one base unit and
        initiates triggering time-dependent events and states. This function is repeatedly called during evaluation
        in backtesting at each time step (number of data points supplied to backtesting).
        """

    @abstractmethod
    def total_balance(self):
        """
        Calculates total balance of account.
        :return: float
        """

    @abstractmethod
    def position(self, unit):
        """
        Returns current value of position regarding volume of param:unit.
        :param unit: str
        """

    @abstractmethod
    def _reset(self):
        """
        Resets account but retains certain attribute (e.g. reference currency).
        Clock is set to 0.
        Depot position and all data structures used for computation should be reset as well.
        :return: None
        """