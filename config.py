import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# FastAPI Server URL
FASTAPI_URL = "http://127.0.0.1:8000"  # ✅ Full dataset (contains mistakes_corrected)
# FASTAPI_PERFORMANCE_URL = "http://127.0.0.1:8000/performance"  # ✅ Only performance metrics


# API Keys
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "dummy_value")  # ✅ Ensures a fallback value

# Check API key loading
if not YOUTUBE_API_KEY:
    print("⚠️ Warning: YOUTUBE_API_KEY is missing! Check your .env file.")
if not SERPER_API_KEY:
    print("⚠️ Warning: SERPER_API_KEY is missing! Check your .env file.")
if not OPENAI_API_KEY:
    print("⚠️ Warning: OPENAI_API_KEY is missing! Using default 'dummy_value'.")