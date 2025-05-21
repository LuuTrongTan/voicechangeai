from flask import Blueprint, jsonify, request
from database import db, User, SystemLog
from datetime import datetime
import json
import psutil
import sqlite3
import traceback
import logging
import os

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/stats', methods=['GET'])
def get_admin_stats():
    """Lấy thống kê tổng quan cho admin dashboard"""
    try:
        # Đếm số người dùng
        user_count = User.query.count()
        
        # Người dùng mới trong 30 ngày qua
        thirty_days_ago = datetime.utcnow().timestamp() - (30 * 24 * 60 * 60)
        new_users = User.query.filter(User.created_at >= datetime.fromtimestamp(thirty_days_ago)).count()
        
        # Thống kê chuyển đổi giọng nói từ file lịch sử
        try:
            # Đường dẫn tới các file lịch sử JSON
            rvc_conversion_history_path = os.path.join(os.path.dirname(__file__), 'results', 'rvc', 'voice_conversion', 'conversion_history.json')
            openvoice_conversion_history_path = os.path.join(os.path.dirname(__file__), 'results', 'openvoice', 'voice_conversion', 'conversion_history.json')
            tts_history_path = os.path.join(os.path.dirname(__file__), 'results', 'openvoice', 'tts', 'tts_history.json')
            uvr_history_path = os.path.join(os.path.dirname(__file__), 'results', 'rvc', 'uvr', 'uvr_history.json')
            
            # Đếm số lượng chuyển đổi RVC
            rvc_conversions = 0
            if os.path.exists(rvc_conversion_history_path):
                try:
                    with open(rvc_conversion_history_path, 'r', encoding='utf-8') as f:
                        rvc_history = json.load(f)
                        rvc_conversions = len(rvc_history)
                except Exception as e:
                    logging.error(f"Lỗi khi đọc lịch sử RVC: {str(e)}")
            
            # Đếm số lượng chuyển đổi OpenVoice
            openvoice_conversions = 0
            if os.path.exists(openvoice_conversion_history_path):
                try:
                    with open(openvoice_conversion_history_path, 'r', encoding='utf-8') as f:
                        openvoice_history = json.load(f)
                        openvoice_conversions = len(openvoice_history)
                except Exception as e:
                    logging.error(f"Lỗi khi đọc lịch sử OpenVoice: {str(e)}")
            
            # Đếm số lượng TTS
            tts_count = 0
            if os.path.exists(tts_history_path):
                try:
                    with open(tts_history_path, 'r', encoding='utf-8') as f:
                        tts_history = json.load(f)
                        tts_count = len(tts_history)
                except Exception as e:
                    logging.error(f"Lỗi khi đọc lịch sử TTS: {str(e)}")
            
            # Đếm số lượng UVR
            uvr_count = 0
            if os.path.exists(uvr_history_path):
                try:
                    with open(uvr_history_path, 'r', encoding='utf-8') as f:
                        uvr_history = json.load(f)
                        uvr_count = len(uvr_history)
                except Exception as e:
                    logging.error(f"Lỗi khi đọc lịch sử UVR: {str(e)}")
            
            # Đếm số lượng models từ thư mục models
            openvoice_voice_models_dir = os.path.join(os.path.dirname(__file__), '..', 'ai', 'openvoice', 'sample_voices')
            rvc_models_dir = os.path.join(os.path.dirname(__file__), '..', 'ai', 'rvc', 'assets', 'weights')
            tts_models_dir = os.path.join(os.path.dirname(__file__), '..', 'ai', 'openvoice', 'checkpoints_v2', 'base_speakers', 'ses')
            uvr_models_dir = os.path.join(os.path.dirname(__file__), '..', 'ai', 'rvc', 'assets', 'uvr5_weights')
            
            openvoice_models = 0
            if os.path.exists(openvoice_voice_models_dir):
                openvoice_models = len([d for d in os.listdir(openvoice_voice_models_dir) 
                                      if os.path.isdir(os.path.join(openvoice_voice_models_dir, d))])
            
            rvc_models = 0
            if os.path.exists(rvc_models_dir):
                rvc_models = len([f for f in os.listdir(rvc_models_dir) 
                                if f.endswith('.pth')])
            
            tts_models = 0
            if os.path.exists(tts_models_dir):
                tts_models = len([f for f in os.listdir(tts_models_dir) 
                                if f.endswith('.pth')])
            
            uvr_models = 0
            if os.path.exists(uvr_models_dir):
                uvr_models = len([f for f in os.listdir(uvr_models_dir) 
                                if f.endswith('.pth') and not os.path.isdir(os.path.join(uvr_models_dir, f))])
            
        except Exception as e:
            logging.error(f"Lỗi khi đọc dữ liệu thống kê từ file: {str(e)}")
            openvoice_conversions = 0
            rvc_conversions = 0
            tts_count = 0
            uvr_count = 0
            openvoice_models = 0
            rvc_models = 0
            tts_models = 0
            uvr_models = 0
        
        # Tổng hợp thống kê
        voice_conversions = openvoice_conversions + rvc_conversions
        
        stats = {
            'user_count': user_count,
            'new_users': new_users,
            'voice_conversions': voice_conversions,
            'openvoice_conversions': openvoice_conversions,
            'rvc_conversions': rvc_conversions,
            'tts_count': tts_count,
            'uvr_count': uvr_count,
            'openvoice_models': openvoice_models,
            'rvc_models': rvc_models,
            'tts_models': tts_models,
            'uvr_models': uvr_models
        }
        
        return jsonify(stats)
    
    except Exception as e:
        logging.error(f"Lỗi khi lấy thống kê admin: {str(e)}")
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users', methods=['GET'])
def get_users():
    """Lấy danh sách người dùng"""
    try:
        users = User.query.all()
        users_data = []
        
        for user in users:
            users_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'last_login': user.last_login.isoformat() if user.last_login else None,
                'is_active': user.is_active
            })
        
        return jsonify(users_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/logs', methods=['GET'])
def get_system_logs():
    """Lấy logs hệ thống"""
    try:
        # Tham số filter từ request
        level = request.args.get('level')
        source = request.args.get('source')
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        limit = int(request.args.get('limit', 100))
        
        # Query cơ bản
        query = SystemLog.query
        
        # Thêm các filter nếu có
        if level:
            query = query.filter(SystemLog.level == level)
        if source:
            query = query.filter(SystemLog.source == source)
        if start_date:
            start_datetime = datetime.fromisoformat(start_date)
            query = query.filter(SystemLog.timestamp >= start_datetime)
        if end_date:
            end_datetime = datetime.fromisoformat(end_date)
            query = query.filter(SystemLog.timestamp <= end_datetime)
        
        # Sắp xếp theo thời gian và giới hạn số lượng
        logs = query.order_by(SystemLog.timestamp.desc()).limit(limit).all()
        logs_data = []
        
        for log in logs:
            logs_data.append({
                'id': log.id,
                'timestamp': log.timestamp.isoformat(),
                'level': log.level,
                'message': log.message,
                'source': log.source,
                'user_id': log.user_id,
                'details': json.loads(log.details) if log.details else {}
            })
        
        return jsonify(logs_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/system-performance', methods=['GET'])
def get_system_performance():
    """Lấy thông tin về hiệu suất hệ thống (APM)"""
    try:
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        cpu_count = psutil.cpu_count()
        
        # Memory usage
        memory = psutil.virtual_memory()
        
        # Disk usage
        disk = psutil.disk_usage('/')
        
        # Network stats
        net_io = psutil.net_io_counters()
        
        # Process info
        process = psutil.Process(os.getpid())
        process_memory = process.memory_info()
        
        performance_data = {
            'cpu': {
                'percent': cpu_percent,
                'count': cpu_count
            },
            'memory': {
                'total': memory.total,
                'available': memory.available,
                'percent': memory.percent,
                'used': memory.used
            },
            'disk': {
                'total': disk.total,
                'used': disk.used,
                'free': disk.free,
                'percent': disk.percent
            },
            'network': {
                'bytes_sent': net_io.bytes_sent,
                'bytes_recv': net_io.bytes_recv,
                'packets_sent': net_io.packets_sent,
                'packets_recv': net_io.packets_recv
            },
            'process': {
                'memory_rss': process_memory.rss,
                'memory_vms': process_memory.vms,
                'threads': process.num_threads(),
                'cpu_percent': process.cpu_percent(interval=1)
            }
        }
        
        return jsonify(performance_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/database-info', methods=['GET'])
def get_database_info():
    """Lấy thông tin về database"""
    try:
        # Lấy thông tin về các bảng trong database
        tables_info = []
        
        # Kết nối trực tiếp đến SQLite database
        conn = sqlite3.connect('instance/database.db')
        cursor = conn.cursor()
        
        # Lấy danh sách các bảng
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        for table in tables:
            table_name = table[0]
            
            # Đếm số bản ghi trong bảng
            cursor.execute(f"SELECT COUNT(*) FROM {table_name};")
            row_count = cursor.fetchone()[0]
            
            # Lấy thông tin về cấu trúc bảng
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = cursor.fetchall()
            columns_info = [{'name': col[1], 'type': col[2]} for col in columns]
            
            tables_info.append({
                'name': table_name,
                'row_count': row_count,
                'columns': columns_info
            })
        
        conn.close()
        
        return jsonify(tables_info)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/error-analysis', methods=['GET'])
def analyze_errors():
    """Phân tích lỗi từ logs"""
    try:
        # Lấy các log ERROR
        error_logs = SystemLog.query.filter(SystemLog.level == 'ERROR').order_by(SystemLog.timestamp.desc()).limit(100).all()
        
        # Nhóm lỗi theo source
        errors_by_source = {}
        
        for log in error_logs:
            source = log.source
            if source not in errors_by_source:
                errors_by_source[source] = []
            
            errors_by_source[source].append({
                'id': log.id,
                'timestamp': log.timestamp.isoformat(),
                'message': log.message,
                'details': json.loads(log.details) if log.details else {}
            })
        
        # Thống kê số lỗi theo source
        error_stats = {
            'total_errors': len(error_logs),
            'by_source': {source: len(errors) for source, errors in errors_by_source.items()},
            'errors_by_source': errors_by_source
        }
        
        return jsonify(error_stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/log-file', methods=['GET'])
def get_log_file():
    """Lấy nội dung file log trực tiếp"""
    try:
        log_type = request.args.get('type', 'app')
        lines = int(request.args.get('lines', 100))
        
        log_file_path = 'app.log'
        if log_type == 'voice_changer':
            log_file_path = 'voice_changer.log'
        
        # Đọc n dòng cuối của file log
        with open(log_file_path, 'r', encoding='utf-8') as file:
            log_lines = file.readlines()[-lines:]
        
        return jsonify({'log_content': log_lines})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500 