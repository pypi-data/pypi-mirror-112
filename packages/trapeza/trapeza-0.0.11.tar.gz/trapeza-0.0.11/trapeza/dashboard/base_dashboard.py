from abc import ABCMeta, abstractmethod


class BaseDashboard(metaclass=ABCMeta):
    """
    Base class for dashboards.
    This is a pretty slim skeleton because concrete implementation of visualization is dependent on third party library
    (e.g. FXDashboard is implemented via Python Dash and Plotly).
    """

    @abstractmethod
    def run(self):
        """
        Launch dashboard.
        :return: None
        """

    @abstractmethod
    def load_result(self, strategy_name):
        """
        Wrapper function for BaseEngine.load_result(). param:strategy_name might be passed as page path from Dash
        application and might need additional parsing.
        :param strategy_name: str, path from Dash application
        :return: see BaseEngine.load_result()
        """
