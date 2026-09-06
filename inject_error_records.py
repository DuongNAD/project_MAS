import random
import numpy as np
import pandas as pd

# Thêm các "bản ghi lỗi" vào bảng dữ liệu sạch để luyện làm sạch dữ liệu
# (data cleaning). Chạy trên nền dữ liệu sạch gốc (_clean_base.csv).
#
# Cấu trúc lỗi được đối chiếu với form khảo sát thật (Google Form):
# https://docs.google.com/forms/d/e/1FAIpQLSeEphqFbC8KqumvFsbYmmcjsILfTLIC6UTYcfQh0T-X_rOyNw/viewform
#   - Câu BẮT BUỘC (không thể để trống khi nộp form): Họ tên, Mã SV,
#     Khu vực, Khoảng cách, Giá thuê, Số người.
#   - Câu KHÔNG bắt buộc (có thể bỏ qua -> để trống thật sự): Giới tính,
#     Ngành học, Loại hình phòng ở, Phương tiện di chuyển.
#   - Giới tính / Ngành / Khu vực / Phương tiện đều có lựa chọn "Mục khác"
#     (free text) -> sinh viên có thể nhập giá trị ngoài danh sách chuẩn.
#   - Khu vực còn có thêm Dom F, Dom H; Phương tiện có thêm Xe đạp (form có
#     nhưng data hiện tại chưa từng dùng).
#
# 4 nhóm lỗi, trộn thẳng vào cuối bảng dữ liệu sạch hiện có:
#   1. Thiếu dữ liệu     - bỏ trống các câu KHÔNG bắt buộc (đúng hành vi
#                           thật của Google Form: câu bắt buộc không thể trống)
#   2. Giá trị phi lý    - âm / bằng 0 / quá lớn ở các câu bắt buộc dạng số
#                           (Form không chặn định dạng câu trả lời ngắn)
#   3. Sai định dạng     - đơn vị dính vào số, dấu phẩy thập phân, khoảng
#                           trắng thừa, viết hoa/không dấu sai, mã SV sai
#                           định dạng
#   4. "Mục khác"        - giá trị tự do/ngoài danh sách lựa chọn chuẩn,
#                           mô phỏng đúng hành vi chọn "Mục khác" trên form

random.seed(777)
np.random.seed(777)

df = pd.read_csv('_clean_base.csv')
COLUMNS = list(df.columns)
existing_ma_sv = set(df['Ma_SV'])
used_names = set(df['Ho_Ten'])

SURNAMES = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Hoàng', 'Huỳnh', 'Phan', 'Vũ', 'Võ',
            'Đặng', 'Bùi', 'Đỗ', 'Hồ', 'Ngô', 'Dương', 'Lý', 'Đoàn', 'Phùng', 'Trịnh']
MALE_MIDDLE = ['Văn', 'Hữu', 'Đức', 'Minh', 'Quang', 'Xuân', 'Công', 'Khắc']
FEMALE_MIDDLE = ['Thị', 'Ngọc', 'Thu', 'Kim', 'Diệu', 'Mỹ', 'Hồng', 'Bích']
MALE_FIRST = ['An', 'Bình', 'Cường', 'Dũng', 'Đăng', 'Giang', 'Hùng', 'Kiên', 'Long',
              'Minh', 'Nam', 'Phong', 'Quân', 'Sơn', 'Tuấn', 'Việt', 'Hải', 'Đạt']
FEMALE_FIRST = ['Bình', 'Dung', 'Phương', 'Hoa', 'Lan', 'Ngân', 'Cúc', 'Sen', 'Uyên',
                'Xuân', 'Yến', 'Vy', 'Nga', 'Hạnh', 'Khánh', 'Linh', 'Trinh', 'Quỳnh']
NGANH_MAP = {'HE': 'Công nghệ thông tin', 'HS': 'An toàn thông tin',
             'HA': 'Quản trị kinh doanh', 'HC': 'Thiết kế mỹ thuật số'}

# Theo đúng thuộc tính "Required" của từng câu hỏi trên form thật.
REQUIRED_COLS = ['Ho_Ten', 'Ma_SV', 'Khu_Vuc', 'Khoang_Cach_km', 'Gia_Thue_Trieu', 'So_Nguoi']
OPTIONAL_COLS = ['Gioi_Tinh', 'Nganh', 'Loai_Phong', 'Phuong_Tien']


def gen_name(gender):
    for _ in range(100):
        ho = random.choice(SURNAMES)
        if gender == 'Nam':
            mid, first = random.choice(MALE_MIDDLE), random.choice(MALE_FIRST)
        else:
            mid, first = random.choice(FEMALE_MIDDLE), random.choice(FEMALE_FIRST)
        name = f"{ho} {mid} {first}"
        if name not in used_names:
            used_names.add(name)
            return name
    return name


def gen_ma_sv(prefix):
    while True:
        code = f"{prefix}{random.randint(180000, 220000)}"
        if code not in existing_ma_sv:
            existing_ma_sv.add(code)
            return code


def clone_base_row():
    """Lấy 1 dòng sạch làm khuôn, đổi tên/mã SV để thành 1 quan sát mới."""
    template = df.sample(1, random_state=random.randint(0, 10**6)).iloc[0].to_dict()
    prefix = template['Ma_SV'][:2]
    gender = template['Gioi_Tinh']
    template['Ho_Ten'] = gen_name(gender)
    template['Ma_SV'] = gen_ma_sv(prefix)
    return template


error_rows = []

# ---------------------------------------------------------------
# 1. Thiếu dữ liệu (35 dòng) - chỉ bỏ trống câu KHÔNG bắt buộc,
#    1-2 trường/dòng (câu bắt buộc không thể trống khi đã nộp form)
# ---------------------------------------------------------------
for _ in range(35):
    row = clone_base_row()
    n_missing = random.choice([1, 1, 2])
    for col in random.sample(OPTIONAL_COLS, n_missing):
        row[col] = None
    error_rows.append(row)

# ---------------------------------------------------------------
# 2. Giá trị phi lý (35 dòng) - âm / bằng 0 / quá lớn ở các câu bắt
#    buộc dạng số (form chỉ chặn "trống", không chặn định dạng/khoảng
#    giá trị của câu trả lời ngắn). Một số dòng phi lý ở 2 trường
#    cùng lúc để "bẩn" nặng hơn.
# ---------------------------------------------------------------
ILLOGICAL_PRICE = [-2.5, -1.5, -0.8, 0, 0, 85, 99, 120, 250]
ILLOGICAL_DIST = [-5, -2, -0.5, 0, 300, 500, 999, 9999]
ILLOGICAL_SONGUOI = [0, -1, -3, 30, 50, 99]
ILLOGICAL_FIELDS = ['Gia_Thue_Trieu', 'Khoang_Cach_km', 'So_Nguoi']


def apply_illogical(row, field):
    if field == 'Gia_Thue_Trieu':
        row['Gia_Thue_Trieu'] = random.choice(ILLOGICAL_PRICE)
    elif field == 'Khoang_Cach_km':
        row['Khoang_Cach_km'] = random.choice(ILLOGICAL_DIST)
    else:
        row['So_Nguoi'] = random.choice(ILLOGICAL_SONGUOI)


for _ in range(35):
    row = clone_base_row()
    n_bad = random.choice([1, 1, 2])
    for field in random.sample(ILLOGICAL_FIELDS, n_bad):
        apply_illogical(row, field)
    error_rows.append(row)

# ---------------------------------------------------------------
# 3. Sai định dạng / chính tả (35 dòng) - áp dụng cho mọi câu (bắt
#    buộc hay không), vì form không kiểm tra định dạng câu trả lời
#    ngắn/lựa chọn tự nhập. Một số dòng dính 2 lỗi khác cột cùng lúc.
# ---------------------------------------------------------------
FORMAT_ERRORS = [
    ('Gia_Thue_Trieu', lambda v: f"{v}tr"),
    ('Gia_Thue_Trieu', lambda v: f"{v} triệu"),
    ('Gia_Thue_Trieu', lambda v: str(v).replace('.', ',')),
    ('Khoang_Cach_km', lambda v: f"{v}km"),
    ('Khoang_Cach_km', lambda v: str(v).replace('.', ',')),
    ('Gioi_Tinh', lambda v: ' ' + v if random.random() < 0.5 else v + '  '),
    ('Gioi_Tinh', lambda v: 'nam' if v == 'Nam' else 'nu'),
    ('Gioi_Tinh', lambda v: 'M' if v == 'Nam' else 'F'),
    ('Phuong_Tien', lambda v: v.lower().replace('ề', 'e').replace('ầ', 'a').replace('ộ', 'o')
        .replace('ú', 'u').replace('á', 'a').replace('â', 'a').replace('ê', 'e').replace('ạ', 'a')),
    ('Phuong_Tien', lambda v: '  ' + v),
    ('Loai_Phong', lambda v: v.upper()),
    ('Loai_Phong', lambda v: v + ' '),
    ('Ma_SV', lambda v: v.lower()),
    ('Ma_SV', lambda v: v[:2] + '-' + v[2:]),
    ('Ma_SV', lambda v: v[2:]),
    ('Khu_Vuc', lambda v: v + '   '),
]
for _ in range(35):
    row = clone_base_row()
    n_errs = random.choice([1, 1, 2])
    cols_used = set()
    for _ in range(n_errs):
        col, fn = random.choice(FORMAT_ERRORS)
        if col in cols_used:
            continue
        cols_used.add(col)
        row[col] = fn(row[col])
    error_rows.append(row)

# ---------------------------------------------------------------
# 4. "Mục khác" (20 dòng) - giá trị tự do/ngoài danh sách chuẩn, đúng
#    như khi sinh viên chọn "Mục khác" trên form. Gồm cả giá trị THẬT
#    SỰ hợp lệ mà form có nhưng data cũ chưa dùng (Dom F, Dom H, Xe
#    đạp) lẫn giá trị tự do nằm ngoài mọi danh sách (khó chuẩn hoá).
# ---------------------------------------------------------------
OTHER_VALUE_POOL = [
    ('Gioi_Tinh', 'Khác'),
    ('Gioi_Tinh', 'Không muốn tiết lộ'),
    ('Nganh', 'Ngôn ngữ Anh'),
    ('Nganh', 'Kỹ thuật phần mềm'),
    ('Nganh', 'Trí tuệ nhân tạo'),
    ('Khu_Vuc', 'Dom F'),
    ('Khu_Vuc', 'Dom H'),
    ('Khu_Vuc', 'Xuân Mai'),
    ('Khu_Vuc', 'Đồng Trúc'),
    ('Phuong_Tien', 'Xe đạp'),
    ('Phuong_Tien', 'Grab'),
    ('Phuong_Tien', 'Ba mẹ đưa đón'),
    ('Phuong_Tien', 'Đi nhờ bạn'),
]
for _ in range(20):
    row = clone_base_row()
    col, value = random.choice(OTHER_VALUE_POOL)
    row[col] = value
    error_rows.append(row)

error_df = pd.DataFrame(error_rows, columns=COLUMNS)

# Đảm bảo tuyệt đối: không có dòng lỗi nào để trống trường bắt buộc
assert error_df[REQUIRED_COLS].isna().sum().sum() == 0, "Trường bắt buộc bị lọt null!"

final_df = pd.concat([df, error_df], ignore_index=True)
final_df.to_csv('data.csv', index=False)

print(f"Tổng số dòng sau khi thêm lỗi: {len(final_df)} ({len(df)} sạch + {len(error_df)} lỗi)")
print(f"Tỉ lệ dòng bẩn: {len(error_df) / len(final_df):.1%}")
print(f"Mã SV các dòng lỗi (để đối chiếu khi làm sạch):")
print(error_df['Ma_SV'].tolist())
