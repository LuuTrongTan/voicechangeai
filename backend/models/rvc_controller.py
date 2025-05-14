import os
import logging
import sys
import traceback
import subprocess
import shutil
import datetime

logger = logging.getLogger(__name__)

class RVCController:
    def __init__(self):
        """Khởi tạo controller cho mô hình RVC (Retrieval-based Voice Conversion)"""
        self.model_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'ai', 'rvc'))
        self.output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'results'))
        self.models_dir = os.path.join(self.model_dir, 'models')
        self.weights_dir = os.path.join(self.model_dir, 'weights')
        self.logs_dir = os.path.join(self.model_dir, 'logs')
        self.uvr_dir = os.path.join(self.model_dir, 'infer', 'modules', 'uvr5')
        
        # Tạo các thư mục cần thiết nếu chưa tồn tại
        os.makedirs(self.output_dir, exist_ok=True)
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
        Chuyển đổi giọng nói từ file âm thanh đầu vào sang giọng nói đích sử dụng RVC
        
        Args:
            input_file_path (str): Đường dẫn đến file âm thanh đầu vào
            target_voice (str): Tên của giọng nói đích
            f0up_key (int): Điều chỉnh pitch, 0 nếu không thay đổi
            index_rate (float): Tỷ lệ áp dụng index feature, từ 0.0 đến 1.0
            protect (float): Bảo vệ tiếng nổi (consonants), từ 0.0 đến 0.5
            rms_mix_rate (float): Tỷ lệ trộn RMS, từ 0.0 đến 1.0
            
        Returns:
            str: Đường dẫn đến file âm thanh kết quả nếu thành công, None nếu thất bại
        """
        if not self.is_model_available:
            logger.error("Không thể chuyển đổi: Mô hình RVC chưa được cài đặt")
            return None
            
        # Tạo tên file kết quả
        base_name = os.path.basename(input_file_path)
        filename, ext = os.path.splitext(base_name)
        output_file = os.path.join(self.output_dir, f"{filename}_rvc_{target_voice}{ext}")
        
        try:
            # Kiểm tra xem có model và index tương ứng không
            model_path = self._find_model_path(target_voice)
            index_path = self._find_index_path(target_voice)
            
            if not model_path:
                logger.error(f"Không tìm thấy model cho {target_voice}")
                return None
            
            # Kiểm tra và giới hạn các tham số
            f0up_key = int(f0up_key)  # Đảm bảo là số nguyên
            
            # Giới hạn index_rate trong khoảng [0, 1]
            index_rate = max(0.0, min(1.0, float(index_rate)))
            
            # Giới hạn protect trong khoảng [0, 0.5]
            protect = max(0.0, min(0.5, float(protect)))
            
            # Giới hạn rms_mix_rate trong khoảng [0, 1]
            rms_mix_rate = max(0.0, min(1.0, float(rms_mix_rate)))
            
            # Gọi trực tiếp đến infer-web.py của RVC
            infer_web_path = os.path.join(self.model_dir, "infer-web.py")
            
            # Thiết lập các tham số cho infer-web.py với cú pháp mới
            cmd = [
                sys.executable,
                infer_web_path,
                "--tab", "0",                    # Tab 0: chuyển đổi giọng nói
                "--input_path", input_file_path,
                "--output_path", output_file,
                "--model_path", model_path,
                "--f0up_key", str(f0up_key),
                "--index_rate", str(index_rate),
                "--protect", str(protect),
                "--rms_mix_rate", str(rms_mix_rate),
                "--filter_radius", "3",          # Giá trị mặc định
                "--resample_sr", "0",            # Giữ nguyên tần số lấy mẫu
                "--mode", "1"                    # Chế độ chuyển đổi trực tiếp
            ]
            
            # Thêm index path nếu có
            if index_path:
                cmd.extend(["--index_path", index_path])
            
            logger.info(f"Đang chạy lệnh: {' '.join(cmd)}")
            
            # Thực thi và lấy kết quả
            original_dir = os.getcwd()
            try:
                # Chuyển đến thư mục RVC để script có thể tìm thấy các module cần thiết
                os.chdir(self.model_dir)
                
                process = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                stdout, stderr = process.communicate()
                
                # Ghi log kết quả
                logger.info(f"Kết quả từ RVC: {stdout}")
                if stderr:
                    logger.error(f"Lỗi từ RVC: {stderr}")
                
                # Kiểm tra kết quả và log
                if process.returncode != 0:
                    logger.error(f"Lỗi khi chạy RVC, mã trả về: {process.returncode}")
                    return None
            finally:
                # Khôi phục thư mục làm việc
                os.chdir(original_dir)
                
            # Kiểm tra xem file kết quả có tồn tại không
            if os.path.exists(output_file):
                logger.info(f"Đã tạo file kết quả: {output_file}")
                return output_file
            else:
                logger.error(f"Không tìm thấy file kết quả: {output_file}")
                return None
                
        except Exception as e:
            logger.exception(f"Lỗi khi xử lý RVC: {str(e)}")
            logger.error(traceback.format_exc())
            return None
    
    def separate_vocals(self, input_file_path, vocal_type='vocals'):
        """
        Tách giọng nói khỏi âm nhạc sử dụng UVR5
        
        Args:
            input_file_path (str): Đường dẫn đến file âm thanh đầu vào
            vocal_type (str): Loại tách ("vocals", "instrumental", "both")
            
        Returns:
            dict: Dictionary chứa đường dẫn đến các file kết quả
        """
        if not self.is_model_available:
            logger.error("Không thể tách giọng: Mô hình RVC chưa được cài đặt")
            return None
            
        # Tạo tên file kết quả
        base_name = os.path.basename(input_file_path)
        filename, ext = os.path.splitext(base_name)
        
        # Tạo thư mục output nếu chưa tồn tại
        os.makedirs(self.output_dir, exist_ok=True)
        
        try:
            # Gọi trực tiếp đến infer-web.py với tab UVR
            infer_web_path = os.path.join(self.model_dir, "infer-web.py")
            
            if not os.path.exists(infer_web_path):
                logger.error(f"Không tìm thấy script infer-web.py: {infer_web_path}")
                return None
            
            # Thiết lập tham số cho RVC UVR
            cmd = [
                sys.executable,
                infer_web_path,
                "--tab", "4",                   # Tab 4 là UVR (tách giọng nói)
                "--dir_wav_input", "",         # Để trống vì chúng ta chỉ xử lý một file
                "--wav_inputs", input_file_path,
                "--opt_vocal_root", self.output_dir,
                "--opt_ins_root", self.output_dir,
                "--opt_model", "HP2_all",      # Model mặc định cho UVR5
                "--format0", "wav"             # Format xuất ra
            ]
            
            logger.info(f"Đang chạy lệnh tách giọng nói: {' '.join(cmd)}")
            
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
                logger.info(f"Kết quả từ RVC UVR: {stdout}")
                if stderr:
                    logger.error(f"Lỗi từ RVC UVR: {stderr}")
                
                if process.returncode != 0:
                    logger.error(f"Lỗi khi tách giọng nói, mã trả về: {process.returncode}")
                    return None
            finally:
                os.chdir(original_dir)
            
            # Xác định tên file kết quả dựa trên quy ước đặt tên của RVC
            # Thông thường RVC sẽ tạo vocals_{tên_file} và instrument_{tên_file}
            vocals_output = os.path.join(self.output_dir, f"vocals_{filename}.wav")
            instrumental_output = os.path.join(self.output_dir, f"instrument_{filename}.wav")
            
            # Nếu không tìm thấy, tìm kiếm thêm
            if not os.path.exists(vocals_output):
                for file in os.listdir(self.output_dir):
                    if file.startswith("vocals_") and filename in file:
                        vocals_output = os.path.join(self.output_dir, file)
                        break
            
            if not os.path.exists(instrumental_output):
                for file in os.listdir(self.output_dir):
                    if file.startswith("instrument_") and filename in file:
                        instrumental_output = os.path.join(self.output_dir, file)
                        break
            
            # Trả về kết quả dựa trên yêu cầu
            results = {}
            
            if (vocal_type == 'vocals' or vocal_type == 'both') and os.path.exists(vocals_output):
                results['vocals'] = vocals_output
                
            if (vocal_type == 'instrumental' or vocal_type == 'both') and os.path.exists(instrumental_output):
                results['instrumental'] = instrumental_output
                
            if not results:
                logger.error("Không tìm thấy file kết quả sau khi tách giọng")
                return None
                
            return results
                
        except Exception as e:
            logger.exception(f"Lỗi khi tách giọng nói: {str(e)}")
            logger.error(traceback.format_exc())
            return None
            
    def train_model(self, dataset_path, model_name, epoch=200, batch_size=8, f0_method='dio'):
        """
        Huấn luyện model RVC mới

        Args:
            dataset_path (str): Đường dẫn đến thư mục chứa dữ liệu huấn luyện
            model_name (str): Tên cho model mới
            epoch (int): Số epoch huấn luyện
            batch_size (int): Kích thước batch
            f0_method (str): Phương pháp tính F0 ('dio', 'harvest', 'crepe')

        Returns:
            str: Đường dẫn đến model mới nếu thành công, None nếu thất bại
        """
        if not self.is_model_available:
            logger.error("Không thể huấn luyện: Mô hình RVC chưa được cài đặt")
            return None
        
        # Tạo thời gian bắt đầu để đặt tên cho model
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        full_model_name = f"{model_name}_{timestamp}"
        
        try:
            # Gọi trực tiếp đến infer-web.py với tab huấn luyện
            infer_web_path = os.path.join(self.model_dir, "infer-web.py")
            
            if not os.path.exists(infer_web_path):
                logger.error(f"Không tìm thấy script infer-web.py: {infer_web_path}")
                return None
            
            # Thiết lập tham số cho quá trình huấn luyện
            cmd = [
                sys.executable,
                infer_web_path,
                "--tab", "2",                     # Tab 2 là huấn luyện model
                "--exp_dir1", full_model_name,    # Tên thư mục thí nghiệm
                "--trainset_dir4", dataset_path,  # Đường dẫn tới dữ liệu huấn luyện
                "--sr2", "40k",                   # Tần số lấy mẫu mục tiêu
                "--if_f0_3", "True",              # Có sử dụng F0 không
                "--save_epoch10", "10",           # Lưu mỗi bao nhiêu epoch
                "--total_epoch11", str(epoch),    # Tổng số epoch
                "--batch_size12", str(batch_size), # Kích thước batch
                "--if_save_latest13", "True",     # Có lưu mô hình mới nhất không
                "--f0method8", f0_method,         # Phương pháp tính F0
                "--version19", "v2"               # Phiên bản RVC (v2 mới nhất)
            ]
            
            logger.info(f"Đang chạy lệnh huấn luyện model: {' '.join(cmd)}")
            
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
                logger.info(f"Kết quả từ quá trình huấn luyện: {stdout}")
                if stderr:
                    logger.error(f"Lỗi từ quá trình huấn luyện: {stderr}")
                
                if process.returncode != 0:
                    logger.error(f"Lỗi khi huấn luyện model, mã trả về: {process.returncode}")
                    return None
            finally:
                os.chdir(original_dir)
            
            # Đường dẫn dự kiến đến model đã huấn luyện
            model_path = os.path.join(self.logs_dir, full_model_name, "best_model.pth")
            index_path = os.path.join(self.logs_dir, full_model_name, f"{full_model_name}.index")
            
            # Kiểm tra xem model có tồn tại không
            if os.path.exists(model_path):
                # Sao chép model vào thư mục models
                target_path = os.path.join(self.models_dir, f"{full_model_name}.pth")
                shutil.copy(model_path, target_path)
                
                logger.info(f"Đã huấn luyện model thành công: {target_path}")
                return target_path
            else:
                logger.error(f"Không tìm thấy model sau khi huấn luyện: {model_path}")
                return None
                
        except Exception as e:
            logger.exception(f"Lỗi khi huấn luyện model: {str(e)}")
            logger.error(traceback.format_exc())
            return None
    
    def extract_f0(self, input_file_path, f0_method='dio'):
        """
        Trích xuất đường cong F0 từ file âm thanh
        
        Args:
            input_file_path (str): Đường dẫn đến file âm thanh
            f0_method (str): Phương pháp trích xuất F0 ('dio', 'harvest', 'crepe')
            
        Returns:
            str: Đường dẫn đến file F0 đã trích xuất nếu thành công, None nếu thất bại
        """
        if not self.is_model_available:
            logger.error("Không thể trích xuất F0: Mô hình RVC chưa được cài đặt")
            return None
            
        # Tạo tên file kết quả
        base_name = os.path.basename(input_file_path)
        filename, ext = os.path.splitext(base_name)
        output_file = os.path.join(self.output_dir, f"{filename}_f0.npy")
        
        try:
            # Gọi trực tiếp đến infer-web.py với tab trích xuất đặc trưng
            infer_web_path = os.path.join(self.model_dir, "infer-web.py")
            
            if not os.path.exists(infer_web_path):
                logger.error(f"Không tìm thấy script infer-web.py: {infer_web_path}")
                return None
            
            # Tạo thư mục dataset tạm để RVC xử lý
            temp_dataset_dir = os.path.join(self.output_dir, f"temp_dataset_{filename}")
            os.makedirs(temp_dataset_dir, exist_ok=True)
            
            # Sao chép file vào thư mục dataset
            temp_input_file = os.path.join(temp_dataset_dir, base_name)
            shutil.copy(input_file_path, temp_input_file)
            
            # Thiết lập tham số để trích xuất F0
            cmd = [
                sys.executable,
                infer_web_path,
                "--tab", "2",                      # Tab 2 là huấn luyện (bao gồm trích xuất đặc trưng)
                "--exp_dir1", f"f0_extract_{filename}", # Tên thư mục thí nghiệm
                "--trainset_dir4", temp_dataset_dir, # Đường dẫn đến dữ liệu input
                "--sr2", "40k",                    # Tần số lấy mẫu mục tiêu
                "--if_f0_3", "True",               # Có sử dụng F0 không
                "--f0method8", f0_method           # Phương pháp tính F0
            ]
            
            logger.info(f"Đang chạy lệnh trích xuất F0: {' '.join(cmd)}")
            
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
                logger.info(f"Kết quả từ quá trình trích xuất F0: {stdout}")
                if stderr:
                    logger.error(f"Lỗi từ quá trình trích xuất F0: {stderr}")
                
                if process.returncode != 0:
                    logger.error(f"Lỗi khi trích xuất F0, mã trả về: {process.returncode}")
                    return None
            finally:
                os.chdir(original_dir)
            
            # Tìm file F0 được trích xuất
            f0_output_dir = os.path.join(self.logs_dir, f"f0_extract_{filename}")
            f0_file_path = None
            
            if os.path.exists(f0_output_dir):
                # Tìm file .npy chứa thông tin F0
                for root, dirs, files in os.walk(f0_output_dir):
                    for file in files:
                        if file.endswith("_f0.npy"):
                            f0_file_path = os.path.join(root, file)
                            break
                    if f0_file_path:
                        break
            
            # Nếu tìm thấy, sao chép vào thư mục kết quả
            if f0_file_path:
                shutil.copy(f0_file_path, output_file)
                
                # Xóa thư mục tạm
                shutil.rmtree(temp_dataset_dir, ignore_errors=True)
                
                logger.info(f"Đã trích xuất F0 thành công: {output_file}")
                return output_file
            else:
                logger.error(f"Không tìm thấy file F0 sau khi trích xuất.")
                return None
                
        except Exception as e:
            logger.exception(f"Lỗi khi trích xuất F0: {str(e)}")
            logger.error(traceback.format_exc())
            return None
        finally:
            # Đảm bảo xóa thư mục tạm nếu còn tồn tại
            temp_dataset_dir = os.path.join(self.output_dir, f"temp_dataset_{filename}")
            if os.path.exists(temp_dataset_dir):
                shutil.rmtree(temp_dataset_dir, ignore_errors=True)
    
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
            weights_dir = os.path.join(self.model_dir, 'weights')
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
                            if voice_name not in voices:
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
            onnx_output_dir = os.path.join(self.output_dir, f"{model_name}_onnx")
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
            output_dir = os.path.join(self.output_dir, f"batch_{target_voice}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
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