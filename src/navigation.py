import numpy as np
from filterpy.kalman import KalmanFilter
from exceptions import CriticalNavigationError, SensorError

class NavigationSystem:
    """
    Manages the drone's navigation by continuously updating its position and orientation based on sensor inputs.
    """
    def __init__(self):
        # Initialize the state vector with position and velocity (x, y, z, vx, vy, vz)
        self.state = np.zeros(6)
        self.kalman_filter = self.initialize_kalman_filter()

    def initialize_kalman_filter(self):
        """
        Setup a Kalman Filter for estimating position and velocity from noisy sensor data.
        """
        kf = KalmanFilter(dim_x=6, dim_z=6)
        kf.F = np.array([[1, 0, 0, 1, 0, 0],  # State transition matrix
                         [0, 1, 0, 0, 1, 0],
                         [0, 0, 1, 0, 0, 1],
                         [0, 0, 0, 1, 0, 0],
                         [0, 0, 0, 0, 1, 0],
                         [0, 0, 0, 0, 0, 1]])
        kf.H = np.eye(6)  # Measurement function
        kf.R *= 0.05  # Measurement uncertainty
        kf.P *= 1000  # Initial state uncertainty
        kf.Q = np.eye(6) * 0.01  # Process noise
        return kf

    def update_navigation_state(self, sensor_data):
        """
        Update the navigation state based on new sensor data.
        Raise SensorError if sensor data is invalid.
        """
        if np.any(np.isnan(sensor_data)) or np.any(np.isinf(sensor_data)):
            raise SensorError("Invalid sensor data received.")
        try:
            self.kalman_filter.predict()
            self.kalman_filter.update(sensor_data)
            self.state = self.kalman_filter.x
        except Exception as e:
            raise CriticalNavigationError(f"Failed to update navigation state: {str(e)}")

    def get_position(self):
        """
        Return the current estimated position.
        """
        return self.state[:3]

    def get_velocity(self):
        """
        Return the current estimated velocity.
        """
        return self.state[3:6]


# Example usage can be:
# navigation_system = NavigationSystem()
# try:
#     new_sensor_data = np.array([1, 2, 3, 0.1, 0.1, 0.1])  # Example sensor data (position and velocity)
#     navigation_system.update_navigation_state(new_sensor_data)
#     print("Current Position:", navigation_system.get_position())
#     print("Current Velocity:", navigation_system.get_velocity())
# except CriticalNavigationError as e:
#     print(f"Navigation error occurred: {e}")
