from flask import Blueprint, request, jsonify, send_from_directory, session
import os
import json
import logging
from werkzeug.utils import secure_filename
from datetime import datetime

# Import các thành phần cần thiết
from models.openvoice_controller import OpenVoiceController
from database import db, User, TextToSpeech, SystemLog, VoiceModel

# Import các decorators
from auth import login_required, admin_required, ai_engineer_required

# Khởi tạo logger
logger = logging.getLogger(__name__)

# Khởi tạo Blueprint
openvoice_bp = Blueprint('openvoice', __name__, url_prefix='/api')

# Khởi tạo controller
openvoice = OpenVoiceController()

# API Routes
@openvoice_bp.route('/tts/speakers', methods=['GET'])
def list_tts_speakers():
    """Liệt kê các speakers có sẵn cho Text-to-Speech"""
    speakers = openvoice.list_available_speakers()
    return jsonify({
        'speakers': speakers
    })

@openvoice_bp.route('/tts/generate', methods=['POST'])
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
        
        # Xác định người dùng (nếu đã đăng nhập)
        user_id = session.get('user_id')
        
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
            
            # Lưu thông tin vào cơ sở dữ liệu
            tts = TextToSpeech(
                user_id=user_id,
                text=text,
                result_file=os.path.basename(result_path),
                speaker=speaker,
                language=language,
                speed=speed
            )
            db.session.add(tts)
            db.session.commit()
            
            # Thêm log
            log = SystemLog(
                level='INFO',
                message=f"TTS thành công: {text[:30]}... -> {os.path.basename(result_path)}",
                component='openvoice'
            )
            db.session.add(log)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'result_url': result_url,
                'speaker': speaker,
                'language': language,
                'speed': speed
            })
        else:
            logger.error("Lỗi khi chuyển văn bản thành giọng nói")
            
            # Thêm log lỗi
            log = SystemLog(
                level='ERROR',
                message=f"Lỗi khi chuyển văn bản '{text[:30]}...' thành giọng nói",
                component='openvoice'
            )
            db.session.add(log)
            db.session.commit()
            
            return jsonify({
                'success': False,
                'error': 'Không thể chuyển văn bản thành giọng nói'
            }), 500
    except Exception as e:
        logger.exception(f"Lỗi xử lý TTS: {str(e)}")
        
        # Thêm log lỗi
        log = SystemLog(
            level='ERROR',
            message=f"Lỗi xử lý TTS: {str(e)}",
            component='openvoice'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'error': f'Lỗi xử lý: {str(e)}'}), 500

@openvoice_bp.route('/tts-history', methods=['GET'])
def get_tts_history():
    """Lấy lịch sử text-to-speech"""
    # Xác định người dùng
    user_id = session.get('user_id')
    
    # Chuẩn bị query
    query = TextToSpeech.query
    
    # Nếu không phải admin, chỉ hiển thị dữ liệu của người dùng hiện tại
    if user_id:
        user = User.query.get(user_id)
        if user and user.role != 'admin':
            query = query.filter_by(user_id=user_id)
    
    tts_entries = query.order_by(TextToSpeech.created_at.desc()).limit(100).all()
    
    history = [{
        'id': entry.id,
        'text': entry.text,
        'result_file': entry.result_file,
        'result_url': f"/api/download/{entry.result_file}",
        'speaker': entry.speaker,
        'language': entry.language,
        'speed': entry.speed,
        'created_at': entry.created_at.strftime('%Y-%m-%d %H:%M:%S')
    } for entry in tts_entries]
    
    return jsonify({
        'success': True,
        'history': history
    })

def init_openvoice(app):
    """Khởi tạo và đăng ký blueprint OpenVoice"""
    app.register_blueprint(openvoice_bp)
    return openvoice 