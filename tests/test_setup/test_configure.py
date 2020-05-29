#!/usr/bin/env/python3

import os
import unittest
import sys
import tempfile
import yaml
# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(EXEC_DIR, os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}test_setup'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)
    
from setup.configure.configure import Configure
from tests.libraries.configuration import UnittestConfig


class Test_Configure(unittest.TestCase):
    """Checks all functions and methods"""

    def test__init__(self):
        """Unnittest to test the __init__ method"""
        pass

    def test_set_configuration_directory(self):
        """Unittest to test the method set_configdir."""

        expected = True
        results = []
        config_path = '/opt/pattoo/config'
        env_variable = 'export PATTOO_CONFIGDIR={}'.format(config_path)
        Configure.set_configdir(self) # Insert param for file path
        file_path = os.path.join(os.path.join(
            os.path.expanduser('~')), '.bash_profile')
        with open(file_path, 'r') as file:
            for line in file:
                if line == env_variable:
                    results.append(True)
        results.append(os.environ['PATTOO_CONFIGDIR']) == config_path
        result = all(results)
        self.assertEqual(result, expected)


    def test_pattoo_server_config(self):
        """Unittest to test the method pattoo_server_config """
        pass

    def test_read_config(self):
        """Unittest to test the method read_server_config."""
        expected = Configure.default_config
        # Create temporary directory using the temp file package
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir,"pattoo_temp_config.yaml")
            #Dumps default configuration to file in temp directory
            with open(file_path, 'w+') as temp_config:
                yaml.dump(expected,temp_config,default_flow_style=False)
            result = Configure.read_config(self,file_path,expected)
            result == expected
            self.assertEqual(result == expected,True)

    def test_already_written(self):
        """ Unnittest to test the method already_written"""
        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = os.path.join(temp_dir,'test_file.txt')
            line = 'export PATTOO_CONFIGDIR=/opt/Calico/config'
            with open(file_path,'w') as file:
                file.write(line)
            expected = True
            result = Configure.already_written(self,file_path,line)
            self.assertEqual(expected,result)

    def test_mkdir(self):
        """Unitttest to test the _mkdir method."""
        with tempfile.TemporaryDirectory() as temp_dir:
            directory = os.path.join(temp_dir,'test_dir')
            Configure._mkdir(self,directory)
            expected = True
            result = os.path.isdir(directory)
            self.assertEqual(expected,result)


    def test_log(self):
        """Unittest to test the _log method."""
        with self.assertRaises(SystemExit) as cm:
            Configure._log(self,"Test Error Message")
        self.assertEqual(cm.exception.code,3)
        
    def test_promt(self):
        """ Testing method prompt """
        pass


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
