from google import genai

from src.config import settings


client = genai.Client(api_key=settings.google_api_key)
def get_llm_response(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-pro-exp-03-25", contents=prompt
    )

    return response.text
