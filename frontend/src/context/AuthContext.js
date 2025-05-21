import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

// Cấu hình API base URL
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

// Instance Axios
const api = axios.create({
    baseURL: API_URL,
    headers: {
        'Content-Type': 'application/json'
    }
});

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        // Kiểm tra token trong localStorage
        const token = localStorage.getItem('token');
        if (token) {
            api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            // Lấy thông tin user
            loadUser();
        } else {
            setLoading(false);
        }
    }, []);

    const loadUser = async () => {
        try {
            const response = await api.get('/api/auth/me');
            setUser(response.data);
            setError(null);
        } catch (err) {
            console.error('Lỗi khi lấy thông tin user:', err);
            localStorage.removeItem('token');
            delete api.defaults.headers.common['Authorization'];
            setUser(null);
            setError('Phiên đăng nhập hết hạn');
        } finally {
            setLoading(false);
        }
    };

    const register = async (username, email, password) => {
        try {
            const response = await api.post('/api/auth/register', {
                username,
                email,
                password
            });
            
            return response.data;
        } catch (err) {
            console.error('Lỗi đăng ký:', err);
            if (err.response && err.response.data) {
                setError(err.response.data.error || 'Đăng ký thất bại');
            } else {
                setError('Đăng ký thất bại. Vui lòng thử lại sau.');
            }
            throw err;
        }
    };

    const login = async (username, password) => {
        try {
            const response = await api.post('/api/auth/login', { username, password });
            const { token, user: userData } = response.data;
            
            localStorage.setItem('token', token);
            api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            setUser(userData);
            setError(null);
            
            return userData;
        } catch (err) {
            console.error('Lỗi đăng nhập:', err);
            if (err.response && err.response.data) {
                setError(err.response.data.error || 'Đăng nhập thất bại');
            } else {
                setError('Đăng nhập thất bại. Vui lòng thử lại sau.');
            }
            throw err;
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        delete api.defaults.headers.common['Authorization'];
        setUser(null);
        setError(null);
    };

    const changePassword = async (currentPassword, newPassword) => {
        try {
            const response = await api.post('/api/auth/change-password', {
                current_password: currentPassword,
                new_password: newPassword
            });
            
            return response.data;
        } catch (err) {
            console.error('Lỗi đổi mật khẩu:', err);
            if (err.response && err.response.data) {
                setError(err.response.data.error || 'Đổi mật khẩu thất bại');
            } else {
                setError('Đổi mật khẩu thất bại. Vui lòng thử lại sau.');
            }
            throw err;
        }
    };

    const value = {
        user,
        login,
        logout,
        register,
        changePassword,
        loading,
        error,
        isAuthenticated: !!user,
        isAdmin: user && user.role === 'admin',
        isAiEngineer: user && (user.role === 'ai_engineer' || user.role === 'admin')
    };

    return (
        <AuthContext.Provider value={value}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

// Thêm interceptor để xử lý phiên hết hạn
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            // Xóa token nếu server trả về 401 Unauthorized
            localStorage.removeItem('token');
            delete api.defaults.headers.common['Authorization'];
            // Reload trang để reset trạng thái
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

export default api; 