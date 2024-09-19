import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine, text
import requests

# Set up the Dash app
app = dash.Dash(__name__)

# Connect to PostgreSQL database
DATABASE_URL = "postgresql://postgres:mimi@localhost/weather_db"
engine = create_engine(DATABASE_URL)

# Function to fetch data from PostgreSQL
def fetch_data():
    query = """
    SELECT forecast_date, latitude, longitude, predicted_temperature, request_time
    FROM weather_data
    ORDER BY request_time DESC
    LIMIT 100
    """
    
    # Using the engine's connection to fetch data
    with engine.connect() as conn:
        result = conn.execute(text(query))  # Execute the SQL query
        df = pd.DataFrame(result.fetchall(), columns=result.keys())  # Convert results to a DataFrame
    return df

# Function to call the forecast API
def call_forecast_api(latitude, longitude, forecast_date):
    url = "http://127.0.0.1:8000/forecast/"  # URL of your FastAPI server
    payload = {
        "latitude": latitude,
        "longitude": longitude,
        "forecast_date": forecast_date
    }
    
    # Send a POST request to the forecast API
    response = requests.post(url, json=payload)
    
    if response.status_code == 200:
        return response.json()["predicted_temperature"]
    else:
        return None

# Initial data fetch
df = fetch_data()

# Create a Plotly figure for visualization
fig = px.line(df, x="forecast_date", y="predicted_temperature", title="Temperature Forecast Over Time")

# Set up the layout of the Dash app
app.layout = html.Div(children=[
    html.H1(children="Real-Time Temperature Forecast Dashboard"),

    # Input fields to get user input for forecasting
    html.Div([
        dcc.Input(id='input-latitude', type='number', placeholder='Latitude', value=52.52),
        dcc.Input(id='input-longitude', type='number', placeholder='Longitude', value=13.41),
        dcc.Input(id='input-date', type='text', placeholder='YYYY-MM-DD', value='2024-09-20'),
        html.Button('Submit Forecast Request', id='submit-button', n_clicks=0)
    ], style={'padding': '10px'}),
    
    # Graph to display forecast data
    dcc.Graph(
        id='forecast-graph',
        figure=fig
    ),

    # Interval component for real-time updates (every minute)
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # 1 minute interval
        n_intervals=0
    )
])

# Callback to handle the API request and update graph
@app.callback(
    Output('forecast-graph', 'figure'),
    [Input('submit-button', 'n_clicks'), Input('interval-component', 'n_intervals')],
    [State('input-latitude', 'value'), State('input-longitude', 'value'), State('input-date', 'value')]
)
def update_graph_live(n_clicks, n_intervals, latitude, longitude, forecast_date):
    # Only call the API if the submit button is clicked
    if n_clicks > 0:
        predicted_temp = call_forecast_api(latitude, longitude, forecast_date)
        if predicted_temp is not None:
            print(f"API called: {latitude}, {longitude}, {forecast_date} -> {predicted_temp}")
    
    # Fetch updated data from the database
    df = fetch_data()  # Fetch the latest data
    
    # Update the figure
    fig = px.line(df, x="forecast_date", y="predicted_temperature", title="Temperature Forecast Over Time")
    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
