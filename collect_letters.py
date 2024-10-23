import os
import cv2

# Thư mục lưu dữ liệu
DATA_DIR = './data'
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Danh sách các chữ cái cần thu thập dữ liệu
letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
dataset_size = 100  # Số lượng ảnh cho mỗi chữ cái

cap = cv2.VideoCapture(0)  # Sử dụng webcam mặc định

# Duyệt qua từng chữ cái trong danh sách
for letter in letters:
    letter_dir = os.path.join(DATA_DIR, letter)

    # Tạo thư mục cho mỗi chữ cái nếu chưa tồn tại
    if not os.path.exists(letter_dir):
        os.makedirs(letter_dir)

    print(f'Collecting data for letter: {letter}')

    # Bắt đầu chế độ chờ để sẵn sàng thu thập dữ liệu cho chữ cái
    while True:
        ret, frame = cap.read()
        cv2.putText(frame, f'Ready to collect "{letter}"? Press "Q" to start!', (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('frame', frame)

        if cv2.waitKey(25) == ord('q'):
            break

    # Bắt đầu thu thập ảnh cho chữ cái
    counter = 0
    while counter < dataset_size:
        ret, frame = cap.read()

        # Hiển thị ảnh thu được và nhắc nhở số lượng ảnh đã thu thập
        cv2.putText(frame, f'Collecting "{letter}" - Image {counter + 1}/{dataset_size}',
                    (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow('frame', frame)

        # Lưu ảnh vào thư mục tương ứng
        cv2.imwrite(os.path.join(letter_dir, f'{counter}.jpg'), frame)

        # Chờ trước khi thu thập ảnh tiếp theo
        cv2.waitKey(100)  # Đợi 100ms (điều chỉnh thời gian nếu cần)

        counter += 1

cap.release()
cv2.destroyAllWindows()

print("Data collection complete.")
