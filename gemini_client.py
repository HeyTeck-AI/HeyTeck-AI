import os
from typing import Optional

def generate_heyteck_output(prompt: str, api_key: Optional[str] = None, model_name: str = "gemini-3.6-flash") -> str:
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError("🔑 Gemini API Key missing!")

    models_to_try = [model_name, "gemini-3.6-flash", "gemini-1.5-flash"]
    seen = set()
    models_to_try = [m for m in models_to_try if not (m in seen or seen.add(m))]

    last_error = None
    for m in models_to_try:
        try:
            from google import genai
            client = genai.Client(api_key=key)
            response = client.models.generate_content(
                model=m,
                contents=prompt,
            )
            return response.text
        except Exception as e:
            last_error = e

    raise RuntimeError(f"Error calling Gemini API: {str(last_error)}")
