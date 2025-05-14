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
from models.openvoice_controller import OpenVoiceController

def test_openvoice_connection():
    """
    Kiểm tra kết nối với model OpenVoice
    """
    # Khởi tạo controller
    controller = OpenVoiceController()
    
    # Đường dẫn đến file checkpoint và config
    config_path = os.path.join(controller.model_dir, "checkpoints_v2", "converter", "config.json")
    checkpoint_path = os.path.join(controller.model_dir, "checkpoints_v2", "converter", "checkpoint.pth")
    
    # Kiểm tra các file cần thiết có tồn tại không
    if not os.path.exists(checkpoint_path) or not os.path.exists(config_path):
        print(f"\n❌ Không tìm thấy các file model cần thiết:")
        if not os.path.exists(checkpoint_path):
            print(f"   - Thiếu file checkpoint: {checkpoint_path}")
        if not os.path.exists(config_path):
            print(f"   - Thiếu file config: {config_path}")
        return False
    
    # Lấy danh sách giọng nói có sẵn
    voices = controller.list_available_voices()
    if not voices or len(voices) < 2:
        print(f"\n❌ Không đủ file giọng nói tham khảo để thực hiện chuyển đổi")
        print(f"   Tìm thấy {len(voices)} giọng nói")
        
        # Thử tạo file mẫu
        try:
            # Tạo thư mục sample_voices nếu chưa tồn tại
            sample_dir = os.path.join(controller.model_dir, "sample_voices")
            os.makedirs(sample_dir, exist_ok=True)
            
            # Tạo file âm thanh mẫu - 1 giây silence
            file_path = os.path.join(sample_dir, "sample1.wav")
            if not os.path.exists(file_path):
                import numpy as np
                import soundfile as sf
                sample_rate = 24000
                silence_1s = np.zeros(sample_rate)
                sf.write(file_path, silence_1s, sample_rate)
                print(f"\n✅ Đã tạo file mẫu: {file_path}")
            
            # Tạo file âm thanh mẫu 2 - 1 giây sine wave
            file_path2 = os.path.join(sample_dir, "sample2.wav")
            if not os.path.exists(file_path2):
                import numpy as np
                import soundfile as sf
                sample_rate = 24000
                t = np.arange(sample_rate) / sample_rate
                sine_wave = np.sin(2 * np.pi * 440 * t) * 0.5
                sf.write(file_path2, sine_wave, sample_rate)
                print(f"✅ Đã tạo file mẫu: {file_path2}")
                
            # Lấy lại danh sách giọng nói sau khi tạo file mẫu
            voices = controller.list_available_voices()
            if not voices or len(voices) < 2:
                print(f"\n❌ Vẫn không đủ file giọng nói. Cần ít nhất 2 file.")
                return False
        except Exception as e:
            print(f"\n❌ Không thể tạo file mẫu: {str(e)}")
            print("Vui lòng thêm ít nhất 2 file âm thanh (WAV) vào thư mục sample_voices.")
            return False
    
    # Chọn 2 file đầu tiên để thực hiện chuyển đổi
    source_file = voices[0]
    target_voice = voices[1]
    
    print(f"\nSử dụng file nguồn: {os.path.basename(source_file)}")
    print(f"Sử dụng file tham chiếu: {os.path.basename(target_voice)}")
    
    # Gọi OpenVoice để xử lý chuyển đổi giọng nói
    print(f"\nĐang thực hiện chuyển đổi giọng nói...")
    output_file = controller.convert_voice(source_file, target_voice)
    
    if output_file and os.path.exists(output_file):
        print(f"\n✅ Chuyển đổi thành công! File kết quả: {output_file}")
        print(f"   Kích thước file: {os.path.getsize(output_file) / 1024:.2f} KB")
        return True
    else:
        print("\n❌ Chuyển đổi thất bại!")
        return False

def main():
    print("=" * 50)
    print("KIỂM TRA KẾT NỐI BACKEND - OPENVOICE")
    print("=" * 50)
    
    result = test_openvoice_connection()
    
    if result:
        print("\n✅ HỆ THỐNG OPENVOICE HOẠT ĐỘNG TỐT!\n")
        return 0
    else:
        print("\n❌ HỆ THỐNG OPENVOICE GẶP VẤN ĐỀ!\n")
        return 1

if __name__ == "__main__":
    main() 