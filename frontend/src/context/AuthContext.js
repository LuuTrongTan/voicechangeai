import React, { createContext, useState, useContext, useEffect } from 'react';
import api from '../services/api';

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
            api.get('/api/user/profile')
                .then(response => {
                    setUser(response.data);
                    setError(null);
                })
                .catch((err) => {
                    console.error('Lỗi khi lấy thông tin user:', err);
                    localStorage.removeItem('token');
                    delete api.defaults.headers.common['Authorization'];
                    setError('Không thể lấy thông tin người dùng');
                })
                .finally(() => {
                    setLoading(false);
                });
        } else {
            setLoading(false);
        }
    }, []);

    const login = async (username, password) => {
        try {
            const response = await api.post('/api/auth/login', { username, password });
            const { token, user: userData } = response.data;
            localStorage.setItem('token', token);
            api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
            setUser(userData);
            setError(null);
        } catch (err) {
            console.error('Lỗi đăng nhập:', err);
            setError('Đăng nhập thất bại');
            throw err;
        }
    };

    const logout = () => {
        localStorage.removeItem('token');
        delete api.defaults.headers.common['Authorization'];
        setUser(null);
        setError(null);
    };

    const value = {
        user,
        login,
        logout,
        loading,
        error
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