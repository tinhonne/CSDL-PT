import os
from utils.feature_extractor import extract_features
from utils.db_utils import insert_features

AUDIO_DIR = 'audio_processed'

def process_all():
    for file in os.listdir(AUDIO_DIR):
        if not file.endswith('.wav'):
            continue

        path = os.path.join(AUDIO_DIR, file)
        try:
            features = extract_features(path)
            insert_features(file, features)
            print("✔ Đã lưu:", file)
        except Exception as e:
            print("✘ Lỗi:", file, "→", e)

if __name__ == '__main__':
    process_all()
