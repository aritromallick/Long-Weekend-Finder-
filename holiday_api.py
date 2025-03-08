import requests
from datetime import datetime
from typing import List, Dict, Optional
import json
import os

class HolidayAPI:
    BASE_URL = "https://date.nager.at/api/v3"
    CACHE_FILE = "holiday_cache.json"
    
    def __init__(self):
        self.cache = self._load_cache()
    
    def _load_cache(self) -> dict:
        if os.path.exists(self.CACHE_FILE):
            try:
                with open(self.CACHE_FILE, 'r') as f:
                    return json.load(f)
            except:
                return {}
        return {}
    
    def _save_cache(self):
        with open(self.CACHE_FILE, 'w') as f:
            json.dump(self.cache, f)
    
    def _get_cache_key(self, country: str, year: int) -> str:
        return f"{country}_{year}"
    
    def get_holidays(self, country_code: str, year: int) -> List[Dict]:
        """
        Get holidays for a specific country and year
        
        Args:
            country_code: ISO country code (e.g., 'IN' for India)
            year: Year to get holidays for
            
        Returns:
            List of holiday dictionaries
        """
        cache_key = self._get_cache_key(country_code, year)
        
        # Check cache first
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            response = requests.get(f"{self.BASE_URL}/PublicHolidays/{year}/{country_code}")
            response.raise_for_status()
            
            holidays = []
            for holiday in response.json():
                holidays.append({
                    "date": holiday["date"],
                    "name": holiday["name"],
                    "day": datetime.strptime(holiday["date"], "%Y-%m-%d").strftime("%A")
                })
            
            # Cache the results
            self.cache[cache_key] = holidays
            self._save_cache()
            
            return holidays
            
        except requests.RequestException as e:
            print(f"Error fetching holidays: {e}")
            # Fallback to local data if available
            return self._get_fallback_holidays(country_code, year)
    
    def _get_fallback_holidays(self, country_code: str, year: int) -> List[Dict]:
        """Fallback to local holiday data if API fails"""
        try:
            with open('holidays.json', 'r') as f:
                data = json.load(f)
                country_map = {'IN': 'India'}  # Add more mappings as needed
                country_name = country_map.get(country_code)
                if country_name and str(year) in data.get(country_name, {}):
                    return data[country_name][str(year)]
        except:
            pass
        return []

# Create singleton instance
holiday_api = HolidayAPI()
