import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { 
    Box, 
    TextField, 
    Button, 
    Typography, 
    Alert,
    Paper,
    Grid,
    Container,
    Divider
} from '@mui/material';
import { useAuth } from '../../context/AuthContext';

const Register = () => {
    const [formData, setFormData] = useState({
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
    });
    const [errors, setErrors] = useState({});
    const [serverError, setServerError] = useState('');
    const navigate = useNavigate();
    const { register } = useAuth();

    const handleChange = (e) => {
        const { name, value } = e.target;
        setFormData({
            ...formData,
            [name]: value
        });
        
        // Xóa lỗi khi người dùng nhập lại
        if (errors[name]) {
            setErrors({
                ...errors,
                [name]: ''
            });
        }
    };

    const validateForm = () => {
        const newErrors = {};
        
        // Kiểm tra tên đăng nhập
        if (!formData.username.trim()) {
            newErrors.username = 'Vui lòng nhập tên đăng nhập';
        } else if (formData.username.length < 3) {
            newErrors.username = 'Tên đăng nhập phải có ít nhất 3 ký tự';
        }
        
        // Kiểm tra email
        const emailRegex = /^[\w\.-]+@[\w\.-]+\.\w+$/;
        if (!formData.email.trim()) {
            newErrors.email = 'Vui lòng nhập email';
        } else if (!emailRegex.test(formData.email)) {
            newErrors.email = 'Email không hợp lệ';
        }
        
        // Kiểm tra mật khẩu
        if (!formData.password) {
            newErrors.password = 'Vui lòng nhập mật khẩu';
        } else if (formData.password.length < 6) {
            newErrors.password = 'Mật khẩu phải có ít nhất 6 ký tự';
        }
        
        // Kiểm tra xác nhận mật khẩu
        if (!formData.confirmPassword) {
            newErrors.confirmPassword = 'Vui lòng xác nhận mật khẩu';
        } else if (formData.password !== formData.confirmPassword) {
            newErrors.confirmPassword = 'Mật khẩu xác nhận không khớp';
        }
        
        setErrors(newErrors);
        return Object.keys(newErrors).length === 0;
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setServerError('');
        
        if (validateForm()) {
            try {
                await register(formData.username, formData.email, formData.password);
                navigate('/login');
            } catch (err) {
                if (err.response && err.response.data && err.response.data.error) {
                    setServerError(err.response.data.error);
                } else {
                    setServerError('Đăng ký thất bại. Vui lòng thử lại sau.');
                }
            }
        }
    };

    return (
        <Container maxWidth="sm" sx={{ mt: 8, mb: 4 }}>
            <Paper elevation={3} sx={{ p: 4 }}>
                <Typography variant="h4" component="h1" align="center" gutterBottom>
                    Đăng ký tài khoản
                </Typography>
                
                {serverError && (
                    <Alert severity="error" sx={{ mb: 3 }}>
                        {serverError}
                    </Alert>
                )}
                
                <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
                    <Grid container spacing={2}>
                        <Grid item xs={12}>
                            <TextField
                                name="username"
                                label="Tên đăng nhập"
                                fullWidth
                                value={formData.username}
                                onChange={handleChange}
                                error={!!errors.username}
                                helperText={errors.username}
                                required
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                name="email"
                                label="Email"
                                fullWidth
                                type="email"
                                value={formData.email}
                                onChange={handleChange}
                                error={!!errors.email}
                                helperText={errors.email}
                                required
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                name="password"
                                label="Mật khẩu"
                                fullWidth
                                type="password"
                                value={formData.password}
                                onChange={handleChange}
                                error={!!errors.password}
                                helperText={errors.password}
                                required
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField
                                name="confirmPassword"
                                label="Xác nhận mật khẩu"
                                fullWidth
                                type="password"
                                value={formData.confirmPassword}
                                onChange={handleChange}
                                error={!!errors.confirmPassword}
                                helperText={errors.confirmPassword}
                                required
                            />
                        </Grid>
                    </Grid>
                    
                    <Button
                        type="submit"
                        fullWidth
                        variant="contained"
                        size="large"
                        sx={{ mt: 3, mb: 2 }}
                    >
                        Đăng ký
                    </Button>
                    
                    <Divider sx={{ my: 2 }} />
                    
                    <Box sx={{ textAlign: 'center' }}>
                        <Typography variant="body2">
                            Đã có tài khoản?{' '}
                            <Link to="/login" style={{ textDecoration: 'none' }}>
                                Đăng nhập ngay
                            </Link>
                        </Typography>
                    </Box>
                </Box>
            </Paper>
        </Container>
    );
};

export default Register; 