"""Functions for creating URIs."""

import time

# Pattoo imports
from pattoo.configuration import ConfigIngester
from pattoo_shared.times import normalized_timestamp


def chart_timestamp_args(secondsago=None):
    """Create URI arguments for charts.

    Args:
        secondsago: Number of seconds in the past to calculate start and
            stop times for charts

    Returns:
        result: tuple of (ts_start, ts_stop)

    """
    # Calculate stop. This takes into account the ingester cycle and subtracts
    # a few extra seconds to prevent zero values at the end.
    config = ConfigIngester()
    polling_interval = config.polling_interval()
    ts_norm = normalized_timestamp(polling_interval, int(time.time() * 1000))
    ts_stop = ts_norm - (
        (config.ingester_interval() * 1000) + (3 * config.polling_interval()))

    # Calculate start
    if bool(secondsago) is True and isinstance(secondsago, int) is True:
        ts_start = ts_stop - (abs(secondsago) * 1000)
    else:
        # ts_start = ts_stop - (604800 * 1000)
        ts_start = ts_stop - (3600 * 24 * 7) * 1000

    # Return
    result = (ts_start, ts_stop)
    return result
