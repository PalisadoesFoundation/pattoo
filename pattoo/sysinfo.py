"""Functions for getting system information."""

import psutil


def process_running(process_name):
    """Check for existence of running process by name.

    Args:
        process_name: Name of process

    Returns:
        result: True if running

    """
    # Initialize key variables
    result = False
    if isinstance(process_name, list) is True:
        process_name = ' '.join(process_name)
    else:
        process_name = str(process_name)

    # Check existence
    for proc in psutil.process_iter():
        try:
            # Get process CLI
            command_line = ' '.join(proc.cmdline())
            if bool(command_line) is False:
                continue
            if process_name in command_line:
                result = True
                break
        except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess):
            pass

    return result
