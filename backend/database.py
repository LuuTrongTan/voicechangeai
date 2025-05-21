from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), default='user')  # user, admin, ai_engineer
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.username}>'

class SystemLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    level = db.Column(db.String(10))  # INFO, WARNING, ERROR
    message = db.Column(db.Text)
    source = db.Column(db.String(50))  # API, SYSTEM, USER
    user_id = db.Column(db.Integer, nullable=True)  # Đã xóa ForeignKey tạm thời
    details = db.Column(db.Text)  # JSON string for additional details

    def __repr__(self):
        return f'<SystemLog {self.timestamp} {self.level}>'

def init_db(app):
    """Khởi tạo và cập nhật database"""
    with app.app_context():
        # Xóa tất cả các bảng
        db.drop_all()
        
        # Tạo lại tất cả các bảng với cấu trúc mới
        db.create_all()
        
        print("Đã khởi tạo lại database thành công!") 