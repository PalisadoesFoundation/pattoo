"""Functions for creating URIs."""

import time

# Pattoo imports
from pattoo.configuration import ConfigIngester


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
    ts_stop = int(time.time() * 1000) - (
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
