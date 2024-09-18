from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from forecast import TemperatureForecaster  

# Create a FastAPI instance
app = FastAPI()

# Define the request body structure
class ForecastRequest(BaseModel):
    latitude: float
    longitude: float
    forecast_date: str  # Expected format: 'YYYY-MM-DD'

# Instantiate the TemperatureForecaster
forecaster = TemperatureForecaster()

# Define a POST endpoint for temperature forecasting
@app.post("/forecast/")
def get_forecast(request: ForecastRequest):
    try:
        # Get the forecast using the forecaster class
        result = forecaster.forecast(
            latitude=request.latitude, 
            longitude=request.longitude, 
            forecast_date=request.forecast_date
        )
        # Return the predicted temperature in a JSON response
        return {"predicted_temperature": result}
    except Exception as e:
        # If something goes wrong, raise an HTTP exception
        raise HTTPException(status_code=400, detail=str(e))

# Define a simple GET endpoint to check if the API is running
@app.get("/")
def read_root():
    return {"message": "Temperature forecasting API is running."}
