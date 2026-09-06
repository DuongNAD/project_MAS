import re
import pandas as pd

# Làm sạch data.csv (bản có lẫn 60 dòng lỗi do inject_error_records.py thêm
# vào để luyện data cleaning) và xuất ra data_clean.csv - giữ nguyên data.csv
# gốc để dùng làm bài tập / đối chiếu.
#
# Nguyên tắc:
#   - Lỗi SAI ĐỊNH DẠNG (đơn vị dính số, dấu phẩy thập phân, khoảng trắng
#     thừa, hoa/thường sai, dấu gạch ngang trong Ma_SV...) -> SỬA lại đúng.
#   - Lỗi THIẾU DỮ LIỆU (ô trống) hoặc GIÁ TRỊ PHI LÝ (âm, bằng 0, quá lớn,
#     Ma_SV sai cấu trúc không suy ra được) -> LOẠI BỎ dòng đó, vì không có
#     căn cứ để tự bịa ra giá trị đúng.

SRC = 'data.csv'
OUT = 'data_clean.csv'

VALID_GIOI_TINH = {'nam': 'Nam', 'm': 'Nam', 'nữ': 'Nữ', 'nu': 'Nữ', 'f': 'Nữ'}

VALID_LOAI_PHONG = ['Ký túc xá', 'Phòng trọ cơ bản', 'Phòng khép kín',
                     'Chung cư mini', 'Chung cư mini/Studio']
LOAI_PHONG_MAP = {v.lower(): v for v in VALID_LOAI_PHONG}

VALID_PHUONG_TIEN = ['Đi bộ', 'Xe máy', 'Xe buýt', 'Xe đạp']
PHUONG_TIEN_MAP = {
    'di bo': 'Đi bộ', 'đi bộ': 'Đi bộ', 'đi bo': 'Đi bộ',
    'xe may': 'Xe máy', 'xe máy': 'Xe máy',
    'xe buyt': 'Xe buýt', 'xe buýt': 'Xe buýt',
    'xe dap': 'Xe đạp', 'xe đạp': 'Xe đạp',
}

# Khớp đúng danh sách lựa chọn thật trên Google Form khảo sát (bao gồm cả
# Dom F, Dom H mà data cũ chưa từng dùng tới).
VALID_KHU_VUC = {'Dom A', 'Dom B', 'Dom C', 'Dom D', 'Dom F', 'Dom H',
                  'Tân Xã', 'Thạch Hòa', 'Hòa Lạc'}
VALID_NGANH = {'Công nghệ thông tin', 'An toàn thông tin',
               'Quản trị kinh doanh', 'Thiết kế mỹ thuật số'}

MA_SV_RE = re.compile(r'^(HE|HS|HA|HC)\d{6}$')

DIST_MAX = 15.0     # km hợp lý xa nhất trong khảo sát (Hòa Lạc xa nhất ~8.7km)
PRICE_MAX = 4.0      # triệu, cao nhất là chung cư mini/studio Tân Xã ~3.3tr
SO_NGUOI_MAX = 6      # phòng dom đông nhất là 6 người


def clean_number(raw):
    """'2.5tr' / '2,5' / ' 3.0km ' -> float, hoặc None nếu không parse được."""
    if pd.isna(raw):
        return None
    s = str(raw).strip()
    s = re.sub(r'(tr|triệu|km)$', '', s, flags=re.IGNORECASE).strip()
    s = s.replace(',', '.')
    try:
        return float(s)
    except ValueError:
        return None


def clean_gioi_tinh(raw):
    if pd.isna(raw):
        return None
    return VALID_GIOI_TINH.get(str(raw).strip().lower())


def clean_categorical(raw, canon_map, valid_set=None):
    if pd.isna(raw):
        return None
    s = str(raw).strip()
    if canon_map is not None and s.lower() in canon_map:
        return canon_map[s.lower()]
    if valid_set is not None and s in valid_set:
        return s
    return None


def clean_ma_sv(raw):
    if pd.isna(raw):
        return None
    s = str(raw).strip().upper().replace('-', '').replace(' ', '')
    return s if MA_SV_RE.match(s) else None


def clean_row(row):
    reasons = []

    ho_ten = row['Ho_Ten'].strip() if pd.notna(row['Ho_Ten']) else None
    if not ho_ten:
        reasons.append('thiếu Ho_Ten')

    gioi_tinh = clean_gioi_tinh(row['Gioi_Tinh'])
    if gioi_tinh is None:
        reasons.append('thiếu/sai Gioi_Tinh')

    ma_sv = clean_ma_sv(row['Ma_SV'])
    if ma_sv is None:
        reasons.append('Ma_SV sai cấu trúc')

    nganh = row['Nganh'].strip() if pd.notna(row['Nganh']) else None
    if nganh not in VALID_NGANH:
        reasons.append('thiếu/sai Nganh')

    khu_vuc = row['Khu_Vuc'].strip() if pd.notna(row['Khu_Vuc']) else None
    if khu_vuc not in VALID_KHU_VUC:
        reasons.append('thiếu/sai Khu_Vuc')

    loai_phong = clean_categorical(row['Loai_Phong'], LOAI_PHONG_MAP)
    if loai_phong is None:
        reasons.append('thiếu/sai Loai_Phong')

    dist = clean_number(row['Khoang_Cach_km'])
    if dist is None or not (0 < dist <= DIST_MAX):
        reasons.append('Khoang_Cach_km phi lý')

    price = clean_number(row['Gia_Thue_Trieu'])
    if price is None or not (0 < price <= PRICE_MAX):
        reasons.append('Gia_Thue_Trieu phi lý')

    so_nguoi = clean_number(row['So_Nguoi'])
    if so_nguoi is None or not (1 <= so_nguoi <= SO_NGUOI_MAX) or so_nguoi != int(so_nguoi):
        reasons.append('So_Nguoi phi lý')

    phuong_tien = clean_categorical(row['Phuong_Tien'], PHUONG_TIEN_MAP)
    if phuong_tien is None:
        reasons.append('thiếu/sai Phuong_Tien')

    if reasons:
        return None, reasons

    cleaned = {
        'Ho_Ten': ho_ten,
        'Gioi_Tinh': gioi_tinh,
        'Ma_SV': ma_sv,
        'Nganh': nganh,
        'Khu_Vuc': khu_vuc,
        'Loai_Phong': loai_phong,
        'Khoang_Cach_km': round(dist, 1),
        'Gia_Thue_Trieu': round(price, 1),
        'So_Nguoi': int(so_nguoi),
        'Phuong_Tien': phuong_tien,
    }
    return cleaned, []


df = pd.read_csv(SRC, dtype=str, keep_default_na=True)

kept, dropped = [], []
for _, row in df.iterrows():
    cleaned, reasons = clean_row(row)
    if cleaned is not None:
        kept.append(cleaned)
    else:
        dropped.append((row.get('Ma_SV'), reasons))

clean_df = pd.DataFrame(kept, columns=df.columns)
before_dedup = len(clean_df)
clean_df = clean_df.drop_duplicates(subset=['Ma_SV'])
clean_df.to_csv(OUT, index=False)

print(f"Tổng số dòng gốc: {len(df)}")
print(f"Số dòng giữ lại (đã làm sạch): {len(clean_df)}")
print(f"Số dòng loại bỏ: {len(dropped)}")
if before_dedup != len(clean_df):
    print(f"  (trong đó {before_dedup - len(clean_df)} dòng trùng Ma_SV sau khi sửa, đã loại bớt)")
print(f"Đã lưu vào: {OUT}")
print()
print("Chi tiết các dòng bị loại (Ma_SV gốc - lý do):")
for ma_sv, reasons in dropped:
    print(f"  {ma_sv if pd.notna(ma_sv) else '(không có)'}: {', '.join(reasons)}")
