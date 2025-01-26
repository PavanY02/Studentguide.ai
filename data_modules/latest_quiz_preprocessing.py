import requests
from fastapi import FastAPI, HTTPException

app = FastAPI()

# **API Endpoints**
QUIZ_API = "https://www.jsonkeeper.com/b/LLQT"
STUDENT_API = "https://api.jsonserve.com/rJvd7g"


def fetch_quiz_data():
    response = requests.get(QUIZ_API)
    if response.status_code == 200:
        return response.json()["quiz"]  # ✅ Return quiz data only
    else:
        raise HTTPException(status_code=500, detail="❌ Failed to fetch quiz data")


def fetch_student_data():
    response = requests.get(STUDENT_API)
    if response.status_code == 200:
        return response.json()  # ✅ Return student data only
    else:
        raise HTTPException(status_code=500, detail="❌ Failed to fetch student data")



def get_full_quiz_data():
    quiz_data = fetch_quiz_data()
    student_data = fetch_student_data()

    combined_data = {
        "quiz_details": {
            "quiz_id": quiz_data["id"],
            "quiz_title": quiz_data["title"],
            "topic": quiz_data["topic"],
            "total_questions": quiz_data["questions_count"],
            "date": quiz_data["time"],
            "negative_marks": quiz_data["negative_marks"],
            "correct_answer_marks": quiz_data["correct_answer_marks"],
            "duration": quiz_data["duration"]
        },
        "student_performance": {
            "user_id": student_data["user_id"],
            "submitted_at": student_data["submitted_at"],
            "score": student_data["score"],
            "accuracy": student_data["accuracy"],
            "correct_answers": student_data["correct_answers"],
            "incorrect_answers": student_data["incorrect_answers"],
            "negative_score": student_data["negative_score"],
            "final_score": student_data["final_score"],
            "rank_text": student_data["rank_text"]
        }
    }

    return combined_data
