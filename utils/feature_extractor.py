import numpy as np
from scipy.io import wavfile
import librosa

def extract_features(filepath):
    print("Đang tải file:", filepath)
    try:
        sr, y = wavfile.read(filepath)
        y = y.astype(np.float32)
        if y.ndim > 1:
            y = y.mean(axis=1)  # chuyển về mono nếu là stereo
    except Exception as e:
        print("❌ Lỗi khi tải file âm thanh:", e)
        raise

    # Chuẩn hóa tín hiệu về [-1, 1] để các đặc trưng đều là số thực nhỏ
    y = y / (np.max(np.abs(y)) + 1e-10)

    # ZCR (Zero Crossing Rate)
    zcr = float(np.mean(np.abs(np.diff(np.sign(y)))) / 2)

    # RMS (Root Mean Square)
    rms = float(np.sqrt(np.mean(y ** 2)))

    # Centroid (Spectral Centroid)
    spectrum = np.abs(np.fft.rfft(y))
    freqs = np.fft.rfftfreq(len(y), d=1/sr)
    centroid = float(np.sum(freqs * spectrum) / (np.sum(spectrum) + 1e-10))

    # Bandwidth (Spectral Bandwidth)
    bandwidth = float(np.sqrt(np.sum(((freqs - centroid) ** 2) * spectrum) / (np.sum(spectrum) + 1e-10)))

    # Rolloff (Spectral Rolloff, 85%)
    cumulative = np.cumsum(spectrum)
    rolloff_threshold = 0.85 * cumulative[-1]
    rolloff = float(freqs[np.where(cumulative >= rolloff_threshold)[0][0]])

    # MFCC dùng librosa
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    mfcc_mean = [float(x) for x in np.mean(mfcc, axis=1)]

    return [zcr, rms, centroid, bandwidth, rolloff] + mfcc_mean