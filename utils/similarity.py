import numpy as np
from utils.feature_extractor import extract_features
import sqlite3
from sklearn.metrics.pairwise import cosine_similarity

DB_PATH = 'database/animalsounds.db'

def find_similar(filepath, k=10):
    print("🔍 Đang trích xuất đặc trưng từ:", filepath)
    try:
        query_vec = np.array(extract_features(filepath), dtype=np.float32)
    except Exception as e:
        print("❌ Lỗi khi trích xuất đặc trưng:", e)
        raise

    # Lấy dữ liệu từ CSDL
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT filename, zcr, rms, centroid, bandwidth, rolloff, " +
        ",".join([f"mfcc{i}" for i in range(1, 21)]) + " FROM features"
    )
    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print("⚠️ Không tìm thấy dữ liệu trong CSDL!")
        return []

    # Vector đặc trưng từ database
    db_features = np.array([
        [float(x) if x is not None else 0.0 for x in row[1:]]
        for row in rows
    ], dtype=np.float32)

    # Chuẩn hóa bằng z-score
    mean = np.mean(db_features, axis=0)
    std = np.std(db_features, axis=0) + 1e-10
    db_features_norm = (db_features - mean) / std
    query_vec_norm = (query_vec - mean) / std

    # Tính cosine similarity
    query_vec_norm = query_vec_norm.reshape(1, -1)
    cos_sim = cosine_similarity(query_vec_norm, db_features_norm)[0]  # vector 1D

    # Lấy top k
    top_k_idx = np.argsort(cos_sim)[::-1][:k]
    top_k = [(rows[i][0], float(cos_sim[i])) for i in top_k_idx]

    # Định dạng lại độ giống thành phần trăm
    results = []
    for filename, sim in top_k:
        percent = round(sim * 100, 2)
        results.append((filename, f"{percent}%", sim))

    return results
