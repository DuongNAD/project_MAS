import pandas as pd
import numpy as np
import os

# Thiết lập seed để kết quả sinh ngẫu nhiên đồng nhất ở mọi lần chạy
np.random.seed(42)

# Số lượng mẫu khảo sát
n_samples = 50

# 1. Sinh ngẫu nhiên khoảng cách (Distance) từ trọ tới trường (đơn vị: km)
# Dao động từ 0.2 km đến 5.0 km
distances = np.round(np.random.uniform(0.2, 5.0, n_samples), 2)

# 2. Sinh giá thuê trọ (RentPrice) dựa trên khoảng cách (đơn vị: triệu VNĐ/tháng)
# Giả sử giá trọ trung bình sát trường (distance = 0) là 4.5 triệu.
# Cứ xa trường thêm 1km thì giá giảm trung bình khoảng 0.5 triệu.
# Sai số ngẫu nhiên (noise) tuân theo phân phối chuẩn với độ lệch chuẩn là 0.3 triệu VNĐ.
noise = np.random.normal(0, 0.3, n_samples)
rent_prices = 4.5 - 0.5 * distances + noise

# Làm tròn giá thuê đến 1 chữ số thập phân (ví dụ 3.2 triệu, 2.5 triệu)
rent_prices = np.round(rent_prices, 1)

# Giới hạn giá trọ tối thiểu là 1.2 triệu (không thể âm hoặc quá rẻ)
rent_prices = np.clip(rent_prices, 1.2, 5.5)

# 3. Tạo DataFrame và lưu thành file CSV
df = pd.DataFrame({
    'No': range(1, n_samples + 1),
    'Distance_km': distances,
    'RentPrice_M_VND': rent_prices
})

# Đảm bảo thư mục đích tồn tại
os.makedirs(os.path.dirname(__file__), exist_ok=True)

csv_path = os.path.join(os.path.dirname(__file__), 'rent_data.csv')
df.to_csv(csv_path, index=False)

print(f"Đã sinh {n_samples} mẫu dữ liệu trọ thành công tại: {csv_path}")
print("5 dòng dữ liệu đầu tiên:")
print(df.head())
