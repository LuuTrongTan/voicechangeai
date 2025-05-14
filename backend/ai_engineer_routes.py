from flask import Blueprint, jsonify, request
from database import db, User, SystemLog
import os
import time
from werkzeug.utils import secure_filename

ai_engineer_bp = Blueprint('ai_engineer', __name__, url_prefix='/api/ai-engineer')

# Thư mục lưu trữ model
MODELS_DIR = os.path.join(os.path.dirname(__file__), 'models')
os.makedirs(MODELS_DIR, exist_ok=True)

# Thư mục lưu trữ trainings
TRAININGS_DIR = os.path.join(os.path.dirname(__file__), 'trainings')
os.makedirs(TRAININGS_DIR, exist_ok=True)

@ai_engineer_bp.route('/models', methods=['GET'])
def get_models():
    """Lấy danh sách các models"""
    try:
        models = []
        
        # Tìm tất cả các files trong thư mục models
        openvoice_dir = os.path.join(MODELS_DIR, 'openvoice')
        rvc_dir = os.path.join(MODELS_DIR, 'rvc')
        
        os.makedirs(openvoice_dir, exist_ok=True)
        os.makedirs(rvc_dir, exist_ok=True)
        
        # Lấy danh sách models OpenVoice
        if os.path.exists(openvoice_dir):
            for model in os.listdir(openvoice_dir):
                if os.path.isdir(os.path.join(openvoice_dir, model)):
                    models.append({
                        'id': len(models) + 1,
                        'name': model,
                        'type': 'openvoice',
                        'is_active': True,
                        'created_at': time.time()
                    })
        
        # Lấy danh sách models RVC
        if os.path.exists(rvc_dir):
            for model in os.listdir(rvc_dir):
                if os.path.isdir(os.path.join(rvc_dir, model)):
                    models.append({
                        'id': len(models) + 1,
                        'name': model,
                        'type': 'rvc',
                        'is_active': True,
                        'created_at': time.time()
                    })
        
        return jsonify(models)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_engineer_bp.route('/trainings', methods=['GET'])
def get_trainings():
    """Lấy danh sách các phiên training"""
    try:
        trainings = []
        
        # Tạo dữ liệu mẫu
        # Trong thực tế, dữ liệu này sẽ được lấy từ cơ sở dữ liệu
        trainings = [
            {
                'id': 1,
                'model': 'Speaker 1',
                'type': 'openvoice',
                'status': 'completed',
                'start_time': time.time() - 3600,
                'end_time': time.time() - 1800,
                'progress': 100
            },
            {
                'id': 2,
                'model': 'Singer 2',
                'type': 'rvc',
                'status': 'in_progress',
                'start_time': time.time() - 1800,
                'end_time': None,
                'progress': 65
            }
        ]
        
        return jsonify(trainings)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_engineer_bp.route('/models/upload', methods=['POST'])
def upload_model():
    """Upload model mới"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Không có file được gửi lên'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Tên file trống'}), 400
        
        model_type = request.form.get('type', 'openvoice')
        model_name = request.form.get('name', file.filename)
        description = request.form.get('description', '')
        
        # Đường dẫn lưu model
        model_dir = os.path.join(MODELS_DIR, model_type, model_name)
        os.makedirs(model_dir, exist_ok=True)
        
        # Lưu file
        filename = secure_filename(file.filename)
        file_path = os.path.join(model_dir, filename)
        file.save(file_path)
        
        return jsonify({
            'success': True,
            'message': 'Upload model thành công',
            'model': {
                'name': model_name,
                'type': model_type,
                'description': description,
                'file': filename
            }
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@ai_engineer_bp.route('/training/start', methods=['POST'])
def start_training():
    """Bắt đầu training model"""
    try:
        data = request.json
        model_name = data.get('model_name')
        model_type = data.get('model_type')
        
        if not model_name:
            return jsonify({'error': 'Vui lòng cung cấp tên model'}), 400
        
        if not model_type:
            return jsonify({'error': 'Vui lòng cung cấp loại model'}), 400
        
        # Trong thực tế, tại đây sẽ bắt đầu quá trình training
        # Có thể sử dụng threading hoặc celery để xử lý bất đồng bộ
        
        training_id = int(time.time())
        
        return jsonify({
            'success': True,
            'message': f'Đã bắt đầu training model {model_name}',
            'training_id': training_id
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500 