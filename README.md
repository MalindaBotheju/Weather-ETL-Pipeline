I completely understand—the "Power BI" drag-and-drop stuff feels like a chore when you’re here for the actual engineering. Since you've successfully built a live cloud-connected pipeline, let’s wrap this up with a professional `README.md`.

This file documents the hard work: the API integration, the database architecture, and the cloud connection.

---

# Weather Data Engineering Pipeline

A containerized ETL (Extract, Transform, Load) pipeline that fetches global weather data and stores it in a cloud-hosted PostgreSQL database for real-time visualization.

## 🚀 Project Overview
This project automates the collection of weather metrics for major global cities. It bridges the gap between raw API data and a cloud-based Business Intelligence (BI) layer.

### Tech Stack
* **Language:** Python 3.x
* **API:** Open-Meteo (Historical & Current Weather)
* **Database:** PostgreSQL (Hosted on **Supabase**)
* **Visualization:** Google Looker Studio
* **Libraries:** `pandas`, `sqlalchemy`, `psycopg2-binary`, `requests`

---

## 🛠️ Data Pipeline Architecture

### 1. Extraction (API Layer)
The script targets specific coordinates for **New York**, **London**, and **Tokyo**. It requests a 5-day window of historical weather data including:
* Temperature (Max/Min)
* Precipitation
* Wind Speed

### 2. Transformation (Processing Layer)
* Converts raw JSON responses into structured **Pandas DataFrames**.
* Cleans and renames columns for database compatibility.
* Handles unit conversions (Celsius and KM/H).

### 3. Loading (Cloud Database Layer)
* Establishes a secure connection to **Supabase** via SQLAlchemy.
* Uses an `IF EXISTS: APPEND` logic to ensure data is updated without overwriting historical records.
* Enforces **SSL encryption** for secure data transit.

---

## 📊 Database Schema (`daily_weather`)

| Column | Type | Description |
| :--- | :--- | :--- |
| **date** | DATE | The date of the weather reading |
| **city** | TEXT | City name (Primary key context) |
| **max_temp_celsius** | FLOAT | Maximum daily temperature |
| **min_temp_celsius** | FLOAT | Minimum daily temperature |
| **precipitation_mm** | FLOAT | Total daily rainfall |
| **max_wind_kmh** | FLOAT | Peak wind speed |

---

## 🔑 Setup & Connection Notes

### Cloud Configuration
To replicate the connection in Looker Studio or any other BI tool:
* **Connector:** PostgreSQL
* **Host:** `db.zyyhodigkrfifqvqhvel.supabase.co`
* **Port:** `5432`
* **User/DB:** `postgres`
* **SSL:** Enabled (Required for Supabase)

### Running the Script
1. Install dependencies: `pip install pandas sqlalchemy requests psycopg2-binary`
2. Configure the database password in the connection string.
3. Execute the pipeline: `python weather_pipeline.py`

---

## 🏁 Future Improvements
* **Automation:** Deploy as a GitHub Action or Cron job to run every 24 hours.
* **Scaling:** Add more cities by updating the `cities` dictionary in the source code.
* **Monitoring:** Add logging to track successful API hits and database inserts.