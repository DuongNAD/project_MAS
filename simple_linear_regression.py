import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# GHI CHÚ: Gia_Thue_Trieu chỉ là tiền phòng (cập nhật theo mặt bằng giá thực tế
# quanh FPTU, có phân biệt Loai_Phong: chung cư mini/studio đầy đủ nội thất giá
# cao hơn phòng trọ cơ bản). Chưa bao gồm điện (~3.500-4.000đ/số), nước, mạng,
# gửi xe, vệ sinh chung - cần cộng thêm nếu ước tính tổng chi phí sinh hoạt.

# GHI CHÚ: Cột Nganh đã ghi tên đầy đủ; 2 ký tự đầu của Ma_SV là mã ngành tương ứng:
#   HE = Cong nghe thong tin
#   HS = An toan thong tin
#   HA = Quan tri kinh doanh
#   HC = Thiet ke my thuat so
# 4 số cuối của Ma_SV là số thứ tự ngẫu nhiên trong từng nhóm (ngành, khóa).

# GHI CHÚ: Các dòng có Khu_Vuc = "Dom A/B/C/D" là ký túc xá (Dom), không phải
# phòng trọ tư nhân. Giá thuê ở đây là giá CẢ PHÒNG/tháng theo khảo sát thực tế:
# phòng 4 người ~ 1.1 triệu/tháng, phòng 6 người ~ 0.8 triệu/tháng. Vì giá KTX do
# nhà trường quy định cố định (không tăng giảm theo khoảng cách tới trường như
# phòng trọ ngoài), các dòng này là ngoại lệ so với xu hướng chung của mô hình
# hồi quy khoảng cách - giá thuê, dù nằm rất gần trường (Khoang_Cach_km ~0.1-0.7).

# Đọc dữ liệu từ file CSV
df = pd.read_csv('data.csv')

# Chọn biến độc lập (X) và biến phụ thuộc (y)
# Trong mô hình đơn tuyến tính, ta chọn 1 biến dự báo, ở đây là Khoảng cách (km) để dự đoán Giá thuê (Triệu)
X = df[['Khoang_Cach_km']]
y = df['Gia_Thue_Trieu']

# Khởi tạo mô hình hồi quy tuyến tính
model = LinearRegression()

# Huấn luyện mô hình
model.fit(X, y)

# Dự đoán giá trị
y_pred = model.predict(X)

# In các hệ số của mô hình
print(f"Hệ số góc (Coefficient - Slope): {model.coef_[0]:.4f}")
print(f"Hệ số chặn (Intercept): {model.intercept_:.4f}")

# Đánh giá mô hình
mse = mean_squared_error(y, y_pred)
r2 = r2_score(y, y_pred)
print(f"Mean Squared Error (MSE): {mse:.4f}")
print(f"R-squared (R2): {r2:.4f}")

# Trực quan hóa dữ liệu và đường hồi quy
plt.figure(figsize=(8, 5))
plt.scatter(X, y, color='blue', label='Dữ liệu thực tế')
plt.plot(X, y_pred, color='red', linewidth=2, label='Đường hồi quy')
plt.title('Hồi quy đơn tuyến tính: Khoảng cách vs Giá thuê')
plt.xlabel('Khoảng cách (km)')
plt.ylabel('Giá thuê (Triệu)')
plt.legend()
plt.grid(True)
plt.savefig('simple_linear_regression.png')
print("Đã lưu biểu đồ vào file 'simple_linear_regression.png'")
