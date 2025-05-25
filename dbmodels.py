from fastapi import FastAPI, Depends
from joblib import load
from pydantic import BaseModel
import numpy as np
from sqlalchemy.orm import Session
from .database import engine, get_db
from . import dbmodels

# Create tables if they don't exist
dbmodels.Base.metadata.create_all(bind=engine)

app = FastAPI()

model = load('HousePrediction.joblib')

class HousePredictionData(BaseModel):
    latitude: float
    longitude: float
    total_rooms: float
    population: float
    households: float
    median_income: float

@app.post("/predict")
async def predict_house_value(data: HousePredictionData, db: Session = Depends(get_db)):
    input_data = np.array([
        data.latitude,
        data.longitude,
        data.total_rooms,
        data.population,
        data.households,
        data.median_income
    ]).reshape(1, -1)

    prediction = model.predict(input_data)
    predicted_value = float(prediction[0])

    # Save to database
    house_record = dbmodels.House(
        latitude=data.latitude,
        longitude=data.longitude,
        total_rooms=data.total_rooms,
        population=data.population,
        households=data.households,
        median_income=data.median_income,
        median_house_value=predicted_value
    )
    db.add(house_record)
    db.commit()
    db.refresh(house_record)

    return {
        'prediction': predicted_value,
        'record_id': house_record.id
    }
