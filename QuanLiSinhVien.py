import tkinter as tk 
from tkinter import ttk, messagebox 
from tkcalendar import DateEntry 
import mysql.connector 
from DatabaseConnection import connect_db
 
# ====== Hàm canh giữa cửa sổ ====== 
def center_window(win, w=700, h=500): 
    ws = win.winfo_screenwidth() 
    hs = win.winfo_screenheight() 
    x = (ws // 2) - (w // 2) 
    y = (hs // 2) - (h // 2) 
    win.geometry(f'{w}x{h}+{x}+{y}') 
 
# ====== Cửa sổ chính ====== 
root = tk.Tk() 
root.title("Quản lý sinh viên") 
center_window(root, 700, 500) 
root.resizable(False, False) 

# ====== Tiêu đề ====== 
lbl_title = tk.Label(root, text="QUẢN LÝ SINH VIÊN", font=("Arial", 18, "bold")) 
lbl_title.pack(pady=10) 

# ====== Frame nhập thông tin ====== 
frame_info = tk.Frame(root) 
frame_info.pack(pady=5, padx=10, fill="x") 

# ===== Mã số sinh viên =====
tk.Label(frame_info, text="Mssv").grid(row=0, column=0, padx=5, pady=5, 
sticky="w") 
entry_mssv = tk.Entry(frame_info, width=10) 
entry_mssv.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# ===== Họ lót =====
tk.Label(frame_info, text="Họ lót").grid(row=1, column=0, padx=5, pady=5, 
sticky="w") 
entry_holot = tk.Entry(frame_info, width=25) 
entry_holot.grid(row=1, column=1, padx=5, pady=5, sticky="w") 
 
# ===== Tên =====
tk.Label(frame_info, text="Tên").grid(row=1, column=2, padx=5, pady=5, sticky="w") 
entry_ten = tk.Entry(frame_info, width=15) 
entry_ten.grid(row=1, column=3, padx=5, pady=5, sticky="w") 

# ===== Khoa =====
tk.Label(frame_info, text="Khoa").grid(row=0, column=2, padx=5, pady=5, 
sticky="w") 
tk.Label(frame_info, text="Khoa").grid(row=2, column=2, padx=5, pady=5, sticky="w")
cbb_khoa = ttk.Combobox(frame_info, values=[ "CNTT", "Du Lịch Và Văn Hóa Nghệ Thuật", "Nông Nghiệp - Tài Nguyên Thiên Nhiên", "Sư Phạm",
    "Kinh Tế - Quản Trị Kinh Doanh", "Kỹ Thuật - Công Nghệ - Môi Trường", "Ngoại Ngữ", "Luật - Khoa Học Chính Trị "], width=22)
cbb_khoa.grid(row=0, column=3, padx=5, pady=5, sticky="w")
 
# ===== Giới tính =====
tk.Label(frame_info, text="Giới tính").grid(row=2, column=0, padx=5, pady=5, sticky="w") 
gender_var = tk.StringVar(value="Nam") 
tk.Radiobutton(frame_info, text="Nam", variable=gender_var, value="Nam").grid(row=2, column=1, padx=5, sticky="w") 
tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ").grid(row=2, column=1, padx=60, sticky="w") 

# ===== Ngày sinh =====
tk.Label(frame_info, text="Ngày sinh").grid(row=2, column=2, padx=5, pady=5, 
sticky="w") 
entry_date = DateEntry(frame_info, width=12, background="darkblue", 
foreground="white", date_pattern="yyyy-mm-dd") 
entry_date.grid(row=2, column=3, padx=5, pady=5, sticky="w")

# ===== Lớp =====
tk.Label(frame_info, text="Lớp").grid(row=0, column=4, padx=5, pady=5, 
sticky="w")
entry_lop = tk.Entry(frame_info, width=15)
entry_lop.grid(row=0, column=5, padx=5, pady=5, sticky="w")

#====== Bảng danh sách nhân viên ====== 
lbl_ds = tk.Label(root, text="Danh sách sinh viên", font=("Arial", 10, "bold")) 
lbl_ds.pack(pady=5, anchor="w", padx=10) 
 
columns = ("Mssv", "Họ", "Tên", "Giới tính", "Ngày sinh", "khoa", "Lớp") 
tree = ttk.Treeview(root, columns=columns, show="headings", height=10) 
 
for col in columns: 
    tree.heading(col, text=col.capitalize()) 
 
tree.column("Mssv", width=60, anchor="center") 
tree.column("Họ", width=120) 
tree.column("Tên", width=100) 
tree.column("Giới tính", width=70, anchor="center") 
tree.column("Ngày sinh", width=100, anchor="center") 
tree.column("khoa", width=80, anchor="center")
tree.column("Lớp", width=80, anchor="center") 
 
tree.pack(padx=10, pady=5, fill="both") 

# ====== Chức năng CRUD ====== 
def clear_input(): 
    entry_mssv.delete(0, tk.END) 
    entry_holot.delete(0, tk.END) 
    entry_ten.delete(0, tk.END) 
    gender_var.set("Nam") 
    entry_date.set_date("2000-01-01") 
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
    mssv = entry_mssv.get() 
    holot = entry_holot.get() 
    ten = entry_ten.get() 
    gioitinh = gender_var.get() 
    ngaysinh = entry_date.get() 
    khoa = cbb_khoa.get() 
    lop = entry_lop.get()

    if mssv == "" or holot == "" or ten == "": 
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin") 
        return 
 
    conn = connect_db() 
    cur = conn.cursor() 
    try: 
        cur.execute("INSERT INTO sinhvien VALUES (%s, %s, %s, %s, %s, %s, %s)", 
                    (mssv, holot, ten, gioitinh, ngaysinh, khoa, lop)) 
        conn.commit() 
        load_data() 
        clear_input() 
    except Exception as e: 
        messagebox.showerror("Lỗi", str(e)) 
    conn.close() 

def xoa_sv(): 
    selected = tree.selection() 
    if not selected: 
        messagebox.showwarning("Chưa chọn", "Hãy chọn nhân viên để xóa") 
        return 
    mssv = tree.item(selected)["values"][0] 
    conn = connect_db() 
    cur = conn.cursor() 
    cur.execute("DELETE FROM nhanvien WHERE mssv=%s", (mssv,)) 
    conn.commit() 
    conn.close() 
    load_data()

def sua_nv(): 
    selected = tree.selection() 
    if not selected: 
        messagebox.showwarning("Chưa chọn", "Hãy chọn nhân viên để sửa") 
        return 
    values = tree.item(selected)["values"] 
    entry_mssv.delete(0, tk.END) 
    entry_mssv.insert(0, values[0]) 
    entry_holot.delete(0, tk.END) 
    entry_holot.insert(0, values[1]) 
    entry_ten.delete(0, tk.END) 
    entry_ten.insert(0, values[2]) 
    gender_var.set(values[3]) 
    entry_date.set_date(values[4]) 
    cbb_khoa.set(values[5])
    entry_lop.delete(0, tk.END) 
    entry_lop.insert(0, values[6])




root.mainloop()