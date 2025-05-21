from flask import Blueprint, request, jsonify, g
from database import db, User, SystemLog
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import json
from auth import generate_token, login_required
import re

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Đăng ký người dùng mới"""
    try:
        data = request.json
        
        # Kiểm tra các trường bắt buộc
        required_fields = ['username', 'email', 'password']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({'error': f'Thiếu thông tin {field}'}), 400
        
        username = data['username']
        email = data['email']
        password = data['password']
        
        # Kiểm tra định dạng email
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            return jsonify({'error': 'Email không hợp lệ'}), 400
        
        # Kiểm tra độ dài mật khẩu
        if len(password) < 6:
            return jsonify({'error': 'Mật khẩu phải có ít nhất 6 ký tự'}), 400
        
        # Kiểm tra username đã tồn tại chưa
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Tên đăng nhập đã tồn tại'}), 400
        
        # Kiểm tra email đã tồn tại chưa
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email đã được đăng ký'}), 400
        
        # Mặc định role là 'user'
        role = 'user'
        # Nếu là người dùng đầu tiên, gán quyền admin
        if User.query.count() == 0:
            role = 'admin'
        
        # Tạo người dùng mới
        hashed_password = generate_password_hash(password)
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            role=role,
            created_at=datetime.utcnow(),
            is_active=True
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        # Ghi log hệ thống
        log_entry = SystemLog(
            level='INFO',
            message=f'Người dùng mới đăng ký: {username}',
            source='AUTH',
            user_id=new_user.id,
            details=json.dumps({
                'username': username,
                'email': email,
                'role': role
            })
        )
        db.session.add(log_entry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Đăng ký thành công',
            'user': {
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'role': new_user.role
            }
        })
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """Đăng nhập và tạo token"""
    try:
        data = request.json
        
        # Kiểm tra các trường bắt buộc
        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'error': 'Thiếu thông tin đăng nhập'}), 400
        
        username = data['username']
        password = data['password']
        
        # Tìm người dùng
        user = User.query.filter_by(username=username).first()
        
        # Kiểm tra người dùng tồn tại và mật khẩu
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Thông tin đăng nhập không chính xác'}), 401
        
        # Kiểm tra tài khoản có bị khóa không
        if not user.is_active:
            return jsonify({'error': 'Tài khoản đã bị khóa'}), 403
        
        # Cập nhật thời gian đăng nhập gần nhất
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Tạo token
        token = generate_token(user.id, user.role)
        
        # Ghi log đăng nhập
        log_entry = SystemLog(
            level='INFO',
            message=f'Đăng nhập thành công: {username}',
            source='AUTH',
            user_id=user.id,
            details=json.dumps({
                'username': username,
                'role': user.role
            })
        )
        db.session.add(log_entry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'token': token,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/me', methods=['GET'])
@login_required
def get_current_user():
    """Lấy thông tin người dùng hiện tại từ token"""
    try:
        user = g.user
        
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'role': user.role,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'is_active': user.is_active
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/change-password', methods=['POST'])
@login_required
def change_password():
    """Thay đổi mật khẩu"""
    try:
        data = request.json
        
        # Kiểm tra các trường bắt buộc
        if not data or 'current_password' not in data or 'new_password' not in data:
            return jsonify({'error': 'Thiếu thông tin mật khẩu'}), 400
        
        current_password = data['current_password']
        new_password = data['new_password']
        
        # Kiểm tra độ dài mật khẩu mới
        if len(new_password) < 6:
            return jsonify({'error': 'Mật khẩu mới phải có ít nhất 6 ký tự'}), 400
        
        # Lấy người dùng hiện tại
        user = g.user
        
        # Kiểm tra mật khẩu hiện tại
        if not check_password_hash(user.password_hash, current_password):
            return jsonify({'error': 'Mật khẩu hiện tại không chính xác'}), 401
        
        # Cập nhật mật khẩu
        user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        # Ghi log thay đổi mật khẩu
        log_entry = SystemLog(
            level='INFO',
            message=f'Thay đổi mật khẩu: {user.username}',
            source='AUTH',
            user_id=user.id,
            details=json.dumps({
                'username': user.username
            })
        )
        db.session.add(log_entry)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Thay đổi mật khẩu thành công'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500 