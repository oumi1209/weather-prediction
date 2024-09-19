from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from table import WeatherData
from database import engine, SessionLocal, get_db  # Import the database and session dependencies
from pydantic import BaseModel
from forecast import TemperatureForecaster

# Create the database tables
from table import Base
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Define the request model
class ForecastRequest(BaseModel):
    latitude: float
    longitude: float
    forecast_date: str  # Expected format 'YYYY-MM-DD'

# Initialize the forecaster
forecaster = TemperatureForecaster()

@app.post("/forecast/")
def get_forecast(request: ForecastRequest, db: Session = Depends(get_db)):
    try:
        # Step 1: Get the forecast
        result = forecaster.forecast(
            latitude=request.latitude, 
            longitude=request.longitude, 
            forecast_date=request.forecast_date
        )
        
        # Step 2: Store the result in the database
        forecast = WeatherData(
            latitude=request.latitude,
            longitude=request.longitude,
            forecast_date=request.forecast_date,
            predicted_temperature=result
        )
        db.add(forecast)
        db.commit()
        db.refresh(forecast)
        
        # Step 3: Return the result
        return {"predicted_temperature": result}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/")
def read_root():
    return {"message": "Temperature forecasting API is running."}
