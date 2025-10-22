import tkinter as tk 
from tkinter import ttk, messagebox 
from tkcalendar import DateEntry 
import mysql.connector 
 
# ====== Kết nối MySQL ====== 
def connect_db(): 
    return mysql.connector.connect( 
        host="localhost", 
        user="root",        
        password="123456",        
        database="qlsv" 
    ) 
# ====== Hàm canh giữa cửa sổ ====== 
def center_window(win, w=700, h=500): 
    ws = win.winfo_screenwidth() 
    hs = win.winfo_screenheight() 
    x = (ws // 2) - (w // 2) 
    y = (hs // 2) - (h // 2) 
    win.geometry(f'{w}x{h}+{x}+{y}') 
 
# ====== Cửa sổ chính ====== 
root = tk.Tk() 
root.title("Quản lý sinh viên ") 
center_window(root, 700, 500) 
root.resizable(False, False) 
 
# ====== Tiêu đề ====== 
lbl_title = tk.Label(root, text="QUẢN LÝ SINH VIÊN", font=("Arial", 18, "bold")) 
lbl_title.pack(pady=10) 
 
# ====== Frame nhập thông tin ====== 
frame_info = tk.Frame(root) 
frame_info.pack(pady=5, padx=10, fill="x") 
 
tk.Label(frame_info, text="Mã số").grid(row=0, column=0, padx=5, pady=5, 
sticky="w") 
entry_maso = tk.Entry(frame_info, width=10) 
entry_maso.grid(row=0, column=1, padx=5, pady=5, sticky="w") 

 
tk.Label(frame_info, text="Khoa").grid(row=0, column=2, padx=5, pady=5, 
sticky="w") 
cbb_khoa = ttk.Combobox(frame_info, values=[ 
    "CNTT", "Du Lịch Và Văn Hóa Nghệ Thuật", "Nông Nghiệp - Tài Nguyên Thiên Nhiên", "Sư Phạm",
    "Kinh Tế - Quản Trị Kinh", "Kỹ Thuật - Công Nghệ - Môi Trường", "Ngoại Ngữ", "Luật - Khoa Học Chính "], width=20) 
cbb_khoa.grid(row=0, column=3, padx=5, pady=5, sticky="w") 
 
tk.Label(frame_info, text="Họ lót").grid(row=1, column=0, padx=5, pady=5, 
sticky="w") 
entry_holot = tk.Entry(frame_info, width=25) 
entry_holot.grid(row=1, column=1, padx=5, pady=5, sticky="w") 
 
tk.Label(frame_info, text="Tên").grid(row=1, column=2, padx=5, pady=5, sticky="w") 
entry_ten = tk.Entry(frame_info, width=15) 
entry_ten.grid(row=1, column=3, padx=5, pady=5, sticky="w") 
 
tk.Label(frame_info, text="Phái").grid(row=2, column=0, padx=5, pady=5, sticky="w") 
gender_var = tk.StringVar(value="Nam") 
tk.Radiobutton(frame_info, text="Nam", variable=gender_var, 
value="Nam").grid(row=2, column=1, padx=5, sticky="w") 
tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ").grid(row=2, 
column=1, padx=60, sticky="w") 
tk.Label(frame_info, text="Ngày sinh").grid(row=2, column=2, padx=5, pady=5, 
sticky="w") 
date_entry = DateEntry(frame_info, width=12, background="darkblue", 
foreground="white", date_pattern="yyyy-mm-dd") 
date_entry.grid(row=2, column=3, padx=5, pady=5, sticky="w") 

tk.Label(frame_info, text="Lớp").grid(row=0, column=4, padx=5, pady=5, 
sticky="w") 
entry_lop = tk.Entry(frame_info, width=10) 
entry_lop.grid(row=0, column=6, padx=5, pady=5, sticky="w") 
 
# ====== Bảng danh sách nhân viên ====== 
lbl_ds = tk.Label(root, text="Danh sách nhân viên", font=("Arial", 10, "bold")) 
lbl_ds.pack(pady=5, anchor="w", padx=10) 
 
columns = ("MSSV", "holot", "ten", "phai", "ngaysinh", "lop", "khoa") 
tree = ttk.Treeview(root, columns=columns, show="headings", height=10) 
 
for col in columns: 
    tree.heading(col, text=col.capitalize()) 
 
tree.column("MSSV", width=60, anchor="center") 
tree.column("holot", width=150) 
tree.column("ten", width=100) 
tree.column("phai", width=70, anchor="center") 
tree.column("ngaysinh", width=100, anchor="center") 
tree.column("lop", width=100)
tree.column("khoa", width=100) 
 
tree.pack(padx=10, pady=5, fill="both") 
 
# ====== Chức năng CRUD ====== 
def clear_input(): 
    entry_maso.delete(0, tk.END) 
    entry_holot.delete(0, tk.END) 
    entry_ten.delete(0, tk.END) 
    gender_var.set("Nam") 
    date_entry.set_date("2000-01-01") 
    cbb_khoa.set("") 
    entry_lop.delete(0, tk.END)
 
def load_data(): 
    for i in tree.get_children(): 
        tree.delete(i) 
    conn = connect_db() 
    cur = conn.cursor() 
    cur.execute("SELECT * FROM sinhvien") 
    for row in cur.fetchall(): 
        tree.insert("", tk.END, values=row) 
    conn.close() 
 
def them_sv(): 
    maso = entry_maso.get() 
    holot = entry_holot.get() 
    ten = entry_ten.get() 
    phai = gender_var.get() 
    ngaysinh = date_entry.get() 
    khoa = cbb_khoa.get() 
    lop = entry_lop.get()
 
    if maso == "" or holot == "" or ten == "": 
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin") 
        return 
 
    conn = connect_db() 
    cur = conn.cursor() 
    try: 
        cur.execute("INSERT INTO sinhvien VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (maso, holot, ten, phai, ngaysinh, khoa, lop)) 
        conn.commit() 
        load_data() 
        clear_input() 
    except Exception as e: 
        messagebox.showerror("Lỗi", str(e)) 
    conn.close() 
 
def xoa_sv(): 
    selected = tree.selection() 
    if not selected: 
        messagebox.showwarning("Chưa chọn", "Hãy chọn sinh viên để xóa") 
        return 
    maso = tree.item(selected)["values"][0] 
    conn = connect_db() 
    cur = conn.cursor() 
    cur.execute("DELETE FROM sinhvien WHERE maso=%s", (maso,)) 
    conn.commit() 
    conn.close() 
    load_data() 
 
def sua_sv(): 
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Chưa chọn", "Hãy chọn sinh viên để sửa")
        return

    values = tree.item(selected)["values"]

    entry_maso.delete(0, tk.END)
    entry_maso.insert(0, values[0])

    entry_holot.delete(0, tk.END)
    entry_holot.insert(0, values[1])

    entry_ten.delete(0, tk.END)
    entry_ten.insert(0, values[2])

    gender_var.set(values[3])
    date_entry.set_date(values[4])

    # Cập nhật lớp
    entry_lop.delete(0, tk.END)
    entry_lop.insert(0, values[5])

    # Cập nhật khoa (nếu là combobox)
    cbb_khoa.set(values[6])


def luu_sv(): 
    maso = entry_maso.get() 
    holot = entry_holot.get() 
    ten = entry_ten.get() 
    phai = gender_var.get() 
    ngaysinh = date_entry.get() 
    khoa = cbb_khoa.get() 
    lop = entry_lop.get()
    conn = connect_db() 
    cur = conn.cursor() 
    cur.execute("""UPDATE sinhvien 
               SET holot=%s, ten=%s, phai=%s, ngaysinh=%s, khoa=%s, lop=%s 
               WHERE maso=%s""",
            (holot, ten, phai, ngaysinh, khoa, lop, maso))
    conn.commit() 
    conn.close() 
    load_data() 
    clear_input() 


# ====== Form quản lý điểm rèn luyện ======
def mo_form_drl():
    drl_win = tk.Toplevel(root)
    drl_win.title("Quản lý điểm rèn luyện")
    drl_win.geometry("850x520")
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

    # --- Hàm thao tác ---
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


# ====== Frame nút ====== 
frame_btn = tk.Frame(root) 
frame_btn.pack(pady=5) 
 
tk.Button(frame_btn, text="Thêm", width=8, command=them_sv).grid(row=0,     column=0, padx=5) 
tk.Button(frame_btn, text="Lưu", width=8, command=luu_sv).grid(row=0,       column=1, padx=5) 
tk.Button(frame_btn, text="Sửa", width=8, command=sua_sv).grid(row=0,       column=2, padx=5) 
tk.Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=0,  column=3, padx=5) 
tk.Button(frame_btn, text="Xóa", width=8, command=xoa_sv).grid(row=0,       column=4, padx=5) 
tk.Button(frame_btn, text="Thoát", width=8, command=root.quit).grid(row=0,  column=5, padx=5) 
tk.Button(frame_btn, text="Điểm rèn luyện", width=15, command=lambda: mo_form_drl()).grid(row=0, column=6, padx=5)


# ====== Load dữ liệu ban đầu ====== 
load_data() 
root.mainloop()