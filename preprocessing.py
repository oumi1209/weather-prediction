import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np

class DataPreprocessor:
    def __init__(self):
        self.scaler = MinMaxScaler(feature_range=(0, 1))

    def preprocess(self, df, fit=True):
        # Select relevant features
        features = df[['Temperature', 'Humidity', 'Dew Point', 'Surface Pressure', 'Precipitation', 'Cloud Cover']]
        
        # If 'fit' is True, fit and transform, otherwise just transform (useful for new data)
        if fit:
            scaled_features = self.scaler.fit_transform(features)
        else:
            scaled_features = self.scaler.transform(features)
        
        return scaled_features, self.scaler

    def create_sequences(self, data, time_steps):
        X, y = [], []
        for i in range(time_steps, len(data)):
            # Take 'time_steps' of data as the input sequence
            X.append(data[i-time_steps:i])  
            # Predict the next time step's temperature
            y.append(data[i, 0])  # Assuming the first column is 'Temperature'
        return np.array(X), np.array(y)

