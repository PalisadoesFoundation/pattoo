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
        result: Starting time

    """
    # Calculate stop. This takes into account the ingester cycle and subtracts
    # a few extra seconds to prevent zero values at the end.
    config = ConfigIngester()
    polling_interval = config.polling_interval()
    now = normalized_timestamp(polling_interval, int(time.time() * 1000))

    # Calculate start
    if bool(secondsago) is True and isinstance(secondsago, int) is True:
        result = now - (abs(secondsago) * 1000)
    else:
        # result = ts_stop - (604800 * 1000)
        result = now - (3600 * 24 * 7) * 1000

    # Return
    return result
