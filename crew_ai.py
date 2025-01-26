from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool, YoutubeVideoSearchTool
from config import GOOGLE_API_KEY, SERPER_API_KEY, YOUTUBE_API_KEY


google_search_tool = SerperDevTool(api_key=SERPER_API_KEY)
youtube_search_tool = YoutubeVideoSearchTool(api_key=YOUTUBE_API_KEY)
import json

gemini_llm = LLM(
    model="gemini/gemini-1.5-pro-latest",
    api_key=GOOGLE_API_KEY,
    temperature=0.7
)

import json

def create_crewai_agent(topic, quiz_data_json, performance_summary):
    """Creates CrewAI system with full quiz history and performance trends."""

    student_guide = Agent(
        role="Student Performance Guide",
        goal="Analyze all quiz attempts to track student progress and suggest study resources.",
        verbose=True,
        llm=gemini_llm,
        backstory=(
            "You are an AI Mentor Assigned  to monitor and  help the student and  do  student performance analysis. "
            "Your task is to review ALL quiz attempts, compare them over time, and "
            "provide accurate feedback on whether the student is improving or struggling."
            "Talk to him like He is Your Student ,You know hom for a while"
        ),
        tools=[google_search_tool, youtube_search_tool]
    )


    quiz_data_str = json.dumps(quiz_data_json, indent=4).replace("{", "{{").replace("}", "}}")


    guide_task_description = (
        f"Analyze the student's quiz performance in **{topic}**.\n\n"
        f"### 📊 **Performance Trends**\n"
        f"{performance_summary}\n\n"
        f"Here is the student's complete quiz history:\n\n"
        f"{quiz_data_str}\n\n"  
        f"### 🔹 Key Points to Analyze:\n"
        f"1️⃣ **Highlight weak areas, improvement trends, and performance gaps for a given user.**\n\n"
        f"2️⃣ **Identify specific strengths and weaknesses with creative labels or insights.**\n"
        f"3️⃣ **Analyze if the student is improving over multiple attempts.**\n"
        f"4️⃣ **Detect the weakest concepts based on repeated mistakes.**\n\n"
        f"5️⃣ **Use `youtube_search_tool.run('{topic} tutorial')` to find 2 relevant YouTube videos.**\n"
        f"6️⃣ **Use `google_search_tool.run('{topic} tutorial')` to find 2 relevant articles.**\n"
        f"7️⃣ **Ensure the YouTube video links are clickable for easy access.**"
        f"🎯 **Your output MUST include clickable YouTube and article links.**"
    )

    guide_task = Task(
        description=guide_task_description,
        expected_output="A structured report tracking performance trends and study recommendations, including clickable links and aslo the students  data you have in a  good human readable format .",
        tools=[google_search_tool, youtube_search_tool],
        agent=student_guide
    )

    crew = Crew(
        agents=[student_guide],
        tasks=[guide_task],
        process=Process.sequential
    )

    return crew
