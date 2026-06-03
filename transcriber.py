import whisper
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model("base").to(device)


def transcribe_video(video_path):
    try:
        result = model.transcribe(
            video_path,
            fp16=torch.cuda.is_available(),
            language="en",
        )

        return result.get("text", "")

    except Exception as e:
        print(f"Transcription error: {e}")
        return ""
