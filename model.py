from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib

class ModelBuilder:
    def __init__(self):
        self.model = None
        self.feature_scaler = None  # Scaler for features
        self.temperature_scaler = None  # Scaler for temperature

    def build_model(self, input_shape):
        self.model = Sequential()
        self.model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
        self.model.add(LSTM(50))
        self.model.add(Dense(1))  # Predicting temperature
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def train_model(self, X_train, y_train, epochs=20, batch_size=24):
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)

    def save_model(self, model_path='saved_models/model.keras', 
                   feature_scaler_path='saved_models/feature_scaler.pkl', 
                   temperature_scaler_path='saved_models/temperature_scaler.pkl'):
    
        # Save the model in the recommended Keras format
        self.model.save(model_path)     
        
        # Save the feature scaler if it's set
        if self.feature_scaler is not None:
            joblib.dump(self.feature_scaler, feature_scaler_path)
        else:
            print("Feature scaler is not set. Skipping saving the feature scaler.")
        
        # Save the temperature scaler if it's set
        if self.temperature_scaler is not None:
            joblib.dump(self.temperature_scaler, temperature_scaler_path)
        else:
            print("Temperature scaler is not set. Skipping saving the temperature scaler.")

    # Functions to set scalers from outside
    def set_feature_scaler(self, feature_scaler):
        self.feature_scaler = feature_scaler
    
    def set_temperature_scaler(self, temperature_scaler):
        self.temperature_scaler = temperature_scaler
