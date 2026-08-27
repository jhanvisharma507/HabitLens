# HabitLens

## Overview

HabitLens is a personal habit and productivity analytics application that analyzes daily habits such as sleep, study time, exercise, screen time, and mood to understand their relationship with productivity.

The application also uses a Machine Learning model to predict a user's productivity score based on their current habits.

## Features

- Store daily habit data in MySQL
- REST API using FastAPI
- CRUD operations for daily entries
- Habit and productivity analytics
- Correlation analysis
- Interactive Streamlit dashboard
- Productivity trend visualization
- Machine Learning based productivity prediction
- Random Forest regression model
- Model evaluation using MAE and R² score

## Technology Stack

- Python
- FastAPI
- Streamlit
- MySQL
- SQLAlchemy
- Pandas
- Scikit-learn
- Matplotlib
- Requests

## Machine Learning

The project uses a Random Forest Regressor to predict productivity.

Input features:

- Sleep hours
- Study hours
- Exercise minutes
- Screen time hours
- Mood score

Target:

- Productivity score

The trained model is evaluated using:

- Mean Absolute Error (MAE)
- R² Score

## Project Structure

HabitLens/
├── app/
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── analytics.py
├── analytics/
│   └── analysis.py
├── dashboard.py
├── ml_model.py
├── create_tables.py
├── requirements.txt
├── README.md
└── .gitignore

## How It Works

User
↓
Streamlit Dashboard
↓
FastAPI
↓
MySQL Database

For productivity prediction:

User habits
↓
Streamlit
↓
FastAPI
↓
Random Forest Model
↓
Predicted Productivity Score

## How to Run

### 1. Clone the repository

git clone <your-github-repository-url>

### 2. Create and activate a virtual environment

python -m venv venv

Windows:

venv\Scripts\activate

### 3. Install dependencies

pip install -r requirements.txt

### 4. Configure the database

Create a `.env` file containing your MySQL database configuration.

Do not commit the `.env` file to GitHub.

### 5. Start FastAPI

python -m uvicorn app.main:app --reload

### 6. Start Streamlit

streamlit run dashboard.py

The Streamlit dashboard can then be opened in the browser.

## Model Performance

Using the current dataset:

- Mean Absolute Error: 0.22
- R² Score: 0.96

## Future Improvements

- User authentication
- Larger real-world dataset
- Personalized recommendations
- Cloud deployment
- Automated daily habit tracking
