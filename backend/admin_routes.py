from flask import Blueprint, jsonify, request
from database import db, User, SystemLog
from datetime import datetime

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
        
        # Đếm số chuyển đổi giọng nói
        voice_conversions = 0
        
        # Đếm số lần sử dụng TTS
        tts_count = 0
        
        stats = {
            'user_count': user_count,
            'new_users': new_users,
            'voice_conversions': voice_conversions,
            'tts_count': tts_count
        }
        
        return jsonify(stats)
    
    except Exception as e:
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
        # Lấy 100 log gần nhất
        logs = SystemLog.query.order_by(SystemLog.timestamp.desc()).limit(100).all()
        logs_data = []
        
        for log in logs:
            logs_data.append({
                'id': log.id,
                'timestamp': log.timestamp.isoformat(),
                'level': log.level,
                'message': log.message,
                'source': log.source,
                'user_id': log.user_id,
                'details': log.details
            })
        
        return jsonify(logs_data)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500 