from google import genai

from src.constants import GOOGLE_API_KEY


client = genai.Client(api_key=GOOGLE_API_KEY)
def get_llm_response(prompt: str) -> str:
    response = client.models.generate_content(
        model="gemini-2.5-pro-exp-03-25", contents=prompt
    )

    return response.text
