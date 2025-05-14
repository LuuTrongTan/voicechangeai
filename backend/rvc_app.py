from flask import Blueprint, request, jsonify, send_from_directory, session
import os
import time
import json
import logging
import shutil
from werkzeug.utils import secure_filename

# Import các thành phần cần thiết
from models.rvc_controller import RVCController
from database import db, User, VoiceConversion, SystemLog, VoiceModel

# Import các decorators
from auth import login_required, admin_required, ai_engineer_required

# Khởi tạo logger
logger = logging.getLogger(__name__)

# Khởi tạo Blueprint
rvc_bp = Blueprint('rvc', __name__, url_prefix='/api')

# Khởi tạo controller
rvc = RVCController()

@rvc_bp.route('/rvc/models', methods=['GET'])
def list_rvc_models():
    """API để liệt kê các mô hình RVC có sẵn, bao gồm models, indices và uvr_models"""
    try:
        # Lấy danh sách mô hình từ controller
        models = rvc.list_available_voices()
        
        # Mặc định hiện tại chưa có hàm lấy indices và uvr_models
        # Chúng ta có thể thêm sau khi phát triển các hàm này trong controller
        indices = []
        uvr_models = ["HP2", "HP5", "VR"]  # Các model UVR mặc định
        
        return jsonify({
            "models": models,
            "indices": indices,
            "uvr_models": uvr_models
        })
    except Exception as e:
        logger.exception(f"Lỗi khi liệt kê mô hình RVC: {str(e)}")
        return jsonify({
            "error": f"Lỗi: {str(e)}"
        }), 500

@rvc_bp.route('/rvc/train', methods=['POST'])
@ai_engineer_required
def train_rvc_model():
    """API để huấn luyện model RVC mới (chỉ dành cho Kỹ sư AI)"""
    if 'dataset' not in request.files:
        return jsonify({'error': 'Không có dữ liệu huấn luyện'}), 400
        
    dataset_file = request.files['dataset']
    if dataset_file.filename == '':
        return jsonify({'error': 'Tên file trống'}), 400
        
    model_name = request.form.get('model_name')
    if not model_name:
        return jsonify({'error': 'Thiếu tên model'}), 400
        
    # Tham số huấn luyện tùy chọn
    epochs = int(request.form.get('epochs', 200))
    batch_size = int(request.form.get('batch_size', 8))
    f0_method = request.form.get('f0_method', 'dio')
    
    # Lưu dataset vào thư mục tạm
    upload_folder = os.path.join(os.path.dirname(__file__), 'uploads')
    dataset_dir = os.path.join(upload_folder, 'rvc_dataset_' + str(int(time.time())))
    os.makedirs(dataset_dir, exist_ok=True)
    
    # Nếu là file zip, giải nén
    if dataset_file.filename.endswith('.zip'):
        import zipfile
        zip_path = os.path.join(upload_folder, secure_filename(dataset_file.filename))
        dataset_file.save(zip_path)
        
        # Giải nén file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(dataset_dir)
            
        # Xóa file zip sau khi giải nén
        os.remove(zip_path)
    else:
        # Nếu là file âm thanh đơn lẻ
        audio_path = os.path.join(dataset_dir, secure_filename(dataset_file.filename))
        dataset_file.save(audio_path)
    
    # Huấn luyện model
    try:
        result_path = rvc.train_model(
            dataset_path=dataset_dir,
            model_name=model_name,
            epoch=epochs,
            batch_size=batch_size,
            f0_method=f0_method
        )
        
        if result_path:
            # Thêm log thành công
            log = SystemLog(
                level='INFO',
                message=f"Huấn luyện model RVC thành công: {model_name}",
                component='rvc'
            )
            db.session.add(log)
            
            # Thêm model vào database
            new_model = VoiceModel(
                name=model_name,
                file_path=result_path,
                type='rvc',
                is_public=True,
                created_by=session.get('user_id')
            )
            db.session.add(new_model)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'model_path': result_path,
                'model_name': model_name
            })
        else:
            # Thêm log lỗi
            log = SystemLog(
                level='ERROR',
                message=f"Huấn luyện model RVC thất bại: {model_name}",
                component='rvc'
            )
            db.session.add(log)
            db.session.commit()
            
            return jsonify({
                'success': False,
                'error': 'Không thể huấn luyện model. Kiểm tra logs để biết thêm chi tiết.'
            }), 500
    except Exception as e:
        logger.exception(f"Lỗi khi huấn luyện model RVC: {str(e)}")
        
        # Thêm log lỗi
        log = SystemLog(
            level='ERROR',
            message=f"Lỗi khi huấn luyện model RVC: {str(e)}",
            component='rvc'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'error': f'Lỗi xử lý: {str(e)}'}), 500
    finally:
        # Xóa thư mục tạm sau khi xử lý
        shutil.rmtree(dataset_dir, ignore_errors=True)

@rvc_bp.route('/rvc/separate-vocals', methods=['POST'])
def separate_vocals():
    """API để tách giọng nói khỏi âm nhạc sử dụng UVR5"""
    if 'audio' not in request.files:
        return jsonify({'error': 'Không có file audio được gửi lên'}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'Tên file trống'}), 400
        
    # Lấy tham số
    vocal_type = request.form.get('vocal_type', 'both')
    
    # Lưu file tạm thời
    upload_folder = os.path.join(os.path.dirname(__file__), 'uploads')
    filename = secure_filename(audio_file.filename)
    file_path = os.path.join(upload_folder, filename)
    audio_file.save(file_path)
    
    try:
        # Gọi hàm tách giọng
        results = rvc.separate_vocals(file_path, vocal_type)
        
        if not results:
            return jsonify({
                'success': False,
                'error': 'Không thể tách giọng nói. Vui lòng kiểm tra file đầu vào.'
            }), 500
            
        # Chuẩn bị kết quả trả về
        response_data = {'success': True}
        
        # Thêm URL tải xuống cho mỗi file kết quả
        if 'vocals' in results:
            response_data['vocals_url'] = f"/api/download/{os.path.basename(results['vocals'])}"
            
        if 'instrumental' in results:
            response_data['instrumental_url'] = f"/api/download/{os.path.basename(results['instrumental'])}"
            
        # Thêm log thành công
        log = SystemLog(
            level='INFO',
            message=f"Tách giọng nói thành công: {filename}",
            component='rvc'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify(response_data)
    except Exception as e:
        logger.exception(f"Lỗi khi tách giọng nói: {str(e)}")
        
        # Thêm log lỗi
        log = SystemLog(
            level='ERROR',
            message=f"Lỗi khi tách giọng nói: {str(e)}",
            component='rvc'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'error': f'Lỗi xử lý: {str(e)}'}), 500
    finally:
        # Xóa file gốc sau khi xử lý
        if os.path.exists(file_path):
            os.remove(file_path)

@rvc_bp.route('/rvc/extract-f0', methods=['POST'])
def extract_f0():
    """API để trích xuất đường cong F0 từ file âm thanh"""
    if 'audio' not in request.files:
        return jsonify({'error': 'Không có file audio được gửi lên'}), 400
    
    audio_file = request.files['audio']
    if audio_file.filename == '':
        return jsonify({'error': 'Tên file trống'}), 400
        
    # Lấy tham số
    f0_method = request.form.get('f0_method', 'dio')
    
    # Lưu file tạm thời
    upload_folder = os.path.join(os.path.dirname(__file__), 'uploads')
    filename = secure_filename(audio_file.filename)
    file_path = os.path.join(upload_folder, filename)
    audio_file.save(file_path)
    
    try:
        # Gọi hàm trích xuất F0
        result_path = rvc.extract_f0(file_path, f0_method)
        
        if not result_path:
            return jsonify({
                'success': False,
                'error': 'Không thể trích xuất F0. Vui lòng kiểm tra file đầu vào.'
            }), 500
            
        # Chuẩn bị kết quả trả về
        response_data = {
            'success': True,
            'f0_url': f"/api/download/{os.path.basename(result_path)}"
        }
            
        # Thêm log thành công
        log = SystemLog(
            level='INFO',
            message=f"Trích xuất F0 thành công: {filename}",
            component='rvc'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify(response_data)
    except Exception as e:
        logger.exception(f"Lỗi khi trích xuất F0: {str(e)}")
        
        # Thêm log lỗi
        log = SystemLog(
            level='ERROR',
            message=f"Lỗi khi trích xuất F0: {str(e)}",
            component='rvc'
        )
        db.session.add(log)
        db.session.commit()
        
        return jsonify({'error': f'Lỗi xử lý: {str(e)}'}), 500
    finally:
        # Xóa file gốc sau khi xử lý
        if os.path.exists(file_path):
            os.remove(file_path)

def init_rvc(app):
    """Khởi tạo và đăng ký blueprint RVC"""
    app.register_blueprint(rvc_bp)
    return rvc 