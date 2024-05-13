import logging
from exceptions import EnergyManagementError

class EnergyManager:
    """
    Manages the energy consumption and battery level of the drone, ensuring efficient use of power and safe operation.
    Enhanced to offer user control over critical decisions and integrate environmental factors affecting energy use.
    """
    def __init__(self, initial_battery_level=100, critical_level=20, return_home_callback=None, user_decision_callback=None):
        self.battery_level = initial_battery_level
        self.critical_level = critical_level
        self.auto_return_enabled = True
        self.return_home_callback = return_home_callback
        self.user_decision_callback = user_decision_callback
        self.logger = self.setup_logging()

    def setup_logging(self):
        """
        Set up a logger for energy management events.
        """
        logger = logging.getLogger('DroneEnergyManager')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('drone_energy_management.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def update_energy_usage(self, power_consumed, weather_impact=0):
        """
        Update the battery level based on power consumed and manage critical energy levels.
        Consider weather impacts on power consumption.
        """
        try:
            adjusted_consumption = power_consumed + weather_impact
            self.battery_level -= adjusted_consumption
            self.logger.info(f"Updated battery level: {self.battery_level}% after weather impact: {weather_impact}%")
            if self.battery_level <= self.critical_level:
                self.logger.warning("Critical battery level reached.")
                if self.auto_return_enabled:
                    decision = self.handle_user_decision()
                    if decision:
                        self.initiate_auto_return()
        except Exception as e:
            raise EnergyManagementError(f"Failed to update energy usage: {str(e)}")

    def handle_user_decision(self):
        """
        Handle user decisions regarding auto-return when battery is critical.
        """
        if self.user_decision_callback:
            return self.user_decision_callback()
        return True  # Default to auto-return if no user decision callback is provided

    def initiate_auto_return(self):
        """
        Automatically initiate return to home base if the battery level is critical.
        """
        try:
            self.logger.info("Initiating auto-return due to critical battery level.")
            if self.return_home_callback:
                self.return_home_callback()
        except Exception as e:
            raise EnergyManagementError(f"Failed to initiate auto-return: {str(e)}")

    def toggle_auto_return(self, enable):
        """
        Enable or disable the auto-return feature based on user preference.
        """
        self.auto_return_enabled = enable
        self.logger.info(f"Auto-return {'enabled' if enable else 'disabled'}.")

# Example usage can be :
def return_home():
    print("Drone is returning home due to low battery.")

def user_decision():
    # Simulate a user deciding whether to allow auto-return
    print("User decision: Allow auto-return.")
    return True  # Simulate user approval for auto-return

energy_manager = EnergyManager(return_home_callback=return_home, user_decision_callback=user_decision)
energy_manager.update_energy_usage(10, weather_impact=5)  # Simulate consumption of 10% battery and 5% additional due to weather
energy_manager.toggle_auto_return(True)
