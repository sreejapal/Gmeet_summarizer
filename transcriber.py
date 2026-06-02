import whisper
import torch

device = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model("base").to(device)

def transcribe_video(video_path):
    result = model.transcribe(video_path)

    transcript = result["text"]

    return transcript