"""Functions for getting system information."""

from subprocess import run, PIPE


def process_running(process_name):
    """Check for existence of running process by name.

    Args:
        None

    Returns:
        result: True if running

    """
    # Initialize key variables
    result = False
    command = 'ps -ef'

    # Check if process name contains the given name string.
    output = run(command.split(), stdout=PIPE, check=True).stdout.decode()
    print(output)
    if process_name.lower() in output.lower():
        result = True

    return result
