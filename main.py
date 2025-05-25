from fastapi import FastAPI
from joblib import load
from pydantic import BaseModel
import numpy as np

#initalise the app
app = FastAPI()

#load the modol
model = load('HousePrediction.joblib')

#Use ppydantic to define what modelm input
class HousePredictionData(BaseModel):
    latitude : float
    longitude : float
    total_rooms : float
    population : float
    household : float
    median_income : float


@app.post("/predict")
async def predict_house_value(data:HousePredictionData):
    input_data = np.array([data.latitude, data.longitude,data.total_rooms,data.population,data.household,data.median_income]).reshape(1,-1)
    prediction = model.predict(input_data)
    return {
        'prediction': float(prediction[0])
    }