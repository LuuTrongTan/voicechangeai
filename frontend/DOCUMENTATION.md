# Tài liệu chức năng Frontend của hệ thống chuyển đổi giọng nói

## 1. Cấu trúc thư mục

```
frontend/
├── public/               # Chứa các file tĩnh và HTML gốc
├── src/                  # Mã nguồn chính của ứng dụng
│   ├── components/       # Các thành phần giao diện
│   │   ├── layout/       # Bố cục chung của ứng dụng
│   │   └── user/         # Các thành phần liên quan đến người dùng
│   ├── services/         # Các dịch vụ kết nối API
│   ├── App.js            # Thành phần gốc của ứng dụng
│   ├── index.js          # Điểm khởi chạy ứng dụng
│   ├── index.css         # Styles chung cho toàn ứng dụng
│   └── reportWebVitals.js # Theo dõi hiệu suất ứng dụng
└── package.json          # Cấu hình và dependencies của dự án
```

## 2. Mô tả chi tiết từng file

### 2.1. File cấu hình và khởi tạo

#### `package.json`
- **Chức năng**: Cấu hình dự án React và quản lý dependencies
- **Nhiệm vụ**: 
  - Định nghĩa thông tin dự án và các phụ thuộc
  - Cung cấp các lệnh scripts (start, build, test)
  - Cấu hình proxy để kết nối với backend tại "http://localhost:5000"

#### `src/index.js`
- **Chức năng**: Điểm khởi chạy chính của ứng dụng React
- **Nhiệm vụ**:
  - Render thành phần gốc App vào DOM
  - Thiết lập BrowserRouter cho định tuyến
  - Khởi chạy báo cáo hiệu suất (reportWebVitals)

#### `src/index.css`
- **Chức năng**: Cung cấp styles chung cho toàn ứng dụng
- **Nhiệm vụ**:
  - Định nghĩa kiểu cơ bản cho body, code, container, v.v.
  - Thiết lập bố cục flex cho ứng dụng
  - Cung cấp các lớp tiện ích (card, button, responsive)

#### `src/reportWebVitals.js`
- **Chức năng**: Theo dõi và báo cáo hiệu suất ứng dụng
- **Nhiệm vụ**: Thu thập và báo cáo các chỉ số Web Vitals cho ứng dụng

### 2.2. Thành phần chính

#### `src/App.js`
- **Chức năng**: Thành phần gốc của ứng dụng
- **Nhiệm vụ**:
  - Thiết lập ThemeProvider với theme tùy chỉnh
  - Định nghĩa cấu trúc bố cục chung (Header, main, Footer)
  - Thiết lập các routes cho ứng dụng

### 2.3. Dịch vụ API

#### `src/services/api.js`
- **Chức năng**: Quản lý kết nối với backend API
- **Nhiệm vụ**:
  - Cấu hình Axios với baseURL và timeout
  - Cung cấp interceptor để xử lý lỗi
  - Định nghĩa các hàm tương tác với API:
    - `getModels()`: Lấy danh sách giọng nói
    - `convertVoice()`: Gửi yêu cầu chuyển đổi giọng
    - `checkHealth()`: Kiểm tra trạng thái máy chủ
    - `downloadResult()`: Tải xuống file kết quả

### 2.4. Thành phần bố cục (Layout)

#### `src/components/layout/Header.js`
- **Chức năng**: Thanh điều hướng phía trên của ứng dụng
- **Nhiệm vụ**:
  - Hiển thị logo và tên ứng dụng
  - Cung cấp liên kết điều hướng đến trang chính
  - Responsive trên các kích thước màn hình khác nhau

#### `src/components/layout/Footer.js`
- **Chức năng**: Chân trang của ứng dụng
- **Nhiệm vụ**:
  - Hiển thị thông tin bản quyền
  - Hiển thị nguồn sử dụng (Powered by OpenVoice)
  - Cung cấp liên kết đến trang GitHub của OpenVoice

#### `src/components/layout/NotFound.js`
- **Chức năng**: Trang lỗi 404 khi không tìm thấy đường dẫn
- **Nhiệm vụ**:
  - Hiển thị thông báo lỗi "Không tìm thấy trang"
  - Cung cấp nút để quay lại trang chủ
  - Tối ưu hóa trải nghiệm người dùng khi gặp lỗi

### 2.5. Thành phần người dùng

#### `src/components/user/UserDashboard.js`
- **Chức năng**: Trang chính cho người dùng thực hiện chuyển đổi giọng nói
- **Nhiệm vụ**:
  - Quản lý state của ứng dụng:
    - `audioFile`: File âm thanh được tải lên
    - `availableVoices`: Danh sách giọng nói có sẵn
    - `selectedVoice`: Giọng nói được chọn
    - `isLoading`: Trạng thái xử lý
    - `result`: Kết quả chuyển đổi
    - `error`: Thông báo lỗi
  - Thực hiện các thao tác:
    - Tải danh sách giọng nói từ backend (`useEffect`)
    - Xử lý tải lên file âm thanh (`handleFileChange`)
    - Xử lý thay đổi giọng nói (`handleVoiceChange`) 
    - Gửi yêu cầu chuyển đổi (`handleConvert`)
    - Tải xuống kết quả (`handleDownload`)
  - Render giao diện chuyển đổi giọng nói:
    - Khu vực tải lên file âm thanh
    - Dropdown chọn giọng nói mục tiêu
    - Nút chuyển đổi giọng nói
    - Khu vực hiển thị kết quả với trình phát âm thanh
    - Nút tải xuống kết quả

## 3. Luồng dữ liệu và tương tác

1. Người dùng truy cập ứng dụng tại đường dẫn chính
2. `UserDashboard` tải danh sách giọng nói từ backend
3. Người dùng tải lên file âm thanh và chọn giọng nói mục tiêu
4. Khi nhấn nút "Chuyển đổi giọng nói", dữ liệu được gửi đến backend
5. Kết quả chuyển đổi được hiển thị với trình phát âm thanh và nút tải xuống
6. Người dùng có thể nghe thử và tải xuống file âm thanh đã chuyển đổi

## 4. Lưu ý quan trọng

- Frontend không tạo bất kỳ kết quả giả nào, mà chỉ hiển thị kết quả thực từ API backend
- Tất cả các xử lý chuyển đổi giọng nói đều được thực hiện phía backend
- Frontend chỉ giao tiếp với backend thông qua API
- OpenVoice V2 chỉ hỗ trợ chuyển đổi giọng nói, không hỗ trợ TTS

## 5. Công nghệ sử dụng

- **React**: Thư viện UI để xây dựng giao diện người dùng
- **Material-UI**: Hệ thống component cho giao diện người dùng
- **React Router**: Quản lý định tuyến trong ứng dụng
- **Axios**: Thư viện HTTP client để giao tiếp với API 