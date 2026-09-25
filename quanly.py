import os
import sqlite3
import datetime
import streamlit as st

# Cấu hình giao diện Streamlit rộng rãi toàn màn hình
st.set_page_config(page_title="Hệ Thống Quản Lý Sơn Tĩnh Điện", layout="wide")

# =============================================================
# 1. CẤU HÌNH HỆ THỐNG & THÔNG TIN CƠ SỞ
# =============================================================
DB_FILE = "dulieu_son_tinh_dien.db"  # Đã tối ưu không dấu tránh lỗi hệ thống
TEN_CO_SO = "XƯỞNG SƠN TĨNH ĐIỆN HƯỞNG THỦY"
SDT_CHU_XUONG = "0979.141.588...0354.179.792"
DIA_CHI_XUONG = "Tân Lập Hợp Lý Phú Thọ"
STK_NGAN_HANG = "104869545034...0979141588"
TEN_NGAN_HANG = "VietinBank - CN VINH PHUC"
TEN_CHU_TK = "LE VAN HUONG"
def lay_khung_html_a4(ten_chuan_hoa, sdt, diachi, rows_html, no_dau_ky, tong_phat_sinh, tong_da_tra, tong_no_cuoi_ky):
    ngay_lap_he_thong = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    no_dau_ky_int = int(no_dau_ky or 0)
    tong_phat_sinh_int = int(tong_phat_sinh or 0)
    tong_da_tra_int = int(tong_da_tra or 0)
    tong_no_cuoi_ky_int = int(tong_no_cuoi_ky or 0)
    
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
# =============================================================
# 2. KHỞI TẠO CƠ SỞ DỮ LIỆU & ĐIỀU HƯỚNG GIAO DIỆN
# =============================================================
with sqlite3.connect(DB_FILE) as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS khach_hang (ten TEXT PRIMARY KEY, sdt TEXT, diachi TEXT, nocu REAL DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS lich_su_mua (id INTEGER PRIMARY KEY AUTOINCREMENT, ten_khach TEXT, ngay TEXT, loai_gd TEXT, ten_hang TEXT, dvt TEXT, dongia REAL DEFAULT 0, soluong REAL DEFAULT 0, thanhtien REAL DEFAULT 0)")
    conn.commit()

st.title("🏭 HỆ THỐNG QUẢN LÝ BẠN HÀNG & CÔNG NỢ SƠN TĨNH ĐIỆN")
tab1, tab2 = st.tabs(["👤 CHI TIẾT KHÁCH HÀNG & IN ẤN", "📊 TỔNG HỢP CÔNG NỢ TOÀN XƯỞNG"])

with tab1:
    col_trai, col_phai = st.columns([1, 1.2])
    
    with col_trai:
        st.header("🛠️ Thống Kê & Nhập Liệu")
        
        # Nút xóa tài khoản khách hàng đưa lên đầu cột trái lộ diện rõ ràng
        st.subheader("🚨 Quản trị hệ thống")
        ten_xoa_tuy_chon = st.text_input("Nhập CHÍNH XÁC tên khách muốn xóa bỏ hoàn toàn:", key="xoa_khach_doc_lap")
        
        # Thêm hộp kiểm xác nhận an toàn dữ liệu
        xac_nhan_xoa = st.checkbox("⚠️ Tôi chắc chắn muốn xóa toàn bộ lịch sử và công nợ của khách hàng này.", key="chk_xac_nhan")
        
        if st.button("🗑️ BẤM VÀO ĐỂ XÓA SẠCH KHÁCH HÀNG NÀY"):
            if not ten_xoa_tuy_chon.strip():
                st.warning("Vui lòng gõ tên khách hàng vào ô trên trước khi bấm xóa!")
            elif not xac_nhan_xoa:
                st.error("Bạn phải tích chọn ô xác nhận phía trên trước khi thực hiện xóa!")
            else:
                with sqlite3.connect(DB_FILE) as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM khach_hang WHERE TRIM(LOWER(ten)) = TRIM(LOWER(?))", (ten_xoa_tuy_chon.strip(),))
                    cursor.execute("DELETE FROM lich_su_mua WHERE TRIM(LOWER(ten_khach)) = TRIM(LOWER(?))", (ten_xoa_tuy_chon.strip(),))
                    conn.commit()
                
                st.session_state["thong_bao_xoa"] = f"💥 Đã xóa sạch khách hàng [{ten_xoa_tuy_chon.strip()}] khỏi hệ thống!"
                st.rerun()
                
        if "thong_bao_xoa" in st.session_state:
            st.error(st.session_state.pop("thong_bao_xoa"))
            
        st.write("---")

        ten_nhap_raw = st.text_input("Gõ tên khách hàng để tra cứu:", value="tuyển k1")
        ten_chuan_hoa = " ".join([w.strip() for w in ten_nhap_raw.strip().split()])
        
        sdt_mac_dinh, diachi_mac_dinh, nocu_mac_dinh = "", "", 0.0
        khach_cu = False

        if ten_chuan_hoa:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT ten, sdt, diachi, nocu FROM khach_hang WHERE TRIM(LOWER(ten)) = TRIM(LOWER(?))", (ten_chuan_hoa,))
                row_khach = cursor.fetchone()
            if row_khach:
                ten_chuan_hoa, sdt_mac_dinh, diachi_mac_dinh, nocu_mac_dinh = row_khach
                khach_cu = True
                st.success(f"🔍 Hệ thống tìm thấy khách cũ: {ten_chuan_hoa}")
            else:
                st.info(f"🆕 Chuẩn bị tạo hồ sơ khách mới: {ten_chuan_hoa}")
        st.subheader("👤 Cập nhật thông tin khách")
        with st.form("form_khach_hang"):
            sdt = st.text_input("Số Điện Thoại:", value=sdt_mac_dinh)
            diachi = st.text_input("Địa chỉ:", value=diachi_mac_dinh)
            no_dau_ky = st.number_input("Nợ gốc mang sang ban đầu (VNĐ):", value=float(nocu_mac_dinh), step=10000.0, format="%.0f")
            
            if st.form_submit_button("💾 LƯU THÔNG TIN HỒ SƠ"):
                if ten_chuan_hoa:
                    with sqlite3.connect(DB_FILE) as conn:
                        cursor = conn.cursor()
                        if khach_cu:
                            cursor.execute("UPDATE khach_hang SET sdt=?, diachi=?, nocu=? WHERE TRIM(LOWER(ten))=TRIM(LOWER(?))", (sdt, diachi, no_dau_ky, ten_chuan_hoa))
                        else:
                            cursor.execute("INSERT INTO khach_hang (ten, sdt, diachi, nocu) VALUES (?, ?, ?, ?)", (ten_chuan_hoa, sdt, diachi, no_dau_ky))
                        conn.commit()
                    st.success("✅ Đã lưu thông tin khách hàng!")
                    st.rerun()
                else:
                    st.error("⚠️ Vui lòng gõ tên khách hàng ở ô tra cứu trước!")

        if ten_chuan_hoa:
            st.subheader("📝 Giao dịch mới")
            with st.form("form_giao_dich"):
                loai_gd = st.radio("Loại giao dịch:", ["Mua hàng", "Khách trả tiền"], horizontal=True)
                ngay_gd = st.date_input("Ngày thực hiện:", datetime.date.today()).strftime("%d/%m/%Y")
                ten_hang = st.text_input("Tên hàng / Nội dung công việc:", value="Sơn gia công tĩnh điện")
                
                # SỬA LỖI: Chuyển thành text_input trực tiếp trong form giúp điền ĐVT nhanh gọn mà không bị đơ giao diện
                dvt = st.text_input("Đơn vị tính (ĐVT):", value="Bộ", help="Gõ Bộ, Bộ kđ, kg, Cái... tùy ý")
                
                if loai_gd == "Mua hàng":
                    dongia = st.number_input("Đơn giá:", min_value=0.0, step=1000.0, format="%.0f")
                    soluong = st.number_input("Số lượng mua:", min_value=0.0, step=1.0, value=1.0, format="%.1f")
                    tien_tra_kem = st.number_input("Tiền khách trả (nếu có):", min_value=0.0, step=1000.0, format="%.0f")
                else:
                    dongia = 0.0
                    soluong = 0.0
                    tien_tra_kem = st.number_input("Số tiền khách trả nợ:", min_value=0.0, step=1000.0, format="%.0f")
                
                if st.form_submit_button("➕ KÍCH LƯU GIAO DỊCH"):
                    if loai_gd == "Khách trả tiền" and tien_tra_kem <= 0:
                        st.error("⚠️ Vui lòng nhập số tiền khách trả lớn hơn 0 đ!")
                    else:
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
                                cursor.execute("INSERT INTO lich_su_mua (ten_khach, ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                                               (ten_chuan_hoa, ngay_gd, "Khách trả tiền mặt/CK", "Khách trả tiền nợ", "-", 0, 0, tien_tra_kem))
                            conn.commit()
                        st.success("✅ Đã ghi sổ và cân trừ công nợ thành công!")
                        st.rerun()
    with col_phai:
        st.header("🖨️ Xem Trước Hóa Đơn Hướng Phôi A4")
        
        # Nút xóa dòng giao dịch nhập sai đưa lên đầu cột phải lộ diện rõ ràng
        st.subheader("⚠️ Sửa lỗi nhập sai")
        ten_khach_can_xoa_dong = st.text_input("Xác nhận tên khách cần xóa dòng giao dịch cuối:", value=ten_chuan_hoa if ten_chuan_hoa else "")
        if st.button("🗑️ BẤM VÀO ĐÂY ĐỂ XÓA DÒNG GIAO DỊCH CUỐI CÙNG"):
            if ten_khach_can_xoa_dong.strip():
                with sqlite3.connect(DB_FILE) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT id FROM lich_su_mua WHERE TRIM(LOWER(ten_khach)) = TRIM(LOWER(?)) ORDER BY id DESC LIMIT 1", (ten_khach_can_xoa_dong.strip(),))
                    last_row = cursor.fetchone()
                    if last_row:
                        # SỬA LỖI CRASH: Trích xuất phần tử số nguyên đầu tiên của bộ tuple
                        cursor.execute("DELETE FROM lich_su_mua WHERE id = ?", (last_row[0],))
                        conn.commit()
                        st.success(f"✅ Đã hủy bỏ thành công dòng dữ liệu cuối của khách {ten_khach_can_xoa_dong}!")
                        st.rerun()
                    else:
                        st.warning("Khách hàng này hiện chưa có dòng giao dịch nào để xóa!")
            else:
                st.warning("Vui lòng nhập hoặc chọn tên khách hàng cần xóa dòng!")
        st.write("---")

        if ten_chuan_hoa:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien FROM lich_su_mua WHERE ten_khach = ? ORDER BY id ASC", (ten_chuan_hoa,))
                rows = cursor.fetchall()

            rows_html = ""
            tong_phat_sinh = 0
            tong_da_tra = 0
            stt = 1

            for row in rows:
                r_id, r_ngay, r_loai, r_hang, r_dvt, r_gia, r_sl, r_tien = row
                # SỬA LỖI: Đã bổ sung thuộc tính border cho tất cả ô td đảm bảo in hóa đơn ra lưới kẻ
                if r_loai == "Bán hàng phát sinh":
                    tong_phat_sinh += r_tien
                    rows_html += f"""
                    <tr style="height: 24px;">
                        <td style="text-align:center; border: 1px solid #000;">{stt}</td>
                        <td style="text-align:center; border: 1px solid #000;">{r_ngay}</td>
                        <td style="padding-left: 5px; border: 1px solid #000;">{r_hang}</td>
                        <td style="text-align:center; border: 1px solid #000;">{r_dvt}</td>
                        <td style="text-align:right; padding-right: 5px; border: 1px solid #000;">{int(r_gia):,}</td>
                        <td style="text-align:center; border: 1px solid #000;">{r_sl}</td>
                        <td style="text-align:right; padding-right: 5px; border: 1px solid #000;">{int(r_tien):,}</td>
                    </tr>
                    """
                else:
                    tong_da_tra += r_tien
                    rows_html += f"""
                    <tr style="height: 24px; background-color: #f9fffb;">
                        <td style="text-align:center; border: 1px solid #000;">{stt}</td>
                        <td style="text-align:center; border: 1px solid #000;">{r_ngay}</td>
                        <td style="padding-left: 5px; color: green; font-weight: bold; border: 1px solid #000;">💵 {r_hang}</td>
                        <td style="text-align:center; border: 1px solid #000;">-</td>
                        <td style="text-align:right; padding-right: 5px; border: 1px solid #000;">-</td>
                        <td style="text-align:center; border: 1px solid #000;">-</td>
                        <td style="text-align:right; padding-right: 5px; color: green; font-weight: bold; border: 1px solid #000;">-{int(r_tien):,}</td>
                    </tr>
                    """
                stt += 1

            tong_no_cuoi_ky = no_dau_ky + tong_phat_sinh - tong_da_tra

            html_content = lay_khung_html_a4(ten_chuan_hoa, sdt, diachi, rows_html, no_dau_ky, tong_phat_sinh, tong_da_tra, tong_no_cuoi_ky)
            
            st.subheader("🖨️ Thao tác in")
            # SỬA LỖI: Xử lý chuỗi xuống dòng chống đơ nút lệnh in JavaScript
            js_safe_html = html_content.replace("`", "\\`").replace("\n", "\\n").replace("\r", "")
            st.components.v1.html(f"""
                <script>
                    function handlePrint() {{
                        var w = window.open();
                        w.document.write(`{js_safe_html}`);
                        w.document.close();
                        w.focus();
                        setTimeout(function() {{ w.print(); w.close(); }}, 200);
                    }}
                </script>
                <button onclick="handlePrint()" style="width: 100%; padding: 12px; font-size: 15px; font-weight: bold; background-color: #1E88E5; color: white; border: none; border-radius: 5px; cursor: pointer; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                    🖨️ KÍCH HOẠT LỆNH IN HÓA ĐƠN A4 (BẤM VÀO ĐÂY)
                </button>
            """, height=60)
            
            st.html(html_content)
        else:
            st.info("Nhập tên khách hàng ở cột trái để trích xuất dữ liệu hóa đơn.")

with tab2:
    st.header("📊 Danh Sách Quản Lý Công Nợ Toàn Hệ Thống")
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT ten, sdt, diachi, nocu FROM khach_hang")
        all_khach = cursor.fetchall()
        
    if all_khach:
        search_all = st.text_input("🔍 Nhập từ khóa lọc nhanh danh sách (Tên / Số điện thoại):", value="")
        bang_tong_hop = []
        stt_tong = 1
        
        for k in all_khach:
            k_ten, k_sdt, k_dc, k_nocu = k
            if search_all.lower() in k_ten.lower() or search_all in (k_sdt or ""):
                with sqlite3.connect(DB_FILE) as conn:
                    cursor = conn.cursor()
                    cursor.execute("SELECT loai_gd, thanhtien FROM lich_su_mua WHERE ten_khach = ?", (k_ten,))
                    k_giao_dich = cursor.fetchall()
                
                # SỬA LỖI TÍNH TOÁN: Phân rã chuẩn tuple (loai_gd, tien) để hàm sum hoạt động đúng thực tế
                k_phat_sinh = sum(float(tien) for loai_gd, tien in k_giao_dich if loai_gd == "Bán hàng phát sinh")
                k_da_tra = sum(float(tien) for loai_gd, tien in k_giao_dich if loai_gd != "Bán hàng phát sinh")
                k_no_hien_tai = k_nocu + k_phat_sinh - k_da_tra
                
                bang_tong_hop.append({
                    "STT": stt_tong, "Khách Hàng": k_ten, "SĐT": k_sdt if k_sdt else "...", "Địa Chỉ": k_dc if k_dc else "...",
                    "Nợ Mang Sang (đ)": f"{int(k_nocu):,}", "Phát Sinh Mới (đ)": f"{int(k_phat_sinh):,}", "Đã Trả (đ)": f"{int(k_da_tra):,}", "Nợ Hiện Tại (đ)": f"{int(k_no_hien_tai):,}"
                })
                stt_tong += 1
                
        if bang_tong_hop:
            st.table(bang_tong_hop)
        else:
            st.warning("Không khớp với bất kỳ thông tin bạn hàng nào.")
    else:
        st.info("Hệ thống dữ liệu trống. Hãy thêm khách hàng mới ở Tab 1.")
