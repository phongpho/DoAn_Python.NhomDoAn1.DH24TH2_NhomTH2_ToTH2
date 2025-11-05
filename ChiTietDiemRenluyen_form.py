import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from DatabaseConnection import connect_db
from DatabaseConnection import center_window

def open_ChiTietDiemRenLuyen(main_root):

    form4_win = tk.Toplevel(main_root)
    form4_win.title("Quản lý Điểm rèn luyện theo Học kỳ")
    center_window(form4_win, 1200, 700)
    form4_win.resizable(False, False)
    form4_win.grab_set()
    form4_win.config(bg="white")

    frame_sidebar = tk.Frame(form4_win, relief=tk.RIDGE, bd=2, padx=10, pady=10, bg="#EAF2F8")
    frame_sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    lbl_sidebar_title = tk.Label(frame_sidebar, text="NHẬP ĐIỂM RÈN LUYỆN", 
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

    tk.Label(frame_info, text="Chọn Học Kỳ", bg="#EAF2F8", fg="#333333").grid(row=2, column=0, padx=5, pady=10, sticky="w")
    cbb_hocky = ttk.Combobox(frame_info, width=30)
    cbb_hocky.grid(row=2, column=1, padx=5, pady=10, sticky="w")
    
    hocky_list = [
        "Học kỳ 1 (Năm 1)",
        "Học kỳ 2 (Năm 1)",
        "Học kỳ 3 (Năm 2)",
        "Học kỳ 4 (Năm 2)",
        "Học kỳ 5 (Năm 3)",
        "Học kỳ 6 (Năm 3)",
        "Học kỳ 7 (Năm 4)",
        "Học kỳ 8 (Năm 4)",
    ]
    cbb_hocky['values'] = hocky_list

    tk.Label(frame_info, text="Nhập điểm rèn luyện", bg="#EAF2F8", fg="#333333").grid(row=3, column=0, padx=5, pady=10, sticky="w")
    entry_diem = tk.Entry(frame_info, width=10)
    entry_diem.grid(row=3, column=1, padx=5, pady=10, sticky="w")

    frame_btn = tk.Frame(frame_sidebar, bg="#EAF2F8")
    frame_btn.pack(pady=20, fill=tk.X)
    
    tk.Button(frame_btn, text="Lưu Điểm", command=lambda: luu_drl(),
              bg="#28A745", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold"), height=2).pack(fill=tk.X, pady=4)
    tk.Button(frame_btn, text="Xóa Điểm", command=lambda: xoa_drl(),
              bg="#DC3545", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold"), height=2).pack(fill=tk.X, pady=4)
    tk.Button(frame_btn, text="Hủy", command=lambda: clear_input(),
              bg="#6C757D", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold"), height=2).pack(fill=tk.X, pady=4)
    tk.Button(frame_btn, text="Thoát", command=form4_win.destroy,
              bg="#6C757D", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold"), height=2).pack(fill=tk.X, pady=4)

    frame_main = tk.Frame(form4_win, padx=10, pady=10, bg="white") 
    frame_main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
    
    lbl_title = tk.Label(frame_main, text="QUẢN LÝ ĐIỂM RÈN LUYỆN", 
                         font=("Arial", 18, "bold"), bg="white", fg="#2874A6")
    lbl_title.pack(pady=(5, 15))

    lbl_ds = tk.Label(frame_main, text="Danh sách điểm đã có (chọn sinh viên để xem)", 
                      font=("Arial", 10, "bold"), bg="white", fg="#333333")
    lbl_ds.pack(pady=5, anchor="w", padx=10)

    style = ttk.Style(form4_win)
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
    
    columns = ("Mssv", "Hoten", "Hocky", "Diemrenluyen")
    tree = ttk.Treeview(frame_main, columns=columns, show="headings", height=10)

    tree.heading("Mssv", text="MSSV")
    tree.heading("Hoten", text="Họ tên")
    tree.heading("Hocky", text="Học kỳ")
    tree.heading("Diemrenluyen", text="Điểm Rèn Luyện")
    
    tree.column("Mssv", width=80, anchor="center")
    tree.column("Hoten", width=250)
    tree.column("Hocky", width=120, anchor="center")
    tree.column("Diemrenluyen", width=100, anchor="center")

    tree.pack(padx=10, pady=5, fill="both", expand=True)
    
    student_data = {} 
    
    def load_cbb_khoa():
        try:
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT DISTINCT khoa FROM sinhvien WHERE khoa IS NOT NULL AND khoa != ''")
            khoa_list = [row[0] for row in cur.fetchall()]
            cbb_khoa['values'] = khoa_list
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải ComboBox Khoa: {e}", parent=form4_win)

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
            messagebox.showerror("Lỗi CSDL", f"Không thể tải ComboBox Sinh viên: {e}", parent=form4_win)

    def on_khoa_select(event):
        khoa_chon = cbb_khoa.get()
        if not khoa_chon:
            return
            
        load_cbb_sv(khoa_chon)
        
        cbb_hocky.set("")
        entry_diem.delete(0, tk.END)
        for i in tree.get_children():
            tree.delete(i)

    def load_tree_data(mssv):
        for i in tree.get_children():
            tree.delete(i)
        
        try:
            conn = connect_db()
            cur = conn.cursor()
            sql = """SELECT s.mssv, s.hoten, drl.hocky, drl.diem
                     FROM diem_renluyen drl
                     JOIN sinhvien s ON drl.mssv = s.mssv
                     WHERE drl.mssv = %s
                     ORDER BY drl.hocky"""
            cur.execute(sql, (mssv,))
            
            for row in cur.fetchall():
                tree.insert("", tk.END, values=row)
            conn.close()
        except Exception as e:
            messagebox.showerror("Lỗi CSDL", f"Không thể tải bảng điểm DRL: {e}", parent=form4_win)

    def on_student_select(event):
        selected_display = cbb_sinhvien.get()
        mssv = student_data.get(selected_display)
        if not mssv:
            for i in tree.get_children():
                tree.delete(i)
            return
        load_tree_data(mssv)
    
    def on_tree_select(event):
        selected = tree.selection()
        if not selected:
            return
        
        item = tree.item(selected[0])
        values = item["values"]
        
        cbb_hocky.set(values[2])
        entry_diem.delete(0, tk.END)
        entry_diem.insert(0, values[3])

    def update_avg_drl(cursor, mssv):
        sql_cal_drl = "SELECT AVG(diem) FROM diem_renluyen WHERE mssv = %s"
        cursor.execute(sql_cal_drl, (mssv,))
        result = cursor.fetchone()
        
        new_drl_avg = result[0] if result[0] is not None else 0
        
        sql_update_drl = "UPDATE sinhvien SET drl = %s WHERE mssv = %s"
        cursor.execute(sql_update_drl, (new_drl_avg, mssv))

    def clear_input():
        cbb_khoa.set("")
        cbb_sinhvien.set("")
        cbb_sinhvien['values'] = []
        cbb_hocky.set("")
        entry_diem.delete(0, tk.END)
        student_data.clear()
        for i in tree.get_children():
            tree.delete(i)

    def luu_drl():
        selected_sv = cbb_sinhvien.get()
        hocky = cbb_hocky.get()
        diem_str = entry_diem.get()
        
        mssv = student_data.get(selected_sv)
        
        if not mssv or not hocky:
            messagebox.showwarning("Thiếu thông tin", "Vui lòng chọn Sinh viên và Học kỳ.", parent=form4_win)
            return
        
        try:
            diem = float(diem_str)
            if not (0 <= diem <= 100):
                raise ValueError("Điểm phải từ 0-100")
        except ValueError:
            messagebox.showerror("Lỗi dữ liệu", "Điểm rèn luyện phải là số hợp lệ (từ 0 đến 100).", parent=form4_win)
            return
            
        conn = None
        try:
            conn = connect_db()
            cur = conn.cursor()
            
            cur.execute("SELECT COUNT(*) FROM diem_renluyen WHERE mssv = %s AND hocky = %s", (mssv, hocky))
            exists = cur.fetchone()[0]
            
            if exists:
                cur.execute("UPDATE diem_renluyen SET diem = %s WHERE mssv = %s AND hocky = %s", (diem, mssv, hocky))
            else:
                cur.execute("INSERT INTO diem_renluyen (mssv, hocky, diem) VALUES (%s, %s, %s)", (mssv, hocky, diem))
            
            update_avg_drl(cur, mssv)
            
            conn.commit()
            messagebox.showinfo("Thành công", "Lưu điểm DRL thành công!", parent=form4_win)
            
            load_tree_data(mssv) 
            cbb_hocky.set("")
            entry_diem.delete(0, tk.END)

        except Exception as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Lỗi CSDL", f"Không thể lưu điểm DRL: {e}", parent=form4_win)
        finally:
            if conn:
                conn.close()

    def xoa_drl():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Chưa chọn", "Vui lòng chọn một học kỳ trong bảng để xóa.", parent=form4_win)
            return
            
        values = tree.item(selected_item)["values"]
        mssv = values[0]
        hocky = values[2]

        if not messagebox.askyesno("Xác nhận xóa", f"Bạn có chắc muốn xóa điểm DRL học kỳ '{hocky}' của sinh viên này không?", parent=form4_win):
            return

        conn = None
        try:
            conn = connect_db()
            cur = conn.cursor()
            
            cur.execute("DELETE FROM diem_renluyen WHERE mssv = %s AND hocky = %s", (mssv, hocky))
            
            update_avg_drl(cur, mssv)
            
            conn.commit()
            messagebox.showinfo("Thành công", "Đã xóa điểm và cập nhật lại DRL trung bình.", parent=form4_win)
            
            load_tree_data(mssv)

        except Exception as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Lỗi CSDL", f"Không thể xóa điểm DRL: {e}", parent=form4_win)
        finally:
            if conn:
                conn.close()

    cbb_khoa.bind("<<ComboboxSelected>>", on_khoa_select)
    cbb_sinhvien.bind("<<ComboboxSelected>>", on_student_select)
    tree.bind("<<TreeviewSelect>>", on_tree_select)
    
    load_cbb_khoa()