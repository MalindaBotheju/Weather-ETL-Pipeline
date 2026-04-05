import time
# Import the functions we built in the other files
from extract import extract_weather_data
from transform import transform_weather_data
from load import load_weather_data

def run_pipeline():
    print("🚀 STARTING DAILY WEATHER PIPELINE...\n")
    
    try:
        # Step 1: Extract
        print("▶️ STEP 1: Running Extraction...")
        extract_weather_data()
        time.sleep(2) # Pausing for a second just so we can read the terminal
        
        # Step 2: Transform
        print("\n▶️ STEP 2: Running Transformation...")
        transform_weather_data()
        time.sleep(2)
        
        # Step 3: Load
        print("\n▶️ STEP 3: Running Load to Data Warehouse...")
        load_weather_data()
        
        print("\n✅ PIPELINE COMPLETED SUCCESSFULLY!")
        
    except Exception as e:
        # If any step fails, the pipeline stops and alerts us
        print(f"\n❌ PIPELINE FAILED! Error: {e}")

if __name__ == "__main__":
    run_pipeline()