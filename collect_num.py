import os
import cv2


DATA_DIR = './data'
# Kiểm tra xem thư mục đã tồn tại chưa, nếu chưa thì tạo mới
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

number_of_classes = 3  # Số lượng lớp (hoặc loại) dữ liệu để thu thập
dataset_size = 100  # Số lượng ảnh cho mỗi lớp

# Mở camera (0 là camera mặc định)
cap = cv2.VideoCapture(0)

# Vòng lặp qua từng lớp
for j in range(number_of_classes):
    # Tạo thư mục cho lớp nếu chưa tồn tại
    if not os.path.exists(os.path.join(DATA_DIR, str(j))):
        os.makedirs(os.path.join(DATA_DIR, str(j)))

    print('Collecting data for class {}'.format(j))  # Thông báo đang thu thập dữ liệu cho lớp hiện tại

    done = False  # Biến đánh dấu trạng thái
    while True:
        # Đọc khung hình từ camera
        ret, frame = cap.read()
        # Hiển thị thông báo trên khung hình
        cv2.putText(frame, 'Ready? Press "Q" ! :)', (100, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 0), 3, cv2.LINE_AA)
        cv2.imshow('frame', frame)  #

        # Kiểm tra xem người dùng có nhấn phím 'Q' không để bắt đầu thu thập ảnh
        if cv2.waitKey(25) == ord('q'):
            break  # Thoát vòng lặp nếu nhấn 'Q'

    counter = 0  # Biến đếm số lượng ảnh đã thu thập
    # Vòng lặp thu thập ảnh cho mỗi lớp
    while counter < dataset_size:
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        cv2.waitKey(25)  # Đợi 25ms để người dùng có thời gian xem khung hình

        # Lưu khung hình vào thư mục tương ứng với tên ảnh là số thứ tự
        cv2.imwrite(os.path.join(DATA_DIR, str(j), '{}.jpg'.format(counter)), frame)

        counter += 1

cap.release()
cv2.destroyAllWindows()
