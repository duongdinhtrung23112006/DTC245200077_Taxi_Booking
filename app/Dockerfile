# Đây là bản thiết kế (blueprint) để Docker đóng gói toàn bộ mã nguồn web app thành một môi trường độc lập (Container). 
#Điểm đắt giá nhất của file này là áp dụng chuẩn bảo mật Hardening (Non-root user) — chạy ứng dụng dưới một tài khoản 
#thường thay vì tài khoản quản trị tối cao (root), giúp ngăn chặn tin tặc chiếm quyền kiểm soát toàn bộ hệ thống nếu
# ứng dụng bị tấn công.

FROM python:3.11-slim

# Tạo một user hệ thống mới tên là 'appuser' với quyền hạn hạn chế (Không dùng tài khoản root)
RUN useradd -m appuser

# Thiết lập thư mục làm việc mặc định bên trong container là /app
WORKDIR /app

# Copy file kê khai thư viện requirements.txt từ máy host vào thư mục làm việc của container
COPY requirements.txt .

# Tiến hành cài đặt các thư viện Python được liệt kê trong file mà không lưu cache để giảm dung lượng image
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn code web còn lại từ máy host vào thư mục /app trong container
COPY . .

# Thay đổi quyền sở hữu toàn bộ thư mục /app sang cho tài khoản 'appuser' vừa tạo ở trên
RUN chown -R appuser:appuser /app

# Chuyển quyền thực thi container sang tài khoản 'appuser' (Tăng cường bảo mật theo chuẩn Hardening)
USER appuser

# Khai báo mở cổng mạng 5000 bên trong container để phục vụ request
EXPOSE 5000

# Lệnh mặc định sẽ được thực thi khi container khởi động lên (Chạy ứng dụng Flask)
CMD ["python", "app.py"]