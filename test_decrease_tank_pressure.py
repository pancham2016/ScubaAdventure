import unittest
from scoreboard import decrease_tank_pressure

class TankTestCase(unittest.TestCase):
    """Class that tests for 'decrease_tank_pressure'."""

    def test_tank_pressure(self):
        """Will the tank pressure decrease after a certain amount of time."""