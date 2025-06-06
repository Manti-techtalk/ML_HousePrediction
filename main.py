from fastapi import FastAPI, Depends
from joblib import load
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
from sqlalchemy.orm import Session
from database import engine, get_db, Base  # absolute imports
import dbmodels


# Create tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://172.17.18.168:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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
        latitude=str(data.latitude),
        longitude=str(data.longitude),
        total_rooms=str(data.total_rooms),
        population=str(data.population),
        households=str(data.households),
        median_income=str(data.median_income),
        median_house_value=str(predicted_value)
    )

    db.add(house_record)
    db.commit()
    db.refresh(house_record)

    return {
        "prediction": predicted_value,
        "record_id": house_record.id
    }
