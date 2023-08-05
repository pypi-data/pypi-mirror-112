import itertools
import datetime

import numpy as np
import pandas as pd
from sklearn.preprocessing import minmax_scale
from sklearn.neighbors import KernelDensity
from matplotlib import cm

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.figure_factory as ff
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly import express as px
from flask import request

from trapeza.engine.base_engine import BaseEngine
from trapeza.dashboard.base_dashboard import BaseDashboard
from trapeza.utils import check_types
from trapeza import metric
from trapeza import exception as tpz_exception


class FXDashboard(BaseDashboard):
    """
    Derived from BaseDashboard class. This implementation is meant to be used with FXEngine and its temporary file
    structure and its class attributes/ internal data structure. In principal (but not guaranteed) this class should
    work with any class objects derived from BaseAccount, BaseStrategy and BaseEngine (even though their might be some
    additional specifics to pay attention to, see docstrings of base classes for further information).

    USES SLOTS: ['engine', 'signal_symbols', '_xx', 'overview_page_layout', 'strategy_page_layout', 'len_data', 'app',
                 'palette']

    The main focus of this library does not lay on visualization than rather enable statistical backtesting.
    Nevertheless, this class provides a basic visualization of customisable metrics. See FXEngine for further details.

    FXEngine has to call FXEngine.run() and FXEngine.analyze() before FXDashboard can be initialized, as FXDashboard
    relies on temporary files and data from FXEngine.

    FXDashboard is implemented via Python Dash library. See Dash and Plotly for further details.

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
        >>  # build visualization
        >>  dashboard = FXDashboard(engine)
        >>
        >>  # open dashboard at Dash port in web browser
        >>  dashboard.run()
        >>
        >>  # do not forget to close engine
        >>  engine.close()

    Dash will provide in a dashboard in the web browser. Port address should be displayed in the console. See Dash for
    further information.

    Furthermore, FXDashboard has some customization options.
        - A dictionary of signal symbols can be passed:
            dict with
                keys: str
                values: tuple(shape, color) with
                    shape: https://plotly.com/python/marker-style/#custom-marker-symbols
                    color: https://htmlcolorcodes.com/color-names/
            FXDashboard tries to perform a substring matching of all keys in all signals emitted by FXEngine's
            strategies. If FXDashboard finds a substring match, the corresponding strategy signal is assigned the
            symbol shape and color of the dictionary's key for visualization in a plotly plot.
            Furthermore, FXDashboard performs a substring match of all currencies (or alternative asset which is the key
            of FXEngine.price_data, see FXEngine for further details regarding data format of FXEngine.price_data)
            in FXEngine.price_data in all signals emitted by FXEngine's strategy. If FXDashboard finds a substring
            match, the corresponding signal will be visualized such that the symbol is placed onto the corresponding
            line trace of the respective currency (or asset or whatever is the key of FXEngine.price_data dictionary)
            within the plotly plot.

            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            !!! signal names, which are appended with FXStrategy.add_signal(), should not contain multiple substrings
                of either currencies (or assets or whatever defines keys of FXEngine.price_data dictionary) nor keys
                of shape defining dictionary (param:signal_symbols at FXDashboard.__init__) !!!
                Recommendation: signal names should be mutual free of substring parts, otherwise they might be
                visualized multiple times at FXDashboard !!!
            !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        - A 1D List of date times can be passed: must be same length as FXEngine.price_data and is then used for the
            x-axis in plotly plots
        - Selection of page layouts: see param:overview_page_layout and param:strategy_page_layout at
            FXDashboard.__init__ toggles how much information is displayed on the dashboard

    Within FXDashboard.run(), debug mode can be toggled. If set to True, FXEngine might run multiple times, but is
    easier to debug as hot reloading is active.

    If FXEngine.volume_data is not None (see FXEngine class description for further details), volume data will be
    visualized as well. If FXEngine.volume_data is None, volume data will simply be ignored.

    FXDashboard provides an "EXIT"-page with exit button, which shuts down the internal dash app server, such that
    subsequent code can be run.

    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    !!! Do not forget to explicitly close FXEngine with FXEngine.close() after using FXDashboard.run() (even though
        FXEngine should be garbage collected automatically) !!!
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    FXDashboard has the following dashboard pages
    (assuming default parameters at FXDashboard.__init__):
        - Overview: displays underlyings' prices, comparison of strategies' performances, metrics defined in the
                    FXEngine standard metrics dict and a distribution of percentage changes of strategies in the given
                    frequency of supplied price data
        - A Page for each Strategy with sub-pages (via dropdown):
            - Metrics: displays underlyings with signals, strategy (merged) positions, strategy performance (indexed to
                       100 base points), distribution of log returns in given frequency of supplied data dependent on
                       'time-being_invested' and FXEngine custom metrics dict as distribution over the multiple runs of
                       FXEngine.run()
            - Runs: displays single run of FXEngine.run() (via dropdown) with underlyings and corresponding strategy
                    signals, strategy (merged) position, strategy performance (indexed to 100 base points) with high
                    water marks and max dropdown (peak and through)

    Besides providing a full dashboard, FXDashboard implements all drawing functions as separate functions, which either
    can return a fully configured plotly figure plot or a list of plotly graphical objects (which can be re-used
    elsewhere).
    """
    __slots__ = ['engine', 'signal_symbols', '_xx', 'overview_page_layout', 'strategy_page_layout', 'len_data', 'app',
                 'palette']

    # noinspection PyProtectedMember
    def __init__(self, fx_engine, signal_symbols=None, date_time=None,
                 overview_page_layout='simple', strategy_page_layout='full'):
        """
        Initializes dashboard object but does not start Dash app server.

        :param fx_engine: FXEngine object (or objects derived from trapeza.engine.base_engine.BaseEngine)
        :param signal_symbols: None or dict
            if dict:
                    dict with
                    keys: str
                    values: tuple(shape, color) with
                        shape: https://plotly.com/python/marker-style/#custom-marker-symbols
                        color: https://htmlcolorcodes.com/color-names/
                FXDashboard tries to perform a substring matching of all keys in all signals emitted by FXEngine's
                strategies. If FXDashboard finds a substring match, the corresponding strategy signal is assigned the
                symbol shape and color of the dictionary's key for visualization in a plotly plot.
                Furthermore, FXDashboard performs a substring match of all currencies (or alternative asset which is the
                key of FXEngine.price_data, see FXEngine for further details regarding data format of
                FXEngine.price_data) in FXEngine.price_data in all signals emitted by FXEngine's strategy.
                If FXDashboard finds a substring match, the corresponding signal will be visualized such that the symbol
                is placed onto the corresponding line trace of the respective currency (or asset or whatever is the key
                of FXEngine.price_data dictionary) within the plotly plot.

                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                !!! signal names, which are appended with FXStrategy.add_signal(), should not contain multiple
                    substrings of either currencies (or assets or whatever defines keys
                    of FXEngine.price_data dictionary) nor keys of shape defining dictionary (param:signal_symbols at
                    FXDashboard.__init__) !!!
                    Recommendation: signal names should be mutual free of substring parts, otherwise they might be
                    visualized multiple times at FXDashboard !!!
                !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            if None: signals of strategies of FXEngine will not be visualized
        :param date_time: None or 1D list, numpy array, pandas dataframe or pandas series of tick labels for x axis
                          if None, x axis is labeled with numbers starting from 0 (reaching up to max index of given
                            data set or sub-sample of data, see FXEngine class description for data sampling during
                            backtesting)
                          if not None: must be same length as FXEngine.price_data values and all elements must be of
                                       type:
                                        datetime.date, datetime.datetime, datetime.time, datetime.timedelta,
                                        numpy.datetime64, numpy.timedelta64,
                                        pandas.Timestamp, pandas.datetime, pandas.DatetimeIndex, pandas.Timedelta or
                                        pandas.TimedeltaIndex
                                       plotly is somehow quite tedious regarding acceptable time formats
        :param overview_page_layout: str, {'simple', 'full'},
                                     simple: only results/ metrics from the run with the larges window length will be
                                             displayed (maximal number of time steps, see FXEngine for further details)
                                     full: results/ metrics from all runs will be displayed
        :param strategy_page_layout: str, {'simple', 'full'}
                                     simple: simple histograms
                                     full: stacked histograms per window length of runs generated during FXEngine.run()
                                           overlaid with approximated probability density function
        :return: None
        :raises: trapeza.exceptions.OperatingError, if FXEngine has not called FXEngine.analyze() before initializing
                                                  FXDashboard
                 trapeza.exceptions.StrategyError, if param:fx_engine does not inherit from
                                                   trapeza.engine.base_engine.BaseEngine
                 ValueError, if param:overview_page_layout or param:strategy_page_layout not in {'simple', 'full'}
                 TypeError, if parameters do not match specified types
                 if exception is raised, FXEngine will be automatically closed (including its clean up routine)
        """
        super().__init__()

        # check inheritance
        if not issubclass(fx_engine.__class__, BaseEngine):
            raise tpz_exception.StrategyError(fx_engine, 'Engine has to inherit from '
                                                         'trapeza.engine.base_engine.BaseEngine.')

        self.engine = fx_engine

        # check if engine is already analyzed
        if self.engine.is_analyzed is False:
            self.engine.close()
            raise tpz_exception.OperatingError('Strategies have not been analyzed.')

        # check types
        try:
            check_types([overview_page_layout, strategy_page_layout],
                        [str, str],
                        ['overview_page_layout', 'strategy_page_layout'])
            if date_time is not None:
                if type(date_time) is list:
                    if (type(date_time[0]) is datetime.date
                            or type(date_time[0]) is datetime.time
                            or type(date_time[0]) is datetime.timedelta
                            or type(date_time[0]) is np.datetime64
                            or type(date_time[0]) is np.timedelta64
                            or type(date_time[0]) is pd.Timestamp
                            or type(date_time[0]) is pd.datetime
                            or type(date_time[0]) is pd.DatetimeIndex
                            or type(date_time[0]) is pd.Timedelta
                            or type(date_time[0]) is pd.TimedeltaIndex):
                        pass
                    else:
                        raise TypeError('date_time must be list of datetime objects, numpy array of dtype="datetime64" '
                                        'or pandas DataFrame containing Timestamp.')
                elif type(date_time) is np.ndarray:
                    if (type(date_time[0]) is datetime.date
                            or type(date_time[0]) is datetime.time
                            or type(date_time[0]) is datetime.timedelta
                            or type(date_time[0]) is np.datetime64
                            or type(date_time[0]) is np.timedelta64
                            or type(date_time[0]) is pd.Timestamp
                            or type(date_time[0]) is pd.datetime
                            or type(date_time[0]) is pd.DatetimeIndex
                            or type(date_time[0]) is pd.Timedelta
                            or type(date_time[0]) is pd.TimedeltaIndex):
                        pass
                    else:
                        raise TypeError('date_time must be list of datetime objects, numpy array of dtype="datetime64" '
                                        'or pandas DataFrame containing Timestamp.')
                elif isinstance(date_time, pd.DataFrame) or isinstance(date_time, pd.Series):
                    if (type(date_time[0]) is datetime.date
                            or type(date_time[0]) is datetime.time
                            or type(date_time[0]) is datetime.timedelta
                            or type(date_time[0]) is np.datetime64
                            or type(date_time[0]) is np.timedelta64
                            or type(date_time[0]) is pd.Timestamp
                            or type(date_time[0]) is pd.datetime
                            or type(date_time[0]) is pd.DatetimeIndex
                            or type(date_time[0]) is pd.Timedelta
                            or type(date_time[0]) is pd.TimedeltaIndex):
                        pass
                    else:
                        raise TypeError('date_time must be list of datetime objects, numpy array of dtype="datetime64" '
                                        'or pandas DataFrame containing Timestamp.')
                else:
                    raise TypeError('date_time must be list of datetime objects, numpy array of dtype="datetime64" '
                                    'or pandas DataFrame containing Timestamp.')
            if signal_symbols is not None:
                check_types([signal_symbols], [dict], ['signal_symbols'])
        except TypeError as type_e:
            self.engine.close()
            raise type_e

        # check string kwargs
        if overview_page_layout not in ['simple', 'full']:
            self.engine.close()
            raise ValueError('overview_page_layout must be {simple, full}')
        if strategy_page_layout not in ['simple', 'full']:
            self.engine.close()
            raise ValueError('strategy_page_layout must be {simple, full}')

        # assign internal variables
        self.len_data = len(list(self.engine.price_data.values())[0])
        if date_time is None:
            self._xx = np.arange(start=0, stop=self.len_data)
        elif type(date_time) is list:
            self._xx = np.array(date_time)
        else:
            self._xx = date_time    # that is the case if numpy array or pandas DataFrame
        self.signal_symbols = signal_symbols
        self.overview_page_layout = overview_page_layout
        self.strategy_page_layout = strategy_page_layout
        self.app = None
        color_cycle = itertools.cycle(px.colors.qualitative.Plotly)
        self.palette = {k: next(color_cycle) for k in self.engine.price_data.keys()}

    def max_window_min_start_index(self, strategy_name):
        """
        Get max window and min start index from FXEngine.run_register[strategy_name]
        :param strategy_name: str
        :return: _max_window: int (might be formatted as str though...)
                 _min_index: int or 'runthrough'
        """
        _max_window = np.max(list(self.engine.run_register[strategy_name].keys()))
        _indices = set(self.engine.run_register[strategy_name][_max_window])
        if 'runthrough' in _indices:
            _min_index = 'runthrough'
        else:
            _indices = [i for i in _indices if type(i) is not str]
            _min_index = np.min(_indices)
        return _max_window, _min_index

    # noinspection PyProtectedMember
    def load_result(self, strategy_name, window=None, index=None):
        """
        Wrapper for FXEngine.load_result() which parses param:strategy_name to the right string format.
        :param strategy_name: str, path via Dash application
        :param window: see FXEngine.load_result()
        :param index: see FXEngine.load_result()
        :return: see FXEngine.load_result()
        :raises: see FXEngine.load_result()
        """
        strategy_name = strategy_name.replace('%20', ' ')
        return self.engine.load_result(strategy_name, window, index)

    # noinspection DuplicatedCode
    def draw_volumes(self, from_index=0, to_index=-1, return_type='fig'):
        """
        Draws FXEngine.volume_data
        :param from_index: int,
                           start index, from which to start plotting volume data
        :param to_index: int,
                         end index (not included), to which to end plotting volume data
        :param return_type: str, {'fig', 'go'}
                            'go': list of plotly graphical objects, each key in FXEngine.volume_data (see FXEngine for
                                  data format) is turned into a separate go.Bar object and enlisted in return value
                            'fig': a single plotly figure will be returned, which additionally updates figure style
        :return: see return_type
        :raises: NotImplementedError, if param:return_type not in {'fig', go'}
                 if exception is raised, FXEngine will be automatically closed (including its clean up routine)
        """
        # figure for volumes
        _scatter = list()
        price_keys = set(self.engine.price_data.keys())
        for key in self.engine.volume_data.keys():
            if to_index == -1:
                to_index = self.len_data
            if key in price_keys:
                _scatter.append(go.Bar(x=self._xx[from_index:to_index],
                                       y=self.engine.volume_data[key][from_index:to_index],
                                       name='{}|{} volume'.format(key[0], key[1]), marker_color=self.palette[key]))
            else:
                _scatter.append(go.Bar(x=self._xx[from_index:to_index],
                                       y=self.engine.volume_data[key][from_index:to_index],
                                       name='{}|{} volume'.format(key[0], key[1])))

        if return_type == 'go':
            return _scatter
        elif return_type == 'fig':
            _fig_volumes = go.Figure()
            for _scatter_i in _scatter:
                _fig_volumes.add_trace(_scatter_i)
            _fig_volumes.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            return _fig_volumes
        else:
            self.engine.close()
            raise NotImplementedError('return_type={fig, go}')

    # noinspection PyProtectedMember
    def draw_underlyings(self, from_index=0, to_index=-1, return_type='fig'):
        """
        Draws FXEngine.price_data
        :param from_index: int,
                           start index, from which to start plotting price data
        :param to_index: int,
                         end index (not included), to which to end plotting price data
        :param return_type: str, {'fig', 'go'}
                            'go': list of plotly graphical objects, each key in FXEngine.price_data (see FXEngine for
                                  data format) is turned into a separate go.Scatter object and enlisted in return value
                            'fig': a single plotly figure will be returned, which additionally updates figure style and
                                   adds in volume data from self.draw_volumes() if FXEngine.volume_data is not None
        :return: see return_type
        :raises: NotImplementedError, if param:return_type not in {'fig', go'}
                 if exception is raised, FXEngine will be automatically closed (including its clean up routine)
        """
        # figure for underlyings
        _scatter = list()
        for key in self.engine.price_data.keys():
            if to_index == -1:
                to_index = self.len_data
            _scatter.append(go.Scatter(x=self._xx[from_index:to_index],
                                       y=self.engine.price_data[key][from_index:to_index],
                                       name='{}|{}'.format(key[0], key[1]), marker_color=self.palette[key]))
        if return_type == 'go':
            return _scatter
        elif return_type == 'fig':
            if self.engine.volume_data is not None:
                _go_volumes = self.draw_volumes(from_index, to_index, return_type='go')
                _fig_underlyings = make_subplots(rows=2, cols=1, vertical_spacing=0.02, horizontal_spacing=0.009)
            else:
                _fig_underlyings = go.Figure()

            for _scatter_i in _scatter:
                _fig_underlyings.add_trace(_scatter_i)

            if self.engine.volume_data is not None:
                # noinspection PyUnboundLocalVariable
                for _bar_i in _go_volumes:
                    _fig_underlyings.add_trace(_bar_i, row=2, col=1)

            _fig_underlyings.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            return _fig_underlyings
        else:
            self.engine.close()
            raise NotImplementedError('return_type={fig, go}')

    # noinspection PyProtectedMember,DuplicatedCode
    def draw_strategy_signals(self, str_strategy, win_len, start_ind, return_type='fig'):
        """
        Draws strategy signals of FXStrategy, which are part of FXEngine

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!! signal names, which are appended with FXStrategy.add_signal(), should not contain multiple
            substrings of either currencies (or assets or whatever defines keys
            of FXEngine.price_data dictionary) nor keys of shape defining dictionary (param:signal_symbols at
            FXDashboard.__init__) !!!
            Recommendation: signal names should be mutual free of substring parts, otherwise they might be
            visualized multiple times at FXDashboard !!!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        For further information, see FXDashboard class description.

        :param str_strategy: str, strategy name
        :param win_len: int, window length (see FXEngine)
        :param start_ind: int or 'runthrough' (see FXEngine)
        :param return_type: str, {'fig', 'go'}
                            'go': list of plotly graphical objects go.Scatter, wherein each go.Scatter contains each
                                  unique set of the total set of all signals of given strategy of FXEngine
                            'fig': a single plotly figure will be returned, which additionally updates figure style
        :return: see return_type
        :raises: NotImplementedError, if param:return_type not in {'fig', go'}
                 if exception is raised, FXEngine will be automatically closed (including its clean up routine)
        """
        _signals = self.load_result(str_strategy, win_len, start_ind)['signals']
        _scatter = list()

        if start_ind == 'runthrough':
            start_ind = 0
        start_ind = int(start_ind)

        _all_legend_groups = np.array([], dtype='object')
        _all_colors = np.array([], dtype='object')
        _all_symbols = np.array([], dtype='object')
        _all_x = np.array([], dtype=np.float)
        _all_y = np.array([], dtype=np.float)

        for _i, _signals_t in enumerate(_signals):
            for _signals_t_acc in _signals_t:
                if len(_signals_t_acc) == 0:
                    continue
                _signals_t_acc = np.array(_signals_t_acc)
                _colors = np.array(_signals_t_acc, dtype='object')
                _symbols = np.array(_signals_t_acc, dtype='object')
                _legend_group = np.array(_signals_t_acc)
                _y = np.zeros((len(_colors),))
                _x = np.array([_i + self.engine.lookbacks[str_strategy] + start_ind for _ in range(len(_colors))])

                # check for exact match
                for dict_key in self.signal_symbols.keys():
                    _colors[_signals_t_acc == dict_key] = self.signal_symbols[dict_key][1]
                    _symbols[_signals_t_acc == dict_key] = self.signal_symbols[dict_key][0]
                    _legend_group[_signals_t_acc == dict_key] = dict_key

                # check for partial match
                for dict_key in self.signal_symbols.keys():
                    _colors[(_signals_t_acc != dict_key)
                            & np.flatnonzero(np.core.defchararray.find(_signals_t_acc, dict_key) != -1)] \
                        = self.signal_symbols[dict_key][1]
                    _symbols[(_signals_t_acc != dict_key)
                             & np.flatnonzero(np.core.defchararray.find(_signals_t_acc, dict_key) != -1)] \
                        = self.signal_symbols[dict_key][0]
                    _legend_group[(_signals_t_acc != dict_key)
                                  & np.flatnonzero(np.core.defchararray.find(_signals_t_acc, dict_key) != -1)] \
                        = dict_key

                # default colors and symbols
                _colors[_colors == _signals_t_acc] = 'Black'
                _symbols[_symbols == _signals_t_acc] = 'circle'

                # get positions
                for _underlying in set(itertools.chain(*self.engine.price_data.keys())):
                    if ((_underlying, self.engine.reference_currency) in self.engine.price_data.keys()
                            and (_underlying != self.engine.reference_currency)):
                        _ref_key = (_underlying, self.engine.reference_currency)
                    elif _underlying != self.engine.reference_currency:
                        _ref_key = (self.engine.reference_currency, _underlying)
                    else:
                        continue
                    _y[np.flatnonzero(np.char.find(_signals_t_acc, _underlying) != -1) &
                       np.flatnonzero(np.char.find(_signals_t_acc, self.engine.reference_currency) != -1)] \
                        = self.engine.price_data[_ref_key][_i + start_ind + self.engine.lookbacks[str_strategy]]

                assert len(_y) == len(_x) == len(_colors) == len(_legend_group) == len(_symbols)

                # add to drawing frame
                _all_x = np.concatenate([_all_x, _x])
                _all_y = np.concatenate([_all_y, _y])
                _all_colors = np.concatenate([_all_colors, _colors])
                _all_symbols = np.concatenate([_all_symbols, _symbols])
                _all_legend_groups = np.concatenate([_all_legend_groups, _legend_group])

        unique_legends = np.unique(_all_legend_groups)
        for u_legend in unique_legends:
            _scatter.append(go.Scatter(x=self._xx[_all_x[_all_legend_groups == u_legend].astype(np.int)],
                                       y=_all_y[_all_legend_groups == u_legend],
                                       mode='markers',
                                       marker=dict(color=_all_colors[_all_legend_groups == u_legend],
                                                   symbol=_all_symbols[_all_legend_groups == u_legend],
                                                   size=np.array([10 for _ in range(len(
                                                       _all_x[_all_legend_groups == u_legend]))]),
                                                   opacity=np.array([0.7 for _ in range(len(
                                                       _all_x[_all_legend_groups == u_legend]))])),
                                       name=u_legend))

        if return_type == 'go':
            return _scatter
        elif return_type == 'fig':
            _fig_signals = go.Figure()
            for _scatter_i in _scatter:
                _fig_signals.add_trace(_scatter_i)
            _fig_signals.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            return _fig_signals
        else:
            self.engine.close()
            raise NotImplementedError('return_type={fig, go}')

    # noinspection PyProtectedMember
    def draw_strategy_performance(self, str_strategy, win_len, start_ind, return_type='fig'):
        """
        Draws strategy performance, which is indexed to 100 base points at time step 0 of each run of FXEngine.run()
        :param str_strategy: str, strategy name
        :param win_len: int, window length (see FXEngine)
        :param start_ind: int or 'runthrough' (see FXEngine)
        :param return_type: str, {'fig', 'go'}
                            'go': list of plotly graphical objects go.Scatter, wherein each go.Scatter contains the
                                  strategy performance (indexed to 100 base points) time series of given strategy in
                                  FXEngine
                            'fig': a single plotly figure will be returned, which additionally updates figure style and
                                   adds high water marks, horizontal line at 100 base points and max drawdown
        :return: see return_type
        :raises: NotImplementedError, if param:return_type not in {'fig', go'}
                 if exception is raised, FXEngine will be automatically closed (including its clean up routine)
        """
        # load temp file holding results
        _results = self.load_result(str_strategy, win_len, start_ind)
        _performance = (np.array(_results['merged_total_balances']) * 100) / _results['merged_total_balances'][0]

        if start_ind == 'runthrough':
            start_ind = 0
        start_ind = int(start_ind)
        win_len = int(win_len)

        # make scatter plot object
        _scatter = go.Scatter(x=self._xx[start_ind + self.engine.lookbacks[str_strategy]:
                                         start_ind + self.engine.lookbacks[str_strategy] + win_len],
                              y=_performance, name=str_strategy)

        if return_type == 'go':
            return _scatter
        elif return_type == 'fig':
            _fig_performance = go.Figure()

            # add strategy performance to plot
            _fig_performance.add_trace(_scatter)
            _fig_performance.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                           legend_title='strategy')
            _fig_performance.add_hline(100, line=dict(color='Black', dash='dot', width=1))
            _water_marks = metric.high_water_marks(_results['merged_total_balances'])[1]
            _x_water_marks = self._xx[_water_marks + self.engine.lookbacks[str_strategy] + start_ind]
            if len(_x_water_marks) == 1:
                _x_water_marks = [_x_water_marks]
            _fig_performance.add_trace(go.Scatter(x=_x_water_marks,
                                                  y=_performance[_water_marks], mode='markers',
                                                  marker=dict(color='Black', size=5, symbol='x', opacity=0.5),
                                                  name='High Water Mark'))
            _mdd = metric.max_drawdown(_results['merged_total_balances'])
            _mdd_peak = _mdd[1]
            _mdd_through = _mdd[2]
            if _mdd_peak is not None:
                _fig_performance.add_trace(go.Scatter(x=[self._xx[_mdd_peak + self.engine.lookbacks[str_strategy]
                                                                  + start_ind]],
                                                      y=[_performance[_mdd_peak]], mode='markers',
                                                      marker=dict(color='Blue'), name='Max Drawdown Peak'))
                _fig_performance.add_trace(go.Scatter(x=[self._xx[_mdd_through + self.engine.lookbacks[str_strategy]
                                                                  + start_ind]],
                                                      y=[_performance[_mdd_through]], mode='markers',
                                                      marker=dict(color='Red'), name='Max Drawdown Through'))
            return _fig_performance
        else:
            self.engine.close()
            raise NotImplementedError('return_type={fig, go}')

    # noinspection PyProtectedMember
    def draw_strategy_composition(self, str_strategy, _win_len, _start_index, return_type='fig'):
        """
        Draws strategy positions (if strategy contains multiple accounts, similar positions will be merged to one
        position over all accounts, see FXStrategy) in reference_currency of FXEngine, which is set at FXEngine.run(),
        as stacked bars
        :param str_strategy: str, strategy name
        :param _win_len: int, window length (see FXEngine)
        :param _start_index: int or 'runthrough' (see FXEngine)
        :param return_type: str, {'fig', 'go'}
                            'go': list of plotly graphical objects go.Scatter, wherein each go.Scatter contains the
                                  time series of each merged position of given strategy of FXEngine
                            'fig': a single plotly figure will be returned, which additionally updates figure style and
                                   adds total strategy value (sum of all positions) on top as line
        :return: see return_type
        :raises: NotImplementedError, if param:return_type not in {'fig', go'}
                 if exception is raised, FXEngine will be automatically closed (including its clean up routine)
        TODO: potential precision loss at inverting exchange rates:
                _exchange_rate = 1 / np.array(
                        self.engine.price_data[self.engine.reference_currency, _symbol]
                        [_start_index + self.engine.lookbacks[str_strategy]:
                         _start_index + self.engine.lookbacks[str_strategy] + _win_len], dtype=np.float64)
        """
        _result = self.load_result(str_strategy, _win_len, _start_index)
        _scatter = []

        if _start_index == 'runthrough':
            _start_index = 0
        _win_len = int(_win_len)

        for _symbol in _result['merged_positions'].keys():
            if _symbol != self.engine.reference_currency:
                if (_symbol, self.engine.reference_currency) in self.engine.price_data.keys():
                    _exchange_rate = np.array(
                        self.engine.price_data[_symbol, self.engine.reference_currency]
                        [_start_index + self.engine.lookbacks[str_strategy]:
                         _start_index + self.engine.lookbacks[str_strategy] + _win_len], dtype=np.float64)
                elif (self.engine.reference_currency, _symbol) in self.engine.price_data.keys():
                    _exchange_rate = 1 / np.array(
                        self.engine.price_data[self.engine.reference_currency, _symbol]
                        [_start_index + self.engine.lookbacks[str_strategy]:
                         _start_index + self.engine.lookbacks[str_strategy] + _win_len], dtype=np.float64)
                else:
                    self.engine.close()
                    raise KeyError('{}|{} or {}|{} are not included in '
                                   'exchange_rates.'.format(_symbol, self.engine.reference_currency,
                                                            self.engine.reference_currency, _symbol))
                # check if base|quote == 1 / quote|base (see _exchange_rate) --> is already checked in strategy.run
                _y = _result['merged_positions'][_symbol] * _exchange_rate
                _scatter.append(go.Scatter(x=self._xx[self.engine.lookbacks[str_strategy] + _start_index:
                                                      _start_index + self.engine.lookbacks[str_strategy] + _win_len],
                                           y=_y, mode='lines', stackgroup='one', name=_symbol))
            else:
                _y = _result['merged_positions'][_symbol]
                _scatter.append(go.Scatter(x=self._xx[self.engine.lookbacks[str_strategy] + _start_index:
                                                      _start_index + self.engine.lookbacks[str_strategy] + _win_len],
                                           y=_y, mode='lines', stackgroup='one', name=_symbol))
        if return_type == 'go':
            return _scatter
        elif return_type == 'fig':
            _fig_comp = go.Figure()
            for _scatter_i in _scatter:
                _fig_comp.add_trace(_scatter_i)
            _fig_comp.add_trace(go.Scatter(x=self._xx[self.engine.lookbacks[str_strategy] + _start_index:
                                                      _start_index + self.engine.lookbacks[str_strategy] + _win_len],
                                           y=np.array(_result['merged_total_balances']), name='total',
                                           line=dict(dash='dot', color='rgb(228, 26, 28)')))
            _fig_comp.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    legend_title='assets')
            return _fig_comp
        else:
            self.engine.close()
            raise NotImplementedError('return_type={fig, go}')

    # noinspection PyProtectedMember
    def draw_strategy_metric_yield(self, str_strategy, str_metric, return_type='fig'):
        """
        Draws distribution of param:str_metric (e.g. expected log returns) dependent on 'time-being-invested' in the
        same frequency as the frequency within given FXEngine.price_data, which can be interpreted as yield curve.

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        str_metric must be a key in FXEngine.standard_analysis_results dictionary (which describes a given
        metric and its calculation function, see FXEngine.analyze() for further details)
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        :param str_strategy: str, strategy name
        :param str_metric: str, key describing metric in FXEngine.standard_analysis_results dictionary !!!
        :param return_type: str, {'fig', 'go'}
                            'go': list of plotly graphical objects, with
                                at index [0]: go.Scatter for min value of all runs for each window length of
                                              FXEngine.run()
                                at index [1]: go.Scatter for max value of all runs for each window length of
                                              FXEngine.run()
                                at index [2]: go.Scatter for average value over all runs for each window length of
                                              FXEngine.run()
                            'fig': a single plotly figure will be returned, which additionally updates figure style and
                                   dotted line for annual compounded 3% value visualized for reference
        :return: see return_type
        :raises: NotImplementedError, if param:return_type not in {'fig', go'}
                 if exception is raised, FXEngine will be automatically closed (including its clean up routine)
        """
        _list_mean = list()
        _list_max = list()
        _list_min = list()

        _win_lens = np.array(list(self.engine.run_register[str_strategy].keys()))
        for _win_len in _win_lens:
            _vals = list()
            for _start_index in self.engine.run_register[str_strategy][_win_len]:
                _vals.append(self.engine.standard_analysis_results[str_strategy][str(_win_len), str(_start_index)]
                             [str_metric])
            _list_mean.append(np.mean(_vals))
            _list_max.append(np.max(_vals))
            _list_min.append(np.min(_vals))

        _scatter = [go.Scatter(x=_win_lens, y=np.array(_list_min), name='min', mode='lines',
                               line=dict(dash='dot', color='rgb(128, 177, 211)')),
                    go.Scatter(x=_win_lens, y=np.array(_list_max), name='max', mode='lines',
                               line=dict(dash='dot', color='rgb(128, 177, 211)'), fill='tonexty'),
                    go.Scatter(x=_win_lens, y=np.array(_list_mean), name='avg', mode='lines',
                               line=dict(color='rgb(128, 177, 211)'), fill=None)]
        if return_type == 'fig':
            _fig_yield = go.Figure(_scatter[0])
            _fig_yield.add_trace(_scatter[1])
            _fig_yield.add_trace(_scatter[2])
            _fig_yield.add_trace(go.Scatter(x=_win_lens, y=[0.0296 / 252 for _ in _win_lens],
                                            name='annual compounded <br>to 3% (0.000117297)',
                                            mode='lines', line=dict(color='Black', dash='dot', width=1), fill=None))
            _fig_yield.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            return _fig_yield
        elif return_type == 'go':
            return _scatter
        else:
            self.engine.close()
            raise NotImplementedError('return_type={fig, go}')

    # noinspection PyProtectedMember
    def draw_strategy_metric_stacked_hist(self, str_strategy, str_metric, res_dict, return_type='fig'):
        """
        Draws stacked histograms for custom metric dictionary of FXEngine, see FXEngine.analyze() for further details.
        Stacking is done for every window length of FXEngine.run().

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        str_metric must be a key in res_dict, which is either FXEngine.standard_analysis_result dict or
        FXEngine.analysis_result dict (str_metric describes a given metric and its calculation function,
        see FXEngine.analyze() for further details)
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        :param str_strategy: str, strategy name
        :param str_metric: str, key describing metric in param:res_dict, which is either standardized
                           FXEngine.standard_analysis_result dict or custom FXEngine.analysis_result dict
        :param res_dict: dict,
                         either standardized FXEngine.standard_analysis_result dict
                         or custom FXEngine.analysis_result dict
        :param return_type: str, {'fig', 'go'}
                            'go': list of plotly graphical objects, with stacked histograms for each metric in
                                  param:res_dict for each window length of FXEngine.run() (see FXEngine.run() for
                                  further details)
                            'fig': a single plotly figure will be returned, which additionally updates figure style,
                                   approximated probability density function, ruge plot and vertical line at mean values
        :return: see return_type
        :raises: NotImplementedError, if param:return_type not in {'fig', go'}
                 if exception is raised, FXEngine will be automatically closed (including its clean up routine)
        """
        _data_metric = list()
        _win_lens = np.array(list(self.engine.run_register[str_strategy].keys()))
        for _win_len in _win_lens:
            _vals = list()
            for _start_index in self.engine.run_register[str_strategy][_win_len]:
                _vals.append(res_dict[str_strategy][str(_win_len), str(_start_index)][str_metric])
            _data_metric.append(_vals)
        color_blues = cm.get_cmap('Blues', len(_win_lens))

        def get_rgb_string(value_float):
            """
            Helper function to get rgb values from single float value
            :param value_float: float
            :return: array with shape: (3,) to corresponding rgb values
            """
            rgb = np.array(color_blues(value_float)[:3]) * 100
            rgb = np.round(rgb)
            return rgb

        _hist = [go.Histogram(x=_data_metric[i], name=str(_win_lens[i]), opacity=0.75,
                              marker=dict(color='rgb({},{},{})'.format(*get_rgb_string(i / len(_win_lens)))))
                 for i in range(len(_data_metric))]

        if return_type == 'go':
            return _hist
        elif return_type == 'fig':
            _fig_hist = make_subplots(specs=[[{"secondary_y": True}]])
            for n, _trace in enumerate(_hist):
                _fig_hist.add_trace(_trace)
            _data = np.concatenate(_data_metric).reshape(-1)
            _data = np.nan_to_num(_data, posinf=np.nanmax(_data), neginf=np.nanmax(_data))
            _kde = KernelDensity(kernel='gaussian', bandwidth=0.25).fit(_data.reshape(-1, 1))
            _x_d = np.linspace(start=np.min(_data), stop=np.max(_data), num=len(_data) * 10)
            _dens = np.exp(_kde.score_samples(_x_d.reshape(-1, 1)))
            _fig_hist.add_trace(go.Scatter(x=_x_d, y=np.array(_dens), mode='lines',
                                           line=dict(color='Black', dash='dot', width=1),
                                           name='kernel density estimation'),
                                secondary_y=True)
            _fig_hist.add_trace(go.Scatter(x=_data, y=-1 - 1.5 * np.random.random(_data.shape[0]), mode='markers',
                                           marker=dict(color='Black', symbol='x'), showlegend=False))
            _fig_hist.add_vline(np.mean(_data), line=dict(color='Red', dash='dot', width=1))
            _fig_hist.update_yaxes(title_text='absolute frequency', secondary_y=False, tickformat='.1r')
            _range_min = np.min(_dens) - 0.1 * np.abs(np.min(_dens))
            _range_max = np.max(_dens) + 0.1 * np.abs(np.min(_dens))
            _fig_hist.update_yaxes(title_text='probability density', secondary_y=True, tickformat='.3r',
                                   range=[_range_min, _range_max])
            _fig_hist.update_layout(barmode='stack', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                    legend_title='simulated window length')
            return _fig_hist
        else:
            self.engine.close()
            raise NotImplementedError('return_type={fig, go}')

    def draw_strategy_metric_simple_hist(self, str_strategy, str_metric, res_dict, return_type='fig'):
        """
        Draws simple histograms for custom metric dictionary of FXEngine, see FXEngine.analyze() for further details.
        No stacking applied, histograms are taken over all windows of FXEngine.run() results.

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        str_metric must be a key in res_dict, which is either FXEngine.standard_analysis_result dict or
        FXEngine.analysis_result dict (str_metric describes a given metric and its calculation function,
        see FXEngine.analyze() for further details)
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        :param str_strategy: str, strategy name
        :param str_metric: str, key describing metric in param:res_dict, which is either standardized
                           FXEngine.standard_analysis_result dict or custom FXEngine.analysis_result dict
        :param res_dict: dict,
                         either standardized FXEngine.standard_analysis_result dict
                         or custom FXEngine.analysis_result dict
        :param return_type: str, {'fig', 'go'}
                            'go': list of plotly graphical objects, with simple histograms for each metric in
                                  param:res_dict over all window lengths of FXEngine.run() (see FXEngine.run() for
                                  further details)
                            'fig': a single plotly figure will be returned, which additionally updates figure style
                                   and vertical line at mean values
        :return: see return_type
        :raises: NotImplementedError, if param:return_type not in {'fig', go'}
                 if exception is raised, FXEngine will be automatically closed (including its clean up routine)
        """
        _data_metric = list()
        _win_lens = np.array(list(self.engine.run_register[str_strategy].keys()))
        for _win_len in _win_lens:
            for _start_index in self.engine.run_register[str_strategy][_win_len]:
                _data_metric.append(res_dict[str_strategy][str(_win_len), str(_start_index)][str_metric])
        _hist = go.Histogram(x=_data_metric, name=str_metric, marker=dict(color='rgb(128, 177, 211)'))

        if return_type == 'go':
            return _hist
        elif return_type == 'fig':
            _fig_hist = go.Figure()
            _fig_hist.add_trace(_hist)
            _fig_hist.add_vline(np.mean(_data_metric), line=dict(color='Red', dash='dot', width=1))
            _fig_hist.update_layout(barmode='stack', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            return _fig_hist
        else:
            # noinspection PyProtectedMember
            self.engine.close()
            raise NotImplementedError('return_type={fig, go}')

    # noinspection PyProtectedMember
    def page_overview(self):
        """
        Defines page 'Overview'.
        :return: None
        """
        fig_underlyings = self.draw_underlyings()

        # figure for indexed performance for each strategy and distribution of expected returns
        fig_performance = go.Figure()
        distrib_exp_ror = dict()
        for strategy in self.engine.strategies:
            max_window, min_index = self.max_window_min_start_index(strategy.name)

            # load temp file holding results
            results = self.load_result(strategy.name, max_window, min_index)

            # add strategy performance to plot
            fig_performance.add_trace(go.Scatter(x=self._xx[strategy.lookback: self.len_data],
                                                 y=((np.array(results['merged_total_balances']) * 100) /
                                                    results['merged_total_balances'][0]), name=strategy.name))
            # add distribution of expected rate of return of strategy
            # noinspection PyProtectedMember
            distrib_exp_ror[strategy.name] = metric._returns(results['merged_total_balances'], 'pct_return')
        fig_performance.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                      legend_title='strategy')
        fig_performance.add_hline(100, line=dict(color='Black', dash='dot', width=1))
        fig_distrib_exp_ror = ff.create_distplot(list(distrib_exp_ror.values()), list(distrib_exp_ror.keys()),
                                                 show_hist=False)
        fig_distrib_exp_ror.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                          xaxis_title='daily percentage change', legend_title='strategy')

        # figure for portfolio presentation
        fig_vola_exp_ror = go.Figure()
        fig_sharpe_sortino = go.Figure()
        fig_tot_ret_exp_ror = go.Figure()
        fig_var_mdd = go.Figure()

        # collect data of annualized volatility (x-axis), expected rate of return (y-axis) and sharpe and sortino
        # values (radius)
        for strategy in self.engine.strategies:
            keys = [(str(length), str(index)) for length in list(self.engine.run_register[strategy.name].keys())
                    for index in self.engine.run_register[strategy.name][length]]
            win_lengths = [int(length) for length in list(self.engine.run_register[strategy.name].keys())
                           for _ in self.engine.run_register[strategy.name][length]]
            if self.overview_page_layout == 'full':
                vola = [self.engine.standard_analysis_results[strategy.name][key]['volatility'] for key in keys]
                exp_ror = [self.engine.standard_analysis_results[strategy.name][key]['expected_rate_of_return']
                           for key in keys]
                sharpe = [self.engine.standard_analysis_results[strategy.name][key]['sharpe_ratio'] for key in keys]
                sortino = [self.engine.standard_analysis_results[strategy.name][key]['sortino_ratio'] for key in keys]
                tot_ret = [self.engine.standard_analysis_results[strategy.name][key]['total_rate_of_return']
                           for key in keys]
                mdd = [self.engine.standard_analysis_results[strategy.name][key]['max_drawdown'] for key in keys]
                v_a_r = [self.engine.standard_analysis_results[strategy.name][key]['value_at_risk'] for key in keys]
            elif self.overview_page_layout == 'simple':
                max_window, min_index = self.max_window_min_start_index(strategy.name)
                max_window = str(max_window)
                min_index = str(min_index)
                vola = [self.engine.standard_analysis_results[strategy.name][max_window, min_index]['volatility']]
                exp_ror = [self.engine.standard_analysis_results[strategy.name][max_window, min_index]
                           ['expected_rate_of_return']]
                sharpe = [self.engine.standard_analysis_results[strategy.name][max_window, min_index]['sharpe_ratio']]
                sortino = [self.engine.standard_analysis_results[strategy.name][max_window, min_index]
                           ['sortino_ratio']]
                tot_ret = [self.engine.standard_analysis_results[strategy.name][max_window, min_index]
                           ['total_rate_of_return']]
                mdd = [self.engine.standard_analysis_results[strategy.name][max_window, min_index]['max_drawdown']]
                v_a_r = [self.engine.standard_analysis_results[strategy.name][max_window, min_index]['value_at_risk']]
            else:
                self.engine.close()
                raise NotImplementedError(self.overview_page_layout, ' not implemented. overview_page={simple, full}.')

            fig_vola_exp_ror.add_trace(go.Scatter(x=vola, y=exp_ror, mode='markers', name=strategy.name,
                                                  marker=dict(size=minmax_scale(win_lengths, (10, 50))),
                                                  text=['Volatility: {},<br>'
                                                        'expect. return: {},<br>'
                                                        'window length: {}'.format(vola[i],
                                                                                   exp_ror[i],
                                                                                   win_lengths[i])
                                                        for i in range(len(vola))]))
            fig_sharpe_sortino.add_trace(go.Scatter(x=sharpe, y=sortino, mode='markers', name=strategy.name,
                                                    marker=dict(size=minmax_scale(win_lengths, (10, 50))),
                                                    text=['Sharpe Ratio: {},<br>'
                                                          'Sortino Ratio: {},<br>'
                                                          'window length: {}'.format(sharpe[i],
                                                                                     sortino[i],
                                                                                     win_lengths[i])
                                                          for i in range(len(vola))]))
            fig_tot_ret_exp_ror.add_trace(go.Scatter(x=tot_ret, y=exp_ror, mode='markers', name=strategy.name,
                                                     marker=dict(size=minmax_scale(win_lengths, (10, 50))),
                                                     text=['Total rate of return: {},<br>'
                                                           'expect. return: {},<br>'
                                                           'window length: {}'.format(tot_ret[i],
                                                                                      exp_ror[i],
                                                                                      win_lengths[i])
                                                           for i in range(len(tot_ret))]))
            fig_var_mdd.add_trace(go.Scatter(x=v_a_r, y=mdd, mode='markers', name=strategy.name,
                                             marker=dict(size=minmax_scale(win_lengths, (10, 50))),
                                             text=['Value at Risk: {},<br>'
                                                   'Maximum Drawdown: {},<br>'
                                                   'window length: {}'.format(v_a_r[i],
                                                                              mdd[i],
                                                                              win_lengths[i])
                                                   for i in range(len(v_a_r))]))
        fig_vola_exp_ror.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                       xaxis_title='volatility', yaxis_title='exp. rate of return',
                                       legend_title='strategy')
        fig_sharpe_sortino.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                         xaxis_title='ann. sharpe', yaxis_title='ann. sortino',
                                         legend_title='strategy')
        fig_tot_ret_exp_ror.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                          xaxis_title='ann. total return', yaxis_title='exp. rate of return',
                                          legend_title='strategy')
        fig_var_mdd.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                                  xaxis_title='ann. value at risk', yaxis_title='max drawdown',
                                  legend_title='strategy')
        if self.overview_page_layout == 'full':
            fig_vola_exp_ror.update_layout(title='radius: backtesting window length')
            fig_sharpe_sortino.update_layout(title='radius: backtesting window length')
            fig_tot_ret_exp_ror.update_layout(title='radius: backtesting window length')
            fig_var_mdd.update_layout(title='radius: backtesting window length')

        return_page = [html.H1('Overview of all Strategies'),
                       html.P('WARNING: Decimal rounding error might occur', className='pb-5'),
                       html.H2('Underlyings'),
                       dcc.Graph(id='fig_underlyings', figure=fig_underlyings),
                       html.H2('Strategy Performances'),
                       html.P('Indexed on entire dataframe'),
                       dcc.Graph(id='indexed_performance', figure=fig_performance),
                       dbc.Row(className='pt-5', children=[
                           dbc.Col(align='end', children=[
                               html.H2('Expected Rate of Return vs. Annualized Volatility'),
                               html.P('Calculation based on: percentage return & normal distribution'),
                               dcc.Graph(id='vola_exp_ror', figure=fig_vola_exp_ror)]),
                           dbc.Col(align='end', children=[
                               html.H2('Annualized Sortino Ratio vs. Annualized Sharpe Ratio'),
                               html.P('Calculation based on: percentage return & normal distribution'),
                               dcc.Graph(id='sharpe_sortino', figure=fig_sharpe_sortino)])]),
                       dbc.Row(className='pt-5', children=[
                           dbc.Col(align='end', children=[
                               html.H2('Expected Rate of Return vs. Annualized Total Return'),
                               html.P('Calculation based on: percentage return & normal distribution'),
                               dcc.Graph(id='tot_ret_exp_ror', figure=fig_tot_ret_exp_ror)]),
                           dbc.Col(align='end', children=[
                               html.H2('Max Drawdown vs. Annualized Value at Risk'),
                               html.P('Calculation based on: percentage return & normal distribution'),
                               dcc.Graph(id='var_mdd', figure=fig_var_mdd)])]),
                       html.H2('Distribution of daily Returns', className='pt-5'),
                       html.P('Indexed on entire dataframe, daily in percent'),
                       dcc.Graph(id='distrib_exp_ror', figure=fig_distrib_exp_ror)
                       ]
        return return_page

    def strategy_page(self, str_strategy):
        """
        Defines basic structure with sidebar for strategy pages.
        :param str_strategy: str, strategy name
        :return: HTML dash structure with sidebar and container for plotting
        """
        _sidebar_style = {
            "position": "fixed",
            "top": 0,
            "left": 0,
            "bottom": 0,
            "width": "10rem",
            "padding": "2rem 1rem",
            "background-color": "#f8f9fa",
        }
        _content_style = {
            "margin-left": "1rem",
            "margin-right": "1rem",
            "padding": "2rem 1rem",
        }

        _sidebar = html.Div([
            html.H5("Dashboard", className="display-6"),
            html.Hr(),
            html.P(str_strategy, className="lead"),
            dbc.Nav([dbc.NavLink("Metrics", href="/strategy/{}/metrics".format(str_strategy), active="exact"),
                     dbc.NavLink("Runs", href="/strategy/{}/runs".format(str_strategy), active="exact")],
                    vertical=True, pills=True),
        ], style=_sidebar_style,
        )
        _strategy_content = dbc.Container(id='strategy-page-content', className='pt-4', style=_content_style,
                                          children=self.strategy_page_metrics(str_strategy))
        return html.Div([_sidebar, _strategy_content])

    # noinspection PyProtectedMember,DuplicatedCode
    def strategy_page_metrics(self, str_strategy):
        """
        Defines page 'Metrics' at strategy page, which is inserted into the basic structure defined by
        self.strategy_page.
        :param str_strategy: str, strategy name
        :return: list of HTML dash elements with plotly plots
        """
        _max_window, _min_index = self.max_window_min_start_index(str_strategy)
        _max_window, _min_index = str(_max_window), str(_min_index)

        if _min_index == 'runthrough':
            _underlying_start = 0
        else:
            _underlying_start = int(_min_index)

        if self.engine.volume_data is not None:
            fig_underlyings = make_subplots(rows=2, cols=1)
            gos_volumes = self.draw_volumes(return_type='go')
        else:
            fig_underlyings = go.Figure()
        if self.signal_symbols is not None:
            gos_signals = self.draw_strategy_signals(str_strategy, _max_window, _min_index, return_type='go')
            for scatter_i in gos_signals:
                fig_underlyings.add_trace(scatter_i)
        gos_underlyings = self.draw_underlyings(return_type='go')
        for scatter_i in gos_underlyings:
            fig_underlyings.add_trace(scatter_i)
        if self.engine.volume_data is not None:
            # noinspection PyUnboundLocalVariable
            for bar_i in gos_volumes:
                fig_underlyings.add_trace(bar_i, row=2, col=1)
        fig_underlyings.add_vline(self._xx[self.engine.lookbacks[str_strategy]], line=dict(color='Black', dash='dot',
                                                                                           width=1))

        fig_comp = self.draw_strategy_composition(str_strategy, _max_window, _min_index, return_type='fig')
        fig_perform = self.draw_strategy_performance(str_strategy, _max_window, _min_index, return_type='fig')
        fig_yield = self.draw_strategy_metric_yield(str_strategy, str_metric='expected_rate_of_log_return',
                                                    return_type='fig')

        std_page = [html.H1('STRATEGY: {}'.format(str_strategy)),
                    html.P('WARNING: Decimal rounding error might occur, '
                           'KDE estimation might appear flatter than in reality',
                           className='pb-5'),
                    html.H2('Underlyings'),
                    dcc.Graph(id='strategy_page_fig_underlyings', figure=fig_underlyings),
                    html.H2('Strategy Composition'),
                    html.P('Reference currency: {}'.format(self.engine.reference_currency)),
                    dcc.Graph(id='strategy_page_fig_comp', figure=fig_comp),
                    html.H2('Strategy Performance'),
                    html.P('Indexed on entire dataframe'),
                    dcc.Graph(id='strategy_page_fig_perform', figure=fig_perform),
                    html.H2('Yield Curve of Expected Log Returns'),
                    html.P('Expected Log Returns per simulated window length'),
                    dcc.Graph(id='strategy_page_fig_yield', figure=fig_yield)]
        metric_page = list()
        if self.strategy_page_layout == 'full':
            strategy_render_func = self.draw_strategy_metric_stacked_hist
        elif self.strategy_page_layout == 'simple':
            strategy_render_func = self.draw_strategy_metric_simple_hist
        else:
            self.engine.close()
            raise NotImplementedError(self.strategy_page_layout, ' not implemented. '
                                                                 'strategy_page_layout={simple, full}.')
        for metric_key in self.engine.metrics:
            metric_page.extend([html.H2(str(metric_key)),
                                dcc.Graph(id='strategy_page_fig_{}'.format(metric_key),
                                          figure=strategy_render_func(str_strategy, metric_key,
                                                                      self.engine.analysis_results,
                                                                      return_type='fig'))])
        std_page.extend(metric_page)
        return std_page

    def strategy_page_runs(self, str_strategy):
        """
        Defines basic structure 'Runs' at strategy page, which is inserted into the basic structure defined by
        self.strategy_page.
        :param str_strategy: str, strategy name
        :return: list of HTML dash elements with plotly plots
        """
        std_page = [html.H1('STRATEGY: {}'.format(str_strategy)),
                    html.P('WARNING: Decimal rounding error might occur', className='pb-5'),
                    dcc.Dropdown(id='strategy-runs-page-dropdown',
                                 options=[{'label': '{} {}'.format(_length, _start_index),
                                           'value': '{} {}'.format(_length, _start_index)}
                                          for _length in self.engine.run_register[str_strategy].keys()
                                          for _start_index in self.engine.run_register[str_strategy][_length]]),
                    dbc.Container(id='strategy-runs-page-content', className='pt-4')]

        return std_page

    # noinspection DuplicatedCode
    def strategy_page_runs_dropdown(self, str_strategy, win_len, start_id):
        """
        Defines page 'Runs' at strategy page after a specific 'run' of FXEngine.run() is selected via the dropdown menu.
        This is inserted into the basic structure defined by self.strategy_page_runs and respectively by
        self.strategy_page.
        :param str_strategy:
        :param win_len:
        :param start_id:
        :return:
        """
        _result = self.load_result(str_strategy, win_len, start_id)

        if start_id == 'runthrough':
            start_id = 0
        win_len = int(win_len)
        start_id = int(start_id)

        fig_underlyings = go.Figure()
        if self.signal_symbols is not None:
            gos_signals = self.draw_strategy_signals(str_strategy, win_len, start_id, return_type='go')
            for scatter_i in gos_signals:
                fig_underlyings.add_trace(scatter_i)
        gos_underlyings = self.draw_underlyings(return_type='go')
        for scatter_i in gos_underlyings:
            fig_underlyings.add_trace(scatter_i)
        fig_underlyings.add_vline(self._xx[self.engine.lookbacks[str_strategy]], line=dict(color='Black', dash='dot',
                                                                                           width=1))

        fig_comp = self.draw_strategy_composition(str_strategy, win_len, start_id, return_type='fig')
        fig_perform = self.draw_strategy_performance(str_strategy, win_len, start_id, return_type='fig')

        _page = [html.H2('Underlyings'),
                 dcc.Graph(id='strategy_runs_page_fig_underlyings', figure=fig_underlyings),
                 html.H2('Strategy Composition'),
                 html.P('Reference currency: {}'.format(self.engine.reference_currency)),
                 dcc.Graph(id='strategy_runs_page_fig_comp', figure=fig_comp),
                 html.H2('Strategy Performance'),
                 html.P('Indexed on entire dataframe'),
                 dcc.Graph(id='strategy_page_fig_perform', figure=fig_perform)]
        return _page

    def run(self, debug=False):
        """
        Launches Dash app server and opens port for web browser. Port is displayed in console. For further information
        please refer to the Dash library.

        FXDashboard provides an "EXIT-page" with an exit button, which stops the Dash app server and enables to proceed
        with any following code in the main control flow (where FXEngine.close() should be explicitly called).

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!! Do not forget to explicitly close FXEngine via FXEngine.close() (even though FXEngine is automatically
            garbage collected !!!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        !!! signal names, which are appended with FXStrategy.add_signal(), should not contain multiple substrings
            of either currencies (or assets or whatever defines keys of FXEngine.price_data dictionary) nor keys
            of shape defining dictionary (param:signal_symbols at FXDashboard.__init__) !!!
            Recommendation: signal names should be mutual free of substring parts, otherwise they might be
            visualized multiple times at FXDashboard !!!
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        (see FXDashboard class description for further information)

        :param debug: bool, default=False,
                      if True, Dash application is launched in debug mode, which might trigger multiple calls to
                        FXEngine.run(), but is in general easier to debug and enables hot reloading
                      if False, Dash application is launched in normal mode, which might increase performance but might
                        be harder to handle and to debug
        :return: None
        """
        # #################################################################################
        # ################################   app dashboard ################################
        # #################################################################################
        self.app = dash.Dash(external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)
        self.app.layout = html.Div(
            children=[
                dcc.Location(id='url', refresh=False),
                dbc.NavbarSimple(brand='Dashboard', color='primary', dark=True, fluid=True,
                                 children=[
                                     dbc.NavItem(dbc.NavLink('Overview', href='/overview', active='exact')),
                                     dbc.DropdownMenu(nav=True, in_navbar=True, label='Strategies',
                                                      children=[
                                                          dbc.DropdownMenuItem(strategy.name,
                                                                               href='/strategy/'
                                                                                    '{}'.format(strategy.name))
                                                          for strategy in self.engine.strategies
                                                      ]),
                                     dbc.NavItem(dbc.NavLink('Exit', href='/exit', active='exact'))
                                 ]),
                dbc.Container(id='page-content', className='pt-4')
            ])

        @self.app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
        def render_page_content_cb(pathname):
            """
            Navigate main pages.
            :param pathname: str
            :return: call to respective page or dash bootstrap component Jumbotron
            """
            pathname = pathname.replace('%20', ' ')
            if pathname == '/overview':
                return self.page_overview()
            elif pathname == '/':
                return self.page_overview()
            elif pathname.split('/')[1] == 'strategy':
                selected_strategy = pathname.split('/')[2]
                return self.strategy_page(selected_strategy)
            elif pathname == '/exit':
                return dbc.Jumbotron([html.H1('Click exit to shut down', className="text-danger"),
                                      html.Hr(className="my-2"),
                                      html.P('Click exit button to shut down dashboard. '
                                             'No additional confirmation pop up after shut down.'),
                                      html.P(dbc.Button('EXIT', id='exit-button', color='primary'), className='lead'),
                                      html.P(id='exit-placeholder')])

        @self.app.callback(Output('exit-placeholder', 'children'), [Input('exit-button', 'n_clicks')])
        def exit_server(n):
            """
            Shuts down Dash application server.
            :param n: int or None, click event of button
            :return: None
            """
            if n is None:
                return
            self.engine.close()
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Flask environ not configured as werkzeug.server.')
            func()

        @self.app.callback(Output('strategy-page-content', 'children'), [Input('url', 'pathname')])
        def strategy_page_metrics_cb(pathname):
            """
            Navigates between 'Metrics' and 'Runs' on strategy page, selection via sidebar on strategy page.
            :param pathname: str
            :return: call to respective sub-page
            """
            pathname = pathname.replace('%20', ' ')
            if len(pathname.split('/')) > 2:
                str_strategy = pathname.split('/')[2]
            else:
                return None
            if len(pathname.split('/')) > 3:
                str_sidebar = pathname.split('/')[3]
            else:
                str_sidebar = 'metrics'
            if str_sidebar == 'metrics':
                return self.strategy_page_metrics(str_strategy)
            elif str_sidebar == 'runs':
                return self.strategy_page_runs(str_strategy)
            else:
                dbc.Jumbotron([html.H1("404: Not found", className="text-danger"),
                               html.Hr(),
                               html.P(f"The pathname {pathname} was not recognised...")])

        @self.app.callback(Output('strategy-runs-page-content', 'children'),
                           [Input('strategy-runs-page-dropdown', 'value'), Input('url', 'pathname')])
        def strategy_page_runs_dropdown_cb(value, pathname):
            """
            Triggers dropdown selection at 'Runs' sub-page of strategy page.
            :param value: str or None, value of dropdown at 'Runs' sub-page of strategy page
            :param pathname: str
            :return: None or respective page visualization for given dropdown selection
            """
            pathname = pathname.replace('%20', ' ')

            if len(pathname.split('/')) < 3:
                return None

            if value is not None:
                win_len = value.split(' ')[0]
                start_index = value.split(' ')[1]
                str_strategy = pathname.split('/')[2]
                return self.strategy_page_runs_dropdown(str_strategy, win_len, start_index)
            else:
                return None

        # ###########################################################################
        # ############################   run dashboard ##############################
        # ###########################################################################
        self.app.run_server(debug=debug)
