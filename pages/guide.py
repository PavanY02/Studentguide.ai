import json
import streamlit as st
from crew_ai import create_crewai_agent
from tools.performance_analysis import analyze_performance

st.title("💡 AI Guide for Students")

# ✅ Check if a topic is selected in `st.session_state`
if "selected_topic" in st.session_state and st.session_state["selected_topic"]:
    selected_topic = st.session_state["selected_topic"]
    st.sidebar.write(f"📌 **Selected Topic:** {selected_topic}")

    # ✅ Reset AI response when the topic changes
    if "last_topic" not in st.session_state:
        st.session_state["last_topic"] = selected_topic  # Store first selected topic

    if st.session_state["last_topic"] != selected_topic:
        st.session_state["ai_response"] = None  # Reset AI response
        st.session_state["last_topic"] = selected_topic  # Update stored topic

else:
    st.sidebar.warning("⚠️ No topic selected! Please go back and choose a topic.")
    st.stop()  # 🔹 Stops execution if no topic is selected

# ✅ Keep AI response persistent across page reloads
if "ai_response" not in st.session_state:
    st.session_state["ai_response"] = None

# ✅ Fetch AI Guidance Based on Selected Topic
if st.sidebar.button("📢 Get Guidance") or st.session_state["ai_response"]:
    st.subheader(f"🎯 Guidance on **{selected_topic}**")

    # ✅ Only fetch new data if AI response is empty
    if st.session_state["ai_response"] is None:
        # ✅ Fetch full student quiz data for the selected topic
        quiz_history, performance_summary = analyze_performance(selected_topic)

        if not quiz_history:
            st.warning(performance_summary)  # Show warning message if no data found
        else:
            # ✅ Pass only topic, quiz history, and performance summary
            crew = create_crewai_agent(selected_topic, quiz_data_json=quiz_history,
                                       performance_summary=performance_summary)
            result = crew.kickoff(inputs={
                "topic": selected_topic,
                "quiz_history": quiz_history
            })

            # ✅ Extract raw text from CrewOutput
            if hasattr(result, "raw") and isinstance(result.raw, str):
                st.session_state["ai_response"] = result.raw  # ✅ Store response in session state
            else:
                st.session_state["ai_response"] = str(result)  # ✅ Convert to string if needed

    # ✅ Display the stored AI response (Persistent!)
    st.subheader("📊 Performance Summary")
    st.write(st.session_state["ai_response"])

    # 🔹 Format Recommendations as Clickable Links
    st.subheader("📚 Recommended Learning Resources")

    # ✅ Extract YouTube & Google Links
    lines = st.session_state["ai_response"].split("\n")  # ✅ Now this will work!
    article_section = "\n".join([line for line in lines if "http" in line and "youtube" not in line])
    video_section = "\n".join([line for line in lines if "youtube" in line])

    st.markdown("#### 📖 Articles")
    st.markdown(article_section, unsafe_allow_html=True)

    st.markdown("#### 🎥 YouTube Videos")
    st.markdown(video_section, unsafe_allow_html=True)
