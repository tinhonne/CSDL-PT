# Project Search Sound Animal

## Mô tả
Hệ thống tìm kiếm tiếng kêu động vật dựa trên đặc trưng âm thanh:
- **Đầu vào:** 1 file âm thanh `.wav` bất kỳ về một loài động vật.
- **Đầu ra:** 3 file âm thanh giống nhất trong database, kèm theo % độ giống và khoảng cách.

## Cấu trúc thư mục

```
audio_raw/           # Âm thanh gốc (phân theo loài)
audio_processed/     # Âm thanh đã chuẩn hóa (wav, 22050Hz, mono)
database/            # Chứa file animalsounds.db
gui/                 # Giao diện Tkinter
scripts/             # Script chuẩn hóa audio, tạo database, trích xuất đặc trưng
utils/               # Các hàm tiện ích: trích xuất đặc trưng, tìm kiếm, database
requirements.txt     # Danh sách thư viện cần cài
README.md            # File hướng dẫn này
```

## Cài đặt thư viện

```bash
pip install -r requirements.txt
```

**Nếu dùng pydub:**  
- Cần cài ffmpeg cho hệ điều hành:
    - Windows: tải tại [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) và thêm vào PATH.

## Hướng dẫn sử dụng

### 1. Chuẩn hóa audio

Chạy script để chuyển file âm thanh về chuẩn wav, mono, 22050Hz:

```bash
python -m scripts.normalize_audio
```

### 2. Tạo database và trích xuất đặc trưng

Chạy script tạo database:

```bash
python -m scripts.init_db
```

Sau đó, trích xuất đặc trưng và lưu vào database:

```bash
python -m scripts.extract_and_insert
```

### 3. Chạy giao diện tìm kiếm

```bash
python -m gui.main
```

- Chọn file `.wav` để tìm kiếm.
- Xem top 3 kết quả giống nhất, có thể nghe thử từng file.
- Xem bảng so sánh đặc trưng giữa file input và các file kết quả.

## Ghi chú

- Nếu gặp lỗi khi phát âm thanh, hãy kiểm tra lại định dạng file wav và cài đặt pygame.
- Nếu gặp lỗi thiếu thư viện, hãy kiểm tra lại `requirements.txt` và cài đặt đúng môi trường Python.
- Nếu file âm thanh đầu vào không chuẩn (không phải wav, không đúng sample rate), hãy chuẩn hóa lại bằng script.

---

**Chúc bạn thành công!**