import requests
import json
import re

# **API Endpoints**
QUIZ_API = "https://www.jsonkeeper.com/b/LLQT"  # Replace with actual quiz API URL
STUDENT_API = "https://api.jsonserve.com/rJvd7g"  # Replace with actual student API URL

# **Output JSON File**
OUTPUT_FILE = "../quiz_knowledge_base.json"


# **🔹 Fetch Quiz Data**
def fetch_quiz_data():
    response = requests.get(QUIZ_API)
    if response.status_code == 200:
        return response.json()["quiz"]["questions"]  # ✅ Extracting only questions
    else:
        raise Exception("❌ Failed to fetch quiz data")


# **🔹 Fetch Student Data**
def fetch_student_data():
    response = requests.get(STUDENT_API)
    if response.status_code == 200:
        return response.json()  # ✅ Extracting full student data
    else:
        raise Exception("❌ Failed to fetch student data")


# **🔹 Clean Text Function (Removes Markdown & Extra Spaces)**
def clean_text(text):
    if text:
        text = re.sub(r'\*\*|\*', '', text)  # ✅ Remove Markdown (**bold** and *italic*)
        text = re.sub(r'\n+', ' ', text).strip()  # ✅ Replace newlines with spaces
    return text


# **🔹 Process Data & Create JSON**
def process_quiz_data():
    questions = fetch_quiz_data()
    student_data = fetch_student_data()

    # Extract student response map (Question ID -> Answer ID)
    response_map = student_data.get("response_map", {})

    quiz_knowledge_base = []

    for question in questions:
        question_id = question["id"]
        question_text = question["description"]
        context = clean_text(question.get("detailed_solution", ""))  # ✅ Cleaned context

        # Finding the Correct Answer
        correct_answer = None
        correct_answer_id = None
        all_options = []
        for option in question["options"]:
            all_options.append(option["description"])  # ✅ Store all answer choices
            if option["is_correct"]:  # ✅ If is_correct == True
                correct_answer = option["description"]
                correct_answer_id = option["id"]

        # Remove the correct answer from options to keep only incorrect ones
        other_options = [opt for opt in all_options if opt != correct_answer]

        # **Check if Student Answered**
        student_answered = "Yes" if str(question_id) in response_map else "No"

        # **Check if Student Answer was Correct**
        student_selected_answer_id = response_map.get(str(question_id), None)
        was_answer_correct = "No"
        if student_selected_answer_id == correct_answer_id:
            was_answer_correct = "Yes"

        # Append Processed Question
        quiz_knowledge_base.append({
            "question_id": question_id,
            "question": question_text,
            "answer_id": correct_answer_id,
            "answer": correct_answer,
            "student_answered": student_answered,
            "was_answer_correct": was_answer_correct,
            "other_options": other_options,  # ✅ Added other options
            "context": context
        })

    # **Save Data as JSON**
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump({"quiz_questions": quiz_knowledge_base}, f, indent=4, ensure_ascii=False)

    print(f"✅ JSON file '{OUTPUT_FILE}' created successfully!")


# **🔹 Run the Script**
if __name__ == "__main__":
    process_quiz_data()
