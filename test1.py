import os
import subprocess

ffmpeg_path = os.path.join("ffmpeg", "bin", "ffmpeg.exe")

result = subprocess.run([ffmpeg_path, "-version"], capture_output=True, text=True)

print(result.stdout)