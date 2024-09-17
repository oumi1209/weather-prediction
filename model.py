from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import joblib

class ModelBuilder:
    def __init__(self):
        self.model = None
        self.scaler = None  # Initialize scaler as None

    def build_model(self, input_shape):
        self.model = Sequential()
        self.model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
        self.model.add(LSTM(50))
        self.model.add(Dense(1))  # Predicting temperature
        self.model.compile(optimizer='adam', loss='mean_squared_error')

    def train_model(self, X_train, y_train, epochs=20, batch_size=64):
        self.model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size)

    def save_model(self, model_path='saved_models/temperature_model.keras', scaler_path='saved_models/scaler.pkl'):
        # Save the model in the recommended Keras format
        self.model.save(model_path)
        
        # Save the scaler if it's set
        if self.scaler is not None:
            joblib.dump(self.scaler, scaler_path)
        else:
            print("Scaler is not set. Skipping saving the scaler.")

    # Function to set the scaler from outside
    def set_scaler(self, scaler):
        self.scaler = scaler
