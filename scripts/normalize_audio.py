# scripts/normalize_audio.py
import os
from pydub import AudioSegment

RAW_DIR = 'audio_raw'
OUT_DIR = 'audio_processed'
os.makedirs(OUT_DIR, exist_ok=True)

def normalize_audio():
    index = 0
    for folder in os.listdir(RAW_DIR):
        folder_path = os.path.join(RAW_DIR, folder)
        if os.path.isdir(folder_path):
            for file in os.listdir(folder_path):
                if file.endswith(('.mp3', '.wav')):
                    path = os.path.join(folder_path, file)
                    try:
                        audio = AudioSegment.from_file(path)
                        audio = audio.set_channels(1).set_frame_rate(22050)
                        filename = f"{folder}_{index}.wav"
                        audio.export(os.path.join(OUT_DIR, filename), format="wav")
                        print("✔", filename)
                        index += 1
                    except Exception as e:
                        print("✘", file, e)

if __name__ == "__main__":
    normalize_audio()
