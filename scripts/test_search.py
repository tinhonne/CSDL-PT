import sys
import os

# In sys.path để debug
print("sys.path:", sys.path)

# Thêm thư mục gốc vào sys.path nếu cần
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from utils.similarity import find_similar
except Exception as e:
    print("❌ Lỗi khi nhập khẩu utils.similarity:", e)
    sys.exit(1)

print("✅ Đang chạy test_search.py...")

if len(sys.argv) != 2:
    print("Cách dùng: python -m scripts.test_search <đường_dẫn_file.wav>")
    sys.exit(1)

file_path = sys.argv[1]
print("🔎 Đang tìm file giống nhất với:", file_path)

try:
    results = find_similar(file_path)
    print("🎯 Top 3 kết quả giống nhất:")
    for i, f in enumerate(results, 1):
        print(f"{i}. {f}")
except Exception as e:
    print("❌ Lỗi khi tìm kiếm:", e)