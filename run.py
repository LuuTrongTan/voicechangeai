import os
import sys
import time
import subprocess
import platform
from pathlib import Path

# Màu sắc cho console
class Colors:
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    GREEN = '\033[92m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text, color):
    """In văn bản có màu"""
    print(f"{color}{text}{Colors.ENDC}")

def run_command(command, cwd=None, shell=True):
    """Chạy lệnh và trả về kết quả"""
    try:
        result = subprocess.run(command, cwd=cwd, shell=shell, 
                               check=True, text=True, capture_output=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def main():
    # Đường dẫn thư mục
    root_dir = Path(__file__).parent
    frontend_dir = root_dir / "frontend"
    backend_dir = root_dir / "backend"
    
    print_colored("=== HỆ THỐNG VOICE CHANGER ===", Colors.CYAN)
    
    # Kiểm tra tham số dòng lệnh
    run_mode = "dev"  # Chế độ mặc định
    if len(sys.argv) > 1 and sys.argv[1] == "prod":
        run_mode = "prod"
    
    if run_mode == "prod":
        # Chế độ production: build frontend và serve từ backend
        print_colored("\n=== CHẾ ĐỘ PRODUCTION ===", Colors.YELLOW)
        
        # Kiểm tra và build frontend nếu cần
        build_dir = frontend_dir / "build"
        if not build_dir.exists():
            print_colored("\n=== ĐANG BUILD FRONTEND ===", Colors.YELLOW)
            
            # Build frontend
            success, output = run_command("npm run build", cwd=str(frontend_dir))
            if not success:
                print_colored("ERROR: Không thể build ứng dụng React.", Colors.RED)
                print(output)
                return 1
            
            print_colored("✅ Frontend đã được build thành công!", Colors.GREEN)
    else:
        # Chế độ dev: chạy frontend development server
        print_colored("\n=== CHẾ ĐỘ DEVELOPMENT ===", Colors.YELLOW)
    
    # Xác định lệnh chạy python
    python_cmd = "python"
    if platform.system() == "Windows":
        # Kiểm tra môi trường ảo
        venv_path = root_dir / "venv" / "Scripts" / "python.exe"
        if venv_path.exists():
            python_cmd = str(venv_path)
    else:
        # Linux/Mac
        venv_path = root_dir / "venv" / "bin" / "python"
        if venv_path.exists():
            python_cmd = str(venv_path)
    
    # Chạy backend
    print_colored("\n=== ĐANG KHỞI ĐỘNG BACKEND ===", Colors.YELLOW)
    backend_app = backend_dir / "app.py"
    backend_process = subprocess.Popen(
        [python_cmd, str(backend_app)], 
        cwd=str(backend_dir)
    )
    
    # Chờ backend khởi động
    time.sleep(2)
    print_colored("✅ Backend đã được khởi động!", Colors.GREEN)
    
    # Chạy frontend nếu ở chế độ dev
    frontend_process = None
    if run_mode == "dev":
        print_colored("\n=== ĐANG KHỞI ĐỘNG FRONTEND ===", Colors.YELLOW)
        
        # Khởi động frontend development server
        if platform.system() == "Windows":
            frontend_process = subprocess.Popen(
                "npm start", 
                cwd=str(frontend_dir),
                shell=True
            )
        else:
            frontend_process = subprocess.Popen(
                ["npm", "start"], 
                cwd=str(frontend_dir)
            )
            
        # Chờ frontend khởi động
        time.sleep(3)
        print_colored("✅ Frontend đã được khởi động!", Colors.GREEN)
        
        print_colored("\nTruy cập Frontend: http://localhost:3000", Colors.CYAN)
    
    print_colored("\nTruy cập Backend: http://localhost:5000", Colors.CYAN)
    print("\nNhấn Ctrl+C để dừng ứng dụng")
    
    try:
        # Chờ cho đến khi người dùng dừng chương trình
        if frontend_process:
            frontend_process.wait()
        else:
            backend_process.wait()
            
    except KeyboardInterrupt:
        print_colored("\nĐang dừng ứng dụng...", Colors.YELLOW)
    finally:
        # Dừng cả backend và frontend nếu đang chạy
        if backend_process and backend_process.poll() is None:
            if platform.system() == "Windows":
                subprocess.run(f"taskkill /F /PID {backend_process.pid} /T", shell=True)
            else:
                backend_process.terminate()
            print_colored("Backend đã dừng.", Colors.GREEN)
            
        if frontend_process and frontend_process.poll() is None:
            if platform.system() == "Windows":
                subprocess.run(f"taskkill /F /PID {frontend_process.pid} /T", shell=True)
            else:
                frontend_process.terminate()
            print_colored("Frontend đã dừng.", Colors.GREEN)

if __name__ == "__main__":
    sys.exit(main()) 