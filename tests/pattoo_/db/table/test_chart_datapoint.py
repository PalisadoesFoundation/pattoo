import os
import unittest
import sys
from random import random

# Try to create a working PYTHONPATH
EXEC_DIR = os.path.dirname(os.path.realpath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(
    os.path.abspath(os.path.join(
        os.path.abspath(os.path.join(
            os.path.abspath(os.path.join(
                EXEC_DIR,
                os.pardir)), os.pardir)), os.pardir)), os.pardir))
_EXPECTED = '{0}pattoo{0}tests{0}pattoo_{0}db{0}table'.format(os.sep)
if EXEC_DIR.endswith(_EXPECTED) is True:
    # We need to prepend the path in case the repo has been installed
    # elsewhere on the system using PIP. This could corrupt expected results
    sys.path.insert(0, ROOT_DIR)
else:
    print('''This script is not installed in the "{0}" directory. Please fix.\
'''.format(_EXPECTED))
    sys.exit(2)

from pattoo_shared import data
from tests.libraries.configuration import UnittestConfig
from pattoo.db.table import user, chart, favorite, chart_datapoint
from pattoo.db.table import datapoint, agent
from pattoo.constants import DbRowUser, DbRowChart, DbRowFavorite
from pattoo.constants import DbRowChartDataPoint
from pattoo_shared.constants import DATA_FLOAT


def _idx_datapoint():
    """Create a new DataPoint db entry.

    Args:
        value: Value to convert

    Returns:
        result: idx_datapoint value for new DataPoint

    """
    # Initialize key variables
    polling_interval = 1

    # Create a new Agent entry
    agent_id = data.hashstring(str(random()))
    agent_target = data.hashstring(str(random()))
    agent_program = data.hashstring(str(random()))
    agent.insert_row(agent_id, agent_target, agent_program)
    idx_agent = agent.exists(agent_id, agent_target)

    # Create entry and check
    _checksum = data.hashstring(str(random()))
    result = datapoint.checksum_exists(_checksum)
    datapoint.insert_row(
        _checksum, DATA_FLOAT, polling_interval, idx_agent)
    result = datapoint.checksum_exists(_checksum)
    return result


class TestBasicFunctions(unittest.TestCase):
    """Checks all functions and methods."""

    def test_idx_exists(self):
        """Testing method or function named "idx_exists"."""
        # Add chart entry to database
        chart_name = data.hashstring(str(random()))
        chart_checksum = data.hashstring(str(random()))
        chart.insert_row(
            DbRowChart(name=chart_name, checksum=chart_checksum, enabled=0))

        # Make sure chart entry exists
        idx_chart = chart.exists(chart_checksum)
        self.assertTrue(bool(idx_chart))

        # Create idx datapoint
        idx_datapoint = _idx_datapoint()

        # Add chart datapoint entry to database
        chart_datapoint.insert_row(
            DbRowChartDataPoint(
                idx_datapoint=idx_datapoint,
                idx_chart=idx_chart,
                enabled=0
            )
        )

        # Make sure the chart datapoint exists
        idx_chart_datapoint = chart_datapoint.exists(idx_chart, idx_datapoint)

        # Verify that the index exists
        result = chart_datapoint.idx_exists(idx_chart_datapoint)
        self.assertTrue(result)

    def test_exists(self):
        """Testing method or function named "exists"."""
        # Add chart entry to database
        chart_name = data.hashstring(str(random()))
        chart_checksum = data.hashstring(str(random()))
        chart.insert_row(
            DbRowChart(name=chart_name, checksum=chart_checksum, enabled=0))

        # Make sure chart entry exists
        idx_chart = chart.exists(chart_checksum)

        # Create idx datapoint
        idx_datapoint = _idx_datapoint()

        # Subtest to make sure chart datapoint does not exist
        with self.subTest():
            result = chart_datapoint.exists(idx_chart, idx_datapoint)
            self.assertFalse(bool(result))

        # Add chart datapoint entry to database
        chart_datapoint.insert_row(
            DbRowChartDataPoint(
                idx_datapoint=idx_datapoint,
                idx_chart=idx_chart,
                enabled=0
            )
        )

        # Make sure the chart datapoint exists
        result = chart_datapoint.exists(idx_chart, idx_datapoint)
        self.assertTrue(bool(result))

    def test_insert_row(self):
        """Testing method or function named "insert_row"."""
        # Add chart entry to database
        chart_name = data.hashstring(str(random()))
        chart_checksum = data.hashstring(str(random()))
        chart.insert_row(
            DbRowChart(name=chart_name, checksum=chart_checksum, enabled=0))

        # Make sure chart entry exists
        idx_chart = chart.exists(chart_checksum)

        # Create idx datapoint
        idx_datapoint = _idx_datapoint()

        # Add chart datapoint entry to database
        chart_datapoint.insert_row(
            DbRowChartDataPoint(
                idx_datapoint=idx_datapoint,
                idx_chart=idx_chart,
                enabled=0
            )
        )

        # Make sure the chart datapoint exists
        idx_chart_datapoint = chart_datapoint.exists(idx_chart, idx_datapoint)

        # Verify that the index exists
        result = chart_datapoint.idx_exists(idx_chart_datapoint)
        self.assertTrue(result)


if __name__ == '__main__':
    # Make sure the environment is OK to run unittests
    UnittestConfig().create()

    # Do the unit test
    unittest.main()
