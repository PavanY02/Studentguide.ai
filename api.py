from fastapi import FastAPI
from data_modules.past_quizzes_preprocessing import analyze_performance as analyze_past_quizzes,load_quiz_data
from data_modules.latest_quiz_preprocessing import get_full_quiz_data as latest_quiz_data

# Initialize FastAPI
app = FastAPI()

# **Root Endpoint**
@app.get("/")
async def root():
    return {"message": "Welcome to the Student Quiz Analysis API"}
@app.get("/all")
async def get_quiz_info():
    quiz_data = load_quiz_data()
    return {"quizzes": quiz_data}
# **Performance Analysis for A**
@app.get("/performance")
async def past_performance():
    return analyze_past_quizzes()

# **Performance Analysis for B**
@app.get("/latestquiz")
async def latest_performance():
    return latest_quiz_data()

# **Run FastAPI**
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
