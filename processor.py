from transcriber import transcribe_video
from summarizer import generate_summary
import json
import os


def process_video(video_path, meeting_name):
    # Route .txt files directly — ffmpeg cannot read them,
    # which caused transcribe_video() to return "" and all
    # summary fields to come back empty.
    if video_path.lower().endswith(".txt"):
        with open(video_path, "r", encoding="utf-8") as f:
            transcript = f.read()
    else:
        transcript = transcribe_video(video_path)

    result = generate_summary(transcript)

    save_summary(result)

    return result


def process_transcript_file(transcript_file):

    with open(
        transcript_file,
        "r",
        encoding="utf-8"
    ) as f:

        transcript = f.read()

    result = generate_summary(transcript)

    save_summary(result)

    return result


def process_transcript_text(transcript):

    result = generate_summary(transcript)

    save_summary(result)

    return result


def save_summary(result):

    try:

        os.makedirs(
            "summaries",
            exist_ok=True
        )

        with open(
            "summaries/summary.json",
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                result,
                f,
                indent=4
            )

    except Exception as e:

        print(
            f"Error saving summary: {e}"
        )