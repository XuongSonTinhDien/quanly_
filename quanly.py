import os
import psycopg2
import datetime
import streamlit as st
import pandas as pd

# Cấu hình giao diện Streamlit rộng rãi toàn màn hình
st.set_page_config(page_title="Hệ Thống Quản Lý Sơn Tĩnh Điện", layout="wide")

# =============================================================
# 1. CẤU HÌNH CLOUD DATABASE TRỰC TUYẾN MIỄN PHÍ
# =============================================================
DB_URL = "postgresql://postgres:Huong1985%40%40123@db.hyatrmkculrugytuvzeg.supabase.co:5432/postgres"
TEN_CO_SO = "XƯỞNG SƠN TĨNH ĐIỆN HƯỞNG THỦY"
SDT_CHU_XUONG = "0979.141.588...0354.179.792"
DIA_CHI_XUONG = "Tân Lập Hợp Lý Phú Thọ"
STK_NGAN_HANG = "104869545034...0979141588"
TEN_NGAN_HANG = "VietinBank - CN VINH PHUC"
TEN_CHU_TK = "LE VAN HUONG"
def lay_khung_html_a4(ten_chuan_hoa, sdt, diachi, rows_html, no_dau_ky, tong_phat_sinh, tong_da_tra, tong_no_cuoi_ky):
    ngay_lap_he_thong = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    no_dau_ky_int = int(float(no_dau_ky or 0))
    tong_phat_sinh_int = int(float(tong_phat_sinh or 0))
    tong_da_tra_int = int(float(tong_da_tra or 0))
    tong_no_cuoi_ky_int = int(float(tong_no_cuoi_ky or 0))
    
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

st.title("🏭 HỆ THỐNG QUẢN LÝ BẠN HÀNG & CÔNG NỢ SƠN TĨNH ĐIỆN CLOUD")
tab1, tab2 = st.tabs(["👤 CHI TIẾT KHÁCH HÀNG & IN ẤN", "📊 TỔNG HỢP CÔNG NỢ TOÀN XƯỞNG"])
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
                with psycopg2.connect(DB_URL) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("DELETE FROM khach_hang WHERE ten = %s", (ten_xoa_chuan,))
                        cursor.execute("DELETE FROM lich_su_mua WHERE ten_khach = %s", (ten_xoa_chuan,))
                        conn.commit()
                st.success(f"💥 Đã xóa sạch khách hàng [{ten_xoa_chuan}] khỏi hệ thống trực tuyến!")
                st.rerun()
            
        st.write("---")

        # Tải danh sách tên khách hàng trực tuyến tự động vượt phân quyền chặn bảo mật mạng
        cac_khach_hien_co = []
        try:
            with psycopg2.connect(DB_URL) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT DISTINCT ten FROM khach_hang ORDER BY ten ASC")
                    rows = cursor.fetchall()
                    for r in rows:
                        t_name = r[0] if isinstance(r, (tuple, list)) else r
                        if t_name not in danh_sach_khach_chuan:
                            cac_khach_hien_co.append(t_name)
        except Exception as e:
            pass
        
        danh_sach_chon = ["-- Chọn khách hàng sẵn có --", "➕ THÊM KHÁCH HÀNG MỚI HOÀN TOÀN"] + cac_khach_hien_co
        st.subheader("🔍 Chọn Bạn Hàng")
        lua_chon_khach = st.selectbox("Chọn tên khách hàng cần xử lý dữ liệu:", options=danh_sach_chon, index=0)
        
        ten_chuan_hoa = ""
        sdt_mac_dinh, diachi_mac_dinh, nocu_mac_dinh = "", "", 0.0
        khach_cu = False

        if lua_chon_khach == "➕ THÊM KHÁCH HÀNG MỚI HOÀN TOÀN":
            ten_nhap_raw = st.text_input("Gõ tên khách hàng mới vào đây:")
            ten_chuan_hoa = " ".join([w.strip() for w in ten_nhap_raw.strip().split()])
            if ten_chuan_hoa:
                st.info(f"🆕 Chuẩn bị tạo hồ sơ khách mới: {ten_chuan_hoa}")
        elif lua_chon_khach != "-- Chọn khách hàng sẵn có --" and lua_chon_khach is not None:
            ten_chuan_hoa = lua_chon_khach
            with psycopg2.connect(DB_URL) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT ten, sdt, diachi, nocu FROM khach_hang WHERE ten = %s", (ten_chuan_hoa,))
                    row_khach = cursor.fetchone()
            if row_khach:
                _, sdt_mac_dinh, diachi_mac_dinh, nocu_mac_dinh = row_khach
                khach_cu = True
                st.success(f"🔍 Đã lấy hồ sơ đám mây của khách cũ: {ten_chuan_hoa}")

        st.subheader("👤 Cập nhật thông tin khách")
        with st.form("form_khach_hang"):
            sdt = st.text_input("Số Điện Thoại:", value=sdt_mac_dinh)
            diachi = st.text_input("Địa chỉ:", value=diachi_mac_dinh)
            no_dau_ky = st.number_input("Nợ gốc mang sang ban đầu (VNĐ):", value=float(nocu_mac_dinh), step=10000.0, format="%.0f")
            
            if st.form_submit_button("💾 LƯU THÔNG TIN HỒ SƠ LÊN CLOUD"):
                if ten_chuan_hoa:
                    with psycopg2.connect(DB_URL) as conn:
                        with conn.cursor() as cursor:
                            if khach_cu:
                                cursor.execute("UPDATE khach_hang SET sdt=%s, diachi=%s, nocu=%s WHERE ten=%s", (sdt, diachi, no_dau_ky, ten_chuan_hoa))
                            else:
                                cursor.execute("INSERT INTO khach_hang (ten, sdt, diachi, nocu) VALUES (%s, %s, %s, %s)", (ten_chuan_hoa, sdt, diachi, no_dau_ky))
                            conn.commit()
                    st.success("✅ Đã cập nhật hồ sơ lưu trữ trực tuyến thành công!")
                    st.rerun()
                else:
                    st.error("⚠️ Vui lòng chọn khách hàng hoặc gõ tên khách mới trước!")
        if ten_chuan_hoa:
            st.subheader("📝 Giao dịch mới")
            with st.form("form_giao_dich"):
                loai_gd = st.radio("Loại giao dịch:", ["Mua hàng", "Khách trả tiền"], horizontal=True)
                ngay_gd = st.date_input("Ngày thực hiện:", datetime.date.today()).strftime("%d/%m/%Y")
                ten_hang = st.text_input("Tên hàng / Nội dung công việc:", value="Sơn gia công tĩnh điện")
                dvt = st.selectbox("Đơn vị tính (ĐVT):", ["kg", "mét", "cái", "Bộ", "lượt"])
                
                if loai_gd == "Mua hàng":
                    dongia = st.number_input("Đơn giá:", min_value=0.0, step=1000.0, format="%.0f", value=15000.0)
                    soluong = st.number_input("Số lượng mua:", min_value=0.0, step=1.0, value=1.0, format="%.1f")
                    thanh_tien_tam_tinh = int(dongia * soluong)
                    st.markdown(f"👉 **Thành tiền mặt hàng (Tự động nhân tính):** <span style='color:blue; font-size:16px;'>{thanh_tien_tam_tinh:,} VNĐ</span>", unsafe_allow_html=True)
                    tien_tra_kem = st.number_input("Tiền khách trả kèm đơn (nếu có):", min_value=0.0, step=1000.0, format="%.0f")
                else:
                    dongia = 0.0
                    soluong = 0.0
                    tien_tra_kem = st.number_input("Số tiền khách trả nợ:", min_value=0.0, step=1000.0, format="%.0f")
                
                if st.form_submit_button("➕ KÍCH LƯU GIAO DỊCH"):
                    with psycopg2.connect(DB_URL) as conn:
                        with conn.cursor() as cursor:
                            if loai_gd == "Mua hàng":
                                thanhtien = dongia * soluong
                                cursor.execute("INSERT INTO lich_su_mua (ten_khach, ngay, loai_gd, text_hang, dvt, dongia, soluong, thanhtien) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (ten_chuan_hoa, ngay_gd, "Bán hàng phát sinh", ten_hang, dvt, dongia, soluong, thanhtien))
                                if tien_tra_kem > 0:
                                    cursor.execute("INSERT INTO lich_su_mua (ten_khach, ngay, loai_gd, text_hang, dvt, dongia, soluong, thanhtien) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (ten_chuan_hoa, ngay_gd, "Khách trả tiền mặt/CK", "Khách thanh toán kèm đơn", "-", 0, 0, tien_tra_kem))
                            elif loai_gd == "Khách trả tiền":
                                if tien_tra_kem <= 0:
                                    st.error("⚠️ Vui lòng nhập số tiền khách trả lớn hơn 0 đ!")
                                else:
                                    cursor.execute("INSERT INTO lich_su_mua (ten_khach, ngay, loai_gd, text_hang, dvt, dongia, soluong, thanhtien) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (ten_chuan_hoa, ngay_gd, "Khách trả tiền mặt/CK", "Khách trả tiền nợ", "-", 0, 0, tien_tra_kem))
                            conn.commit()
                    st.success("✅ Đã ghi sổ đám mây trực tuyến thành công!")
                    st.rerun()

    with col_phai:
        st.header("🖨️ Xem Trước Hóa Đơn Hướng Phôi A4")
        st.subheader("⚠️ Sửa lỗi nhập sai")
        ten_khach_can_xoa_dong = st.text_input("Xác nhận tên khách cần xóa dòng giao dịch cuối:", value=ten_chuan_hoa if ten_chuan_hoa else "")
        if st.button("🗑️ BẤM VÀO ĐÂY ĐỂ XÓA DÒNG GIAO DỊCH CUỐI CÙNG"):
            if ten_khach_can_xoa_dong.strip():
                with psycopg2.connect(DB_URL) as conn:
                    with conn.cursor() as cursor:
                        cursor.execute("SELECT id FROM lich_su_mua WHERE ten_khach = %s ORDER BY id DESC LIMIT 1", (ten_khach_can_xoa_dong.strip(),))
                        row_id = cursor.fetchone()
                        if row_id:
                            cursor.execute("DELETE FROM lich_su_mua WHERE id = %s", (row_id,))
                            conn.commit()
                            st.success(f"💥 Đã xóa dòng giao dịch cuối trên Cloud!")
                            st.rerun()
            else:
                st.error("Vui lòng nhập tên khách cần xóa dòng giao dịch cuối!")

        st.write("---")
        if ten_chuan_hoa:
            with psycopg2.connect(DB_URL) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT ngay, loai_gd, text_hang, dvt, dongia, soluong, thanhtien FROM lich_su_mua WHERE ten_khach = %s ORDER BY id ASC", (ten_chuan_hoa,))
                    giao_dich_khach = cursor.fetchall()
            rows_html = ""
            stt = 1
            tong_phat_sinh = 0
            tong_da_tra = 0
            for gd in giao_dich_khach:
                ngay, loai, text_h, dvt_h, dg, sl, tt = gd
                dg_int = int(float(dg or 0))
                tt_int = int(float(tt or 0))
                sl_float = float(sl or 0)
                if loai == "Bán hàng phát sinh":
                    tong_phat_sinh += tt_int
                    hien_thi_tt = f"{tt_int:,}"
                    hien_thi_dg = f"{dg_int:,}"
                    hien_thi_sl = f"{int(sl_float):,}" if sl_float.is_integer() else f"{sl_float:,}"
                else:
                    tong_da_tra += tt_int
                    hien_thi_tt = f"-{tt_int:,}"
                    hien_thi_dg = "-"
                    hien_thi_sl = "-"
                rows_html += f"""
                <tr style="height: 24px; text-align: center;">
                    <td style="border: 1px solid #000;">{stt}</td>
                    <td style="border: 1px solid #000;">{ngay}</td>
                    <td style="border: 1px solid #000; text-align: left; padding-left: 5px;">{text_h}</td>
                    <td style="border: 1px solid #000;">{dvt_h}</td>
                    <td style="border: 1px solid #000; text-align: right; padding-right: 5px;">{hien_thi_dg}</td>
                    <td style="border: 1px solid #000;">{hien_thi_sl}</td>
                    <td style="border: 1px solid #000; text-align: right; padding-right: 5px; font-weight: bold;">{hien_thi_tt}</td>
                </tr>
                """
                stt += 1
            tong_no_cuoi_ky = float(nocu_mac_dinh) + tong_phat_sinh - tong_da_tra
            html_content = lay_khung_html_a4(ten_chuan_hoa, sdt_mac_dinh, diachi_mac_dinh, rows_html, nocu_mac_dinh, tong_phat_sinh, tong_da_tra, tong_no_cuoi_ky)
            st.subheader("🖨️ Thao tác in")
            js_safe_html = html_content.replace("`", "\\`").replace("\n", "\\n").replace("\r", "")
            st.components.v1.html(f"""
                <script>
                    function handlePrint() {{
                        var w = window.open('', '_blank'); w.document.write(`{js_safe_html}`); w.document.close(); w.focus();
                        setTimeout(function() {{ w.print(); w.close(); }}, 500);
                    }}
                </script>
                <button onclick="handlePrint()" style="width: 100%; padding: 12px; font-size: 15px; font-weight: bold; background-color: #1E88E5; color: white; border: none; border-radius: 5px; cursor: pointer;">🖨️ KÍCH HOẠT LỆNH IN HÓA ĐƠN A4</button>
            """, height=60)
            st.html(html_content)
with tab2:
    st.header("📊 Danh Sách Quản Lý Công NỢ Toàn Hệ Thống")
    with psycopg2.connect(DB_URL) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT ten, sdt, diachi, nocu FROM khach_hang")
            all_khach = cursor.fetchall()
    if all_khach:
        bang_tong_hop = []
        stt_tong = 1
        for k in all_khach:
            k_ten, k_sdt, k_dc, k_nocu = k
            with psycopg2.connect(DB_URL) as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT loai_gd, thanhtien FROM lich_su_mua WHERE ten_khach = %s", (k_ten,))
                    k_giao_dich = cursor.fetchall()
            k_phat_sinh = sum([float(t or 0) for l, t in k_giao_dich if l == "Bán hàng phát sinh"])
            k_da_tra = sum([float(t or 0) for l, t in k_giao_dich if l == "Khách trả tiền mặt/CK"])
            k_no_hien_tai = float(k_nocu or 0) + k_phat_sinh - k_da_tra
            bang_tong_hop.append({"STT": stt_tong, "Khách Hàng": k_ten, "SĐT": k_sdt if k_sdt else "...", "Địa Chỉ": k_dc if k_dc else "...", "Nợ Mang Sang_RAW": int(float(k_nocu)), "Phát Sinh Mới_RAW": int(k_phat_sinh), "Đã Trả_RAW": int(k_da_tra), "Nợ Hiện Tại_RAW": int(k_no_hien_tai)})
            stt_tong += 1
        search_all = st.text_input("🔍 Nhập từ khóa lọc nhanh danh sách (Tên / Số điện thoại):", value="", key="search_tab2")
        bang_hien_thi = []
        bang_excel_raw = []
        stt_moi = 1
        tong_xuong_mang_sang = tong_xuong_doanh_thu = tong_xuong_da_tra = tong_xuong_cong_no_hien_tai = 0
        for row in bang_tong_hop:
            sdt_check = row["SĐT"] if row["SĐT"] else ""
            if search_all.lower() in row["Khách Hàng"].lower() or search_all in sdt_check:
                tong_xuong_mang_sang += row["Nợ Mang Sang_RAW"]; tong_xuong_doanh_thu += row["Phát Sinh Mới_RAW"]; tong_xuong_da_tra += row["Đã Trả_RAW"]; tong_xuong_cong_no_hien_tai += row["Nợ Hiện Tại_RAW"]
                bang_hien_thi.append({"STT": stt_moi, "Khách Hàng": row["Khách Hàng"], "SĐT": row["SĐT"], "Địa Chỉ": row["Địa Chỉ"], "Nợ Mang Sang (đ)": f"{row['Nợ Mang Sang_RAW']:,}", "Phát Sinh Mới (đ)": f"{row['Phát Sinh Mới_RAW']:,}", "Đã Trả (đ)": f"{row['Đã Trả_RAW']:,}", "Nợ Hiện Tại (đ)": f"{row['Nợ Hiện Tại_RAW']:,}"})
                bang_excel_raw.append({"STT": stt_moi, "Khách Hàng": row["Khách Hàng"], "Số Điện Thoại": "" if row["SĐT"] == "..." else row["SĐT"], "Địa Chỉ": "" if row["Địa Chỉ"] == "..." else row["Địa Chỉ"], "Nợ Mang Sang (VNĐ)": row["Nợ Mang Sang_RAW"], "Phát Sinh Mới (VNĐ)": row["Phát Sinh Mới_RAW"], "Đã Trả (VNĐ)": row["Đã Trả_RAW"], "Nợ Hiện Tại (VNĐ)": row["Nợ Hiện Tại_RAW"]})
                stt_moi += 1
        st.markdown("### 🏪 Thống Kê Dòng Tiền Theo Bộ Lọc CLOUD")
        col1, col2, col3 = st.columns(3)
        with col1: st.metric(label="💰 TỔNG DOANH THU PHÁT SINH", value=f"{int(tong_xuong_doanh_thu):,} VNĐ")
        with col2: st.metric(label="🛑 TỔNG CÔNG NỢ ĐANG BỊ ĐỌNG", value=f"{int(tong_xuong_cong_no_hien_tai):,} VNĐ", delta="Khách chưa trả", delta_color="inverse")
        with col3: st.metric(label="✅ TỔNG TIỀM MẶT / CK ĐÃ THU", value=f"{int(tong_xuong_da_tra):,} VNĐ")
        st.write("---") 
        if bang_hien_thi:
            bang_hien_thi.append({"STT": "Tổng", "Khách Hàng": "TOÀN HỆ THỐNG", "SĐT": "-", "Địa Chỉ": "-", "Nợ Mang Sang (đ)": f"{int(tong_xuong_mang_sang):,}", "Phát Sinh Mới (đ)": f"{int(tong_xuong_doanh_thu):,}", "Đã Trả (đ)": f"{int(tong_xuong_da_tra):,}", "Nợ Hiện Tại (đ)": f"{int(tong_xuong_cong_no_hien_tai):,}"})
            st.table(bang_hien_thi)
            st.write("---"); st.subheader("📥 Xuất dữ liệu báo cáo Excel trực tuyến")
            bang_excel_raw.append({"STT": "Tổng", "Khách Hàng": "TOÀN HỆ THỐNG", "Số Điện Thoại": "-", "Địa Chỉ": "-", "Nợ Mang Sang (VNĐ)": int(tong_xuong_mang_sang), "Phát Sinh Mới (VNĐ)": int(tong_xuong_doanh_thu), "Đã Trả (VNĐ)": int(tong_xuong_da_tra), "Nợ Hiện Tại (VNĐ)": int(tong_xuong_cong_no_hien_tai)})
            df = pd.DataFrame(bang_excel_raw)
            def convert_df_to_excel(df_data):
                import io; output = io.BytesIO()
                with pd.ExcelWriter(output, engine='xlsxwriter') as writer: df_data.to_excel(writer, index=False, sheet_name='Cloud_Bao_Cao')
                return output.getvalue()
            excel_data = convert_df_to_excel(df); ngay_tai_file = datetime.datetime.now().strftime("%d_%m_%Y")
            st.download_button(label="📥 XUẤT FILE EXCEL BÁO CÁO CÔNG NỢ CLOUD", data=excel_data, file_name=f"Bao_Cao_Cloud_{ngay_tai_file}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        else:
            st.warning("Không khớp với bất kỳ thông tin bạn hàng nào.")
    else:
        st.info("Hệ thống dữ liệu đám mây trống. Hãy chạy file chuyen_du_lieu.py trước để đẩy số liệu lên mạng.")
