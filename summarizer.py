from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_summary(transcript):

    prompt = f"""
Analyze the transcript.

Return ONLY valid JSON.

{{
  "overview": "",
  "discussion_points": [],
  "action_items": [],
  "decisions": [],
  "task_assignments": [],
  "next_steps": []
}}

Transcript:

{transcript}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    response_text = response.text

    response_text = (
        response_text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    data = json.loads(response_text)

    return data