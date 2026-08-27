import requests
import pandas as pd
import streamlit as st


# --------------------------------------------------
# Configuration
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000"


# --------------------------------------------------
# Page configuration
# --------------------------------------------------

st.set_page_config(
    page_title="HabitLens",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📊 HabitLens")
st.subheader("Personal Habit & Productivity Analytics")


# --------------------------------------------------
# Load daily entries
# --------------------------------------------------

def get_entries():
    try:
        response = requests.get(
            f"{API_URL}/daily-entries",
            timeout=5
        )

        if response.status_code == 200:
            return response.json()

        st.error("Unable to fetch daily entries.")
        return []

    except requests.exceptions.RequestException:
        st.error(
            "FastAPI is not running. "
            "Start Uvicorn on port 8000."
        )
        return []


entries = get_entries()


# --------------------------------------------------
# Convert data to DataFrame
# --------------------------------------------------

if entries:

    df = pd.DataFrame(entries)

    # --------------------------------------------------
    # KPI section
    # --------------------------------------------------

    st.markdown("## 📈 Your Habit Summary")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Avg Sleep",
        f"{df['sleep_hours'].mean():.1f} hrs"
    )

    col2.metric(
        "Avg Study",
        f"{df['study_hours'].mean():.1f} hrs"
    )

    col3.metric(
        "Avg Exercise",
        f"{df['exercise_minutes'].mean():.0f} min"
    )

    col4.metric(
        "Avg Productivity",
        f"{df['productivity_score'].mean():.1f}/10"
    )

    st.divider()

    # --------------------------------------------------
    # Productivity trend
    # --------------------------------------------------

    st.markdown("## 📈 Productivity Trend")

    chart_df = df.copy()
    chart_df["date"] = pd.to_datetime(chart_df["date"])
    chart_df = chart_df.sort_values("date")

    st.line_chart(
        chart_df.set_index("date")["productivity_score"]
    )

    # --------------------------------------------------
    # Habit analysis
    # --------------------------------------------------

    st.markdown("## 🔍 Habit Analysis")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### Sleep vs Productivity")

        st.scatter_chart(
            df,
            x="sleep_hours",
            y="productivity_score"
        )

    with col2:

        st.markdown("### Study vs Productivity")

        st.scatter_chart(
            df,
            x="study_hours",
            y="productivity_score"
        )

    col3, col4 = st.columns(2)

    with col3:

        st.markdown("### Screen Time vs Productivity")

        st.scatter_chart(
            df,
            x="screen_time_hours",
            y="productivity_score"
        )

    with col4:

        st.markdown("### Exercise vs Productivity")

        st.scatter_chart(
            df,
            x="exercise_minutes",
            y="productivity_score"
        )

    st.divider()

    # --------------------------------------------------
    # Recent records
    # --------------------------------------------------

    st.markdown("## 📋 Daily Records")

    display_columns = [
        "date",
        "sleep_hours",
        "study_hours",
        "exercise_minutes",
        "screen_time_hours",
        "mood_score",
        "productivity_score"
    ]

    st.dataframe(
        df[display_columns],
        use_container_width=True
    )

else:

    st.info("No daily entries found.")


# ==================================================
# ML PRODUCTIVITY PREDICTOR
# ==================================================

st.divider()

st.markdown("## 🤖 Productivity Predictor")

st.write(
    "Enter your current habits and HabitLens will "
    "estimate your productivity score using the trained ML model."
)


col1, col2 = st.columns(2)

with col1:

    sleep = st.number_input(
        "Sleep Hours",
        min_value=0.0,
        max_value=24.0,
        value=7.0,
        step=0.5
    )

    study = st.number_input(
        "Study Hours",
        min_value=0.0,
        max_value=24.0,
        value=6.0,
        step=0.5
    )

    exercise = st.number_input(
        "Exercise Minutes",
        min_value=0,
        max_value=1440,
        value=30,
        step=5
    )


with col2:

    screen_time = st.number_input(
        "Screen Time Hours",
        min_value=0.0,
        max_value=24.0,
        value=4.0,
        step=0.5
    )

    mood = st.slider(
        "Mood Score",
        min_value=1,
        max_value=10,
        value=7
    )


# --------------------------------------------------
# Prediction button
# --------------------------------------------------

if st.button(
    "🔮 Predict Productivity",
    use_container_width=True
):

    prediction_data = {
        "sleep_hours": sleep,
        "study_hours": study,
        "exercise_minutes": exercise,
        "screen_time_hours": screen_time,
        "mood_score": mood
    }

    try:

        response = requests.post(
            f"{API_URL}/predict-productivity",
            json=prediction_data,
            timeout=5
        )

        if response.status_code == 200:

            result = response.json()

            prediction = result["predicted_productivity"]

            st.success(
                f"Predicted Productivity: {prediction}/10"
            )

            st.progress(
                prediction / 10
            )

        else:

            st.error(
                f"Prediction failed: {response.text}"
            )

    except requests.exceptions.RequestException:

        st.error(
            "Could not connect to FastAPI. "
            "Make sure Uvicorn is running."
        )

# ==================================================
# ADD DAILY DATA
# ==================================================

st.divider()

st.markdown("## 📝 Add Daily Data")

st.write(
    "Enter your daily habits and save them to your HabitLens database."
)

with st.form("daily_entry_form"):

    entry_date = st.date_input(
        "Date"
    )

    col1, col2 = st.columns(2)

    with col1:

        sleep_hours = st.number_input(
            "Sleep Hours",
            min_value=0.0,
            max_value=24.0,
            value=7.0,
            step=0.5
        )

        study_hours = st.number_input(
            "Study Hours",
            min_value=0.0,
            max_value=24.0,
            value=4.0,
            step=0.5
        )

        exercise_minutes = st.number_input(
            "Exercise Minutes",
            min_value=0,
            max_value=1440,
            value=30,
            step=5
        )

    with col2:

        screen_time_hours = st.number_input(
            "Screen Time Hours",
            min_value=0.0,
            max_value=24.0,
            value=3.0,
            step=0.5
        )

        mood_score = st.slider(
            "Mood Score",
            min_value=1,
            max_value=10,
            value=7
        )

        productivity_score = st.slider(
            "Actual Productivity Score",
            min_value=1,
            max_value=10,
            value=7
        )

    submitted = st.form_submit_button(
        "💾 Save Daily Entry",
        use_container_width=True
    )

    if submitted:

        entry_data = {
            "date": str(entry_date),
            "sleep_hours": sleep_hours,
            "study_hours": study_hours,
            "exercise_minutes": exercise_minutes,
            "screen_time_hours": screen_time_hours,
            "mood_score": mood_score,
            "productivity_score": productivity_score
        }

        try:

            response = requests.post(
                f"{API_URL}/daily-entry",
                json=entry_data,
                timeout=5
            )

            if response.status_code == 200:

                st.success(
                    "✅ Daily entry saved successfully!"
                )

                st.info(
                    "Refresh the page to see the new entry "
                    "in your dashboard."
                )

            else:

                st.error(
                    f"Failed to save entry: {response.text}"
                )

        except requests.exceptions.RequestException:

            st.error(
                "Could not connect to FastAPI. "
                "Make sure Uvicorn is running."
            )