import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from DatabaseConnection import connect_db
from DatabaseConnection import center_window

def open_KQHT(main_root):
    form2_win = tk.Toplevel(main_root)
    form2_win.title("Tra cứu Kết quả Học tập")
    center_window(form2_win, 800, 500)
    form2_win.resizable(False, False)
    form2_win.grab_set()

    lbl_title = tk.Label(form2_win, text="TRA CỨU KẾT QUẢ HỌC TẬP", font=("Arial", 18, "bold"))
    lbl_title.pack(pady=10)

    frame_info = tk.Frame(form2_win)
    frame_info.pack(pady=5, padx=10, fill="x")

    tk.Label(frame_info, text="Chọn khoa").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    cbb_khoa = ttk.Combobox(frame_info, width=30)
    cbb_khoa.grid(row=0, column=1, padx=5, pady=5, sticky="w") 

    tk.Label(frame_info, text="Chọn sinh viên (theo khoa)").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    cbb_sinhvien = ttk.Combobox(frame_info, width=30)
    cbb_sinhvien.grid(row=0, column=3, padx=5, pady=5, sticky="w") 

    lbl_ds = tk.Label(form2_win, text="Bảng điểm tổng hợp", font=("Arial", 10, "bold"))
    lbl_ds.pack(pady=5, anchor="w", padx=10)

    columns = ("Mssv", "Họ và tên", "Khoa", "Lớp", "DRL", "DTL", "XepLoai")
    tree = ttk.Treeview(form2_win, columns=columns, show="headings", height=10)
    
    tree.heading("Mssv", text="MSSV")
    tree.heading("Họ và tên", text="Họ và tên")
    tree.heading("Khoa", text="Khoa")
    tree.heading("Lớp", text="Lớp")
    tree.heading("DRL", text="Điểm Rèn Luyện")
    tree.heading("DTL", text="Điểm Tích Lũy")
    tree.heading("XepLoai", text="Xếp Loại")

    tree.column("Mssv", width=80, anchor="center")
    tree.column("Họ và tên", width=150)
    tree.column("Khoa", width=120)
    tree.column("Lớp", width=80, anchor="center")
    tree.column("DRL", width=100, anchor="center")
    tree.column("DTL", width=100, anchor="center")
    tree.column("XepLoai", width=100, anchor="center")
    
    tree.pack(padx=10, pady=5, fill="both", expand=True)

    #Hàm xử lý
    sinhvien_data = {} 
    
    def load_tree_data(khoa_filter=None, mssv_filter=None, load_all=False): 
        for i in tree.get_children():
            tree.delete(i)
        
        if not khoa_filter and not mssv_filter and not load_all:
            return 
            
        try:
            conn = connect_db()
            cur = conn.cursor()
            
            sql = "SELECT mssv, hoten, khoa, lop, drl, dtl FROM sinhvien"
            params = ()
            
            if mssv_filter and not load_all:
                sql += " WHERE mssv = %s"
                params = (mssv_filter,)
            elif khoa_filter and not load_all:
                sql += " WHERE khoa = %s"
                params = (khoa_filter,)
            
            cur.execute(sql, params)
            for row in cur.fetchall():
                drl = row[4]
                dtl = row[5]

                loai = xep_loai_hoc_tap(dtl, drl)

                values_with_xeploai = row + (loai,)

                tree.insert("", tk.END, values=values_with_xeploai)
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải bảng điểm: {e}", parent=form2_win)

    def load_cbb_khoa():
        try:
            conn = connect_db()
            cur = conn.cursor()

            cur.execute("SELECT DISTINCT khoa FROM sinhvien WHERE khoa IS NOT NULL AND khoa != ''")
            khoa_list = []

            for khoa_tuple in cur.fetchall():
                khoa_list.append(khoa_tuple[0]) 
            
            cbb_khoa['values'] = khoa_list
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải ComboBox Khoa: {e}", parent=form2_win)

    def load_cbb_sinhvien(khoa):
        try:
            conn = connect_db()
            cur = conn.cursor()
            
            cur.execute("SELECT mssv, hoten FROM sinhvien WHERE khoa = %s", (khoa,))
            
            sinhvien_data.clear()
            sv_list = []
            for mssv, hoten in cur.fetchall():
                temp_str = f"{mssv} - {hoten}"
                sinhvien_data[temp_str] = mssv
                sv_list.append(temp_str)
                
            cbb_sinhvien['values'] = sv_list
            cbb_sinhvien.set("")
            
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải ComboBox Sinh viên: {e}", parent=form2_win)

    def khoa_select(event):
        khoa_chon = cbb_khoa.get()
        if not khoa_chon:
            return
        load_cbb_sinhvien(khoa_chon)
        load_tree_data(khoa_filter=khoa_chon)

    def sinhvien_select(event):
        sv_chon = cbb_sinhvien.get()
        mssv = sinhvien_data.get(sv_chon)
        if not mssv:
            return
        load_tree_data(mssv_filter=mssv)

    def reset_view():
        cbb_khoa.set("")
        cbb_sinhvien['values'] = []
        cbb_sinhvien.set("")
        sinhvien_data.clear()
        
        for i in tree.get_children():
            tree.delete(i)

    def tai_tat_ca():
        cbb_khoa.set("")
        cbb_sinhvien['values'] = []
        cbb_sinhvien.set("")
        sinhvien_data.clear()
        
        load_tree_data(load_all=True)

    def xep_loai_hoc_tap(dtl, drl):

        if drl < 50:
            return "Yếu (DRL < 50)"


        if dtl >= 9.0:
            dtl_he_4 = 4.0
        elif dtl >= 8.5:
            dtl_he_4 = 3.7
        elif dtl >= 8.0:
            dtl_he_4 = 3.5
        elif dtl >= 7.0:
            dtl_he_4 = 3.0
        elif dtl >= 6.5:
            dtl_he_4 = 2.5
        elif dtl >= 5.5:
            dtl_he_4 = 2.0
        elif dtl >= 5.0:
            dtl_he_4 = 1.5
        elif dtl >= 4.0:
            dtl_he_4 = 1.0
        else:
            dtl_he_4 = 0.0

        if dtl_he_4 >= 3.6:
            return "Xuất sắc"
        elif dtl_he_4 >= 3.2:
            return "Giỏi"
        elif dtl_he_4 >= 2.5:
            return "Khá"
        elif dtl_he_4 >= 2.0:
            return "Trung bình"
        else:
            return "Yếu"
    cbb_khoa.bind("<<ComboboxSelected>>", khoa_select)
    cbb_sinhvien.bind("<<ComboboxSelected>>", sinhvien_select)

    #Nút
    frame_btn = tk.Frame(form2_win)
    frame_btn.pack(pady=10)

    tk.Button(frame_btn, text="Tải Tất Cả", width=10, command=tai_tat_ca).grid(row=0, column=0, padx=10)
    tk.Button(frame_btn, text="Xóa Bảng", width=10, command=reset_view).grid(row=0, column=1, padx=10)
    tk.Button(frame_btn, text="Thoát", width=10, command=form2_win.destroy).grid(row=0, column=2, padx=10)

    # ====== Tải dữ liệu ban đầu ======
    load_cbb_khoa()
