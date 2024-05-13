import unittest
from unittest.mock import patch, MagicMock
import requests
from weather_interaction import WeatherInteraction

class TestWeatherInteraction(unittest.TestCase):
    def setUp(self):
        self.api_key = "fake_api_key"
        self.weather_interaction = WeatherInteraction(self.api_key)
        self.sample_weather_response = {
            "weather": [{"main": "Clear"}],
            "cod": 200
        }

    def test_get_weather_data_success(self):
        """Test successful retrieval of weather data."""
        with patch('requests.get') as mock_get:
            mock_get.return_value.ok = True
            mock_get.return_value.json = MagicMock(return_value=self.sample_weather_response)
            
            response = self.weather_interaction.get_weather_data("New York")
            self.assertIsNotNone(response)
            self.assertEqual(response['weather'][0]['main'], 'Clear')

    def test_get_weather_data_failure(self):
        """Test failure in retrieving weather data logs an error."""
        with patch('requests.get', side_effect=requests.exceptions.RequestException("Connection error")):
            with self.assertLogs('WeatherInteractionLogger', level='ERROR') as cm:
                self.assertIsNone(self.weather_interaction.get_weather_data("New York"))
            self.assertIn("Failed to retrieve weather data", cm.output[0])

    def test_evaluate_weather_conditions(self):
        """Test evaluation of weather conditions."""
        # Test adverse condition without override
        self.assertFalse(self.weather_interaction.evaluate_weather_conditions({"weather": [{"main": "Rain"}], "cod": 200}, False))
        
        # Test clear condition
        self.assertTrue(self.weather_interaction.evaluate_weather_conditions(self.sample_weather_response, False))

if __name__ == '__main__':
    unittest.main()
