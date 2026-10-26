-- Tạo bảng lưu trữ thông tin tài khoản người dùng trong hệ thống
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,                        -- Mã định danh tự tăng (Primary Key) cho từng user
    username VARCHAR(50) UNIQUE NOT NULL,         -- Tên đăng nhập (phải là duy nhất, không được để trống)
    password VARCHAR(255) NOT NULL,               -- Mật khẩu đã được mã hóa dạng băm (hashed password) để bảo mật
    role VARCHAR(20) DEFAULT 'customer'           -- Phân quyền tài khoản, mặc định là khách hàng ('customer') hoặc 'admin'
);

-- Tạo bảng lưu trữ thông tin các chuyến xe đặt qua hệ thống
CREATE TABLE IF NOT EXISTS rides (
    id SERIAL PRIMARY KEY,                        -- Mã định danh tự tăng cho mỗi chuyến xe
    user_id INT REFERENCES users(id),             -- Khóa ngoại (Foreign Key) liên kết chuyến xe với ID của người dùng đã đặt
    passenger_name VARCHAR(100) NOT NULL,         -- Tên hành khách đi xe
    pickup_location VARCHAR(200) NOT NULL,        -- Điểm đón khách
    dropoff_location VARCHAR(200) NOT NULL,       -- Điểm đến của khách
    status VARCHAR(20) DEFAULT 'PENDING',         -- Trạng thái chuyến xe (mặc định là 'PENDING' - chờ xử lý, có thể đổi thành ACCEPTED/CANCELLED)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- Thời gian tạo chuyến xe, tự động lấy mốc giờ hiện tại
);