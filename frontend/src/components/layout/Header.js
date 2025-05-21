import React, { useState } from 'react';
import { Link as RouterLink, useNavigate } from 'react-router-dom';
import {
    AppBar,
    Box,
    Toolbar,
    Typography,
    Button,
    IconButton,
    Menu,
    MenuItem,
    Link,
    Avatar
} from '@mui/material';
import { AccountCircle } from '@mui/icons-material';
import { useAuth } from '../../context/AuthContext';

const Header = () => {
    const { user, logout } = useAuth();
    const navigate = useNavigate();
    const [anchorEl, setAnchorEl] = useState(null);

    const handleMenu = (event) => {
        setAnchorEl(event.currentTarget);
    };

    const handleClose = () => {
        setAnchorEl(null);
    };

    const handleLogout = () => {
        logout();
        handleClose();
        navigate('/login');
    };

    return (
        <AppBar position="static">
            <Toolbar>
                <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
                    <Link
                        component={RouterLink}
                        to="/"
                        color="inherit"
                        underline="none"
                    >
                        
                    </Link>
                </Typography>

                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                    {/* Public Routes */}
                    <Button
                        color="inherit"
                        component={RouterLink}
                        to="/"
                    >
                        OpenVoice
                    </Button>
                    <Button
                        color="inherit"
                        component={RouterLink}
                        to="/rvc"
                    >
                        RVC
                    </Button>

                    {/* User Menu */}
                    {user ? (
                        <>
                            {/* Admin và AI Engineer Routes */}
                            {user.role === 'admin' && (
                                <Button
                                    color="inherit"
                                    component={RouterLink}
                                    to="/admin"
                                >
                                    Admin
                                </Button>
                            )}
                            {user.role === 'ai_engineer' && (
                                <Button
                                    color="inherit"
                                    component={RouterLink}
                                    to="/ai-engineer"
                                >
                                    AI Engineer
                                </Button>
                            )}

                            <IconButton
                                size="large"
                                onClick={handleMenu}
                                color="inherit"
                            >
                                {user.avatar ? (
                                    <Avatar
                                        src={user.avatar}
                                        sx={{ width: 32, height: 32 }}
                                    />
                                ) : (
                                    <AccountCircle />
                                )}
                            </IconButton>
                            <Menu
                                anchorEl={anchorEl}
                                open={Boolean(anchorEl)}
                                onClose={handleClose}
                            >
                                <MenuItem>
                                    <Typography variant="body2" color="textSecondary">
                                        Đăng nhập với {user.username}
                                    </Typography>
                                </MenuItem>
                                <MenuItem onClick={handleLogout}>
                                    Đăng xuất
                                </MenuItem>
                            </Menu>
                        </>
                    ) : (
                        <Button
                            color="inherit"
                            component={RouterLink}
                            to="/login"
                        >
                            Đăng nhập
                        </Button>
                    )}
                </Box>
            </Toolbar>
        </AppBar>
    );
};

export default Header; 