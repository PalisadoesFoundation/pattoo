"""Shared functions and methods utilized by the pattoo installation."""
# Standard imports
import sys
import subprocess
import traceback
import getpass
import os


def run_script(cli_string, die=True, verbose=True):
    """Run the cli_string UNIX CLI command and record output.

    Args:
        cli_string: String of command to run
        die: Exit with error if True

    Returns:
        (returncode, stdoutdata, stderrdata):
            Execution code, STDOUT output and STDERR output.

    """
    # Initialize key variables
    messages = []
    stdoutdata = ''.encode()
    stderrdata = ''.encode()
    returncode = 1

    # Enable verbose mode if True
    if verbose is True:
        print('Running Command: "{}"'.format(cli_string))

    # Run update_targets script
    do_command_list = list(cli_string.split(' '))

    # Create the subprocess object
    try:
        process = subprocess.Popen(
            do_command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE)
        stdoutdata, stderrdata = process.communicate()
        returncode = process.returncode
    except:
        (exc_type, exc_value, exc_traceback) = sys.exc_info()
        messages.append('''\
Bug: Exception Type:{}, Exception Instance: {}, Stack Trace Object: {}]\
    '''.format(exc_type, exc_value, exc_traceback))
        messages.append(traceback.format_exc())

    # Crash if the return code is not 0
    if bool(returncode) is True:
        # Print the Return Code header
        messages.append(
            'Return code:{}'.format(returncode)
        )

        # Print the STDOUT
        for line in stdoutdata.decode().split('\n'):
            messages.append(
                'STDOUT: {}'.format(line)
            )

        # Print the STDERR
        for line in stderrdata.decode().split('\n'):
            messages.append(
                'STDERR: {}'.format(line)
            )

        # Log message
        if verbose is True:
            print('messages: {}'.format(messages))
        if bool(messages) is True:
            for log_message in messages:
                if verbose is True:
                    print(log_message)

            if bool(die) is True:
                # All done
                sys.exit(2)

    # Return
    return (returncode, stdoutdata, stderrdata)


def unittest_environment_setup():
    """Set up config dir to the unittest configdir if the user is not root.

    Args:
        None

    Returns:
        unittest_dir: The directory where unittest resources are stored

    """
    # Initialize key variables
    config_suffix = '.pattoo-unittests{}config'.format(os.sep)
    unittest_config_dir = (
        '{}{}{}'.format(os.environ['HOME'], os.sep, config_suffix))
    print('Setting config directory to {}'.format(unittest_config_dir))

    # Sets PATTOO_CONFIGDIR environment varaible to the unittest config dir
    if 'unittest' not in os.environ['PATTOO_CONFIGDIR']:
        os.environ['PATTOO_CONFIGDIR'] = unittest_config_dir

    unittest_dir = os.path.join(
                        os.path.expanduser('~'), config_suffix.split(os.sep)[0])
    return unittest_dir


def root_check():
    """Check if the user is root or travis.

    Args:
        None

    Returns:
        True: If the user is root
        False: If the user is not root
    """
    if getpass.getuser() == 'root':
        return True
    else:
        return False


def log(message):
    """Log messages and exit abnormally.

    Args:
        message: Message to print

    Returns:
        None

    """
    # exit
    print('\nPATTOO Error: {}'.format(message))
    sys.exit(3)
