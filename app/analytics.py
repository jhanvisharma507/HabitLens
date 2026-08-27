import pandas as pd
from sqlalchemy.orm import Session

from app.models import DailyEntry


def get_correlation_data(db: Session):

    entries = db.query(DailyEntry).all()

    if not entries:
        return {}

    data = [
        {
            "sleep_hours": entry.sleep_hours,
            "study_hours": entry.study_hours,
            "exercise_minutes": entry.exercise_minutes,
            "screen_time_hours": entry.screen_time_hours,
            "mood_score": entry.mood_score,
            "productivity_score": entry.productivity_score,
        }
        for entry in entries
    ]

    df = pd.DataFrame(data)

    correlations = (
        df.corr()["productivity_score"]
        .drop("productivity_score")
        .round(3)
        .to_dict()
    )

    return correlations