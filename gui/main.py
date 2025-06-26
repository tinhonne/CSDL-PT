import tkinter as tk
from tkinter import filedialog, messagebox
from utils.similarity import find_similar
from utils.feature_extractor import extract_features
import os
import pygame

results_cache = []

# Ẩm thanh
def play_audio(filepath):
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.play()
    except Exception as e:
        messagebox.showerror("Lỗi phát âm thanh", f"{e}\nFile: {filepath}")

# Chọn file input
def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("WAV files", "*.wav")])
    if file_path:
        entry.delete(0, tk.END)
        entry.insert(0, file_path)

# Phát file âm thanh đã chọn trong list
def play_selected():
    sel = output.curselection()
    if not sel:
        messagebox.showinfo("Chọn file", "Hãy chọn 1 kế quả để nghe thử!")
        return
    idx = sel[0]
    if idx < len(results_cache):
        fname = results_cache[idx][0]
        file_path = os.path.join("audio_processed", os.path.basename(fname))
        if not os.path.isfile(file_path):
            messagebox.showerror("Lỗi", f"Không tìm thấy file: {file_path}")
            return
        play_audio(file_path)

# Phát file input
def play_input_audio():
    file_path = entry.get()
    if not file_path or not os.path.isfile(file_path):
        messagebox.showinfo("Chọn file", "Vui lòng chọn file âm thanh hợp lệ!")
        return
    play_audio(file_path)

# Tìm kiếm file giống nhất
def search():
    file_path = entry.get()
    if not file_path.endswith(".wav"):
        messagebox.showerror("Lỗi", "Vui lòng chọn file .wav hợp lệ!")
        return

    try:
        global results_cache
        results = find_similar(file_path, k=10)  # Trả về (filename, percent_str, sim)
        results_cache = results
        output.delete(0, tk.END)

        if not results:
            messagebox.showinfo("Thông báo", "Không tìm thấy kế quả hợp lệ!")
            return

        for i, (fname, percent_str, sim_val) in enumerate(results[:3], 1):
            output.insert(
                tk.END,
                f"{i}. {os.path.basename(fname)} (Độ giống: {percent_str})"
            )

    except FileNotFoundError as e:
        messagebox.showerror("Lỗi cơ sở dữ liệu", str(e))
    except Exception as e:
        messagebox.showerror("Lỗi tìm kiếm", str(e))

# Hiển thị bảng đặc trưng
def show_input_features():
    file_path = entry.get()
    if not file_path or not os.path.isfile(file_path):
        messagebox.showinfo("Chọn file", "Vui lòng chọn file âm thanh hợp lệ!")
        return
    try:
        features_input = extract_features(file_path)
        features_results = []
        file_names = []
        for i in range(3):
            if i < len(results_cache):
                fname = os.path.basename(results_cache[i][0])
                file_names.append(fname)
                features_results.append(
                    extract_features(os.path.join("audio_processed", fname))
                )
            else:
                file_names.append(f"File {i+1}")
                features_results.append([""] * 25)

        feature_names = [
            "ZCR", "RMS", "Centroid", "Bandwidth", "Rolloff"
        ] + [f"MFCC{i}" for i in range(1, 21)]

        top = tk.Toplevel(root)
        top.title("Bảng đặc trưng so sánh")
        text = tk.Text(top, width=80, height=30, font=("Consolas", 11))
        text.pack(padx=10, pady=10)

        header = f"{'\u0110ặc trưng':<15} {'Input':>15} {file_names[0]:>15} {file_names[1]:>15} {file_names[2]:>15}\n"
        lines = [header]
        for idx, name in enumerate(feature_names):
            val_input = f"{features_input[idx]:.4f}" if features_input else ""
            val1 = f"{features_results[0][idx]:.4f}" if features_results[0][idx] != "" else ""
            val2 = f"{features_results[1][idx]:.4f}" if features_results[1][idx] != "" else ""
            val3 = f"{features_results[2][idx]:.4f}" if features_results[2][idx] != "" else ""
            lines.append(f"{name:<15} {val_input:>15} {val1:>15} {val2:>15} {val3:>15}")

        text.insert(tk.END, "\n".join(lines))
        text.config(state=tk.DISABLED)
    except Exception as e:
        messagebox.showerror("Lỗi trích xuất đặc trưng", str(e))

# Danh sách top 10 khoảng cách
def show_distance_list():
    if not results_cache:
        messagebox.showinfo("Thông báo", "Vui lòng thực hiện tìm kiếm trước!")
        return

    top = tk.Toplevel(root)
    top.title("Danh sách 10 file có khoảng cách nhỏ nhất")
    top.geometry("600x400")

    text = tk.Text(top, width=80, height=20, font=("Consolas", 11))
    text.pack(padx=10, pady=10)

    header = f"{'STT':<5} {'Tên file':<40} {'Khoảng cách':>15}\n"
    lines = [header, "-" * 60 + "\n"]

    for i, (fname, percent_str, sim_val) in enumerate(results_cache[:10], 1):
        distance = 1 - sim_val
        lines.append(f"{i:<5} {os.path.basename(fname):<40} {distance:>15.4f}")

    text.insert(tk.END, "\n".join(lines))
    text.config(state=tk.DISABLED)

# Giao diện chính
root = tk.Tk()
root.title("Tìm kiếm tiếng động vật")
root.geometry("1280x720")

tk.Label(root, text="\U0001f50a Chọn file âm thanh:", font=("Arial", 14)).pack(pady=10)
frame = tk.Frame(root)
frame.pack()

entry = tk.Entry(frame, width=60, font=("Arial", 12))
entry.pack(side=tk.LEFT, padx=5)
tk.Button(frame, text="Chọn", command=select_file, font=("Arial", 12)).pack(side=tk.LEFT)

tk.Button(root, text="\U0001f50d Tìm kiếm", command=search, font=("Arial", 12)).pack(pady=10)

tk.Label(root, text="\U0001f3af Top 3 kế quả giống nhất:", font=("Arial", 14)).pack()
output = tk.Listbox(root, width=80, height=7, font=("Arial", 12))
output.pack(pady=5)

tk.Button(root, text="▶ Nghe thử", command=play_selected, font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="▶ Nghe thử file input", command=play_input_audio, font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Xem đặc trưng", command=show_input_features, font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Xem danh sách khoảng cách", command=show_distance_list, font=("Arial", 12)).pack(pady=5)
tk.Button(root, text="Thoát", command=root.quit, font=("Arial", 12)).pack(pady=5)

root.mainloop()
