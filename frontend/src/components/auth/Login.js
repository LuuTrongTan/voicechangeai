import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { 
    Box, 
    TextField, 
    Button, 
    Typography, 
    Alert, 
    Paper, 
    Container,
    Divider,
    InputAdornment,
    IconButton
} from '@mui/material';
import { Visibility, VisibilityOff } from '@mui/icons-material';
import { useAuth } from '../../context/AuthContext';

const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [showPassword, setShowPassword] = useState(false);
    const navigate = useNavigate();
    const { login } = useAuth();

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        
        if (!username.trim()) {
            setError('Vui lòng nhập tên đăng nhập');
            return;
        }
        
        if (!password) {
            setError('Vui lòng nhập mật khẩu');
            return;
        }
        
        try {
            await login(username, password);
            navigate('/dashboard');
        } catch (err) {
            if (err.response && err.response.data && err.response.data.error) {
                setError(err.response.data.error);
            } else {
                setError('Đăng nhập thất bại. Vui lòng thử lại.');
            }
        }
    };

    const handleClickShowPassword = () => {
        setShowPassword(!showPassword);
    };

    return (
        <Container maxWidth="sm" sx={{ mt: 8, mb: 4 }}>
            <Paper elevation={3} sx={{ p: 4 }}>
                <Typography variant="h4" component="h1" align="center" gutterBottom>
                    Đăng nhập
                </Typography>
                
                {error && <Alert severity="error" sx={{ mb: 3 }}>{error}</Alert>}
                
                <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        label="Tên đăng nhập"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        autoFocus
                    />
                    <TextField
                        margin="normal"
                        required
                        fullWidth
                        label="Mật khẩu"
                        type={showPassword ? "text" : "password"}
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        InputProps={{
                            endAdornment: (
                                <InputAdornment position="end">
                                    <IconButton
                                        aria-label="toggle password visibility"
                                        onClick={handleClickShowPassword}
                                        edge="end"
                                    >
                                        {showPassword ? <VisibilityOff /> : <Visibility />}
                                    </IconButton>
                                </InputAdornment>
                            )
                        }}
                    />
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        size="large"
                        sx={{ mt: 3, mb: 2 }}
                    >
                        Đăng nhập
                    </Button>
                    
                    <Divider sx={{ my: 2 }} />
                    
                    <Box sx={{ textAlign: 'center' }}>
                        <Typography variant="body2">
                            Chưa có tài khoản?{' '}
                            <Link to="/register" style={{ textDecoration: 'none' }}>
                                Đăng ký ngay
                            </Link>
                        </Typography>
                    </Box>
                </Box>
            </Paper>
        </Container>
    );
};

export default Login; 