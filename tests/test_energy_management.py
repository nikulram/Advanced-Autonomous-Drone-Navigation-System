import unittest
from unittest.mock import MagicMock
from energy_management import EnergyManager

class TestEnergyManager(unittest.TestCase):
    def setUp(self):
        self.initial_battery_level = 100
        self.critical_level = 20
        self.return_home_callback = MagicMock()
        self.user_decision_callback = MagicMock(return_value=True)
        self.energy_manager = EnergyManager(
            initial_battery_level=self.initial_battery_level,
            critical_level=self.critical_level,
            return_home_callback=self.return_home_callback,
            user_decision_callback=self.user_decision_callback
        )

    def test_update_energy_usage_normal(self):
        """Test energy usage update under normal conditions without reaching critical level."""
        power_consumed = 10
        self.energy_manager.update_energy_usage(power_consumed)
        expected_battery_level = self.initial_battery_level - power_consumed
        self.assertEqual(self.energy_manager.battery_level, expected_battery_level)
        self.return_home_callback.assert_not_called()

    def test_critical_battery_level(self):
        """Test automatic return initiation when reaching critical battery level."""
        power_consumed = 85  # Set a consumption that will drop battery level below critical level
        self.energy_manager.update_energy_usage(power_consumed)
        self.assertTrue(self.energy_manager.battery_level <= self.critical_level)
        self.return_home_callback.assert_called_once()

    def test_user_decision_override(self):
        """Test user decision override when critical level is reached."""
        self.user_decision_callback.return_value = False  # User decides not to return home
        power_consumed = 85
        self.energy_manager.update_energy_usage(power_consumed)
        self.return_home_callback.assert_not_called()

    def test_auto_return_toggle(self):
        """Test toggling the auto-return functionality."""
        self.energy_manager.toggle_auto_return(False)
        self.assertFalse(self.energy_manager.auto_return_enabled)
        self.energy_manager.toggle_auto_return(True)
        self.assertTrue(self.energy_manager.auto_return_enabled)

if __name__ == '__main__':
    unittest.main()
