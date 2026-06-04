import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm
import statsmodels.formula.api as smf
import os

# Thiết lập thư mục làm việc và đường dẫn file dữ liệu
base_dir = os.path.dirname(__file__)
csv_path = os.path.join(base_dir, 'rent_data.csv')

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"Không tìm thấy file dữ liệu tại {csv_path}. Vui lòng chạy data_generator.py trước.")

# 1. Đọc dữ liệu
df = pd.read_csv(csv_path)

# Thiết lập font chữ hỗ trợ hiển thị tiếng Việt trên biểu đồ (nếu có)
plt.rcParams['figure.figsize'] = [10, 6]
plt.rcParams['font.size'] = 12

# 2. Thống kê mô tả
desc_stats = df[['Distance_km', 'RentPrice_M_VND']].describe()
print("="*50)
print("THỐNG KÊ MÔ TẢ DỮ LIỆU:")
print("="*50)
print(desc_stats)
print("\n")

# 3. Vẽ biểu đồ phân tán (Scatter Plot) với đường hồi quy
plt.figure(figsize=(8, 6))
sns.regplot(x='Distance_km', y='RentPrice_M_VND', data=df, 
            scatter_kws={'color': '#1f77b4', 'alpha': 0.7, 's': 50}, 
            line_kws={'color': '#d62728', 'linewidth': 2})
plt.title('Biểu đồ phân tán giữa Khoảng cách và Giá thuê trọ')
plt.xlabel('Khoảng cách tới trường (km)')
plt.ylabel('Giá thuê trọ (triệu VNĐ/tháng)')
plt.grid(True, linestyle='--', alpha=0.5)
scatter_img_path = os.path.join(base_dir, 'scatter_plot.png')
plt.savefig(scatter_img_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Đã lưu biểu đồ phân tán tại: {scatter_img_path}")

# 4. Xây dựng mô hình hồi quy tuyến tính đơn biến (OLS)
# Công thức: RentPrice_M_VND ~ Distance_km
model = smf.ols('RentPrice_M_VND ~ Distance_km', data=df).fit()

print("="*50)
print("TÓM TẮT MÔ HÌNH HỒI QUY (REGRESSION SUMMARY):")
print("="*50)
print(model.summary())
print("\n")

# 5. Phân tích sai số (Model Diagnostics - Residual Analysis)
# Biểu đồ Q-Q plot của sai số để kiểm tra giả định phân phối chuẩn (Normality)
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Q-Q plot
sm.qqplot(model.resid, line='45', fit=True, ax=ax[0])
ax[0].set_title('Đồ thị Q-Q Plot của Sai số (Residuals)')
ax[0].grid(True, linestyle='--', alpha=0.5)

# Đồ thị Residuals vs Fitted values để kiểm tra phương sai đồng đều (Homoscedasticity)
ax[1].scatter(model.fittedvalues, model.resid, color='#2ca02c', alpha=0.7, edgecolors='none', s=50)
ax[1].axhline(y=0, color='red', linestyle='--', linewidth=1.5)
ax[1].set_title('Đồ thị Sai số so với Giá trị Dự báo (Residuals vs Fitted)')
ax[1].set_xlabel('Giá trị dự báo (Fitted values)')
ax[1].set_ylabel('Sai số (Residuals)')
ax[1].grid(True, linestyle='--', alpha=0.5)

residual_img_path = os.path.join(base_dir, 'residual_analysis.png')
plt.savefig(residual_img_path, dpi=300, bbox_inches='tight')
plt.close()
print(f"Đã lưu biểu đồ phân tích sai số tại: {residual_img_path}")

# 6. Dự báo thử nghiệm
# Dự báo cho khoảng cách là 2.0 km
test_dist = 2.0
pred_price = model.predict(pd.DataFrame({'Distance_km': [test_dist]}))[0]

print("="*50)
print("DỰ BÁO VÀ PHÂN TÍCH HỆ SỐ:")
print("="*50)
beta_0 = model.params['Intercept']
beta_1 = model.params['Distance_km']
p_val_beta1 = model.pvalues['Distance_km']
r_sq = model.rsquared

print(f"Hệ số tự do (Intercept) beta_0 = {beta_0:.4f}")
print(f"Hệ số góc (Slope) beta_1 = {beta_1:.4f}")
print(f"Hệ số xác định R-squared = {r_sq:.4f}")
print(f"P-value của hệ số góc = {p_val_beta1:.4e}")
print("-" * 50)
print(f"Phương trình hồi quy tuyến tính tìm được là:")
print(f"  Giá trọ = {beta_0:.2f} + ({beta_1:.2f}) * Khoảng cách")
print("-" * 50)
print(f"Ý nghĩa thực tế:")
print(f"- Giá trọ lý thuyết tại sát trường (0 km) là: {beta_0:.2f} triệu VNĐ.")
print(f"- Khi khoảng cách tăng thêm 1 km, giá trọ giảm trung bình: {abs(beta_1):.2f} triệu VNĐ.")
print(f"- Ví dụ: Một phòng trọ cách trường {test_dist} km dự báo có giá thuê là: {pred_price:.2f} triệu VNĐ/tháng.")
print("="*50)

# 7. Dự báo tương tác từ bàn phím (Interactive Input)
print("\n" + "="*50)
print("CHƯƠNG TRÌNH DỰ BÁO GIÁ TRỌ TƯƠNG TÁC:")
print("="*50)
print("Nhập khoảng cách (km) để dự báo giá phòng trọ.")
print("Gõ 'exit' hoặc 'q' để thoát.")

while True:
    try:
        user_input = input("\nNhập khoảng cách từ trọ đến trường (km): ").strip()
        if user_input.lower() in ['exit', 'q']:
            print("Cảm ơn bạn đã sử dụng chương trình!")
            break
        
        dist = float(user_input)
        if dist < 0:
            print("Khoảng cách không thể là số âm. Vui lòng nhập lại!")
            continue
            
        # Tính toán dự báo bằng mô hình hồi quy
        predicted = model.predict(pd.DataFrame({'Distance_km': [dist]}))[0]
        # Giới hạn giá trọ tối thiểu là 0 (nếu khoảng cách nhập vào quá lớn)
        predicted = max(predicted, 0.0)
        
        print(f"--> Giá thuê trọ dự báo: {predicted:.2f} triệu VNĐ/tháng")
        print(f"    (Công thức tính: {beta_0:.2f} + ({beta_1:.2f}) * {dist})")
    except ValueError:
        print("Vui lòng nhập một số hợp lệ (ví dụ: 1.5, 2.7).")

