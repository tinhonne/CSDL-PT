import sqlite3
import numpy as np
import os
import math
from utils.feature_extractor import extract_features

DB_PATH = 'database/animalsounds.db'

def find_similar(filepath, k=10):
    print("DB_PATH absolute:", os.path.abspath(DB_PATH))
    if not os.path.exists(DB_PATH):
        raise FileNotFoundError("File cơ sở dữ liệu không tồn tại!")

    print("Đang trích xuất đặc trưng từ:", filepath)
    try:
        query_vec = np.array(extract_features(filepath), dtype=np.float32)
    except Exception as e:
        print("❌ Lỗi khi trích xuất đặc trưng:", e)
        raise

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT filename, zcr, rms, centroid, bandwidth, rolloff, " +
        ",".join([f"mfcc{i}" for i in range(1, 21)]) + " FROM features"
    )

    rows = cursor.fetchall()
    results = []
    for row in rows:
        try:
            filename = row[0]
            db_vec = np.array([float(x) if x is not None else 0.0 for x in row[1:]], dtype=np.float32)
            distance = np.linalg.norm(query_vec - db_vec)
            results.append((distance, filename, row))
        except (ValueError, TypeError) as e:
            print(f"⚠️ Bỏ qua hàng {filename} do lỗi: {e}")

    conn.close()
    if not results:
        print("⚠️ Không tìm thấy kết quả hợp lệ!")
        return []
    
    results.sort()  # Sắp xếp theo distance tăng dần

    # Lọc trùng lặp dựa trên vector đặc trưng
    unique_features = []
    unique_results = []
    for distance, filename, row in results:
        vec = np.array(row[1:], dtype=np.float32)
        is_duplicate = False
        for uvec in unique_features:
            if np.array_equal(vec, uvec):
                is_duplicate = True
                break
        if not is_duplicate:
            unique_features.append(vec)
            unique_results.append((distance, filename, row))

    top_k = unique_results[:k]
    for distance, filename, _ in top_k:
        print(f"🎯 {filename} | Khoảng cách: {distance:.4f}")
    
    return [(filename, distance) for distance, filename, _ in top_k]