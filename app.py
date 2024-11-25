import cv2
import mediapipe as mp
import pickle
import numpy as np
import time
import pyttsx3
from threading import Thread
from tkinter import Tk, Label, Button, filedialog, StringVar, Toplevel, messagebox
from PIL import Image, ImageTk

# Tải mô hình đã lưu
model_dict = pickle.load(open('model/model.p', 'rb'))
model = model_dict['model']

# Initialize Mediapipe Hand solution
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

# Khởi tạo pyttsx3
engine = pyttsx3.init()
speech_in_progress = False

# Hàm đọc văn bản
def speak_text(text):
    global speech_in_progress
    if speech_in_progress:
        messagebox.showinfo("Thông báo", "Đang đọc văn bản. Vui lòng chờ!")
        return

    def run_speech():
        global speech_in_progress
        try:
            speech_in_progress = True
            engine.say(text)
            engine.runAndWait()
        finally:
            speech_in_progress = False

    Thread(target=run_speech, daemon=True).start()

# Hàm xử lý video từ webcam hoặc tệp
def process_video(use_webcam=True, video_path=None):
    global predicted_text
    if use_webcam:
        vid = cv2.VideoCapture(0)  # Mở webcam
    else:
        vid = cv2.VideoCapture(video_path)  # Mở tệp video

    if not vid.isOpened():
        messagebox.showerror("Lỗi", "Không thể mở video.")
        return

    predicted_text = ""
    countdown_started = False
    countdown_time = 3
    countdown_start_time = 0

    def update_frame():
        global predicted_text
        nonlocal countdown_started, countdown_start_time
        ret, img = vid.read()
        if not ret:
            vid.release()
            return

        img = cv2.flip(img, 1)
        frame_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        predicted_character = "Không phát hiện tay"
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                x_, y_, data_aux = [], [], []

                for lm in hand_landmarks.landmark:
                    x_.append(lm.x)
                    y_.append(lm.y)
                for i in range(len(hand_landmarks.landmark)):
                    data_aux.append(x_[i] - min(x_))
                    data_aux.append(y_[i] - min(y_))

                try:
                    prediction = model.predict([np.asarray(data_aux)])
                    predicted_character = prediction[0]
                except Exception:
                    predicted_character = "Lỗi Dự Đoán"

                if not countdown_started:
                    countdown_started = True
                    countdown_start_time = time.time()

        if countdown_started:
            elapsed_time = time.time() - countdown_start_time
            if elapsed_time < countdown_time:
                # Hiển thị đếm ngược
                countdown_display = countdown_time - int(elapsed_time)
                cv2.putText(img, f"Time: {countdown_display}", (50, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            else:
                # Kết thúc đếm ngược
                if predicted_character == "1":
                    predicted_text += " "
                elif predicted_character == "2":
                    predicted_text = ""
                elif predicted_character not in ["Không phát hiện tay", "Lỗi Dự Đoán"]:
                    predicted_text += predicted_character
                countdown_started = False

        # Hiển thị kết quả trên giao diện
        predicted_char_label.config(text=f"Ký tự dự đoán: {predicted_character}")
        predicted_text_label.config(text=f"Văn bản dự đoán: {predicted_text}")

        # Cập nhật khung hình
        frame = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        frame = cv2.resize(frame, (640, 480))
        img_tk = ImageTk.PhotoImage(image=Image.fromarray(frame))
        video_label.img_tk = img_tk
        video_label.configure(image=img_tk)
        root.after(10, update_frame)

    update_frame()

# Hàm chọn tệp video
def select_video():
    file_path = filedialog.askopenfilename(filetypes=[("Video Files", "*.mp4 *.mov *.avi *.asf *.m4v")])
    if file_path:
        process_video(use_webcam=False, video_path=file_path)

# Khởi tạo giao diện Tkinter
root = Tk()
root.title("Chuyển Ngôn Ngữ Ký Hiệu Thành Văn Bản")

# Cửa sổ chính
video_label = Label(root)
video_label.pack()

predicted_char_label = Label(root, text="Ký tự dự đoán: ", font=("Arial", 16))
predicted_char_label.pack()

predicted_text_label = Label(root, text="Văn bản dự đoán: ", font=("Arial", 16))
predicted_text_label.pack()

# Nút chọn video
select_button = Button(root, text="Chọn Video", command=select_video, font=("Arial", 14))
select_button.pack()

# Nút sử dụng webcam
webcam_button = Button(root, text="Sử dụng Webcam", command=lambda: process_video(use_webcam=True), font=("Arial", 14))
webcam_button.pack()

# Nút đọc văn bản
read_button = Button(root, text="Đọc Văn Bản", command=lambda: speak_text(predicted_text), font=("Arial", 14))
read_button.pack()

# Biến lưu trữ văn bản dự đoán
predicted_text = ""

# Chạy ứng dụng
root.mainloop()
