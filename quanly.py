import os
import sqlite3
import datetime
import streamlit as st

# =============================================================
# CẤU HÌNH HỆ THỐNG & THÔNG TIN CƠ SỞ
# =============================================================
DB_FILE = "dulieu_sơn tĩnh điện.db"
TEN_CO_SO = "XƯỞNG SƠN TĨNH ĐIỆN HƯỞNG THỦY"
SDT_CHU_XUONG = "0979.141.588"
DIA_CHI_XUONG = "Tân Lập Hợp Lý Phú Thọ"
STK_NGAN_HANG = "104869545034"
TEN_NGAN_HANG = "VietinBank - CN VINH PHUC"
TEN_CHU_TK = "LE VAN HUONG"

# Hàm tạo giao diện in ấn HTML phôi A4 (Đã sửa đổi co giãn tự động)
def lay_khung_html_a4(ten_chuan_hoa, sdt, diachi, rows_html, no_dau_ky, tong_phat_sinh, tong_da_tra, tong_nong_cuoi_ky):
    ngay_lap_he_thong = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
    
    no_dau_ky_int = int(no_dau_ky or 0)
    tong_phat_sinh_int = int(tong_phat_sinh or 0)
    tong_da_tra_int = int(tong_da_tra or 0)
    tong_nong_cuoi_ky_int = int(tong_nong_cuoi_ky or 0)
    
    return f"""
    <div id="hoa_don_print_target" style="font-family: Arial, sans-serif; background-color: #fff; color: #000; max-width: 680px; margin: 0 auto; box-sizing: border-box; display: flex; flex-direction: column; padding: 10px;">
        <style>
            @media print {{
                #vung_cuon_hang {{ border: none !important; }}
                thead tr th {{ position: static !important; background-color: #f2f2f2 !important; }}
                body {{ margin: 0; padding: 0; }}
            }}
        </style>
        <div style="text-align: center; margin-bottom: 15px; flex-shrink: 0;">
            <h2 style="margin: 0; text-transform: uppercase; font-size: 20px; font-weight: bold; color: #000;">🏪 {TEN_CO_SO}</h2>
            <p style="margin: 5px 0; font-size: 13px;">📞 Hotline/Zalo quản lý: {SDT_CHU_XUONG}</p>
            <p style="margin: 3px 0; font-size: 13px; color: #000;">📍 Địa chỉ: {DIA_CHI_XUONG}</p>
            
            <p style="margin: 8px 0 3px 0; font-size: 13px; font-weight: bold; text-transform: uppercase;">THÔNG TIN THANH TOÁN CHUYỂN KHOẢN:</p>
            <p style="margin: 3px 0; font-size: 14px;">Số tài khoản: <strong style="font-size: 16px;">{STK_NGAN_HANG}</strong></p>
            <p style="margin: 3px 0; font-size: 13px;">Ngân hàng: {TEN_NGAN_HANG} - Chủ TK: {TEN_CHU_TK}</p>
            <hr style="border: none; border-top: 1px dashed #000; margin: 15px 0 10px 0;">
            <table style="width: 100%; border: none; font-size: 13px; margin-bottom: 5px; line-height: 1.5; text-align: left;">
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
        <div id="vung_cuon_hang" style="border: 1px solid #000; margin-bottom: 15px; padding: 2px;">
            <table style="width: 100%; border-collapse: collapse;" border="1">
                <thead>
                    <tr style="background-color: #f2f2f2; font-size: 12px; height: 30px; font-weight: bold;">
                        <th style="width: 8%; text-align:center; background-color: #f2f2f2;">STT</th>
                        <th style="width: 14%; text-align:center; background-color: #f2f2f2;">Ngày</th>
                        <th style="width: 38%; text-align:left; padding-left: 5px; background-color: #f2f2f2;">Nội dung mặt hàng / Giao dịch</th>
                        <th style="width: 8%; text-align:center; background-color: #f2f2f2;">ĐVT</th>
                        <th style="width: 10%; text-align:right; padding-right: 5px; background-color: #f2f2f2;">Đơn giá</th>
                        <th style="width: 8%; text-align:center; background-color: #f2f2f2;">SL</th>
                        <th style="width: 14%; text-align:right; padding-right: 5px; background-color: #f2f2f2;">Thành tiền (đ)</th>
                    </tr>
                </thead>
                <tbody>{rows_html}</tbody>
            </table>
        </div>
        <div style="flex-shrink: 0; margin-top: auto; border-top: 1px solid #000; padding-top: 5px;">
            <table style="width: 100%; border: none; font-size: 14px; line-height: 1.8; text-align: left;">
                <tr>
                    <td style="width: 53%; vertical-align: top;">
                        🔷 Nợ gốc mang sang: <strong>{no_dau_ky_int:,} đ</strong><br>
                        ➕ Tổng phát sinh mới: <strong>{tong_phat_sinh_int:,} đ</strong><br>
                        ➖ Tổng tiền đã trả: <strong style="color: green;">-{tong_da_tra_int:,} đ</strong>
                    </td>
                    <td style="text-align: right; width: 47%; vertical-align: middle;">
                        <div style="border: 2px double #000; padding: 8px; display: inline-block; background-color: #f9f9f9; text-align: center;">
                            <span style="font-weight: bold; font-size: 13px; text-transform: uppercase; color: #000;">⚪ TỔNG NỢ CUỐI CÙNG:</span><br>
                            <strong style="font-size: 20px; color: #000;">{tong_nong_cuoi_ky_int:,} VNĐ</strong>
                        </div>
                    </td>
                </tr>
            </table>
        </div>
    </div>
    """
# =============================================================
# KHỞI TẠO CƠ SỞ DỮ LIỆU (SQLITE)
# =============================================================
with sqlite3.connect(DB_FILE) as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS khach_hang (ten TEXT PRIMARY KEY, sdt TEXT, diachi TEXT, nocu REAL DEFAULT 0)")
    cursor.execute("CREATE TABLE IF NOT EXISTS lich_su_mua (id INTEGER PRIMARY KEY AUTOINCREMENT, ten_khach TEXT, ngay TEXT, loai_gd TEXT, ten_hang TEXT, dvt TEXT, dongia REAL DEFAULT 0, soluong REAL DEFAULT 0, thanhtien REAL DEFAULT 0)")
    conn.commit()

st.set_page_config(page_title="Hệ Thống Quản Lý Sơn Tĩnh Điện", layout="wide")
st.title("🏭 HỆ THỐNG QUẢN LÝ BẠN HÀNG & CÔNG NỢ SƠN TĨNH ĐIỆN")

tab1, tab2 = st.tabs(["👤 CHI TIẾT KHÁCH HÀNG & IN ẤN", "📊 TỔNG HỢP CÔNG NỢ TOÀN XƯỞNG"])
with tab1:
    col_trai, col_phai = st.columns([1, 1.3])
    
    with col_trai:
        st.header("🛠️ Nhập Liệu")
        ten_nhap_raw = st.text_input("Gõ tên khách hàng để tra cứu:", value="tuyen k1")
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
                st.success(f"🔍 Đã tìm thấy khách cũ: {ten_chuan_hoa}")
            else:
                st.info(f"🆕 Chuẩn bị tạo khách mới: {ten_chuan_hoa}")

        st.subheader("👤 Thông tin khách")
        with st.form("form_khach_hang"):
            sdt = st.text_input("Số ĐT Khách:", value=sdt_mac_dinh)
            diachi = st.text_input("Địa chỉ Khách:", value=diachi_mac_dinh)
            no_dau_ky = st.number_input("Nợ gốc mang sang (VNĐ):", value=float(nocu_mac_dinh), step=10000.0, format="%.0f")
            if st.form_submit_button("💾 LƯU THÔNG TIN KHÁCH"):
                if ten_chuan_hoa:
                    with sqlite3.connect(DB_FILE) as conn:
                        cursor = conn.cursor()
                        if khach_cu:
                            cursor.execute("UPDATE khach_hang SET sdt = ?, diachi = ?, nocu = ? WHERE TRIM(LOWER(ten)) = TRIM(LOWER(?))", (sdt, diachi, no_dau_ky, ten_chuan_hoa))
                        else:
                            cursor.execute("INSERT INTO khach_hang (ten, sdt, diachi, nocu) VALUES (?, ?, ?, ?)", (ten_chuan_hoa, sdt, diachi, no_dau_ky))
                        conn.commit()
                    st.rerun()

        st.subheader("📝 Giao dịch mới")
        with st.form("form_giao_dich"):
            ngay_ghi_so = st.date_input("Ngày phát sinh giao dịch:", datetime.date.today())
            loai_gd = st.radio("Loại giao dịch:", options=["Mua hàng", "Khách trả tiền"], horizontal=True)
            ten_hang = st.text_input("Tên hàng / Nội dung công việc:")
            dvt = st.selectbox("ĐVT:", options=["kg", "bộ", "m2", "cái", "lần"])
            dongia = st.number_input("Đơn giá / Số tiền khách trả:", min_value=0.0, step=500.0, format="%.0f")
            soluong = st.number_input("Số lượng mua (Bằng 1 nếu là khách trả tiền):", min_value=0.0, step=1.0, value=1.0)
            tien_tra_kem = st.number_input("Tiền Khách trả kèm lúc mua (nếu có):", min_value=0.0, step=10000.0, format="%.0f")
            if st.form_submit_button("➕ KÍCH LƯU GIAO DỊCH"):
                if ten_chuan_hoa and khach_cu:
                    ngay_format = ngay_ghi_so.strftime("%d/%m/%Y")
                    with sqlite3.connect(DB_FILE) as conn:
                        cursor = conn.cursor()
                        if loai_gd == "Mua hàng":
                            thanhtien_mua = dongia * soluong
                            cursor.execute("INSERT INTO lich_su_mua (ten_khach, ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (ten_chuan_hoa, ngay_format, "Mua hàng", ten_hang, dvt, dongia, soluong, thanhtien_mua))
                            if tien_tra_kem > 0:
                                cursor.execute("INSERT INTO lich_su_mua (ten_khach, ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (ten_chuan_hoa, ngay_format, "Khách trả tiền", "Khách thanh toán tiền mặt/CK", "lần", 0.0, 1.0, -tien_tra_kem))
                        else:
                            ten_hang_tra = "Khách thanh toán tiền mặt/CK" if not ten_hang else ten_hang
                            sotientra = dongia if dongia > 0 else tien_tra_kem
                            if sotientra > 0:
                                cursor.execute("INSERT INTO lich_su_mua (ten_khach, ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (ten_chuan_hoa, ngay_format, "Khách trả tiền", ten_hang_tra, "lần", 0.0, 1.0, -sotientra))
                        conn.commit()
                    st.rerun()
                else:
                    st.error("🔒 Hãy lưu thông tin khách trước khi kích lưu giao dịch!")
    with col_phai:
        st.header("📋 Bộ Lọc & Đối Soát")
        st.selectbox("Thời gian xem hóa đơn:", options=["Tất cả thời gian"])
        rows_html, tong_phat_sinh, tong_da_tra = "", 0.0, 0.0

        if ten_chuan_hoa and khach_cu:
            with sqlite3.connect(DB_FILE) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien FROM lich_su_mua WHERE TRIM(LOWER(ten_khach)) = TRIM(LOWER(?)) ORDER BY id ASC", (ten_chuan_hoa,))
                giao_dichs = cursor.fetchall()
            
            # Xây dựng bảng hiển thị hóa đơn in ấn
            for idx, gd in enumerate(giao_dichs, 1):
                gd_id, ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien = gd
                if thanhtien < 0:
                    tong_da_tra += abs(thanhtien)
                    thanhtien_fmt = f"-{int(abs(thanhtien)):,}"
                    dongia_fmt = "-"
                    soluong_fmt = "-"
                else:
                    tong_phat_sinh += thanhtien
                    thanhtien_fmt = f"{int(thanhtien):,}"
                    dongia_fmt = f"{int(dongia):,}" if dongia > 0 else "-"
                    soluong_fmt = f"{soluong:g}" if soluong > 0 else "-"
                rows_html += f'<tr style="height: 30px; font-size: 13px;"><td style="text-align:center; border: 1px solid #000;">{idx}</td><td style="text-align:center; border: 1px solid #000;">{ngay}</td><td style="text-align:left; padding-left: 5px; border: 1px solid #000;">{ten_hang}</td><td style="text-align:center; border: 1px solid #000;">{dvt}</td><td style="text-align:right; padding-right: 5px; border: 1px solid #000;">{dongia_fmt}</td><td style="text-align:center; border: 1px solid #000;">{soluong_fmt}</td><td style="text-align:right; padding-right: 5px; border: 1px solid #000; font-weight: bold;">{thanhtien_fmt}</td></tr>'

            tong_nong_cuoi_ky = no_dau_ky + tong_phat_sinh - tong_da_tra
            hoa_don_html = lay_khung_html_a4(ten_chuan_hoa, sdt, diachi, rows_html, no_dau_ky, tong_phat_sinh, tong_da_tra, tong_nong_cuoi_ky)
            
            # Khung hiển thị hóa đơn đạt chuẩn chiều cao 750px không lo che khuất phần đuôi tổng nợ
            st.components.v1.html(hoa_don_html, height=750, scrolling=True)
            
            # Nút in mở tab mới gốc an toàn
            html_nut_bam_in_chuan = f"<script>function thucHienLenhIn() {{ var staticPage = window.open('about:blank', '_blank'); staticPage.document.write(`{hoa_don_html}`); staticPage.document.close(); staticPage.focus(); setTimeout(function() {{ staticPage.print(); }}, 500); }}</script><button onclick='thucHienLenhIn()' style='width: 100%; height: 42px; background-color: #315277; color: white; border: none; border-radius: 4px; font-weight: bold; font-size: 14px; cursor: pointer;'>🖨️ KÍCH HOẠT LỆNH IN HOẶC XUẤT FILE PDF NGAY TẠI ĐẦY</button>"
            st.components.v1.html(html_nut_bam_in_chuan, height=50, scrolling=False)
            
            # Khung sửa lỗi sổ sách bóc tách tuple an toàn bằng ID hệ thống
            st.subheader("❌ Sửa Lỗi Sổ Sách (Xóa giao dịch nhập nhầm)")
            dict_xoa = {}
            for gd in giao_dichs:
                gd_id, ngay, loai_gd, ten_hang, dvt, dongia, soluong, thanhtien = gd
                tien_hien_thi = int(abs(thanhtien))
                ten_dong_xoa = f"Mã #{gd_id} | Ngày {ngay}: {ten_hang} ({tien_hien_thi:,} đ)"
                dict_xoa[ten_dong_xoa] = gd_id
                
            dong_chon_xoa = st.selectbox("Chọn dòng giao dịch nhập sai cần xóa bỏ:", options=["-- Chọn dòng cần xóa --"] + list(dict_xoa.keys()))
            
            if dong_chon_xoa != "-- Chọn dòng cần xóa --":
                id_database_xoa = dict_xoa[dong_chon_xoa]
                if st.button("🗑️ XÁC NHẬN XÓA DÒNG NÀY KHỎI SỔ NỢ", use_container_width=True, type="primary"):
                    with sqlite3.connect(DB_FILE) as conn:
                        cursor = conn.cursor()
                        cursor.execute("DELETE FROM lich_su_mua WHERE id = ?", (id_database_xoa,))
                        conn.commit()
                    st.success("Đã xóa giao dịch nhập nhầm! Đang tải lại sổ nợ...")
                    st.rerun()
        else:
            st.info("💡 Gõ tên một khách hàng hợp lệ để hiển thị hóa đơn đối soát.")
# =============================================================
# TAB 2: TỔNG HỢP CÔNG NỢ TOÀN BỘ KHÁCH HÀNG TRONG XƯỞNG
# =============================================================
with tab2:
    st.header("📊 BẢNG TỔNG HỢP CÔNG NỢ TOÀN XƯỞNG SƠN")
    st.markdown("Danh sách tất cả các khách hàng đang lưu trong hệ thống kèm số tiền tổng nợ hiện tại:")
    
    # Sử dụng LEFT JOIN nhóm theo khách hàng để quét toàn bộ hệ thống siêu tốc chỉ với 1 câu lệnh SQL
    with sqlite3.connect(DB_FILE) as conn:
        cursor = conn.cursor()
        query = """
            SELECT k.ten, k.sdt, k.diachi, k.nocu, 
                   COALESCE(SUM(l.thanhtien), 0) as tong_phat_sinh
            FROM khach_hang k
            LEFT JOIN lich_su_mua l ON TRIM(LOWER(k.ten)) = TRIM(LOWER(l.ten_khach))
            GROUP BY k.ten
            ORDER BY k.ten ASC
        """
        cursor.execute(query)
        all_khach_toi_uu = cursor.fetchall()
        
    if all_khach_toi_uu:
        rows_tong_hop = ""
        tong_no_phai_thu_ca_xuong = 0.0
        
        for stt, kh in enumerate(all_khach_toi_uu, 1):
            t_ten, t_sdt, t_diachi, t_nocu, t_phat_sinh = kh
            
            # Tính toán chuẩn số liệu công nợ không lo chính tả
            tong_no_cuoi_khach = t_nocu + t_phat_sinh
            tong_no_phai_thu_ca_xuong += tong_no_cuoi_khach
            
            rows_tong_hop += f"""
            <tr style="height: 35px; font-size: 14px;">
                <td style="text-align: center;">{stt}</td>
                <td style="padding-left: 8px; font-weight: bold; text-transform: uppercase;">{t_ten}</td>
                <td style="text-align: center;">{t_sdt if t_sdt else '-'}</td>
                <td style="padding-left: 8px;">{t_diachi if t_diachi else '-'}</td>
                <td style="text-align: right; padding-right: 10px; font-weight: bold; color: {'red' if tong_no_cuoi_khach > 0 else 'green'};">{int(tong_no_cuoi_khach):,} đ</td>
            </tr>
            """
            
        html_bang_tong_hop = f"""
        <table style="width: 100%; border-collapse: collapse; margin-top: 10px;" border="1">
            <thead>
                <tr style="background-color: #315277; color: white; height: 38px; font-size: 14px; font-weight: bold;">
                    <th style="width: 6%;">STT</th>
                    <th style="width: 25%; text-align: left; padding-left: 8px;">Tên khách hàng</th>
                    <th style="width: 15%;">Số điện thoại</th>
                    <th style="width: 34%; text-align: left; padding-left: 8px;">Địa chỉ</th>
                    <th style="width: 20%; text-align: right; padding-right: 10px;">Tổng nợ hiện tại (đ)</th>
                </tr>
            </thead>
            <tbody>
                {rows_tong_hop}
                <tr style="height: 40px; background-color: #f2f2f2; font-size: 16px; font-weight: bold;">
                    <td colspan="4" style="text-align: right; padding-right: 15px; color: #000;">💰 TỔNG CÔNG NỢ PHẢI THU TOÀN XƯỞNG SƠN:</td>
                    <td style="text-align: right; padding-right: 10px; color: red; font-size: 18px;">{int(tong_no_phai_thu_ca_xuong):,} đ</td>
                </tr>
            </tbody>
        </table>
        """
        st.components.v1.html(html_bang_tong_hop, height=600, scrolling=True)
    else:
        st.info("💡 Chưa có dữ liệu khách hàng nào trong hệ thống.")
