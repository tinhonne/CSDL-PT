from utils.db_utils import init_db
import os

print("🛠 Bắt đầu tạo CSDL...")
init_db()

# Kiểm tra file đã tạo chưa
db_path = 'database/animalsounds.db'
if os.path.exists(db_path):
    print("✅ Tạo thành công:", db_path)
else:
    print("❌ Không tạo được database.")
