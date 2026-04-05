import sqlite3
import csv

def load_weather_data():
    csv_file = "clean_weather_2026-04-04.csv" # Ensure date matches your file
    db_file = "weather_warehouse.db"

    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # 1. THE FIX: We added a UNIQUE constraint on City + Date
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_weather (
            city TEXT,
            date TEXT,
            max_temp_celsius REAL,
            min_temp_celsius REAL,
            precipitation_mm REAL,
            max_wind_kmh REAL,
            UNIQUE(city, date)
        )
    ''')
    
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # 2. THE FIX: INSERT OR REPLACE (Upsert) instead of just INSERT
            cursor.execute('''
                INSERT OR REPLACE INTO daily_weather 
                (city, date, max_temp_celsius, min_temp_celsius, precipitation_mm, max_wind_kmh)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                row['city'], 
                row['date'], 
                row['max_temp_celsius'], 
                row['min_temp_celsius'], 
                row['precipitation_mm'], 
                row['max_wind_kmh']
            ))

    conn.commit()
    
    print("\n--- Current Data in Warehouse ---")
    cursor.execute("SELECT * FROM daily_weather")
    for record in cursor.fetchall():
        print(record)

    conn.close()

if __name__ == "__main__":
    load_weather_data()