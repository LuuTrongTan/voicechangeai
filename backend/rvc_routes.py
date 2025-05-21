from flask import Blueprint, request, jsonify
import os
import time
import json
from models.rvc_controller import RVCController
import logging

rvc_bp = Blueprint('rvc', __name__)
rvc = RVCController()
logger = logging.getLogger(__name__)

@rvc_bp.route('/api/rvc/models', methods=['GET'])
def list_rvc_models():
    """Liệt kê các mô hình RVC có sẵn"""
    try:
        models = rvc.list_available_voices()
        return jsonify({
            'success': True,
            'models': models
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@rvc_bp.route('/api/rvc/convert', methods=['POST'])
def convert_voice():
    """Chuyển đổi giọng nói sử dụng RVC"""
    if 'audio' not in request.files:
        return jsonify({'error': 'Không có file audio'}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'Tên file trống'}), 400
    
    target_voice = request.form.get('target_voice', 'default')
    f0up_key = int(request.form.get('f0up_key', 0))
    index_rate = float(request.form.get('index_rate', 0.5))
    protect = float(request.form.get('protect', 0.33))
    rms_mix_rate = float(request.form.get('rms_mix_rate', 0.25))
    
    try:
        # Lưu file tạm thời
        filename = os.path.join('uploads', audio_file.filename)
        audio_file.save(filename)
        
        # Chuyển đổi giọng nói
        result_path = rvc.convert_voice(
            filename, 
            target_voice, 
            f0up_key=f0up_key, 
            index_rate=index_rate, 
            protect=protect, 
            rms_mix_rate=rms_mix_rate
        )
        
        if result_path:
            return jsonify({
                'success': True,
                'result_url': f'/api/download/{os.path.basename(result_path)}'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Không thể chuyển đổi giọng nói'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        # Xóa file tạm
        if os.path.exists(filename):
            os.remove(filename)

@rvc_bp.route('/api/rvc/train', methods=['POST'])
def train_model():
    """Huấn luyện mô hình RVC mới"""
    if 'audio' not in request.files:
        return jsonify({'error': 'Không có file audio'}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'Tên file trống'}), 400
    
    model_name = request.form.get('model_name', '')
    if not model_name:
        return jsonify({'error': 'Tên mô hình không được để trống'}), 400
    
    try:
        # Lưu file tạm thời
        filename = os.path.join('uploads', audio_file.filename)
        audio_file.save(filename)
        
        # Huấn luyện mô hình
        success = rvc.train_model(filename, model_name)
        
        if success:
            return jsonify({
                'success': True,
                'message': f'Đã huấn luyện mô hình {model_name} thành công'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Không thể huấn luyện mô hình'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
    finally:
        # Xóa file tạm
        if os.path.exists(filename):
            os.remove(filename)

@rvc_bp.route('/api/uvr/models', methods=['GET'])
def list_uvr_models():
    """Lấy danh sách các model UVR5 có sẵn"""
    try:
        models = rvc.list_uvr_models()
        return jsonify({
            'success': True,
            'models': models
        })
    except Exception as e:
        logger.exception(f"Lỗi khi lấy danh sách model UVR5: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Không thể lấy danh sách model UVR5'
        }), 500

@rvc_bp.route('/api/rvc/separate-vocals', methods=['POST'])
def separate_vocals():
    """Tách giọng nói khỏi nhạc nền bằng UVR5"""
    if 'audio' not in request.files:
        return jsonify({'success': False, 'error': 'Không có file audio'}), 400
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'success': False, 'error': 'Tên file trống'}), 400
    model_name = request.form.get('model', None)
    if not model_name:
        return jsonify({'success': False, 'error': 'Thiếu tên mô hình UVR'}), 400
    # Lưu file tạm
    filename = os.path.join('uploads', audio_file.filename)
    audio_file.save(filename)
    try:
        logger.info(f"Bắt đầu tách vocals với model: {model_name}, file: {filename}")
        result = rvc.separate_vocals(filename, model_name)
        if result:
            logger.info(f"Kết quả tách vocals: {result}")
            response = {'success': True}
            if 'vocals' in result:
                vocals_path = result['vocals']
                vocals_filename = os.path.basename(vocals_path)
                vocals_url = f"/api/download/{vocals_filename}"
                logger.info(f"Vocals URL: {vocals_url}")
                response['vocals_url'] = vocals_url
            if 'instrumental' in result:
                instrumental_path = result['instrumental']
                instrumental_filename = os.path.basename(instrumental_path)
                instrumental_url = f"/api/download/{instrumental_filename}"
                logger.info(f"Instrumental URL: {instrumental_url}")
                response['instrumental_url'] = instrumental_url
            return jsonify(response)
        else:
            logger.error("Tách giọng thất bại: Không có kết quả từ controller")
            return jsonify({'success': False, 'error': 'Tách giọng thất bại'}), 500
    except Exception as e:
        logger.exception(f"Lỗi khi tách vocals: {str(e)}")
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        if os.path.exists(filename):
            os.remove(filename) 