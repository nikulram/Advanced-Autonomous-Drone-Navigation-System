"""
Drone Navigation System Package
-------------------------------
Initializes the drone navigation system with all components integrated.
This package handles various functionalities such as navigation, communication,
obstacle detection, and decision making based on sensor inputs and image data.
"""

import logging
from .decision_net import DecisionNet  # Importing the neural network for decision making
from .decision_maker import DecisionMaker  # Importing the decision-making component

# Set up a logger for the entire drone package
def setup_package_logging():
    """ Sets up a package-wide logging configuration. """
    logger = logging.getLogger('DronePackage')
    logger.setLevel(logging.INFO)

    # File handler for detailed debug logs
    fh = logging.FileHandler('drone_package.log')
    fh.setLevel(logging.DEBUG)

    # Console handler for critical errors and higher level messages
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # Formatter to define the log message format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # Adding handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

# Initialize logging for the package
package_logger = setup_package_logging()
package_logger.info('Initializing the Drone Navigation System package')

# Import and expose the key components of the package
from .frequency_hopper import AdaptiveFrequencyHopper
from .drone_encryption import DroneEncryption
from .energy_management import EnergyManager
from .sensor import SensorInput
from .navigation import NavigationSystem
from .obstacle import ObstacleDetector
from .flight_plan import FlightPlanner
from .user_interface import DroneControlPanel
from .emergency import EmergencyHandler
from .drone_swarm import DroneSwarm
from .weather_interaction import WeatherInteraction

# Notify that the package has been initialized
package_logger.info('Drone Navigation System package initialized successfully.')

# List of publicly exposed modules
__all__ = [
    "AdaptiveFrequencyHopper",
    "DroneEncryption",
    "EnergyManager",
    "SensorInput",
    "NavigationSystem",
    "ObstacleDetector",
    "FlightPlanner",
    "DecisionMaker",
    "DecisionNet",
    "DroneControlPanel",
    "EmergencyHandler",
    "DroneSwarm",
    "WeatherInteraction"
]
