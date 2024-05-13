import unittest
import numpy as np
from navigation import NavigationSystem
from exceptions import SensorError, CriticalNavigationError

class TestNavigationSystem(unittest.TestCase):
    def setUp(self):
        self.nav_system = NavigationSystem()

    def test_initialization(self):
        """ Test if the Kalman filter and state are initialized correctly. """
        self.assertIsNotNone(self.nav_system.kalman_filter, "Kalman filter should be initialized.")
        self.assertEqual(len(self.nav_system.state), 6, "State vector should have 6 elements.")

    def test_state_update(self):
        """ Test the state update with simulated sensor data. """
        initial_state = self.nav_system.state.copy()
        sensor_data = np.array([1, 2, 3, 0.1, 0.1, 0.1])
        self.nav_system.update_navigation_state(sensor_data)
        self.assertFalse(np.array_equal(self.nav_system.state, initial_state), "State should change after processing sensor data.")

    def test_error_handling(self):
        """ Test handling of erroneous sensor data. """
        sensor_data = np.array([np.nan, np.inf, -np.inf, np.nan, np.inf, -np.inf])  # Invalid data
        with self.assertRaises(SensorError):
            self.nav_system.update_navigation_state(sensor_data)

if __name__ == '__main__':
    unittest.main()
