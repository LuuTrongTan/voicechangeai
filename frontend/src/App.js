import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CircularProgress, Box, Alert } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';

// Components
import Login from './components/auth/Login';
import AdminDashboard from './components/admin/Dashboard';
import AIEngineerDashboard from './components/ai_engineer/Dashboard';
import VoiceChangeOpenVoice from './components/OpenVoice/VoiceChangeOpenVoice';
import RVCTab from './components/RVC/RVCTab';
import Header from './components/layout/Header';
import NotFound from './components/layout/NotFound';
import Register from './components/auth/Register';

// Context
import { AuthProvider, useAuth } from './context/AuthContext';

// Tạo theme
const theme = createTheme({
    palette: {
        mode: 'light',
        primary: {
            main: '#1976d2',
        },
        secondary: {
            main: '#dc004e',
        },
    },
});

// PrivateRoute component để bảo vệ các route cần đăng nhập
const PrivateRoute = ({ children, requiredRole = null }) => {
    const { user, loading, isAuthenticated } = useAuth();
    
    if (loading) {
        return <div>Đang tải...</div>;
    }
    
    if (!isAuthenticated) {
        return <Navigate to="/login" />;
    }
    
    // Kiểm tra quyền nếu cần
    if (requiredRole) {
        if (requiredRole === 'admin' && user.role !== 'admin') {
            return <Navigate to="/" />;
        }
        if (requiredRole === 'ai_engineer' && user.role !== 'ai_engineer' && user.role !== 'admin') {
            return <Navigate to="/" />;
        }
    }
    
    return children;
};

const AppContent = () => {
    const { loading, error } = useAuth();

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
                <CircularProgress />
            </Box>
        );
    }

    if (error) {
        return (
            <Box m={2}>
                <Alert severity="error">{error}</Alert>
            </Box>
        );
    }

    return (
        <>
            <Header />
            <Routes>
                {/* Route đăng nhập, đăng ký */}
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                
                {/* Route cần xác thực */}
                <Route path="/dashboard" element={
                    <PrivateRoute>
                        <VoiceChangeOpenVoice />
                    </PrivateRoute>
                } />
                
                {/* Route cho Admin */}
                <Route path="/admin/*" element={
                    <PrivateRoute requiredRole="admin">
                        <AdminDashboard />
                    </PrivateRoute>
                } />
                
                {/* Route cho AI Engineer */}
                <Route path="/ai-engineer/*" element={
                    <PrivateRoute requiredRole="ai_engineer">
                        <AIEngineerDashboard />
                    </PrivateRoute>
                } />
                
                {/* Route cho RVC */}
                <Route path="/rvc" element={
                    <PrivateRoute>
                        <RVCTab />
                    </PrivateRoute>
                } />
                
                {/* Route mặc định */}
                <Route path="/" element={<Navigate to="/dashboard" />} />
                
                {/* 404 Route */}
                <Route path="*" element={<NotFound />} />
            </Routes>
        </>
    );
};

const App = () => {
    return (
        <ThemeProvider theme={theme}>
            <CssBaseline />
            <AuthProvider>
                <AppContent />
            </AuthProvider>
        </ThemeProvider>
    );
};

export default App; 