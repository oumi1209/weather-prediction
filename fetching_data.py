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
            # Extract the date part from the Datetime column (removes the time)
            df['Datetime'] = df['Datetime'].dt.date
            # Group by the date and calculate the mean for the other columns
            df_grouped = df.groupby('Datetime').mean()
            return df_grouped.dropna()
        else:
            raise Exception(f"Failed to fetch data. Status code: {response.status_code}")

    def fetch_4_years_data(self):
        start_date = datetime(2015, 1, 1).date()  # Set the start date to 2020-01-01
        end_date = start_date + timedelta(days=7*365)  # Calculate the end date as 4 years later
        return self.fetch_data(start_date=start_date, end_date=end_date)

    
        # Fetch custom data based on forecast date
    def fetch_data_based_on_forecast(self, forecast_date, historical_days=14):
        """
        Fetch historical weather data ending 4 days before the forecast date.
        :param forecast_date: The target date for forecasting (in 'YYYY-MM-DD' format).
        :param historical_days: Number of days of historical data to fetch (default: 35 days).
        """
        # Convert forecast_date to datetime object
        forecast_date_obj = datetime.strptime(forecast_date, "%Y-%m-%d")
        
        #historical data to fetch
        end_date = forecast_date_obj - timedelta(days=4)  #4 days before the forecast date
        start_date = end_date - timedelta(days=historical_days)  # Historical days before the end date
        
        return self.fetch_data(start_date=start_date.strftime('%Y-%m-%d'), end_date=end_date.strftime('%Y-%m-%d'))


d=WeatherDataFetcher(52.52,13.41)
f=d.fetch_data_based_on_forecast("2024-09-20")
print(len(f))