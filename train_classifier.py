import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# Tải dữ liệu từ tệp pickle
data_dict = pickle.load(open('./data.pickle', 'rb'))

data = np.asarray(data_dict['data'])
labels = np.asarray(data_dict['labels'])

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
x_train, x_test, y_train, y_test = train_test_split(data, labels, test_size=0.2, shuffle=True, stratify=labels)

# Khởi tạo mô hình Random Forest
model = RandomForestClassifier()

# Huấn luyện mô hình
model.fit(x_train, y_train)

# Dự đoán nhãn trên tập kiểm tra
y_predict = model.predict(x_test)

# Tính toán độ chính xác
accuracy = accuracy_score(y_test, y_predict)
print('{}% of samples were classified correctly!'.format(accuracy * 100))

# In báo cáo phân loại
report = classification_report(y_test, y_predict)
print("\nClassification Report:\n", report)

# Lưu mô hình vào tệp
with open('model.p', 'wb') as f:
    pickle.dump({'model': model}, f)
