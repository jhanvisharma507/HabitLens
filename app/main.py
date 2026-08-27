import pickle
from pathlib import Path
from datetime import date

import pandas as pd
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.analytics import get_correlation_data
from app.database import get_db
from app.models import DailyEntry as DailyEntryDB


app = FastAPI()


# ==================================================
# LOAD TRAINED ML MODEL
# ==================================================

MODEL_PATH = Path(__file__).resolve().parent.parent / "productivity_model.pkl"

with open(MODEL_PATH, "rb") as file:
    model = pickle.load(file)


# ==================================================
# PYDANTIC MODELS
# ==================================================

class DailyEntry(BaseModel):
    date: date

    sleep_hours: float = Field(ge=0, le=24)
    study_hours: float = Field(ge=0, le=24)
    exercise_minutes: int = Field(ge=0, le=1440)
    screen_time_hours: float = Field(ge=0, le=24)

    mood_score: int = Field(ge=1, le=10)
    productivity_score: int = Field(ge=1, le=10)


class PredictionInput(BaseModel):
    sleep_hours: float = Field(ge=0, le=24)
    study_hours: float = Field(ge=0, le=24)
    exercise_minutes: int = Field(ge=0, le=1440)
    screen_time_hours: float = Field(ge=0, le=24)
    mood_score: int = Field(ge=1, le=10)


class DailyEntryResponse(BaseModel):
    id: int
    date: date
    sleep_hours: float
    study_hours: float
    exercise_minutes: int
    screen_time_hours: float
    mood_score: int
    productivity_score: int

    class Config:
        from_attributes = True


# ==================================================
# BASIC ROUTES
# ==================================================

@app.get("/")
def home():
    return {
        "message": "Welcome to HabitLens"
    }


@app.get("/about")
def about():
    return {
        "project": "HabitLens",
        "purpose": "Analyze habits and predict productivity"
    }


@app.get("/greet/{name}")
def greet(name: str):
    return {
        "message": f"Hello, {name}!"
    }


# ==================================================
# ANALYTICS
# ==================================================

@app.get("/analytics/correlation")
def correlation_analysis(
    db: Session = Depends(get_db)
):
    return {
        "message": "Correlation with productivity",
        "data": get_correlation_data(db)
    }


# ==================================================
# DAILY ENTRIES - GET ALL
# ==================================================

@app.get(
    "/daily-entries",
    response_model=list[DailyEntryResponse]
)
def get_entries(
    db: Session = Depends(get_db)
):
    return db.query(DailyEntryDB).all()


# ==================================================
# DAILY ENTRIES - GET ONE
# ==================================================

@app.get(
    "/daily-entries/{entry_id}",
    response_model=DailyEntryResponse
)
def get_entry(
    entry_id: int,
    db: Session = Depends(get_db)
):

    entry = db.query(DailyEntryDB).filter(
        DailyEntryDB.id == entry_id
    ).first()

    if entry is None:
        raise HTTPException(
            status_code=404,
            detail="Entry not found"
        )

    return entry


# ==================================================
# DAILY ENTRY - CREATE
# ==================================================

@app.post("/daily-entry", response_model=DailyEntryResponse)
def add_entry(
    entry: DailyEntry,
    db: Session = Depends(get_db)
):
    # Check whether an entry already exists for this date
    existing_entry = db.query(DailyEntryDB).filter(
        DailyEntryDB.date == entry.date
    ).first()

    if existing_entry:
        raise HTTPException(
            status_code=400,
            detail="An entry for this date already exists."
        )

    new_entry = DailyEntryDB(
        date=entry.date,
        sleep_hours=entry.sleep_hours,
        study_hours=entry.study_hours,
        exercise_minutes=entry.exercise_minutes,
        screen_time_hours=entry.screen_time_hours,
        mood_score=entry.mood_score,
        productivity_score=entry.productivity_score
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)

    return new_entry


# ==================================================
# DAILY ENTRY - UPDATE
# ==================================================

@app.put(
    "/daily-entries/{entry_id}",
    response_model=DailyEntryResponse
)
def update_entry(
    entry_id: int,
    entry: DailyEntry,
    db: Session = Depends(get_db)
):

    existing_entry = db.query(DailyEntryDB).filter(
        DailyEntryDB.id == entry_id
    ).first()

    if not existing_entry:
        raise HTTPException(
            status_code=404,
            detail="Entry not found"
        )

    existing_entry.date = entry.date
    existing_entry.sleep_hours = entry.sleep_hours
    existing_entry.study_hours = entry.study_hours
    existing_entry.exercise_minutes = entry.exercise_minutes
    existing_entry.screen_time_hours = entry.screen_time_hours
    existing_entry.mood_score = entry.mood_score
    existing_entry.productivity_score = entry.productivity_score

    db.commit()
    db.refresh(existing_entry)

    return existing_entry


# ==================================================
# DAILY ENTRY - DELETE
# ==================================================

@app.delete("/daily-entries/{entry_id}")
def delete_entry(
    entry_id: int,
    db: Session = Depends(get_db)
):

    existing_entry = db.query(DailyEntryDB).filter(
        DailyEntryDB.id == entry_id
    ).first()

    if not existing_entry:
        raise HTTPException(
            status_code=404,
            detail="Entry not found"
        )

    db.delete(existing_entry)
    db.commit()

    return {
        "message": "Entry deleted successfully"
    }


# ==================================================
# ML PRODUCTIVITY PREDICTION
# ==================================================

@app.post("/predict-productivity")
def predict_productivity(
    data: PredictionInput
):

    # Prepare input in the SAME order
    # used during model training
    input_data = pd.DataFrame([{
        "sleep_hours": data.sleep_hours,
        "study_hours": data.study_hours,
        "exercise_minutes": data.exercise_minutes,
        "screen_time_hours": data.screen_time_hours,
        "mood_score": data.mood_score
    }])

    # Make prediction
    prediction = model.predict(input_data)[0]

    # Keep prediction within 1-10 scale
    prediction = max(1, min(10, prediction))

    prediction = round(float(prediction), 2)

    return {
        "predicted_productivity": prediction,
        "scale": "1-10",
        "message": "Productivity predicted successfully"
    }

