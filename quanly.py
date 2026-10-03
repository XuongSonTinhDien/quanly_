import streamlit as st
import datetime
import sqlite3
import pandas as pd

# 1. CẤU HÌNH TRANG HIỂN THỊ
st.set_page_config(page_title="Hóa Đơn Công Nợ v9.7", layout="wide")

# THÔNG TIN CƠ SỞ CỦA ANH HƯỞNG
TEN_CO_SO = "XƯỞNG SƠN TĨNH ĐIỆN PHÚ THỌ"
SDT_CHU_XUONG = "0979.141.588"
STK_NGAN_HANG = "104869545034"
MA_BIN_NGAN_HANG = "ICB"  # VietinBank
TEN_NGAN_HANG = "VietinBank - CN VINH PHUC"
TEN_CHU_TK = "LE VAN HUONG"

# 2. KẾT NỐI CƠ SỞ DỮ LIỆU CŨ (SQLITE)
DB_FILE = "dulieu_sơn tĩnh điện.db"

def ket_noi_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS khach_hang (
            ten TEXT PRIMARY KEY, sdt TEXT, diachi TEXT, nocu REAL DEFAULT 0
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lich_su_mua (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            ten_khach TEXT, ngay TEXT, loai_gd TEXT, 
            ten_hang TEXT, dvt TEXT, dongia REAL DEFAULT 0, 
            soluong REAL DEFAULT 0, thanhtien REAL DEFAULT 0
        )
    """)
    conn.commit()
    return conn

conn = ket_noi_db()
cursor = conn.cursor()

# 3. GIAO DIỆN CHÍNH
st.title("🏪 HỆ THỐNG QUẢN LÝ BÁN HÀNG & CÔNG NỢ SƠN TĨNH ĐIỆN")
col_nhap, col_hoadon = st.columns([1, 1.3])
with col_nhap:
    st.header("🛠️ Khu Vực Nhập Liệu")
    ten_nhap_raw = st.text_input("Gõ tên khách hàng để tra cứu/Tạo mới:", value="Anh Hưởng")
    ten_chuan_hoa = " ".join([w.capitalize() for w in ten_nhap_raw.strip().split()])

    sdt_mac_dinh, diachi_mac_dinh, nocu_mac_dinh = "", "", 0.0
    khach_cu = False

    cursor.execute("SELECT ten, sdt, diachi, nocu FROM khach_hang WHERE ten LIKE ?", (ten_chuan_hoa,))
    row_khach = cursor.fetchone()

    if row_khach:
        ten_chuan_hoa, sdt_mac_dinh, diachi_mac_dinh, nocu_mac_dinh = row_khach
        khach_cu = True
        st.success(f"🔍 Đã tìm thấy khách hàng: **{ten_chuan_hoa}**")
    else:
        st.info(f"🆕 Khách mới: **{ten_chuan_hoa}**")

    # FORM 1: THÔNG TIN KHÁCH HÀNG
    with st.form("form_khach_hang"):
        st.subheader("👤 Thông tin khách hàng")
        sdt = st.text_input("Số ĐT Khách:", value=sdt_mac_dinh)
        diachi = st.text_input("Địa chỉ Khách:", value=diachi_mac_dinh)
        no_dau_ky = st.number_input("Nợ gốc mang sang (VNĐ):", value=float(nocu_mac_dinh), step=10000.0, format="%.0f")
        if st.form_submit_button("💾 LƯU THÔNG TIN KHÁCH"):
            if not khach_cu:
                cursor.execute("INSERT INTO khach_hang VALUES (?, ?, ?, ?)", (ten_chuan_hoa, sdt, diachi, no_dau_ky))
            else:
                cursor.execute("UPDATE khach_hang SET sdt = ?, diachi = ?, nocu = ? WHERE ten = ?", (sdt, diachi, no_dau_ky, ten_chuan_hoa))
            conn.commit()
            st.success("Đã lưu thành công!")
            st.rerun()

    # FORM 2: PHÁT SINH GIAO DỊCH (Có chọn ngày)
    with st.form("form_giao_dich"):
        st.subheader("📦 Phát sinh giao dịch mới")
        loai_gd = st.radio("Loại giao dịch:", ["Mua hàng", "Khách trả tiền mặt/Chuyển khoản"], horizontal=True)
        
        # Ô chọn ngày mới thêm vào đây
        ngay_gd_chon = st.date_input("Ngày giao dịch (Bấm vào để chọn ngày cũ):", value=datetime.date.today())
        ngay_dinh_dang_str = ngay_gd_chon.strftime("%d/%m/%Y")

        ten_hang = st.text_input("Tên mặt hàng / Nội dung công việc:")
        dvt = st.selectbox("Đơn vị tính:", ["bộ", "cái", "kg", "m2", "lượt"])
        don_gia = st.number_input("Đơn giá (VNĐ):", min_value=0.0, step=5000.0, format="%.0f")
        so_luong = st.number_input("Số lượng mua:", min_value=0.1, step=1.0, value=1.0)
        so_tien_tra = st.number_input("Số tiền khách trả (nếu trả tiền):", min_value=0.0, step=50000.0, format="%.0f")

        if st.form_submit_button("➕ KÍCH LƯU GIAO DỊCH"):
            if not khach_cu:
                cursor.execute("INSERT INTO khach_hang VALUES (?, ?, ?, ?)", (ten_chuan_hoa, sdt, diachi, no_dau_ky))
            
            if loai_gd == "Mua hàng":
                if ten_hang.strip() == "": 
                    st.error("Vui lòng nhập tên mặt hàng!")
                else:
                    thanhtien = don_gia * so_luong
                    cursor.execute("""
                        INSERT INTO lich_su_mua (ten_khach, ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (ten_chuan_hoa, ngay_dinh_dang_str, "Mua hàng", ten_hang, dvt, don_gia, so_luong, thanhtien))
                    conn.commit()
                    st.rerun()
            else:
                if so_tien_tra <= 0: 
                    st.error("Vui lòng nhập số tiền!")
                else:
                    cursor.execute("""
                        INSERT INTO lich_su_mua (ten_khach, ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (ten_chuan_hoa, ngay_dinh_dang_str, "Trả tiền", "Khách thanh toán tiền mặt/CK", "-", 0, 0, -so_tien_tra))
                    conn.commit()
                    st.rerun()

    # KHU VỰC SỬA LỖI XÓA CHỌN LỌC
    st.markdown("---")
    st.subheader("🗑️ Sửa Lỗi Gõ Sai / Xóa Giao Dịch")
    cursor.execute("SELECT id, ngay, loai_gd, ten_hang, thanhtien FROM lich_su_mua WHERE ten_khach = ?", (ten_chuan_hoa,))
    all_products = cursor.fetchall()

    if all_products:
        options_xoa = {}
        for p_id, p_ngay, p_loai, p_ten, p_tt in all_products:
            ngay_ngan = p_ngay[:5] if p_ngay else ""
            hien_thi_tien = f"{int(p_tt):,}" if p_loai == "Mua hàng" else f"Trừ nợ: {int(abs(p_tt)):,}"
            options_xoa[f"[{ngay_ngan}] {p_loai} - {p_ten} ({hien_thi_tien} đ)"] = p_id

        san_pham_chon_xoa = st.selectbox("👉 Chọn dòng muốn xóa khỏi hóa đơn:", list(options_xoa.keys()))
        id_can_xoa = options_xoa[san_pham_chon_xoa]

        col_x1, col_x2 = st.columns(2)
        with col_x1:
            if st.button("❌ XÓA DÒNG ĐÃ CHỌN", use_container_width=True):
                cursor.execute("DELETE FROM lich_su_mua WHERE id = ?", (id_can_xoa,))
                conn.commit()
                st.rerun()
        with col_x2:
            if st.button("🗑️ XÓA SẠCH KHÁCH HÀNG NÀY", use_container_width=True):
                cursor.execute("DELETE FROM khach_hang WHERE ten = ?", (ten_chuan_hoa,))
                cursor.execute("DELETE FROM lich_su_mua WHERE ten_khach = ?", (ten_chuan_hoa,))
                conn.commit()
                st.rerun()
# 4. KHU VỰC HIỂN THỊ HÓA ĐƠN VÀ THÔNG TIN THANH TOÁN (CỘT PHẢI)
with col_hoadon:
    st.subheader("📅 Bộ Lọc Xem Hóa Đơn")
    thang_chon = st.selectbox("Khoảng thời gian cần in/xem:", ["Tất cả thời gian", "Tháng hiện tại", "Tháng trước"])

    ngay_hien_tai_dt = datetime.datetime.now()
    thang_hien_tai_str = ngay_hien_tai_dt.strftime("/%m/%Y")

    nam_truoc = ngay_hien_tai_dt.year
    thang_truoc = ngay_hien_tai_dt.month - 1
    if thang_truoc == 0:
        thang_truoc = 12
        nam_truoc -= 1
    thang_truoc_str = f"/{thang_truoc:02d}/{nam_truoc}"

    # TRUY VẤN LỊCH SỬ GIAO DỊCH THEO BỘ LỌC THỜI GIAN
    query = "SELECT ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien FROM lich_su_mua WHERE ten_khach = ?"
    params = [ten_chuan_hoa]
    
    if thang_chon == "Tháng hiện tại":
        query += " AND ngay LIKE ?"
        params.append(f"%{thang_hien_tai_str}")
    elif thang_chon == "Tháng trước":
        query += " AND ngay LIKE ?"
        params.append(f"%{thang_truoc_str}")

    cursor.execute(query, tuple(params))
    rows_giao_dich = cursor.fetchall()

    # TÍNH TOÁN TIỀN BẠC
    tong_phat_sink = 0.0
    tong_da_tra = 0.0
    
    rows_html = ""
    stt = 1
    for r_ngay, r_loai, r_ten, r_dvt, r_dg, r_sl, r_tt in rows_giao_dich:
        if r_loai == "Mua hàng":
            tong_phat_sink += r_tt
            rows_html += f"""
            <tr>
                <td style='text-align:center;'>{stt}</td>
                <td style='text-align:center;'>{r_ngay}</td>
                <td>{r_ten}</td>
                <td style='text-align:center;'>{r_dvt}</td>
                <td style='text-align:right;'>{int(r_dg):,}</td>
                <td style='text-align:center;'>{r_sl:g}</td>
                <td style='text-align:right;'>{int(r_tt):,}</td>
            </tr>
            """
        else:
            tong_da_tra += abs(r_tt)
            rows_html += f"""
            <tr style='background-color: #f9f9f9; font-style: italic;'>
                <td style='text-align:center;'>{stt}</td>
                <td style='text-align:center;'>{r_ngay}</td>
                <td>{r_ten}</td>
                <td style='text-align:center;'>-</td>
                <td style='text-align:right;'>-</td>
                <td style='text-align:center;'>-</td>
                <td style='text-align:right; color: green;'>-{int(abs(r_tt)):,}</td>
            </tr>
            """
        stt += 1

    # Tổng nợ cuối cùng = Nợ mang sang + Phát sinh mới - Số tiền đã trả
    tong_no_cuoi = no_dau_ky + tong_phat_sink - tong_da_tra

    # 5. THIẾT KẾ KHU VỰC INẤN HÓA ĐƠN BẰNG HTML (Dễ dàng căn chỉnh để xuất file PDF)
    html_hoadon = f"""
    <div id="print-section" style="font-family: Arial, sans-serif; color: #333; padding: 15px; border: 1px solid #ccc; border-radius: 5px; background: #fff;">
        <h2 style='text-align: center; color: #D32F2F; margin-bottom: 5px;'>🏪 {TEN_CO_SO}</h2>
        <p style='text-align: center; margin: 0 0 5px 0;'>📞 Hotline/Zalo quản lý: <b>{SDT_CHU_XUONG}</b></p>
        <p style='text-align: center; margin: 0; font-size: 14px; color: #1E3A8A;'><b>THÔNG TIN THANH TOÁN CHUYỂN KHOẢN:</b></p>
        <p style='text-align: center; margin: 2px 0;'>Số tài khoản: <span style='font-size: 16px; color: red; font-weight: bold;'>{STK_NGAN_HANG}</span></p>
        <p style='text-align: center; margin: 0; font-size: 13px;'>Ngân hàng: <b>{TEN_NGAN_HANG}</b> - Chủ TK: <b>{TEN_CHU_TK}</b></p>
        <hr style='border-top: 2px dashed #bbb; margin: 15px 0;'>

        <table style="width: 100%; margin-bottom: 15px; font-size: 14px;">
            <tr>
                <td style="width: 50%;"><b>Khách hàng:</b> {ten_chuan_hoa.upper()}</td>
                <td style="width: 50%;"><b>Số ĐT:</b> {sdt if sdt else '...................................'}</td>
            </tr>
            <tr>
                <td><b>Địa chỉ:</b> {diachi if diachi else '...................................'}</td>
                <td><b>Ngày in:</b> {ngay_hien_tai_dt.strftime('%d/%m/%Y %H:%M')}</td>
            </tr>
        </table>

        <table style="width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 15px;" border="1" cellpadding="5">
            <thead style="background-color: #f2f2f2;">
                <tr>
                    <th style="width: 5%;">STT</th>
                    <th style="width: 12%;">Ngày</th>
                    <th>Nội dung mặt hàng / Giao dịch</th>
                    <th style="width: 8%;">ĐVT</th>
                    <th style="width: 12%;">Đơn giá</th>
                    <th style="width: 8%;">SL</th>
                    <th style="width: 15%;">Thành tiền (đ)</th>
                </tr>
            </thead>
            <tbody>
                {rows_html if rows_html else "<tr><td colspan='7' style='text-align:center;'>Không có dữ liệu giao dịch phát sinh.</td></tr>"}
            </tbody>
        </table>

        <table style="width: 100%; font-size: 14px;">
            <tr>
                <td style="width: 50%; vertical-align: top;">
                    <p style="margin: 3px 0;">🔹 Nợ gốc mang sang: <b>{int(no_dau_ky):,} đ</b></p>
                    <p style="margin: 3px 0;">➕ Tổng phát sinh mới: <b>{int(tong_phat_sink):,} đ</b></p>
                    <p style="margin: 3px 0;">➖ Tổng tiền đã trả: <b>{int(tong_da_tra):,} đ</b></p>
                </td>
                <td style="width: 50%; text-align: right; vertical-align: top;">
                    <h3 style="margin: 0; color: #333;">🛑 TỔNG NỢ CUỐI CÙNG:</h3>
                    <h2 style="color: red; margin: 5px 0 0 0;">{int(tong_no_cuoi):,} VNĐ</h2>
                </td>
            </tr>
        </table>
    </div>
    """

    # 6. NÚT LỆNH IN HOẶC LƯU PDF THỰC TẾ QUA JAVASCRIPT
    js_print_code = f"""
    <script>
    function printInvoice() {{
        var printContents = document.getElementById('print-section').innerHTML;
        var originalContents = document.body.innerHTML;
        document.body.innerHTML = printContents;
        window.print();
        document.body.innerHTML = originalContents;
        window.location.reload();
    }}
    </script>
    <button onclick="printInvoice()" style="width: 100%; background-color: #2E7D32; color: white; padding: 12px 20px; border: none; border-radius: 4px; cursor: pointer; font-size: 16px; font-weight: bold; margin-top: 15px;">
        🖨️ KÍCH BẤM ĐỂ IN HÓA ĐƠN / LƯU FILE PDF
    </button>
    """
    
    st.components.v1.html(html_hoadon + js_print_code, height=650, scrolling=True)

# ĐÓNG KẾT NỐI DB KHI KẾT THÚC SCRIPT
conn.close()

