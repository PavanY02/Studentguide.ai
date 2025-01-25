import json

def fetch_quiz_data():
    """Fetches quiz data from the JSON file."""
    try:
        with open("quiz_data.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def get_available_topics():
    """Extracts unique topics from quiz data."""
    quiz_data = fetch_quiz_data()
    if not quiz_data:
        return []

    # ✅ Get unique topics
    topics = sorted(set(quiz["topic"] for quiz in quiz_data if "topic" in quiz))
    return topics
