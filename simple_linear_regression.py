import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

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
