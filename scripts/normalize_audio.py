# scripts/normalize_audio.py
import os
from pydub import AudioSegment
from pydub.silence import detect_nonsilent

RAW_DIR = 'audio_raw'
OUT_DIR = 'audio_processed'
os.makedirs(OUT_DIR, exist_ok=True)

def remove_silence(audio, silence_thresh=-40, min_silence_len=300):
    nonsilent_ranges = detect_nonsilent(audio, min_silence_len=min_silence_len, silence_thresh=silence_thresh)
    if not nonsilent_ranges:
        return audio
    start_trim = nonsilent_ranges[0][0]
    end_trim = nonsilent_ranges[-1][1]
    return audio[start_trim:end_trim]

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
                        audio = remove_silence(audio)
                        # Bỏ qua file ngắn hơn 2 giây
                        if len(audio) < 2000:  # len(audio) tính bằng milliseconds
                            print(f"Bỏ qua {file} (sau cắt còn {len(audio)/1000:.2f}s)")
                            continue
                        filename = f"{folder}_{index}.wav"
                        audio.export(os.path.join(OUT_DIR, filename), format="wav")
                        print("✔", filename)
                        index += 1
                    except Exception as e:
                        print("✘", file, e)

if __name__ == "__main__":
    normalize_audio()
