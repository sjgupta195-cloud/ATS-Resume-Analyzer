import google.generativeai as genai
from config import API_KEY
from dotenv import load_dotenv
load_dotenv()

genai.configure(
    api_key=API_KEY
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

def get_resume_feedback(prompt):

    response = model.generate_content(
        prompt
    )

    return response.text

