from fastapi import FastAPI
from pydantic import BaseModel
import mlflow
import mlflow.pyfunc
import pandas as pd

# Define input schema
class TrackFeatures(BaseModel):
    danceability: float
    energy: float
    loudness: float
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    duration_ms: int
    key: int
    mode: int
    time_signature: int
    year: int

# Initialize app
app = FastAPI()

# Connect to MLflow tracking server
mlflow.set_tracking_uri("http://localhost:5000")

# Load model from the registry
model_uri = "models:/SpotifyPopularityClassifier/Production"
model = mlflow.pyfunc.load_model(model_uri)

@app.get("/")
def root():
    return {"message": " Spotify Popularity API is running!"}

@app.post("/predict")
def predict_popularity(track: TrackFeatures):
    input_df = pd.DataFrame([track.dict()])
    prediction = model.predict(input_df)
    return {"popular": int(prediction[0])}

