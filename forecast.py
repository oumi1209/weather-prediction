from tensorflow.keras.models import load_model
import joblib
import numpy as np
from fetching_data import WeatherDataFetcher
from preprocessing import DataPreprocessor

class TemperatureForecaster:
    def __init__(self, model_path='saved_models/model.keras', 
                 feature_scaler_path='saved_models/feature_scaler.pkl',
                 temperature_scaler_path='saved_models/temperature_scaler.pkl'):
        self.model = load_model(model_path)
        self.feature_scaler = joblib.load(feature_scaler_path)  # Load pre-fitted feature scaler
        self.temperature_scaler = joblib.load(temperature_scaler_path)  # Load pre-fitted temperature scaler

    def forecast(self, latitude, longitude, forecast_date):
        # Step 1: Fetch historical weather data ending 4 days before forecast_date
        fetcher = WeatherDataFetcher(latitude, longitude)
        df = fetcher.fetch_data_based_on_forecast(forecast_date)

        # Step 2: Preprocess the data using pre-fitted scalers
        preprocessor = DataPreprocessor()
        
        # Scale features only using the pre-fitted feature_scaler
        scaled_features = self.feature_scaler.transform(df[['Humidity', 'Dew Point', 'Surface Pressure', 'Precipitation', 'Cloud Cover']])

        # Step 3: Reshape the data for LSTM input (for prediction)
        X = np.array(scaled_features).reshape(1, scaled_features.shape[0], scaled_features.shape[1])

        # Step 4: Predict the scaled temperature
        prediction = self.model.predict(X)

        # Step 5: Inverse scale the prediction using the temperature scaler
        predicted_temperature = self.temperature_scaler.inverse_transform([[prediction[0][0]]])[0][0]
        
        return predicted_temperature

# Example usage:
#forecaster = TemperatureForecaster()
#result = forecaster.forecast(latitude=52.52, longitude=13.41, forecast_date="2024-09-20")
#print(f"Predicted temperature for 2024-09-20: {result}")
