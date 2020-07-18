"""Install pip3 packages."""

# Main python libraries
import os
import sys
import getpass

from _pattoo import shared


def install_missing_pip3(package, pip_dir, verbose=True):
    """Automatically Install missing pip3 packages.

    Args:
        package: The pip3 package to be installed
        pip_dir: The directory the packages should be installed to

    Returns:
        True: if the package could be successfully installed

    """
    # Validate pip directory
    if not os.path.isdir(pip_dir):
        shared.log('Pip directory is invalid')
    # Installs to the directory specified as pip_dir if the user is not travis
    username = getpass.getuser()
    if username == 'root':
        shared.run_script(
            'python3 -m pip install {0} -t {1}'.format(package, pip_dir),
            verbose=verbose)
    elif username == 'travis':
        shared.run_script(
            'python3 -m pip install {0}'.format(package), verbose=verbose)
    else:
        shared.log('Installation user is not "root" or "travis"')


def install(requirements_dir, installation_directory=None, verbose=True):
    """Ensure PIP3 packages are installed correctly.

    Args:
        requirements_dir: The directory with the pip_requirements file.
        installation_directory: Directory where packages must be installed.
        verbose: Print status messages if True

    Returns:
        True if pip3 packages are installed successfully

    """
    # Initialize key variables
    lines = []
    if bool(installation_directory) is False:
        installation_directory = '/opt/pattoo-daemon/.python'

    # Check if valid directory wa passed in
    if os.path.isdir(installation_directory) is False:
        shared.log('Invalid directory {} passed in'.format(
                                                    installation_directory))
    # Appends pip3 dir to python path
    sys.path.append(installation_directory)

    # Read pip_requirements file
    filepath = '{}{}pip_requirements.txt'.format(requirements_dir, os.sep)
    if verbose:
        print('Checking pip3 packages')
    if os.path.isfile(filepath) is False:
        shared.log('Cannot find PIP3 requirements file {}'.format(filepath))

    # Opens pip_requirements file for reading
    with open(filepath, 'r') as _fp:
        line = _fp.readline()
        while line:
            # Strip line
            _line = line.strip()
            # Read line
            if True in [_line.startswith('#'), bool(_line) is False]:
                pass
            else:
                lines.append(_line)
            line = _fp.readline()

    # Process each line of the file
    for line in lines:
        # Determine the package
        package = line.split('=', 1)[0]
        package = package.split('>', 1)[0]

        # If verbose is true, the package being checked is shown
        if verbose:
            print('Installing package {}'.format(package))
        command = 'python3 -m pip show {}'.format(package)
        (returncode, _, _) = shared.run_script(
            command, verbose=verbose, die=False)

        # Install any missing pip3 package
        if bool(returncode) is True:
            install_missing_pip3(
                package, installation_directory, verbose=verbose)

    # Set ownership of any newly installed python packages to pattoo user
    if getpass.getuser() == 'root':
        if os.path.isdir(installation_directory) is True:
            shared.run_script('chown -R pattoo:pattoo {}'.format(
                installation_directory), verbose=verbose)

    print('pip3 packages successfully installed')
