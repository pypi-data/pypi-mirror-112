from abc import ABCMeta, abstractmethod


class BaseEngine(metaclass=ABCMeta):
    """
    Base class for backtesting engines.
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    If derived class shall be used with FXDashboard, then call signature of load_result has to be:
        dict = load_result(strategy_name, window_size, start_index)
                strategy_name: str,
                               same as FXStrategy.name of strategy, which was passed to FXEngine at __init__
                window_size: int or None,
                             window length (which does not need to take lookback size into account)
                             None: defaults to largest window size available in self.run_register, which filled during
                                   self.run()
                start_index: int, 'runthrough' or None
                             start index of run (which also includes lookback size)
                             None: defaults either to 'runthrough' if 'runthrough' is present in
                                   self.run_register[strategy_name][window_size], which is filled during self.run(),
                                   or if 'runthrough' is not present, to the minimal start_index in
                                   self.run_register[strategy_name][window_size]
                returns dict,
                     keys: {'signals', 'positions', 'merged_positions', 'total_balances', 'merged_total_balances'}
                           see FXStrategy for further details
                     values: list of str ('signals') or list of floats (other keys)
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    """

    @abstractmethod
    def run(self, data, reference_currency):
        """
        Performs backtesting by executing all strategies bound to this class.
        :param data: dict with:
                     keys: currency pair as tuple of strings: (currency_0, currency_1)
                     values: list of floats as exchange rates per time step t or array of floats

                     {(base, quote): [rate_0, rate_1, ..., rate_t],
                      (base, quote): [rate_0, rate_1, ..., rate_t],
                      ...}

                     All values (list or array of floats) of all keys (currency pairs) have to be of same length.

                     Exchange rate is expressed in FX notation convention (direct notation, not volume notation)
                     1.2 EUR|USD --> 1.2 USD for 1 EUR

                     None values allowed (if handling via accounts during account.tick(data_point_t) is ensured.
                     data_point_t is a data dict only containing time steps which are fed to strategy decision function
                     at each loop).
        :param reference_currency: str
        :return: run_balances: dict,
                               dictionary holding start and final balance/ total value in param:reference_currency of
                               each run.
        """

    @abstractmethod
    def analyze(self):
        """
        Analyzes results from run() method, e.g. with a given set of metrics.
        """

    @abstractmethod
    def reset(self):
        """
        Resets engine. Resets internal storage of last analysis results. This called every time as first at run()
        method to ensure a clean backtesting start without any remaining data from previous runs.
        :return: None
        """

    @abstractmethod
    def close(self):
        """
        Performs clean up routine and can be bound via weakref.finalize in order to ensure, this method is also
        performed when object gets garbage collected.
        :return: None
        """

    @abstractmethod
    def load_result(self, strategy_name):
        """
        Returns numerical results of self.run() for given strategy (identified by strategy name) as the total
        time series of strategy executions at every time step of data, which was used at self.run()
        If derived class shall be used with FXDashboard, then call signature has to be:
            dict = load_result(strategy_name, window_size, start_index)
                strategy_name: str,
                               same as FXStrategy.name of strategy, which was passed to FXEngine at __init__
                window_size: int or None,
                             window length (which does not need to take lookback size into account)
                             None: defaults to largest window size available in self.run_register, which filled during
                                   self.run()
                start_index: int, 'runthrough' or None
                             start index of run (which also includes lookback size)
                             None: defaults either to 'runthrough' if 'runthrough' is present in
                                   self.run_register[strategy_name][window_size], which is filled during self.run(),
                                   or if 'runthrough' is not present, to the minimal start_index in
                                   self.run_register[strategy_name][window_size]
                returns dict,
                     keys: {'signals', 'positions', 'merged_positions', 'total_balances', 'merged_total_balances'}
                           see FXStrategy for further details
                     values: list of str ('signals') or list of floats (other keys)
        :param strategy_name: str
        :return: dict,
                 keys: {'signals', 'positions', 'merged_positions', 'total_balances', 'merged_total_balances'}
                       see BaseStrategy for further details
                 values: list of str ('signals') or list of floats (other keys)
        """

    @property
    @abstractmethod
    def name(self):
        """
        Implement self.name={str} as class attribute
        """

    @property
    @abstractmethod
    def lookbacks(self):
        """
        Implement self.lookback=dict as class attribute, e.g. self.lookback[strategy_name] = int
        """

    @property
    @abstractmethod
    def reference_currency(self):
        """
        Implement self.reference_currency={str} as class attribute
        """

    @property
    @abstractmethod
    def analysis_results(self):
        """
        Implement self.analysis_results=dict as class attribute, which holds results from self.analyze()
        regarding a custom set of metrics
        """

    @property
    @abstractmethod
    def standard_analysis_results(self):
        """
        Implement self.standard_analysis_results=dict as class attribute, which holds results from self.analyze()
        regarding a default set of metrics
        """

    @property
    @abstractmethod
    def is_analyzed(self):
        """
        Implement self.is_analyzed=bool as class attribute, which is set to True after calling self.analyze()
        """

    @property
    @abstractmethod
    def price_data(self):
        """
        Implement self.price_data=dict as class attribute, which holds the price data supplied to self.run(). see
        def run() for details about data format. This is done, because analysis results only make sense for a given
        set of data.
        """

    @property
    @abstractmethod
    def volume_data(self):
        """
        Implement self.volume_data=dict as class attribute, which holds the volume data supplied to self.run(). see
        def run() for details about data format. This is done, because analysis results only make sense for a given
        set of data.
        """

    @property
    @abstractmethod
    def run_register(self):
        """
        Implement self.run_register=dict as class attribute, which stores how data was sampled and sliced into sub-sets
        for performing backtesting through out different market phases represented in data, e.g. as
        self.run_register[strategy_name][window_length] = [start_index_0, start_index_1, ..., start_index_n]
        where window_length and start_index_x are used to sliced data.
        """

    @property
    @abstractmethod
    def _tmp_dir(self):
        """
        Implement self._tmp_dir={str} as class attribute, which holds the path to temporary directory. Temporary
        directory is used to cache results from self.run(), as this is easier and more efficient regarding
        parallelization.
        """

    @property
    @abstractmethod
    def strategies(self):
        """
        Implement self.strategies=list as class attributes, which holds trapeza.strategy.base_strategy.BaseStrategy
        objects. Those strategies will be backtested, analyzed and compared.
        """

    @property
    @abstractmethod
    def metrics(self):
        """
        Implement self.metrics=list as class attribute, which holds all keys of self.analysis_results as strings
        (metric names of custom metric dictionary passed to self.analyze()).
        """
