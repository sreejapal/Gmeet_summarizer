from google import genai
from dotenv import load_dotenv
import os
import json

# -----------------------------
# SETUP
# -----------------------------
load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODEL_NAME = "gemini-2.5-flash"


# -----------------------------
# SPLIT TRANSCRIPT
# -----------------------------
def split_transcript(text, max_words=1500):
    words = text.split()
    if not words:
        return []
    return [
        " ".join(words[i:i + max_words])
        for i in range(0, len(words), max_words)
    ]


# -----------------------------
# SAFE JSON PARSER
# -----------------------------
def safe_json_parse(text):
    text = text.replace("```json", "").replace("```", "").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None


# -----------------------------
# SUMMARIZE ONE CHUNK
# -----------------------------
def summarize_chunk(chunk):
    prompt = f"""
You are a strict JSON generator.

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
{chunk}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        parsed = safe_json_parse(response.text)
        if parsed:
            return parsed
    except Exception as e:
        print(f"[ERROR] summarize_chunk failed: {type(e).__name__}: {e}")

    return {
        "overview": "",
        "discussion_points": [],
        "action_items": [],
        "decisions": [],
        "task_assignments": [],
        "next_steps": []
    }


# -----------------------------
# MERGE SUMMARIES
# -----------------------------
def merge_summaries(summaries):
    merged = {
        "overview": "",
        "discussion_points": [],
        "action_items": [],
        "decisions": [],
        "task_assignments": [],
        "next_steps": []
    }
    for s in summaries:
        merged["overview"] += s.get("overview", "") + " "
        merged["discussion_points"].extend(s.get("discussion_points", []))
        merged["action_items"].extend(s.get("action_items", []))
        merged["decisions"].extend(s.get("decisions", []))
        merged["task_assignments"].extend(s.get("task_assignments", []))
        merged["next_steps"].extend(s.get("next_steps", []))
    return merged


# -----------------------------
# FINAL REFINEMENT
# -----------------------------
def refine_summary(merged_summary):
    prompt = f"""
Clean and refine the following meeting summary.

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
{json.dumps(merged_summary)}
"""

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        parsed = safe_json_parse(response.text)
        if parsed:
            return parsed
    except Exception as e:
        print(f"[ERROR] refine_summary failed: {type(e).__name__}: {e}")

    return merged_summary


# -----------------------------
# MAIN FUNCTION
# -----------------------------
def generate_summary(transcript):
    if not transcript or not transcript.strip():
        return {
            "overview": "Error: transcript was empty. Check that the uploaded file contains audio or text.",
            "discussion_points": [],
            "action_items": [],
            "decisions": [],
            "task_assignments": [],
            "next_steps": []
        }

    try:
        chunks = split_transcript(transcript)

        summaries = []
        for chunk in chunks:
            summaries.append(summarize_chunk(chunk))

        merged = merge_summaries(summaries)
        final = refine_summary(merged)
        return final

    except Exception as e:
        return {
            "overview": f"Error: {str(e)}",
            "discussion_points": [],
            "action_items": [],
            "decisions": [],
            "task_assignments": [],
            "next_steps": []
        }