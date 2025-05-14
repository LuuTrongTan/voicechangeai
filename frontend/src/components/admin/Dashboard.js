import React, { useState, useEffect } from 'react';
import {
    Box,
    Grid,
    Paper,
    Typography,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableRow,
    Card,
    CardContent,
    CircularProgress
} from '@mui/material';
import { adminService } from '../../services/api';

const Dashboard = () => {
    const [stats, setStats] = useState(null);
    const [users, setUsers] = useState([]);
    const [logs, setLogs] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const [statsData, usersData, logsData] = await Promise.all([
                    adminService.getStats(),
                    adminService.getUsers(),
                    adminService.getLogs()
                ]);
                setStats(statsData);
                setUsers(usersData);
                setLogs(logsData);
            } catch (error) {
                console.error('Lỗi khi tải dữ liệu:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, []);

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
                <CircularProgress />
            </Box>
        );
    }

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>
                Bảng điều khiển Admin
            </Typography>

            {/* Thống kê tổng quan */}
            <Grid container spacing={3} sx={{ mb: 3 }}>
                <Grid item xs={12} sm={6} md={3}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                Tổng số người dùng
                            </Typography>
                            <Typography variant="h5">
                                {users.length}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                Chuyển đổi giọng nói
                            </Typography>
                            <Typography variant="h5">
                                {stats?.voice_conversions || 0}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                Text-to-Speech
                            </Typography>
                            <Typography variant="h5">
                                {stats?.tts_count || 0}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
                <Grid item xs={12} sm={6} md={3}>
                    <Card>
                        <CardContent>
                            <Typography color="textSecondary" gutterBottom>
                                Người dùng mới
                            </Typography>
                            <Typography variant="h5">
                                {stats?.new_users || 0}
                            </Typography>
                        </CardContent>
                    </Card>
                </Grid>
            </Grid>

            {/* Danh sách người dùng */}
            <Paper sx={{ mb: 3, p: 2 }}>
                <Typography variant="h6" gutterBottom>
                    Người dùng gần đây
                </Typography>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>ID</TableCell>
                            <TableCell>Tên đăng nhập</TableCell>
                            <TableCell>Email</TableCell>
                            <TableCell>Vai trò</TableCell>
                            <TableCell>Ngày tạo</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {users.slice(0, 5).map((user) => (
                            <TableRow key={user.id}>
                                <TableCell>{user.id}</TableCell>
                                <TableCell>{user.username}</TableCell>
                                <TableCell>{user.email}</TableCell>
                                <TableCell>{user.role}</TableCell>
                                <TableCell>
                                    {new Date(user.created_at).toLocaleDateString()}
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Paper>

            {/* System Logs */}
            <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                    Logs hệ thống
                </Typography>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Thời gian</TableCell>
                            <TableCell>Level</TableCell>
                            <TableCell>Message</TableCell>
                            <TableCell>Source</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {logs.slice(0, 10).map((log, index) => (
                            <TableRow key={index}>
                                <TableCell>
                                    {new Date(log.timestamp).toLocaleString()}
                                </TableCell>
                                <TableCell>{log.level}</TableCell>
                                <TableCell>{log.message}</TableCell>
                                <TableCell>{log.source}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Paper>
        </Box>
    );
};

export default Dashboard; 