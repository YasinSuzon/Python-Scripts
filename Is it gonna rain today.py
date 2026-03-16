import requests
import time
import os
from datetime import datetime

def get_dhaka_hourly_rain():
    # Coordinates for Dhaka, Bangladesh
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": 23.7104,
        "longitude": 90.4074,
        "hourly": ["precipitation_probability", "precipitation"],
        "timezone": "auto",
        "forecast_days": 1
    }

    try:
        # Clear the terminal screen (works for Windows and Mac/Linux)
        os.system('cls' if os.name == 'nt' else 'clear')
        
        response = requests.get(url, params=params)
        data = response.json()
        
        current_time = datetime.now().strftime("%Y-%m-%d %I:%M %p")
        print(f"=== DHAKA RAIN TRACKER ===")
        print(f"Last Updated: {current_time}")
        print("-" * 30)

        hourly_data = data['hourly']
        found_rain = False

        print("Upcoming Rain Times (Next 24 Hours):")
        for i in range(len(hourly_data['time'])):
            prob = hourly_data['precipitation_probability'][i]
            
            # Only show hours where probability is 20% or higher
            if prob >= 20:
                raw_time = hourly_data['time'][i]
                # Convert '2026-03-14T18:00' to a readable format
                clean_time = datetime.strptime(raw_time, "%Y-%m-%dT%H:%M").strftime("%I:%M %p")
                amount = hourly_data['precipitation'][i]
                
                print(f" > {clean_time}: {prob}% chance ({amount}mm)")
                found_rain = True
        
        if not found_rain:
            print("No significant rain expected in the next 24 hours.")

    except Exception as e:
        print(f"Error fetching data: {e}")

if __name__ == "__main__":
    while True:
        get_dhaka_hourly_rain()
        print("\nRefreshing in 5 minutes... (Press Ctrl+C to stop)")
        time.sleep(300) # 300 seconds = 5 minutes
