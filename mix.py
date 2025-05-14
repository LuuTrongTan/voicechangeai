from pydub import AudioSegment
import sys
import os

def auto_mix(vocal_path, instrumental_path, output_path, vocal_gain=5, inst_gain=-5):
    # Kiểm tra file tồn tại
    if not os.path.exists(vocal_path):
        print(f"Lỗi: Không tìm thấy file vocals tại {vocal_path}")
        return
    if not os.path.exists(instrumental_path):
        print(f"Lỗi: Không tìm thấy file nhạc nền tại {instrumental_path}")
        return
    
    # Đọc file âm thanh
    print("Đang đọc file vocals...")
    vocal = AudioSegment.from_file(vocal_path)
    print("Đang đọc file nhạc nền...")
    instrumental = AudioSegment.from_file(instrumental_path)
    
    # Thông báo độ dài
    vocal_length = len(vocal) / 1000  # Chuyển từ ms sang giây
    inst_length = len(instrumental) / 1000
    print(f"Vocals: {vocal_length:.2f} giây | Nhạc nền: {inst_length:.2f} giây")
    
    # Cân bằng độ dài
    if len(vocal) > len(instrumental):
        print(f"Cắt vocals để khớp với nhạc nền...")
        vocal = vocal[:len(instrumental)]
    elif len(vocal) < len(instrumental):
        print(f"Cắt nhạc nền để khớp với vocals...")
        instrumental = instrumental[:len(vocal)]
    
    # Điều chỉnh âm lượng
    print(f"Điều chỉnh âm lượng vocals: +{vocal_gain}dB")
    vocal = vocal + vocal_gain  # tăng âm lượng vocals
    print(f"Điều chỉnh âm lượng nhạc nền: {inst_gain}dB")
    instrumental = instrumental + inst_gain  # giảm nhạc nền
    
    # Ghép lại
    print("Đang ghép vocals và nhạc nền...")
    mixed = vocal.overlay(instrumental)
    
    # Xuất file
    print(f"Đang xuất file {output_path}...")
    mixed.export(output_path, format=output_path.split(".")[-1])
    print(f"Đã ghép thành công: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Sử dụng: python mix.py <vocal.wav> <instrumental.wav> <output.mp3> [vocal_gain] [inst_gain]")
        print("  vocal_gain: Tăng/giảm âm lượng vocals (mặc định: +5dB)")
        print("  inst_gain: Tăng/giảm âm lượng nhạc nền (mặc định: -5dB)")
    else:
        vocal_path = sys.argv[1]
        instrumental_path = sys.argv[2]
        output_path = sys.argv[3]
        
        vocal_gain = 5
        inst_gain = -5
        
        if len(sys.argv) >= 5:
            vocal_gain = float(sys.argv[4])
        if len(sys.argv) >= 6:
            inst_gain = float(sys.argv[5])
            
        auto_mix(vocal_path, instrumental_path, output_path, vocal_gain, inst_gain) 