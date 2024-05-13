import random
import time
import logging

class AdaptiveFrequencyHopper:
    """
    Manages frequency hopping to maintain secure and reliable communication for the drone, adaptable to swarm coordination and weather conditions.
    """
    def __init__(self, available_frequencies, min_signal_quality=0.3, hop_interval=10, weather_impact_callback=None):
        self.available_frequencies = available_frequencies
        self.min_signal_quality = min_signal_quality
        self.hop_interval = hop_interval
        self.current_frequency = random.choice(available_frequencies)
        self.last_hop_time = time.time()
        self.weather_impact_callback = weather_impact_callback
        self.user_override = False
        self.logger = self.setup_logging()

    def setup_logging(self):
        """
        Setup a logger for frequency hopping events.
        """
        logger = logging.getLogger('DroneFrequencyHopper')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('frequency_hopping.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def get_current_signal_quality(self):
        """
        Obtain the current signal quality, potentially adjusted for weather impacts.
        """
        quality = random.uniform(0, 1)  # Simulated quality from 0 (poor) to 1 (excellent)
        if self.weather_impact_callback:
            quality = self.weather_impact_callback(quality)
        return quality

    def check_and_hop(self):
        """
        Check if conditions warrant a frequency hop and execute if necessary, unless overridden by the user.
        """
        if self.user_override:
            self.logger.info("User has overridden frequency hopping.")
            return

        current_time = time.time()
        if (current_time - self.last_hop_time) >= self.hop_interval:
            self.hop_frequency()
        current_signal_quality = self.get_current_signal_quality()
        if current_signal_quality < self.min_signal_quality:
            self.hop_frequency()

    def hop_frequency(self):
        """
        Hop to a new frequency based on the conditions.
        """
        old_frequency = self.current_frequency
        self.current_frequency = random.choice([f for f in self.available_frequencies if f != old_frequency])
        self.last_hop_time = time.time()
        self.logger.info(f"Hopped from {old_frequency} GHz to {self.current_frequency} GHz due to conditions.")

    def user_override_hopping(self, enable):
        """
        Allow the user to enable or disable automatic frequency hopping.
        """
        self.user_override = enable
        self.logger.info(f"User override {'enabled' if enable else 'disabled'} for frequency hopping.")

# Example usage (for demonstration purposes only!) :
def weather_impact_on_signal_quality(quality):
    """
    Dummy function to simulate the effect of weather on signal quality.
    """
    return quality * 0.9  #suppose weather reduces signal quality by 10%

frequencies = [2.4, 2.425, 2.45, 2.475, 2.5]  # Possible frequencies in GHz
hopper = AdaptiveFrequencyHopper(frequencies, weather_impact_callback=weather_impact_on_signal_quality)
hopper.user_override_hopping(True)  # Enable user control over frequency hopping
while True:
    hopper.check_and_hop()
    time.sleep(1)  # Regular interval check
