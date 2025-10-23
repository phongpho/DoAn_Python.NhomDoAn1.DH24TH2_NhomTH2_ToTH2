import tkinter as tk
from tkinter import ttk, messagebox


def mo_form_drl(root, connect_db, center_window):
    drl_win = tk.Toplevel(root)
    drl_win.title("Quản lý điểm rèn luyện")
    center_window(drl_win, 850, 520)
    drl_win.resizable(False, False)

    tk.Label(drl_win, text="QUẢN LÝ ĐIỂM RÈN LUYỆN", font=("Arial", 14, "bold")).pack(pady=10)
    frame_drl = tk.Frame(drl_win)
    frame_drl.pack(pady=5)

    # --- Nhập dữ liệu ---
    tk.Label(frame_drl, text="Mã SV").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_maso_drl = tk.Entry(frame_drl, width=10)
    entry_maso_drl.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_drl, text="Năm học").grid(row=0, column=2, padx=5, pady=5, sticky="w")
    entry_namhoc = tk.Entry(frame_drl, width=10)
    entry_namhoc.insert(0, "2024-2025")
    entry_namhoc.grid(row=0, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame_drl, text="Học kỳ").grid(row=0, column=4, padx=5, pady=5, sticky="w")
    cbb_hocky = ttk.Combobox(frame_drl, values=["HK1", "HK2", "HK3"], width=8)
    cbb_hocky.grid(row=0, column=5, padx=5, pady=5, sticky="w")

    tk.Label(frame_drl, text="Điểm").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_diem = tk.Entry(frame_drl, width=10)
    entry_diem.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_drl, text="Xếp loại:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    lbl_loai_val = tk.Label(frame_drl, text="", width=15, anchor="w", relief="sunken")
    lbl_loai_val.grid(row=1, column=3, padx=5, pady=5, sticky="w")

    # --- Hàm xếp loại ---
    def xep_loai(diem):
        try:
            d = int(diem)
        except:
            return ""
        if d >= 90: return "Xuất sắc"
        elif d >= 80: return "Tốt"
        elif d >= 65: return "Khá"
        elif d >= 50: return "Trung bình"
        else: return "Yếu"

    def tinh_xeploai(event=None):
        lbl_loai_val.config(text=xep_loai(entry_diem.get()))

    entry_diem.bind("<KeyRelease>", tinh_xeploai)

    # --- Bảng dữ liệu ---
    columns = ("maso", "hoten", "namhoc", "hocky", "diem", "xeploai")
    tree_drl = ttk.Treeview(drl_win, columns=columns, show="headings", height=12)

    for col, text in zip(columns, ["Mã SV", "Họ tên", "Năm học", "Học kỳ", "Điểm", "Xếp loại"]):
        tree_drl.heading(col, text=text)
        tree_drl.column(col, width=130, anchor="center")

    tree_drl.pack(padx=10, pady=10, fill="both")

    # --- Hàm xử lý ---
    def load_drl():
        for i in tree_drl.get_children():
            tree_drl.delete(i)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT d.maso, CONCAT(s.holot, ' ', s.ten) AS hoten, d.namhoc, d.hocky, d.diem
            FROM diemrenluyen d
            JOIN sinhvien s ON d.maso = s.maso
        """)
        for maso, hoten, namhoc, hocky, diem in cur.fetchall():
            tree_drl.insert("", tk.END, values=(maso, hoten, namhoc, hocky, diem, xep_loai(diem)))
        conn.close()

    def clear_input():
        entry_maso_drl.delete(0, tk.END)
        entry_namhoc.delete(0, tk.END)
        entry_diem.delete(0, tk.END)
        cbb_hocky.set("")
        lbl_loai_val.config(text="")

    def them_drl():
        maso = entry_maso_drl.get()
        namhoc = entry_namhoc.get()
        hocky = cbb_hocky.get()
        diem = entry_diem.get()
        if maso == "" or hocky == "" or diem == "" or namhoc == "":
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
            return
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO diemrenluyen (maso, namhoc, hocky, diem) VALUES (%s, %s, %s, %s)",
                        (maso, namhoc, hocky, diem))
            conn.commit()
            load_drl()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()

    def sua_drl():
        selected = tree_drl.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn dòng để sửa")
            return
        values = tree_drl.item(selected)["values"]
        entry_maso_drl.delete(0, tk.END)
        entry_maso_drl.insert(0, values[0])
        entry_namhoc.delete(0, tk.END)
        entry_namhoc.insert(0, values[2])
        cbb_hocky.set(values[3])
        entry_diem.delete(0, tk.END)
        entry_diem.insert(0, values[4])
        lbl_loai_val.config(text=values[5])

    def luu_drl():
        maso = entry_maso_drl.get()
        namhoc = entry_namhoc.get()
        hocky = cbb_hocky.get()
        diem = entry_diem.get()
        if maso == "" or namhoc == "" or hocky == "":
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đầy đủ thông tin")
            return
        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("""
                UPDATE diemrenluyen
                SET diem=%s
                WHERE maso=%s AND namhoc=%s AND hocky=%s
            """, (diem, maso, namhoc, hocky))
            conn.commit()
            load_drl()
            clear_input()
        except Exception as e:
            messagebox.showerror("Lỗi", str(e))
        conn.close()

    def xoa_drl():
        selected = tree_drl.selection()
        if not selected:
            messagebox.showwarning("Chưa chọn", "Hãy chọn dữ liệu để xóa")
            return
        maso = tree_drl.item(selected)["values"][0]
        namhoc = tree_drl.item(selected)["values"][2]
        hocky = tree_drl.item(selected)["values"][3]
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM diemrenluyen WHERE maso=%s AND namhoc=%s AND hocky=%s",
                    (maso, namhoc, hocky))
        conn.commit()
        conn.close()
        load_drl()

    def tim_drl():
        maso = entry_maso_drl.get()
        if maso == "":
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập mã sinh viên cần tìm")
            entry_maso_drl.focus_set()
            return
        for i in tree_drl.get_children():
            tree_drl.delete(i)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("""
            SELECT d.maso, CONCAT(s.holot, ' ', s.ten) AS hoten, d.namhoc, d.hocky, d.diem
            FROM diemrenluyen d
            JOIN sinhvien s ON d.maso = s.maso
            WHERE d.maso = %s
        """, (maso,))
        for maso, hoten, namhoc, hocky, diem in cur.fetchall():
            tree_drl.insert("", tk.END, values=(maso, hoten, namhoc, hocky, diem, xep_loai(diem)))
        conn.close()

    # --- Nút thao tác ---
    frame_btn_drl = tk.Frame(drl_win)
    frame_btn_drl.pack(pady=5)

    tk.Button(frame_btn_drl, text="Thêm", width=8, command=them_drl).grid(row=0, column=0, padx=5)
    tk.Button(frame_btn_drl, text="Sửa", width=8, command=sua_drl).grid(row=0, column=1, padx=5)
    tk.Button(frame_btn_drl, text="Lưu", width=8, command=luu_drl).grid(row=0, column=2, padx=5)
    tk.Button(frame_btn_drl, text="Xóa", width=8, command=xoa_drl).grid(row=0, column=3, padx=5)
    tk.Button(frame_btn_drl, text="Tìm kiếm", width=10, command=tim_drl).grid(row=0, column=4, padx=5)
    tk.Button(frame_btn_drl, text="Tải lại", width=8, command=load_drl).grid(row=0, column=5, padx=5)
    tk.Button(frame_btn_drl, text="Thoát", width=8, command=drl_win.destroy).grid(row=0, column=6, padx=5)

    load_drl()
