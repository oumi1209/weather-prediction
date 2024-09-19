# Use the official Python image with version 3.9
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8050 for Dash and 8000 for FastAPI
EXPOSE 8050 
EXPOSE 8000

# Command to run both FastAPI (on port 8000) and Dash (on port 8050)
CMD ["bash", "-c", "uvicorn app:app --host 0.0.0.0 --port 8000 & python dash_app.py"]
