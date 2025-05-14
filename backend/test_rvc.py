#!/usr/bin/env python3
import os
import sys
import argparse
import logging
import traceback
import time

# Thêm thư mục cha vào sys.path
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if root_dir not in sys.path:
    sys.path.append(root_dir)

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Import controller
from models.rvc_controller import RVCController

def test_rvc_connection():
    """
    Kiểm tra kết nối với model RVC
    """
    # Khởi tạo controller
    controller = RVCController()
    
    # Kiểm tra xem mô hình đã được cài đặt chưa
    if not controller.is_model_available:
        print(f"\n❌ Mô hình RVC chưa được cài đặt hoặc thiếu các file cần thiết")
        # Kiểm tra các file cần thiết
        required_files = [
            os.path.join(controller.model_dir, 'requirements.txt'),
            os.path.join(controller.model_dir, 'infer-web.py')
        ]
        
        for file in required_files:
            if not os.path.exists(file):
                print(f"   - Thiếu file: {file}")
        
        return False
    
    # Lấy danh sách giọng nói có sẵn
    voices = controller.list_available_voices()
    if not voices or len(voices) < 1:
        print(f"\n❌ Không tìm thấy mô hình giọng nói cho RVC")
        print(f"   Vui lòng thêm ít nhất một mô hình vào thư mục models hoặc weights")
        return False
    
    print(f"\nĐã tìm thấy {len(voices)} mô hình RVC:")
    for i, voice in enumerate(voices):
        print(f"   {i+1}. {voice}")
    
    # Nếu có ít nhất một giọng nói, thử chuyển đổi từ file mẫu
    if len(voices) > 0:
        # Tạo file âm thanh mẫu - 1 giây sine wave
        sample_dir = os.path.join(controller.model_dir, "samples")
        os.makedirs(sample_dir, exist_ok=True)
        sample_file = os.path.join(sample_dir, "test_sample.wav")
        
        if not os.path.exists(sample_file):
            try:
                import numpy as np
                import soundfile as sf
                sample_rate = 24000
                t = np.arange(sample_rate) / sample_rate
                sine_wave = np.sin(2 * np.pi * 440 * t) * 0.5
                sf.write(sample_file, sine_wave, sample_rate)
                print(f"\n✅ Đã tạo file âm thanh mẫu: {sample_file}")
            except Exception as e:
                print(f"\n❌ Không thể tạo file âm thanh mẫu: {str(e)}")
                # Tìm file mẫu khác
                for root, dirs, files in os.walk(controller.model_dir):
                    for file in files:
                        if file.endswith(('.wav', '.mp3')):
                            sample_file = os.path.join(root, file)
                            print(f"   Sử dụng file mẫu có sẵn: {sample_file}")
                            break
                    if os.path.exists(sample_file):
                        break
        
        # Nếu có file mẫu, thử chuyển đổi
        if os.path.exists(sample_file):
            target_voice = voices[0]  # Lấy mô hình đầu tiên
            
            print(f"\nSử dụng file nguồn: {os.path.basename(sample_file)}")
            print(f"Sử dụng model đích: {target_voice}")
            
            # Gọi RVC để xử lý chuyển đổi giọng nói
            print(f"\nĐang thực hiện chuyển đổi giọng nói...")
            output_file = controller.convert_voice(sample_file, target_voice)
            
            if output_file and os.path.exists(output_file):
                print(f"\n✅ Chuyển đổi thành công! File kết quả: {output_file}")
                print(f"   Kích thước file: {os.path.getsize(output_file) / 1024:.2f} KB")
                return True
            else:
                print("\n❌ Chuyển đổi thất bại!")
                return False
        else:
            print("\n❌ Không tìm thấy file âm thanh mẫu để test!")
            return False
    
    return False

def main():
    print("=" * 50)
    print("KIỂM TRA KẾT NỐI BACKEND - RVC")
    print("=" * 50)
    
    result = test_rvc_connection()
    
    if result:
        print("\n✅ HỆ THỐNG RVC HOẠT ĐỘNG TỐT!\n")
        return 0
    else:
        print("\n❌ HỆ THỐNG RVC GẶP VẤN ĐỀ!\n")
        return 1

if __name__ == "__main__":
    main() 