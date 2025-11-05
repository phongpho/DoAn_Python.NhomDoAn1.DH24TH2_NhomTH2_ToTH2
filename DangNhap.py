import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  
from QuanLiSinhVien import open_main_window 
from DatabaseConnection import center_window

def check_login():
    username = entry_user.get()
    password = entry_pass.get()

    if username == "admin" and password == "123":
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Lỗi Đăng Nhập", "Tên người dùng hoặc mật khẩu không đúng!")

login_window = tk.Tk()
login_window.title("Đăng nhập - Quản lý sinh viên")
login_window.geometry("800x600")
center_window(login_window, 800, 600)
login_window.resizable(False, False)

try:
    bg_image = Image.open("background.jpg")
    bg_image = bg_image.resize((800, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    bg_label = tk.Label(login_window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"Lỗi tải ảnh nền: {e}. Dùng nền trơn.")
    login_window.config(bg="#F0F0F0")

login_frame = tk.Frame(login_window, bg="white", relief="solid", bd=1)
login_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400)

try:
    logo_image = Image.open("logo_agu.jpg")
    logo_image = logo_image.resize((100, 100), Image.LANCZOS) 
    logo_photo = ImageTk.PhotoImage(logo_image)
    
    logo_label = tk.Label(login_frame, image=logo_photo, bg="white")
    logo_label.pack(pady=(20, 10))
except Exception as e:
    print(f"Lỗi tải logo: {e}")

title_label = tk.Label(login_frame, text="HỆ THỐNG QUẢN LÝ SINH VIÊN", font=("Arial", 16, "bold"), bg="white")
title_label.pack(pady=10)

user_label = tk.Label(login_frame, text="Tên người dùng", font=("Arial", 12), bg="white")
user_label.pack(pady=(10, 5))

entry_user = tk.Entry(login_frame, font=("Arial", 12), width=30)
entry_user.pack()

pass_label = tk.Label(login_frame, text="Mật khẩu", font=("Arial", 12), bg="white")
pass_label.pack(pady=(10, 5))

entry_pass = tk.Entry(login_frame, font=("Arial", 12), width=30, show="*")
entry_pass.pack()

login_button = tk.Button(login_frame, text="Đăng nhập", font=("Arial", 12, "bold"), 
                         width=28, command=check_login, bg="#0078D4", fg="white")
login_button.pack(pady=20)

login_window.mainloop()