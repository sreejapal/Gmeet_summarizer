import whisper
import torch
import os
import subprocess

# ✅ Device setup
device = "cuda" if torch.cuda.is_available() else "cpu"

# ✅ Add FFmpeg to PATH
ffmpeg_bin = os.path.join(os.getcwd(), "ffmpeg", "bin")
os.environ["PATH"] += os.pathsep + ffmpeg_bin

# ✅ Load model
model = whisper.load_model("base").to(device)


# 🔹 Step 1: Convert video → audio
def convert_video_to_audio(video_path):
    audio_path = "temp_audio.mp3"

    ffmpeg_path = os.path.join("ffmpeg", "bin", "ffmpeg.exe")

    subprocess.run([
        ffmpeg_path,
        "-i", video_path,
        "-vn",                # no video
        "-acodec", "mp3",     # audio format
        audio_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    return audio_path


# 🔹 Step 2: Transcribe
def transcribe_video(video_path):
    try:
        # ✅ Convert first
        audio_path = convert_video_to_audio(video_path)

        # ✅ Then transcribe
        result = model.transcribe(
            audio_path,
            fp16=torch.cuda.is_available(),
            language="en",
        )

        # ✅ Optional: delete temp file
        if os.path.exists(audio_path):
            os.remove(audio_path)

        return result.get("text", "")

    except Exception as e:
        print(f"Transcription error: {e}")
        return ""