# 🐍 ĐỒ ÁN LẬP TRÌNH PYTHON - QUẢN LÝ SINH VIÊN

## 👨‍💻 Thông tin nhóm

| Họ và tên | MSSV | Lớp |
| :--- | :--- | :--- |
| **Phó Bảo Phong** | **DTH235731** | **DH24TH2** |
| **Tống Nhựt Nam** | **DTH235702** | **DH24TH2** |

---

## 📘 Môn học
- **Tên môn:** Lập trình Python (hoặc Lập trình Giao diện Đồ họa)
- **Đề tài:** Xây dựng ứng dụng **Quản lý Sinh viên** bằng giao diện đồ họa (GUI).
- **Ngôn ngữ:** Python

---

## 🎯 Mục tiêu đồ án
- Xây dựng **ứng dụng quản lý sinh viên** có giao diện trực quan, thân thiện và dễ sử dụng bằng thư viện `tkinter`.
- Áp dụng các kỹ năng:
  - Lập trình hướng đối tượng (OOP) và lập trình hàm.
  - Thiết kế giao diện Desktop với **Tkinter** và **ttk (Themed Tkinter)**.
  - Kết nối và thao tác dữ liệu với **MySQL** thông qua thư viện `mysql.connector`.
  - Xử lý **CRUD** và tính toán/tra cứu dữ liệu (DTL, DRL, Xếp loại) trực quan.

---

## ⚙️ Công nghệ sử dụng

| Công nghệ | Chi tiết | Vai trò |
| :--- | :--- | :--- |
| **Ngôn ngữ** | Python 3.x | Ngôn ngữ phát triển chính. |
| **Giao diện (GUI)** | **Tkinter** (và **ttk**) | Xây dựng giao diện cửa sổ, Frame, Button, Treeview. |
| **Cơ sở dữ liệu** | **MySQL** | Hệ quản trị CSDL lưu trữ thông tin (`qlsv`). |
| **Kết nối CSDL** | **`mysql.connector`** | Thư viện kết nối và thực thi truy vấn. |
| **Thư viện khác** | **`tkcalendar`** | Điều khiển chọn ngày (DateEntry) cho Ngày sinh. |

---

## ✨ Tính năng chính

Ứng dụng cho phép **Admin** thực hiện quản lý sinh viên và điểm số, đồng thời cung cấp khả năng **tra cứu** điểm.

### 🔐 Phân quyền và Đăng nhập
- Hệ thống có Form đăng nhập (`DangNhap.py`).
- Tài khoản mặc định: `admin` / `123`.

### 🛠️ Quản lý Nghiệp vụ (CRUD)

| Form/File | Chức năng | Chi tiết |
| :--- | :--- | :--- |
| **`QuanLiSinhVien.py`** | **Quản lý Sinh viên** | Form CRUD chính: Thêm, Sửa, Xóa, Hủy thông tin cá nhân. |
| **`ChiTietDiemTichLuy_form.py`** | **Quản lý Điểm Tích Lũy** | Cho phép Admin nhập, sửa, xóa điểm môn học, tự động **cập nhật DTL** trung bình. |
| **`ChiTietDiemRenluyen_form.py`** | **Quản lý Điểm Rèn Luyện** | Cho phép Admin nhập, sửa, xóa điểm rèn luyện theo học kỳ, tự động **cập nhật DRL** trung bình. |

### 📊 Tra cứu và Thống kê
- **Form:** `KetQuaHocTap_form.py`
- Chức năng tra cứu tổng hợp: Lọc theo **Khoa** hoặc **MSSV**, đồng thời tính toán và hiển thị cột **Xếp loại Học tập** dựa trên DTL và DRL.

---

## 📂 Cấu trúc Module
Code được tổ chức thành các file Python riêng biệt để áp dụng kiến trúc module và dễ bảo trì:

* `DangNhap.py`: Logic xử lý đăng nhập.
* `QuanLiSinhVien.py`: Cửa sổ chính và logic CRUD sinh viên.
* `DatabaseConnection.py`: Định nghĩa hàm **`connect_db()`** (cấu hình kết nối MySQL) và **`center_window()`** (hàm căn giữa cửa sổ).
* `KetQuaHocTap_form.py`: Logic tra cứu tổng hợp (Xếp loại).
* `ChiTietDiemTichLuy_form.py`: Logic quản lý điểm môn học chi tiết.
* `ChiTietDiemRenluyen_form.py`: Logic quản lý điểm rèn luyện chi tiết.
