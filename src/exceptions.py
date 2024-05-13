class NavigationError(Exception):
    """Exception raised for errors in the navigation system."""
    def __init__(self, message="An error occurred in navigation"):
        super().__init__(message)

class CriticalNavigationError(Exception):
    """Exception raised for errors that are critical for the navigation system."""
    def __init__(self, message="Critical error in navigation system"):
        self.message = message
        super().__init__(self.message)

class PathfindingError(Exception):
    """Exception raised when pathfinding fails due to missing nodes or blocked paths."""
    def __init__(self, message="Pathfinding error"):
        super().__init__(message)

class SensorError(Exception):
    """Exception raised when there are issues with any of the drone's sensors."""
    def __init__(self, sensor, message="Error with sensor operation"):
        self.sensor = sensor
        self.message = f"{message}: {sensor}"
        super().__init__(self.message)

class EnergyManagementError(Exception):
    """Exception raised for errors in energy management and critical battery levels."""
    def __init__(self, level, message="Energy management issue detected"):
        self.level = level
        self.message = f"{message} at {level}% battery level"
        super().__init__(self.message)

class FlightPlanError(Exception):
    """Exception raised for errors in flight planning, such as invalid waypoints or pathfinding issues."""
    def __init__(self, details, message="Flight plan could not be completed"):
        self.details = details
        self.message = f"{message}: {details}"
        super().__init__(self.message)

class SwarmControlError(Exception):
    """Exception raised for errors in controlling the drone swarm."""
    def __init__(self, drone_id, task=None, message="Error in swarm task management"):
        self.drone_id = drone_id
        self.task = task
        self.message = f"{message} - Drone ID: {drone_id}, Task: {task}"
        super().__init__(self.message)

class WeatherImpactError(Exception):
    """Exception raised for operational decisions affected by adverse weather conditions."""
    def __init__(self, condition, message="Adverse weather condition affecting operation"):
        self.condition = condition
        self.message = f"{message}: {condition}"
        super().__init__(self.message)

class ObstacleDetectionError(Exception):
    """Exception raised when there is an error in detecting obstacles."""
    def __init__(self, message="Failed to detect obstacles correctly"):
        super().__init__(message)

class EmergencyHandlingError(Exception):
    """Exception raised for errors during the handling of emergencies."""
    def __init__(self, message="Error handling emergency"):
        super().__init__(message)
