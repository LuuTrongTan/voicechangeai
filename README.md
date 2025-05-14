# Hệ Thống Chuyển Đổi Giọng Nói

Ứng dụng này cho phép chuyển đổi giọng nói giữa các giọng khác nhau sử dụng OpenVoice - công nghệ AI tiên tiến.

## Cấu Trúc Hệ Thống

Hệ thống gồm 3 phần chính:

1. **AI Models (`/ai`)**: Chứa các mô hình AI chuyển đổi giọng nói (OpenVoice).
2. **Backend (`/backend`)**: API backend làm cầu nối giữa frontend và các mô hình AI.
3. **Frontend (`/frontend`)**: Giao diện người dùng để tương tác với hệ thống.

## Yêu Cầu Hệ Thống

- Python 3.8 trở lên
- Node.js và npm
- Dependencies Python (xem file requirements.txt trong thư mục backend)

## Cài Đặt và Khởi Động

### Cài đặt các dependencies

```bash
# Cài đặt dependencies cho backend
cd backend
pip install -r requirements.txt

# Cài đặt dependencies cho frontend
cd ../frontend
npm install
```

### Tải model OpenVoice

1. Tải checkpoint của OpenVoice V2 tại: https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip
2. Giải nén và đặt thư mục `checkpoints_v2` vào thư mục `ai/openvoice/`

### Khởi động hệ thống

Cách đơn giản nhất là sử dụng script khởi động:

```bash
python start.py
```

Script này sẽ thực hiện:
- Build frontend React
- Khởi động backend Flask
- Mở trình duyệt web tại địa chỉ http://localhost:5000

### Khởi động riêng từng phần

#### Backend

```bash
cd backend
python app.py
```

Backend sẽ chạy tại http://localhost:5000

#### Frontend (chế độ phát triển)

```bash
cd frontend
npm start
```

Frontend sẽ chạy tại http://localhost:3000

## Cách Sử Dụng

1. Mở trình duyệt và truy cập http://localhost:5000
2. Tải lên file âm thanh cần chuyển đổi (định dạng WAV, MP3, FLAC)
3. Chọn giọng nói tham chiếu 
4. Nhấn nút "Chuyển đổi giọng nói"
5. Sau khi xử lý hoàn tất, bạn có thể nghe và tải xuống kết quả

## Lưu Ý

- OpenVoice V2 chỉ hỗ trợ chuyển đổi giọng nói, không hỗ trợ chuyển văn bản thành giọng nói (TTS).
- Cần thêm ít nhất 2 file mẫu giọng nói trong thư mục `ai/openvoice/sample_voices` để sử dụng chức năng chuyển đổi giọng nói.

## Thông Tin Liên Hệ

Nếu gặp vấn đề khi sử dụng hệ thống, vui lòng báo cáo qua phần Issues của repository. 