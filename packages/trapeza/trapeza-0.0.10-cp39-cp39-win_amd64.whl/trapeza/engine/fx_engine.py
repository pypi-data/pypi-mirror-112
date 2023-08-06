import tempfile
import inspect
import warnings
import os
import pathlib
import shutil
import weakref

import pickle
import math
import random
from joblib import Parallel, delayed, cpu_count

import numpy as np

from trapeza.strategy.base_strategy import BaseStrategy
from trapeza.engine.base_engine import BaseEngine
from trapeza import metric
from trapeza.utils import check_types, find_prefix, StringTupleKeyDict
from trapeza import exception as tpz_exception


# noinspection PyAbstractClass
class FXEngine(BaseEngine):
    """
    Derived from BaseEngine class. This implementation is meant to be used with FXStrategy (and FXAccount).
    Strategy names must not contain any other strategy's name as substring (must truly be unique).
    In principal, this implementation works with any class objects derived from BaseAccount and BaseStrategy.

    USES SLOTS: ['strategies', 'name', 'lookbacks', 'reference_currency', '_tmp_dir',
                 'is_analyzed', 'analysis_results', 'standard_analysis_results', 'metrics',
                 'run_register', 'has_run', 'price_data', 'volume_data', 'is_loaded_from_file', 'clean_cache_artifacts',
                 'n_jobs', 'from_child', '_finalizer', '_ignore_type_checking']

    This class is a backtest automation designed for use with FXStrategy.
    The overall goal of this backtesting framework is to retrieve statistically analyzable results. Therefore, the
    backtest engine slices coherent and consecutive time series sub-portions from the supplied data and executes a
    trading strategy (supplied as FXStrategy class object). The backtest engine uses different window sizes and
    different start indices for slicing time series sub-portion. Thereby, strategies can be tested for dependencies of
    their performance with respect to time-being-invested and to different market phases (if they are captured
    within the supplied data). If the underlying supplied data can be interpreted as random walk (e.g. stock prices),
    this methodology is comparable to random sampling of strategy execution results, which in turn can be statistically
    interpreted. This is especially useful for strategies, which are path-dependent. This approach roughly follows the
    idea of Monte Carlo analysis.

    For backtesting, price data has to be provided, whereas volume data is optional. Furthermore, by calling
    FXEngine.run(), supplied price and volume data (the latter defaults to None) are stored in class attributes
    FXEngine.price_data and FXEngine.volume_data. This is done to unambiguously connect used data and analysis results
    (e.g. when saving and re-loading FXEngine class object).

    In order to handle the data volume, which is produced by running strategies over a quite large domain of sampled
    data (sliced sub-portioned time series from supplied data), strategy results are stored in a temporary directory.
    For each strategy run, all results from the FXStrategy class are stored (FXStrategy.signals,
    FXStrategy.positions, FXStrategy.total_balances, FXStrategy.merged positions, FXStrategy.merged_total_balances)
    in a temporary file, as well as start and end balances (given in a user specified reference currency) per run.
    The temporary file structure is organized as follows:
        - directory:
            -[cache_dir]/[name_id]_xxx,
                e.g.: trapeza/__cache__/[name_id]_xxx where name_id is the name_id of FXEngine
                this temporary directory is created for each new object of FXEngine. cache_dir serves as parent
                directory where new FXEngine objects create their own temporary (sub-)directory named name_id.
        - files:
            - decision-function-loc_xxx
                dict: decision_fnc_loc[strategy.name] = inspect.getsource(strategy.strategy_func)
            - [strategy_name]_[window_size]_[start_index]_run_xxx
                (window_size: does not include lookback size, but only number of simulation steps)
                dict: {'signals': strategy.signals, 'positions': strategy.positions,
                       'merged_positions': strategy.merged_positions, 'total_balances': strategy.total_balances,
                       'merged_total_balances': strategy.merged_total_balances}
            - [strategy_name]_[window_size]_runthrough_run_xxx
                (window_size: len(data)-strategy.lookback)
                same as [strategy_name]_[window_size]_[start_index]_run_xxx, but this file is created if runthrough
                is enforced at FXEngine.run(), where start_index is replaced by the string 'runthrough'
                dict: {'signals': strategy.signals, 'positions': strategy.positions,
                       'merged_positions': strategy.merged_positions, 'total_balances': strategy.total_balances,
                       'merged_total_balances': strategy.merged_total_balances}
            - runs-total-balances-start-end_xxx
                dict: run_balances[(strategy.name, len_data-strategy.lookback, 'runthrough')] = [start_balance,
                                                                                                 end_balance]
                        (for runthrough)
                      run_balances[(strategy.name, window_size, start_index)] = [start_balance, end_balance]
                        (for normal runs)
    The location of the temporary directory can be specified by the user (see docstring FXEngine.__init__).
    Housekeeping of the temporary directory is handled by this class as far as possible. Nevertheless, temporary files
    might leak, leading to a cluttered disk storage. Therefore the user either can set the param:clean_cache_artifacts
    at FXEngine.__init__ to True, which tries to clean up temporary directories as far as possible, or manually
    clean up.
    Be sure not to accidentally delete other temporary files when using param:clean_cache_artifacts. This can be
    avoided by specifying a unique location at FXEngine.__init__ (see docstring of FXEngine.__init__)

    Furthermore the user can specify minimal and maximal window lengths as well as the total number of data slices for
    running FXStrategy on. Additionally, the user can enforce one run on the entire data frame independent of any
    window specifications, which is entitled with the start index 'runthrough'.
    When accessing results, each simulation run performed by FXEngine.run() is specified by its window length
    (regarding the sliced time series sub-portion of supplied data) and its start index.
    Start index indicates start point for slicing data into samples. The data is then sliced to
    [start_index: start_index + window_length + lookback]. Start index therefore factors in lookback size (opposed
    to window length). Window length, on the other hand, does not factor in lookback size, but only describes the total
    number of time steps on which the strategy should be executed on. Window size only describes the number of
    simulation steps within the respective sampled time series (lookback not factored in, see FXStrategy for
    further details of lookbacks).
    If a run on the entire data frame is enforced (see docstring of FXEngine.run() method), then the start index is
    entitled with 'runthrough' (as opposed to a integer value which specifies the time step index at which the
    simulation starts - not including lookback).
    Multiple FXStrategy class objects can be passed to FXEngine, which are then run on the same
    sliced data samples. This is especially handy for comparing and benchmarking different strategies.
    Between each run of FXEngine, all strategies are reset to the initial status to ensure correct results. All
    strategies are reset as well as soon as FXEngine has completed its run.

    The main goal of FXEngine is gathering statistical metrics instead of gathering strategy execution results as
    time series data. Nevertheless, all strategy execution data are stored as temporary file. Results can therefore be
    accessed via opening those temporary files (FXEngine._tmp_dir gives path to directory, see above temporary file
    structure for naming convention of temporary files) or via FXEngine.load_result(). Make sure to release loaded files
    etc. such that temporary file directory can be cleaned up afterwards.

    As mentioned, the main goal of FXEngine is to gather statistical metrics. This is done via FXEngine.analyze by
    passing a dictionary of metric names and metric functions. Currently, only metrics, which operate on the total
    balance time series values of a strategy expressed in a reference currency (namely FXStrategy.merged_total_balances
    is passed to any metrics function, see documentation of FXStrategy for further information), are supported.
    A standard dictionary of metrics is already implemented:
        {'total_rate_of_return': _std_tot_rate_of_ret, 'volatility': _std_annual_vola,
         'expected_rate_of_return': _std_annual_exp_rate_of_ret,
         'expected_rate_of_log_return': _std_exp_rate_of_log_ret,
         'sharpe_ratio': _std_annual_sharpe, 'sortino_ratio': _std_annual_sortino,
         'value_at_risk': _std_var, 'max_drawdown': _std_max_drawdown
         },
         (see FXEngine.analyze() for detailed description)
    where metrics functions are implemented in trapeza.metric. Users can supply any additional metrics
    dict to FXEngine.analyze(). The FXEngine.analyze() method is only callable, if FXEngine.run() has been called
    beforehand. FXEngine.analyze() loads results from temporary directory as basis of any calculations, but only uses
    'merged_total_balances'. Results of FXEngine.analyze() are accessible via FXEngine.standard_analysis_results
    (standard metrics) and FXEngine.analysis_results (user-specified metrics), which are both a dict of dicts:
        FXEngine.standard_analysis_results[strategy_name][window_size, start_index] = metric_value.

    In the case of custom metrics dictionary (respective the default metrics dictionary, if none is supplied), the
    metric names (keys of FXEngine.analysis_results[strategy_name]/ param:metric_dict of FXEngine.analyze()) are listed
    within FXEngine.metrics class attribute.

    A custom dictionary of metrics can be passed to FXEngine.analyze(). param:metric must have following signature:
             dictionary keys: str,
                              metric name
             dictionary values: callable function,
                                callable function must have following call signature:

                                    float = metric_fnc(merged_total_balances)

                                    merged_total_balances: list, see trapeza.strategy.fx_strategy.FXStrategy class

    Currently, metrics can only be evaluated on 'merged_total_balances' of each strategy of FXEngine
    (see FXStrategy for further information regarding 'merged_total_balances': FXStrategy.merged_total_balances).
    If param:metric_dict is None at FXEngine.analyze(), a default metrics dictionary is used: see FXEngine.analyze().
    Results of param:metric_dict are stored in FXEngine.analysis_results, which is a dict (keys: strategy names) of
    dict (keys: (window_size, start_index) as strings or ints, values: metric_value):
        FXEngine.analysis_results[strategy.name][window_size, start_index] = metric_value

    FXEngine.standard_analysis_results and FXEngine.analysis_results are computed in pretty much the same way and hold
    their analysis results in the same format (as dict of dicts).

    FXEngine.analysis_results holds all analysis results of custom metrics dictionary, whereas FXEngine.metrics
    holds all keys of FXEngine.analysis_results as strings (metric names of custom dictionary passed to
    FXEngine.analyze()).

    Each metric is calculated on each simulation run of FXEngine.run() (sampled sliced time series sub-portion of
    supplied data, see description above). Those metrics can then be used e.g. for further statistical analysis.
    trapeza.metric implements the most common financial metrics, which are also used in the default
    dicts.

    New strategies can be registered with the FXEngine.register() method, which overrides existing strategies in
    FXEngine class object. This method is used to avoid creating a new FXEngine class object. All internal class object
    attributes are reset or emptied (e.g. FXEngine.standard_analysis_results). In general, resetting during
    FXEngine.run() is always referenced to the status, at which strategies and their accounts (see FXAccount) where
    registered via FXEngine.register() or via FXEngine.__init__() (initial status from which to start benchmarking).

    !!! FXEngine should be closed explicitly by using FXEngine.close() !!!
    This deletes and cleans up all temporary files and directories and destroys the class object. Nevertheless,
    this is also done, when FXEngine class object is garbage collected, but users should not solely rely on that this
    automated clean up performs problem-free. Furthermore, if the main process gets unexpectedly interrupted, temporary
    files and directories might leak and might need manual clean up in order to avoid cluttering disk space (see
    description above).

    If any exception is thrown internally, e.g. by passing wrong arguments, FXEngine will perform an auto-clean up
    routine, which deletes all temporarily created files (same routine as in FXEngine.close()). Nevertheless,
    users shouldn't rely to heavily on this!!!

    FXEngine class object can be saved and loaded with its current internal states (e.g. metric dicts ect.).
    As all supplied data is also written internally to FXEngine.price_data and FXEngine.volume_data class attributes,
    data, that has been supplied to FXEngine.run(), is also saved and re-loaded into those attributes. If the user wants
    to reduce the size of the saved FXEngine files and has the data persistently saved separately, then set the
    attributes FXEngine.price_data=None and FXEngine.volume_data=None and re-set them after loading FXEngine class
    object via FXEngine.price_data=prices and FXEngine.volume_data=volumes.

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
        >>  # create a backtesting engine
        >>  engine = FXEngine('gemini', strat)
        >>
        >>  # perform backtesting simulation where strategy is tested on 100 data frames, which consist of a
        >>  #   window length between 10 and 50 time steps plus one simulation run, which is done on the entire
        >>  #   data frame
        >>  engine.run(prices, 'USD', volumes,
        >>             min_run_length=10, max_run_length=50, max_total_runs=100, run_through=True)
        >>
        >>  # analyze metrics
        >>  engine.analyze()
        >>
        >>  # access result for the simulation run, which was performed on the entire data frame
        >>  print(engine.standard_analysis_results['genesis'][len_data, 'runthrough'])
        >>
        >>  # do not forget to close engine
        >>  engine.close()  # !!!

    Furthermore, results from FXEngine.run() and FXEngine.analyze() can be visualised via FXDashboard. As the main goal
    of this library is numerical backtesting, FXDashboard only provides a minimal viable visualization implemented via
    Python Dash. FXDashboard analyzes results stored in temporary file structure. It is sufficient to only pass the
    FXEngine class object, as the path to those temporary files is stored in the FXEngine._tmp_dir attribute.
    Analysis results in FXEngine.standard_analysis_results and FXEngine.analysis_results are used by FXDashboard for
    visualization as well. Do not overwrite or manipulate class attributes or temporary files manually.

    FXEngine.run_register gives an overview of all windows and start indices, which were created/ used
    during FXEngine.run():
        FXEngine.run_register[strategy.name][window_size] = [start_index_0, start_index_1, ...]
    (dict of dict, window_size as integer).
    """
    __slots__ = ['strategies', 'name', 'lookbacks', 'reference_currency', '_tmp_dir',
                 'is_analyzed', 'analysis_results', 'standard_analysis_results', 'metrics',
                 'run_register', 'has_run', 'price_data', 'volume_data', 'is_loaded_from_file',
                 'n_jobs', 'from_child', '_finalizer', '_ignore_type_checking']

    def __init__(self, name_id, strategies, cache_dir='__system__', loc_decision_functions=False,
                 clean_cache_artifacts=False, ignore_type_checking=False, n_jobs=-1):
        """
        Initializes FXEngine class object for backtesting.
        Parallelization is implemented via joblib.

        Recommendation: For safety reasons, use loc_decision_functions=False in order to avoid that source code
                        of strategy decision function is written to a temporary file (which eventually might leak
                        if process is unexpectedly interrupted).
                        Be careful when using clean_cache_artifacts=True to not unintentionally delete temporary files
                        of other programs. Therefore set cache_dir appropriately (default setting should be safe to use)

        In most cases, if an exception is thrown internally, this class will auto-clean up all temporary files,
        which have been created by this class object. Nevertheless, users shouldn't rely to heavily on this
        auto-clean up.

        Each new FXEngine creates a new temporary sub-directory under cache_dir, which serves as some kind of parent
        directory of this library. FXEngine then stores all results as temporary files under the freshly created
        temporary sub-directory, which was created under cache_dir. It is recommended to use a unique cache_dir path
        (default argument should do the job well enough). If clean_cache_artifacts is set to true, all temporary
        sub-directories and temporary files created by any FXEngine class instance will be deleted and cleaned up
        (so be sure to use a cache_dir, which is not used by any other programs to avoid unintentionally deleting other
        program's temporary files). cache_dir will not be deleted by clean_cache_artifacts as, in general, it serves
        as some kind of parent directory for this library (or at least for FXEngine class).

        :param name_id: str,
                        unique name of Engine
        :param strategies: list of FXStrategy objects (or objects derived from
                           trapeza.strategy.base_strategy.BaseStrategy),
                           strategy must have unique names (no two strategies with same name attribute FXStrategy.name),
                           strategy names must not contain any other strategy's name as substring
        :param cache_dir: str,
                          specifies path to directory, in which to store a temporary directory (gets cleaned up and
                          deleted afterwards) used as cache
                          '__system__' directs to platform specific default directory of python tempfile package in
                                       which the directory trapeza/FXEngine/self.name is created to store all
                                       temporary files
                                       under Windows: C:/Users/username/AppData/Local/Temp/trapeza/FXEngine/self.name
                          '__cache__' directs to 'package_path/__cache__/' where a new temporary sub-directory
                                      with directory name given by self.name will be created to store all temporary
                                      files
                          or use user-specific path at which a new temporary sub-directory is created with the name
                                              given by self.name to store all temporary files
        :param loc_decision_functions: bool,
                                       if True, line of codes (source file) of decision function of each strategy is
                                                retrieved for later use e.g. in dashboard visualization.
                                                Source code of strategy decision function will be written to a temporary
                                                file (see temporary file structure a class description).
                                       if False, does not try to read line of codes of decision function

                                       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                       Be careful using this option, as it exposes code to temporary directory, which
                                       might be readable for third parties (even though tempfile library is used).
                                       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        :param clean_cache_artifacts: bool,
                                      if True, files and subdirectories in param:cache_dir are deleted before object
                                      is initiated.
                                      Usually, there shouldn't be any residue temporary folders left within
                                      param:cache_dir, as this class cleans everything up automatically. In some cases,
                                      e.g. if the running Python process is interrupted by exception or killed by user,
                                      temporary files and subdirectory may remain unintentionally in param:cache_dir.
                                      To avoid cluttering, param:clean_cache_artifacts can be set to True in order to
                                      clean up those unintentionally left temporary files and subdirectories from
                                      previously interrupted Python processes (which ran this class).
                                      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                      Be careful not to unintentionally delete any temporary files from other programs.
                                      This can be avoided by setting param:cache_dir appropriately.
                                      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        :param ignore_type_checking: bool,
                                     if True, type checking of input arguments is suppressed which increases performance
                                     if False, explicit type checking is done. If types do not comply, an exception is
                                     thrown and clean up routine (see self.close()) is invoked automatically to clean
                                     up all temporary files created by this class object. This might decrease
                                     performance but increases safety.
        :param n_jobs: int,
                       number of jobs running in parallel during self.run(), implementation based on joblib
                       -1: run maximal number of jobs in parallel (either max number of cores of max number of jobs
                           if the latter is less than max number of cores)
                       0: run in single process, no extra process will be spawned for parallelization
                       int > 0: distinct number of cores
        :raises: TypeError, if parameters do not match specified types,
                            only thrown if ignore_type_checking is False (type_checking enabled at __init__)
                 trapeza.exceptions.StrategyError, if strategies not derived from
                                                   trapeza.strategy.base_strategy.BaseStrategy or if
                                                   at least two strategies have same name attributes strategy.name
                 auto-clean up via self.close() if any exception is thrown internally
        """
        super().__init__()

        # clean artifacts from previous failed runs
        if clean_cache_artifacts is True:
            if cache_dir == '__cache__':
                clean_dir = (pathlib.Path(__file__).parent / '..' / cache_dir).resolve()
            elif cache_dir == '__system__':
                clean_dir = os.path.join(tempfile.gettempdir(), 'trapeza', 'FXEngine')
            else:
                if os.path.isabs(cache_dir):
                    clean_dir = cache_dir
                else:
                    clean_dir = os.path.join(os.getcwd(), cache_dir)
            # check whether directory exists
            if os.path.exists(clean_dir):
                self._clean_artifacts(clean_dir)

        check_types([ignore_type_checking], [bool], ['ignore_type_checking'])
        self._ignore_type_checking = ignore_type_checking

        # check types
        check_types([name_id, cache_dir, loc_decision_functions, n_jobs, clean_cache_artifacts],
                    [str, str, bool, int, bool],
                    ['name_id', 'cache_dir', 'loc_decision_functions', 'n_jobs', 'clean_cache_artifacts'],
                    self._ignore_type_checking)

        # unique name used to build temp file directory
        self.name = name_id

        # checks and holds all strategies
        self.strategies = None
        self._check_assign_strategies(strategies)

        # check if a strategy name is substring of any other  strategy name
        # noinspection PyTypeChecker
        if len(self.strategies) > 1:  # only relevant, if more than on strategy is assigned
            # noinspection PyTypeChecker
            name_list = [strategy.name for strategy in self.strategies]
            shortest_name = min(name_list, key=len)
            is_substring = [True if shortest_name != strategy_name and shortest_name in strategy_name else False
                            for strategy_name in name_list]
            if True in is_substring:
                raise tpz_exception.StrategyError('At least on of the strategy names is a substring of one other '
                                                  'strategy name. Use unique and mutual substring-free strategy names.')

        # parallelization
        self.n_jobs = n_jobs
        self.from_child = False  # used to identify child process and control __del__

        # check if strategies have unique names
        # noinspection PyTypeChecker
        strategy_names = set([strats.name for strats in self.strategies])
        # noinspection PyTypeChecker
        if len(strategy_names) < len(self.strategies):
            raise tpz_exception.StrategyError('All strategies must have unique name attributes (strategy.name).')

        # open cache directory and store
        if cache_dir == '__cache__':
            cache_dir = (pathlib.Path(__file__).parent / '..' / cache_dir).resolve()
        elif cache_dir == '__system__':
            if not os.path.exists(os.path.join(tempfile.gettempdir(), 'trapeza', 'FXEngine')):
                os.makedirs(os.path.join(tempfile.gettempdir(), 'trapeza', 'FXEngine'))
            cache_dir = os.path.join(tempfile.gettempdir(), 'trapeza', 'FXEngine')
        else:
            if os.path.isabs(cache_dir):
                if not os.path.exists(cache_dir):
                    os.makedirs(cache_dir)
            else:
                if not os.path.exists(os.path.join(os.getcwd(), cache_dir)):
                    os.makedirs(os.path.join(os.getcwd(), cache_dir))
                cache_dir = os.path.join(os.getcwd(), cache_dir)
        self._tmp_dir = tempfile.mkdtemp(prefix='{}_'.format(self.name), dir=cache_dir)

        # variables for analysis
        self.has_run = False
        self.is_analyzed = False
        self.analysis_results = dict()
        self.standard_analysis_results = dict()
        # structure of self.analysis_results:
        # self.analysis_results[strategy_name][length, start_index][metric]
        self.metrics = None
        self.run_register = dict()
        # self.run_register[strategy_name][length] = [start_index_0, start_index_1, ..., start_index_n]
        self.reference_currency = None

        # store data
        self.price_data = None
        self.volume_data = None

        # define if object is initiated or loaded from file, which doesn't need deleting temp directory
        self.is_loaded_from_file = False

        # holds lookback values of all strategies for visualization input data correctly
        # noinspection PyTypeChecker
        self.lookbacks = {strat.name: strat.lookback for strat in self.strategies}

        # dump line of codes of source files of decision functions of strategies into temporary directory
        if loc_decision_functions:
            try:
                self._tmp_dump_decision_funcs()
            except Exception as e:
                self._deconstruct_tmp_dir()
                raise e

        # make sure temp directory gets cleaned up afterwards
        self._finalizer = weakref.finalize(self, self._deconstruct_tmp_dir_finalize, self.is_loaded_from_file,
                                           self.from_child, self._tmp_dir)

    @staticmethod
    def _clean_artifacts(clean_dir):
        """
        Uses shutil.rmtree(cache_dir) to delete sub-directories and files of cache_dir (cache_dir itself will not
        be deleted).
        In general, cache_dir is the parent directory, where FXEngine defaults to store temporary files. Therefore,
        FXEngine creates a new directory for each new class object of FXEngine under cache_dir to store results via
        temporary files.
        :param clean_dir: str, path to parent directory where FXEngine defaults to create new temporary director for
                               each __init__, absolute full path
        :return: None
        :raises: auto-clean up via self.close() if any exception is thrown internally
        """
        for file in os.listdir(clean_dir):
            f_name = os.path.join(clean_dir, os.fsdecode(file))
            try:
                shutil.rmtree(f_name)
            except FileNotFoundError:
                pass
            except OSError as ose:
                warnings.warn('OSError: could not remove file {}. See: {}'.format(f_name, ose))

    def _check_assign_strategies(self, strategies):
        """
        Checks if strategies (or strategy) are derived from trapeza.strategy.base_strategy.BaseStrategy
        and assigns them internally to self.strategies (or [strategy])

        :param strategies: list of FXStrategy objects
        :return: None
        :raises: trapeza.exceptions.StrategyError, if strategies not derived from
                                                   trapeza.strategy.base_strategy.BaseStrategy
                 auto-clean up via self.close() if any exception is thrown internally
        """
        try:
            for strategy in strategies:
                if not issubclass(strategy.__class__, BaseStrategy):
                    raise tpz_exception.StrategyError(strategy, 'Strategy has to inherit from '
                                                                'trapeza.strategy.base_strategy.BaseStrategy.')
            self.strategies = strategies
        except TypeError:
            if not issubclass(strategies.__class__, BaseStrategy):
                raise tpz_exception.StrategyError(strategies, 'Strategy has to inherit from '
                                                              'trapeza.strategy.base_strategy.BaseStrategy.')
            self.strategies = [strategies]
        except tpz_exception.StrategyError as e:
            # re-raise
            raise e

    def _build_partitioning_indices(self, length_data, lookback, min_window_length, max_window_length,
                                    max_total_runs=None):
        """
        Calculates sampling windows and randomly samples appropriate start indices for each sampling window w.r.t
        max_total_runs and lookback of respective strategy.

        Window size already takes account of lookback size, so just focus on 'simulation steps' as window size.
        That means, that window length do not need to respect lookback. Just pass number of simulation steps as window
        length.

        If possible, min_window_length, max_window_length and max_total_runs are auto-adapted.
        See parameter description.

        Start index indicates start point for slicing data into samples. Data is sliced to
        [start_index: start_index + window_length + lookback]. Start index therefore factors in lookback size (opposed
        to window length, which does not account for lookback but only gives total number of time steps per simulation
        run).

        :param length_data: int,
                            length of data dict used e.g. in self.run()
        :param lookback: int,
                         lookback steps of respective strategy for which to sample data
        :param min_window_length: int > 0,
                                  minimal sampling window size, must be less than max_window_length (see auto-restrict
                                  of param:max_window_length)
        :param max_window_length: int,
                                  maximal sampling window size.
                                  If max_window_length is greater than effectively available data time steps
                                  (len of data - lookback), then max_window_length is auto-restricted to max available
                                  number of data time steps (len of data - lookback)
        :param max_total_runs: int, {'all_once'} or None,
                               maximal number of runs in total over all possible window sizes and samples
                               if None, number of total runs will not be constrained (runs simulation on all possible
                                    windows for each given window size/ run length)
                               if 'all_once', each window size/ run length will be run exactly once
                               if int and max_total_runs < number of possible windows (max_window_length
                                    - min_window_length + 1), then some window lengths/ run lengths
                                    will be left out (randomly) such that the number of total runs is close but never
                                    greater than max_total_runs
        :return: dict_indices: dict,
                               key: int, window_size
                               value: int, start_index in data_dict
                                      start_index is the index, at which to start slicing data,
                                      data has then to be sliced to start_index + win_size + lookback
        :raises: ValueError, if length_data <= lookback, min_window_length is less than 1 or
                             if min_window_length is greater than max_window_length
                 TypeError, if param:max_total_runs is not of specified type,
                            only thrown if ignore_type_checking is False (type_checking enabled at __init__)
                 auto-clean up via self.close() if any exception is thrown internally
        """
        # calculate partitions
        # randomly sample indices per partition
        # return indices

        try:
            eff_length_data = length_data - lookback
            if eff_length_data <= 0:
                raise ValueError('Data does not contain enough time steps: {}. '
                                 'Data has to contain more time steps than '
                                 'specified by lookback: {}.'.format(length_data, lookback))
            if eff_length_data < max_window_length:
                max_window_length = eff_length_data
                warnings.warn('Data does not contain enough time steps: {}. Data has to contain more time steps than '
                              'specified by max_window_length + lookback: {} + {}. Auto-restricting max_window_length '
                              'to {}.'.format(length_data, max_window_length, lookback, eff_length_data))
            if min_window_length < 0:
                raise ValueError('min_window_length must be greater 0.')
            if min_window_length > max_window_length:
                raise ValueError('min_window_length must be less or equal to max_window_length.')
            nr_windows = max_window_length - min_window_length + 1
            if isinstance(max_total_runs, int):
                max_nr_runs_per_window = max_total_runs / nr_windows
                if max_nr_runs_per_window < 1:
                    warnings.warn('max_total_runs is too small, not all sampling windows can be covered '
                                  'sufficiently. max_total_runs: {}, min_run_length: {}, max_run_length: {} and '
                                  'number of possible windows: {}. Under-sampling is done such that not all window '
                                  'lengths will be covered (left out randomly such that the total number of runs is '
                                  'close but at least not greater then max_total_runs).'.format(max_total_runs,
                                                                                                min_window_length,
                                                                                                max_window_length,
                                                                                                nr_windows))
                else:
                    max_nr_runs_per_window = math.floor(max_nr_runs_per_window)
                    max_total_runs = int(max_nr_runs_per_window * nr_windows)
            elif max_total_runs == 'all_once':
                max_nr_runs_per_window = 1
                max_total_runs = nr_windows
            elif max_total_runs is None:
                max_nr_runs_per_window = np.inf
            else:
                # Raise TypeError even tough ValueError might suit as well. This is because check_types would throw
                # a TypeError, therefore this is the most consistent error type
                raise TypeError('max_total_runs must be int, {all_once} or None.')
            dict_indices = dict()
            counter_runs = 0
            for window_size in range(min_window_length, max_window_length + 1):
                n_max_runs = eff_length_data - window_size + 1
                if max_nr_runs_per_window < 1:
                    if np.random.binomial(1, max_nr_runs_per_window) == 1 and counter_runs < max_total_runs:
                        start_indices = [random.randrange(0, n_max_runs)]
                        counter_runs += 1
                    else:
                        continue
                else:
                    start_indices = np.random.choice(n_max_runs,
                                                     int(np.min((n_max_runs, max_nr_runs_per_window))),
                                                     replace=False).tolist()
                dict_indices[window_size] = start_indices
        except Exception as e:
            self._deconstruct_tmp_dir()
            raise e
        return dict_indices

    def _iter_partition_indices(self, dict_partitioning_indices):
        """
        Iterator over self._build_partitioning_indices return value (dict) yielding window length and start index.

        :param dict_partitioning_indices: dict,
                                          see return value from self._building_partitioning_indices
        :return: list,
                 next [window size, start index] yielded from self._build_partitioning_indices return value
        :raises: auto-clean up via self.close() if any exception is thrown internally
        """
        # yield data subset
        try:
            for window_size in dict_partitioning_indices.keys():
                for start_index in dict_partitioning_indices[window_size]:
                    yield [window_size, start_index]
        except Exception as e:
            self._deconstruct_tmp_dir()
            raise e

    def _reset_tmp_dir(self, clean_lookbacks=True, clean_loc_decision_funcs=True):
        """
        Removes all files within temporary directory self._tmp_dir, which is used as cache.
        Exception is not raised if no temporary dictionary is available.
        :param clean_lookbacks: bool,
                               if True, also deletes file, which stores lookback values
                               if False, keeps file storing lookback values
                               use param:clean_lookback=False if engines has to be cleaned up for next run
                               use param:clean_lookback=True if engines is going to be closed
                               exceptions is not raised if no lookbacks in temporary dictionary
        :param clean_loc_decision_funcs: bool,
                                         if True, also deletes file, which stores loc_decision_functions values
                                         if False, keeps file storing loc_decision_functions values
                                         use param:clean_loc_decision_funcs=False if engines has to be cleaned up for
                                            next run
                                         use param:clean_loc_decision_funcs=True if engines is going to be closed
                                         exceptions is not raised if no loc_decision_funcs in temporary dictionary
        :return: None
        :raises: auto-clean up via self.close() if any exception is thrown internally
        """
        if self.is_loaded_from_file is True:
            return

        if not pathlib.Path(self._tmp_dir).is_dir():
            return
        for file in os.listdir(self._tmp_dir):
            f_name = os.path.join(self._tmp_dir, os.fsdecode(file))
            if clean_lookbacks is False and 'lookbacks_' in f_name:
                continue
            if clean_loc_decision_funcs is False and 'decision-function-loc_' in f_name:
                continue
            try:
                os.remove(f_name)
            except FileNotFoundError:
                pass
            except PermissionError:
                shutil.rmtree(self._tmp_dir)

    def _deconstruct_tmp_dir(self):
        """
        Removes all files within temporary directory self._tmp_dir, which is used as cache, and delete temporary
        directory.
        Exception is suppressed if no temporary dictionary is available
        :return: None
        """
        if self.is_loaded_from_file is True:
            return

        if self.from_child is True:
            return

        if not pathlib.Path(self._tmp_dir).is_dir():
            return
        try:
            shutil.rmtree(self._tmp_dir)
        except Exception as e:
            warnings.warn('Unable to clean up temporary directory at {}. '
                          'Files are leaked and not deleted at {}. '
                          'Extant files have to be removed manually'.format(self._tmp_dir, self._tmp_dir))
            raise e

    @classmethod
    def _deconstruct_tmp_dir_finalize(cls, _is_loaded_from_file, _from_child, _tmp_dir):
        """
        Used for handling via weakref.finalize (garbage collection). See self._deconstruct_tmp_dir.
        :param _is_loaded_from_file: plug in self.is_loaded_from_file
        :param _from_child: plug in self.from_child
        :param _tmp_dir: plug in self._tmp_dir
        :return: None
        """
        if _is_loaded_from_file is True:
            return

        if _from_child is True:
            return

        if not pathlib.Path(_tmp_dir).is_dir():
            return

        shutil.rmtree(_tmp_dir)

    def reset(self, delete_dir=False, clean_lookbacks=False, clean_loc_decision_funcs=False):
        """
        Resets engine. Cleans up temporary directory and resets each strategy.
        Use default values to just clean up temporary results from last self.run()
        Resets internal storage of last analysis results.
        :param delete_dir: bool, default=False,
                           if True, entire temporary directory is deleted
                           if False, only files within temporary directory (cached results) are deleted, but
                                     temporary directory remains and is usable to cache results again
                           exception is not raised if no temporary directory is available
        :param clean_lookbacks: bool, default=False,
                               if True, also deletes file, which stores lookback values
                               if False, keeps file storing lookback values
                               use param:clean_lookback=False if engines has to be cleaned up for next run
                               use param:clean_lookback=True if engines is going to be closed
                               exception is not raised if no lookbacks in temporary directory
        :param clean_loc_decision_funcs: bool, default=False,
                                         if True, also deletes file, which stores loc_decision_functions values
                                         if False, keeps file storing loc_decision_functions values
                                         use param:clean_loc_decision_funcs=False if engines has to be cleaned up for
                                            next run
                                         use param:clean_loc_decision_funcs=True if engines is going to be closed
                                         exception is not raised if no loc_decision_funcs in temporary dictionary
        :return: None
        :raises: auto-clean up via self.close() if any exception is thrown internally
        """
        self._reset_tmp_dir(clean_lookbacks=clean_lookbacks, clean_loc_decision_funcs=clean_loc_decision_funcs)
        self.analysis_results = dict()
        self.standard_analysis_results = dict()
        self.is_analyzed = False
        self.run_register = dict()
        self.has_run = False
        self.reference_currency = None
        self.metrics = None
        self.from_child = False
        self.price_data = None
        self.volume_data = None
        try:
            for strategy in self.strategies:
                try:
                    strategy.c_reset()
                except AttributeError:
                    strategy.reset()
        except Exception as e:
            self._deconstruct_tmp_dir()
            raise e
        if delete_dir:
            self._deconstruct_tmp_dir()

    def _tmp_dump_decision_funcs(self):
        """
        Retrieves line of codes of strategy decision function of each strategy, such that the code used in each strategy
        can be visualized in dashboard. Dumps results into temporary directory if possible.
        Source code of strategy decision function is then accessible as string via temporary file, so use with care
        due to safety concerns.
        See class description for file naming convention and temporary file structure.
        :return: None
        :raises: auto-clean up via self.close() if any exception is thrown internally
        """
        try:
            tmp_files = []
            try:
                decision_fnc_loc = dict()
                for strategy in self.strategies:
                    decision_fnc_loc[strategy.name] = inspect.getsource(strategy.strategy_func)
                tmp = tempfile.NamedTemporaryFile(prefix='decision-function-loc_', mode='w+b', delete=False)
                tmp_files.append(tmp)
                try:
                    pickle.dump(decision_fnc_loc, tmp, protocol=pickle.HIGHEST_PROTOCOL)
                except PermissionError as pme:
                    tmp.close()
                    self._deconstruct_tmp_dir()
                    raise pme
                tmp.flush()
                tmp.close()
            except OSError as ose:
                try:
                    for tmp in tmp_files:
                        tmp.close()
                        try:
                            os.unlink(tmp.name)
                        except FileNotFoundError:
                            pass
                except Exception as e:
                    self._deconstruct_tmp_dir()
                    raise e
                warnings.warn('Could not retrieve lines of code of decision function of strategy decision functions: '
                              '{}'.format(ose))
        except Exception as e:
            self._deconstruct_tmp_dir()
            raise e

    def run_strategy(self, strategy_index, reference_currency, window_size, start_index):
        """
        Runs single strategy with one data sample/ set (data partition) and dumps results into
        temporary directory self._tmp_dir.
        See class description for naming convention and file structure of temporary files.

        Start index takes lookback size of strategy into account such that the actual simulation starts from
        start_index + lookback (lookback provides historic data to strategy decision function for implementing custom
        trade logic). Start index gives the start point for slicing data into respective samples, therefore start index
        has to factor in lookback. The actual strategy execution starts at start_index + lookback. See class description
        and self._build_partitioning_indices() for further information.
        Opposed to start index, window length does not factor in lookback but just gives the total number
        of time steps per simulation run.
        Data is sliced according to [start_index: start_index + window_length + lookback].

        If a runthrough on the entire data frame is enforced (by setting param:run_through=True in self.run()), then
        start index is set to 'runthrough', whereas start index normally is an integer.

        :param strategy_index: int,
                               index number within self.strategies in order to select strategy, which shall be run
        :param reference_currency: str,
                                   reference currency in which to bill total balances of all accounts
        :param window_size: int,
                            sampling window size of respective price_data_partition and volume_data_partition, which are
                            fed into strategy.run, indexing with respect to complete data sets self.price_data and
                            self.volume_data
        :param start_index: int or 'runthrough',
                            start index of respective price_data_partition and volume_data_partition, which are fed
                            into strategy.run, indexing with respect to complete data sets self.price_data and
                            self.volume_data
                            if start_index='runthrough', start_index is internally set to 0
        :return: strategy.merged_total_balances[0]: int,
                                                    start balance/ total value of strategy in param:reference_currency
                 strategy.merged_total_balances[-1]: int,
                                                     final balance/ total value of strategy in param:reference_currency
        :raises: TypeError, if parameters do not match specified types (pay attention, that type checking might be
                            turned off, cf. self._ignore_type_checking at self.__init__, in which case, this error is
                            only thrown, if self.price_data is None)
                 auto-clean up via self.close() if any exception is thrown internally
        """
        # runs single strategy and save to temp file
        try:
            if self.price_data is None:
                raise TypeError('self.data is None. If this function shall be called independent from FXEngine.run(),'
                                'then pre-set FXEngine.data=data before calling FXEngine.run_strategy().')

            check_types([reference_currency, window_size], [str, int], ['reference_currency', 'window_size'],
                        self._ignore_type_checking)

            if start_index == 'runthrough':
                s_ind = 0
            else:
                s_ind = start_index

            self.from_child = True
            strategy = self.strategies[strategy_index]
            price_data_partition = {k: self.price_data[k][s_ind: s_ind + window_size + self.lookbacks[strategy.name]]
                                    for k in self.price_data.keys()}
            if self.volume_data is not None:
                volume_data_partition = {
                    k: self.volume_data[k][s_ind:s_ind + window_size + self.lookbacks[strategy.name]]
                    for k in self.volume_data.keys()}
            else:
                volume_data_partition = None
            try:
                if volume_data_partition is None:
                    parsed_volume_data_partition = {}
                else:
                    parsed_volume_data_partition = volume_data_partition
                len_data = len(price_data_partition[list(price_data_partition.keys())[0]])
                strategy.c_wrap_run(price_data_partition, reference_currency.encode(), parsed_volume_data_partition,
                                    len_data)
            except AttributeError:
                strategy.run(price_data_partition, reference_currency, volume_data_partition)

            tmp = tempfile.NamedTemporaryFile(prefix='{}_{}_{}_run_'.format(strategy.name, window_size, start_index),
                                              dir=self._tmp_dir,
                                              mode='w+b', delete=False)
            results = {'signals': list(strategy.signals),
                       'positions': dict(strategy.positions),
                       'merged_positions': dict(strategy.merged_positions),
                       'total_balances': list(strategy.total_balances),
                       'merged_total_balances': list(strategy.merged_total_balances)}
            try:
                pickle.dump(results, tmp, protocol=pickle.HIGHEST_PROTOCOL)
            except Exception as e:
                tmp.close()
                self._deconstruct_tmp_dir()
                raise e
            tmp.flush()
            tmp.close()
        except Exception as e:
            self._deconstruct_tmp_dir()
            raise e
        return (strategy.name, window_size, start_index,
                strategy.merged_total_balances[0], strategy.merged_total_balances[-1])

    # noinspection DuplicatedCode
    def run(self, price_data, reference_currency, volume_data=None,
            min_run_length=None, max_run_length=None, max_total_runs=None, run_through=True):
        """
        Performs random sampling of input data into different sized windows, runs all strategies on sampled data and
        dumps results into temporary directory self._tmp_dir. See class description for file naming convention and
        file structure of temporary directory.

        Just focus on 'simulation steps' as window size. Do not extra calculate lookback size into window size as this
        is handled automatically.

        Strategies of FXEngine are reset after run(), e.g. clocks and depots of accounts (contained within each
        strategy) as well as all results such as signals, positions, merged_positions, total_balances, merged_balances
        of strategies. Results are emptied out, depots and clocks are restored to the same status as of the time as
        they were bond to FXStrategy by initialization of FXStrategy after run() finishes. Resetting is also done
        at each loop within run(), such that each loop simulates a freshly initialized FXStrategy.run().

        Results of run() are dumped into temporary directory self._tmp_dir:
            'runs-total-balances-start-end_....':
                    dict,
                    key: (strategy.name, window_size, start_index)
                         or if runthrough: (strategy.name, len_data-strategy.lookback, 0)
                    value: [start_balance_at_t_0, end_balance_at_t_-1]

            '{}_{}_{}_run_...'.format(strategy.name, window_size, start_index):
                    dict,
                    key: str {'signals', 'positions', 'merged_positions', 'total_balances', 'merged_total_balances'}
                    value: respective FXStrategy result
            '{}_{len_data-lookback}_runthrough...':.format(strategy.name):
                    dict,
                    key: str {'signals', 'positions', 'merged_positions', 'total_balances', 'merged_total_balances'}
                    value: respective FXStrategy result

        Further temporary files:
            'lookbacks_.....':
                    dict,
                    keys: str, strategy name
                    value: int, lookback size
            'decision-function-loc_....':
                    dict,
                    keys: str, strategy name
                    value: str, line of codes

        win_size: Size of data sampling window, which describes number of simulation steps for corresponding data
                  sample. Size of lookback is excluded from this (e.g. sample size is win_size+lookback)
        start_ind: Index within param:data at which data sample starts. This already accounts for lookback, e.g.
                   simulation starts at index=lookback. start_ind describes where to start slicing for taking
                   respective data sample out of param:data: [start_ind: start_ind+win_size+lookback]
                   (start_ind already includes prepending lookback data)
        lookback: amount of historic data to prepend for each run, see FXStrategy

        The main goal of FXEngine is to perform statistical analysis via metrics instead of providing a full data log
        of all simulation runs. Nevertheless, results can be accessed via temporary files of self.load_result().

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
        :param min_run_length: None or int > 0,
                               minimal length of data to simulate a strategy run through randomly and
                               consecutive sampled subset of data time steps (minimal window length for simulation run),
                               must be less than max_window_length (see auto-restrict of param:max_window_length).
                               If None, min_run_length = 1.
        :param max_run_length: None or int > param:min_run_length,
                               maximum length of data to simulate a strategy run through randomly and
                               consecutive sampled subset of data time steps (maximal window length for simulation run),
                               If max_window_length is greater than effectively available data time steps
                               (len of data - lookback), then max_window_length is auto-restricted to max available
                               number of data time steps (len of data - lookback)
                               if None, max_run_length is set to maximum: len of data - lookback
                               if param:max_run_length <= min_run_length, then ValueError is thrown
        :param max_total_runs: int, {'all_once'} or None,
                               maximum number of total runs for each strategy in FXEngine,
                               maximal number of runs in total over all possible window sizes and samples for each
                               strategy
                               if None, number of total runs will not be constrained (runs simulation on all possible
                                    windows for each given window size/ run length)
                               if 'all_once', each window size/ run length will be run exactly once
                               if int and max_total_runs < number of possible windows (max_window_length
                                    - min_window_length + 1), then some window lengths/ run lengths
                                    will be left out (randomly) such that the number of total runs is close but never
                                    greater than max_total_runs
                               for each strategy in FXEngine
        :param run_through: bool,
                            if True, strategy run is performed once on total data set additionally to sampled data set
                                     specified by param:min_run_length and param:max_run_length
                            if False, only strategy runs on sampled data set specified by param:min_run_length and
                                      param:max_run_length are performed
        :return: run_balances: dict,
                               key: (strategy.name, window_size, start_index)
                               value: [start_balance, end_balance]
                               dictionary holding start and final balance/ total value in param:reference_currency of
                               each run.
                               Each run is defined by strategy, sampling window sized (defined through min_run_length
                               and max_run_length) and start index of random sample (see key).
        :raises: TypeError, if parameters do not match specified types,
                            only thrown if ignore_type_checking is False (type_checking enabled at __init__)
                            (except price_data is None, then TypeError is still thrown regardless of
                             self._ignore_type_checking)
                 ValueError, if length_data <= lookback, min_run_length is less than 1 or
                             if min_run_length is greater than max_run_length (except default value None)
                 IndexError, if dictionary values of param:data (list or 1D-Array) have different lengths,
                            only thrown if ignore_type_checking is False (type_checking enabled at __init__)
                 auto-clean up via self.close() if any exception is thrown internally
        """
        self.reset(delete_dir=False, clean_lookbacks=False, clean_loc_decision_funcs=False)

        # check types
        try:
            check_types([price_data], [dict], ['price_data'], self._ignore_type_checking)
            len_data = len(price_data[list(price_data.keys())[0]])

            if min_run_length is None:
                min_run_length = 1

            if not self._ignore_type_checking:
                check_types([reference_currency, min_run_length, run_through],
                            [str, int, bool],
                            ['reference_currency', 'min_run_length', 'run_through'],
                            self._ignore_type_checking)

                if max_run_length is not None:
                    check_types([max_run_length], [int], ['max_run_length'], self._ignore_type_checking)

                # >>price data
                for k in price_data.keys():
                    check_types([k], [tuple], ['price_data_key'], self._ignore_type_checking)
                    check_types([k[0], k[1]], [str, str], ['price_data_key_tuple_0', 'price_data_key_tuple_1'],
                                self._ignore_type_checking)
                    # sample check
                    check_types([price_data[k][0]], [float], ['data_value'], self._ignore_type_checking)
                    if len(price_data[k]) != len_data:
                        raise IndexError

                # >>volume data
                if volume_data is not None:
                    check_types([volume_data], [dict], ['volume_data'], self._ignore_type_checking)
                    for k in volume_data.keys():
                        check_types([k], [tuple], ['volume_data_key'], self._ignore_type_checking)
                        check_types([k[0], k[1]], [str, str],
                                    ['volume_data_key_tuple_0', 'volume_data_key_tuple_1'],
                                    self._ignore_type_checking)
                        # sample check
                        check_types([volume_data[k][0]], [float], ['volume_data_value'],
                                    self._ignore_type_checking)
                        if len(volume_data[k]) != len_data:
                            raise IndexError

                if max_total_runs != np.inf and max_total_runs is not None and max_total_runs != 'all_once':
                    check_types([max_total_runs], [int], ['max_total_runs'], self._ignore_type_checking)
        except (TypeError, IndexError) as e:
            self._deconstruct_tmp_dir()
            raise e

        self.reference_currency = reference_currency
        self.price_data = price_data
        self.volume_data = volume_data

        try:
            # >>>assemble run_register and job input for parallel pipeline
            job_input = list()
            for i, strategy in enumerate(self.strategies):
                if max_run_length is None:
                    max_run_length = len_data - strategy.lookback
                partition_indices = self._build_partitioning_indices(length_data=len_data,
                                                                     lookback=strategy.lookback,
                                                                     min_window_length=min_run_length,
                                                                     max_window_length=max_run_length,
                                                                     max_total_runs=max_total_runs)
                self.run_register[strategy.name] = partition_indices
                job_input.extend([(i, reference_currency, window_size, start_index)
                                  for (window_size, start_index) in self._iter_partition_indices(partition_indices)])
            if run_through:
                for i, strategy in enumerate(self.strategies):
                    if len_data - strategy.lookback in self.run_register[strategy.name].keys():
                        self.run_register[strategy.name][len_data - strategy.lookback].append('runthrough')
                    else:
                        self.run_register[strategy.name][len_data - strategy.lookback] = ['runthrough']
                    job_input.append((i, reference_currency, len_data - strategy.lookback, 'runthrough'))

            # >>>determine if single process or parallel pipeline shall be used
            if self.n_jobs == 0:
                # >>run single process
                job_result = [self.run_strategy(*i) for i in job_input]
            else:
                # >>calculate max number of jobs in parallel
                if self.n_jobs == -1:
                    num_cores = min(len(job_input), cpu_count())
                else:
                    num_cores = self.n_jobs
                # >>launch parallel joblib pipeline
                job_result = Parallel(n_jobs=num_cores)(delayed(self.run_strategy)(*i) for i in job_input)

            # >>>process results
            strategy_names, window_sizes, start_indices, start_balances, end_balances = zip(*job_result)
            # >>assemble run_balances
            run_balances = dict(zip(zip(strategy_names, window_sizes, start_indices),
                                    zip(start_balances, end_balances)))

            # >>>write to temporary file
            tmp = tempfile.NamedTemporaryFile(prefix='runs-total-balances-start-end_', dir=self._tmp_dir,
                                              mode='w+b', delete=False)
            try:
                pickle.dump(run_balances, tmp, protocol=pickle.HIGHEST_PROTOCOL)
            except PermissionError as pme:
                tmp.close()
                self._deconstruct_tmp_dir()
                raise pme
            tmp.flush()
            tmp.close()

            # reset strategies and accounts but keep temp dir files for later analysis
            for strategy in self.strategies:
                try:
                    strategy.c_reset()
                except AttributeError:
                    strategy.reset()

            self.has_run = True

        except Exception as e:
            self._deconstruct_tmp_dir()
            raise e

        return run_balances

    def register_strategies(self, strategies, loc_decision_functions=False):
        """
        Registers new strategies to Engine. Cleans up before registering.
        Strategies, which have been bound to Engine will be overwritten by newly registered strategies.

        All class attributes will be reset or overwritten except:
            self._ignore_type_checking,
            self._tmp_dir,
            self._is_loaded_from_file (checks if object was loaded from previously saved file,
                                       see self.load() and self.save()),
            self.n_jobs,
            self.name

        :param strategies: list of FXStrategy objects (or objects derived from
                           trapeza.strategy.base_strategy.BaseStrategy)
        :param loc_decision_functions: bool,
                                       if True, line of codes (source file) of decision function of each strategy is
                                                retrieved for later use in dashboard visualization
                                       if False, does not try to read line of codes of decision function

                                       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                                       Be careful using this option, as it exposes code to temporary directory, which
                                       might be readable for third parties (even though tempfile library is used).
                                       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        :return: None
        :raises: TypeError, if parameters do not match specified type
                 auto-clean up via self.close() if any exception is thrown internally
        """
        # leave untouched: self._ignore_type_checking, self._tmp_dir, self._is_loaded_from_file, self.n_jobs, self.name
        self.reset(delete_dir=False, clean_lookbacks=True, clean_loc_decision_funcs=True)

        # holds all strategies to be compared
        self.strategies = None
        try:
            self._check_assign_strategies(strategies)
        except Exception as e:
            self._deconstruct_tmp_dir()
            raise e

        # noinspection PyTypeChecker
        self.lookbacks = {strat.name: strat.lookback for strat in self.strategies}

        self._finalizer = weakref.finalize(self, self._deconstruct_tmp_dir_finalize, self.is_loaded_from_file,
                                           self.from_child, self._tmp_dir)

        # dump line of codes of source files of decision functions of strategies into temporary directory
        if loc_decision_functions:
            try:
                self._tmp_dump_decision_funcs()
            except Exception as e:
                self._deconstruct_tmp_dir()
                raise e

    def close(self):
        """
        Closes Engine and deconstructs temporary directory. It is recommended to use this function explicitly, but
        nevertheless this routine should also execute whenever the class object is garbage collected.
        :return: None
        """
        # tempfile handler are handled at each call to file objects
        # parallelization handlers are handled via joblib
        # pickle is neglectable
        # temporary directory is handled via self._deconstruct_tmp_dir_finalize
        # so call self._finalizer (which handles self._deconstruct_tmp_dir via weakref) or self._deconstruct_tmp_dir
        self._finalizer()

    def load_result(self, strategy_name, window_size=None, start_index=None):
        """
        After FXEngine.run(), results of every simulation run are stored as temporary file within the temporary
        sub-directory under self._tmp_dir. See class description for further details.
        This method is a convenience function for loading results from those temporary files.
        window_size and start_index have to part of the domain of sampled data of self.run(), otherwise there won't be
        a temporary file (which is logically if it hasn't been simulated at self.run()). See self.run() or
        self._build_partitioning_indices for further details regarding how data is sampled.

        :param strategy_name: str,
                              same as FXStrategy.name of strategy, which was passed to FXEngine at __init__
        :param window_size: int or None,
                            window length (which does not need to take lookback size into account)
                            None: defaults to largest window size available in self.run_register, which filled during
                                  self.run()
        :param start_index: int, 'runthrough' or None
                            start index of run (which also includes lookback size)
                            None: defaults either to 'runthrough' if 'runthrough' is present in
                                  self.run_register[strategy_name][window_size], which is filled during self.run(),
                                  or if 'runthrough' is not present, to the minimal start_index in
                                  self.run_register[strategy_name][window_size]
        :return: dict,
                 keys: {'signals', 'positions', 'merged_positions', 'total_balances', 'merged_total_balances'}
                       see FXStrategy for further details
                 values: list of str ('signals') or list of floats (other keys)
        :raises: TypeError, if parameters do not match specified types,
                            only thrown if ignore_type_checking is False (type_checking enabled at __init__)
                 FileNotFoundError if file with specified strategy name, window length and start index cannot be found
                 auto-clean up via self.close() if any exception is thrown internally
        """
        try:
            check_types([strategy_name], [str], ['strategy_name'], self._ignore_type_checking)

            if window_size is None:
                windows = list(map(int, self.run_register[strategy_name].keys()))
                window_size = max(windows)

            if start_index is None:
                start_indices = set(self.run_register[strategy_name][window_size])
                if 'runthrough' in start_indices:
                    start_index = 'runthrough'
                else:
                    start_index = min(start_indices)

            name_set = [strategy_name]
            for fn in os.listdir(self._tmp_dir):
                name_index = find_prefix(name_set, fn)
                if name_index == -1:
                    continue

                fn_split = fn[len(name_set[name_index]) + 1:].split('_')
                win_size = fn_split[0]
                start_ind = fn_split[1]

                if str(window_size) == str(win_size) and str(start_index) == str(start_ind):
                    fn_path = os.path.join(self._tmp_dir, fn)
                    with open(fn_path, 'rb') as fn_inp:
                        results = pickle.load(fn_inp)
                    return results
            raise FileNotFoundError('No temporary file with results for {}, {} and {} '
                                    ' in {} found.'.format(strategy_name, window_size, start_index, self._tmp_dir))
        except Exception as e:
            self._deconstruct_tmp_dir()
            raise e

    def analyze_strategy(self, strategy_name, file_name, window_size, start_index, std_metric_dict, metric_dict):
        """
        Loops through temporary files which contain results of strategy_name and analyzes metric_dict.
        Callables listed in metric_dict must have following call signature:
            float = metric_fnc(merged_total_balances),
            merged_total_balances: see trapeza.strategy.fx_strategy.FXStrategy class
        :param strategy_name: str,
                              name of strategy, which is listed within self.strategies
        :param file_name: str,
                          filename of temporary file, which was created during self.run() and which shall be analysed
                          with respect to param:metric_dict
        :param window_size: int,
                            window size of param:file_name temporary file, see self.run() or class description for
                            further details
        :param start_index: int or 'runthrough',
                            start index at which data is sliced into sample, which was used for param:file_name
                            temporary file during self.run(), see self.run() or class description for
                            further details
       :param std_metric_dict: dict,
                               {metric_name: metric_fnc}, metric_name as str, metric_fnc as callable function
                               standard pre-implemented metrics,
                               see self.analyze or docstring of FXEngine for further details
        :param metric_dict: dict,
                            {metric_name: metric_fnc}, metric_name as str, metric_fnc as callable function
                            metric_fnc call signature:
                                float = metric_fnc(merged_total_balances)
                                merged_total_balances: list, see trapeza.strategy.fx_strategy.FXStrategy class
                            custom metrics
                            see self.analyze or docstring of FXEngine for further details
        :return: strategy_name, window_size, start_index, metric_result, dict_type,
                 strategy_name: see param:strategy_name
                 window_size: see param:window_size
                 start_index: see param:start_index
                 std_metric_result: dict,
                                    key: metric_name from param:metric_dict
                                    value: computed value of metric_fnc from param:metric_dict
                                    pre-implemented metrics
                 metric_result: dict,
                                key: metric_name from param:metric_dict
                                value: computed value of metric_fnc from param:metric_dict
                                custom metrics
        :raises: TypeError, if parameters do not match specified type,
                            only thrown if ignore_type_checking is False (type_checking enabled at __init__)
                 auto-clean up via self.close() if any exception is thrown internally
        TODO: Currently metrics are analyzed on results['merged_total_balances'] of each strategy (see
                 trapeza.strategy.fx_strategy.FXStrategy.merged_total_balances). For more complex metrics,
                 enable analysis on 'merged_positions' as well and not only on 'merged_total_balances' (provided,
                 that there are metrics which need to be analyzed on 'merged_positions').
        """
        try:
            window_size = int(window_size)  # sanity cast
            if not self._ignore_type_checking:
                check_types([file_name, window_size, std_metric_dict, metric_dict],
                            [str, int, dict, dict],
                            ['file_name', 'window_size', 'standard_metric_dict', 'metric_dict'],
                            self._ignore_type_checking)
                check_types(list(metric_dict.values()), [callable for _ in range(len(metric_dict))],
                            list(metric_dict.keys()), self._ignore_type_checking)
                check_types(list(std_metric_dict.values()), [callable for _ in range(len(std_metric_dict))],
                            list(std_metric_dict.keys()), self._ignore_type_checking)
            if start_index != 'runthrough':
                start_index = int(start_index)  # sanity cast
                check_types([start_index], [int], ['start_index'], self._ignore_type_checking)
        except TypeError as type_e:
            self._deconstruct_tmp_dir()
            raise type_e

        try:
            with open(file_name, 'rb') as fn_inp:
                results = pickle.load(fn_inp)

            metric_result = dict()
            for metric_key in metric_dict.keys():
                metric_result[metric_key] = metric_dict[metric_key](results['merged_total_balances'])

            std_metric_result = dict()
            for std_metric_key in std_metric_dict.keys():
                std_metric_result[std_metric_key] = std_metric_dict[std_metric_key](results['merged_total_balances'])
        except Exception as e:
            self._deconstruct_tmp_dir()
            raise e

        return strategy_name, window_size, start_index, std_metric_result, metric_result

    # noinspection DuplicatedCode
    def analyze(self, metric_dict=None):
        """
        Performs analysis by calculating a given set of metrics over all simulation runs performed by self.run() and
        can be used to retrieve statistical insights.

        This methods loads in all temporary files, which have been created during self.run(). Loading results is done
        via searching through temporary directory given by self._tmp_dir. In order to analyse results, self.run() has to
        be called beforehand, otherwise an exception is raised.

        A custom dictionary of metrics can be passed as argument. param:metric must have following signature:
             dictionary keys: str,
                              metric name
             dictionary values: callable function,
                                callable function must have following call signature:

                                    float = metric_fnc(merged_total_balances)

                                    merged_total_balances: list, see trapeza.strategy.fx_strategy.FXStrategy class

        Currently, metrics can only be evaluated on 'merged_total_balances' of each strategy of FXEngine
        (see FXStrategy for further information regarding 'merged_total_balances': FXStrategy.merged_total_balances).

        If param:metric_dict is None, a default metrics dictionary is used:
            {'total_rate_of_return': metric.total_rate_of_return, # total rate of return in percent, not annualized
            'volatility': metric.volatility,   # volatility based on log returns and normal distribution assumption,
                                                  not annualized
            'downside_risk': _downside_risk,    # downside risk, risk-free: 3%, normal distribution assumption
            'value_at_risk': metric.value_at_risk, # value at risk at 95% confidence based on log returns and normal
                                                      distribution assumptions, historic simulation used as computation
                                                      method
            'expected_rate_of_return': _expected_rate_of_return, # expected rate of excess return per time step,
                                                                   risk-free: 3%, based on log return and normal
                                                                   distribution assumption
            'sharpe_ratio': metric.sharpe_ratio,   # sharpe ratio, risk-free: 3%, based on percentage return and
                                                      normal distribution assumption, not annualized
            'sortino_ratio': metric.sortino_ratio, # sortino ratio, risk-free: 3%, based on percentage return and
                                                      normal distribution assumption, not annualized
            'max_drawdown': _std_max_drawdown   # max drawdown
            }
        Results of param:metric_dict are stored in self.analysis_results, which is a dict (keys: strategy names) of
        dict (keys: (window_size, start_index) as strings or ints, values: metric_value):
            self.analysis_results[strategy.name][window_size, start_index] = metric_value
        window_size and start_index are described in docstring of self.run() and in the class description.

        self.run_register gives an overview of all windows and start indices, which were created/ used during
        self.run():
            self.run_register[strategy.name][window_size] = [start_index_0, start_index_1, ...]
            (dict of dict)

        Furthermore, a standard metrics dictionary is used besides the user-specified param:metric_dict:
            {'total_rate_of_return': _std_tot_rate_of_ret,      # annualized total rate of return in percent
            'volatility': _std_annual_vola,   # annualized volatility based on percentage return and normal distribution
            'expected_rate_of_return': _std_annual_exp_rate_of_ret, # expected rate of return per time step, returns are
                                                                      converted to log and converted back to percent
                                                                      after calculating expected rate of log returns,
                                                                      normal distribution is assumed
            'expected_rate_of_log_return': _std_exp_rate_of_log_ret,    # see expected_rate_of_return, but all in logs
            'sharpe_ratio': _std_annual_sharpe, # annualized sharpe ratio, risk-free: 3%, calculations based on
                                                  percentage return and normal distribution assumption
            'sortino_ratio': _std_annual_sortino,   # annualized sortino ratio, risk-free: 3%, calculations based on
                                                      percentage return and normal distribution assumption
            'value_at_risk': _std_var,  # annualized value at risk at 95% confidence level, calculation based on
                                          percentage return and normal distribution assumption, historic simulation used
                                          as computation method
            'max_drawdown': _std_max_drawdown   # maximum drawdown
            }
        The standard metric dict is stored at self.standard_analysis_result and can be accessed in the same way as
        self.analysis_result. It assumes daily data for annualization

        trapeza.metrics implements the most common financial metrics, which are also used in the default
        dicts.

        Analysis results in self.standard_analysis_results and self.analysis_results are used by FXDashboard for
        visualization (even though the main purpose of this library is not to visualize, but lying the basis to perform
        numerical and statistical analysis). Do not overwrite or manipulate data or temporary files manually.
        :param metric_dict: dict,
                            {metric_name: metric_fnc}, metric_name as str, metric_fnc as callable function
                            metric_fnc call signature:
                                float = metric_fnc(merged_total_balances)
                                merged_total_balances: list, see trapeza.strategy.fx_strategy.FXStrategy class
        :return: None
        :raises: TypeError, if parameters do not match specified type,
                            only thrown if ignore_type_checking is False (type_checking enabled at __init__)
                 OperatingError
                 auto-clean up via self.close() if any exception is thrown internally
        TODO: Currently metrics are analyzed on results['merged_total_balances'] of each strategy (see
                 trapeza.strategy.fx_strategy.FXStrategy.merged_total_balances). For more complex metrics,
                 enable analysis on 'merged_positions' as well and not only on 'merged_total_balances' (provided,
                 that there are metrics which need to be analyzed on 'merged_positions').
        """
        # analyze all
        # include specification of metrics and custom metrics

        # >>>type and input checking
        if metric_dict is not None:
            try:
                check_types([metric_dict], [dict], ['metric_dict'], self._ignore_type_checking)
            except TypeError as type_e:
                self._deconstruct_tmp_dir()
                raise type_e
        if self.is_analyzed is True:
            warnings.warn('Strategies have already been analyzed. Use self.analysis_results to access '
                          'analysis results or re-call self.run() with new data.')
            return
        if self.has_run is False:
            self._deconstruct_tmp_dir()
            raise tpz_exception.OperatingError('Strategies have not been run on data. self.run() must be called '
                                               'before calling self.analyze().')

        # >>>define standard metrics dictionary
        def _std_tot_rate_of_ret(data):
            return metric.total_rate_of_return(data, reference='pct_return', period_length=len(data))

        def _std_annual_vola(data):
            return metric.volatility(data, reference='pct_return', prob_model='norm', annualization_factor=252)

        def _std_annual_exp_rate_of_ret(data):
            # noinspection PyProtectedMember
            # converted to pct_ret
            return metric.expected_rate_of_return(np.exp(metric._returns(data, 'log_return')) - 1, 0,
                                                  'norm', 'gaussian', 0.75)

        def _std_exp_rate_of_log_ret(data):
            # noinspection PyProtectedMember
            return metric.expected_rate_of_return(metric._returns(data, 'log_return'), 0, 'norm', 'gaussian', 0.75)

        def _std_annual_sharpe(data):
            return metric.sharpe_ratio(data, annualization_factor=252)

        def _std_annual_sortino(data):
            return metric.sortino_ratio(data, annualization_factor=252)

        def _std_var(data):
            return metric.value_at_risk(data, reference='pct_return', annualization_factor=252)

        def _std_max_drawdown(data):
            return metric.max_drawdown(data)[0]

        standard_metric_dict = {'total_rate_of_return': _std_tot_rate_of_ret, 'volatility': _std_annual_vola,
                                'expected_rate_of_return': _std_annual_exp_rate_of_ret,
                                'expected_rate_of_log_return': _std_exp_rate_of_log_ret,
                                'sharpe_ratio': _std_annual_sharpe, 'sortino_ratio': _std_annual_sortino,
                                'value_at_risk': _std_var, 'max_drawdown': _std_max_drawdown}

        # >>>define default metric dict if none is supplied
        if metric_dict is None:
            def _downside_risk(data):
                # target -> 3% in absolute percent --> daily percent: 0.00011730371383444904
                # log(1.00011730371383444904) = 0.0001172968
                return metric.downside_risk(data, target=0.0001172968, reference='log_return')

            def _expected_rate_of_return(data):
                # target -> 3% in absolute percent --> daily percent: 0.00011730371383444904
                # log(1.00011730371383444904) = 0.0001172968
                # noinspection PyProtectedMember
                return metric.expected_rate_of_return(metric._returns(data, 'log_return'),
                                                      0.0001172968, 'norm', 'gaussian', 0.75)

            metric_dict = {'total_rate_of_return': metric.total_rate_of_return, 'volatility': metric.volatility,
                           'downside_risk': _downside_risk, 'value_at_risk': metric.value_at_risk,
                           'expected_rate_of_return': _expected_rate_of_return, 'sharpe_ratio': metric.sharpe_ratio,
                           'sortino_ratio': metric.sortino_ratio, 'max_drawdown': _std_max_drawdown}

        try:
            # >>>assemble input for parallel pipeline, which consists of all temporary files generated during self.run()
            name_set = [strategy.name for strategy in self.strategies]
            job_input = list()
            for fn in os.listdir(self._tmp_dir):
                name_index = find_prefix(name_set, fn)
                if name_index == -1:
                    continue

                fn_split = fn[len(name_set[name_index]) + 1:].split('_')
                strategy_name = name_set[name_index]
                window_size = fn_split[0]
                start_index = fn_split[1]
                fn_path = os.path.join(self._tmp_dir, fn)

                job_input.append((strategy_name, fn_path, window_size, start_index, standard_metric_dict, metric_dict))

            # >>>determine if single process or parallel pipeline shall be use
            if self.n_jobs == 0:
                # >>run single process
                job_result = [self.analyze_strategy(*i) for i in job_input]
            else:
                # >>calculate max number of jobs in parallel
                if self.n_jobs == -1:
                    num_cores = min(len(job_input), cpu_count())
                else:
                    num_cores = self.n_jobs
                # >>launch parallel joblib pipeline
                job_result = Parallel(n_jobs=num_cores)(delayed(self.analyze_strategy)(*i) for i in job_input)

            # >>>process results
            strategy_names, window_sizes, start_indices, std_metric_results, metric_results = zip(*job_result)
            # >>>assemble results
            for i in range(len(strategy_names)):
                if strategy_names[i] not in self.standard_analysis_results.keys():
                    self.standard_analysis_results[strategy_names[i]] = StringTupleKeyDict(
                        {(str(window_sizes[i]), str(start_indices[i])): std_metric_results[i]})
                else:
                    self.standard_analysis_results[strategy_names[i]][window_sizes[i],
                                                                      start_indices[i]] = std_metric_results[i]

                if strategy_names[i] not in self.analysis_results.keys():
                    self.analysis_results[strategy_names[i]] = StringTupleKeyDict(
                        {(str(window_sizes[i]), str(start_indices[i])): metric_results[i]})
                else:
                    self.analysis_results[strategy_names[i]][window_sizes[i], start_indices[i]] = metric_results[i]

            self.is_analyzed = True
            self.metrics = list(metric_dict.keys())

        except Exception as e:
            self._deconstruct_tmp_dir()
            raise e

    def save(self, pth_dir):
        """
        Saves current FXEngine class object.
        A new sub-directory {pth_dir}/{FXEngine.name}_temp/ will be created, in which all temporary files under
        self._tmp_dir will be copied into (this includes all results from self.run() as well as files that
        e.g. store lookback configuration, etc.). The FXEngine object (self) will be stored as pickle file directly
        under the {pth_dir} directory as {self.name}.pkl. Do not rename any of those files and directories manually
        in order not to break loading routine via self.load()!
        All internal states of the FXEngine will be saved accordingly and are re-loadable via self.load().

        DO ONLY USE UNIQUE NAME_IDs AT FXEngine.__init__() AT SAME pth_dir!!!
        Otherwise, previously saved engines under pth_dir with same engine names will be overwritten!

        If the user wants to reduce the file size of object.pkl, then set FXEngine.price_data=None and
        FXEngine.volume_data=None. Otherwise, data will also be stored within FXEngine object. This is only recommended
        if data is persistently accessible (as results only make sense for a given data set!).

        :param pth_dir: str,
                        directory where to store object.pkl (containing FXEngine object) and where to create a new
                        sub-directory {pth_dir}/temp/ to copy all temporary files
        :return: None
        :raises: TypeError, if pth_dir includes '.', which indicates file instead of path,
                            or if parameters do not match specified types (which is only thrown if ignore_type_checking
                            is False (type_checking enabled at __init__))
                 auto-clean up via self.close() if any exception is thrown internally
        """
        try:
            check_types([pth_dir], [str], ['pth_dir'], self._ignore_type_checking)
        except Exception as e:
            self._deconstruct_tmp_dir()
            raise e

        if '.' in pth_dir:
            self._deconstruct_tmp_dir()
            raise TypeError('Takes path to directory, not file.')

        pth_tmp_dir = '{}/{}_temp/'.format(pth_dir, self.name)
        file_name = '{}/{}.pkl'.format(pth_dir, self.name)

        if not os.path.isabs(pth_tmp_dir):
            pth_tmp_dir = os.path.join(os.getcwd(), pth_tmp_dir)
            file_name = os.path.join(os.getcwd(), file_name)

        tmp_pth = self._tmp_dir
        if not os.path.isabs(tmp_pth):
            tmp_pth = os.path.join(os.getcwd(), tmp_pth)

        try:
            if not os.path.exists(pth_tmp_dir):
                os.makedirs(pth_tmp_dir)
            else:
                for file in os.listdir(pth_tmp_dir):
                    f_name = os.path.join(pth_tmp_dir, os.fsdecode(file))
                    os.remove(f_name)
            for file in os.listdir(tmp_pth):
                f_name = os.path.join(tmp_pth, os.fsdecode(file))
                shutil.copyfile(f_name, os.path.join(pth_tmp_dir, file))
            with open(file_name, 'wb') as out:
                pickle.dump(self, out, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            warnings.warn('Exception during saving. Incomplete save process. '
                          'Corrupted files might be stored erroneously at {}.'.format(pth_dir))
            self._deconstruct_tmp_dir()
            raise e

    def load(self, pth_dir):
        """
        Loads FXEngine object, which was saved via FXEngine.save().
        Use exact same name_id for FXEngine.__init__ and pth_dir, which were used when calling FXEngine.save().
        (pth_dir is the path location, where pickle file and sub-directory, which contains all saved temporary files,
         are located - see self.save() for further information. The pickle file is identified via FXEngine.name,
         respectively the name_id argument at FXEngine.__init__(), which is way, they have to exactly match those of
         the saved engine object)

        If user has cleaned internal data storage of the FXEngine object before saving (in order to decrease file size),
        then manually (!!!) re-load data into FXEngine.price_data=prices and FXEngine.volume_data=volumes (with prices
        and volumes as dictionary from external source, see e.g. FXEngine.run() for further information about data
        format of price_data and volume_data).

        :param pth_dir: str,
                        directory where object.pkl (containing FXEngine object) was stored and where
                        sub-directory {pth_dir}/temp/ was created with all copied temporary files
        :return: None
        :raises: TypeError, if pth_dir includes '.', which indicates file instead of path,
                            or if parameters do not match specified types (which is only thrown if ignore_type_checking
                            is False (type_checking enabled at __init__))
                 auto-clean up via self.close() if any exception is thrown internally
        """
        try:
            check_types([pth_dir], [str], ['pth_dir'], self._ignore_type_checking)
        except Exception as e:
            self._deconstruct_tmp_dir()
            raise e

        if '.' in pth_dir:
            self._deconstruct_tmp_dir()
            raise TypeError('Takes path to directory, not file.')

        file_name = '{}/{}.pkl'.format(pth_dir, self.name)
        original_tmp_dir = self._tmp_dir

        try:
            with open(file_name, 'rb') as inp:
                loaded_object = pickle.load(inp)

            self.strategies = loaded_object.strategies
            self.name = loaded_object.name
            self.lookbacks = loaded_object.lookbacks
            self.reference_currency = loaded_object.reference_currency
            # noinspection PyProtectedMember
            self._tmp_dir = '{}/{}_temp'.format(pth_dir, self.name)
            self.is_analyzed = loaded_object.is_analyzed
            self.analysis_results = loaded_object.analysis_results
            self.standard_analysis_results = loaded_object.standard_analysis_results
            self.metrics = loaded_object.metrics
            self.run_register = loaded_object.run_register
            self.has_run = loaded_object.has_run
            self.price_data = loaded_object.price_data
            self.volume_data = loaded_object.volume_data
            self.is_loaded_from_file = True
        except Exception as e:
            warnings.warn('Not able to load object.')
            self._tmp_dir = original_tmp_dir
            self._deconstruct_tmp_dir()
            raise e

    def __del__(self):
        """
        Call self.close via weakref.finalize if object gets garbage collected
        :return: None
        """
        if hasattr(self, '_tmp_dir') and not self.from_child:
            self._finalizer()
