
# Drowsiness Detection with OpenCV and MediaPipe Face Mesh

Ứng dụng web phát hiện buồn ngủ có hỗ trợ theo thời gian dựng được xây dựng với Flask và OpenCV và MediaPipe Face MeshMesh. Hệ thống cho phép tải lên ảnh, video hoặc dùng real-timetime để phát hiện liệu đối tượng có đang buồn ngủ hay không.

## 🧠 Mô tả dự án

Ứng dụng sử dụng Flask làm backend, OpenCV để xử lý landmark cho mắt, Face Mesh để tìm ra các landmark của mắt. Với giao diện trực quan, người dùng có thể dễ dàng tải lên ảnh, video thậm chí video realtime từ webcam để phát hiện liệu đối tượng có đang buồn ngủ hay không.

## 🛠️ Công nghệ sử dụng

- Python 3.x
- Flask
- MediaPipe Face MeshMesh
- OpenCV

## 📁 Cấu trúc thư mục

```
drowsiness-detectiondetection/
├── app.py                 # Flask application
├── utils.py               # Hàm hỗ trợ tìm landmark, xác định eye state 
├── requirements.txt       # Danh sách thư viện cần thiết
├── templates/             # Giao diện HTML
├── static/                # Chứa file js để xử lý logic
└── uploads/               # Thư mục lưu ảnh tải lên
```

## 🚀 Cài đặt và chạy ứng dụng

1. **Clone repository:**

   ```bash
   git clone https://github.com/dattrieuK17/drowsiness-detection.git
   cd drowsiness-detection
   ```

2. **Tạo môi trường ảo và cài đặt dependencies:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # Trên Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```


3. **Chạy ứng dụng:**

   ```bash
   python app.py
   ```

4. **Truy cập ứng dụng:**

   Mở trình duyệt và truy cập `http://localhost:5000`.

## 📸 Chức năng chính

- Tải lên ảnh, video để phát hiện trạng thái buồn ngủ.
- Có hỗ trợ real-time
- Hiển thị kết quả một cách trực quan trên giao diện web.


