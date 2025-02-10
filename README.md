# Student Guider AI - Quiz Analysis System

## 📌 Project Overview
The **Student Guider AI** is an intelligent system designed to analyze student quiz performances, providing AI-powered insights into their strengths and areas for improvement. The system processes quiz data, evaluates student answers, and leverages **Crewai**, **LangChain** and **Google Gemini AI** to generate feedback based on quiz results.

## 🚀 Features
- **Fetch & Process Quiz Data**: Extract quiz details and student responses from FastAPI endpoints.
- **RAG-based AI Analysis**: Utilize FAISS vector storage and Gemini AI for retrieval-augmented generation (RAG).
- **Streamlit Dashboard**: Provide an interactive interface for students to review their performance.
- **Agentic Ai Feedback**: Provides detailed  Analysis like Strengths,Weakness, Areas of Improvement and Provide Resources using Serper and YoutubeSearchTools for Student  improvement .
- **Multi-Page Navigation**: Includes AI analysis, study guide, and past performance tracking.

## 🛠️ Setup Instructions

### 🔹 Prerequisites
- Python 3.8+
- Virtual Environment (`venv` or `conda`)
- API Keys (Google Gemini API, FastAPI URL)

### 🔹 Installation
1. **Clone the Repository**
   ```sh
   git clone <repo_url>
   cd studentguide.ai
   ```
2. **Create a Virtual Environment**
   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On macOS/Linux
   .venv\Scripts\activate     # On Windows
   ```
3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```
4. **Set Up API Keys**
   - Create a `.env` file in the `tools/` directory and add:
     ```sh
     GOOGLE_API_KEY=<your_google_api_key>
     FASTAPI_URL=http://localhost:8000
     SERPER_API_KEY=<your_serper_api_key>
     YOUTUBE_API_KEY=<your_youtube_api_key>
     ```

### 🔹 Run the Application
1. **Start FastAPI Server**
   ```sh
   uvicorn tools.api:app --reload
   ```
2. **Run Streamlit Dashboard**
   ```sh
   streamlit run app.py
   ```

## 📊 Approach & Data Processing

### **1️⃣ Fetching Quiz & Student Data**
- The application retrieves quiz questions and student responses from FastAPI (`latestquiz`, `performance`).
- The data is structured into `quiz_knowledge_base.json` for AI analysis.

### **2️⃣ FAISS Vector Storage for RAG And AI Analysis with Langchain & Gemini AI **
- Questions, correct answers, and explanations are embedded using **HuggingFace Sentence Transformers**.
- FAISS stores these embeddings for efficient similarity searches.
- - LangChain’s **RetrievalQA** fetches relevant information based on the selected question.
- **Google Gemini AI** generates explanations and feedback for incorrect answers.

### **3️⃣ CrewAi RAG Agent for Topic Specific Analysis with Gemini AI and CrewAi tools**
- Crewai **Agent** fetches relevant information of student  and based on the selected data Generate detail suggestions.
- **Crewai_tools** Helps gather additional Resources related to specific topic and  Recommend  it to student for their improvement .

### **4️⃣ Interactive UI with Streamlit**
- **Dashboard (`app.py`)**: Displays past and latest quiz performance.
- **AI Analysis (`ai_analysis.py`)**: Provides detailed explanations and recommendations.
- **Study Guide (`guide.py`)**: Helps students learn how to overcome their Weakness and Make a room for Improvement .

## 📷 Screenshots
Below are key screenshots showcasing the system’s functionalities:

### **Student Quiz Performance Dashboard**
![image](https://github.com/user-attachments/assets/85b7ad17-07f6-47a2-9e1a-9010f588a398)



### **AI Quiz Analysis**
![image](https://github.com/user-attachments/assets/0a92fdb1-3589-421e-a8eb-1f5d6149ef1b)


### **Testline Mentor**
![image](https://github.com/user-attachments/assets/a99f6a9d-c43e-43a5-bc72-3004f7c9b45f)
![image](https://github.com/user-attachments/assets/163f8d4a-26a3-4e49-8ce9-96c8dc5d860c)


![image](https://github.com/user-attachments/assets/ab30b41a-5c30-434b-96cb-6e18a947143e)

![image](https://github.com/user-attachments/assets/2825a0ec-7a46-42f3-a5bd-08df4a11ce7d)

### **Fast APi END points**
![image](https://github.com/user-attachments/assets/c4bb7b6c-62f5-444d-bc8b-8ca39b33b2ca)




## 🔮 Future Enhancements
- **Voice-based AI Assistant** for guiding students.
- **Personalized Study Plan** generation.






