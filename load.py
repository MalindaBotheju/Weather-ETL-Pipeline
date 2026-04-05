import psycopg2
import csv
import os
from dotenv import load_dotenv

# Load the hidden database URL from the .env file
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

def load_weather_data():
    csv_file = "clean_weather_2026-04-04.csv" # Update to match your CSV date if needed
    
    print("Connecting to Supabase Cloud Data Warehouse...")
    
    # 1. Connect to PostgreSQL
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    # 2. Create the table in the cloud
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS daily_weather (
            city VARCHAR(255),
            date DATE,
            max_temp_celsius REAL,
            min_temp_celsius REAL,
            precipitation_mm REAL,
            max_wind_kmh REAL,
            UNIQUE(city, date)
        )
    ''')
    
    print("Table verified. Upserting data to the cloud...")

    # 3. Read the CSV and Upsert into PostgreSQL
    with open(csv_file, "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cursor.execute('''
                INSERT INTO daily_weather 
                (city, date, max_temp_celsius, min_temp_celsius, precipitation_mm, max_wind_kmh)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (city, date) 
                DO UPDATE SET 
                    max_temp_celsius = EXCLUDED.max_temp_celsius,
                    min_temp_celsius = EXCLUDED.min_temp_celsius,
                    precipitation_mm = EXCLUDED.precipitation_mm,
                    max_wind_kmh = EXCLUDED.max_wind_kmh;
            ''', (
                row['city'], 
                row['date'], 
                row['max_temp_celsius'], 
                row['min_temp_celsius'], 
                row['precipitation_mm'], 
                row['max_wind_kmh']
            ))

    # 4. Commit and close
    conn.commit()
    print("Data successfully loaded into Supabase!")

    # 5. Prove it worked
    print("\n--- Current Data in Cloud Warehouse ---")
    cursor.execute("SELECT * FROM daily_weather")
    for record in cursor.fetchall():
        print(record)

    cursor.close()
    conn.close()

if __name__ == "__main__":
    load_weather_data()