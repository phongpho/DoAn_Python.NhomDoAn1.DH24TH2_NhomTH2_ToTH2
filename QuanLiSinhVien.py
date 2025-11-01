import tkinter as tk 
from tkinter import ttk, messagebox 
from tkcalendar import DateEntry 
import mysql.connector 
from DatabaseConnection import connect_db
from KetQuaHocTap_form import open_KQHT
from ChiTietDiemTichLuy_form import open_ChiTietDiem
from ChiTietDiemRenluyen_form import open_ChiTietDiemRenLuyen
 
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
tk.Label(frame_info, text="Mã số sinh viên").grid(row=0, column=0, padx=5, pady=5, sticky="w") 
entry_mssv = tk.Entry(frame_info, width=20) 
entry_mssv.grid(row=0, column=1, padx=5, pady=5, sticky="w")

# ===== Họ và tên =====
tk.Label(frame_info, text="Họ tên sinh viên").grid(row=1, column=0, padx=5, pady=5, sticky="w") 
entry_hoten = tk.Entry(frame_info, width=25) 
entry_hoten.grid(row=1, column=1, padx=5, pady=5, sticky="w") 

# ===== Khoa =====
tk.Label(frame_info, text="Khoa").grid(row=0, column=2, padx=5, pady=5, sticky="w")
cbb_khoa = ttk.Combobox(frame_info, values=[ "Công Nghệ Thông Tin", "Du Lịch Và Văn Hóa Nghệ Thuật", "Nông Nghiệp - Tài Nguyên Thiên Nhiên", "Sư Phạm",
    "Kinh Tế - Quản Trị Kinh Doanh", "Kỹ Thuật - Công Nghệ - Môi Trường", "Ngoại Ngữ", "Luật - Khoa Học Chính Trị "], width=22)
cbb_khoa.grid(row=0, column=3, padx=5, pady=5, sticky="w")

# ===== Lớp =====
tk.Label(frame_info, text="Lớp").grid(row=1, column=2, padx=5, pady=5, sticky="w")
entry_lop = tk.Entry(frame_info, width=20)
entry_lop.grid(row=1, column=3, padx=5, pady=5, sticky="w")
 
# ===== Giới tính =====
tk.Label(frame_info, text="Giới tính").grid(row=2, column=0, padx=5, pady=5, sticky="w") 
gender_var = tk.StringVar(value="Nam") 
tk.Radiobutton(frame_info, text="Nam", variable=gender_var, value="Nam").grid(row=2, column=1, padx=5, sticky="w") 
tk.Radiobutton(frame_info, text="Nữ", variable=gender_var, value="Nữ").grid(row=2, column=1, padx=60, sticky="w") 

# ===== Ngày sinh =====
tk.Label(frame_info, text="Ngày sinh").grid(row=2, column=2, padx=5, pady=5, sticky="w") 
entry_date = DateEntry(frame_info, width=12, background="darkblue", 
foreground="white", date_pattern="yyyy-mm-dd") 
entry_date.grid(row=2, column=3, padx=5, pady=5, sticky="w")


#====== Bảng danh sách nhân viên ====== 
lbl_ds = tk.Label(root, text="Danh sách sinh viên", font=("Arial", 10, "bold")) 
lbl_ds.pack(pady=5, anchor="w", padx=10) 
 
columns = ("Mssv", "Họ và tên", "Giới tính", "Ngày sinh", "khoa", "Lớp") 
tree = ttk.Treeview(root, columns=columns, show="headings", height=10) 
 
for col in columns: 
    tree.heading(col, text=col.capitalize()) 
 
tree.column("Mssv", width=60, anchor="center") 
tree.column("Họ và tên", width=120, anchor="center") 
tree.column("Giới tính", width=50, anchor="center") 
tree.column("Ngày sinh", width=80, anchor="center") 
tree.column("khoa", width=120, anchor="center")
tree.column("Lớp", width=80, anchor="center") 
 
tree.pack(padx=10, pady=5, fill="both") 

# ====== Chức năng CRUD ====== 
def clear_input(): 
    entry_mssv.delete(0, tk.END) 
    entry_hoten.delete(0, tk.END) 
    gender_var.set("Nam") 
    entry_date.set_date("2000-01-01") 
    cbb_khoa.set("") 
    entry_lop.delete(0, tk.END)

def load_data():
    for i in tree.get_children():
        tree.delete(i)
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute("SELECT mssv, hoten, gioitinh, ngaysinh, khoa, lop FROM sinhvien")
    
    for row in cur.fetchall():
        tree.insert("", tk.END, values=row)
    conn.close()

def them_sv():
    mssv = entry_mssv.get()
    hoten = entry_hoten.get()
    gioitinh = gender_var.get()
    ngaysinh = entry_date.get()
    khoa = cbb_khoa.get()
    lop = entry_lop.get()

    if mssv == "" or hoten == "" or khoa == "" or lop == "":
        messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin")
        return

    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO sinhvien VALUES (%s, %s, %s, %s, %s, %s, 0.0, 0.0)",
                      (mssv, hoten, ngaysinh, gioitinh, khoa, lop))
        conn.commit()
        load_data()
        clear_input()
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Lỗi", str(e))
    conn.close()

def xoa_sv(): 
    selected = tree.selection() 
    if not selected: 
        messagebox.showwarning("Chưa chọn", "Hãy chọn sinh viên để xóa", parent=root) 
        return 
        
    # Thêm bước xác nhận cho an toàn
    if not messagebox.askyesno("Xác nhận xóa", 
                             "Bạn có chắc muốn xóa sinh viên này?\n(TOÀN BỘ điểm tích lũy và điểm rèn luyện của sinh viên này cũng sẽ bị xóa vĩnh viễn)", 
                             parent=root):
        return
        
    mssv = tree.item(selected)["values"][0] 
    
    conn = None # Khởi tạo conn
    try:
        conn = connect_db() 
        cur = conn.cursor() 
    
        cur.execute("DELETE FROM diem_tichluy WHERE mssv=%s", (mssv,)) 
        
        cur.execute("DELETE FROM diem_renluyen WHERE mssv=%s", (mssv,))
        
        cur.execute("DELETE FROM sinhvien WHERE mssv=%s", (mssv,)) 
        
        conn.commit() 
        messagebox.showinfo("Thành công", "Đã xóa sinh viên và toàn bộ điểm liên quan.", parent=root)
        
        load_data()
        clear_input()
        
    except Exception as e:
        if conn:
            conn.rollback()
        messagebox.showerror("Lỗi CSDL", f"Không thể xóa: {e}", parent=root)
        
    finally:
        if conn:
            conn.close()

def sua_sv(): 
    selected = tree.selection() 
    if not selected: 
        messagebox.showwarning("Chưa chọn", "Hãy chọn nhân viên để sửa") 
        return 
    values = tree.item(selected)["values"] 
    entry_mssv.delete(0, tk.END) 
    entry_mssv.insert(0, values[0]) 
    entry_hoten.delete(0, tk.END) 
    entry_hoten.insert(0, values[1])  
    gender_var.set(values[2]) 
    entry_date.set_date(values[3]) 
    cbb_khoa.set(values[4])
    entry_lop.delete(0, tk.END) 
    entry_lop.insert(0, values[5])

def luu_sv():
    mssv = entry_mssv.get()
    hoten = entry_hoten.get()
    gioitinh = gender_var.get()
    ngaysinh = entry_date.get()
    khoa = cbb_khoa.get()
    lop = entry_lop.get()
    
    if mssv == "":
        messagebox.showwarning("Lỗi", "Hãy dùng nút 'Sửa' trước khi 'Lưu'")
        return

    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""UPDATE sinhvien SET hoten=%s, gioitinh=%s, ngaysinh=%s, khoa=%s, lop=%s
                  WHERE mssv=%s""",
                  (hoten, gioitinh, ngaysinh, khoa, lop, mssv))
    conn.commit()
    conn.close()
    load_data()
    clear_input()
# ====== Frame nút ====== 
frame_btn = tk.Frame(root) 
frame_btn.pack(pady=5) 
 
tk.Button(frame_btn, text="Thêm", width=8, command=them_sv).grid(row=0, column=0, padx=5) 
tk.Button(frame_btn, text="Lưu", width=8, command=luu_sv).grid(row=0, column=1, padx=5) 
tk.Button(frame_btn, text="Sửa", width=8, command=sua_sv).grid(row=0, column=2, padx=5) 
tk.Button(frame_btn, text="Hủy", width=8, command=clear_input).grid(row=0, column=3, padx=5) 
tk.Button(frame_btn, text="Xóa", width=8, command=xoa_sv).grid(row=0, column=4, padx=5) 
tk.Button(frame_btn, text="Thoát", width=8, command=root.quit).grid(row=0, column=5, padx=5) 

# ====== Nút mở form KQHT và Chi Tiết Điểm ======
tk.Button(frame_btn, text="Kết quả học tập", width=20, 
          command=lambda: open_KQHT(root)).grid(row=1, column=0, columnspan=2, pady=5)
tk.Button(frame_btn, text="Chỉnh Sửa Điểm Tích Lũy", width=20, 
          command=lambda: open_ChiTietDiem(root)).grid(row=1, column=2, columnspan=2, pady=5)
tk.Button(frame_btn, text="Chỉnh Sửa Điểm Rèn Luyện", width=20, 
          command=lambda: open_ChiTietDiemRenLuyen(root)).grid(row=1, column=4, columnspan=2, pady=5)
 
load_data() 
root.mainloop()
