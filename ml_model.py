import pickle

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score

from app.database import SessionLocal
from app.models import DailyEntry


# --------------------------------------------------
# 1. Load data from MySQL
# --------------------------------------------------

db = SessionLocal()

try:
    entries = db.query(DailyEntry).all()

    if len(entries) < 10:
        raise ValueError(
            f"Not enough data for training. Found {len(entries)} records."
        )

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

finally:
    db.close()


# --------------------------------------------------
# 2. Convert data to DataFrame
# --------------------------------------------------

df = pd.DataFrame(data)

print("\nTraining data:")
print(df.head())

print(f"\nTotal records: {len(df)}")


# --------------------------------------------------
# 3. Select features and target
# --------------------------------------------------

features = [
    "sleep_hours",
    "study_hours",
    "exercise_minutes",
    "screen_time_hours",
    "mood_score",
]

X = df[features]
y = df["productivity_score"]


# --------------------------------------------------
# 4. Split data into training and testing
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# --------------------------------------------------
# 5. Create and train ML model
# --------------------------------------------------

model = RandomForestRegressor(
    n_estimators=200,
    random_state=42,
    max_depth=5
)

model.fit(X_train, y_train)


# --------------------------------------------------
# 6. Evaluate model
# --------------------------------------------------

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("\nModel Performance")
print("-----------------")
print(f"Mean Absolute Error: {mae:.2f}")
print(f"R² Score: {r2:.2f}")


# --------------------------------------------------
# 7. Feature importance
# --------------------------------------------------

importance = pd.DataFrame({
    "feature": features,
    "importance": model.feature_importances_
})

importance = importance.sort_values(
    by="importance",
    ascending=False
)

print("\nFeature Importance")
print("------------------")
print(importance)


# --------------------------------------------------
# 8. Save trained model
# --------------------------------------------------

with open("productivity_model.pkl", "wb") as file:
    pickle.dump(model, file)

print("\nModel saved successfully!")
print("File: productivity_model.pkl")