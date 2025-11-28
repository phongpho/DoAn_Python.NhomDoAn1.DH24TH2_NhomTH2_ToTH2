import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import mysql.connector
import pandas as pd
from DatabaseConnection import connect_db
from DatabaseConnection import center_window

def open_KQHT(main_root):
    form2_win = tk.Toplevel(main_root)
    form2_win.title("Tra cứu Kết quả Học tập")
    center_window(form2_win, 1200, 700) 
    form2_win.resizable(False, False)
    form2_win.grab_set()
    form2_win.config(bg="white")

    frame_sidebar = tk.Frame(form2_win, relief=tk.RIDGE, bd=2, padx=10, pady=10, bg="#EAF2F8")
    frame_sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

    lbl_sidebar_title = tk.Label(frame_sidebar, text="BỘ LỌC TRA CỨU", 
                                 font=("Arial", 16, "bold"), 
                                 bg="#2874A6", fg="white")
    lbl_sidebar_title.pack(pady=(5, 15), fill=tk.X)

    frame_info = tk.Frame(frame_sidebar, bg="#EAF2F8")
    frame_info.pack(pady=5, padx=10)

    tk.Label(frame_info, text="Chọn khoa", bg="#EAF2F8", fg="#333333").grid(row=0, column=0, padx=5, pady=10, sticky="w")
    cbb_khoa = ttk.Combobox(frame_info, width=30)
    cbb_khoa.grid(row=0, column=1, padx=5, pady=10, sticky="w") 

    tk.Label(frame_info, text="Chọn sinh viên", bg="#EAF2F8", fg="#333333").grid(row=1, column=0, padx=5, pady=10, sticky="w")
    cbb_sinhvien = ttk.Combobox(frame_info, width=30)
    cbb_sinhvien.grid(row=1, column=1, padx=5, pady=10, sticky="w") 

    tk.Label(frame_info, text="Chọn để lọc", bg="#EAF2F8", fg="#333333").grid(row=2, column=0, padx=5, pady=10, sticky="w")
    cbb_loai = ttk.Combobox(frame_info, width=30, 
                            values=["Xuất sắc", "Giỏi", "Khá", "Trung bình", "Yếu", "Yếu (DRL < 50)"])
    cbb_loai.grid(row=2, column=1, padx=5, pady=10, sticky="w") 


    btn_loc_ngay = tk.Button(frame_info, text="LỌC NGAY", bg="#FFC107", fg="#333333", font=("Arial", 9, "bold"), width=25)
    btn_loc_ngay.grid(row=3, column=1, padx=5, pady=5)

    frame_btn = tk.Frame(frame_sidebar, bg="#EAF2F8")
    frame_btn.pack(pady=20, fill=tk.X)
    

    sinhvien_data = {} 

    def load_tree_data(khoa_filter=None, mssv_filter=None, loai_filter=None, load_all=False): 
        for i in tree.get_children():
            tree.delete(i)
        
        if not khoa_filter and not mssv_filter and not loai_filter and not load_all:
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
                

                if loai_filter and loai != loai_filter:
                    continue 

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
        cbb_loai.set("") 
        load_tree_data(khoa_filter=khoa_chon)

    def sinhvien_select(event):
        sv_chon = cbb_sinhvien.get()
        mssv = sinhvien_data.get(sv_chon)
        if not mssv:
            return
        cbb_loai.set("") 
        load_tree_data(mssv_filter=mssv)

    def xu_ly_loc_theo_loai():
        loai_chon = cbb_loai.get()
        khoa_chon = cbb_khoa.get()
        
        if not loai_chon:
            messagebox.showinfo("Nhắc nhở", "Vui lòng chọn loại xếp hạng cần lọc!", parent=form2_win)
            return

        if khoa_chon:
            load_tree_data(khoa_filter=khoa_chon, loai_filter=loai_chon)
        else:
            load_tree_data(load_all=True, loai_filter=loai_chon)


    btn_loc_ngay.config(command=xu_ly_loc_theo_loai)


    def reset_view():
        cbb_khoa.set("")
        cbb_sinhvien['values'] = []
        cbb_sinhvien.set("")
        cbb_loai.set("") 
        sinhvien_data.clear()
        for i in tree.get_children():
            tree.delete(i)

    def tai_tat_ca():
        cbb_khoa.set("")
        cbb_sinhvien['values'] = []
        cbb_sinhvien.set("")
        cbb_loai.set("")
        sinhvien_data.clear()
        load_tree_data(load_all=True)

    def xep_loai_hoc_tap(dtl, drl):
        if drl < 50:
            return "Yếu (DRL < 50)"
        
        if dtl >= 9.0: dtl_he_4 = 4.0
        elif dtl >= 8.5: dtl_he_4 = 3.7
        elif dtl >= 8.0: dtl_he_4 = 3.5
        elif dtl >= 7.0: dtl_he_4 = 3.0
        elif dtl >= 6.5: dtl_he_4 = 2.5
        elif dtl >= 5.5: dtl_he_4 = 2.0
        elif dtl >= 5.0: dtl_he_4 = 1.5
        elif dtl >= 4.0: dtl_he_4 = 1.0
        else: dtl_he_4 = 0.0

        if dtl_he_4 >= 3.6: return "Xuất sắc"
        elif dtl_he_4 >= 3.2: return "Giỏi"
        elif dtl_he_4 >= 2.5: return "Khá"
        elif dtl_he_4 >= 2.0: return "Trung bình"
        else: return "Yếu"

    def xuat_excel():
        if len(tree.get_children()) < 1:
            messagebox.showwarning("Thông báo", "Không có dữ liệu để xuất!", parent=form2_win)
            return
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All files", "*.*")],
            title="Lưu file Excel",
            parent=form2_win
        )

        if file_path:
            try:
                data = []
                for row_id in tree.get_children():
                    row_values = tree.item(row_id)["values"]
                    data.append(row_values)

                columns = ["MSSV", "Họ tên", "Khoa", "Lớp", "ĐRL", "ĐTL", "Xếp loại"] 
                
                df = pd.DataFrame(data, columns=columns)
                df.to_excel(file_path, index=False)
                messagebox.showinfo("Thành công", f"Đã xuất file thành công tại:\n{file_path}", parent=form2_win)
            except Exception as e:
                messagebox.showerror("Lỗi", f"Không thể xuất file: {e}", parent=form2_win)  

    tk.Button(frame_btn, text="Tải Tất Cả", command=tai_tat_ca, 
              bg="#2874A6", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold"), height=2).pack(fill=tk.X, pady=4)
    
    tk.Button(frame_btn, text="Xóa Bảng", command=reset_view, 
              bg="#2874A6", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold"), height=2).pack(fill=tk.X, pady=4)
    
    tk.Button(frame_btn, text="Xuất File Excel", command=xuat_excel, 
              bg="#217346", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold"), height=2).pack(fill=tk.X, pady=4)
    
    tk.Button(frame_btn, text="Thoát", command=form2_win.destroy, 
              bg="#DC3545", fg="white", relief=tk.FLAT, font=("Arial", 9, "bold"), height=2).pack(fill=tk.X, pady=4)


    frame_main = tk.Frame(form2_win, padx=10, pady=10, bg="white") 
    frame_main.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    lbl_title = tk.Label(frame_main, text="BẢNG ĐIỂM TỔNG HỢP", 
                         font=("Arial", 18, "bold"), bg="white", fg="#2874A6")
    lbl_title.pack(pady=(5, 15))

    style = ttk.Style(form2_win)
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

    columns = ("Mssv", "Họ và tên", "Khoa", "Lớp", "DRL", "DTL", "XepLoai")
    tree = ttk.Treeview(frame_main, columns=columns, show="headings", height=10)
    
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

    cbb_khoa.bind("<<ComboboxSelected>>", khoa_select)
    cbb_sinhvien.bind("<<ComboboxSelected>>", sinhvien_select)


    load_cbb_khoa()