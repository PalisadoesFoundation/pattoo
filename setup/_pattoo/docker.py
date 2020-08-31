"""Install pattoo docker container."""
# Import python related libraries
import os

# Import pattoo related libraries
from _pattoo import shared
from pattoo_shared import files, log
from pattoo_shared.installation import configure


def copy_config(file_path, config_dir, container_name):
    """Copy configuration file from host machine into docker.

    Args:
        file_path: The path of the config file being copied
        config_dir: The configuration directory on the docker container
    Returns:
        None

    """
    command = 'docker cp {0} {1}:{2}'.format(file_path,
                                             container_name,
                                             config_dir)
    shared.run_script(command)


def get_ports(config_path):
    """Get the ip bind ports from the configuration file.

    Args:
        config_path: The path to the configuration file being read

    Returns:
        ports: A list of the ip bind ports to be exposed in docker

    """
    # Initialize key variables
    config_dict = files.read_yaml_file(config_path)
    ports = []

    # Retrieve bind ports from config dict
    if config_dict is not None:
        for key in config_dict:
            bind_port = config_dict.get(key).get('ip_bind_port')
            if bind_port is not None:
                ports.append(bind_port)

    return ports


def expose_ports(config_path, docker_path):
    """Expose ports in the Dockerfile.

    This will write to the docker file based on the configuration
    values in the configuration directory.

    Args:
        config_path: The path to the configuration file with the ports to be
                     exposed
        docker_path: The path to the Dockerfile

    Returns:
        None

    """
    # Initialize key variables
    ports = get_ports(config_path)
    expose_index = None

    # Read Dockerfile and expose the respective ports below the line starting
    # with Expose ports
    try:
        f_handle = open(docker_path, 'r+')
    except FileNotFoundError:
        log.log2die_safe(20319, 'The Dockerfile does not exist')
    except PermissionError:
        log.log2die_safe(
                20591, 'Insufficient permissions for reading the Dockerfile')
    else:
        with f_handle:
            content = f_handle.readlines()

            # Retrieve the index of the line with 'Expose ports'
            for line in content:
                if line.startswith('# Expose ports'):
                    expose_index = content.index(line)
                    break

            if expose_index is not None:
                # Insert new port entries based on the configuration file
                for port in ports:
                    expose_line = 'EXPOSE {}\n'.format(port)

                    # Skip duplicate lines
                    if expose_line in content:
                        pass
                    else:
                        content.insert(expose_index+1, expose_line)

                # Set pointer to beginning of file
                f_handle.seek(0, 0)

                # Rewrite file contents
                f_handle.write(''.join(content))


def docker_check():
    """Check if docker is installed/running.

    Args:
        None

    Returns:
        None

    """
    status = shared.run_script('service docker status', verbose=False, die=False)[0]
    if status == 0:
        return True
    elif status == 3:
        message = '''\
The docker daemon is not running.
Ensure that the docker daemon is running before installing.'''
    elif status == 4:
        message = '''\
Docker has not been installed to the system.
Ensure that docker is installed before creating the pattoo docker container.'''
    else:
        message = '''\
Unknown error code.
Ensure that docker is running and has the adequate permissions'''
    log.log2die_safe(20172, message)


def image_check(image_name):
    """Check if a docker image already exists for the image specified.

    Args:
        The name of the image being checked

    Returns:
        None

    """
    status = shared.run_script(
                'docker image inspect {}'.format(image_name), die=False)[0]
    if status == 0:
        message = 'The docker image "{}" already exists'.format(image_name)
        log.log2die_safe(20170, message)


def install(container_name, config_files, verbose=True):
    """Perform docker installation for the respective pattoo component.

    Args:
        component_name: The name of the pattoo component being dockerized
        config_files: A list of configuration files
        file_path: The filepath to the Dockerfile

    Returns:
        None

    """
    # Initialize key variables
    config_dir = os.environ.get('PATTOO_CONFIGDIR')

    # Insert ports based on config file
    server_path = os.path.join(config_dir, config_files[1])
    expose_ports(server_path, './Dockerfile')

    # Check if docker is installed/running
    docker_check()

    # Build pattoo container
    image_check('pattoo')
    print('Building Pattoo Container. This could take some time...')
    shared.run_script('docker build -t {} .'.format(container_name))

    # Run container in detached mode as pattoo
    run_command = '''\
docker run --privileged -d --network=host --name={0} {0}'''.format(container_name)
    shared.run_script(run_command, verbose=verbose)

    # Copy configuration files from host machine
    for config_file in config_files:
        file_path = os.path.join(config_dir, config_file)
        copy_config(file_path, config_dir, container_name)

    # Run docker installation
    install_command = '''\
docker exec -i {} setup/install.py install all'''.format(container_name)
    shared.run_script(install_command)
