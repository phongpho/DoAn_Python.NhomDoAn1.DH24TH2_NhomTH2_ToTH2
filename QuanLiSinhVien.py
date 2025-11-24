import tkinter as tk 
from tkinter import ttk, messagebox 
from tkcalendar import DateEntry 
import mysql.connector 
from DatabaseConnection import connect_db
from DatabaseConnection import center_window
from KetQuaHocTap_form import open_KQHT
from ChiTietDiemTichLuy_form import open_ChiTietDiemTichLuy
from ChiTietDiemRenluyen_form import open_ChiTietDiemRenLuyen
def open_main_window():

    root = tk.Tk()
    root.title("Hệ Thống Quản Lý Sinh Viên")
    center_window(root, 1000, 640)
    root.resizable(False, False)
    root.config(bg="white")
#frame sidebar
    frame_sidebar = tk.Frame(root, relief=tk.RIDGE, bd=2, padx=10, pady=10, bg="#EAF2F8")
    frame_sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
    lbl_sidebar_title = tk.Label(frame_sidebar, text="THÔNG TIN SINH VIÊN",
                                font=("Arial", 16, "bold"),
                                bg="#2874A6", fg="white")
    lbl_sidebar_title.pack(pady=(5, 15), fill=tk.X)
    #frame info
    frame_info = tk.Frame(frame_sidebar, bg="#EAF2F8")
    frame_info.pack(pady=5, padx=10)

    tk.Label(frame_info, text="Mã số sinh viên", bg="#EAF2F8", fg="#333333").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    entry_mssv = tk.Entry(frame_info, width=30, bg="white", fg="#333333")
    entry_mssv.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Họ tên sinh viên", bg="#EAF2F8", fg="#333333").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    entry_hoten = tk.Entry(frame_info, width=30, bg="white", fg="#333333")
    entry_hoten.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Khoa", bg="#EAF2F8", fg="#333333").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    cbb_khoa = ttk.Combobox(frame_info, values=[ "Công Nghệ Thông Tin", "Du Lịch Và Văn Hóa Nghệ Thuật",
                                                "Nông Nghiệp - Tài Nguyên Thiên Nhiên", "Sư Phạm",
                                                "Kinh Tế - Quản Trị Kinh Doanh", "Kỹ Thuật - Công Nghệ - Môi Trường",
                                                "Ngoại Ngữ", "Luật - Khoa Học Chính Trị "], width=28)
    cbb_khoa.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Lớp", bg="#EAF2F8", fg="#333333").grid(row=3, column=0, padx=5, pady=5, sticky="w")
    entry_lop = tk.Entry(frame_info, width=30, bg="white", fg="#333333")
    entry_lop.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame_info, text="Giới tính", bg="#EAF2F8", fg="#333333").grid(row=4, column=0, padx=5, pady=5, sticky="w")
    gender_var = tk.StringVar(value="Nam")

    frame_gender = tk.Frame(frame_info, bg="#EAF2F8")
    frame_gender.grid(row=4, column=1, sticky="w")

    tk.Radiobutton(frame_gender, text="Nam", variable=gender_var, value="Nam", bg="#EAF2F8", fg="#333333", activebackground="#EAF2F8").pack(side=tk.LEFT, padx=5)
    tk.Radiobutton(frame_gender, text="Nữ", variable=gender_var, value="Nữ", bg="#EAF2F8", fg="#333333", activebackground="#EAF2F8").pack(side=tk.LEFT, padx=10)

    tk.Label(frame_info, text="Ngày sinh", bg="#EAF2F8", fg="#333333").grid(row=5, column=0, padx=5, pady=5, sticky="w")
    entry_date = DateEntry(frame_info, width=12, background="#2874A6", foreground="white",
                        date_pattern="yyyy-mm-dd", headersbackground="#2874A6",
                        selectbackground="#2874A6")
    entry_date.grid(row=5, column=1, padx=5, pady=5, sticky="w")
   
    #frame button CRUD
    frame_btn_crud = tk.Frame(frame_sidebar, bg="#EAF2F8")
    frame_btn_crud.pack(pady=10, fill=tk.X)
    tk.Button(frame_btn_crud, text="Tải Dữ Liệu", command=lambda: load_data(), height=2, bg="#32AC10", fg="white", font=("Arial", 9, "bold"), relief=tk.FLAT).pack(fill=tk.X, pady=3)
    tk.Button(frame_btn_crud, text="Thêm", command=lambda: them_sv(), height=2, bg="#007BFF", fg="white", font=("Arial", 9, "bold"), relief=tk.FLAT).pack(fill=tk.X, pady=3)
    tk.Button(frame_btn_crud, text="Lưu", command=lambda: luu_sv(), height=2, bg="#007BFF", fg="white", font=("Arial", 9, "bold"), relief=tk.FLAT).pack(fill=tk.X, pady=3)
    tk.Button(frame_btn_crud, text="Sửa", command=lambda: sua_sv(), height=2, bg="#007BFF", fg="white", font=("Arial", 9, "bold"), relief=tk.FLAT).pack(fill=tk.X, pady=3)
    tk.Button(frame_btn_crud, text="Hủy", command=lambda: clear_input(), height=2, bg="#007BFF", fg="white", font=("Arial", 9, "bold"), relief=tk.FLAT).pack(fill=tk.X, pady=3)
    tk.Button(frame_btn_crud, text="Xóa", command=lambda: xoa_sv(), height=2, bg="#DC3545", fg="white", font=("Arial", 9, "bold"), relief=tk.FLAT).pack(fill=tk.X, pady=3)
    tk.Button(frame_btn_crud, text="Tìm Kiếm", command=lambda: timkiem(), height=2, bg="#FFC107", fg="white", font=("Arial", 9, "bold"), relief=tk.FLAT).pack(fill=tk.X, pady=3)
#frame main
    frame_main = tk.Frame(root, padx=10, pady=10, bg="white") 
    frame_main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    lbl_title = tk.Label(frame_main, text="HỆ THỐNG QUẢN LÝ SINH VIÊN\n TRƯỜNG ĐẠI HỌC AN GIANG", font=("Arial", 18, "bold"), bg="white", fg="#2874A6") 
    lbl_title.pack(pady=(5, 15)) 

    lbl_ds = tk.Label(frame_main, text="Danh sách sinh viên", font=("Arial", 10, "bold"), bg="white", fg="#333333") 
    lbl_ds.pack(pady=5, anchor="w", padx=10) 

    style = ttk.Style(root)
    style.theme_use("default") 
    style.configure("Treeview", 
                    background="white", 
                    fieldbackground="white", 
                    foreground="black",
                    rowheight=25,
                    bd=1, relief=tk.SOLID)
    style.map("Treeview", background=[('selected', '#AED6F1')]) 
    style.configure("Treeview.Heading", 
                    font=("Arial", 10, "bold"), 
                    background="#EAF2F8", 
                    foreground="black",
                    relief=tk.FLAT)

    columns = ("Mssv", "Họ và tên", "Ngày sinh", "Giới tính", "khoa", "Lớp") 
    tree = ttk.Treeview(frame_main, columns=columns, show="headings", height=10) 

    for col in columns: 
        tree.heading(col, text=col.capitalize()) 

    tree.column("Mssv", width=60, anchor="center") 
    tree.column("Họ và tên", width=100)
    tree.column("Ngày sinh", width=80, anchor="center") 
    tree.column("Giới tính", width=50, anchor="center") 
    tree.column("khoa", width=140)
    tree.column("Lớp", width=80, anchor="center") 

    tree.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
    #frame button mở rộng
    frame_Button_Morong = tk.Frame(frame_main, bg="white") 
    frame_Button_Morong.pack(pady=10)

    tk.Button(frame_Button_Morong, text="Kết quả học tập", width=20, 
            command=lambda: open_KQHT(root), bg="#2874A6", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold")).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(frame_Button_Morong, text="Chỉnh Sửa Điểm Tích Lũy", width=22, 
            command=lambda: open_ChiTietDiemTichLuy(root), bg="#2874A6", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold")).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(frame_Button_Morong, text="Chỉnh Sửa Điểm Rèn Luyện", width=22, 
            command=lambda: open_ChiTietDiemRenLuyen(root), bg="#2874A6", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold")).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(frame_Button_Morong, text="Thoát", width=12, command=root.quit, bg="#DC3545", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold")).grid(row=0, column=3, padx=10, pady=5)

    def clear_input(): 
        entry_mssv.delete(0, tk.END) 
        entry_hoten.delete(0, tk.END) 
        gender_var.set("Nam") 
        entry_date.set_date("2000-01-01") 
        cbb_khoa.set("") 
        entry_lop.delete(0, tk.END)
        if tree.selection():
            tree.selection_remove(tree.selection()[0])

    def load_data():
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT mssv, hoten, ngaysinh, gioitinh, khoa, lop FROM sinhvien")
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
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập đủ thông tin", parent=root)
            return

        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO sinhvien (mssv, hoten, ngaysinh, gioitinh, khoa, lop, drl, dtl) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (mssv, hoten, ngaysinh, gioitinh, khoa, lop, 0.0, 0.0))
            conn.commit()
            load_data()
            clear_input()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi", str(e), parent=root)
        conn.close()

    def xoa_sv(): 
        selected = tree.selection() 
        if not selected: 
            messagebox.showwarning("Chưa chọn", "Hãy chọn sinh viên để xóa", parent=root) 
            return 
        if not messagebox.askyesno("Xác nhận xóa", 
                                "Bạn có chắc muốn xóa sinh viên này?\n(TOÀN BỘ điểm tích lũy và điểm rèn luyện của sinh viên này cũng sẽ bị xóa vĩnh viễn)", 
                                parent=root):
            return
            
        mssv = tree.item(selected)["values"][0] 
        
        conn = None
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
            messagebox.showwarning("Chưa chọn", "Hãy chọn sinh viên để sửa", parent=root) 
            return 
        values = tree.item(selected)["values"]

        entry_mssv.delete(0, tk.END) 
        entry_hoten.delete(0, tk.END) 
        entry_lop.delete(0, tk.END)


        entry_mssv.insert(0, values[0]) 
        entry_hoten.insert(0, values[1]) 
        entry_date.set_date(values[2])
        gender_var.set(values[3])
        cbb_khoa.set(values[4])
        entry_lop.insert(0, values[5])

    def luu_sv():
        mssv = entry_mssv.get()
        hoten = entry_hoten.get()
        gioitinh = gender_var.get()
        ngaysinh = entry_date.get()
        khoa = cbb_khoa.get()
        lop = entry_lop.get()
        
        if mssv == "":
            messagebox.showwarning("Lỗi", "Hãy dùng nút 'Sửa' trước khi 'Lưu'", parent=root)
            return

        conn = connect_db()
        cur = conn.cursor()
        try:
            cur.execute("""UPDATE sinhvien SET hoten=%s, ngaysinh=%s, gioitinh=%s, khoa=%s, lop=%s
                        WHERE mssv=%s""",
                        (hoten, ngaysinh, gioitinh, khoa, lop, mssv))
            conn.commit()
            load_data()
            clear_input()
        except Exception as e:
            conn.rollback()
            messagebox.showerror("Lỗi CSDL", f"Lỗi khi lưu: {e}", parent=root)
        finally:
            conn.close()

    def on_tree_select(event):
        selected = tree.selection()
        if not selected:
            return
        sua_sv()
    def timkiem():
        mssv = entry_mssv.get()
        if mssv == "":
            messagebox.showwarning("Thiếu dữ liệu", "Vui lòng nhập Mã số sinh viên để tìm kiếm", parent=root)
            return
        for i in tree.get_children():
            tree.delete(i)
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT mssv, hoten, ngaysinh, gioitinh, khoa, lop FROM sinhvien WHERE mssv = %s", (mssv,))
        results = cur.fetchall()
        if not results:
            messagebox.showinfo("Không tìm thấy", "Không tìm thấy sinh viên với Mã số đã nhập", parent=root)
        for row in results:
            tree.insert("", tk.END, values=row)
        conn.close()
    tree.bind("<<TreeviewSelect>>", on_tree_select)
    # load_data() 
    root.mainloop()