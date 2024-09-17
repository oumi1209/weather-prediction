from tensorflow.keras.models import load_model
import joblib
import numpy as np
from fetching_data import WeatherDataFetcher
from preprocessing import DataPreprocessor

class TemperatureForecaster:
    def __init__(self, model_path='saved_models/temperature_model.h5', scaler_path='saved_models/scaler.pkl'):
        self.model = load_model(model_path)
        self.scaler = joblib.load(scaler_path)

    def forecast(self, latitude, longitude, start_date, end_date):
        # Fetch weather data
        fetcher = WeatherDataFetcher(latitude, longitude)
        df = fetcher.fetch_data(start_date, end_date)

        # Preprocess the data
        preprocessor = DataPreprocessor()
        scaled_data, _ = preprocessor.preprocess(df)

        # Reshape the data for LSTM
        X = np.array(scaled_data).reshape(1, scaled_data.shape[0], scaled_data.shape[1])

        # Predict the temperature
        prediction = self.model.predict(X)
        return self.scaler.inverse_transform([[prediction[0][0]]])[0][0]  # Inverse scale the prediction
