class CoverageError(Exception):
    """Exception raised when account coverage violated for certain depot positions"""
    def __init__(self, amount, currency, msg=None):
        if msg is None:
            super(CoverageError, self).__init__('Coverage not sufficient to withdraw {} {}.'.format(amount, currency))
        else:
            super(CoverageError, self).__init__('Coverage not sufficient to withdraw {} {}. '
                                                '{}'.format(amount, currency, msg))


class AccountingError(Exception):
    """Exception raised when inconsistencies occur, e.g. arithmetic operations on different currencies"""
    def __init__(self, amount_1, currency_1, amount_2, currency_2):
        super(AccountingError, self).__init__('Cannot perform arithmetic operations on '
                                              '{} {} and {} {}.'.format(amount_1, currency_1, amount_2, currency_2))


class PositionNAError(Exception):
    """Exception raised when position is not listed"""
    def __init__(self, currency):
        super(PositionNAError, self).__init__('{} is not listed/ not available in depot.'.format(currency))


class AccountError(Exception):
    """Exception raised when wrong account/ cannot perform action on respective account"""
    def __init__(self, account, msg=None):
        if msg is None:
            super(AccountError, self).__init__('Cannot perform action on account {}'.format(account))
        else:
            super(AccountError, self).__init__('Cannot perform action on account {}. {}.'.format(account, msg))


class StrategyError(Exception):
    """Exception raised when wrong strategy/ cannot perform action on respective strategy"""
    def __init__(self, strategy, msg=None):
        if msg is None:
            super(StrategyError, self).__init__('Cannot perform action on strategy {}.'.format(strategy))
        else:
            super(StrategyError, self).__init__('Cannot perform action on strategy {}. {}.'.format(strategy, msg))


class OperatingError(Exception):
    """Exception raised when internal operations and transaction cannot be executed due
    to internal program logic error"""
    def __init__(self, msg):
        super(OperatingError, self).__init__(msg)
