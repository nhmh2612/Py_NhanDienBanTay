import pickle
import cv2
import mediapipe as mp
import numpy as np

model_dict = pickle.load(open('./model.p', 'rb'))
model = model_dict['model']

cap = cv2.VideoCapture(0)  # Thử sử dụng camera mặc định, nếu không thành công thì có thể thử các chỉ số khác

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

hands = mp_hands.Hands(static_image_mode=True, min_detection_confidence=0.3)

labels_dict = {0: '1', 1: '2', 2: '3'}

while True:
    data_aux = []
    x_ = []
    y_ = []

    ret, frame = cap.read()  # Đọc khung hình từ camera

    if not ret:  # Kiểm tra nếu không đọc được khung hình
        print("Không thể đọc khung hình từ camera.")
        break  # Thoát khỏi vòng lặp nếu không thành công

    H, W, _ = frame.shape  # Lấy chiều cao, chiều rộng

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Chuyển đổi màu sắc

    results = hands.process(frame_rgb)  # Xử lý ảnh để tìm bàn tay
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(
                frame,  # Hình ảnh để vẽ
                hand_landmarks,  # Đầu ra của mô hình
                mp_hands.HAND_CONNECTIONS,  # Kết nối bàn tay
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing_styles.get_default_hand_connections_style())

        for hand_landmarks in results.multi_hand_landmarks:
            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y

                x_.append(x)
                y_.append(y)

            for i in range(len(hand_landmarks.landmark)):
                x = hand_landmarks.landmark[i].x
                y = hand_landmarks.landmark[i].y
                data_aux.append(x - min(x_))
                data_aux.append(y - min(y_))

        x1 = int(min(x_) * W) - 10
        y1 = int(min(y_) * H) - 10

        x2 = int(max(x_) * W) - 10
        y2 = int(max(y_) * H) - 10

        prediction = model.predict([np.asarray(data_aux)])  # Dự đoán ký tự

        predicted_character = labels_dict[int(prediction[0])]

        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 0), 4)  # Vẽ hình chữ nhật xung quanh bàn tay
        cv2.putText(frame, predicted_character, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 0, 0), 3,
                    cv2.LINE_AA)  # Hiển thị ký tự dự đoán

    cv2.imshow('frame', frame)  # Hiển thị khung hình
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Nhấn 'q' để thoát
        break

cap.release()  # Giải phóng camera
cv2.destroyAllWindows()  # Đóng tất cả các cửa sổ
