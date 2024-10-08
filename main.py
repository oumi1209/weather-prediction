from fetching_data import WeatherDataFetcher
from preprocessing import DataPreprocessor
from model import ModelBuilder
import numpy as np
from sklearn.model_selection import train_test_split

# Step 1: Fetch data for the last 5 years
fetcher = WeatherDataFetcher(latitude=40.7128, longitude=-74.0060)  # Example: New York City
df = fetcher.fetch_last_5_years_data()

# Step 2: Preprocess the data
preprocessor = DataPreprocessor()
scaled_data, scaler = preprocessor.preprocess(df)



# Step 3: Create sequences for LSTM
time_steps = 24  # For example, using 24 time steps (24 hours)
X, y = preprocessor.create_sequences(scaled_data, time_steps)

# Step 4: Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

# Step 5: Build and train the model
model_builder = ModelBuilder()
#model_builder.build_model(input_shape=(X_train.shape[1], X_train.shape[2]))


# Set the scaler for the model builder
model_builder.set_scaler(scaler)
# Build the model
input_shape = (X_train.shape[1], X_train.shape[2])
model_builder.build_model(input_shape)
model_builder.train_model(X_train, y_train, epochs=20, batch_size=64)

# Step 6: Save the trained model and scaler
model_builder.save_model()

# Evaluate the model on the test set (optional)
test_loss = model_builder.model.evaluate(X_test, y_test)
print(f"Test Loss: {test_loss}")
