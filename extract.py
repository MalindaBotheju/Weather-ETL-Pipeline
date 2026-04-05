import requests
import json
from datetime import datetime, timedelta

def extract_weather_data():
    # 1. Define the cities and their coordinates (Latitude, Longitude)
    cities = {
        "New_York": {"lat": 40.7128, "lon": -74.0060},
        "London": {"lat": 51.5074, "lon": -0.1278},
        "Tokyo": {"lat": 35.6762, "lon": 139.6503}
    }

    # 2. We want yesterday's data (so we have a complete 24-hour record)
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    
    all_weather_data = []

    print(f"Starting extraction for date: {yesterday}...")

    # 3. Loop through each city and hit the API
    for city, coords in cities.items():
        print(f"Pulling data for {city}...")
        
        url = f"https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": coords["lat"],
            "longitude": coords["lon"],
            "start_date": yesterday,
            "end_date": yesterday,
            "daily": ["temperature_2m_max", "temperature_2m_min", "precipitation_sum", "wind_speed_10m_max"],
            "timezone": "auto"
        }

        # Send the request to the API
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            # Add the city name so we know whose data this is
            data["city_name"] = city  
            all_weather_data.append(data)
        else:
            print(f"Failed to get data for {city}. Status code: {response.status_code}")

    # 4. Dump the raw, untouched data into a JSON file (Our "Data Lake" drop)
    file_name = f"raw_weather_{yesterday}.json"
    with open(file_name, "w") as f:
        json.dump(all_weather_data, f, indent=4)

    print(f"Extraction complete! Raw data saved to {file_name}")

if __name__ == "__main__":
    extract_weather_data()