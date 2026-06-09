import google.generativeai as genai
from config import API_KEY
from dotenv import load_dotenv
load_dotenv()
from google.api_core.exceptions import ResourceExhausted

genai.configure(
    api_key=API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def get_resume_feedback(prompt):


    try:
        response = model.generate_content(prompt)
        return response.text
    except ResourceExhausted:
        return """   
❌ Gemini API quota exceeded.
Please try again later or use a new API key.    """

    