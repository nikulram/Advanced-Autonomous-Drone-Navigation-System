import logging
from threading import Thread
import random
import time

class DroneSwarm:
    """
    A class to manage a swarm of drones, handling tasks assignments and execution, including emergency handling and user overrides.
    """

    def __init__(self, drone_ids, control_station_callback):
        """
        Initialize the DroneSwarm class with a set of drone IDs and a callback function for the control station.

        Args:
            drone_ids (list): List of unique identifiers for each drone in the swarm.
            control_station_callback (function): Callback function to send updates to the control station.
        """
        # Set up the drones with initial ready status and no assigned tasks
        self.drones = {drone_id: {'status': 'ready', 'task': None} for drone_id in drone_ids}
        self.control_station_callback = control_station_callback
        self.logger = self.setup_logging()  # Initialize logging

    def setup_logging(self):
        """
        Configure logging for drone swarm operations.

        Returns:
            Logger object with specified settings.
        """
        logger = logging.getLogger('DroneSwarmLogger')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('drone_swarm.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def assign_task(self, drone_id, task):
        """
        Assign a task to a specific drone if it is ready.

        Args:
            drone_id (str): The identifier for the drone.
            task (str): The task to be assigned to the drone.
        """
        if drone_id in self.drones and self.drones[drone_id]['status'] == 'ready':
            self.drones[drone_id]['task'] = task
            self.drones[drone_id]['status'] = 'busy'
            self.logger.info(f"Task '{task}' assigned to drone {drone_id}.")
            self.execute_task(drone_id, task)
        else:
            self.logger.error(f"Drone {drone_id} is not ready or does not exist.")

    def execute_task(self, drone_id, task):
        """
        Start the execution of a task by a drone in a separate thread.

        Args:
            drone_id (str): The identifier of the drone executing the task.
            task (str): The task to be executed.
        """
        def task_simulation():
            self.logger.info(f"Drone {drone_id} starting task: {task}.")
            time.sleep(random.randint(1, 5))  # Simulate task duration
            self.drones[drone_id]['status'] = 'ready'
            self.drones[drone_id]['task'] = None
            self.logger.info(f"Drone {drone_id} has completed task: {task}.")
            self.control_station_callback('task_completed', {'drone_id': drone_id, 'task': task})
        
        task_thread = Thread(target=task_simulation)
        task_thread.start()

    def emergency_landing(self, drone_id):
        """
        Initiate an emergency landing for a specific drone.

        Args:
            drone_id (str): The identifier of the drone.
        """
        if drone_id in self.drones:
            self.drones[drone_id]['status'] = 'emergency'
            self.logger.warning(f"Emergency landing initiated for Drone {drone_id}.")
            self.control_station_callback('emergency_landing', {'drone_id': drone_id})

    def user_override(self, drone_id, action):
        """
        Handle user override actions for a drone.

        Args:
            drone_id (str): The identifier of the drone.
            action (str): The override action to take ('cancel_task' or 'proceed_with_task').
        """
        if drone_id in self.drones and action in ['cancel_task', 'proceed_with_task']:
            if action == 'cancel_task':
                self.drones[drone_id]['status'] = 'ready'
                self.drones[drone_id]['task'] = None
                self.logger.info(f"Task for Drone {drone_id} has been cancelled by user.")
            elif action == 'proceed_with_task':
                self.logger.info(f"Drone {drone_id} will continue with task: {self.drones[drone_id]['task']}.")
            self.control_station_callback('user_override', {'drone_id': drone_id, 'action': action})
        else:
            self.logger.error(f"Invalid action or drone ID: {drone_id}")

def control_station_callback(event_type, details):
    """
    Control station callback to handle events reported by drones.

    Args:
        event_type (str): The type of event reported.
        details (dict): Additional details about the event.
    """
    print(f"Event: {event_type}, Details: {details}")

# Example usage can be :
swarm = DroneSwarm(['drone1', 'drone2', 'drone3'], control_station_callback)
swarm.assign_task('drone1', 'photography')
