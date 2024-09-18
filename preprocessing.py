import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class DataPreprocessor:

    def preprocess(self, df, fit=True):
        # Select relevant features (excluding Temperature since it's the target)
        features = df[['Humidity', 'Dew Point', 'Surface Pressure', 'Precipitation', 'Cloud Cover']]
        temperature = df[['Temperature']]

        # Two separate scalers: one for features, one for temperature
        feature_scaler = MinMaxScaler(feature_range=(0, 1))
        temperature_scaler = MinMaxScaler(feature_range=(0, 1))
        if fit:
            # Fit and transform features and temperature separately
            scaled_features = feature_scaler.fit_transform(features)
            scaled_temperature = temperature_scaler.fit_transform(temperature)
        else:
            # Just transform the new data using already fitted scalers
            scaled_features = feature_scaler.transform(features)
            scaled_temperature = temperature_scaler.transform(temperature)

        # Combine the scaled features and temperature as two separate outputs
        return scaled_features, scaled_temperature,feature_scaler,temperature_scaler

    def create_sequences(self, features, temperature, time_steps):
        X, y = [], []
        for i in range(time_steps, len(features)):
            # Take 'time_steps' of features as input sequence (past data)
            X.append(features[i-time_steps:i])
            # Predict the next time step's temperature
            y.append(temperature[i])  # Using the scaled temperature as the target
        return np.array(X), np.array(y)

# Example of usage:
# preprocessor = DataPreprocessor()
# scaled_features, scaled_temperature = preprocessor.preprocess(df)
# X, y = preprocessor.create_sequences(scaled_features, scaled_temperature, time_steps)
