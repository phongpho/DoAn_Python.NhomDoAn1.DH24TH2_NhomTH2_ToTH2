import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from DatabaseConnection import connect_db

# ====== Hàm canh giữa cửa sổ ======
def center_window(win, w=700, h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ====== Cửa sổ Kết quả Học tập (FORM 2) ======
def open_KQHT(main_root):
    form2_win = tk.Toplevel(main_root)
    form2_win.title("Tra cứu Kết quả Học tập")
    center_window(form2_win, 700, 500)
    form2_win.resizable(False, False)
    form2_win.grab_set()

    # ====== Tiêu đề ======
    lbl_title = tk.Label(form2_win, text="TRA CỨU KẾT QUẢ HỌC TẬP", font=("Arial", 18, "bold"))
    lbl_title.pack(pady=10)

    # ====== Frame Lọc ======
    frame_info = tk.Frame(form2_win)
    frame_info.pack(pady=5, padx=10, fill="x")

    # --- Sửa lỗi 1: Tách .grid() ra ---
    tk.Label(frame_info, text="Chọn khoa").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    cbb_khoa = ttk.Combobox(frame_info, width=30)
    cbb_khoa.grid(row=0, column=1, padx=5, pady=5, sticky="w") 

    tk.Label(frame_info, text="Chọn sinh viên (theo khoa)").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    cbb_sinhvien = ttk.Combobox(frame_info, width=30)
    cbb_sinhvien.grid(row=0, column=3, padx=5, pady=5, sticky="w") 

    # ====== Bảng danh sách kết quả (Treeview) ======
    lbl_ds = tk.Label(form2_win, text="Bảng điểm tổng hợp", font=("Arial", 10, "bold"))
    lbl_ds.pack(pady=5, anchor="w", padx=10)

    columns = ("Mssv", "Họ và tên", "Khoa", "Lớp", "DRL", "DTL")
    tree = ttk.Treeview(form2_win, columns=columns, show="headings", height=10)
    
    tree.heading("Mssv", text="MSSV")
    tree.heading("Họ và tên", text="Họ và tên")
    tree.heading("Khoa", text="Khoa")
    tree.heading("Lớp", text="Lớp")
    tree.heading("DRL", text="Điểm Rèn Luyện")
    tree.heading("DTL", text="Điểm Tích Lũy")

    tree.column("Mssv", width=80, anchor="center")
    tree.column("Họ và tên", width=150)
    tree.column("Khoa", width=120)
    tree.column("Lớp", width=80, anchor="center")
    tree.column("DRL", width=100, anchor="center")
    tree.column("DTL", width=100, anchor="center")
    
    tree.pack(padx=10, pady=5, fill="both", expand=True)

    # ===== Hàm chức năng =====
    sinhvien_data = {} 
    
    def load_tree_data(khoa_filter=None, mssv_filter=None):
        for i in tree.get_children():
            tree.delete(i)
        
        if not khoa_filter and not mssv_filter:
            return 
            
        try:
            conn = connect_db()
            cur = conn.cursor()
            
            sql = "SELECT mssv, hoten, khoa, lop, drl, dtl FROM sinhvien"
            params = ()
            
            if mssv_filter:
                sql += " WHERE mssv = %s"
                params = (mssv_filter,)
            elif khoa_filter:
                sql += " WHERE khoa = %s"
                params = (khoa_filter,)
            
            cur.execute(sql, params)
            for row in cur.fetchall():
                tree.insert("", tk.END, values=row)
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

    # Gán sự kiện (bind)
    cbb_khoa.bind("<<ComboboxSelected>>", khoa_select)
    cbb_sinhvien.bind("<<ComboboxSelected>>", sinhvien_select)

    # ====== Frame nút ======
    frame_btn = tk.Frame(form2_win)
    frame_btn.pack(pady=10)

    tk.Button(frame_btn, text="Reset", width=10, command=reset_view).grid(row=0, column=0, padx=10)
    tk.Button(frame_btn, text="Thoát", width=10, command=form2_win.destroy).grid(row=0, column=1, padx=10)

    # ====== Tải dữ liệu ban đầu ======
    load_cbb_khoa()
