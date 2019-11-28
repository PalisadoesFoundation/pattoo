"""Functions for creating URIs."""

import time


def chart_timestamp_args(secondsago=None):
    """Create URI arguments for charts.

    Args:
        secondsago: Number of seconds in the past to calculate start and
            stop times for charts

    Returns:
        result: tuple of (ts_start, ts_stop)

    """
    # Calculate start
    ts_stop = int(time.time() * 1000)

    if bool(secondsago) is True and isinstance(secondsago, int) is True:
        ts_start = ts_stop - (secondsago * 1000)
    else:
        ts_start = ts_stop - (604800 * 1000)

    # Return
    result = (ts_start, ts_stop)
    return result
