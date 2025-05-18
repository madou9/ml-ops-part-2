import streamlit as st
import requests

st.title(" Spotify Track Popularity Predictor")

# Get ALL features 
# features = {
#     "danceability": st.slider("Danceability", 0.0, 1.0, 0.5),
#     "energy": st.slider("Energy", 0.0, 1.0, 0.5),
#     "loudness": st.slider("Loudness (dB)", -60.0, 0.0, -10.0),
#     "speechiness": st.slider("Speechiness", 0.0, 1.0, 0.1),
#     "acousticness": st.slider("Acousticness", 0.0, 1.0, 0.5),
#     "instrumentalness": st.slider("Instrumentalness", 0.0, 1.0, 0.0),
#     "liveness": st.slider("Liveness", 0.0, 1.0, 0.2),
#     "valence": st.slider("Valence", 0.0, 1.0, 0.5),
#     "tempo": st.slider("Tempo (BPM)", 50.0, 250.0, 120.0),
#     "duration_ms": st.slider("Duration (ms)", 30000, 500000, 180000),
#     "key": st.slider("Key", 0, 11, 0),
#     "mode": st.selectbox("Mode", [0, 1]),
#     "time_signature": st.selectbox("Time Signature", [3, 4, 5]),
#     "year": st.slider("Year", 2000, 2023, 2020)
# }

features = {
    "danceability": st.number_input("Danceability", min_value=0.0, max_value=1.0, value=0.5),
    "energy": st.number_input("Energy", min_value=0.0, max_value=1.0, value=0.5),
    "loudness": st.number_input("Loudness (dB)", min_value=-60.0, max_value=0.0, value=-10.0),
    "speechiness": st.number_input("Speechiness", min_value=0.0, max_value=1.0, value=0.1),
    "acousticness": st.number_input("Acousticness", min_value=0.0, max_value=1.0, value=0.5),
    "instrumentalness": st.number_input("Instrumentalness", min_value=0.0, max_value=1.0, value=0.0),
    "liveness": st.number_input("Liveness", min_value=0.0, max_value=1.0, value=0.2),
    "valence": st.number_input("Valence", min_value=0.0, max_value=1.0, value=0.5),
    "tempo": st.number_input("Tempo (BPM)", min_value=50.0, max_value=250.0, value=120.0),
    "duration_ms": st.number_input("Duration (ms)", min_value=30000, max_value=500000, value=180000),
    "key": st.number_input("Key", min_value=0, max_value=11, value=0),
    "mode": st.selectbox("Mode", [0, 1]),
    "time_signature": st.selectbox("Time Signature", [3, 4, 5]),
    "year": st.number_input("Year", min_value=2000, max_value=2023, value=2020)
}


if st.button("Check prediction"):
    try:
        response = requests.post(
            "http://127.0.0.1:8000/predict",
            json={k: features[k] for k in sorted(features.keys())}
        )
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted: {'Popular' if result['popular'] == 1 else 'Not Popular'}")
        else:
            st.error(f"API Error: {response.text}")
    except Exception as e:
        st.error(f"Connection failed: {str(e)}")