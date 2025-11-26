import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv(dotenv_path=os.path.join(os.getcwd(), ".env"))

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in .env")

genai.configure(api_key=API_KEY)

MODEL_NAME = "gemini-2.0-flash"

# create model
model = genai.GenerativeModel(MODEL_NAME)

def ask_gemini(prompt: str, max_output_tokens: int = 500, temperature: float = 0.2):
    try:
        # IMPORTANT: gemini v2 uses list content format
        response = model.generate_content(
            [prompt],  # ← THIS IS THE FIX
            generation_config={
                "temperature": temperature,
                "max_output_tokens": max_output_tokens
            }
        )

        # response.text is always available
        return getattr(response, "text", str(response))

    except Exception as e:
        return f"❌ Gemini error: {e}"
