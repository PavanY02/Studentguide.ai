import requests
import json
import os
import pandas as pd
from fastapi import HTTPException

# API URL for Student A's quiz data
API_URL = "https://api.jsonserve.com/XgAgFJ"

# File Path for JSON Data
DATA_FILE = "quiz_data.json"

# **Fetch and Save Quiz Data**
def fetch_quiz_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        quiz_data = response.json()
        print("✅ Data fetched successfully.")

        cleaned_data = []
        for quiz in quiz_data:
            if "quiz" in quiz and "topic" in quiz["quiz"]:
                cleaned_quiz = {
                    "quiz_id": quiz["quiz_id"],
                    "score": int(quiz["score"]),
                    "accuracy": float(quiz["accuracy"].replace("%", "").strip()),
                    "speed": float(quiz["speed"]),
                    "correct_answers": int(quiz["correct_answers"]),
                    "incorrect_answers": int(quiz["incorrect_answers"]),
                    "correct_answer_marks": float(quiz["quiz"]["correct_answer_marks"]),
                    "negative_marks": float(quiz["quiz"]["negative_marks"]),
                    "negative_score": float(quiz["negative_score"]),
                    "total_questions": int(quiz["quiz"]["questions_count"]),
                    "started_at": quiz["started_at"],
                    "ended_at": quiz["ended_at"],
                    "duration": quiz["duration"],
                    "initial_mistake_count": int(quiz["initial_mistake_count"]),
                    "mistakes_corrected": int(quiz["mistakes_corrected"]),
                    "date": quiz["submitted_at"].split("T")[0],
                    "topic": quiz["quiz"]["topic"],
                    "title": quiz["quiz"]["title"]
                }
                cleaned_data.append(cleaned_quiz)

        # Save cleaned data to JSON
        with open(DATA_FILE, "w") as f:
            json.dump(cleaned_data, f, indent=4)

        print(f"✅ Data saved to `{DATA_FILE}`")
    else:
        print(f"❌ Failed to fetch data: {response.status_code}")
        raise HTTPException(status_code=500, detail="Failed to fetch quiz data.")

# **Load Quiz Data from File**
def load_quiz_data():
    if not os.path.exists(DATA_FILE):
        fetch_quiz_data()  # Fetch data if file doesn't exist
    try:
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        raise HTTPException(status_code=500, detail="❌ Error decoding JSON data.")

# **Analyze Performance**
def analyze_performance():
    quiz_data = load_quiz_data()
    if not quiz_data:
        raise HTTPException(status_code=404, detail="❌ No quiz data available.")

    df = pd.DataFrame(quiz_data)

    # **Create Unique Quiz Identifier**
    df["quiz_identifier"] = df["topic"] + " - " + df["title"]

    # **Compute Performance Metrics**
    df["total_attempted"] = df["correct_answers"] + df["incorrect_answers"]
    df["total_unattempted"] = df["total_questions"] - df["total_attempted"]
    df["accuracy_rate"] = (df["correct_answers"] / df["total_attempted"]) * 100
    df["attempt_rate"] = (df["total_attempted"] / df["total_questions"]) * 100
    df["unanswered_rate"] = (df["total_unattempted"] / df["total_questions"]) * 100
    df["net_score"] = (df["correct_answers"] * df["correct_answer_marks"]) - (
            df["incorrect_answers"] * df["negative_marks"])

    df = df.fillna(0)

    # **Prepare API Response**
    quiz_performance = df[[
        "quiz_identifier", "total_questions", "total_attempted", "correct_answers",
        "incorrect_answers", "total_unattempted", "attempt_rate", "accuracy_rate",
        "unanswered_rate", "net_score"
    ]].to_dict(orient="records")

    return {
        "average_accuracy": round(df["accuracy_rate"].mean(), 2),
        "average_attempt_rate": round(df["attempt_rate"].mean(), 2),
        "average_unanswered_rate": round(df["unanswered_rate"].mean(), 2),
        "all_quiz_performance": quiz_performance
    }
