"""Functions for getting system information."""

from subprocess import run, PIPE


def process_running(process_name):
    """Check for existence of running process by name.

    Args:
        process_name: Name of process

    Returns:
        result: True if running

    """
    # Initialize key variables
    result = False
    command = 'ps -ef'
    if isinstance(process_name, list) is False:
        process_name = [process_name]

    # Check if process name contains the given name string.
    output = run(command.split(), stdout=PIPE, check=True).stdout.decode()
    for item in process_name:
        if item.lower() in output.lower():
            result = True
            break

    return result
