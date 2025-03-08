import requests
from datetime import datetime
import os

class WeatherAPI:
    BASE_URL = "https://api.weatherapi.com/v1"
    
    def __init__(self):
        self.api_key = os.getenv("WEATHER_API_KEY")
        
    def get_forecast(self, city, date):
        """Get weather forecast for a specific date"""
        try:
            response = requests.get(
                f"{self.BASE_URL}/forecast.json",
                params={
                    "key": self.api_key,
                    "q": city,
                    "dt": date
                }
            )
            response.raise_for_status()
            data = response.json()
            
            forecast = data['forecast']['forecastday'][0]['day']
            return {
                'max_temp': forecast['maxtemp_c'],
                'min_temp': forecast['mintemp_c'],
                'condition': forecast['condition']['text'],
                'icon': forecast['condition']['icon']
            }
        except Exception as e:
            print(f"Error fetching weather: {e}")
            return None

# Create singleton instance
weather_api = WeatherAPI()
