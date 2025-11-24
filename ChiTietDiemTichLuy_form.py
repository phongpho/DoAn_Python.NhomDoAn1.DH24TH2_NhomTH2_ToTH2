import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from DatabaseConnection import connect_db
from DatabaseConnection import center_window

def open_ChiTietDiemTichLuy(main_root):
    
    form3_win = tk.Toplevel(main_root)
    form3_win.title("Quản lý Điểm Tích Lũy Chi Tiết")
    center_window(form3_win, 1200, 700) 
    form3_win.resizable(False, False)
    form3_win.grab_set()
    form3_win.config(bg="white")

    frame_sidebar = tk.Frame(form3_win, relief=tk.RIDGE, bd=2, padx=10, pady=10, bg="#EAF2F8")
    frame_sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    lbl_sidebar_title = tk.Label(frame_sidebar, text="NHẬP ĐIỂM", 
                                 font=("Arial", 16, "bold"), 
                                 bg="#2874A6", fg="white")
    lbl_sidebar_title.pack(pady=(5, 15), fill=tk.X)

    frame_info = tk.Frame(frame_sidebar, bg="#EAF2F8")
    frame_info.pack(pady=5, padx=10)

    tk.Label(frame_info, text="Chọn Khoa", bg="#EAF2F8", fg="#333333").grid(row=0, column=0, padx=5, pady=10, sticky="w")
    cbb_khoa = ttk.Combobox(frame_info, width=30)
    cbb_khoa.grid(row=0, column=1, padx=5, pady=10, sticky="w")

    tk.Label(frame_info, text="Chọn Sinh viên", bg="#EAF2F8", fg="#333333").grid(row=1, column=0, padx=5, pady=10, sticky="w")
    cbb_sinhvien = ttk.Combobox(frame_info, width=30)
    cbb_sinhvien.grid(row=1, column=1, padx=5, pady=10, sticky="w")
    
    tk.Label(frame_info, text="Chọn Môn học", bg="#EAF2F8", fg="#333333").grid(row=2, column=0, padx=5, pady=10, sticky="w")
    cbb_monhoc = ttk.Combobox(frame_info, width=30)
    cbb_monhoc.grid(row=2, column=1, padx=5, pady=10, sticky="w")

    tk.Label(frame_info, text="Điểm môn (Hệ 10)", bg="#EAF2F8", fg="#333333").grid(row=3, column=0, padx=5, pady=10, sticky="w")
    entry_diem = tk.Entry(frame_info, width=10)
    entry_diem.grid(row=3, column=1, padx=5, pady=10, sticky="w")

    frame_btn = tk.Frame(frame_sidebar, bg="#EAF2F8")
    frame_btn.pack(pady=20, fill=tk.X)
    tk.Button(frame_btn, text="Load Dữ Liệu", command=lambda: load_data(), 
              bg="#007BFF", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold"), height=2).pack(fill=tk.X, pady=4)
    tk.Button(frame_btn, text="Lưu Điểm", command=lambda: luu_diem(), 
              bg="#28A745", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold"), height=2).pack(fill=tk.X, pady=4)
    tk.Button(frame_btn, text="Xóa Điểm", command=lambda: xoa_diem(), 
              bg="#DC3545", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold"), height=2).pack(fill=tk.X, pady=4)
    tk.Button(frame_btn, text="Hủy", command=lambda: clear_input(), 
              bg="#6C757D", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold"), height=2).pack(fill=tk.X, pady=4)
    tk.Button(frame_btn, text="Thoát", command=form3_win.destroy, 
              bg="#6C757D", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold"), height=2).pack(fill=tk.X, pady=4)

    frame_main = tk.Frame(form3_win, padx=10, pady=10, bg="white") 
    frame_main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    lbl_title = tk.Label(frame_main, text="QUẢN LÝ ĐIỂM CHI TIẾT", 
                         font=("Arial", 18, "bold"), bg="white", fg="#2874A6")
    lbl_title.pack(pady=(5, 15)) 

    lbl_ds = tk.Label(frame_main, text="Danh sách điểm đã có (chọn sinh viên để xem)", 
                      font=("Arial", 10, "bold"), bg="white", fg="#333333")
    lbl_ds.pack(pady=5, anchor="w", padx=10)

    style = ttk.Style(form3_win)
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

    columns = ("MSSV", "MaMH", "TenMH", "SoTC", "Diem")
    tree = ttk.Treeview(frame_main, columns=columns, show="headings", height=10)


    tree.heading("MSSV", text="MSSV")   
    tree.heading("MaMH", text="Mã Môn Học")
    tree.heading("TenMH", text="Tên Môn Học")
    tree.heading("SoTC", text="Số Tín Chỉ")
    tree.heading("Diem", text="Điểm (Hệ 10)")

    tree.column("MSSV", width=80, anchor="center") 
    tree.column("MaMH", width=80, anchor="center")
    tree.column("TenMH", width=250)
    tree.column("SoTC", width=80, anchor="center")
    tree.column("Diem", width=80, anchor="center")

    tree.pack(padx=10, pady=5, fill="both", expand=True)
    
    student_data = {} 
    monhoc_data = {} 
    
    def load_data():
        try:
            for i in tree.get_children():
                tree.delete(i)
            conn = connect_db()
            cur = conn.cursor() 
            cur.execute("SELECT tl.mssv, mh.mamh, mh.tenmh, mh.sotc, tl.diem_mon "
            "FROM diem_tichluy tl "
            "JOIN monhoc mh ON tl.mamh = mh.mamh"
            " ORDER BY tl.mssv")
            for row in cur.fetchall():
                tree.insert("", tk.END, values=row)
            conn.close()
            
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải dữ liệu: {e}", parent=form3_win)
    def load_cbb_khoa():
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT khoa FROM sinhvien WHERE khoa IS NOT NULL AND khoa != ''")
            khoa_list = [row[0] for row in cur.fetchall()]
            cbb_khoa['values'] = khoa_list
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải ComboBox Khoa: {e}", parent=form3_win)

    def load_cbb_sv(khoa_sv):
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT mssv, hoten FROM sinhvien WHERE khoa = %s", (khoa_sv,))
            
            sv_list = []
            student_data.clear()
            
            for mssv, hoten in cur.fetchall():
                temp_str = f"{mssv} - {hoten}"
                student_data[temp_str] = mssv 
                sv_list.append(temp_str)
                
            cbb_sinhvien['values'] = sv_list
            cbb_sinhvien.set("")
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải ComboBox Sinh viên: {e}", parent=form3_win)

    def load_monhoc_cbb(khoa_sv):
        try:
            monhoc_data.clear()
            cbb_monhoc['values'] = []
            cbb_monhoc.set("")
            
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT mamh, tenmh FROM monhoc WHERE makhoa = %s", (khoa_sv,))
            
            mh_list = []
            for mamh, tenmh in cur.fetchall():
                temp_str = f"{mamh} - {tenmh}"
                monhoc_data[temp_str] = mamh 
                mh_list.append(temp_str)
            cbb_monhoc['values'] = mh_list
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải ComboBox Môn học: {e}", parent=form3_win)

    def on_khoa_select(event):
        khoa_chon = cbb_khoa.get()
        if not khoa_chon:
            return
            
        load_cbb_sv(khoa_chon) 
        load_monhoc_cbb(khoa_chon) 
        
        entry_diem.delete(0, tk.END)
        for i in tree.get_children():
            tree.delete(i)

    def on_student_select(event):
        selected_display = cbb_sinhvien.get()
        mssv = student_data.get(selected_display)
        
        if not mssv:
            for i in tree.get_children():
                tree.delete(i)
            return
            
        load_tree_data(mssv)

    def load_tree_data(mssv):
        for i in tree.get_children():
            tree.delete(i)
        
        try:
            conn = connect_db()
            cur = conn.cursor()

            sql = """SELECT mh.mamh, mh.tenmh, mh.sotc, tl.diem_mon
                     FROM diem_tichluy tl
                     JOIN monhoc mh ON tl.mamh = mh.mamh
                     WHERE tl.mssv = %s"""
            cur.execute(sql, (mssv,))
            
            for row in cur.fetchall():            
                full_row = (mssv,) + row 
                tree.insert("", tk.END, values=full_row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải bảng điểm: {e}", parent=form3_win)
    def clear_input():
        cbb_khoa.set("")
        cbb_sinhvien.set("")
        cbb_sinhvien['values'] = []
        cbb_monhoc.set("")
        cbb_monhoc['values'] = []
        entry_diem.delete(0, tk.END)
        
        student_data.clear()
        monhoc_data.clear()
        
        for i in tree.get_children():
            tree.delete(i)

    def update_dtl(cursor, mssv):
        sql_cal_dtl = """
            SELECT SUM(tl.diem_mon * mh.sotc) / SUM(mh.sotc)
            FROM diem_tichluy tl
            JOIN monhoc mh ON tl.mamh = mh.mamh
            WHERE tl.mssv = %s
        """
        cursor.execute(sql_cal_dtl, (mssv,))
        result = cursor.fetchone()
        
        new_dtl = result[0] if result[0] is not None else 0.0
        
        sql_update_dtl = "UPDATE sinhvien SET dtl = %s WHERE mssv = %s"
        cursor.execute(sql_update_dtl, (new_dtl, mssv))

    def luu_diem():
        selected_sv = cbb_sinhvien.get()
        selected_mh = cbb_monhoc.get()
        diem_str = entry_diem.get()
        
        mssv = student_data.get(selected_sv) 
        mamh = monhoc_data.get(selected_mh)
        
        if not mssv or not mamh:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn Khoa, Sinh viên và Môn học.", parent=form3_win)
            return
        
        try:
            diem_mon = float(diem_str)
            if not (0 <= diem_mon <= 10):
                raise ValueError("Điểm ngoài khoảng 0-10")
        except ValueError:
            messagebox.showerror("Lỗi dữ liệu", "Điểm môn phải là số hợp lệ (từ 0 đến 10).", parent=form3_win)
            return
            
        conn = None
        try:
            conn = connect_db()
            cur = conn.cursor()
            
            cur.execute("SELECT COUNT(*) FROM diem_tichluy WHERE mssv = %s AND mamh = %s", (mssv, mamh))
            exists = cur.fetchone()[0]
            
            if exists:
                if messagebox.askyesno("Xác nhận", "Sinh viên đã có điểm môn này. Bạn muốn cập nhật?", parent=form3_win):
                    cur.execute("UPDATE diem_tichluy SET diem_mon = %s WHERE mssv = %s AND mamh = %s", (diem_mon, mssv, mamh))
                else:
                    conn.close()
                    return
            else:
                cur.execute("INSERT INTO diem_tichluy (mssv, mamh, diem_mon) VALUES (%s, %s, %s)", (mssv, mamh, diem_mon))
            
            update_dtl(cur, mssv)
            conn.commit()
            
            messagebox.showinfo("Thành công", "Lưu điểm và cập nhật DTL thành công!", parent=form3_win)
            
            load_tree_data(mssv)
            cbb_monhoc.set("") 
            entry_diem.delete(0, tk.END) 

        except Exception as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Lỗi CSDL", f"Không thể lưu điểm: {e}", parent=form3_win)
        finally:
            if conn:
                conn.close()

    def xoa_diem():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một môn học trong bảng để xóa.", parent=form3_win)
            return
            
        values = tree.item(selected_item)["values"]

        mamh = values[1]   
        tenmh = values[2]  
        mssv = values[0] 

        if not messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa điểm môn '{tenmh}' của sinh viên {mssv} không?", parent=form3_win):
            return

        conn = None
        try:
            conn = connect_db()
            cur = conn.cursor()
            
            cur.execute("DELETE FROM diem_tichluy WHERE mssv = %s AND mamh = %s", (mssv, mamh))
            update_dtl(cur, mssv) 
            conn.commit()
            
            messagebox.showinfo("Thành công", "Đã xóa điểm và cập nhật lại DTL.", parent=form3_win)
            load_tree_data(mssv) 

        except Exception as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Lỗi CSDL", f"Không thể xóa điểm: {e}", parent=form3_win)
        finally:
            if conn:
                conn.close()

    cbb_khoa.bind("<<ComboboxSelected>>", on_khoa_select)
    cbb_sinhvien.bind("<<ComboboxSelected>>", on_student_select)
    
    load_cbb_khoa()