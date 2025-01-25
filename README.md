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
   cd studentguider_ai
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
![Dashboard](screenshots/dashboard.png)

### **AI Quiz Analysis**
![AI Analysis](screenshots/ai_analysis.png)

### **AI Study Guide**
![Study Guide](screenshots/guide.png)

## 🔮 Future Enhancements
- **Voice-based AI Assistant** for guiding students.
- **Personalized Study Plan** generation.
- **Integration with Learning Management Systems (LMS)**.

## 🤝 Contributing
Pull requests are welcome! Please ensure your code follows best practices and includes documentation.

## 📜 License
This project is licensed under the MIT License.

