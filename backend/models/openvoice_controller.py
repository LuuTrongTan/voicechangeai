import os
import logging
import sys
import numpy as np
import soundfile as sf
import librosa
import time
import json
import re
from models.voice_model_interface import VoiceModelInterface

# Tắt GPU để tránh lỗi với GPU cũ
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

logger = logging.getLogger(__name__)

class OpenVoiceController(VoiceModelInterface):
    def __init__(self):
        """Khởi tạo controller cho mô hình OpenVoice"""
        # Giữ nguyên code khởi tạo
        self.initialize()
        
    def initialize(self, config=None):
        """Khởi tạo model với cấu hình tùy chọn"""
        # Buộc sử dụng CPU vì GPU quá cũ
        os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
        
        self.model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ai', 'openvoice'))
        self.results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results'))
        
        # Tạo thư mục output nếu chưa tồn tại
        os.makedirs(self.results_dir, exist_ok=True)
        
        # Tạo cấu trúc thư mục mới
        self.openvoice_dir = os.path.join(self.results_dir, "openvoice")
        os.makedirs(self.openvoice_dir, exist_ok=True)
        
        # Tạo thư mục voice_conversion
        self.voice_conversion_dir = os.path.join(self.openvoice_dir, "voice_conversion")
        os.makedirs(self.voice_conversion_dir, exist_ok=True)
        
        # Tạo thư mục tts
        self.tts_dir = os.path.join(self.openvoice_dir, "tts")
        os.makedirs(self.tts_dir, exist_ok=True)
        
        # Tạo thư mục tạm
        self.temp_dir = os.path.join(self.results_dir, "temp")
        os.makedirs(self.temp_dir, exist_ok=True)
        
        # Kiểm tra và tạo thư mục base_speakers nếu cần thiết
        base_speakers_dir = os.path.join(self.model_dir, "checkpoints_v2", "base_speakers", "ses")
        if not os.path.exists(base_speakers_dir):
            logger.warning(f"Khong tim thay thu muc base_speakers: {base_speakers_dir}")
            # Tạo thư mục nếu chưa tồn tại
            os.makedirs(base_speakers_dir, exist_ok=True)
            logger.info(f"Da tao thu muc base_speakers: {base_speakers_dir}")
        
        # Thêm đường dẫn vào sys.path để import OpenVoice API
        sys.path.append(self.model_dir)
        
        # Cài đặt các gói NLTK cần thiết
        try:
            import nltk
            # Kiểm tra và cài đặt averaged_perceptron_tagger
            try:
                nltk.data.find('taggers/averaged_perceptron_tagger')
            except LookupError:
                logger.info("Đang cài đặt averaged_perceptron_tagger...")
                nltk.download('averaged_perceptron_tagger')
                
            # Kiểm tra và cài đặt averaged_perceptron_tagger_eng nếu cần
            try:
                nltk.data.find('taggers/averaged_perceptron_tagger_eng')
            except LookupError:
                logger.info("Đang cài đặt taggers/averaged_perceptron_tagger_eng...")
                nltk.download('averaged_perceptron_tagger_eng')
                
            # Các gói NLTK khác có thể cần thiết
            for package in ['punkt', 'cmudict']:
                try:
                    nltk.data.find(f'tokenizers/{package}')
                except LookupError:
                    logger.info(f"Đang cài đặt {package}...")
                    nltk.download(package)
        except Exception as e:
            logger.warning(f"Không thể cài đặt các gói NLTK: {str(e)}")
        
        logger.info("Da khoi tao OpenVoice controller (CPU mode)")
        return True
        
    def validate_audio(self, audio_path, target_sr=24000):
        """Ghi đè phương thức của interface với cài đặt riêng"""
        return self._ensure_valid_audio(audio_path, target_sr)
        
    def _ensure_valid_audio(self, audio_path, target_sr=24000):
        """Kiểm tra và sửa file âm thanh nếu cần thiết"""
        try:
            # Đọc file âm thanh
            audio, sr = librosa.load(audio_path, sr=None)
            
            # Kiểm tra âm thanh có hợp lệ không
            if np.isnan(audio).any():
                logger.warning("File am thanh chua NaN values, dang sua loi")
                audio = np.nan_to_num(audio)
                
            if np.max(np.abs(audio)) < 1e-6:
                logger.warning("File am thanh qua nho, dang tang am luong")
                audio = audio * 10.0
            
            # Chuyển sang mono nếu là stereo
            if len(audio.shape) > 1:
                logger.info("Chuyen file am thanh sang mono")
                audio = librosa.to_mono(audio)
            
            # Resample nếu cần
            if sr != target_sr:
                logger.info(f"Resample tu {sr}Hz sang {target_sr}Hz")
                audio = librosa.resample(audio, orig_sr=sr, target_sr=target_sr)
            
            # Lưu file tạm nếu đã sửa đổi
            fixed_path = os.path.join(self.temp_dir, os.path.basename(audio_path))
            sf.write(fixed_path, audio, target_sr)
            logger.info(f"Da luu file fix: {fixed_path}")
            return fixed_path
        except Exception as e:
            logger.error(f"Loi khi kiem tra am thanh: {str(e)}")
            return audio_path  # Trả về file gốc nếu có lỗi

    def convert_voice(self, input_file_path, target_voice, tau=0.4):
        """
        Chuyển đổi giọng nói từ file âm thanh đầu vào sang giọng nói đích
        
        Args:
            input_file_path (str): Đường dẫn đến file âm thanh đầu vào
            target_voice (str): Đường dẫn đến file giọng nói tham chiếu hoặc file đặc trưng .pth
            tau (float): Tham số tau điều chỉnh mức độ áp dụng giọng mới (0.1-1.0)
            
        Returns:
            str: Đường dẫn đến file âm thanh kết quả nếu thành công, None nếu thất bại
        """
        try:
            # Tạo tên file kết quả
            base_name = os.path.basename(input_file_path)
            filename, ext = os.path.splitext(base_name)
            target_voice_basename = os.path.splitext(os.path.basename(target_voice))[0]  # Lấy tên không có đuôi
            output_file = os.path.join(self.voice_conversion_dir, f"{filename}_openvoice_{target_voice_basename}.wav")  # Luôn dùng đuôi .wav
            
            # Kiểm tra file âm thanh đầu vào
            logger.info("Kiểm tra và đảm bảo format âm thanh đầu vào hợp lệ")
            fixed_input = self._ensure_valid_audio(input_file_path)
            
            # Đảm bảo sử dụng CPU
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
            import torch
            torch.set_num_threads(4)  # Giới hạn số thread để tránh quá tải
            
            # Import và khởi tạo OpenVoice API
            from openvoice.api import ToneColorConverter
            
            # Đường dẫn đến file cấu hình và checkpoint
            config_path = os.path.join(self.model_dir, "checkpoints_v2", "converter", "config.json")
            checkpoint_path = os.path.join(self.model_dir, "checkpoints_v2", "converter", "checkpoint.pth")
            
            # Kiểm tra checkpoint tồn tại
            if not os.path.exists(checkpoint_path):
                logger.error(f"Khong tim thay checkpoint: {checkpoint_path}")
                return None
            
            # Kiểm tra file target_voice tồn tại
            if not os.path.exists(target_voice):
                logger.error(f"Không tìm thấy file giọng nói đích: {target_voice}")
                return None
            
            # Sử dụng CPU
            device = 'cpu'
            logger.info(f"Su dung thiet bi: {device}")
            
            # Khởi tạo converter
            logger.info("Khoi tao ToneColorConverter")
            converter = ToneColorConverter(config_path, device=device)
            
            # Load checkpoint
            logger.info(f"Dang load checkpoint: {checkpoint_path}")
            converter.load_ckpt(checkpoint_path)
            
            # Trích xuất đặc trưng từ file nguồn
            logger.info("Trích xuất đặc trưng từ file nguồn")
            src_se = converter.extract_se([fixed_input])
            
            # Xử lý file target voice
            if target_voice.endswith('.pth'):
                # Nếu là file .pth, load trực tiếp đặc trưng giọng nói
                logger.info(f"Đang load đặc trưng giọng nói từ file .pth: {target_voice}")
                try:
                    tgt_se = torch.load(target_voice, map_location=device)
                    logger.info("Đã load thành công đặc trưng giọng nói từ file .pth")
                except Exception as e:
                    logger.error(f"Lỗi khi load file .pth: {str(e)}")
                    return None
            else:
                # Nếu là file âm thanh, trích xuất đặc trưng
                logger.info(f"Trích xuất đặc trưng từ file âm thanh: {target_voice}")
                fixed_target = self._ensure_valid_audio(target_voice)
                tgt_se = converter.extract_se([fixed_target])
            
            # Chuyển đổi và lưu kết quả
            logger.info(f"Chuyển đổi giọng nói với tau={tau}")
            converter.convert(
                audio_src_path=fixed_input,
                src_se=src_se,
                tgt_se=tgt_se,
                output_path=output_file,
                tau=tau
            )
            
            # Kiểm tra kết quả
            if os.path.exists(output_file):
                file_size = os.path.getsize(output_file)
                if file_size < 10000:  # < 10KB
                    logger.warning(f"Kích thước file quá nhỏ: {file_size} bytes")
                else:
                    logger.info(f"Kích thước file hợp lệ: {file_size} bytes")
                    
                    # Kiểm tra âm thanh
                    audio, sr = librosa.load(output_file, sr=None)
                    max_amplitude = np.max(np.abs(audio))
                    if max_amplitude < 0.01:
                        logger.warning("Biên độ âm thanh quá nhỏ!")
                    else:
                        logger.info(f"Biên độ âm thanh hợp lệ: {max_amplitude:.4f}")
            
            logger.info(f"Chuyển đổi thành công: {output_file}")
            return output_file
            
        except Exception as e:
            logger.error(f"Lỗi khi chuyển đổi giọng nói: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None

    def text_to_speech(self, text, speaker="en-us", language="english", speed=1.0):
        """
        Chuyển đổi văn bản thành giọng nói sử dụng MeloTTS và OpenVoice
        
        Args:
            text (str): Văn bản cần chuyển đổi thành giọng nói
            speaker (str): Tên speaker (mặc định là "en-us", tương ứng với file en-us.pth)
            language (str): Ngôn ngữ của văn bản (english/chinese)
            speed (float): Tốc độ phát âm (1.0 là bình thường)
            
        Returns:
            str: Đường dẫn đến file âm thanh kết quả nếu thành công, None nếu thất bại
        """
        try:
            # Đảm bảo GPU tắt
            os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
            import torch
            torch.set_num_threads(4)  # Giới hạn số thread để tránh quá tải
            
            # Tạo tên file kết quả
            output_filename = f"tts_{int(time.time())}_{speaker}.wav"
            output_file = os.path.join(self.tts_dir, output_filename)
            
            # Tên file speaker embedding (.pth)
            if not speaker.endswith(".pth"):
                speaker_file = f"{speaker}.pth"
            else:
                speaker_file = speaker
            
            # Đường dẫn đến file speaker embedding
            speaker_path = os.path.join(self.model_dir, "checkpoints_v2", "base_speakers", "ses", speaker_file)
            
            # Kiểm tra speaker path tồn tại
            if not os.path.exists(speaker_path):
                logger.error(f"Khong tim thay speaker embedding: {speaker_path}")
                available_speakers = self.list_available_speakers()
                if available_speakers:
                    logger.info(f"Cac speaker co san: {available_speakers}")
                return None
            
            logger.info(f"Su dung speaker embedding: {speaker_path}")
            
            # ---------- PHƯƠNG PHÁP 1: Sử dụng MeloTTS + OpenVoice ----------
            logger.info("Phương pháp 1: Dùng MeloTTS kết hợp OpenVoice")
            
            temp_result = self.generate_speech_with_melotts(text, language, speed)
            
            if temp_result and os.path.exists(temp_result):
                # Sử dụng OpenVoice để áp dụng giọng nói
                logger.info("Áp dụng giọng nói bằng OpenVoice")
                
                # Phương pháp tương tự convert_voice nhưng ít tham số điều chỉnh hơn
                try:
                    from openvoice.api import ToneColorConverter
                    
                    # Đường dẫn đến file cấu hình và checkpoint
                    config_path = os.path.join(self.model_dir, "checkpoints_v2", "converter", "config.json")
                    checkpoint_path = os.path.join(self.model_dir, "checkpoints_v2", "converter", "checkpoint.pth")
                    
                    # Sử dụng CPU
                    device = 'cpu'
                    
                    # Khởi tạo converter
                    converter = ToneColorConverter(config_path, device=device)
                    converter.load_ckpt(checkpoint_path)
                    
                    # Trích xuất đặc trưng từ file nguồn
                    src_se = converter.extract_se([temp_result])
                    
                    # Load đặc trưng giọng nói đích
                    tgt_se = torch.load(speaker_path, map_location=device)
                    
                    # Chuyển đổi và lưu kết quả (tau=0.7 để giữ nội dung rõ ràng)
                    converter.convert(
                        audio_src_path=temp_result,
                        src_se=src_se,
                        tgt_se=tgt_se,
                        output_path=output_file,
                        tau=0.7
                    )
                    
                    # Kiểm tra kết quả
                    if os.path.exists(output_file):
                        logger.info(f"TTS thành công, đã lưu kết quả tại: {output_file}")
                        return output_file
                    
                except Exception as e:
                    logger.error(f"Lỗi khi áp dụng giọng nói: {str(e)}")
                    # Nếu bước OpenVoice lỗi, sử dụng kết quả tạm thời
                    logger.info(f"Sử dụng kết quả tạm thời: {temp_result}")
                    # Sao chép file từ thư mục tạm sang thư mục tts
                    import shutil
                    shutil.copy(temp_result, output_file)
                    return output_file
            
            return None
            
        except Exception as e:
            logger.error(f"Lỗi khi thực hiện text-to-speech: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None
            
    def generate_speech_with_melotts(self, text, language, speed):
        """
        Tạo âm thanh từ văn bản sử dụng thư viện MeloTTS
        
        Args:
            text (str): Văn bản cần chuyển đổi
            language (str): Ngôn ngữ của văn bản
            speed (float): Tốc độ phát âm
            
        Returns:
            str: Đường dẫn đến file âm thanh tạm
        """
        try:
            # Thử import MeloTTS
            from melo.api import TTS
            
            # Ánh xạ tên ngôn ngữ sang locale code (viết hoa)
            language_map = {
                "english": "EN",
                "chinese": "ZH",
                "french": "FR",
                "spanish": "ES",
                "japanese": "JP",
                "korean": "KR"
            }
            locale = language_map.get(language.lower(), "EN")
            
            # Tạo tạm file âm thanh tạm
            temp_file = os.path.join(self.temp_dir, f"temp_tts_{int(time.time())}.wav")
            
            # Khởi tạo TTS với ngôn ngữ - NGÔN NGỮ PHẢI VIẾT HOA
            logger.info(f"Khởi tạo MeloTTS với ngôn ngữ: {locale}")
            tts = TTS(language=locale)
            
            # Phân đoạn văn bản nếu quá dài để tránh lỗi
            if len(text) > 500:
                logger.info(f"Văn bản quá dài ({len(text)} ký tự), phân đoạn để xử lý...")
                audio_segments = []
                
                # Phân đoạn theo dấu câu
                if language.lower() == "english":
                    # Sử dụng biểu thức chính quy để tách câu tiếng Anh
                    sentences = re.split(r'(?<=[.!?])\s+', text)
                    
                    # Nhóm các câu thành đoạn nhỏ hơn 500 ký tự
                    chunks = []
                    current_chunk = ""
                    
                    for sentence in sentences:
                        if len(current_chunk) + len(sentence) < 500:
                            current_chunk += (" " if current_chunk else "") + sentence
                        else:
                            if current_chunk:
                                chunks.append(current_chunk)
                            current_chunk = sentence
                    
                    if current_chunk:
                        chunks.append(current_chunk)
                        
                    logger.info(f"Đã phân đoạn thành {len(chunks)} đoạn văn bản")
                    
                    # Xử lý từng đoạn và nối lại
                    temp_files = []
                    for i, chunk in enumerate(chunks):
                        chunk_file = os.path.join(self.temp_dir, f"temp_tts_chunk_{i}_{int(time.time())}.wav")
                        logger.info(f"Xử lý đoạn {i+1}/{len(chunks)}: {chunk[:50]}...")
                        
                        try:
                            tts.tts_to_file(
                                text=chunk, 
                                speaker_id=0,
                                output_path=chunk_file,
                                speed=speed,
                                sdp_ratio=0.2,
                                noise_scale=0.6
                            )
                            temp_files.append(chunk_file)
                        except Exception as chunk_err:
                            logger.error(f"Lỗi khi xử lý đoạn {i+1}: {str(chunk_err)}")
                    
                    # Nối các file âm thanh lại
                    if temp_files:
                        import numpy as np
                        from scipy.io import wavfile
                        
                        audio_data = []
                        sample_rate = None
                        
                        for tf in temp_files:
                            try:
                                sr, data = wavfile.read(tf)
                                if sample_rate is None:
                                    sample_rate = sr
                                audio_data.append(data)
                            except Exception as e:
                                logger.error(f"Lỗi khi đọc file {tf}: {str(e)}")
                        
                        if audio_data and sample_rate:
                            combined = np.concatenate(audio_data)
                            wavfile.write(temp_file, sample_rate, combined)
                            logger.info(f"Đã nối {len(temp_files)} đoạn âm thanh thành công")
                            
                            # Xóa các file tạm
                            for tf in temp_files:
                                try:
                                    os.remove(tf)
                                except:
                                    pass
                            
                            return temp_file
                    
                    # Nếu xử lý đoạn không thành công, thử xử lý cả văn bản
                    logger.warning("Xử lý phân đoạn không thành công, thử xử lý nguyên văn bản...")
                
                # Đối với các ngôn ngữ khác hoặc nếu phân đoạn tiếng Anh thất bại
                else:
                    logger.warning(f"Không hỗ trợ phân đoạn cho ngôn ngữ {language}, cắt ngắn văn bản...")
                    text = text[:500]  # Cắt ngắn văn bản
            
            # Xử lý văn bản (nguyên bản hoặc đã cắt ngắn)
            logger.info(f"Tạo file âm thanh với text: {text[:100]}...")
            tts.tts_to_file(
                text=text, 
                speaker_id=0,  # speaker_id=0 là giá trị mặc định
                output_path=temp_file,
                speed=speed,
                sdp_ratio=0.2,
                noise_scale=0.6
            )
            
            logger.info(f"Đã tạo file âm thanh tạm: {temp_file}")
            return temp_file
            
        except Exception as e:
            logger.error(f"Lỗi khi tạo âm thanh bằng MeloTTS: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return None

    def list_available_voices(self):
        """Liệt kê các giọng nói có sẵn trong mô hình OpenVoice"""
        voices = []
        # Thêm các giọng từ thư mục sample_voices
        try:
            voices_dir = os.path.join(self.model_dir, 'sample_voices')
            if os.path.exists(voices_dir):
                for item in os.listdir(voices_dir):
                    if item.endswith(('.wav', '.mp3', '.flac')):
                        # Bỏ qua các file có "sample" trong tên
                        if 'sample' not in item.lower():
                            voice_path = os.path.join(voices_dir, item)
                            voices.append(voice_path)
        except Exception as e:
            logger.error(f"Loi khi liet ke giong tu sample_voices: {str(e)}")
            
        # Thêm các giọng mẫu từ resources
        try:
            resources_dir = os.path.join(self.model_dir, 'resources')
            if os.path.exists(resources_dir):
                for item in os.listdir(resources_dir):
                    if item.endswith(('.wav', '.mp3')) and (
                        # Bỏ qua các file có "demo" hoặc "example" trong tên
                        not item.startswith('demo_speaker') and 
                        item != 'example_reference.mp3' and
                        'sample' not in item.lower()
                    ):
                        voice_path = os.path.join(resources_dir, item)
                        voices.append(voice_path)
        except Exception as e:
            logger.error(f"Loi khi liet ke giong tu resources: {str(e)}")
        
        return voices
        
    def list_available_speakers(self):
        """Liệt kê các speakers có sẵn cho Text-to-Speech"""
        try:
            # Tìm kiếm các file .pth trong thư mục base_speakers/ses
            speakers_dir = os.path.join(self.model_dir, "checkpoints_v2", "base_speakers", "ses")
            if not os.path.exists(speakers_dir):
                logger.error(f"Khong tim thay thu muc speakers: {speakers_dir}")
                return []
                
            # Lấy danh sách speakers từ các file .pth
            speakers = []
            for item in os.listdir(speakers_dir):
                if item.endswith('.pth'):
                    # Lấy tên không có đuôi .pth
                    speaker_name = os.path.splitext(item)[0]
                    speakers.append(speaker_name)
            
            logger.info(f"Da tim thay {len(speakers)} speakers cho TTS: {speakers}")
            return speakers
        except Exception as e:
            logger.error(f"Loi khi liet ke speakers cho TTS: {str(e)}")
            return []

    def get_model_info(self):
        """Lấy thông tin về model OpenVoice"""
        return {
            "name": "OpenVoice",
            "version": "v2",
            "type": "voice-conversion",
            "features": ["tts", "voice-conversion"],
            "supported_languages": ["english", "chinese", "french", "spanish", "japanese", "korean"]
        } 