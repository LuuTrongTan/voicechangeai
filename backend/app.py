from flask import Flask, request, jsonify, send_from_directory
import os
import time
import json
from werkzeug.utils import secure_filename
import logging
import numpy as np
from flask_cors import CORS  # Thêm import CORS
import sys
import io
from logging.handlers import RotatingFileHandler
import traceback
from datetime import datetime

# Import các controllers và models
from models.openvoice_controller import OpenVoiceController
from models.rvc_controller import RVCController
from database import db, User, SystemLog, init_db
from admin_routes import admin_bp
from ai_engineer_routes import ai_engineer_bp
from rvc_routes import rvc_bp  # Thêm import RVC blueprint
from auth_routes import auth_bp  # Thêm import Auth blueprint

# Đường dẫn tới thư mục build của React
FRONTEND_BUILD_FOLDER = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'build'))

app = Flask(__name__, static_folder=FRONTEND_BUILD_FOLDER, static_url_path='')
# Thêm CORS để cho phép frontend gọi API
CORS(app, origins=["http://localhost:3000"])  # Cho phép tất cả các routes

# Cấu hình Flask
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULTS_FOLDER'] = 'results'
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voice_changer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'  # Thay đổi trong production

# Đường dẫn thư mục OpenVoice
app.config['OPENVOICE_FOLDER'] = os.path.join(app.config['RESULTS_FOLDER'], 'openvoice')
app.config['OPENVOICE_VC_FOLDER'] = os.path.join(app.config['OPENVOICE_FOLDER'], 'voice_conversion')
app.config['OPENVOICE_TTS_FOLDER'] = os.path.join(app.config['OPENVOICE_FOLDER'], 'tts')

# Đường dẫn thư mục RVC
app.config['RVC_FOLDER'] = os.path.join(app.config['RESULTS_FOLDER'], 'rvc')
app.config['RVC_VC_FOLDER'] = os.path.join(app.config['RVC_FOLDER'], 'voice_conversion')
app.config['RVC_UVR_FOLDER'] = os.path.join(app.config['RVC_FOLDER'], 'uvr')

# Khởi tạo database
db.init_app(app)

# Thiết lập logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        # Sử dụng RotatingFileHandler với encoding UTF-8
        RotatingFileHandler(
            'app.log', 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'  # Sử dụng UTF-8 để hỗ trợ tiếng Việt
        ),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Đặt encoding cho stdout để hỗ trợ tiếng Việt
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        # Python < 3.7 không có hàm reconfigure
        logger.warning("Không thể cấu hình lại encoding cho stdout")

# Thêm đường dẫn hiện tại vào sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Khởi tạo các controllers
openvoice = OpenVoiceController()
rvc = RVCController()

# Đảm bảo thư mục upload và results tồn tại
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULTS_FOLDER'], exist_ok=True)
os.makedirs(app.config['OPENVOICE_FOLDER'], exist_ok=True)
os.makedirs(app.config['OPENVOICE_VC_FOLDER'], exist_ok=True)
os.makedirs(app.config['OPENVOICE_TTS_FOLDER'], exist_ok=True)
os.makedirs(app.config['RVC_FOLDER'], exist_ok=True)
os.makedirs(app.config['RVC_VC_FOLDER'], exist_ok=True)
os.makedirs(app.config['RVC_UVR_FOLDER'], exist_ok=True)

# Đăng ký các blueprint
app.register_blueprint(admin_bp)
app.register_blueprint(ai_engineer_bp)
app.register_blueprint(rvc_bp)  # Đăng ký RVC blueprint
app.register_blueprint(auth_bp)  # Đăng ký Auth blueprint

# Tạo bảng database khi khởi động
with app.app_context():
    try:
        # Sử dụng hàm init_db để tạo lại database hoàn toàn
        init_db(app)
    except Exception as e:
        logger.error(f"Lỗi khi khởi tạo database: {str(e)}")

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'})

@app.route('/api/convert', methods=['POST'])
def convert_audio():
    if 'audio' not in request.files:
        logger.error("Không có file audio được gửi lên")
        return jsonify({'error': 'Không có file audio'}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        logger.error("Tên file trống")
        return jsonify({'error': 'Tên file trống'}), 400
    
    # Lấy thông tin chuyển đổi
    model_type = request.form.get('model_type', 'openvoice')
    target_voice = request.form.get('target_voice', 'default')
    tau = float(request.form.get('tau', 0.4))
    
    # Kiểm tra và giới hạn giá trị tau
    if tau < 0.1:
        tau = 0.1
    elif tau > 1.0:
        tau = 1.0
    
    # Lưu file tạm thời
    filename = secure_filename(audio_file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    audio_file.save(file_path)
    
    try:
        # Xử lý chuyển đổi giọng nói dựa trên model được chọn
        if model_type == 'openvoice':
            logger.info(f"Xử lý file {filename} với OpenVoice, target voice: {target_voice}, tau: {tau}")
            result_path = openvoice.convert_voice(file_path, target_voice, tau=tau)
        elif model_type == 'rvc':
            logger.info(f"Xử lý file {filename} với RVC, target voice: {target_voice}")
            result_path = rvc.convert_voice(file_path, target_voice)
        else:
            logger.error(f"Model không được hỗ trợ: {model_type}")
            return jsonify({'error': f'Model {model_type} không được hỗ trợ'}), 400
        
        if result_path:
            # Trả về URL để tải file kết quả
            result_url = f"/api/download/{os.path.basename(result_path)}"
            
            # Lưu thông tin vào lịch sử chuyển đổi
            history_entry = {
                'timestamp': time.time(),
                'source_file': filename,
                'target_voice': target_voice,
                'model_used': model_type,
                'tau': tau,
                'result_file': os.path.basename(result_path),
                'result_url': result_url
            }
            
            # Lưu lịch sử vào file
            if model_type == 'openvoice':
                history_file = os.path.join(app.config['OPENVOICE_VC_FOLDER'], 'conversion_history.json')
            else:
                history_file = os.path.join(app.config['RVC_VC_FOLDER'], 'conversion_history.json')
                
            history = []
            if os.path.exists(history_file):
                try:
                    with open(history_file, 'r', encoding='utf-8') as f:
                        history = json.load(f)
                except:
                    history = []
            
            history.append(history_entry)
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            
            return jsonify({
                'success': True,
                'result_url': result_url,
                'model_used': model_type,
                'tau': tau,
                'target_voice': target_voice
            })
        else:
            # Không sử dụng giải pháp dự phòng, trả về lỗi
            logger.error(f"Lỗi khi xử lý với model {model_type}")
            return jsonify({
                'success': False,
                'error': f'Mô hình {model_type} không thể xử lý file này'
            }), 500
            
    except Exception as e:
        logger.exception(f"Lỗi xử lý: {str(e)}")
        return jsonify({'error': f'Lỗi xử lý: {str(e)}'}), 500
    finally:
        # Xóa file gốc sau khi xử lý
        if os.path.exists(file_path):
            os.remove(file_path)

@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """API để tải xuống file kết quả"""
    # Kiểm tra file trong thư mục OpenVoice voice_conversion
    file_path = os.path.join(app.config['OPENVOICE_VC_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['OPENVOICE_VC_FOLDER'], filename, as_attachment=True)
    
    # Kiểm tra file trong thư mục OpenVoice tts
    file_path = os.path.join(app.config['OPENVOICE_TTS_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['OPENVOICE_TTS_FOLDER'], filename, as_attachment=True)
    
    # Kiểm tra file trong thư mục RVC voice_conversion
    file_path = os.path.join(app.config['RVC_VC_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['RVC_VC_FOLDER'], filename, as_attachment=True)
    
    # Kiểm tra file trong thư mục RVC UVR vocals
    vocals_dir = os.path.join(app.config['RVC_UVR_FOLDER'], 'vocals')
    file_path = os.path.join(vocals_dir, filename)
    if os.path.exists(file_path):
        logger.info(f"Đã tìm thấy file vocals: {file_path}")
        return send_from_directory(vocals_dir, filename, as_attachment=True)
    
    # Kiểm tra file trong thư mục RVC UVR instrumental
    instrumental_dir = os.path.join(app.config['RVC_UVR_FOLDER'], 'instrumental')
    file_path = os.path.join(instrumental_dir, filename)
    if os.path.exists(file_path):
        logger.info(f"Đã tìm thấy file instrumental: {file_path}")
        return send_from_directory(instrumental_dir, filename, as_attachment=True)
    
    # Kiểm tra file trong thư mục RVC UVR (thư mục gốc)
    file_path = os.path.join(app.config['RVC_UVR_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['RVC_UVR_FOLDER'], filename, as_attachment=True)
    
    # Kiểm tra trong các thư mục con của UVR tiềm năng khác
    for subdir in ['vocals', 'instrumental']:
        uvr_dir = os.path.join(app.config['RVC_UVR_FOLDER'], subdir)
        if os.path.exists(uvr_dir):
            # Kiểm tra các file trong thư mục
            for file in os.listdir(uvr_dir):
                # Kiểm tra tên file tương tự
                if filename in file:
                    logger.info(f"Đã tìm thấy file tương tự: {os.path.join(uvr_dir, file)}")
                    return send_from_directory(uvr_dir, file, as_attachment=True)
    
    # Kiểm tra file trong thư mục results chung
    file_path = os.path.join(app.config['RESULTS_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['RESULTS_FOLDER'], filename, as_attachment=True)
    
    # Nếu không tìm thấy file ở tất cả các vị trí
    logger.error(f"Không tìm thấy file: {filename} trong bất kỳ thư mục nào")
    return jsonify({'error': f'Không tìm thấy file {filename}'}), 404

@app.route('/api/play-audio', methods=['GET'])
def play_audio():
    """API để phát file âm thanh"""
    audio_path = request.args.get('path')
    
    if not audio_path:
        return jsonify({'error': 'Không có đường dẫn file'}), 400
    
    logger.info(f"Yêu cầu phát file âm thanh: {audio_path}")
    
    # Kiểm tra xem file có phải là file mẫu từ OpenVoice không
    openvoice_voices = openvoice.list_available_voices()
    if audio_path in openvoice_voices:
        # Phát file mẫu từ OpenVoice
        return send_from_directory(os.path.dirname(audio_path), os.path.basename(audio_path))
    
    # Kiểm tra xem file có phải là file mẫu từ RVC không
    rvc_voices = rvc.list_available_voices()
    if audio_path in rvc_voices:
        # Phát file mẫu từ RVC
        return send_from_directory(os.path.dirname(audio_path), os.path.basename(audio_path))
    
    # Kiểm tra trong các thư mục kết quả
    filename = os.path.basename(audio_path)
    logger.info(f"Tìm kiếm file: {filename}")
    
    # Kiểm tra trong thư mục OpenVoice voice_conversion
    file_path = os.path.join(app.config['OPENVOICE_VC_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['OPENVOICE_VC_FOLDER'], filename)
    
    # Kiểm tra trong thư mục OpenVoice tts
    file_path = os.path.join(app.config['OPENVOICE_TTS_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['OPENVOICE_TTS_FOLDER'], filename)
    
    # Kiểm tra trong thư mục RVC voice_conversion
    file_path = os.path.join(app.config['RVC_VC_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['RVC_VC_FOLDER'], filename)
    
    # Kiểm tra trong thư mục RVC UVR vocals
    vocals_dir = os.path.join(app.config['RVC_UVR_FOLDER'], 'vocals')
    file_path = os.path.join(vocals_dir, filename)
    if os.path.exists(file_path):
        logger.info(f"Đã tìm thấy file vocals để phát: {file_path}")
        return send_from_directory(vocals_dir, filename)
    
    # Kiểm tra trong thư mục RVC UVR instrumental
    instrumental_dir = os.path.join(app.config['RVC_UVR_FOLDER'], 'instrumental')
    file_path = os.path.join(instrumental_dir, filename)
    if os.path.exists(file_path):
        logger.info(f"Đã tìm thấy file instrumental để phát: {file_path}")
        return send_from_directory(instrumental_dir, filename)
    
    # Kiểm tra trong thư mục RVC UVR (thư mục gốc)
    file_path = os.path.join(app.config['RVC_UVR_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_from_directory(app.config['RVC_UVR_FOLDER'], filename)
    
    # Tìm các file tương tự trong các thư mục con của UVR
    for subdir in ['vocals', 'instrumental']:
        uvr_dir = os.path.join(app.config['RVC_UVR_FOLDER'], subdir)
        if os.path.exists(uvr_dir):
            for file in os.listdir(uvr_dir):
                # Kiểm tra tên file tương tự
                if filename in file:
                    logger.info(f"Đã tìm thấy file tương tự để phát: {os.path.join(uvr_dir, file)}")
                    return send_from_directory(uvr_dir, file)
    
    # Kiểm tra trong thư mục chung
    if os.path.exists(os.path.join(app.config['RESULTS_FOLDER'], filename)):
        return send_from_directory(app.config['RESULTS_FOLDER'], filename)
    
    logger.error(f"Không tìm thấy file âm thanh: {filename}")
    return jsonify({'error': 'Không tìm thấy file âm thanh'}), 404

@app.route('/api/models', methods=['GET'])
def list_models():
    """Liệt kê các mô hình và giọng nói có sẵn"""
    models = {
        'openvoice': openvoice.list_available_voices(),
        'rvc': rvc.list_available_voices()
    }
    return jsonify(models)

@app.route('/api/tts/speakers', methods=['GET'])
def list_tts_speakers():
    """Liệt kê các speakers có sẵn cho Text-to-Speech"""
    speakers = openvoice.list_available_speakers()
    return jsonify({
        'speakers': speakers
    })

@app.route('/api/tts/generate', methods=['POST'])
def text_to_speech():
    """API để chuyển văn bản thành giọng nói"""
    try:
        # Lấy dữ liệu từ request
        data = request.json
        
        if not data or 'text' not in data:
            logger.error("Không có dữ liệu văn bản được gửi lên")
            return jsonify({'error': 'Không có dữ liệu văn bản'}), 400
            
        text = data.get('text')
        speaker = data.get('speaker', 'default')
        language = data.get('language', 'english')
        speed = float(data.get('speed', 1.0))
        
        # Kiểm tra giá trị speed
        if speed < 0.5:
            speed = 0.5
        elif speed > 2.0:
            speed = 2.0
        
        logger.info(f"Xử lý text-to-speech: '{text}', speaker: {speaker}, language: {language}, speed: {speed}")
        
        # Chuyển văn bản thành giọng nói
        result_path = openvoice.text_to_speech(text, speaker, language, speed)
        
        if result_path:
            # Trả về URL để tải file kết quả
            result_url = f"/api/download/{os.path.basename(result_path)}"
            
            # Lưu thông tin vào lịch sử
            history_entry = {
                'timestamp': time.time(),
                'text': text,
                'speaker': speaker,
                'language': language,
                'speed': speed,
                'result_file': os.path.basename(result_path),
                'result_url': result_url
            }
            
            # Lưu lịch sử vào file
            history_file = os.path.join(app.config['OPENVOICE_TTS_FOLDER'], 'tts_history.json')
            history = []
            if os.path.exists(history_file):
                try:
                    with open(history_file, 'r', encoding='utf-8') as f:
                        history = json.load(f)
                except:
                    history = []
            
            history.append(history_entry)
            with open(history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
            
            return jsonify({
                'success': True,
                'result_url': result_url,
                'speaker': speaker,
                'language': language,
                'speed': speed
            })
        else:
            logger.error("Lỗi khi chuyển văn bản thành giọng nói")
            return jsonify({
                'success': False,
                'error': 'Không thể chuyển văn bản thành giọng nói'
            }), 500
            
    except Exception as e:
        logger.exception(f"Lỗi xử lý text-to-speech: {str(e)}")
        return jsonify({'error': f'Lỗi xử lý: {str(e)}'}), 500

@app.route('/api/admin/logs', methods=['GET'])
def get_logs():
    """API chỉ dành cho admin để xem logs"""
    # Thêm xác thực admin ở đây
    try:
        with open("app.log", "r") as log_file:
            logs = log_file.readlines()[-100:]  # 100 dòng cuối
        return jsonify({'logs': logs})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/voice-details', methods=['GET'])
def get_voice_details():
    """Lấy thông tin chi tiết về file giọng nói"""
    voice_path = request.args.get('path')
    
    if not voice_path or not os.path.exists(voice_path):
        return jsonify({'error': 'Không tìm thấy file giọng nói'}), 404
    
    try:
        import librosa
        
        # Đọc file âm thanh
        y, sr = librosa.load(voice_path, sr=None)
        
        # Tính toán các thông số
        duration = librosa.get_duration(y=y, sr=sr)
        file_size = os.path.getsize(voice_path)
        
        # Tính toán độ cao giọng trung bình (F0)
        f0, voiced_flag, voiced_probs = librosa.pyin(
            y, fmin=librosa.note_to_hz('C2'), 
            fmax=librosa.note_to_hz('C7'),
            sr=sr
        )
        f0_valid = f0[voiced_flag]
        f0_mean = f0_valid.mean() if len(f0_valid) > 0 else 0
        
        # Tính toán năng lượng
        energy = np.mean(librosa.feature.rms(y=y)[0])
        
        # Phân loại giọng (đơn giản theo F0)
        voice_type = "Nam" if f0_mean < 160 else "Nữ"
        if f0_mean < 110:
            voice_range = "Trầm"
        elif f0_mean < 200:
            voice_range = "Vừa"
        else:
            voice_range = "Cao"
        
        return jsonify({
            'filename': os.path.basename(voice_path),
            'path': voice_path,
            'duration': round(duration, 2),
            'sample_rate': sr,
            'file_size': file_size,
            'file_size_mb': round(file_size / (1024 * 1024), 2),
            'average_pitch': round(f0_mean, 2) if f0_mean else 0,
            'energy': round(energy, 4),
            'voice_type': voice_type,
            'voice_range': voice_range
        })
    except Exception as e:
        logger.exception(f"Lỗi khi phân tích file âm thanh: {str(e)}")
        return jsonify({
            'filename': os.path.basename(voice_path),
            'path': voice_path,
            'file_size': os.path.getsize(voice_path),
            'file_size_mb': round(os.path.getsize(voice_path) / (1024 * 1024), 2),
            'error': str(e)
        })

@app.route('/api/conversion-history', methods=['GET'])
def get_conversion_history():
    """Lấy lịch sử chuyển đổi giọng nói"""
    model_type = request.args.get('model_type', 'all')
    
    if model_type == 'openvoice':
        history_file = os.path.join(app.config['OPENVOICE_VC_FOLDER'], 'conversion_history.json')
    elif model_type == 'rvc':
        history_file = os.path.join(app.config['RVC_VC_FOLDER'], 'conversion_history.json')
    else:
        # Mặc định hoặc 'all' - trả về danh sách trống
        return jsonify([])
    
    if not os.path.exists(history_file):
        return jsonify([])
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        return jsonify(history)
    except Exception as e:
        logger.error(f"Lỗi khi đọc lịch sử chuyển đổi: {str(e)}")
        return jsonify([])

@app.route('/api/uvr-history', methods=['GET'])
def get_uvr_history():
    """Lấy lịch sử tách giọng nói UVR"""
    history_file = os.path.join(app.config['RVC_UVR_FOLDER'], 'uvr_history.json')
    
    logger.info(f"Đang tìm kiếm file lịch sử UVR tại: {history_file}")
    
    if not os.path.exists(history_file):
        logger.warning(f"Không tìm thấy file lịch sử UVR: {history_file}")
        return jsonify([])
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        
        # Thêm log để gỡ lỗi
        logger.info(f"Đã đọc lịch sử UVR: {len(history)} mục")
        
        # Kiểm tra và cập nhật các đường dẫn URL nếu cần
        for item in history:
            # Tạo các đường dẫn đến thư mục vocals và instrumental
            vocals_dir = os.path.join(app.config['RVC_UVR_FOLDER'], 'vocals')
            instrumental_dir = os.path.join(app.config['RVC_UVR_FOLDER'], 'instrumental')
            
            # Kiểm tra file vocals
            expected_vocals_file = item.get('vocals_file')
            if expected_vocals_file:
                vocals_path = os.path.join(vocals_dir, expected_vocals_file)
                if not os.path.exists(vocals_path):
                    # Tìm file thay thế trong thư mục vocals
                    source_file_base = os.path.splitext(item.get('source_file', ''))[0]
                    if source_file_base:
                        for filename in os.listdir(vocals_dir):
                            if source_file_base in filename:
                                logger.info(f"Tìm thấy file vocals thay thế: {filename} thay vì {expected_vocals_file}")
                                item['vocals_file'] = filename
                                item['vocals_url'] = f"/api/download/{filename}"
                                break
            
            # Kiểm tra file instrumental
            expected_instrumental_file = item.get('instrumental_file')
            if expected_instrumental_file:
                instrumental_path = os.path.join(instrumental_dir, expected_instrumental_file)
                if not os.path.exists(instrumental_path):
                    # Tìm file thay thế trong thư mục instrumental
                    source_file_base = os.path.splitext(item.get('source_file', ''))[0]
                    if source_file_base:
                        for filename in os.listdir(instrumental_dir):
                            if source_file_base in filename:
                                logger.info(f"Tìm thấy file instrumental thay thế: {filename} thay vì {expected_instrumental_file}")
                                item['instrumental_file'] = filename
                                item['instrumental_url'] = f"/api/download/{filename}"
                                break
            
            # Đảm bảo rằng vocals_url và instrumental_url đều bắt đầu bằng /api/download/
            if 'vocals_url' in item and not item['vocals_url'].startswith('/api/download/'):
                item['vocals_url'] = f"/api/download/{item['vocals_file']}"
                
            if 'instrumental_url' in item and not item['instrumental_url'].startswith('/api/download/'):
                item['instrumental_url'] = f"/api/download/{item['instrumental_file']}"
                
        # Cập nhật file lịch sử với các đường dẫn đã chỉnh sửa
        with open(history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
            
        return jsonify(history)
    except Exception as e:
        logger.exception(f"Lỗi khi đọc lịch sử UVR: {str(e)}")
        return jsonify([])

@app.route('/api/tts-history', methods=['GET'])
def get_tts_history():
    """Lấy lịch sử text-to-speech"""
    history_file = os.path.join(app.config['OPENVOICE_TTS_FOLDER'], 'tts_history.json')
    
    if not os.path.exists(history_file):
        return jsonify([])
    
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
        return jsonify(history)
    except Exception as e:
        logger.error(f"Lỗi khi đọc lịch sử TTS: {str(e)}")
        return jsonify([])

# Route cho frontend
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Route cho frontend"""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

def log_to_system(level, message, source='API', user_id=None, details=None):
    """Ghi log vào database"""
    log = SystemLog(
        level=level,
        message=message,
        source=source,
        user_id=user_id,
        details=details
    )
    db.session.add(log)
    db.session.commit()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 