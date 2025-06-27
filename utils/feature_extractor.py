import wave
import struct
import math
import numpy as np
from numpy.fft import rfft, rfftfreq
import librosa

# Đọc WAV file (chuẩn hóa về mono và [-1, 1])
def read_wav_file(filepath):
    with wave.open(filepath, 'rb') as wf:
        num_channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        framerate = wf.getframerate()
        num_frames = wf.getnframes()
        raw_data = wf.readframes(num_frames)
        samples = struct.unpack('<' + 'h' * (len(raw_data) // 2), raw_data)
        if num_channels == 2:
            samples = [(samples[i] + samples[i+1]) / 2 for i in range(0, len(samples), 2)]
        return [s / 32768.0 for s in samples], framerate  # Chuẩn hóa về [-1, 1]

# Hàm tính đặc trưng âm thanh
def extract_features(filepath):
    y, sr = read_wav_file(filepath)
    N = len(y)

    # Zero Crossing Rate (ZCR)
    signs = [1 if s >= 0 else -1 for s in y]
    zero_crossings = sum(1 for i in range(1, N) if signs[i] != signs[i - 1])
    zcr = zero_crossings / (2 * N)

    # Root Mean Square (RMS)
    rms = math.sqrt(sum(s * s for s in y) / N)

    # FFT 
    spectrum_cpx = rfft(y)
    spectrum = [abs(x) for x in spectrum_cpx]
    total_spectrum = sum(spectrum) + 1e-10 

    # Tần số tương ứng
    freqs = rfftfreq(N, d=1/sr)

    # Spectral Centroid
    centroid = sum(f * s for f, s in zip(freqs, spectrum)) / total_spectrum

    # Spectral Bandwidth
    bandwidth = math.sqrt(sum(((f - centroid) ** 2) * s for f, s in zip(freqs, spectrum)) / total_spectrum)

    # Spectral Rolloff (85%)
    cumulative = []
    acc = 0
    for s in spectrum:
        acc += s
        cumulative.append(acc)
    rolloff_threshold = 0.85 * acc
    rolloff = 0
    for i, v in enumerate(cumulative):
        if v >= rolloff_threshold:
            rolloff = freqs[i]
            break

    # MFCC
    y_np = np.array(y, dtype=np.float32)
    mfcc = librosa.feature.mfcc(y=y_np, sr=sr, n_mfcc=20)
    mfcc_mean = [float(sum(row) / len(row)) for row in mfcc]

    # Trả về danh sách đặc trưng
    return [zcr, rms, centroid, bandwidth, rolloff] + mfcc_mean
