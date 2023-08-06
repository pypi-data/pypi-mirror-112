import datetime
import numpy as np

from trapeza.engine import FXEngine
from trapeza.tests.setup_test import setup_data, setup_strategies, setup_volume_data
from trapeza.dashboard import FXDashboard

if __name__ == '__main__':
    strats = setup_strategies()
    engine = FXEngine('genesis', strats)
    prices = setup_data()
    volumes = setup_volume_data()
    len_data = len(prices[list(prices.keys())[0]])

    win_diff = 5

    engine.run(prices, 'EUR', volumes, len_data - win_diff - 10, len_data - 10, 50, True)
    engine.analyze()

    start_date = datetime.datetime.today()
    dates = [start_date + datetime.timedelta(days=x) for x in range(len(prices[list(prices.keys())[0]]))]
    dates = np.array(dates, dtype="datetime64")

    dash = FXDashboard(engine, {'buy': ('triangle-up', 'Green'), 'sell': ('triangle-down', 'Red')}, date_time=dates)
    dash.run()

    engine.close()
