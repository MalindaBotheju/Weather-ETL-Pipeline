import json
import csv

def transform_weather_data():
    # 1. Open the raw Data Lake file we just created
    # (Update the date below if needed)
    raw_file = "raw_weather_2026-04-04.json"
    
    with open(raw_file, "r") as f:
        raw_data = json.load(f)

    clean_data = []

    print("Starting data transformation...")

    # 2. Loop through the messy data and flatten it
    for city_data in raw_data:
        city_name = city_data["city_name"]
        
        # The API gives us lists, so we pull the first item [0] from each list
        date = city_data["daily"]["time"][0]
        max_temp = city_data["daily"]["temperature_2m_max"][0]
        min_temp = city_data["daily"]["temperature_2m_min"][0]
        precip = city_data["daily"]["precipitation_sum"][0]
        wind = city_data["daily"]["wind_speed_10m_max"][0]

        # 3. Create a clean, flat dictionary (a perfect row of data)
        clean_row = {
            "city": city_name,
            "date": date,
            "max_temp_celsius": max_temp,
            "min_temp_celsius": min_temp,
            "precipitation_mm": precip,
            "max_wind_kmh": wind
        }
        
        clean_data.append(clean_row)

    # 4. Save the clean data as a CSV (Ready for a Database or ML Model!)
    csv_file = "clean_weather_2026-04-04.csv"
    
    # Write to CSV
    with open(csv_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["city", "date", "max_temp_celsius", "min_temp_celsius", "precipitation_mm", "max_wind_kmh"])
        writer.writeheader()
        writer.writerows(clean_data)

    print(f"Transformation complete! Clean data saved to {csv_file}")

if __name__ == "__main__":
    transform_weather_data()