from fastapi import FastAPI
from pydantic import BaseModel
import mlflow.pyfunc
import pandas as pd
import numpy as np

# Load expected features from MLflow
client = mlflow.tracking.MlflowClient()
run_id = "YOUR_RUN_ID"  # Replace with your actual run ID
expected_features = client.get_run(run_id).data.params["expected_features"]

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

app = FastAPI()

# Load model with retry logic
model = None
for _ in range(3):  # Retry 3 times
    try:
        model = mlflow.pyfunc.load_model(
            "models:/SpotifyPopularityClassifier/Production"
        )
        break
    except Exception as e:
        print(f"Model loading failed: {e}")
        time.sleep(2)

@app.post("/predict")
def predict_popularity(track: TrackFeatures):
    # Convert to DataFrame with correct feature order
    input_data = {feat: [getattr(track, feat)] for feat in expected_features}
    input_df = pd.DataFrame(input_data)
    
    # Ensure correct data types
    for col in input_df.select_dtypes(include=['object']).columns:
        input_df[col] = input_df[col].astype(float)
    
    prediction = model.predict(input_df)
    return {"popular": int(prediction[0])}