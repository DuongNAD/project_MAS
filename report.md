# BÁO CÁO PHÂN TÍCH THỐNG KÊ (MÔN MAS)
## Đề tài: Phân tích mối liên hệ giữa khoảng cách từ phòng trọ tới trường và giá thuê trọ

---

## 1. Giới thiệu đề tài
Trong quá trình học tập tại trường Đại học FPT, việc tìm phòng trọ phù hợp là một trong những mối quan tâm lớn của sinh viên. Có nhiều yếu tố ảnh hưởng đến giá thuê trọ như diện tích, cơ sở vật chất, an ninh, và đặc biệt là vị trí địa lý.
Báo cáo này sử dụng mô hình **Hồi quy tuyến tính đơn biến (Simple Linear Regression)** nhằm định lượng mối liên hệ giữa:
* **Biến độc lập ($X$):** Khoảng cách từ nhà trọ đến trường (km) - `Distance_km`.
* **Biến phụ thuộc ($Y$):** Giá thuê phòng trọ (triệu VNĐ/tháng) - `RentPrice_M_VND`.

Mục tiêu là tìm ra phương trình có dạng:
$$Y = \beta_0 + \beta_1 X + \epsilon$$

---

## 2. Thống kê mô tả dữ liệu
Bộ dữ liệu gồm khảo sát thực tế từ **50 phòng trọ** xung quanh trường. Các chỉ số thống kê mô tả cơ bản của 2 biến như sau:

| Chỉ số | Khoảng cách ($X$ - km) | Giá thuê ($Y$ - triệu VNĐ) |
| :--- | :---: | :---: |
| **Giá trị trung bình (Mean)** | 2.34 km | 3.33 triệu VNĐ |
| **Độ lệch chuẩn (Std Dev)** | 1.39 km | 0.76 triệu VNĐ |
| **Giá trị nhỏ nhất (Min)** | 0.30 km | 1.30 triệu VNĐ |
| **Trung vị (Median)** | 2.29 km | 3.40 triệu VNĐ |
| **Giá trị lớn nhất (Max)** | 4.86 km | 4.80 triệu VNĐ |

*Nhận xét:* Khoảng cách khảo sát trải đều từ sát trường (0.3 km) đến tương đối xa (gần 5 km). Giá trọ trung bình dao động khoảng 3.33 triệu VNĐ/tháng.

---

## 3. Biểu đồ phân tán (Scatter Plot)
Dưới đây là biểu đồ phân tán thể hiện mối tương quan giữa khoảng cách và giá thuê trọ cùng đường thẳng hồi quy tối ưu:

![Biểu đồ phân tán giữa Khoảng cách và Giá thuê trọ](scatter_plot.png)

*Nhìn vào biểu đồ:* Ta thấy một xu hướng tuyến tính đi xuống rất rõ rệt. Khi khoảng cách tới trường càng lớn, giá thuê trọ có xu hướng giảm dần. Mối tương quan này là tương quan nghịch (Negative Correlation).

---

## 4. Kết quả ước lượng mô hình hồi quy
Sau khi khớp mô hình hồi quy tuyến tính bằng phương pháp bình phương tối thiểu (Ordinary Least Squares - OLS), ta thu được bảng kết quả tóm tắt sau:

| Hệ số | Ước lượng (Coef) | Sai số chuẩn (Std Err) | Thống kê t (t-stat) | P-value ($P > \|t\|$) | Khoảng tin cậy 95% |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Hệ số tự do ($\beta_0$)** | 4.5230 | 0.078 | 57.992 | 0.000 | [4.366, 4.680] |
| **Hệ số góc ($\beta_1$)** | -0.5105 | 0.029 | -17.761 | 0.000 | [-0.568, -0.453] |

### Phương trình hồi quy tuyến tính mẫu:
$$\widehat{\text{Giá trọ}} = 4.52 - 0.51 \times \text{Khoảng cách}$$

### Ý nghĩa thực tế của các hệ số:
1. **Hệ số tự do ($\beta_0 = 4.52$):** Về mặt lý thuyết, một phòng trọ nằm ngay sát trường (khoảng cách $\approx 0$ km) và có các điều kiện cơ bản trung bình sẽ có giá thuê ước tính khoảng **4.52 triệu VNĐ/tháng**.
2. **Hệ số góc ($\beta_1 = -0.51$):** Mang giá trị âm, biểu thị mối quan hệ nghịch biến. Khi khoảng cách từ phòng trọ tới trường **tăng thêm 1 km**, giá thuê trọ trung bình sẽ **giảm đi khoảng 0.51 triệu VNĐ/tháng** (khoảng 510,000 VNĐ) nếu các yếu tố khác không đổi.

---

## 5. Đánh giá độ tin cậy và Kiểm định giả thuyết

### a. Hệ số xác định $R^2$ (R-squared)
* Mô hình có **$R^2 = 0.8679$** (hoặc $86.79\%$).
* *Ý nghĩa:* Khoảng cách tới trường giải thích được **86.79%** sự biến động của giá thuê trọ. Đây là một mức độ giải thích rất cao đối với dữ liệu thực tế đời sống, cho thấy khoảng cách đóng vai trò cực kỳ quan trọng quyết định giá phòng trọ. Chỉ còn khoảng 13.21% biến động thuộc về các yếu tố khác (diện tích, nội thất, dịch vụ trọ...).

### b. Kiểm định ý nghĩa hệ số góc ($\beta_1$)
* **Giả thuyết:**
  * $H_0: \beta_1 = 0$ (Khoảng cách không ảnh hưởng đến giá trọ).
  * $H_1: \beta_1 \neq 0$ (Khoảng cách có ảnh hưởng đến giá trọ).
* **Kết quả:** P-value của hệ số góc rất nhỏ ($9.71 \times 10^{-23} \ll 0.05$).
* *Kết luận:* Bác bỏ giả thuyết $H_0$ ở mức ý nghĩa $5\%$. Ta có cơ sở thống kê cực kỳ mạnh mẽ để khẳng định khoảng cách đến trường thực sự có tác động tiêu cực (làm giảm) giá thuê trọ.

---

## 6. Kiểm định các giả định của mô hình (Diagnostics)
Để mô hình hồi quy tuyến tính có độ tin cậy cao, sai số (residuals) cần thỏa mãn các giả định cơ bản:

![Biểu đồ kiểm định sai số](residual_analysis.png)

1. **Giả định phân phối chuẩn (Normality of Residuals):**
   * Đồ thị Q-Q Plot ở bên trái cho thấy các điểm sai số thực tế (màu xanh) bám rất sát đường thẳng 45 độ (màu đỏ).
   * Kiểm định Jarque-Bera có $p\text{-value} = 0.476 > 0.05$, chứng tỏ chưa có cơ sở bác bỏ giả thuyết sai số tuân theo phân phối chuẩn. Giả định phân phối chuẩn được thỏa mãn.
2. **Giả định phương sai sai số không đổi (Homoscedasticity):**
   * Đồ thị Residuals vs Fitted ở bên phải cho thấy các điểm sai số phân tán ngẫu nhiên xung quanh đường $y = 0$, không tạo thành các hình dạng đặc biệt (như hình phễu hay đường cong). Giả định phương sai sai số không đổi được thỏa mãn.
3. **Tính độc lập (Independence):**
   * Chỉ số Durbin-Watson đạt $2.128 \approx 2$, cho thấy không có hiện tượng tự tương quan (autocorrelation) giữa các sai số.

---

## 7. Dự báo thực tế
Nếu một bạn sinh viên muốn thuê trọ ở vị trí cách trường **2.5 km**:
* Áp dụng phương trình hồi quy:
  $$\widehat{\text{Giá trọ}} = 4.52 - 0.51 \times 2.5 = 4.52 - 1.275 = 3.245 \text{ (triệu VNĐ)}$$
* *Kết luận:* Giá thuê trọ dự báo của căn phòng này sẽ khoảng **3.25 triệu VNĐ/tháng**.

---

## 8. Kết luận và Khuyến nghị
* **Kết luận:** Mô hình hồi quy tuyến tính đơn biến được xây dựng cực kỳ vững chắc về mặt toán học thống kê. Nó chứng minh mối tương quan nghịch mạnh mẽ giữa khoảng cách và giá thuê trọ quanh khu vực trường.
* **Khuyến nghị cho sinh viên:** 
  * Nếu sinh viên có ngân sách hạn chế (ví dụ dưới 2.5 triệu VNĐ), nên tìm kiếm phòng trọ cách trường từ 4 km trở lên để có mức giá hợp lý.
  * Nếu ưu tiên thời gian đi lại (ở sát trường dưới 1 km), sinh viên cần chuẩn bị ngân sách tối thiểu từ 4.0 triệu VNĐ trở lên cho một căn phòng tiêu chuẩn trung bình.
