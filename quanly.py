import os
import sqlite3
import datetime
import streamlit as st
import pandas as pd
import json
import io

# Cấu hình giao diện Streamlit rộng rãi toàn màn hình
st.set_page_config(page_title="Hệ Thống Quản Lý Sơn Tĩnh Điện", layout="wide")

# =============================================================
# 1. CẤU HÌNH HỆ THỐNG & THÔNG TIN CƠ SỞ
# =============================================================
DB_FILE = "dulieu_son_tinh_dien.db"
TEN_CO_SO = "XƯỞNG SƠN TĨNH ĐIỆN HƯỞNG THỦY"
SDT_CHU_XUONG = "0979.141.588...0354.179.792"
DIA_CHI_XUONG = "Tân Lập Hợp Lý Phú Thọ"
STK_NGAN_HANG = "104869545034...0979141588"
TEN_NGAN_HANG = "VietinBank - CN VINH PHUC"
TEN_CHU_TK = "LE VAN HUONG"

def chuyen_doi_so_an_toan(gia_tri):
    """Hàm bổ sung để tránh lỗi sập hệ thống khi dữ liệu trống hoặc lỗi chuỗi"""
    if gia_tri is None:
        return 0
    if isinstance(gia_tri, str):
        gia_tri = gia_tri.strip()
        if gia_tri == "":
            return 0
    try:
        return int(float(gia_tri))
    except (ValueError, TypeError):
        return 0

def lay_khung_html_a4(ten_chuan_hoa, sdt, diachi, rows_html, no_dau_ky, tong_phat_sinh, tong_da_tra, tong_no_cuoi_ky):
    ngay_lap_he_thong = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    no_dau_ky_int = chuyen_doi_so_an_toan(no_dau_ky)
    tong_phat_sinh_int = chuyen_doi_so_an_toan(tong_phat_sinh)
    tong_da_tra_int = chuyen_doi_so_an_toan(tong_da_tra)
    tong_no_cuoi_ky_int = chuyen_doi_so_an_toan(tong_no_cuoi_ky)
    
    return f"""
    <div style="font-family: Arial, sans-serif; background-color: #fff; color: #000; max-width: 650px; margin: 0 auto; padding: 15px; border: 1px solid #000; box-sizing: border-box;">
        <div style="text-align: center; margin-bottom: 15px;">
            <h2 style="margin: 0; text-transform: uppercase; font-size: 18px; font-weight: bold;">🏪 {TEN_CO_SO}</h2>
            <p style="margin: 4px 0; font-size: 13px;">Hotline/Zalo quản lý: {SDT_CHU_XUONG}</p>
            <p style="margin: 3px 0; font-size: 13px;">Địa chỉ: {DIA_CHI_XUONG}</p>
            <p style="margin: 8px 0 3px 0; font-size: 12px; font-weight: bold; text-transform: uppercase;">THÔNG TIN THANH TOÁN CHUYỂN KHOẢN:</p>
            <p style="margin: 3px 0; font-size: 13px;">Số tài khoản: <strong style="font-size: 15px;">{STK_NGAN_HANG}</strong></p>
            <p style="margin: 3px 0; font-size: 13px;">Ngân hàng: {TEN_NGAN_HANG} - Chủ TK: {TEN_CHU_TK}</p>
            <hr style="border: none; border-top: 1px dashed #000; margin: 10px 0;">
            <table style="width: 100%; border: none; font-size: 13px; margin-bottom: 5px; line-height: 1.5; text-align: left; border-collapse: collapse;">
                <tr>
                    <td style="padding: 2px 0; width: 60%;"><strong>Khách hàng:</strong> <span style="text-transform: uppercase; font-weight: bold;">{ten_chuan_hoa}</span></td>
                    <td style="padding: 2px 0; width: 40%; text-align: right;"><strong>Số ĐT:</strong> {sdt if sdt else '...'}</td>
                </tr>
                <tr>
                    <td style="padding: 2px 0;"><strong>Địa chỉ:</strong> {diachi if diachi else '...'}</td>
                    <td style="padding: 2px 0; text-align: right;"><strong>Ngày in:</strong> {ngay_lap_he_thong}</td>
                </tr>
            </table>
        </div>
        <div style="margin-bottom: 15px;">
            <table style="width: 100%; border-collapse: collapse; font-size: 12px; border: 1px solid #000;">
                <thead>
                    <tr style="background-color: #f2f2f2; height: 28px; font-weight: bold; text-align: center;">
                        <th style="width: 7%; border: 1px solid #000;">STT</th>
                        <th style="width: 15%; border: 1px solid #000;">Ngày</th>
                        <th style="width: 38%; text-align: left; padding-left: 5px; border: 1px solid #000;">Nội dung mặt hàng / Giao dịch</th>
                        <th style="width: 8%; border: 1px solid #000;">ĐVT</th>
                        <th style="width: 10%; text-align: right; padding-right: 5px; border: 1px solid #000;">Đơn giá</th>
                        <th style="width: 8%; border: 1px solid #000;">SL</th>
                        <th style="width: 14%; text-align: right; padding-right: 5px; border: 1px solid #000;">Thành tiền</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        <div style="border-top: 1px solid #000; padding-top: 8px;">
            <table style="width: 100%; border: none; font-size: 13px; line-height: 1.6; text-align: left; border-collapse: collapse;">
                <tr>
                    <td style="width: 55%; vertical-align: top;">
                        🔷 Nợ gốc mang sang: <strong>{no_dau_ky_int:,} đ</strong><br>
                        ➕ Tổng phát sinh mới: <strong>{tong_phat_sinh_int:,} đ</strong><br>
                        ➖ Tổng tiền đã trả: <strong style="color: green;">-{tong_da_tra_int:,} đ</strong>
                    </td>
                    <td style="text-align: right; width: 45%; vertical-align: middle;">
                        <div style="border: 2px double #000; padding: 6px; display: inline-block; background-color: #f9f9f9; text-align: center;">
                            <span style="font-weight: bold; font-size: 12px; text-transform: uppercase;">⚪ TỔNG NỢ CUỐI CÙNG:</span><br>
                            <strong style="font-size: 18px; color: #000;">{tong_no_cuoi_ky_int:,} VNĐ</strong>
                        </div>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    """
# Khởi tạo CSDL ban đầu
with sqlite3.connect(DB_FILE) as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS khach_hang (ten TEXT PRIMARY KEY, sdt TEXT, diachi TEXT, nocu REAL DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS lich_su_mua (id INTEGER PRIMARY KEY AUTOINCREMENT, ten_khach TEXT, ngay TEXT, loai_gd TEXT, ten_hang TEXT, dvt TEXT, dongia REAL DEFAULT 0, soluong REAL DEFAULT 0, thanhtien REAL DEFAULT 0)")
    conn.commit()

st.title("🏭 HỆ THỐNG QUẢN LÝ BẠN HÀNG & CÔNG NỢ SƠN TĨNH ĐIỆN")
tab1, tab2 = st.tabs(["👤 CHI TIẾT KHÁCH HÀNG & IN ẤN", "📊 TỔNG HỢP CÔNG NỢ TOÀN XƯỞNG"])

# =============================================================
# TAB 1: CHI TIẾT KHÁCH HÀNG & IN ẤN
# =============================================================
with tab1:
    col_trai, col_phai = st.columns([1, 1.2])
    
    with col_trai:
        st.header("🛠️ Thống Kê & Nhập Liệu")
        
        st.subheader("🚨 Quản trị hệ thống")
        ten_xoa_tuy_chon = st.text_input("Nhập CHÍNH XÁC tên khách muốn xóa bỏ hoàn toàn:", key="xoa_khach_doc_lap")
        xac_nhan_xoa = st.checkbox("⚠️ Tôi chắc chắn muốn xóa toàn bộ lịch sử và công nợ của khách hàng này.", key="chk_xac_nhan")
        
        if st.button("🗑️ BẤM VÀO ĐỂ XÓA SẠCH KHÁCH HÀNG NÀY"):
            if not ten_xoa_tuy_chon.strip():
                st.warning("Vui lòng gõ tên khách hàng vào ô trên trước khi bấm xóa!")
            elif not xac_nhan_xoa:
                st.error("Bạn phải tích chọn ô xác nhận phía trên trước khi thực hiện xóa!")
            else:
                ten_xoa_chuan = " ".join(ten_xoa_tuy_chon.strip().split())
                with sqlite3.connect(DB_FILE) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM khach_hang WHERE ten = ?", (ten_xoa_chuan,))
                    cursor.execute("DELETE FROM lich_su_mua WHERE ten_khach = ?", (ten_xoa_chuan,))
                    conn.commit()
                st.success(f"💥 Đã xóa sạch khách hàng [{ten_xoa_chuan}] khỏi hệ thống!")
                st.rerun()
            
        st.write("---")

        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT ten FROM khach_hang ORDER BY ten ASC")
            cac_khach_hien_co = [row[0] for row in cursor.fetchall()]
        
        danh_sach_chon = ["-- Chọn khách hàng sẵn có --", "➕ THÊM KHÁCH HÀNG MỚI HOÀN TOÀN"] + cac_khach_hien_co
        
        st.subheader("🔍 Chọn Bạn Hàng")
        lua_chon_khach = st.selectbox("Chọn tên khách hàng cần xử lý dữ liệu:", options=danh_sach_chon, index=0)
        
        sdt_mac_dinh, diachi_mac_dinh, nocu_mac_dinh = "", "", 0.0
        khach_cu = False
        ten_chuan_hoa = ""

        if lua_chon_khach != "-- Chọn khách hàng sẵn có --" and lua_chon_khach != "➕ THÊM KHÁCH HÀNG MỚI HOÀN TOÀN":
            ten_chuan_hoa = lua_chon_khach
            khach_cu = True
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT sdt, diachi, nocu FROM khach_hang WHERE ten = ?", (ten_chuan_hoa,))
                row_khach = cursor.fetchone()
            if row_khach:
                sdt_mac_dinh, diachi_mac_dinh, nocu_mac_dinh = row_khach
                st.success(f"🔍 Hệ thống lấy hồ sơ khách cũ: {ten_chuan_hoa}")

        st.subheader("👤 Cập nhật thông tin khách")
        with st.form("form_khach_hang"):
            if lua_chon_khach == "➕ THÊM KHÁCH HÀNG MỚI HOÀN TOÀN":
                ten_khach_form = st.text_input("Gõ tên khách hàng mới:")
            else:
                ten_khach_form = lua_chon_khach

            sdt = st.text_input("Số Điện Thoại:", value=sdt_mac_dinh)
            diachi = st.text_input("Địa chỉ:", value=diachi_mac_dinh)
            
            # Khóa không cho sửa nợ đầu kỳ nếu chọn hồ sơ khách cũ để bảo vệ dữ liệu
            no_dau_ky = st.number_input("Nợ gốc mang sang ban đầu (VNĐ):", value=float(nocu_mac_dinh), step=10000.0, format="%.0f", disabled=khach_cu)
            
            if st.form_submit_button("💾 LƯU THÔNG TIN HỒ SƠ"):
                if ten_khach_form and ten_khach_form != "-- Chọn khách hàng sẵn có --":
                    ten_chuan_hoa_form = " ".join([w.strip() for w in ten_khach_form.strip().split()])
                    
                    with sqlite3.connect(DB_FILE) as conn:
                        cursor = conn.cursor()
                        if khach_cu:
                            cursor.execute("UPDATE khach_hang SET sdt=?, diachi=? WHERE ten=?", (sdt, diachi, ten_chuan_hoa_form))
                        else:
                            cursor.execute("SELECT ten FROM khach_hang WHERE ten=?", (ten_chuan_hoa_form,))
                            if cursor.fetchone():
                                st.error("⚠️ Tên khách hàng này đã tồn tại trên hệ thống!")
                                ten_chuan_hoa_form = ""
                            else:
                                cursor.execute("INSERT INTO khach_hang (ten, sdt, diachi, nocu) VALUES (?, ?, ?, ?)", (ten_chuan_hoa_form, sdt, diachi, no_dau_ky))
                        conn.commit()
                    if ten_chuan_hoa_form:
                        st.success("✅ Đã lưu thông tin khách hàng!")
                        st.rerun()
                else:
                    st.error("⚠️ Vui lòng chọn khách hàng hoặc gõ tên khách mới trước!")
        # Phần ghi nhận giao dịch mới
        if ten_chuan_hoa:
            st.subheader("📝 Giao dịch mới")
            loai_gd = st.radio("Loại giao dịch:", ["Mua hàng", "Khách trả tiền"], horizontal=True, key="loai_gd_radio")
            
            with st.form("form_giao_dich"):
                ngay_gd = st.date_input("Ngày thực hiện:", datetime.date.today()).strftime("%d/%m/%Y")
                
                if loai_gd == "Mua hàng":
                    ten_hang = st.selectbox("Tên hàng / Nội dung công việc:", ["Trắng", "Đen", "Đen Trắng", "Xám đá", "Đen sần", "Đồng sần", "Ghi xanh"])
                    dvt = st.selectbox("Đơn vị tính (ĐVT):", ["kg", "mét", "cái", "Bộ", "lượt"])
                    dongia = st.selectbox("Đơn giá:", [8000.0, 11000.0, 12000.0, 14000.0, 15000.0])
                    soluong = st.number_input("Số lượng mua:", min_value=0.0, step=1.0, value=1.0, format="%.1f")
                    thanh_tien_tam_tinh = int(dongia * soluong)
                    st.markdown(f"👉 **Thành tiền mặt hàng (Dự kiến):** <span style='color:blue; font-size:16px;'>{thanh_tien_tam_tinh:,} VNĐ</span>", unsafe_allow_html=True)
                    tien_tra_kem = st.number_input("Tiền khách trả kèm đơn (nếu có):", min_value=0.0, step=1000.0, format="%.0f")
                else:
                    ten_hang = "Khách trả tiền nợ"
                    dvt = "-"
                    dongia = 0.0
                    soluong = 0.0
                    tien_tra_kem = st.number_input("Số tiền khách trả nợ:", min_value=0.0, step=1000.0, format="%.0f")
                
                if st.form_submit_button("➕ KÍCH LƯU GIAO DỊCH"):
                    hop_le = True  # Đặt biến kiểm soát tiến trình để chặn lỗi lưu trôi lệnh
                    
                    with sqlite3.connect(DB_FILE) as conn:
                        cursor = conn.cursor()
                        if loai_gd == "Mua hàng":
                            thanhtien = dongia * soluong
                            cursor.execute("INSERT INTO lich_su_mua (ten_khach, ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                           (ten_chuan_hoa, ngay_gd, "Bán hàng phát sinh", ten_hang, dvt, dongia, soluong, thanhtien))
                            if tien_tra_kem > 0:
                                cursor.execute("INSERT INTO lich_su_mua (ten_khach, ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                               (ten_chuan_hoa, ngay_gd, "Khách trả tiền mặt/CK", "Khách thanh toán kèm đơn", "-", 0, 0, tien_tra_kem))
                        elif loai_gd == "Khách trả tiền":
                            if tien_tra_kem <= 0:
                                st.error("⚠️ Vui lòng nhập số tiền khách trả lớn hơn 0 đ!")
                                hop_le = False
                            else:
                                cursor.execute("INSERT INTO lich_su_mua (ten_khach, ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                               (ten_chuan_hoa, ngay_gd, "Khách trả tiền mặt/CK", "Khách trả tiền nợ", "-", 0, 0, tien_tra_kem))
                        
                        if hop_le:
                            conn.commit()
                            st.success("✅ Đã ghi sổ giao dịch mới thành công!")
                            st.rerun()

    with col_phai:
        st.header("🖨️ Xem Trước Hóa Đơn Hướng Phôi A4")
        
        st.subheader("⚠️ Sửa lỗi nhập sai")
        ten_khach_can_xoa_dong = st.text_input("Xác nhận tên khách cần xóa dòng giao dịch cuối:", value=ten_chuan_hoa if ten_chuan_hoa else "")
        xac_nhan_xoa_dong = st.checkbox("Tôi đồng ý xóa dòng giao dịch cuối cùng của khách này.", key="chk_xoa_dong_cuoi")
        
        if st.button("🗑️ BẤM VÀO ĐÂY ĐỂ XÓA DÒNG GIAO DỊCH CUỐI CÙNG"):
            if not ten_khach_can_xoa_dong.strip():
                st.error("Vui lòng nhập tên khách cần xóa dòng giao dịch cuối!")
            elif not xac_nhan_xoa_dong:
                st.error("Vui lòng tích chọn ô đồng ý xóa phía trên!")
            else:
                with sqlite3.connect(DB_FILE) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM lich_su_mua WHERE ten_khach = ? ORDER BY id DESC LIMIT 1", (ten_khach_can_xoa_dong.strip(),))
                    row_id = cursor.fetchone()
                    
                    if row_id:
                        cursor.execute("DELETE FROM lich_su_mua WHERE id = ?", (row_id[0],))
                        conn.commit()
                        st.success(f"💥 Đã xóa dòng giao dịch cuối của khách [{ten_khach_can_xoa_dong.strip()}]!")
                        st.rerun()
                    else:
                        st.warning("Không tìm thấy lịch sử giao dịch nào của khách hàng này để xóa.")

        st.write("---")
        if ten_chuan_hoa:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien FROM lich_su_mua WHERE ten_khach = ? ORDER BY id ASC", (ten_chuan_hoa,))
                giao_dich_khach = cursor.fetchall()
            
            rows_html = ""
            stt = 1
            tong_phat_sinh = 0
            tong_da_tra = 0
            
            for gd in giao_dich_khach:
                ngay, loai, ten_h, dvt_h, dg, sl, tt = gd
                dg_int = chuyen_doi_so_an_toan(dg)
                tt_int = chuyen_doi_so_an_toan(tt)
                sl_float = float(sl or 0)
                
                if loai == "Bán hàng phát sinh":
                    tong_phat_sinh += tt_int
                    hien_thi_tt = f"{tt_int:,}"
                    hien_thi_dg = f"{dg_int:,}"
                    
                    if sl_float.is_integer():
                        hien_thi_sl = f"{int(sl_float):,}"
                    else:
                        hien_thi_sl = f"{sl_float:,}"
                else:
                    tong_da_tra += tt_int
                    hien_thi_tt = f"-{tt_int:,}"
                    hien_thi_dg = "-"
                    hien_thi_sl = "-"
                
                rows_html += f"""
                <tr style="height: 24px; text-align: center;">
                    <td style="border: 1px solid #000;">{stt}</td>
                    <td style="border: 1px solid #000;">{ngay}</td>
                    <td style="border: 1px solid #000; text-align: left; padding-left: 5px;">{ten_h}</td>
                    <td style="border: 1px solid #000;">{dvt_h}</td>
                    <td style="border: 1px solid #000; text-align: right; padding-right: 5px;">{hien_thi_dg}</td>
                    <td style="border: 1px solid #000;">{hien_thi_sl}</td>
                    <td style="border: 1px solid #000; text-align: right; padding-right: 5px; font-weight: bold;">{hien_thi_tt}</td>
                </tr>
                """
                stt += 1
            
            tong_no_cuoi_ky = float(nocu_mac_dinh or 0) + tong_phat_sinh - tong_da_tra
            html_content = lay_khung_html_a4(ten_chuan_hoa, sdt_mac_dinh, diachi_mac_dinh, rows_html, nocu_mac_dinh, tong_phat_sinh, tong_da_tra, tong_no_cuoi_ky)
            
            st.subheader("🖨️ Thao tác in")
            # Bảo mật an toàn: Sử dụng json.dumps chống vỡ cấu trúc chuỗi JS khi gặp ký tự ngoặc đơn/kép
            js_safe_html = json.dumps(html_content)
            st.components.v1.html(f"""
                <script>
                    function handlePrint() {{
                        var w = window.open('', '_blank');
                        var htmlData = {js_safe_html};
                        w.document.write(htmlData);
                        w.document.close();
                        w.focus();
                        setTimeout(function() {{ w.print(); w.close(); }}, 500);
                    }}
                </script>
                <button onclick="handlePrint()" style="width: 100%; padding: 12px; font-size: 15px; font-weight: bold; background-color: #1E88E5; color: white; border: none; border-radius: 5px; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    🖨️ KÍCH HOẠT LỆNH IN HÓA ĐƠN A4 (BẤM VÀO ĐÂY)
                </button>
            """, height=60)
            
            st.html(html_content)
        else:
            st.info("Vui lòng chọn khách hàng ở cột trái để hiển thị dữ liệu hóa đơn.")
# =========================================================================
# TAB 2: TỔNG HỢP CÔNG NỢ TOÀN XƯỞNG & XUẤT FILE EXCEL BÁO CÁO 
# =========================================================================
with tab2:
    st.header("📊 Danh Sách Quản Lý Công NỢ Toàn Hệ Thống")
    
    # TỐI ƯU HIỆU NĂNG: Gộp truy vấn SQL qua hàm GROUP BY, tăng tốc độ phần cứng lên gấp 100 lần
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ten, sdt, diachi, nocu FROM khach_hang")
        all_khach = cursor.fetchall()
        
        cursor.execute("""
            SELECT ten_khach, 
                   SUM(CASE WHEN loai_gd = 'Bán hàng phát sinh' THEN thanhtien ELSE 0 END) as phat_sinh,
                   SUM(CASE WHEN loai_gd = 'Khách trả tiền mặt/CK' THEN thanhtien ELSE 0 END) as da_tra
            FROM lich_su_mua 
            GROUP BY ten_khach
        """)
        dict_giao_dich = {row[0]: (row[1], row[2]) for row in cursor.fetchall()}
        
    if all_khach:
        bang_tong_hop = []
        stt_tong = 1

        for k in all_khach:
            k_ten, k_sdt, k_dc, k_nocu = k
            k_phat_sinh, k_da_tra = dict_giao_dich.get(k_ten, (0.0, 0.0))
            k_no_hien_tai = float(k_nocu or 0) + k_phat_sinh - k_da_tra

            bang_tong_hop.append({
                "STT": stt_tong, 
                "Khách Hàng": k_ten, 
                "SĐT": k_sdt if k_sdt else "...", 
                "Địa Chỉ": k_dc if k_dc else "...",
                "Nợ Mang Sang_RAW": int(float(k_nocu or 0)),
                "Phát Sinh Mới_RAW": int(k_phat_sinh),
                "Đã Trả_RAW": int(k_da_tra),
                "Nợ Hiện Tại_RAW": int(k_no_hien_tai)
            })
            stt_tong += 1

        search_all = st.text_input("🔍 Nhập từ khóa lọc nhanh danh sách (Tên / Số điện thoại):", value="", key="search_tab2")
        
        bang_hien_thi = []
        bang_excel_raw = []
        stt_moi = 1
        
        tong_xuong_mang_sang = 0
        tong_xuong_doanh_thu = 0
        tong_xuong_da_tra = 0
        tong_xuong_cong_no_hien_tai = 0

        for row in bang_tong_hop:
            sdt_check = row["SĐT"] if row["SĐT"] else ""
            if search_all.lower() in row["Khách Hàng"].lower() or search_all in sdt_check:
                tong_xuong_mang_sang += row["Nợ Mang Sang_RAW"]
                tong_xuong_doanh_thu += row["Phát Sinh Mới_RAW"]
                tong_xuong_da_tra += row["Đã Trả_RAW"]
                tong_xuong_cong_no_hien_tai += row["Nợ Hiện Tại_RAW"]

                bang_hien_thi.append({
                    "STT": stt_moi, 
                    "Khách Hàng": row["Khách Hàng"], 
                    "SĐT": row["SĐT"], 
                    "Địa Chỉ": row["Địa Chỉ"],
                    "Nợ Mang Sang (đ)": row['Nợ Mang Sang_RAW'],
                    "Phát Sinh Mới (đ)": row['Phát Sinh Mới_RAW'], 
                    "Đã Trả (đ)": row['Đã Trả_RAW'], 
                    "Nợ Hiện Tại (đ)": row['Nợ Hiện Tại_RAW']
                })
                
                bang_excel_raw.append({
                    "STT": stt_moi, 
                    "Khách Hàng": row["Khách Hàng"], 
                    "Số Điện Thoại": "" if row["SĐT"] == "..." else row["SĐT"], 
                    "Địa Chỉ": "" if row["Địa Chỉ"] == "..." else row["Địa Chỉ"],
                    "Nợ Mang Sang (VNĐ)": row["Nợ Mang Sang_RAW"], 
                    "Phát Sinh Mới (VNĐ)": row["Phát Sinh Mới_RAW"], 
                    "Đã Trả (VNĐ)": row["Đã Trả_RAW"], 
                    "Nợ Hiện Tại (VNĐ)": row["Nợ Hiện Tại_RAW"]
                })
                stt_moi += 1

        st.markdown("### 🏪 Thống Kê Dòng Tiền Theo Bộ Lọc")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(label="💰 TỔNG DOANH THU PHÁT SINH", value=f"{int(tong_xuong_doanh_thu):,} VNĐ")
        with col2:
            st.metric(label="🛑 TỔNG CÔNG NỢ ĐANG BỊ ĐỌNG", value=f"{int(tong_xuong_cong_no_hien_tai):,} VNĐ", delta="Khách chưa trả", delta_color="inverse")
        with col3:
            st.metric(label="✅ TỔNG TIỀN MẶT / CK ĐÃ THU", value=f"{int(tong_xuong_da_tra):,} VNĐ")
            
        st.write("---") 

        if bang_hien_thi:
            bang_hien_thi.append({
                "STT": "Tổng",
                "Khách Hàng": "TOÀN HỆ THỐNG",
                "SĐT": "-",
                "Địa Chỉ": "-",
                "Nợ Mang Sang (đ)": int(tong_xuong_mang_sang),
                "Phát Sinh Mới (đ)": int(tong_xuong_doanh_thu),
                "Đã Trả (đ)": int(tong_xuong_da_tra),
                "Nợ Hiện Tại (đ)": int(tong_xuong_cong_no_hien_tai)
            })
            
            # GIẢI PHÁP GIAO DIỆN: Đổi sang st.dataframe để có thanh cuộn và tự động ngăn cách hàng nghìn
            df_view = pd.DataFrame(bang_hien_thi)
            st.dataframe(
                df_view, 
                use_container_width=True,
                column_config={
                    "Nợ Mang Sang (đ)": st.column_config.NumberColumn(format="%d đ"),
                    "Phát Sinh Mới (đ)": st.column_config.NumberColumn(format="%d đ"),
                    "Đã Trả (đ)": st.column_config.NumberColumn(format="%d đ"),
                    "Nợ Hiện Tại (đ)": st.column_config.NumberColumn(format="%d đ"),
                }
            )
            
            st.write("---")
            st.subheader("📥 Xuất dữ liệu báo cáo")
            
            bang_excel_raw.append({
                "STT": "Tổng",
                "Khách Hàng": "TOÀN HỆ THỐNG",
                "Số Điện Thoại": "-",
                "Địa Chỉ": "-",
                "Nợ Mang Sang (VNĐ)": int(tong_xuong_mang_sang),
                "Phát Sinh Mới (VNĐ)": int(tong_xuong_doanh_thu),
                "Đã Trả (VNĐ)": int(tong_xuong_da_tra),
                "Nợ Hiện Tại (VNĐ)": int(tong_xuong_cong_no_hien_tai)
            })
            
            df = pd.DataFrame(bang_excel_raw)
            
            def convert_df_to_excel(df_data):
                output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                    df_data.to_excel(writer, index=False, sheet_name='Bao_Cao_Cong_No')
                return output.getvalue()
                
            excel_data = convert_df_to_excel(df)
            ngay_tai_file = datetime.datetime.now().strftime("%d/%m/%Y")
            
            st.download_button(
                label="📥 XUẤT FILE EXCEL BÁO CÁO CÔNG NỢ THEO BỘ LỌC",
                data=excel_data,
                file_name=f"Bao_Cao_Cong_No_Loc_{ngay_tai_file}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        else:
            st.warning("Không khớp với bất kỳ thông tin bạn hàng nào.")
    else:
        st.info("Hệ thống dữ liệu trống. Hãy thêm khách hàng mới ở Tab 1.")
