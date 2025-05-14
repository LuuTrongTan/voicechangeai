from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Union, Any

class VoiceModelInterface(ABC):
    """
    Interface chuẩn cho các model AI xử lý giọng nói.
    Mọi controller AI nên kế thừa interface này để đảm bảo tính nhất quán.
    """
    
    @abstractmethod
    def initialize(self, config: Optional[Dict] = None) -> bool:
        """
        Khởi tạo model với cấu hình tùy chọn.
        
        Args:
            config: Cấu hình cho model (tùy chọn)
            
        Returns:
            bool: True nếu khởi tạo thành công, False nếu thất bại
        """
        pass
    
    @abstractmethod
    def convert_voice(self, input_file_path: str, target_voice: str, **kwargs) -> Optional[str]:
        """
        Chuyển đổi giọng nói từ file âm thanh đầu vào sang giọng nói đích.
        
        Args:
            input_file_path: Đường dẫn đến file âm thanh đầu vào
            target_voice: Đường dẫn đến file giọng nói tham chiếu hoặc ID
            **kwargs: Các tham số bổ sung đặc thù của từng model
            
        Returns:
            Optional[str]: Đường dẫn đến file kết quả nếu thành công, None nếu thất bại
        """
        pass
    
    @abstractmethod
    def text_to_speech(self, text: str, speaker: str, language: str, **kwargs) -> Optional[str]:
        """
        Chuyển văn bản thành giọng nói.
        
        Args:
            text: Văn bản cần chuyển đổi
            speaker: ID hoặc tên của speaker
            language: Ngôn ngữ của văn bản
            **kwargs: Các tham số bổ sung như tốc độ, cao độ...
            
        Returns:
            Optional[str]: Đường dẫn đến file kết quả nếu thành công, None nếu thất bại
        """
        pass
    
    @abstractmethod
    def list_available_voices(self) -> List[str]:
        """
        Liệt kê các giọng nói mẫu có sẵn trong model.
        
        Returns:
            List[str]: Danh sách đường dẫn đến các file giọng nói mẫu
        """
        pass
    
    @abstractmethod
    def list_available_speakers(self) -> List[str]:
        """
        Liệt kê các speakers có sẵn cho TTS.
        
        Returns:
            List[str]: Danh sách ID/tên các speakers
        """
        pass
    
    @abstractmethod
    def get_model_info(self) -> Dict[str, Any]:
        """
        Lấy thông tin về model.
        
        Returns:
            Dict: Thông tin về model như phiên bản, ngày tạo, tác giả...
        """
        pass
    
    def validate_audio(self, audio_path: str, **kwargs) -> str:
        """
        Kiểm tra và sửa file âm thanh nếu cần thiết.
        
        Args:
            audio_path: Đường dẫn đến file âm thanh
            **kwargs: Các tham số tùy chọn
            
        Returns:
            str: Đường dẫn đến file đã sửa
        """
        return audio_path  # Phương thức mặc định
