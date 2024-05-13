import logging
import requests
from requests.exceptions import RequestException

class WeatherInteraction:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "WEBSITE URL_GOES_HERE_OF_API"
        self.logger = self.setup_logging()

    def setup_logging(self):
        logger = logging.getLogger('WeatherInteractionLogger')
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('weather_interaction.log')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def get_weather_data(self, city):
        url = f"{self.base_url}appid={self.api_key}&q={city}"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Will raise an exception for 4XX/5XX status codes
            return response.json()
        except RequestException as e:
            self.logger.error(f"Failed to retrieve weather data: {e}")
            return None

    def evaluate_weather_conditions(self, weather_data, user_override=False):
        if not weather_data or weather_data['cod'] != 200:
            self.logger.error("Invalid weather data received.")
            return False

        conditions = weather_data['weather'][0]['main']
        if conditions in ["Rain", "Snow", "Extreme"]:
            self.logger.warning(f"Adverse weather conditions detected: {conditions}")
            if user_override:
                self.logger.info("User has overridden the weather advisory.")
                return True
            else:
                self.logger.info("Flight not recommended due to weather conditions.")
                return False
        else:
            self.logger.info("Weather conditions are suitable for flight.")
            return True

# Example usage can be :  with API key and city
api_key = "your_api_key_here"
weather_interaction = WeatherInteraction(api_key)
city = "New York"
weather_data = weather_interaction.get_weather_data(city)
user_decision = True  # Simulate user input
flight_ready = weather_interaction.evaluate_weather_conditions(weather_data, user_decision)
