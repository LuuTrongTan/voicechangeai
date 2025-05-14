import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CircularProgress, Box, Alert } from '@mui/material';
import CssBaseline from '@mui/material/CssBaseline';

// Components
import Login from './components/auth/Login';
import AdminDashboard from './components/admin/Dashboard';
import AIEngineerDashboard from './components/ai_engineer/Dashboard';
import OpenVoiceTab from './components/OpenVoice/TextToSpeechTab';
import VoiceChangeOpenVoice from './components/OpenVoice/VoiceChangeOpenVoice';
import RVCTab from './components/RVC/RVCTab';
import Header from './components/layout/Header';
import NotFound from './components/layout/NotFound';

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

// Protected Route component
const ProtectedRoute = ({ children, roles }) => {
    const { user, loading, error } = useAuth();

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

    if (!user) {
        return <Navigate to="/login" />;
    }

    if (roles && !roles.includes(user.role)) {
        return <Navigate to="/" />;
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
                <Route path="/login" element={<Login />} />
                
                {/* Admin Routes */}
                <Route
                    path="/admin"
                    element={
                        <ProtectedRoute roles={['admin']}>
                            <AdminDashboard />
                        </ProtectedRoute>
                    }
                />
                
                {/* AI Engineer Routes */}
                <Route
                    path="/ai-engineer"
                    element={
                        <ProtectedRoute roles={['ai_engineer']}>
                            <AIEngineerDashboard />
                        </ProtectedRoute>
                    }
                />
                
                {/* Public Routes */}
                <Route
                    path="/"
                    element={<VoiceChangeOpenVoice />}
                />
                <Route
                    path="/openvoice"
                    element={<OpenVoiceTab />}
                />
                <Route
                    path="/rvc"
                    element={<RVCTab />}
                />
                
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