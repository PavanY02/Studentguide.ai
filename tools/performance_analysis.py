import pandas as pd
import json
from datetime import datetime

def analyze_performance(topic):
    """Extracts all quiz attempts for the given topic, calculates trends, and tracks student improvement."""

    try:
        with open("quiz_data.json", "r") as f:
            quiz_data = json.load(f)
    except FileNotFoundError:
        return None, "❌ Quiz data file not found."

    df = pd.DataFrame(quiz_data)

    if df.empty:
        return None, "⚠️ No quiz data available."

    # ✅ Filter data for the selected topic
    df_filtered = df[df["topic"].str.lower() == topic.lower()]

    if df_filtered.empty:
        return None, f"⚠️ No quiz data found for the topic: {topic}"

    # ✅ Convert `started_at` to datetime for sorting
    df_filtered["started_at"] = pd.to_datetime(df_filtered["started_at"])

    # ✅ Sort by date (oldest to newest) to track progress
    df_filtered = df_filtered.sort_values(by="started_at")

    # ✅ Convert `Timestamp` to string before returning JSON
    df_filtered["started_at"] = df_filtered["started_at"].dt.strftime("%Y-%m-%d %H:%M:%S")

    # ✅ Calculate missing columns before using them
    df_filtered["total_attempted"] = df_filtered["correct_answers"] + df_filtered["incorrect_answers"]
    df_filtered["total_unattempted"] = df_filtered["total_questions"] - df_filtered["total_attempted"]

    # ✅ Ensure no negative values in `total_unattempted`
    df_filtered["total_unattempted"] = df_filtered["total_unattempted"].apply(lambda x: max(0, x))

    # ✅ Calculate performance metrics
    df_filtered["accuracy_rate"] = (df_filtered["correct_answers"] / df_filtered["total_attempted"]) * 100
    df_filtered["attempt_rate"] = (df_filtered["total_attempted"] / df_filtered["total_questions"]) * 100
    df_filtered["unanswered_rate"] = (df_filtered["total_unattempted"] / df_filtered["total_questions"]) * 100
    df_filtered["net_score"] = (df_filtered["correct_answers"] * df_filtered["correct_answer_marks"]) - (
        df_filtered["incorrect_answers"] * df_filtered["negative_marks"])

    avg_accuracy = df_filtered["accuracy_rate"].mean()
    avg_attempt_rate = df_filtered["attempt_rate"].mean()
    avg_unanswered_rate = df_filtered["unanswered_rate"].mean()

    # ✅ Track improvements by comparing first and last quiz
    first_attempt = df_filtered.iloc[0]
    latest_attempt = df_filtered.iloc[-1]

    accuracy_change = latest_attempt["accuracy_rate"] - first_attempt["accuracy_rate"]
    net_score_change = latest_attempt["net_score"] - first_attempt["net_score"]

    improvement_summary = (
        f"📈 **Performance Over Time in {topic}**\n"
        f"- **First Quiz Date:** {first_attempt['started_at']}\n"
        f"- **Latest Quiz Date:** {latest_attempt['started_at']}\n"
        f"- **Accuracy Change:** {accuracy_change:+.2f}%\n"
        f"- **Net Score Change:** {net_score_change:+.2f} points\n\n"
        f"✅ **Total Quizzes Taken:** {len(df_filtered)}"
        f"\n\nDoes the student show improvement? {'✅ Yes' if accuracy_change > 0 else '❌ No'}"
    )

    # ✅ Convert detailed quiz data to JSON format for AI analysis
    full_quiz_history = df_filtered.to_dict(orient="records")

    # ✅ Final structured performance summary
    performance_summary = (
        f"📊 **Overall Performance in {topic}**\n"
        f"- **Average Accuracy Rate:** {avg_accuracy:.2f}%\n"
        f"- **Average Attempt Rate:** {avg_attempt_rate:.2f}%\n"
        f"- **Average Unanswered Rate:** {avg_unanswered_rate:.2f}%\n"
        f"- **Total Quizzes Taken:** {len(df_filtered)}\n\n"
        f"{improvement_summary}\n\n"
        f"Here is the detailed performance history:"
    )

    return full_quiz_history, performance_summary  # ✅ Removed quiz_id
