from sqlalchemy import Column, Integer, Float, Date
from app.database import Base


class DailyEntry(Base):
    __tablename__ = "daily_entries"

    id = Column(Integer, primary_key=True, index=True)

    date = Column(Date, nullable=False)

    sleep_hours = Column(Float, nullable=False)
    study_hours = Column(Float, nullable=False)
    exercise_minutes = Column(Integer, nullable=False)
    screen_time_hours = Column(Float, nullable=False)

    mood_score = Column(Integer, nullable=False)
    productivity_score = Column(Integer, nullable=False)
