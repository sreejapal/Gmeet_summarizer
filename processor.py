from transcriber import transcribe_video
from summarizer import generate_summary
import json


def process_video(video_path):
    transcript = transcribe_video(video_path)
    return generate_summary(transcript)


def process_transcript_file(transcript_file):
    with open(transcript_file, "r", encoding="utf-8") as f:
        transcript = f.read()

    return generate_summary(transcript)


if __name__ == "__main__":

    choice = input(
        "Choose input type:\n"
        "1. Video (MP4)\n"
        "2. Transcript (TXT)\n"
        "Enter choice: "
    )

    if choice == "1":
        result = process_video("sample.mp4")

    elif choice == "2":
        result = process_transcript_file("test.txt")

    else:
        print("Invalid choice")
        exit()

    with open(
        "summaries/summary.json",
        "w",
        encoding="utf-8"
    ) as f:
        json.dump(result, f, indent=4)

    print("\nSummary saved successfully!")