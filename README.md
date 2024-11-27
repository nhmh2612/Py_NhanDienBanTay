# Hệ thống nhận diện ngôn ngữ ký hiệu và chuyển đổi thành văn bản

Dự án này cung cấp một hệ thống nhận diện ngôn ngữ ký hiệu thông qua camera hoặc video, sử dụng thư viện Mediapipe và mô hình máy học. Hệ thống bao gồm các chức năng thu thập dữ liệu, tạo tập dữ liệu, huấn luyện mô hình và giao diện người dùng để sử dụng webcam hoặc tệp video nhằm nhận diện ký hiệu tay và chuyển đổi thành văn bản.

## Cấu trúc dự án

### 1. `collect_letters.py`
- **Chức năng**: Thu thập dữ liệu hình ảnh từ webcam cho các ký hiệu tay.
- Tạo thư mục riêng biệt cho từng ký hiệu (ví dụ: A, B, C...).
- Lưu hình ảnh vào thư mục `./data`.

### 2. `create_dataset.py`
- **Chức năng**: Xử lý các hình ảnh thu thập được để tạo tập dữ liệu.
- Sử dụng Mediapipe để trích xuất các điểm đặc trưng của tay.
- Chuẩn hóa và lưu trữ dữ liệu vào tệp `data.pickle`.

### 3. `train_classifier.py`
- **Chức năng**: Huấn luyện mô hình máy học.
- Sử dụng mô hình `RandomForestClassifier` để phân loại ký hiệu tay.
- Lưu mô hình đã huấn luyện vào tệp `model.p`.

### 4. Giao diện ứng dụng
- **Mô tả**: Ứng dụng sử dụng Tkinter để nhận diện ngôn ngữ ký hiệu và chuyển đổi thành văn bản.
- **Chức năng**:
  - Dùng webcam để nhận diện ký hiệu tay trong thời gian thực.
  - Chọn tệp video để phân tích và nhận diện ký hiệu.
  - Kết hợp chức năng chuyển văn bản thành giọng nói (text-to-speech).

## Cách sử dụng

### 1. Cài đặt môi trường
Cài đặt các thư viện cần thiết:
```bash
pip install opencv-python mediapipe numpy scikit-learn pyttsx3 pillow
```
### 2. Thu thập dữ liệu
Chạy collect_letters.py để thu thập dữ liệu hình ảnh cho từng ký hiệu tay:
```bash
python collect_letters.py
```
### 3. Tạo tập dữ liệu
Chạy create_dataset.py để xử lý dữ liệu đã thu thập:
```bash
python create_dataset.py
```
### 4. Huấn luyện mô hình
Chạy train_classifier.py để huấn luyện mô hình:
```bash
python train_classifier.py
```
### 5. Chạy giao diện
Khởi chạy ứng dụng giao diện để nhận diện ký hiệu:
```bash
python app.py
```

## Hướng dẫn sử dụng ứng dụng

- **Sử dụng Webcam**: Nhấn nút "Sử dụng Webcam" để nhận diện ký hiệu trong thời gian thực.
- **Chọn Video**: Nhấn nút "Chọn Video" để nhận diện ký hiệu từ tệp video.
- **Đọc Văn Bản**: Nhấn nút "Đọc Văn Bản" để chuyển đổi văn bản đã dự đoán thành giọng nói.

