import json
import pandas as pd
import requests
import streamlit as st
import matplotlib.pyplot as plt
from config import FASTAPI_URL
from tools.data_fetcher import fetch_quiz_data

# 🔹 Fetch Past Quiz Data from FastAPI
@st.cache_data
def fetch_quiz_performance():
    response = requests.get(f"{FASTAPI_URL}/performance")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("❌ Failed to fetch past quiz performance from API")
        return None

# 🔹 Fetch Latest Quiz Data from FastAPI
@st.cache_data
def fetch_latest_quiz():
    response = requests.get(f"{FASTAPI_URL}/latestquiz")
    if response.status_code == 200:
        return response.json()
    else:
        st.error("❌ Failed to fetch latest quiz data from API")
        return None

# 🔹 Streamlit UI
st.title("📊 Student Quiz Performance Dashboard")

# 🔹 Sidebar: Topic Selection (Moved Up)
st.sidebar.header("🔍 Choose a Topic")
data = fetch_quiz_performance()
if data:
    df = pd.DataFrame(data["all_quiz_performance"])
    df["topic_title"] = df["quiz_identifier"]
    unique_topics = sorted(df["topic_title"].unique())

    selected_quiz = st.sidebar.selectbox("Choose a Topic:", unique_topics)
    st.session_state["selected_topic"] = selected_quiz.split(" - ")[0]

# 🔹 Sidebar: Study Guidance Section (Below Topic Selection)
st.sidebar.markdown("---")
st.sidebar.subheader("💬 Need Study Guidance?")
st.sidebar.page_link("pages/guide.py", label="🔹 Talk to AI Guide →")

# 🔹 Sidebar: Latest Quiz Results (Now Below Study Guidance)
st.sidebar.markdown("---")
st.sidebar.subheader("📌 Latest Quiz Results")

latest_quiz_data = fetch_latest_quiz()
if latest_quiz_data:
    quiz = latest_quiz_data["quiz_details"]
    student = latest_quiz_data["student_performance"]

    st.sidebar.text(f"📘 Topic: {quiz['topic']}")
    st.sidebar.text(f"📅 Date: {quiz['date']}")
    st.sidebar.text(f"🎯 Score: {student['score']}")
    st.sidebar.text(f"✅ Correct: {student['correct_answers']}")
    st.sidebar.text(f"❌ Incorrect: {student['incorrect_answers']}")
    st.sidebar.text(f"📊 Accuracy: {student['accuracy']}%")

    # 🔹 "AI Analysis" Button
    if st.sidebar.button("🔍 AI Analysis"):
        st.switch_page("pages/ai_analysis.py")

else:
    st.sidebar.warning("🚨 No recent quiz results available.")

# 🔹 Display Past Quiz Performance Data
if data:
    df_selected = df[df["topic_title"] == selected_quiz]

    st.subheader(f"🔹 Performance Summary for **{selected_quiz}**")
    col1, col2, col3 = st.columns(3)
    col1.metric("📌 Total Questions", int(df_selected["total_questions"].values[0]))
    col2.metric("📌 Total Attempted", int(df_selected["total_attempted"].values[0]))
    col3.metric("📌 Total Unanswered", int(df_selected["total_unattempted"].values[0]))

    col4, col5, col6 = st.columns(3)
    col4.metric("📌 Accuracy Rate", f"{df_selected['accuracy_rate'].values[0]:.2f} %")
    col5.metric("📌 Attempt Rate", f"{df_selected['attempt_rate'].values[0]:.2f} %")
    col6.metric("📌 Net Score", f"{df_selected['net_score'].values[0]:.2f}")

    # 🔹 Display Quiz Performance Table
    st.subheader("📋 Quiz Performance Details")
    st.dataframe(df_selected)

    # 🔹 **Charts**
    st.subheader("📊 Accuracy vs. Attempt Rate")
    fig, ax = plt.subplots(figsize=(6, 4))
    bars = ax.bar(["Accuracy Rate", "Attempt Rate"],
                  [df_selected["accuracy_rate"].values[0], df_selected["attempt_rate"].values[0]],
                  color=["green", "blue"])
    ax.set_ylabel("Percentage (%)")
    ax.set_title("📈 Accuracy vs. Attempt Rate")

    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.1f}%", ha='center', va='bottom')

    st.pyplot(fig)
