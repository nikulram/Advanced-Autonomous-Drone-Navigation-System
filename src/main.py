import tkinter as tk
from threading import Thread
import time

# Import system components
from frequency_hopper import AdaptiveFrequencyHopper
from drone_encryption import DroneEncryption
from energy_management import EnergyManager
from sensor import SensorInput
from navigation import NavigationSystem
from obstacle import ObstacleDetector
from flight_plan import FlightPlanner
from decision_maker import DecisionMaker 
from user_interface import DroneControlPanel
from emergency import EmergencyHandler
from drone_swarm import DroneSwarm
from weather_interaction import WeatherInteraction
from exceptions import CriticalNavigationError, SensorError

class DroneNavigationSystem:
    """
    Integrates various modules to control and monitor drone operations comprehensively.
    Includes management of drone swarms and interactions with weather systems.
    """
    def __init__(self, master):
        self.master = master
        self.ui = DroneControlPanel(master)
        self.setup_components()

    def setup_components(self):
        # Setup individual components of the drone navigation system
        self.weather_interaction = WeatherInteraction(api_key='your_api_key_here')
        self.swarm = DroneSwarm(drone_ids=['drone1', 'drone2', 'drone3'], control_station_callback=self.swarm_callback)

        self.hopper = AdaptiveFrequencyHopper(available_frequencies=[2.4, 2.425, 2.45, 2.475, 2.5])
        self.encryption = DroneEncryption()
        self.energy_manager = EnergyManager(return_home_callback=self.return_home)
        self.sensor = SensorInput(camera_index=0, lidar_config={'port': '/dev/ttyUSB0'})
        self.navigation = NavigationSystem()
        self.obstacle_detector = ObstacleDetector('camera_model.pth', 'lidar_model.pth')
        self.flight_planner = FlightPlanner(destination=[100, 100, 100])
        self.decision_maker = DecisionMaker('decision_model.pth')  # Path to your trained model
        self.emergency_handler = EmergencyHandler(self.handle_emergency)
        
        # UI button configurations
        self.ui.start_button.config(command=self.start_operation_thread)
        self.ui.stop_button.config(command=self.stop_operation)

    def swarm_callback(self, event_type, details):
        """Handle events from the drone swarm, such as task completions and emergencies."""
        self.ui.log_data(f"Swarm Event: {event_type}, Details: {details}")

    def start_operation_thread(self):
        """Start drone operations in a separate thread to keep the UI responsive."""
        self.operation_thread = Thread(target=self.start_operation)
        self.operation_thread.start()

    def start_operation(self):
        """Main operational loop integrating all drone systems, with enhanced error handling and logging."""
        running = True
        try:
            while running:
                # Check weather conditions before starting operations
                weather_data = self.weather_interaction.get_weather_data("New York")
                if not self.weather_interaction.evaluate_weather_conditions(weather_data, user_override=True):
                    self.ui.log_data("Weather conditions are not suitable for flying.")
                    break

                # Drone operation tasks
                camera_data = self.sensor.get_camera_data()
                lidar_data = self.sensor.get_lidar_data()
                position = self.navigation.get_position()
                obstacles = self.obstacle_detector.detect_obstacles_camera(camera_data)
                flight_path = self.flight_planner.find_path(position)
                decision = self.decision_maker.make_decision(camera_data, lidar_data) 
                self.ui.log_data(f"Navigation update: Position {position}, Path {flight_path}, Decision {decision}")
                time.sleep(1)  # Simulate operational delay
        finally:
            self.ui.log_data("Cleaning up operations...")
            self.cleanup_operations()

    def handle_operation_error(self, error):
        """Handle specific errors and decide whether to continue operations."""
        if isinstance(error, CriticalNavigationError):
            self.ui.log_data("Critical error in navigation, stopping operations.")
            return False
        elif isinstance(error, SensorError):
            self.ui.log_data("Sensor error handled, attempting to continue.")
            return True
        else:
            self.ui.log_data("Unhandled error type, stopping operations.")
            return False

    def cleanup_operations(self):
        """Clean up resources and ensure system is in a safe state before closing."""
        self.sensor.release_resources()
        self.ui.log_data("System cleaned up and ready to close.")

    def stop_operation(self):
        """Safely stop all drone operations."""
        if self.operation_thread.is_alive():
            self.operation_thread.join()
        self.ui.log_data("Drone operations stopped.")

    def handle_emergency(self, message):
        """Respond to emergencies by logging and performing necessary actions."""
        self.ui.log_data(message)
        self.stop_operation()

    def return_home(self):
        """Command the drone to return to its home location."""
        self.ui.log_data("Low battery: Returning home.")

# Main execution
if __name__ == "__main__":
    root = tk.Tk()
    drone_system = DroneNavigationSystem(root)
    root.mainloop()
