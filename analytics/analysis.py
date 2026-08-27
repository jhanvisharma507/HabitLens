import os

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from dotenv import load_dotenv
from sqlalchemy import create_engine


# ============================================================
# 1. LOAD DATABASE CONFIGURATION
# ============================================================

load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


# ============================================================
# 2. CREATE DATABASE CONNECTION
# ============================================================

DATABASE_URL = (
    f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


# ============================================================
# 3. FETCH DATA FROM MYSQL
# ============================================================

query = """
SELECT
    date,
    sleep_hours,
    study_hours,
    exercise_minutes,
    screen_time_hours,
    mood_score,
    productivity_score
FROM daily_entries
ORDER BY date
"""

df = pd.read_sql(query, engine)


# ============================================================
# 4. DISPLAY DATA
# ============================================================

print("\n===== HABIT DATA =====")
print(df)


# ============================================================
# 5. BASIC STATISTICS
# ============================================================

print("\n===== BASIC STATISTICS =====")
print(df.describe())


# ============================================================
# 6. CORRELATION WITH PRODUCTIVITY
# ============================================================

print("\n===== CORRELATION WITH PRODUCTIVITY =====")

correlations = df[
    [
        "sleep_hours",
        "study_hours",
        "exercise_minutes",
        "screen_time_hours",
        "mood_score",
        "productivity_score"
    ]
].corr()["productivity_score"].sort_values(ascending=False)

print(correlations)


# ============================================================
# 7. SLEEP vs PRODUCTIVITY
# ============================================================

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="sleep_hours",
    y="productivity_score"
)

plt.title("Sleep Hours vs Productivity")
plt.xlabel("Sleep Hours")
plt.ylabel("Productivity Score")

plt.tight_layout()
plt.show()


# ============================================================
# 8. STUDY HOURS vs PRODUCTIVITY
# ============================================================

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="study_hours",
    y="productivity_score"
)

plt.title("Study Hours vs Productivity")
plt.xlabel("Study Hours")
plt.ylabel("Productivity Score")

plt.tight_layout()
plt.show()


# ============================================================
# 9. SCREEN TIME vs PRODUCTIVITY
# ============================================================

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="screen_time_hours",
    y="productivity_score"
)

plt.title("Screen Time vs Productivity")
plt.xlabel("Screen Time (Hours)")
plt.ylabel("Productivity Score")

plt.tight_layout()
plt.show()


# ============================================================
# 10. EXERCISE vs PRODUCTIVITY
# ============================================================

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="exercise_minutes",
    y="productivity_score"
)

plt.title("Exercise vs Productivity")
plt.xlabel("Exercise (Minutes)")
plt.ylabel("Productivity Score")

plt.tight_layout()
plt.show()


# ============================================================
# 11. MOOD vs PRODUCTIVITY
# ============================================================

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=df,
    x="mood_score",
    y="productivity_score"
)

plt.title("Mood vs Productivity")
plt.xlabel("Mood Score")
plt.ylabel("Productivity Score")

plt.tight_layout()
plt.show()


# ============================================================
# 12. PRODUCTIVITY TREND
# ============================================================

plt.figure(figsize=(10, 5))

sns.lineplot(
    data=df,
    x="date",
    y="productivity_score",
    marker="o"
)

plt.title("Daily Productivity Trend")
plt.xlabel("Date")
plt.ylabel("Productivity Score")

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()