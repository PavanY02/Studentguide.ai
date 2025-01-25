import json
import requests
import streamlit as st
import faiss
import numpy as np
import google.generativeai as genai
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAI

from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from config import GOOGLE_API_KEY

genai.configure(api_key=GOOGLE_API_KEY)

@st.cache_data
def load_quiz_data():
    with open("quiz_knowledge_base.json", "r", encoding="utf-8") as file:
        return json.load(file)

quiz_data = load_quiz_data()

@st.cache_data
def fetch_latest_quiz():
    url = "http://localhost:8000/latestquiz"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        st.error("❌ Failed to fetch latest quiz data from API")
        return None

quiz_metadata = fetch_latest_quiz()

quiz_details = quiz_metadata.get("quiz_details", {})
student_performance = quiz_metadata.get("student_performance", {})

student_id = student_performance.get("user_id", "Unknown Student")
quiz_title = quiz_details.get("quiz_title", "Unknown Quiz")
quiz_topic = quiz_details.get("topic", "Unknown Topic")
quiz_date = quiz_details.get("date", "Unknown Date")
total_questions = quiz_details.get("total_questions", 0)
correct_answers = student_performance.get("correct_answers", 0)
incorrect_answers = student_performance.get("incorrect_answers", 0)
accuracy = student_performance.get("accuracy", "Unknown Accuracy")
final_score = student_performance.get("final_score", "Unknown Score")

documents = []
for item in quiz_data["quiz_questions"]:
    context_text = f"Question: {item['question']}\nContext: {item['context']}\nCorrect Answer: {item['answer']}\nOther Options: {', '.join(item['other_options'])}"
    doc = Document(page_content=context_text, metadata={"question_id": item["question_id"]})
    documents.append(doc)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
split_docs = text_splitter.split_documents(documents)

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

faiss_index_path = "faiss_index"
if os.path.exists(faiss_index_path):
    db = FAISS.load_local(faiss_index_path, embedding_model, allow_dangerous_deserialization=True)
else:
    db = FAISS.from_documents(split_docs, embedding_model)
    db.save_local(faiss_index_path)

gemini_llm = GoogleGenerativeAI(model="gemini-1.5-pro-latest", api_key=GOOGLE_API_KEY)

prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""You are an expert tutor analyzing quiz results.

    Question: {question}
    Context: {context}

    Based on the given context, provide an explanation.
    If the student's answer was incorrect, explain why.
    """
)

qa_chain = RetrievalQA.from_chain_type(
    llm=gemini_llm,
    retriever=db.as_retriever(),
    chain_type_kwargs={"prompt": prompt_template}
)

st.title("🤖 AI-Powered Quiz Insights")
st.subheader(f"📌 Quiz Analysis for {student_id}")
st.write(f"📖 **Quiz Title**: {quiz_title}")
st.write(f"📖 **Topic**: {quiz_topic}")
st.write(f"📅 **Date**: {quiz_date}")
st.write(f"🎯 **Final Score**: {final_score}")

st.subheader("🔍 AI-Powered Quiz Insights")

questions_list = [q["question"] for q in quiz_data["quiz_questions"]]
selected_question = st.selectbox("📌 Select a Question for Analysis:", questions_list)

if selected_question:
    selected_question_data = next(q for q in quiz_data["quiz_questions"] if q["question"] == selected_question)

    # ✅ Fetch values **exactly as they are**
    student_answered = selected_question_data.get("student_answered", "Unknown")
    was_correct = selected_question_data.get("was_answer_correct", "Unknown")
    student_answer = selected_question_data.get("student_answer", "No Answer")
    correct_answer = selected_question_data.get("answer", "Unknown")
    other_options = ", ".join(selected_question_data.get("other_options", []))

    # ✅ Display Data As It Is
    st.markdown(f"✅ **Correct Answer:** {correct_answer}")
    st.markdown(f"🎯 **Did the Student Answer?** {student_answered}")
    st.markdown(f"🎯 **Was Student Correct?** {was_correct}")
    st.markdown(f"📚 **Other Options:** {other_options}")

    if st.button("🤖 Generate AI Feedback"):
        with st.spinner("Analyzing..."):
            response = qa_chain.run(selected_question)
            st.success("✅ AI Analysis Completed!")
            st.write(response)

if st.button("🔙 Back to Dashboard"):
    st.switch_page("app.py")