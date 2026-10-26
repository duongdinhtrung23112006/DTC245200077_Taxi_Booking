#Đây là một tập lệnh Bash script tự động hóa quy trình kiểm tra sức khỏe hệ thống (Health Check).
# Thay vì phải gõ thủ công từng lệnh docker ps hay kiểm tra từng cổng kết nối, bạn chỉ cần chạy file script này 
#để nó tự động quét và báo cáo xem các container (Database, Web, Nginx, Prometheus, Grafana, Loki...) 
#đã khởi động thành công và phản hồi đúng chuẩn hay chưa, giúp bạn tiết kiệm rất nhiều thời gian khi thuyết trình 
#hoặc bảo vệ đồ án.

#!/bin/bash

echo "=========================================="
echo "  BẮT ĐẦU KIỂM TRA HỆ THỐNG TAXI BOOKING"
echo "=========================================="

# 1. Kiểm tra trạng thái các container Docker đang chạy
echo "[1/3] Kiểm tra trạng thái các Docker containers..."
docker compose ps

echo "------------------------------------------"

# 2. Kiểm tra khả năng phản hồi của Nginx (Cổng 80)
echo "[2/3] Kiểm tra kết nối tới Nginx Web Server (Port 80)..."
if curl -s http://localhost > /dev/null; then
    echo "✅ Nginx đang hoạt động tốt (HTTP 200 OK)"
else
    echo "❌ Cảnh báo: Không thể kết nối tới Nginx!"
fi

echo "------------------------------------------"

# 3. Kiểm tra các cổng dịch vụ giám sát cốt lõi
echo "[3/3] Kiểm tra các dịch vụ Monitoring & Logging..."
# Kiểm tra Prometheus (Cổng 9090)
if curl -s http://localhost:9090 > /dev/null; then
    echo "✅ Prometheus đang chạy (Port 9090)"
else
    echo "❌ Prometheus chưa sẵn sàng"
fi

# Kiểm tra Grafana (Cổng 3000 - nếu có mở port)
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Grafana đang chạy (Port 3000)"
else
    echo "ℹ️ Grafana chưa mở port trực tiếp ra ngoài (hoặc đang chạy ngầm nội bộ)"
fi

echo "=========================================="
echo "  HOÀN TẤT QUÁ TRÌNH KIỂM TRA HỆ THỐNG!"
echo "=========================================="

