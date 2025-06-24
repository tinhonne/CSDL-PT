import librosa
import numpy as np

def extract_features(filepath):
    print("Đang tải file:", filepath)
    try:
        y, sr = librosa.load(filepath, sr=22050, mono=True)
    except Exception as e:
        print("❌ Lỗi khi tải file âm thanh:", e)
        raise

    zcr = float(np.mean(librosa.feature.zero_crossing_rate(y)))
    rms = float(np.mean(librosa.feature.rms(y=y)))
    centroid = float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr)))
    bandwidth = float(np.mean(librosa.feature.spectral_bandwidth(y=y, sr=sr)))
    rolloff = float(np.mean(librosa.feature.spectral_rolloff(y=y, sr=sr, roll_percent=0.85)))
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfcc_mean = [float(x) for x in np.mean(mfcc, axis=1)]

    return [zcr, rms, centroid, bandwidth, rolloff] + mfcc_mean