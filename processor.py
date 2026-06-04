from transcriber import transcribe_video
from summarizer import generate_summary


def process_video(video_path):
    if video_path.lower().endswith(".txt"):
        with open(video_path, "r", encoding="utf-8") as f:
            transcript = f.read()
    else:
        transcript = transcribe_video(video_path)

    return generate_summary(transcript)
