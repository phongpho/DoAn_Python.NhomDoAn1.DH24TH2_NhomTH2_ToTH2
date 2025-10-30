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
# ====== Cửa sổ Kết quả Học tập ======
def open_KQHT(main_root):
    form2_win = tk.Toplevel(main_root)
    form2_win.title("Quản lý Kết quả Học tập")
    center_window(form2_win, 700, 500)
    form2_win.resizable(False, False)
    
    form2_win.grab_set()

    # ====== Tiêu đề ======
    lbl_title = tk.Label(form2_win, text="QUẢN LÝ KẾT QUẢ HỌC TẬP", font=("Arial", 18, "bold"))
    lbl_title.pack(pady=10)

    # ====== Frame nhập thông tin ======
    frame_info = tk.Frame(form2_win)
    frame_info.pack(pady=5, padx=10, fill="x")

    # ===== Mã số sinh viên =====
    tk.Label(frame_info, text="Mã số sinh viên").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_mssv = tk.Entry(frame_info, width=25, state="readonly")
    entry_mssv.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # ===== Họ và tên =====
    tk.Label(frame_info, text="Họ tên sinh viên").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_hoten = tk.Entry(frame_info, width=25, state="readonly")
    entry_hoten.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # ===== Điểm Rèn Luyện =====
    tk.Label(frame_info, text="Điểm Rèn Luyện (DRL)").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_drl = tk.Entry(frame_info, width=20)
    entry_drl.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    # ===== Điểm Tích Lũy =====
    tk.Label(frame_info, text="Điểm Tích Lũy (DTL)").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    entry_dtl = tk.Entry(frame_info, width=20, state="readonly")
    entry_dtl.grid(row=1, column=3, padx=5, pady=5, sticky="w")


    # ====== Bảng danh sách kết quả ======
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

#===== Hàm chức năng ======
    def clear_input():

        entry_mssv.delete(0, tk.END)
        entry_hoten.delete(0, tk.END)
        entry_drl.delete(0, tk.END)
        entry_dtl.delete(0, tk.END)
        
        entry_mssv.config(state="readonly")
        entry_hoten.config(state="readonly")
        entry_dtl.config(state="readonly")
        
        if tree.selection():
            tree.selection_remove(tree.selection()[0])

    def load_data():
        for i in tree.get_children():
            tree.delete(i)
        
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT mssv, hoten, khoa, lop, drl, dtl FROM sinhvien")
            
            for row in cur.fetchall():
                tree.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải dữ liệu: {e}", parent=form2_win)

    def on_tree_select(event):
        selected = tree.selection()
        if not selected:
            return
            
        item = tree.item(selected[0])
        values = item["values"]
        
        entry_mssv.config(state="normal")
        entry_hoten.config(state="normal")
        entry_dtl.config(state="normal")
        
        entry_mssv.delete(0, tk.END)
        entry_mssv.insert(0, values[0])  
        
        entry_hoten.delete(0, tk.END)
        entry_hoten.insert(0, values[1])  
        
        entry_drl.delete(0, tk.END)
        entry_drl.insert(0, values[4])  
        
        entry_dtl.delete(0, tk.END)
        entry_dtl.insert(0, values[5])  

        entry_mssv.config(state="readonly")
        entry_hoten.config(state="readonly")
        entry_dtl.config(state="readonly")

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    def luu_drl():
        """Chỉ lưu Điểm Rèn Luyện (DRL)"""
        mssv = entry_mssv.get()
        drl_nhap = entry_drl.get()
        
        if mssv == "":
            messagebox.showwarning("Lỗi", "Vui lòng chọn một sinh viên từ danh sách.", parent=form2_win)
            return

        try:
            drl_value = float(drl_nhap) 
            if not (0 <= drl_value <= 100):
                 messagebox.showwarning("Dữ liệu không hợp lệ", "Điểm rèn luyện phải từ 0 đến 100.", parent=form2_win)
                 return
        except ValueError:
            messagebox.showerror("Lỗi dữ liệu", "Điểm Rèn Luyện phải là một con số.", parent=form2_win)
            return

        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("UPDATE sinhvien SET drl=%s WHERE mssv=%s",
                        (drl_value, mssv))
            conn.commit()
            messagebox.showinfo("Thành công", "Cập nhật Điểm Rèn Luyện thành công!", parent=form2_win)
            load_data()
            clear_input()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", str(e), parent=form2_win)
        conn.close()

    # ====== Frame nút ======
    frame_btn = tk.Frame(form2_win)
    frame_btn.pack(pady=10)

    tk.Button(frame_btn, text="Lưu", width=10, command=luu_drl).grid(row=0, column=0, padx=10)
    tk.Button(frame_btn, text="Hủy", width=10, command=clear_input).grid(row=0, column=1, padx=10)
    tk.Button(frame_btn, text="Thoát", width=10, command=form2_win.destroy).grid(row=0, column=2, padx=10)

    # ====== Load dữ liệu ban đầu ======
    load_data()