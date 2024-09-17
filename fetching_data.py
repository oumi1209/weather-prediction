import requests
import pandas as pd
from datetime import datetime, timedelta

class WeatherDataFetcher:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        self.base_url = "https://archive-api.open-meteo.com/v1/archive"

    def fetch_data(self, start_date, end_date):
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start_date": start_date,
            "end_date": end_date,
            "hourly": ["temperature_2m", "relative_humidity_2m", "dew_point_2m", "surface_pressure", "precipitation", "cloudcover"],
            "timezone": "auto"
        }

        response = requests.get(self.base_url, params=params)

        if response.status_code == 200:
            hourly_data = response.json()["hourly"]
            df = pd.DataFrame({
                "Datetime": pd.to_datetime(hourly_data["time"]),
                "Temperature": hourly_data["temperature_2m"],
                "Humidity": hourly_data["relative_humidity_2m"],
                "Dew Point": hourly_data["dew_point_2m"],
                "Surface Pressure": hourly_data["surface_pressure"],
                "Precipitation": hourly_data["precipitation"],
                "Cloud Cover": hourly_data["cloudcover"]
            })
            return df.dropna()
        else:
            raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

    def fetch_last_5_years_data(self):
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=5*365)
        return self.fetch_data(start_date=start_date, end_date=end_date)

d=WeatherDataFetcher(52.52,13.41)
f=d.fetch_last_5_years_data()
print(f)