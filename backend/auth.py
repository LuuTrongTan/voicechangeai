from flask import request, jsonify, current_app, g
from functools import wraps
import jwt
from datetime import datetime, timedelta
from database import db, User

def generate_token(user_id, role):
    """Tạo token JWT cho người dùng"""
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.utcnow() + timedelta(days=1)  # Token hết hạn sau 1 ngày
    }
    return jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    """Xác thực token JWT"""
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None  # Token đã hết hạn
    except jwt.InvalidTokenError:
        return None  # Token không hợp lệ
    
def auth_middleware():
    """Middleware xác thực người dùng từ token"""
    token = None
    auth_header = request.headers.get('Authorization')
    
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
    
    if not token:
        g.user = None
        return
    
    payload = verify_token(token)
    if not payload:
        g.user = None
        return
    
    user = User.query.get(payload['user_id'])
    if not user or not user.is_active:
        g.user = None
        return
    
    g.user = user

def login_required(f):
    """Decorator yêu cầu đăng nhập"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_middleware()
        
        if g.user is None:
            return jsonify({'error': 'Vui lòng đăng nhập để tiếp tục'}), 401
        
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    """Decorator yêu cầu quyền admin"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_middleware()
        
        if g.user is None:
            return jsonify({'error': 'Vui lòng đăng nhập để tiếp tục'}), 401
        
        if g.user.role != 'admin':
            return jsonify({'error': 'Yêu cầu quyền admin'}), 403
        
        return f(*args, **kwargs)
    return decorated

def ai_engineer_required(f):
    """Decorator yêu cầu quyền AI Engineer"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_middleware()
        
        if g.user is None:
            return jsonify({'error': 'Vui lòng đăng nhập để tiếp tục'}), 401
        
        if g.user.role != 'ai_engineer' and g.user.role != 'admin':
            return jsonify({'error': 'Yêu cầu quyền AI Engineer'}), 403
        
        return f(*args, **kwargs)
    return decorated 