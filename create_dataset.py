import os
import pickle
import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

DATA_DIR = './data'  # Đường dẫn chứa dữ liệu

data = []
labels = []

# Kiểm tra và lưu lại các đặc trưng của bàn tay với chiều dài đồng nhất
for dir_ in os.listdir(DATA_DIR):
    dir_path = os.path.join(DATA_DIR, dir_)
    if os.path.isdir(dir_path):
        for img_path in os.listdir(dir_path):
            img = cv2.imread(os.path.join(dir_path, img_path))

            # Kiểm tra nếu ảnh được đọc thành công
            if img is None:
                continue

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = hands.process(img_rgb)

            if results.multi_hand_landmarks:
                data_aux = []
                x_ = []
                y_ = []

                for hand_landmarks in results.multi_hand_landmarks:
                    for i in range(len(hand_landmarks.landmark)):
                        x = hand_landmarks.landmark[i].x
                        y = hand_landmarks.landmark[i].y
                        x_.append(x)
                        y_.append(y)

                    # Chuẩn hóa đặc trưng của từng điểm
                    for i in range(len(hand_landmarks.landmark)):
                        data_aux.append(hand_landmarks.landmark[i].x - min(x_))
                        data_aux.append(hand_landmarks.landmark[i].y - min(y_))

                # Nếu số lượng đặc trưng là đủ, mới thêm vào danh sách
                if len(data_aux) == 42:  
                    data.append(data_aux)
                    labels.append(dir_)

# Lưu dữ liệu vào tệp pickle
with open('data.pickle', 'wb') as f:
    pickle.dump({'data': data, 'labels': labels}, f)

print("Data saved successfully!")
