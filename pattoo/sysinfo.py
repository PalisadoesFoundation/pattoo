"""Functions for creating URIs."""

import psutil


def process_running(process_name):
    """Check for existence of running process by name.

    Args:
        None

    Returns:
        result: tuple of (ts_start, ts_stop)

    """
    # Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if process_name.lower() in proc.name().lower():
                return True
        except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):
            pass
    return False
