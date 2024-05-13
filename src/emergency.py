import logging
from exceptions import EmergencyHandlingError

class EmergencyHandler:
    """
    Manages and responds to emergency situations for the drone, ensuring safety and operational integrity.
    Provides user options to override or confirm emergency protocols.
    """
    def __init__(self, control_station_callback, user_decision_callback=None):
        self.emergency_status = False
        self.control_station_callback = control_station_callback
        self.user_decision_callback = user_decision_callback
        self.logger = self.setup_logging()

    def setup_logging(self):
        """
        Set up a logger for emergency events.
        """
        logger = logging.getLogger('DroneEmergencyHandler')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('drone_emergency.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def detect_emergency(self, system_checks):
        """
        Analyze system parameters to detect potential emergencies.
        Resets the emergency status for each check to ensure accurate current status.
        """
        self.emergency_status = False  # Reset status each time the function is called
        if not all(system_checks.values()):
            self.emergency_status = True
            try:
                self.handle_emergency(system_checks)
            except Exception as e:
                self.logger.error(f"Failed to handle emergency properly: {str(e)}")
                raise EmergencyHandlingError(f"Handling emergency failed: {str(e)}")
        else:
            self.logger.info("No emergency detected.")
            self.control_station_callback('no_emergency', {})

    def handle_emergency(self, system_checks):
        """
        Handle detected emergencies by executing predefined protocols and notifying the control station.
        Offer user decisions on emergency protocols if user_decision_callback is set.
        """
        emergency_details = {k: v for k, v in system_checks.items() if not v}
        if not emergency_details:
            raise EmergencyHandlingError("No specific emergency conditions identified.")

        protocol = 'return_to_home' if 'power_failure' in emergency_details else 'safe_landing'
        self.logger.error(f"Emergency detected! System failures: {emergency_details}")

        user_decision = 'confirm' if not self.user_decision_callback else self.user_decision_callback(protocol, emergency_details)
        
        if user_decision == 'override':
            self.logger.info("User has overridden the default protocol. Continuing normal operations.")
            self.control_station_callback('user_override', {})
        else:
            self.execute_protocol(protocol, emergency_details)

    def execute_protocol(self, protocol, details):
        """
        Execute specific emergency protocols based on the situation.
        Notifies the control station with detailed protocol execution information.
        """
        self.logger.info(f"Executing {protocol} due to {details}")
        self.control_station_callback('emergency_detected', details)
        if protocol == 'return_to_home':
            self.logger.info("Power failure detected. Returning to home.")
        elif protocol == 'safe_landing':
            self.logger.info("Critical error detected. Performing safe landing.")
