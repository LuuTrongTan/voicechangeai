import os
import logging
import sys
import traceback
import subprocess
import shutil
import datetime
import torch
import json
import time
import glob

logger = logging.getLogger(__name__)

class RVCController:
    def __init__(self):
        """Khởi tạo controller cho mô hình RVC (Retrieval-based Voice Conversion)"""
        self.model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ai', 'rvc'))
        self.results_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results'))
        self.models_dir = os.path.join(self.model_dir, 'models')
        self.weights_dir = os.path.join(self.model_dir, 'assets', 'weights')
        self.logs_dir = os.path.join(self.model_dir, 'logs')
        self.uvr_dir = os.path.join(self.model_dir, 'infer', 'modules', 'uvr5')
        
        # Cấu trúc thư mục mới
        self.rvc_results_dir = os.path.join(self.results_dir, "rvc")
        self.voice_conversion_dir = os.path.join(self.rvc_results_dir, "voice_conversion")
        self.uvr_results_dir = os.path.join(self.rvc_results_dir, "uvr")
        
        # Tạo các thư mục cần thiết nếu chưa tồn tại
        os.makedirs(self.results_dir, exist_ok=True)
        os.makedirs(self.rvc_results_dir, exist_ok=True)
        os.makedirs(self.voice_conversion_dir, exist_ok=True)
        os.makedirs(self.uvr_results_dir, exist_ok=True)
        os.makedirs(self.models_dir, exist_ok=True)
        os.makedirs(self.weights_dir, exist_ok=True)
        os.makedirs(self.logs_dir, exist_ok=True)
        
        # Kiểm tra xem mô hình đã được cài đặt chưa
        self.is_model_available = self._check_model_available()
        
        if not self.is_model_available:
            logger.warning("Mô hình RVC chưa được cài đặt hoặc thiếu các file cần thiết")
        else:
            logger.info("Đã khởi tạo RVC controller")
    
    def _check_model_available(self):
        """Kiểm tra xem mô hình RVC đã được cài đặt và sẵn sàng sử dụng chưa"""
        # Kiểm tra sự tồn tại của thư mục và các file cần thiết
        if not os.path.exists(self.model_dir):
            logger.error(f"Không tìm thấy thư mục RVC: {self.model_dir}")
            return False
            
        # Kiểm tra các file cần thiết
        required_files = [
            'requirements.txt',
            'infer-web.py'
        ]
        
        for file in required_files:
            if not os.path.exists(os.path.join(self.model_dir, file)):
                logger.error(f"Thiếu file {file} trong thư mục RVC")
                return False
                
        return True
    
    def convert_voice(self, input_file_path, target_voice, f0up_key=0, index_rate=0.5, protect=0.33, rms_mix_rate=0.25):
        """
        Chuyển đổi giọng nói từ file âm thanh đầu vào sang giọng nói đích sử dụng RVC CLI
        """
        if not self.is_model_available:
            logger.error("Không thể chuyển đổi: Mô hình RVC chưa được cài đặt")
            return None

        # Tạo tên file kết quả
        base_name = os.path.basename(input_file_path)
        filename, ext = os.path.splitext(base_name)
        target_voice_basename = os.path.splitext(os.path.basename(target_voice))[0]
        output_file = os.path.abspath(os.path.join(self.voice_conversion_dir, f"{filename}_rvc_{target_voice_basename}{ext}"))

        try:
            # Kiểm tra xem có model và index tương ứng không
            model_path = self._find_model_path(target_voice)
            index_path = self._find_index_path(target_voice)

            if not model_path:
                logger.error(f"Không tìm thấy model cho {target_voice}")
                return None

            # Đường dẫn tuyệt đối cho input
            input_path = os.path.abspath(input_file_path)

            # Đường dẫn model và index: chỉ lấy tên file
            model_name = os.path.basename(model_path)
            index_name = os.path.basename(index_path) if index_path else ""

            # Đường dẫn tới CLI script
            cli_script = os.path.join(self.model_dir, 'tools', 'infer_cli.py')
            cli_script = os.path.abspath(cli_script)

            # Thiết lập các tham số cho CLI
            cmd = [
                sys.executable,
                cli_script,
                "--input_path", input_path,
                "--opt_path", output_file,
                "--model_name", model_name,
                "--f0up_key", str(f0up_key),
                "--index_rate", str(index_rate),
                "--protect", str(protect),
                "--rms_mix_rate", str(rms_mix_rate),
            ]
            if index_name:
                cmd.extend(["--index_path", index_name])

            logger.info(f"Đang chạy lệnh CLI: {' '.join(cmd)}")

            # Thực thi và lấy kết quả
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=self.model_dir
            )
            stdout, stderr = process.communicate()

            logger.info(f"Kết quả CLI stdout: {stdout}")
            if stderr:
                logger.error(f"Kết quả CLI stderr: {stderr}")

            if process.returncode != 0:
                logger.error(f"Lỗi khi chạy CLI, mã trả về: {process.returncode}")
                return None

            # Kiểm tra xem file kết quả có tồn tại không
            if os.path.exists(output_file):
                logger.info(f"Đã tạo file kết quả: {output_file}")
                
                # Lưu thông tin vào lịch sử chuyển đổi
                self._save_conversion_history(input_file_path, target_voice, output_file, {
                    'f0up_key': f0up_key,
                    'index_rate': index_rate,
                    'protect': protect,
                    'rms_mix_rate': rms_mix_rate
                })
                
                return output_file
            else:
                logger.error(f"Không tìm thấy file kết quả: {output_file}")
                return None

        except Exception as e:
            logger.exception(f"Lỗi khi xử lý RVC CLI: {str(e)}")
            return None
    
    def _save_conversion_history(self, input_file_path, target_voice, output_file, params=None):
        """Lưu thông tin chuyển đổi vào lịch sử"""
        try:
            history_file = os.path.join(self.voice_conversion_dir, 'conversion_history.json')
            
            # Tạo bản ghi mới
            history_entry = {
                'timestamp': time.time(),
                'source_file': os.path.basename(input_file_path),
                'target_voice': target_voice,
                'result_file': os.path.basename(output_file),
                'result_url': f"/api/download/{os.path.basename(output_file)}",
                'params': params or {}
            }
            
            # Đọc lịch sử hiện tại
            history = []
            if os.path.exists(history_file):
                try:
                    with open(history_file, 'r', encoding='utf-8') as f:
                        history = json.load(f)
                except Exception as e:
                    logger.error(f"Lỗi khi đọc file lịch sử: {str(e)}")
                    history = []
            
            # Thêm bản ghi mới và lưu lại
            history.append(history_entry)
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Đã lưu thông tin chuyển đổi vào lịch sử: {os.path.basename(output_file)}")
            
        except Exception as e:
            logger.error(f"Lỗi khi lưu lịch sử chuyển đổi: {str(e)}")
    
    def separate_vocals(self, input_file_path, model_name=None, vocal_type='vocals'):
        """Tách giọng nói khỏi âm nhạc sử dụng UVR5"""
        if not self.is_model_available:
            logger.error("Không thể tách giọng: Mô hình RVC chưa được cài đặt")
            return None
        
        # Tạo tên file kết quả cố định
        base_name = os.path.basename(input_file_path)
        filename, ext = os.path.splitext(base_name)
        
        # Tạo thư mục đầu ra
        vocals_dir = os.path.join(self.uvr_results_dir, "vocals")
        instrumental_dir = os.path.join(self.uvr_results_dir, "instrumental")
        os.makedirs(vocals_dir, exist_ok=True)
        os.makedirs(instrumental_dir, exist_ok=True)
        
        try:
            # Lưu thư mục hiện tại
            original_dir = os.getcwd()
            
            # Chuyển đổi đường dẫn input thành đường dẫn tuyệt đối
            input_file_abs_path = os.path.abspath(input_file_path)
            
            if not os.path.exists(input_file_abs_path):
                logger.error(f"File đầu vào không tồn tại: {input_file_abs_path}")
                return None
            
            try:
                # Chuyển đến thư mục RVC
                os.chdir(self.model_dir)
                
                # Thêm thư mục RVC vào sys.path
                if self.model_dir not in sys.path:
                    sys.path.insert(0, self.model_dir)
                
                # Chọn model UVR5
                if model_name is None:
                    model_name = "HP2_all_vocals"
                
                # Đường dẫn đến mô hình UVR5
                uvr5_weights_dir = os.path.join(self.model_dir, 'assets', 'uvr5_weights')
                model_path = os.path.join(uvr5_weights_dir, f"{model_name}.pth")
                
                if not os.path.exists(model_path) and not model_name.startswith("onnx_"):
                    logger.error(f"Không tìm thấy mô hình UVR5: {model_path}")
                    available_models = self.list_uvr_models()
                    logger.info(f"Các mô hình khả dụng: {available_models}")
                    if len(available_models) > 0:
                        model_name = available_models[0]
                        model_path = os.path.join(uvr5_weights_dir, f"{model_name}.pth")
                        logger.info(f"Sử dụng mô hình thay thế: {model_name}")
                    else:
                        logger.error("Không có mô hình UVR5 nào khả dụng")
                        return None
                
                # Thiết lập weight_uvr5_root cho infer/modules/uvr5/modules.py
                os.environ["weight_uvr5_root"] = uvr5_weights_dir
                
                # Log thông tin xử lý
                logger.info(f"Tách giọng nói từ file: {input_file_abs_path}")
                logger.info(f"Sử dụng mô hình: {model_name}")
                logger.info(f"Thư mục vocals: {vocals_dir}")
                logger.info(f"Thư mục instrumental: {instrumental_dir}")
                
                # Kiểm tra xem có phải là DeEcho model không
                use_deecho = "DeEcho" in model_name
                
                # Tạo đối tượng xử lý âm thanh
                from infer.modules.uvr5.vr import AudioPre, AudioPreDeEcho
                
                # Kiểm tra GPU
                is_half = torch.cuda.is_available()
                device = "cuda" if torch.cuda.is_available() else "cpu"
                logger.info(f"Sử dụng thiết bị: {device}, half precision: {is_half}")
                
                # Tạo đối tượng xử lý tương ứng
                processor_class = AudioPreDeEcho if use_deecho else AudioPre
                audio_processor = processor_class(
                    agg=0,  # Mức độ xử lý (0-100)
                    model_path=model_path,
                    device=device,
                    is_half=is_half
                )
                
                # Kiểm tra xem model có phải là HP3 không
                is_hp3 = "HP3" in model_name
                
                # Xử lý âm thanh và trích xuất giọng nói
                try:
                    result = audio_processor._path_audio_(
                        input_file_abs_path,  # Đường dẫn tuyệt đối đầu vào
                        instrumental_dir,     # Thư mục cho nhạc nền
                        vocals_dir,           # Thư mục cho giọng hát
                        "wav",                # Định dạng xuất
                        is_hp3=is_hp3         # Có phải là HP3 không
                    )
                    logger.info(f"Kết quả xử lý âm thanh: {result}")
                except Exception as e:
                    logger.exception(f"Lỗi khi xử lý âm thanh: {str(e)}")
                    return None
                
                # Tìm các file kết quả từ UVR5
                result_files = self._find_uvr_output_files(vocals_dir, instrumental_dir, filename)
                
                if result_files:
                    # Sử dụng trực tiếp các file kết quả từ UVR5 thay vì tạo bản sao
                    vocals_output = result_files.get('vocals')
                    instrumental_output = result_files.get('instrumental')
                    
                    if vocals_output and instrumental_output:
                        # Cập nhật lịch sử UVR
                        self._save_uvr_history(input_file_path, model_name, vocals_output, instrumental_output)
                        
                        # Ghi log đường dẫn đầy đủ để debug
                        logger.info(f"UVR Result - vocals: {vocals_output}")
                        logger.info(f"UVR Result - instrumental: {instrumental_output}")
                        
                        # Trả về đường dẫn các file kết quả
                        return {
                            'vocals': vocals_output,
                            'instrumental': instrumental_output
                        }
                    else:
                        logger.error("Không tìm thấy đủ file vocals và instrumental từ UVR5")
                        return None
                else:
                    logger.error("Không tìm thấy file kết quả từ UVR5")
                    return None
                
            finally:
                # Quay lại thư mục ban đầu
                os.chdir(original_dir)
                
        except Exception as e:
            logger.exception(f"Lỗi khi tách giọng nói: {str(e)}")
            return None
        
    def _save_uvr_history(self, input_file_path, model_name, vocals_output, instrumental_output):
        """Lưu thông tin tách giọng nói vào lịch sử"""
        try:
            history_file = os.path.join(self.uvr_results_dir, 'uvr_history.json')
            
            # Tạo bản ghi mới với đường dẫn file thực tế
            history_entry = {
                'timestamp': time.time(),
                'source_file': os.path.basename(input_file_path),
                'model_name': model_name,
                'vocals_file': os.path.basename(vocals_output),
                'vocals_url': f"/api/download/{os.path.basename(vocals_output)}",
                'instrumental_file': os.path.basename(instrumental_output),
                'instrumental_url': f"/api/download/{os.path.basename(instrumental_output)}"
            }
            
            # Đọc lịch sử hiện tại
            history = []
            if os.path.exists(history_file):
                try:
                    with open(history_file, 'r', encoding='utf-8') as f:
                        history = json.load(f)
                except Exception as e:
                    logger.error(f"Lỗi khi đọc file lịch sử UVR: {str(e)}")
                    history = []
            
            # Thêm bản ghi mới và lưu lại
            history.append(history_entry)
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
                
            logger.info(f"Đã lưu thông tin tách giọng nói vào lịch sử UVR")
        
        except Exception as e:
            logger.error(f"Lỗi khi lưu lịch sử UVR: {str(e)}")
    
    def _find_uvr_output_files(self, vocals_dir, instrumental_dir, filename):
        """Tìm các file được tạo ra sau khi tách giọng với UVR5"""
        # Các định dạng tên file cần kiểm tra
        vocals_patterns = [
            os.path.join(vocals_dir, f"vocals_{filename}_*.wav"),
            os.path.join(vocals_dir, f"{filename}_vocals*.wav"),
            os.path.join(vocals_dir, f"{filename}_v*.wav"),
            os.path.join(vocals_dir, f"vocal_{filename}*.wav"),
            os.path.join(vocals_dir, 'uvr_output', f"{filename}*.wav"),
            os.path.join(vocals_dir, 'uvr_output', f"vocals_{filename}*.wav")
        ]
        
        instrumental_patterns = [
            os.path.join(instrumental_dir, f"instrument_{filename}_*.wav"),
            os.path.join(instrumental_dir, f"{filename}_instruments*.wav"),
            os.path.join(instrumental_dir, f"{filename}_i*.wav"),
            os.path.join(instrumental_dir, 'uvr_output', f"instrument_{filename}*.wav"),
            os.path.join(instrumental_dir, 'uvr_output', f"instruments_{filename}*.wav")
        ]
        
        # Kết quả
        results = {}
        
        # Kiểm tra các mẫu file vocal
        for pattern in vocals_patterns:
            matches = glob.glob(pattern)
            if matches:
                # Lấy file mới nhất nếu có nhiều kết quả
                latest_file = max(matches, key=os.path.getctime)
                logger.info(f"Tìm thấy file vocal: {latest_file}")
                results['vocals'] = latest_file
                break
                
        # Kiểm tra các mẫu file instrumental
        for pattern in instrumental_patterns:
            matches = glob.glob(pattern)
            if matches:
                # Lấy file mới nhất nếu có nhiều kết quả
                latest_file = max(matches, key=os.path.getctime)
                logger.info(f"Tìm thấy file instrumental: {latest_file}")
                results['instrumental'] = latest_file
                break
        
        # Nếu không tìm thấy, kiểm tra tất cả các file trong thư mục
        if 'vocals' not in results:
            logger.info(f"Kiểm tra tất cả file trong thư mục: {vocals_dir}")
            for root, _, files in os.walk(vocals_dir):
                for file in files:
                    if filename in file and file.endswith(".wav"):
                        results['vocals'] = os.path.join(root, file)
                        logger.info(f"Đã tìm thấy file vocals: {results['vocals']}")
                        break
        
        if 'instrumental' not in results:
            logger.info(f"Kiểm tra tất cả file trong thư mục: {instrumental_dir}")
            for root, _, files in os.walk(instrumental_dir):
                for file in files:
                    if filename in file and file.endswith(".wav"):
                        results['instrumental'] = os.path.join(root, file)
                        logger.info(f"Đã tìm thấy file instrumental: {results['instrumental']}")
                        break
            
        return results
    
    def _find_model_path(self, target_voice):
        """Tìm đường dẫn đến model dựa trên tên target voice"""
        # Tìm kiếm trong thư mục models
        model_path = None
        
        # Kiểm tra cả trường hợp tên đầy đủ với .pth và không có .pth
        potential_paths = [
            os.path.join(self.models_dir, f"{target_voice}.pth"),
            os.path.join(self.models_dir, target_voice)
        ]
        
        for path in potential_paths:
            if os.path.exists(path):
                model_path = path
                break
                
        # Nếu không tìm thấy, tìm kiếm trong weights
        if not model_path:
            weights_dir = os.path.join(self.model_dir, 'assets', 'weights')
            if os.path.exists(weights_dir):
                for path in [
                    os.path.join(weights_dir, f"{target_voice}.pth"),
                    os.path.join(weights_dir, target_voice)
                ]:
                    if os.path.exists(path):
                        model_path = path
                        break
        
        return model_path
    
    def _find_index_path(self, target_voice):
        """Tìm đường dẫn đến file index dựa trên tên target voice"""
        # Tìm kiếm trong thư mục logs
        index_path = None
        logs_dir = os.path.join(self.model_dir, 'logs')
        
        if os.path.exists(logs_dir):
            # Tìm với đuôi .index
            for item in os.listdir(logs_dir):
                if item.startswith(target_voice) and item.endswith('.index'):
                    index_path = os.path.join(logs_dir, item)
                    break
        
        return index_path
            
    def list_available_voices(self):
        """Liệt kê các giọng nói có sẵn trong mô hình RVC"""
        voices = []
        
        if not self.is_model_available:
            logger.warning("Không thể liệt kê giọng nói: Mô hình RVC chưa được cài đặt")
            return voices
            
        try:
            # Kiểm tra cả hai thư mục: models và weights
            for dir_path in [self.models_dir, self.weights_dir]:
                if os.path.exists(dir_path):
                    # Liệt kê các file mô hình
                    for item in os.listdir(dir_path):
                        if item.endswith('.pth'):
                            voice_name = os.path.splitext(item)[0]
                            # Loại bỏ sample_model khỏi danh sách
                            if voice_name not in voices and voice_name != "sample_model":
                                voices.append(voice_name)
            
            # Nếu không tìm thấy giọng nói nào, thêm giọng nói mặc định
            if not voices:
                voices = ["default"]
                logger.info("Không tìm thấy giọng nói tùy chỉnh RVC, sử dụng giọng mặc định")
                
        except Exception as e:
            logger.exception(f"Lỗi khi liệt kê giọng nói RVC: {str(e)}")
            voices = ["default"]  # Trả về giọng mặc định trong trường hợp lỗi
            
        return voices
        
    def fusion_models(self, model_a_name, model_b_name, alpha=0.5, target_model_name=None):
        """
        Dung hợp hai mô hình RVC thành một mô hình mới
        
        Args:
            model_a_name (str): Tên của mô hình A
            model_b_name (str): Tên của mô hình B
            alpha (float): Trọng số cho mô hình A, từ 0.0 đến 1.0
            target_model_name (str): Tên của mô hình mới, mặc định là "fusion_{model_a}_{model_b}"
            
        Returns:
            str: Đường dẫn đến mô hình mới nếu thành công, None nếu thất bại
        """
        if not self.is_model_available:
            logger.error("Không thể dung hợp mô hình: Mô hình RVC chưa được cài đặt")
            return None
            
        try:
            # Tìm đường dẫn đến các mô hình
            model_a_path = self._find_model_path(model_a_name)
            model_b_path = self._find_model_path(model_b_name)
            
            if not model_a_path:
                logger.error(f"Không tìm thấy mô hình A: {model_a_name}")
                return None
                
            if not model_b_path:
                logger.error(f"Không tìm thấy mô hình B: {model_b_name}")
                return None
                
            # Đảm bảo alpha trong khoảng [0,1]
            alpha = max(0.0, min(1.0, float(alpha)))
            
            # Tạo tên mô hình kết quả nếu không được chỉ định
            if not target_model_name:
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                target_model_name = f"fusion_{model_a_name}_{model_b_name}_{timestamp}"
                
            # Gọi trực tiếp đến infer-web.py với tab xử lý mô hình
            infer_web_path = os.path.join(self.model_dir, "infer-web.py")
            
            if not os.path.exists(infer_web_path):
                logger.error(f"Không tìm thấy script infer-web.py: {infer_web_path}")
                return None
                
            # Thiết lập tham số cho việc dung hợp mô hình
            cmd = [
                sys.executable,
                infer_web_path,
                "--tab", "5",                   # Tab 5 là ckpt处理 (xử lý mô hình)
                "--ckpt_a", model_a_path,       # Đường dẫn đến mô hình A
                "--ckpt_b", model_b_path,       # Đường dẫn đến mô hình B
                "--alpha_a", str(alpha),        # Trọng số cho mô hình A
                "--sr_", "40k",                 # Tần số lấy mẫu
                "--if_f0_", "是",               # Có sử dụng F0 hay không (是 là "có")
                "--info__", f"Fusion của {model_a_name} và {model_b_name}",  # Thông tin mô hình
                "--name_to_save0", target_model_name,  # Tên để lưu
                "--version_2", "v2"             # Phiên bản mô hình
            ]
            
            logger.info(f"Đang chạy lệnh dung hợp mô hình: {' '.join(cmd)}")
            
            # Thực thi và lấy kết quả
            original_dir = os.getcwd()
            try:
                os.chdir(self.model_dir)
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate()
                
                # Log kết quả
                logger.info(f"Kết quả từ quá trình dung hợp mô hình: {stdout}")
                if stderr:
                    logger.error(f"Lỗi từ quá trình dung hợp mô hình: {stderr}")
                
                if process.returncode != 0:
                    logger.error(f"Lỗi khi dung hợp mô hình, mã trả về: {process.returncode}")
                    return None
            finally:
                os.chdir(original_dir)
                
            # Kiểm tra mô hình mới có tồn tại không
            # RVC thường lưu mô hình vào thư mục weights
            expected_model_path = os.path.join(self.weights_dir, f"{target_model_name}.pth")
            
            if os.path.exists(expected_model_path):
                logger.info(f"Đã dung hợp mô hình thành công: {expected_model_path}")
                
                # Sao chép mô hình vào thư mục models để dễ sử dụng
                target_path = os.path.join(self.models_dir, f"{target_model_name}.pth")
                shutil.copy(expected_model_path, target_path)
                
                return target_path
            else:
                logger.error(f"Không tìm thấy mô hình sau khi dung hợp: {expected_model_path}")
                return None
                
        except Exception as e:
            logger.exception(f"Lỗi khi dung hợp mô hình: {str(e)}")
            logger.error(traceback.format_exc())
            return None
            
    def export_to_onnx(self, model_name):
        """
        Xuất mô hình RVC sang định dạng ONNX
        
        Args:
            model_name (str): Tên của mô hình cần xuất
            
        Returns:
            str: Đường dẫn đến thư mục chứa mô hình ONNX nếu thành công, None nếu thất bại
        """
        if not self.is_model_available:
            logger.error("Không thể xuất mô hình: Mô hình RVC chưa được cài đặt")
            return None
            
        try:
            # Tìm đường dẫn đến mô hình
            model_path = self._find_model_path(model_name)
            
            if not model_path:
                logger.error(f"Không tìm thấy mô hình: {model_name}")
                return None
                
            # Tạo thư mục đầu ra cho ONNX
            onnx_output_dir = os.path.join(self.results_dir, f"{model_name}_onnx")
            os.makedirs(onnx_output_dir, exist_ok=True)
            
            # Gọi trực tiếp đến infer-web.py với tab xuất ONNX
            infer_web_path = os.path.join(self.model_dir, "infer-web.py")
            
            if not os.path.exists(infer_web_path):
                logger.error(f"Không tìm thấy script infer-web.py: {infer_web_path}")
                return None
                
            # Thiết lập tham số cho việc xuất ONNX
            cmd = [
                sys.executable,
                infer_web_path,
                "--tab", "6",                   # Tab 6 là Onnx导出 (xuất ONNX)
                "--ckpt_dir", model_path,       # Đường dẫn đến mô hình
                "--onnx_dir", onnx_output_dir   # Đường dẫn đến thư mục đầu ra
            ]
            
            logger.info(f"Đang chạy lệnh xuất mô hình ONNX: {' '.join(cmd)}")
            
            # Thực thi và lấy kết quả
            original_dir = os.getcwd()
            try:
                os.chdir(self.model_dir)
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate()
                
                # Log kết quả
                logger.info(f"Kết quả từ quá trình xuất ONNX: {stdout}")
                if stderr:
                    logger.error(f"Lỗi từ quá trình xuất ONNX: {stderr}")
                
                if process.returncode != 0:
                    logger.error(f"Lỗi khi xuất ONNX, mã trả về: {process.returncode}")
                    return None
            finally:
                os.chdir(original_dir)
                
            # Kiểm tra xem có file ONNX được tạo ra không
            if os.path.exists(onnx_output_dir) and len(os.listdir(onnx_output_dir)) > 0:
                logger.info(f"Đã xuất mô hình ONNX thành công: {onnx_output_dir}")
                return onnx_output_dir
            else:
                logger.error(f"Không tìm thấy file ONNX sau khi xuất")
                return None
                
        except Exception as e:
            logger.exception(f"Lỗi khi xuất mô hình ONNX: {str(e)}")
            logger.error(traceback.format_exc())
            return None
            
    def batch_convert(self, input_dir, target_voice, f0up_key=0, index_rate=0.5, protect=0.33, rms_mix_rate=0.25):
        """
        Chuyển đổi hàng loạt các file âm thanh trong một thư mục
        
        Args:
            input_dir (str): Đường dẫn đến thư mục chứa các file âm thanh đầu vào
            target_voice (str): Tên của giọng nói đích
            f0up_key (int): Điều chỉnh pitch, 0 nếu không thay đổi
            index_rate (float): Tỷ lệ áp dụng index feature, từ 0.0 đến 1.0
            protect (float): Bảo vệ tiếng nổi (consonants), từ 0.0 đến 0.5
            rms_mix_rate (float): Tỷ lệ trộn RMS, từ 0.0 đến 1.0
            
        Returns:
            dict: Dictionary chứa đường dẫn đến các file kết quả nếu thành công, None nếu thất bại
        """
        if not self.is_model_available:
            logger.error("Không thể chuyển đổi hàng loạt: Mô hình RVC chưa được cài đặt")
            return None
            
        # Kiểm tra thư mục đầu vào
        if not os.path.exists(input_dir) or not os.path.isdir(input_dir):
            logger.error(f"Thư mục đầu vào không tồn tại: {input_dir}")
            return None
            
        try:
            # Tìm đường dẫn đến mô hình và index
            model_path = self._find_model_path(target_voice)
            index_path = self._find_index_path(target_voice)
            
            if not model_path:
                logger.error(f"Không tìm thấy mô hình cho {target_voice}")
                return None
                
            # Tạo thư mục đầu ra
            output_dir = os.path.join(self.results_dir, f"batch_{target_voice}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
            os.makedirs(output_dir, exist_ok=True)
            
            # Gọi trực tiếp đến infer-web.py với tab batch inference
            infer_web_path = os.path.join(self.model_dir, "infer-web.py")
            
            # Kiểm tra và giới hạn các tham số
            f0up_key = int(f0up_key)  # Đảm bảo là số nguyên
            
            # Giới hạn index_rate trong khoảng [0, 1]
            index_rate = max(0.0, min(1.0, float(index_rate)))
            
            # Giới hạn protect trong khoảng [0, 0.5]
            protect = max(0.0, min(0.5, float(protect)))
            
            # Giới hạn rms_mix_rate trong khoảng [0, 1]
            rms_mix_rate = max(0.0, min(1.0, float(rms_mix_rate)))
            
            # Thiết lập tham số cho batch inference
            cmd = [
                sys.executable,
                infer_web_path,
                "--tab", "1",                  # Tab 1 là 批量推理 (batch inference)
                "--dir_path", input_dir,       # Thư mục chứa file đầu vào
                "--opt", output_dir,           # Thư mục đầu ra
                "--model_name", model_path,    # Đường dẫn đến mô hình
                "--index_rate", str(index_rate),
                "--f0up_key", str(f0up_key),
                "--filter_radius", "3",
                "--resample_sr", "0",
                "--rms_mix_rate", str(rms_mix_rate),
                "--protect", str(protect)
            ]
            
            # Thêm index path nếu có
            if index_path:
                cmd.extend(["--index_path", index_path])
                
            logger.info(f"Đang chạy lệnh chuyển đổi hàng loạt: {' '.join(cmd)}")
            
            # Thực thi và lấy kết quả
            original_dir = os.getcwd()
            try:
                os.chdir(self.model_dir)
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate()
                
                # Log kết quả
                logger.info(f"Kết quả từ quá trình chuyển đổi hàng loạt: {stdout}")
                if stderr:
                    logger.error(f"Lỗi từ quá trình chuyển đổi hàng loạt: {stderr}")
                
                if process.returncode != 0:
                    logger.error(f"Lỗi khi chuyển đổi hàng loạt, mã trả về: {process.returncode}")
                    return None
            finally:
                os.chdir(original_dir)
                
            # Kiểm tra kết quả trong thư mục đầu ra
            if os.path.exists(output_dir) and len(os.listdir(output_dir)) > 0:
                # Thu thập các file kết quả
                result_files = {}
                for file in os.listdir(output_dir):
                    file_path = os.path.join(output_dir, file)
                    if os.path.isfile(file_path):
                        result_files[file] = file_path
                        
                logger.info(f"Đã chuyển đổi hàng loạt thành công: {len(result_files)} file")
                return result_files
            else:
                logger.error(f"Không tìm thấy file kết quả sau khi chuyển đổi hàng loạt")
                return None
                
        except Exception as e:
            logger.exception(f"Lỗi khi chuyển đổi hàng loạt: {str(e)}")
            logger.error(traceback.format_exc())
            return None
            
    def show_model_info(self, model_name):
        """
        Xem thông tin của mô hình
        
        Args:
            model_name (str): Tên của mô hình cần xem thông tin
            
        Returns:
            dict: Dictionary chứa thông tin của mô hình nếu thành công, None nếu thất bại
        """
        if not self.is_model_available:
            logger.error("Không thể xem thông tin mô hình: Mô hình RVC chưa được cài đặt")
            return None
            
        try:
            # Tìm đường dẫn đến mô hình
            model_path = self._find_model_path(model_name)
            
            if not model_path:
                logger.error(f"Không tìm thấy mô hình: {model_name}")
                return None
                
            # Gọi trực tiếp đến infer-web.py với tab xử lý mô hình để xem thông tin
            infer_web_path = os.path.join(self.model_dir, "infer-web.py")
            
            if not os.path.exists(infer_web_path):
                logger.error(f"Không tìm thấy script infer-web.py: {infer_web_path}")
                return None
                
            # Thiết lập tham số để xem thông tin mô hình
            cmd = [
                sys.executable,
                infer_web_path,
                "--tab", "5",                 # Tab 5 là ckpt处理 (xử lý mô hình)
                "--ckpt_path1", model_path    # Đường dẫn đến mô hình
            ]
            
            logger.info(f"Đang chạy lệnh xem thông tin mô hình: {' '.join(cmd)}")
            
            # Thực thi và lấy kết quả
            original_dir = os.getcwd()
            try:
                os.chdir(self.model_dir)
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate()
                
                # Log kết quả
                logger.info(f"Kết quả từ quá trình xem thông tin mô hình: {stdout}")
                if stderr:
                    logger.error(f"Lỗi từ quá trình xem thông tin mô hình: {stderr}")
                
                if process.returncode != 0:
                    logger.error(f"Lỗi khi xem thông tin mô hình, mã trả về: {process.returncode}")
                    return None
            finally:
                os.chdir(original_dir)
                
            # Phân tích thông tin mô hình từ kết quả
            model_info = {}
            try:
                # Thường RVC sẽ trả về thông tin dưới dạng chuỗi có định dạng
                # Ví dụ: "Info: Version=v2, Sample rate=40000, F0=True, ..."
                for line in stdout.split("\n"):
                    if ":" in line:
                        key, value = line.split(":", 1)
                        model_info[key.strip()] = value.strip()
                    elif "=" in line:
                        # Phân tích thông tin từ chuỗi có chứa các cặp key=value
                        parts = line.split(",")
                        for part in parts:
                            if "=" in part:
                                key, value = part.split("=", 1)
                                model_info[key.strip()] = value.strip()
            except Exception as e:
                logger.warning(f"Không thể phân tích thông tin mô hình: {str(e)}")
                # Nếu không phân tích được, trả về toàn bộ đầu ra dưới dạng thô
                model_info["raw_output"] = stdout
                
            return model_info
                
        except Exception as e:
            logger.exception(f"Lỗi khi xem thông tin mô hình: {str(e)}")
            logger.error(traceback.format_exc())
            return None
            
    def modify_model_info(self, model_name, new_info, new_model_name=None):
        """
        Sửa thông tin của mô hình
        
        Args:
            model_name (str): Tên của mô hình cần sửa thông tin
            new_info (str): Thông tin mới
            new_model_name (str): Tên mô hình mới sau khi sửa, mặc định là None (giữ nguyên tên)
            
        Returns:
            str: Đường dẫn đến mô hình mới nếu thành công, None nếu thất bại
        """
        if not self.is_model_available:
            logger.error("Không thể sửa thông tin mô hình: Mô hình RVC chưa được cài đặt")
            return None
            
        try:
            # Tìm đường dẫn đến mô hình
            model_path = self._find_model_path(model_name)
            
            if not model_path:
                logger.error(f"Không tìm thấy mô hình: {model_name}")
                return None
                
            # Tạo tên mô hình mới nếu không được chỉ định
            if not new_model_name:
                new_model_name = model_name
                
            # Gọi trực tiếp đến infer-web.py với tab xử lý mô hình để sửa thông tin
            infer_web_path = os.path.join(self.model_dir, "infer-web.py")
            
            if not os.path.exists(infer_web_path):
                logger.error(f"Không tìm thấy script infer-web.py: {infer_web_path}")
                return None
                
            # Thiết lập tham số để sửa thông tin mô hình
            cmd = [
                sys.executable,
                infer_web_path,
                "--tab", "5",                      # Tab 5 là ckpt处理 (xử lý mô hình)
                "--ckpt_path0", model_path,        # Đường dẫn đến mô hình
                "--info_", new_info,               # Thông tin mới
                "--name_to_save1", new_model_name  # Tên mô hình mới
            ]
            
            logger.info(f"Đang chạy lệnh sửa thông tin mô hình: {' '.join(cmd)}")
            
            # Thực thi và lấy kết quả
            original_dir = os.getcwd()
            try:
                os.chdir(self.model_dir)
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate()
                
                # Log kết quả
                logger.info(f"Kết quả từ quá trình sửa thông tin mô hình: {stdout}")
                if stderr:
                    logger.error(f"Lỗi từ quá trình sửa thông tin mô hình: {stderr}")
                
                if process.returncode != 0:
                    logger.error(f"Lỗi khi sửa thông tin mô hình, mã trả về: {process.returncode}")
                    return None
            finally:
                os.chdir(original_dir)
                
            # Kiểm tra mô hình mới có tồn tại không
            # RVC thường lưu mô hình với thông tin mới vào thư mục weights
            expected_model_path = os.path.join(self.weights_dir, f"{new_model_name}.pth")
            
            if os.path.exists(expected_model_path):
                logger.info(f"Đã sửa thông tin mô hình thành công: {expected_model_path}")
                
                # Nếu tên mô hình mới khác với tên cũ, sao chép vào thư mục models
                if new_model_name != model_name:
                    target_path = os.path.join(self.models_dir, f"{new_model_name}.pth")
                    shutil.copy(expected_model_path, target_path)
                    return target_path
                    
                return expected_model_path
            else:
                logger.error(f"Không tìm thấy mô hình sau khi sửa thông tin: {expected_model_path}")
                return None
                
        except Exception as e:
            logger.exception(f"Lỗi khi sửa thông tin mô hình: {str(e)}")
            logger.error(traceback.format_exc())
            return None
            
    def extract_small_model(self, checkpoint_path, save_name=None, is_f0=True, model_info=None):
        """
        Trích xuất mô hình nhỏ từ checkpoint lớn
        
        Args:
            checkpoint_path (str): Đường dẫn đến checkpoint cần trích xuất
            save_name (str): Tên để lưu mô hình mới, mặc định là tên của checkpoint + "_small"
            is_f0 (bool): Mô hình có sử dụng F0 hay không
            model_info (str): Thông tin để gắn vào mô hình mới
            
        Returns:
            str: Đường dẫn đến mô hình nhỏ nếu thành công, None nếu thất bại
        """
        if not self.is_model_available:
            logger.error("Không thể trích xuất mô hình: Mô hình RVC chưa được cài đặt")
            return None
            
        try:
            # Kiểm tra checkpoint tồn tại
            if not os.path.exists(checkpoint_path):
                logger.error(f"Không tìm thấy checkpoint: {checkpoint_path}")
                return None
                
            # Tạo tên để lưu nếu không được chỉ định
            if not save_name:
                base_name = os.path.basename(checkpoint_path)
                name, ext = os.path.splitext(base_name)
                save_name = f"{name}_small"
                
            # Tạo thông tin mô hình nếu không được chỉ định
            if not model_info:
                model_info = f"Extracted from {os.path.basename(checkpoint_path)}"
                
            # Gọi trực tiếp đến infer-web.py với tab xử lý mô hình để trích xuất
            infer_web_path = os.path.join(self.model_dir, "infer-web.py")
            
            if not os.path.exists(infer_web_path):
                logger.error(f"Không tìm thấy script infer-web.py: {infer_web_path}")
                return None
                
            # Thiết lập tham số để trích xuất mô hình nhỏ
            cmd = [
                sys.executable,
                infer_web_path,
                "--tab", "5",                     # Tab 5 là ckpt处理 (xử lý mô hình)
                "--ckpt_path2", checkpoint_path,  # Đường dẫn đến checkpoint
                "--save_name", save_name,         # Tên để lưu
                "--sr__", "40k",                  # Tần số lấy mẫu
                "--if_f0__", "1" if is_f0 else "0", # Có sử dụng F0 hay không
                "--version_1", "v2",              # Phiên bản mô hình
                "--info___", model_info           # Thông tin mô hình
            ]
            
            logger.info(f"Đang chạy lệnh trích xuất mô hình nhỏ: {' '.join(cmd)}")
            
            # Thực thi và lấy kết quả
            original_dir = os.getcwd()
            try:
                os.chdir(self.model_dir)
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate()
                
                # Log kết quả
                logger.info(f"Kết quả từ quá trình trích xuất mô hình nhỏ: {stdout}")
                if stderr:
                    logger.error(f"Lỗi từ quá trình trích xuất mô hình nhỏ: {stderr}")
                
                if process.returncode != 0:
                    logger.error(f"Lỗi khi trích xuất mô hình nhỏ, mã trả về: {process.returncode}")
                    return None
            finally:
                os.chdir(original_dir)
                
            # Kiểm tra mô hình mới có tồn tại không
            # RVC thường lưu mô hình trích xuất vào thư mục weights
            expected_model_path = os.path.join(self.weights_dir, f"{save_name}.pth")
            
            if os.path.exists(expected_model_path):
                logger.info(f"Đã trích xuất mô hình nhỏ thành công: {expected_model_path}")
                
                # Sao chép mô hình vào thư mục models để dễ sử dụng
                target_path = os.path.join(self.models_dir, f"{save_name}.pth")
                shutil.copy(expected_model_path, target_path)
                
                return target_path
            else:
                logger.error(f"Không tìm thấy mô hình sau khi trích xuất: {expected_model_path}")
                return None
                
        except Exception as e:
            logger.exception(f"Lỗi khi trích xuất mô hình nhỏ: {str(e)}")
            logger.error(traceback.format_exc())
            return None

    def list_uvr_models(self):
        """
        Liệt kê các model UVR5 có sẵn
        
        Returns:
            list: Danh sách tên các model UVR5 có sẵn
        """
        models = []
        uvr_weights_dir = os.path.join(self.model_dir, 'assets', 'uvr5_weights')
        
        if not os.path.exists(uvr_weights_dir):
            logger.error(f"Không tìm thấy thư mục UVR5 weights: {uvr_weights_dir}")
            return models
            
        try:
            # Liệt kê các file .pth trong thư mục weights
            for file in os.listdir(uvr_weights_dir):
                if file.endswith('.pth'):
                    # Chỉ lấy tên file không có phần mở rộng
                    model_name = os.path.splitext(file)[0]
                    models.append(model_name)
                    
            return models
        except Exception as e:
            logger.exception(f"Lỗi khi liệt kê model UVR5: {str(e)}")
            return models
            
    def _get_uvr_model_type(self, model_name):
        """
        Xác định loại model UVR5 dựa trên tên file
        
        Args:
            model_name (str): Tên file model
            
        Returns:
            str: Loại model ('vocals', 'instrumental', 'echo', 'reverb')
        """
        if 'HP2' in model_name or 'HP3' in model_name or 'HP5' in model_name:
            if 'only_main_vocal' in model_name:
                return 'main_vocal'
            elif 'all_vocals' in model_name:
                return 'all_vocals'
            else:
                return 'vocals'
        elif 'DeEcho' in model_name:
            if 'DeReverb' in model_name:
                return 'echo_reverb'
            elif 'Aggressive' in model_name:
                return 'echo_aggressive'
            else:
                return 'echo'
        else:
            return 'unknown' 