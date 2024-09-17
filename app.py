from fastapi import FastAPI
from forecast import TemperatureForecaster

app = FastAPI()

@app.post("/forecast/")
def get_forecast(latitude: float, longitude: float, start_date: str, end_date: str):
    forecaster = TemperatureForecaster()
    predicted_temp = forecaster.forecast(latitude, longitude, start_date, end_date)
    return {"predicted_temperature": predicted_temp}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
