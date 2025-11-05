import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # Cần thư viện Pillow đã cài ở Bước 0

# Import hàm mở cửa sổ chính từ file của bạn
from QuanLiSinhVien import open_main_window 

# ====== HÀM KIỂM TRA ĐĂNG NHẬP ======
def check_login():
    username = entry_user.get()
    password = entry_pass.get()

    # Đây là tài khoản của bạn
    if username == "nhom1" and password == "12345":
        # Nếu đúng, đóng cửa sổ đăng nhập
        login_window.destroy()
        # Mở cửa sổ quản lý sinh viên
        open_main_window()
    else:
        # Nếu sai, báo lỗi
        messagebox.showerror("Lỗi Đăng Nhập", "Tên người dùng hoặc mật khẩu không đúng!")

# ====== HÀM CANH GIỮA CỬA SỔ ======
def center_window(win, w=700, h=500):
    ws = win.winfo_screenwidth()
    hs = win.winfo_screenheight()
    x = (ws // 2) - (w // 2)
    y = (hs // 2) - (h // 2)
    win.geometry(f'{w}x{h}+{x}+{y}')

# ====== CỬA SỔ ĐĂNG NHẬP CHÍNH ======
login_window = tk.Tk()
login_window.title("Đăng nhập - Quản lý sinh viên")
login_window.geometry("800x600") # Kích thước cửa sổ
center_window(login_window, 800, 600)
login_window.resizable(False, False)

# --- 1. Tải và hiển thị ảnh nền ---
try:
    # Hãy chắc chắn bạn có file "background.jpg" trong thư mục
    bg_image = Image.open("background.jpg")
    bg_image = bg_image.resize((800, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    
    bg_label = tk.Label(login_window, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except Exception as e:
    print(f"Lỗi tải ảnh nền: {e}. Dùng nền trơn.")
    login_window.config(bg="#F0F0F0") # Nền dự phòng nếu không có ảnh

# --- 2. Tạo khung (Frame) trắng ở giữa ---
# Dùng .place() để đặt các widget chồng lên ảnh nền
login_frame = tk.Frame(login_window, bg="white", relief="solid", bd=1)
login_frame.place(relx=0.5, rely=0.5, anchor="center", width=350, height=400)

# --- 3. Tải và hiển thị logo ---
try:
    # Hãy chắc chắn bạn có file "logo_agu.png" trong thư mục
    logo_image = Image.open("logo_agu.jpg")
    logo_image = logo_image.resize((100, 100), Image.LANCZOS) 
    logo_photo = ImageTk.PhotoImage(logo_image)
    
    logo_label = tk.Label(login_frame, image=logo_photo, bg="white")
    logo_label.pack(pady=(20, 10))
except Exception as e:
    print(f"Lỗi tải logo: {e}")

# --- 4. Tiêu đề ---
title_label = tk.Label(login_frame, text="HỆ THỐNG QUẢN LÝ SINH VIÊN", font=("Arial", 16, "bold"), bg="white")
title_label.pack(pady=10)

# --- 5. Tên người dùng ---
user_label = tk.Label(login_frame, text="Tên người dùng", font=("Arial", 12), bg="white")
user_label.pack(pady=(10, 5))

entry_user = tk.Entry(login_frame, font=("Arial", 12), width=30)
entry_user.pack()

# --- 6. Mật khẩu ---
pass_label = tk.Label(login_frame, text="Mật khẩu", font=("Arial", 12), bg="white")
pass_label.pack(pady=(10, 5))

entry_pass = tk.Entry(login_frame, font=("Arial", 12), width=30, show="*")
entry_pass.pack()

# --- 7. Nút Đăng nhập ---
login_button = tk.Button(login_frame, text="Đăng nhập", font=("Arial", 12, "bold"), 
                         width=28, command=check_login, bg="#0078D4", fg="white")
login_button.pack(pady=20)

# Chạy cửa sổ đăng nhập
login_window.mainloop()