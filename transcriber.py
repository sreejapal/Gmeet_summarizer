import whisper
import torch
import os
import subprocess

device = "cuda" if torch.cuda.is_available() else "cpu"

model = whisper.load_model("base").to(device)


def convert_video_to_audio(video_path):
    audio_path = "temp_audio.mp3"

    subprocess.run(
        [
            "ffmpeg",
            "-i",
            video_path,
            "-vn",
            "-acodec",
            "mp3",
            audio_path
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    return audio_path


def transcribe_video(video_path):
    try:
        audio_path = convert_video_to_audio(video_path)

        result = model.transcribe(
            audio_path,
            fp16=torch.cuda.is_available(),
            language="en"
        )

        if os.path.exists(audio_path):
            os.remove(audio_path)

        return result.get("text", "")

    except Exception as e:
        raise e