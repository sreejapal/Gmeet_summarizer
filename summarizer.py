from google import genai
from dotenv import load_dotenv
import os
import json

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash"

EMPTY_SUMMARY = {
    "overview": "",
    "discussion_points": [],
    "action_items": [],
    "decisions": [],
    "task_assignments": [],
    "next_steps": []
}


def split_transcript(text, max_words=1500):
    words = text.split()
    if not words:
        return []
    return [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]


def safe_json_parse(text):
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


def summarize_chunk(chunk):
    prompt = f"""You are a strict JSON generator.

Return ONLY valid JSON. No explanation.

Format:
{{
  "overview": "",
  "discussion_points": [],
  "action_items": [],
  "decisions": [],
  "task_assignments": [],
  "next_steps": []
}}

Transcript:
{chunk}"""

    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        parsed = safe_json_parse(response.text)
        if parsed:
            return parsed
    except Exception as e:
        print(f"[ERROR] summarize_chunk: {type(e).__name__}: {e}")

    return EMPTY_SUMMARY.copy()


def merge_summaries(summaries):
    merged = {key: [] for key in EMPTY_SUMMARY}
    merged["overview"] = ""
    for s in summaries:
        merged["overview"] += s.get("overview", "") + " "
        for key in ["discussion_points", "action_items", "decisions", "task_assignments", "next_steps"]:
            merged[key].extend(s.get(key, []))
    return merged


def refine_summary(merged):
    prompt = f"""Clean and refine the following meeting summary.

Remove duplicates. Make it clear and concise.

Return ONLY valid JSON in this format:
{{
  "overview": "",
  "discussion_points": [],
  "action_items": [],
  "decisions": [],
  "task_assignments": [],
  "next_steps": []
}}

Data:
{json.dumps(merged)}"""

    try:
        response = client.models.generate_content(model=MODEL_NAME, contents=prompt)
        parsed = safe_json_parse(response.text)
        if parsed:
            return parsed
    except Exception as e:
        print(f"[ERROR] refine_summary: {type(e).__name__}: {e}")

    return merged


def generate_summary(transcript):
    if not transcript or not transcript.strip():
        return {
            **EMPTY_SUMMARY,
            "overview": "Error: transcript was empty. Check that the uploaded file contains audio or text."
        }

    try:
        chunks = split_transcript(transcript)
        summaries = [summarize_chunk(chunk) for chunk in chunks]
        merged = merge_summaries(summaries)
        return refine_summary(merged)
    except Exception as e:
        return {**EMPTY_SUMMARY, "overview": f"Error: {str(e)}"}
