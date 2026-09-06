import numpy as np
import pandas as pd

# Hiệu chỉnh dữ liệu Tân Xã theo khảo sát thực tế (ảnh chụp bảng giá trọ +
# tra cứu thị trường) và mở rộng bộ dữ liệu từ 104 lên 137 bản ghi.
#
# Căn cứ thực tế (Tân Xã):
#   YOUNG HOUSE 5      : 3 km    - 2.5tr (dịch vụ 230k)
#   Trọ Mạnh Tuyến      : 3-4 km  - 2.7tr
#   Trọ Kim Bông        : ~5' xe  - 2.7tr
#   Gần hồ Tân Xã       : 2 km    - 1.5tr
#   Trọ Hải Thảo        : ~2 km   - giá không rõ, ước theo mặt bằng chung ~1.6tr
#   Gần hồ (cạnh FPT Software) : 500m - 1.6tr (ngoại lệ gần trường)
#   Thị trường chung    : 1.0-3.0tr, TB ~1.6tr, phòng cao cấp >= 2.6tr
#
# => Khoảng cách Tân Xã trong data.csv trước đây tập trung 0.5-2.5km (quá gần
# so với khảo sát) và giá phòng cao cấp (Chung cư mini/Studio) bị đặt quá cao
# (3.5-4.4tr). Script này giãn khoảng cách Tân Xã lên chủ yếu > 1.8km (chỉ giữ
# lại 1 ngoại lệ 500m đúng như khảo sát thực tế) và hạ giá về đúng mặt bằng.

np.random.seed(2026)

df = pd.read_csv('data.csv')
existing_ma_sv = set(df['Ma_SV'])
used_names = set(df['Ho_Ten'])

SURNAMES = ['Nguyễn', 'Trần', 'Lê', 'Phạm', 'Hoàng', 'Huỳnh', 'Phan', 'Vũ', 'Võ',
            'Đặng', 'Bùi', 'Đỗ', 'Hồ', 'Ngô', 'Dương', 'Lý', 'Đoàn', 'Phùng', 'Trịnh']
MALE_MIDDLE = ['Văn', 'Hữu', 'Đức', 'Minh', 'Quang', 'Xuân', 'Công', 'Khắc']
FEMALE_MIDDLE = ['Thị', 'Ngọc', 'Thu', 'Kim', 'Diệu', 'Mỹ', 'Hồng', 'Bích']
MALE_FIRST = ['An', 'Bình', 'Cường', 'Dũng', 'Đăng', 'Giang', 'Hùng', 'Kiên', 'Long',
              'Minh', 'Nam', 'Phong', 'Quân', 'Sơn', 'Tuấn', 'Việt', 'Hải', 'Đạt',
              'Toàn', 'Vinh', 'Khang', 'Trung', 'Sinh', 'Lâm']
FEMALE_FIRST = ['Bình', 'Dung', 'Phương', 'Hoa', 'Lan', 'Ngân', 'Cúc', 'Sen', 'Uyên',
                'Xuân', 'Yến', 'Vy', 'Nga', 'Hạnh', 'Khánh', 'Linh', 'Trinh', 'Quỳnh',
                'Ánh', 'Mai', 'Nhung', 'Gấm', 'Đào', 'Tú', 'Như', 'Kiều', 'Liễu']
NGANH_MAP = {'HE': 'Công nghệ thông tin', 'HS': 'An toàn thông tin',
             'HA': 'Quản trị kinh doanh', 'HC': 'Thiết kế mỹ thuật số'}
PREFIXES = list(NGANH_MAP.keys())


def gen_name(gender):
    for _ in range(100):
        ho = np.random.choice(SURNAMES)
        if gender == 'Nam':
            mid, first = np.random.choice(MALE_MIDDLE), np.random.choice(MALE_FIRST)
        else:
            mid, first = np.random.choice(FEMALE_MIDDLE), np.random.choice(FEMALE_FIRST)
        name = f"{ho} {mid} {first}"
        if name not in used_names:
            used_names.add(name)
            return name
    return name


def gen_ma_sv(prefix):
    while True:
        code = f"{prefix}{np.random.randint(180000, 220000)}"
        if code not in existing_ma_sv:
            existing_ma_sv.add(code)
            return code


new_rows = []


def make_row(khu_vuc, loai_phong, dist, price, so_nguoi, phuong_tien):
    gender = np.random.choice(['Nam', 'Nữ'])
    prefix = np.random.choice(PREFIXES)
    new_rows.append({
        'Ho_Ten': gen_name(gender),
        'Gioi_Tinh': gender,
        'Ma_SV': gen_ma_sv(prefix),
        'Nganh': NGANH_MAP[prefix],
        'Khu_Vuc': khu_vuc,
        'Loai_Phong': loai_phong,
        'Khoang_Cach_km': round(float(dist), 1),
        'Gia_Thue_Trieu': round(float(price), 1),
        'So_Nguoi': int(so_nguoi),
        'Phuong_Tien': phuong_tien,
    })


# ---------------------------------------------------------------
# 1. Hiệu chỉnh 27 dòng Tân Xã hiện có: giãn khoảng cách sang > 1.8km,
#    hạ giá về đúng mặt bằng khảo sát thực tế.
# ---------------------------------------------------------------
tx_mask = df['Khu_Vuc'] == 'Tân Xã'
old_dist = df.loc[tx_mask, 'Khoang_Cach_km']
new_dist = (1.9 + (old_dist - old_dist.min()) * 1.2).round(1)

noise = np.random.normal(0, 0.15, tx_mask.sum())
loai = df.loc[tx_mask, 'Loai_Phong']
base_price = np.where(
    loai == 'Chung cư mini/Studio',
    3.1 - 0.08 * (new_dist - 1.9),
    2.3 - 0.12 * (new_dist - 1.9),
)
new_price = base_price + noise
new_price = np.where(loai == 'Chung cư mini/Studio',
                      np.clip(new_price, 2.6, 3.3),
                      np.clip(new_price, 1.4, 2.7))

df.loc[tx_mask, 'Khoang_Cach_km'] = new_dist.values
df.loc[tx_mask, 'Gia_Thue_Trieu'] = np.round(new_price, 1)

# ---------------------------------------------------------------
# 2. Thêm 9 dòng Tân Xã mới, bám theo các mốc thực tế thu thập được
#    (chỉ 1 ngoại lệ < 1.8km, đúng như trường hợp thực tế "cách FPT Software 500m")
# ---------------------------------------------------------------
make_row('Tân Xã', 'Phòng khép kín', 3.0, 2.5, 1, 'Xe máy')       # YOUNG HOUSE 5
make_row('Tân Xã', 'Phòng trọ cơ bản', 3.5, 2.7, 2, 'Xe máy')      # Trọ Mạnh Tuyến
make_row('Tân Xã', 'Chung cư mini', 2.3, 2.7, 2, 'Xe máy')         # Trọ Kim Bông (~5 phút xe)
make_row('Tân Xã', 'Phòng trọ cơ bản', 2.0, 1.5, 2, 'Xe máy')      # Gần hồ Tân Xã
make_row('Tân Xã', 'Phòng trọ cơ bản', 2.0, 1.6, 1, 'Xe máy')      # Trọ Hải Thảo
make_row('Tân Xã', 'Phòng trọ cơ bản', 0.5, 1.6, 2, 'Đi bộ')       # Gần hồ, sát FPT Software (ngoại lệ)
make_row('Tân Xã', 'Phòng trọ cơ bản', 2.2, 1.9, 1, 'Xe máy')
make_row('Tân Xã', 'Chung cư mini/Studio', 2.8, 2.8, 2, 'Xe máy')
make_row('Tân Xã', 'Phòng trọ cơ bản', 3.2, 2.0, 2, 'Xe máy')

# ---------------------------------------------------------------
# 3. Mở rộng các khu vực khác theo đúng xu hướng đã có, để tổng đạt 137 dòng
#    (Thạch Hòa +8, Hòa Lạc +8, Dom A-D +2 mỗi khu = +33 dòng)
# ---------------------------------------------------------------
th_dist = [2.6, 3.0, 3.3, 3.6, 3.9, 4.2, 4.5, 4.8]
th_types = ['Phòng trọ cơ bản', 'Chung cư mini', 'Phòng trọ cơ bản', 'Chung cư mini',
            'Phòng trọ cơ bản', 'Chung cư mini', 'Phòng trọ cơ bản', 'Phòng trọ cơ bản']
for d, t in zip(th_dist, th_types):
    if t == 'Chung cư mini':
        price = np.clip(3.15 - 0.08 * d + np.random.normal(0, 0.1), 2.5, 3.1)
        so_nguoi = 2
    else:
        price = np.clip(2.55 - 0.14 * d + np.random.normal(0, 0.1), 1.7, 2.3)
        so_nguoi = int(np.random.choice([1, 2]))
    make_row('Thạch Hòa', t, d, price, so_nguoi, 'Xe máy')

hl_dist = [5.4, 5.7, 6.3, 6.6, 6.9, 7.4, 7.9, 8.7]
for d in hl_dist:
    price = np.clip(2.55 - 0.15 * d + np.random.normal(0, 0.08), 1.1, 2.0)
    so_nguoi = int(np.random.choice([1, 2]))
    make_row('Hòa Lạc', 'Phòng khép kín', d, price, so_nguoi, 'Xe buýt')

dom_specs = [
    ('Dom A', 0.15, 1.1, 4), ('Dom A', 0.45, 0.8, 6),
    ('Dom B', 0.15, 1.1, 4), ('Dom B', 0.50, 0.8, 6),
    ('Dom C', 0.20, 1.1, 4), ('Dom C', 0.55, 0.8, 6),
    ('Dom D', 0.30, 1.1, 4), ('Dom D', 0.60, 0.8, 6),
]
for khu, d, price, so_nguoi in dom_specs:
    make_row(khu, 'Ký túc xá', d, price, so_nguoi, 'Đi bộ')

final_df = pd.concat([df, pd.DataFrame(new_rows)], ignore_index=True)
final_df.to_csv('data.csv', index=False)

print(f"Tổng số dòng: {len(final_df)}")
print(final_df['Khu_Vuc'].value_counts())
tx = final_df[final_df['Khu_Vuc'] == 'Tân Xã']
print(f"\nTân Xã: {len(tx)} dòng, "
      f"{(tx['Khoang_Cach_km'] > 1.8).sum()}/{len(tx)} dòng > 1.8km "
      f"({(tx['Khoang_Cach_km'] > 1.8).mean():.1%})")
print(tx[['Khoang_Cach_km', 'Gia_Thue_Trieu']].describe())
