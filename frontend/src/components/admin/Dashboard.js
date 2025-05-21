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
    CircularProgress,
    Tabs,
    Tab,
    TextField,
    MenuItem,
    Button,
    FormControl,
    InputLabel,
    Select,
    Chip,
    LinearProgress,
    Accordion,
    AccordionSummary,
    AccordionDetails
} from '@mui/material';
import { Line } from 'react-chartjs-2';
import { Chart, registerables } from 'chart.js';
import { adminService } from '../../services/api';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import ErrorIcon from '@mui/icons-material/Error';
import MemoryIcon from '@mui/icons-material/Memory';
import StorageIcon from '@mui/icons-material/Storage';
import BugReportIcon from '@mui/icons-material/BugReport';

// Đăng ký tất cả các components của Chart.js
Chart.register(...registerables);

const Dashboard = () => {
    const [stats, setStats] = useState(null);
    const [users, setUsers] = useState([]);
    const [logs, setLogs] = useState([]);
    const [systemPerformance, setSystemPerformance] = useState(null);
    const [databaseInfo, setDatabaseInfo] = useState([]);
    const [errorAnalysis, setErrorAnalysis] = useState(null);
    const [rawLogs, setRawLogs] = useState([]);
    const [loading, setLoading] = useState(true);
    const [activeTab, setActiveTab] = useState(0);
    const [logFilters, setLogFilters] = useState({
        level: '',
        source: '',
        limit: 100
    });
    const [voiceChangerLogs, setVoiceChangerLogs] = useState([]);
    // Thêm state để lưu trữ lịch sử hiệu suất
    const [performanceHistory, setPerformanceHistory] = useState({
        cpu: [],
        memory: []
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                // Load dữ liệu tab đầu tiên
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

        // Thiết lập polling để cập nhật dữ liệu hiệu suất hệ thống
        const performanceInterval = setInterval(fetchSystemPerformance, 10000);
        return () => clearInterval(performanceInterval);
    }, []);

    // Fetch dữ liệu dựa trên tab đang active
    useEffect(() => {
        const loadTabData = async () => {
            setLoading(true);
            try {
                switch (activeTab) {
                    case 0: // Dashboard
                        const [statsData, usersData, logsData] = await Promise.all([
                            adminService.getStats(),
                            adminService.getUsers(),
                            adminService.getLogs()
                        ]);
                        setStats(statsData);
                        setUsers(usersData);
                        setLogs(logsData);
                        break;
                    case 1: // Logs
                        const logsResponse = await adminService.getLogs(logFilters);
                        setLogs(logsResponse);
                        const [appLogsResponse, voiceChangerLogsResponse] = await Promise.all([
                            adminService.getLogFile('app', 100),
                            adminService.getLogFile('voice_changer', 100)
                        ]);
                        setRawLogs(appLogsResponse.log_content);
                        setVoiceChangerLogs(voiceChangerLogsResponse.log_content);
                        break;
                    case 2: // APM
                        await fetchSystemPerformance();
                        break;
                    case 3: // Database
                        const dbInfo = await adminService.getDatabaseInfo();
                        setDatabaseInfo(dbInfo);
                        break;
                    case 4: // Error Analysis
                        const errorStats = await adminService.analyzeErrors();
                        setErrorAnalysis(errorStats);
                        break;
                    default:
                        break;
                }
            } catch (error) {
                console.error('Lỗi khi tải dữ liệu tab:', error);
            } finally {
                setLoading(false);
            }
        };

        loadTabData();
    }, [activeTab, logFilters]);

    const fetchSystemPerformance = async () => {
        try {
            const perfData = await adminService.getSystemPerformance();
            setSystemPerformance(perfData);
            // Lưu trữ lịch sử hiệu suất, giới hạn 20 điểm dữ liệu
            setPerformanceHistory(prevHistory => {
                const newCpuHistory = [...prevHistory.cpu, perfData.cpu.percent].slice(-20);
                const newMemoryHistory = [...prevHistory.memory, perfData.memory.percent].slice(-20);
                return {
                    cpu: newCpuHistory,
                    memory: newMemoryHistory
                };
            });
        } catch (error) {
            console.error('Lỗi khi tải dữ liệu hiệu suất:', error);
        }
    };

    const handleTabChange = (event, newValue) => {
        setActiveTab(newValue);
    };

    const applyLogFilters = () => {
        // Điều này sẽ trigger useEffect để tải lại logs với filter mới
        setLogFilters({ ...logFilters });
    };

    if (loading) {
        return (
            <Box display="flex" justifyContent="center" alignItems="center" minHeight="80vh">
                <CircularProgress />
                <Typography variant="h6" sx={{ ml: 2 }}>
                    Đang tải dữ liệu...
                </Typography>
            </Box>
        );
    }

    const renderTabs = () => {
        switch (activeTab) {
            case 0: // Dashboard
                return renderDashboard();
            case 1: // Logs
                return renderLogs();
            case 2: // APM
                return renderAPM();
            case 3: // Database
                return renderDatabase();
            case 4: // Error Analysis
                return renderErrorAnalysis();
            default:
                return renderDashboard();
        }
    };

    const renderDashboard = () => {
        return (
            <>
                <Grid container spacing={3} sx={{ mb: 3 }}>
                    <Grid item xs={12} sm={6} md={4}>
                        <Card>
                            <CardContent>
                                <Typography color="textSecondary" gutterBottom>
                                    Tổng người dùng
                                </Typography>
                                <Typography variant="h3" component="div">
                                    {stats?.user_count || 0}
                                </Typography>
                                <Typography variant="body2" sx={{ mt: 1 }}>
                                    Mới trong 30 ngày qua: {stats?.new_users || 0}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                    <Grid item xs={12} sm={6} md={4}>
                        <Card>
                            <CardContent>
                                <Typography color="textSecondary" gutterBottom>
                                    Tổng chuyển đổi giọng nói
                                </Typography>
                                <Typography variant="h3" component="div">
                                    {stats?.voice_conversions || 0}
                                </Typography>
                                <Typography variant="body2" sx={{ mt: 1 }}>
                                    OpenVoice: {stats?.openvoice_conversions || 0} | RVC: {stats?.rvc_conversions || 0}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                    <Grid item xs={12} sm={6} md={4}>
                        <Card>
                            <CardContent>
                                <Typography color="textSecondary" gutterBottom>
                                    Dịch vụ khác
                                </Typography>
                                <Typography variant="h3" component="div">
                                    {(stats?.tts_count || 0) + (stats?.uvr_count || 0)}
                                </Typography>
                                <Typography variant="body2" sx={{ mt: 1 }}>
                                    TTS: {stats?.tts_count || 0} | Tách giọng: {stats?.uvr_count || 0}
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                </Grid>

                <Grid container spacing={3} sx={{ mb: 3 }}>
                    <Grid item xs={12}>
                        <Paper sx={{ p: 2 }}>
                            <Typography variant="h6" gutterBottom>
                                Thống kê mô hình
                            </Typography>
                            <Grid container spacing={3}>
                                <Grid item xs={12} sm={6} md={3}>
                                    <Card sx={{ mb: 1 }}>
                                        <CardContent>
                                            <Typography color="textSecondary" gutterBottom>
                                                OpenVoice
                                            </Typography>
                                            <Typography variant="h5" component="div">
                                                {stats?.openvoice_models || 0}
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                </Grid>
                                <Grid item xs={12} sm={6} md={3}>
                                    <Card sx={{ mb: 1 }}>
                                        <CardContent>
                                            <Typography color="textSecondary" gutterBottom>
                                                RVC
                                            </Typography>
                                            <Typography variant="h5" component="div">
                                                {stats?.rvc_models || 0}
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                </Grid>
                                <Grid item xs={12} sm={6} md={3}>
                                    <Card sx={{ mb: 1 }}>
                                        <CardContent>
                                            <Typography color="textSecondary" gutterBottom>
                                                TTS
                                            </Typography>
                                            <Typography variant="h5" component="div">
                                                {stats?.tts_models || 0}
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                </Grid>
                                <Grid item xs={12} sm={6} md={3}>
                                    <Card sx={{ mb: 1 }}>
                                        <CardContent>
                                            <Typography color="textSecondary" gutterBottom>
                                                UVR
                                            </Typography>
                                            <Typography variant="h5" component="div">
                                                {stats?.uvr_models || 0}
                                            </Typography>
                                        </CardContent>
                                    </Card>
                                </Grid>
                            </Grid>
                        </Paper>
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
                                {Array.isArray(users) && users.length > 0 ? (
                                    users.slice(0, 5).map((user) => (
                                <TableRow key={user.id}>
                                    <TableCell>{user.id}</TableCell>
                                    <TableCell>{user.username}</TableCell>
                                    <TableCell>{user.email}</TableCell>
                                    <TableCell>{user.role}</TableCell>
                                    <TableCell>
                                                {user.created_at ? new Date(user.created_at).toLocaleDateString() : '-'}
                                            </TableCell>
                                        </TableRow>
                                    ))
                                ) : (
                                    <TableRow>
                                        <TableCell colSpan={5} align="center">
                                            Chưa có người dùng nào
                                    </TableCell>
                                </TableRow>
                                )}
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
                            {loading ? (
                                <TableRow>
                                    <TableCell colSpan={4} align="center">
                                        <CircularProgress size={24} sx={{ mr: 1 }} />
                                        Đang tải dữ liệu...
                                    </TableCell>
                                </TableRow>
                            ) : Array.isArray(logs) && logs.length > 0 ? (
                                logs.slice(0, 10).map((log, index) => (
                                    <TableRow key={index}>
                                        <TableCell>
                                            {log.timestamp ? new Date(log.timestamp).toLocaleString() : '-'}
                                        </TableCell>
                                        <TableCell>{log.level || '-'}</TableCell>
                                        <TableCell>{log.message || '-'}</TableCell>
                                        <TableCell>{log.source || '-'}</TableCell>
                                    </TableRow>
                                ))
                            ) : (
                                <TableRow>
                                    <TableCell colSpan={4} align="center">
                                        Không có dữ liệu
                                    </TableCell>
                                </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </Paper>
            </>
        );
    };

    const renderLogs = () => {
        return (
            <>
                <Paper sx={{ p: 2, mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                        Lọc logs
                    </Typography>
                    <Grid container spacing={2} alignItems="center">
                        <Grid item xs={12} sm={3}>
                            <FormControl fullWidth margin="normal">
                                <InputLabel>Level</InputLabel>
                                <Select
                                    value={logFilters.level}
                                    onChange={(e) => setLogFilters({ ...logFilters, level: e.target.value })}
                                    label="Level"
                                >
                                    <MenuItem value="">Tất cả</MenuItem>
                                    <MenuItem value="INFO">INFO</MenuItem>
                                    <MenuItem value="WARNING">WARNING</MenuItem>
                                    <MenuItem value="ERROR">ERROR</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item xs={12} sm={3}>
                            <FormControl fullWidth margin="normal">
                                <InputLabel>Source</InputLabel>
                                <Select
                                    value={logFilters.source}
                                    onChange={(e) => setLogFilters({ ...logFilters, source: e.target.value })}
                                    label="Source"
                                >
                                    <MenuItem value="">Tất cả</MenuItem>
                                    <MenuItem value="API">API</MenuItem>
                                    <MenuItem value="SYSTEM">SYSTEM</MenuItem>
                                    <MenuItem value="USER">USER</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item xs={12} sm={3}>
                            <FormControl fullWidth margin="normal">
                                <InputLabel>Số lượng</InputLabel>
                                <Select
                                    value={logFilters.limit}
                                    onChange={(e) => setLogFilters({ ...logFilters, limit: e.target.value })}
                                    label="Số lượng"
                                >
                                    <MenuItem value={10}>10</MenuItem>
                                    <MenuItem value={50}>50</MenuItem>
                                    <MenuItem value={100}>100</MenuItem>
                                    <MenuItem value={500}>500</MenuItem>
                                </Select>
                            </FormControl>
                        </Grid>
                        <Grid item xs={12} sm={3}>
                            <Button 
                                variant="contained" 
                                color="primary" 
                                onClick={applyLogFilters}
                                sx={{ mt: 2 }}
                            >
                                Áp dụng
                            </Button>
                        </Grid>
                    </Grid>
                </Paper>
                
                <Paper sx={{ p: 2, mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                        Logs hệ thống chi tiết
                    </Typography>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>ID</TableCell>
                                <TableCell>Thời gian</TableCell>
                                <TableCell>Level</TableCell>
                                <TableCell>Message</TableCell>
                                <TableCell>Source</TableCell>
                                <TableCell>User ID</TableCell>
                                <TableCell>Chi tiết</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            {loading ? (
                                <TableRow>
                                    <TableCell colSpan={7} align="center">
                                        <CircularProgress size={24} sx={{ mr: 1 }} />
                                        Đang tải dữ liệu...
                                    </TableCell>
                                </TableRow>
                            ) : Array.isArray(logs) && logs.length > 0 ? (
                                logs.map((log) => (
                                    <TableRow key={log.id || Math.random()}>
                                        <TableCell>{log.id || '-'}</TableCell>
                                        <TableCell>
                                            {log.timestamp ? new Date(log.timestamp).toLocaleString() : '-'}
                                        </TableCell>
                                        <TableCell>
                                            <Chip 
                                                label={log.level || 'UNKNOWN'} 
                                                color={
                                                    log.level === 'ERROR' ? 'error' : 
                                                    log.level === 'WARNING' ? 'warning' : 'default'
                                                }
                                                size="small"
                                            />
                                        </TableCell>
                                        <TableCell>{log.message || '-'}</TableCell>
                                        <TableCell>{log.source || '-'}</TableCell>
                                        <TableCell>{log.user_id || '-'}</TableCell>
                                        <TableCell>
                                            {log.details && Object.keys(log.details).length > 0 ? (
                                                <Accordion>
                                                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                                        <Typography>Chi tiết</Typography>
                                                    </AccordionSummary>
                                                    <AccordionDetails>
                                                        <pre>{JSON.stringify(log.details, null, 2)}</pre>
                                                    </AccordionDetails>
                                                </Accordion>
                                            ) : (
                                                '-'
                                            )}
                                        </TableCell>
                                    </TableRow>
                                ))
                            ) : (
                                <TableRow>
                                    <TableCell colSpan={7} align="center">
                                        Không có dữ liệu logs
                                    </TableCell>
                                </TableRow>
                            )}
                        </TableBody>
                    </Table>
                </Paper>
                
                {/* Hiển thị raw logs từ file */}
                <Grid container spacing={3}>
                    <Grid item xs={12} md={6}>
                        <Paper sx={{ p: 2, mb: 3 }}>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                                <Typography variant="h6" gutterBottom>
                                    Raw logs (app.log)
                                </Typography>
                                <Button 
                                    variant="outlined" 
                                    size="small"
                                    onClick={() => {
                                        adminService.getLogFile('app', 100).then(response => {
                                            setRawLogs(response.log_content);
                                        });
                                    }}
                                >
                                    Tải lại
                                </Button>
                            </Box>
                            {loading ? (
                                <Box display="flex" alignItems="center" p={2}>
                                    <CircularProgress size={24} sx={{ mr: 1 }} />
                                    <Typography>Đang tải dữ liệu...</Typography>
                                </Box>
                            ) : (
                                <Box 
                                    sx={{ 
                                        maxHeight: '400px', 
                                        overflow: 'auto', 
                                        bgcolor: 'background.paper',
                                        fontFamily: 'monospace',
                                        fontSize: '0.8rem',
                                        p: 2,
                                        borderRadius: 1,
                                        border: '1px solid',
                                        borderColor: 'divider'
                                    }}
                                >
                                    {Array.isArray(rawLogs) && rawLogs.length > 0 ? (
                                        rawLogs.map((line, index) => (
                                            <Box 
                                                component="div" 
                                                key={index}
                                                sx={{ 
                                                    whiteSpace: 'pre-wrap', 
                                                    mb: 0.5,
                                                    color: line.includes('ERROR') ? 'error.main' : 
                                                           line.includes('WARNING') ? 'warning.main' : 'text.primary'
                                                }}
                                            >
                                                {line}
                                            </Box>
                                        ))
                                    ) : (
                                        <Typography>Không có dữ liệu logs</Typography>
                                    )}
                                </Box>
                            )}
                        </Paper>
                    </Grid>
                    
                    <Grid item xs={12} md={6}>
                        <Paper sx={{ p: 2, mb: 3 }}>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                                <Typography variant="h6" gutterBottom>
                                    Raw logs (voice_changer.log)
                                </Typography>
                                <Button 
                                    variant="outlined" 
                                    size="small"
                                    onClick={() => {
                                        adminService.getLogFile('voice_changer', 100).then(response => {
                                            setVoiceChangerLogs(response.log_content);
                                        });
                                    }}
                                >
                                    Tải lại
                                </Button>
                            </Box>
                            {loading ? (
                                <Box display="flex" alignItems="center" p={2}>
                                    <CircularProgress size={24} sx={{ mr: 1 }} />
                                    <Typography>Đang tải dữ liệu...</Typography>
                                </Box>
                            ) : (
                                <Box 
                                    sx={{ 
                                        maxHeight: '400px', 
                                        overflow: 'auto', 
                                        bgcolor: 'background.paper',
                                        fontFamily: 'monospace',
                                        fontSize: '0.8rem',
                                        p: 2,
                                        borderRadius: 1,
                                        border: '1px solid',
                                        borderColor: 'divider'
                                    }}
                                >
                                    {Array.isArray(voiceChangerLogs) && voiceChangerLogs.length > 0 ? (
                                        voiceChangerLogs.map((line, index) => (
                                            <Box 
                                                component="div" 
                                                key={index}
                                                sx={{ 
                                                    whiteSpace: 'pre-wrap', 
                                                    mb: 0.5,
                                                    color: line.includes('ERROR') ? 'error.main' : 
                                                           line.includes('WARNING') ? 'warning.main' : 'text.primary'
                                                }}
                                            >
                                                {line}
                                            </Box>
                                        ))
                                    ) : (
                                        <Typography>Không có dữ liệu logs</Typography>
                                    )}
                                </Box>
                            )}
                        </Paper>
                    </Grid>
                </Grid>
            </>
        );
    };

    const renderAPM = () => {
        if (!systemPerformance) {
            return (
                <Box display="flex" justifyContent="center" flexDirection="column" alignItems="center" minHeight="60vh">
                    <CircularProgress sx={{ mb: 2 }} />
                    <Typography>Đang tải dữ liệu hiệu suất...</Typography>
                </Box>
            );
        }

        return (
            <>
                <Grid container spacing={3} sx={{ mb: 3 }}>
                    <Grid item xs={12} sm={6} md={3}>
                        <Card>
                            <CardContent>
                                <Typography color="textSecondary" gutterBottom>
                                    CPU Usage
                                </Typography>
                                <Typography variant="h5">
                                    {systemPerformance.cpu?.percent || 0}%
                                </Typography>
                                <LinearProgress 
                                    variant="determinate" 
                                    value={systemPerformance.cpu?.percent || 0} 
                                    sx={{ mt: 1 }}
                                />
                            </CardContent>
                        </Card>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                        <Card>
                            <CardContent>
                                <Typography color="textSecondary" gutterBottom>
                                    Memory Usage
                                </Typography>
                                <Typography variant="h5">
                                    {systemPerformance.memory?.percent || 0}%
                                </Typography>
                                <LinearProgress 
                                    variant="determinate" 
                                    value={systemPerformance.memory?.percent || 0} 
                                    sx={{ mt: 1 }}
                                />
                            </CardContent>
                        </Card>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                        <Card>
                            <CardContent>
                                <Typography color="textSecondary" gutterBottom>
                                    Disk Usage
                                </Typography>
                                <Typography variant="h5">
                                    {systemPerformance.disk?.percent || 0}%
                                </Typography>
                                <LinearProgress 
                                    variant="determinate" 
                                    value={systemPerformance.disk?.percent || 0} 
                                    sx={{ mt: 1 }}
                                />
                            </CardContent>
                        </Card>
                    </Grid>
                    <Grid item xs={12} sm={6} md={3}>
                        <Card>
                            <CardContent>
                                <Typography color="textSecondary" gutterBottom>
                                    Network (Received)
                                </Typography>
                                <Typography variant="h5">
                                    {systemPerformance.network?.bytes_recv ? 
                                        Math.round(systemPerformance.network.bytes_recv / (1024 * 1024)) : 0} MB
                                </Typography>
                            </CardContent>
                        </Card>
                    </Grid>
                </Grid>

                <Paper sx={{ p: 2, mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                        Biểu đồ hiệu suất
                    </Typography>
                    <Box sx={{ height: 300 }}>
                        <Line 
                            data={{
                                labels: Array(20).fill('').map((_, i) => `${i}`),
                                datasets: [
                                    {
                                        label: 'CPU Usage (%)',
                                        data: performanceHistory.cpu,
                                        borderColor: 'rgb(255, 99, 132)',
                                        backgroundColor: 'rgba(255, 99, 132, 0.5)',
                                    },
                                    {
                                        label: 'Memory Usage (%)',
                                        data: performanceHistory.memory,
                                        borderColor: 'rgb(53, 162, 235)',
                                        backgroundColor: 'rgba(53, 162, 235, 0.5)',
                                    },
                                ],
                            }}
                            options={{
                                responsive: true,
                                maintainAspectRatio: false,
                                scales: {
                                    y: {
                                        beginAtZero: true,
                                        max: 100
                                    }
                                }
                            }}
                        />
                    </Box>
                </Paper>

                <Paper sx={{ p: 2 }}>
                    <Typography variant="h6" gutterBottom>
                        Thông tin chi tiết về process
                    </Typography>
                    <Table>
                        <TableHead>
                            <TableRow>
                                <TableCell>Metric</TableCell>
                                <TableCell>Value</TableCell>
                            </TableRow>
                        </TableHead>
                        <TableBody>
                            <TableRow>
                                <TableCell>Process CPU</TableCell>
                                <TableCell>{systemPerformance.process?.cpu_percent || 0}%</TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Memory (RSS)</TableCell>
                                <TableCell>
                                    {systemPerformance.process?.memory_rss ?
                                        Math.round(systemPerformance.process.memory_rss / (1024 * 1024)) : 0} MB
                                </TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Memory (VMS)</TableCell>
                                <TableCell>
                                    {systemPerformance.process?.memory_vms ?
                                        Math.round(systemPerformance.process.memory_vms / (1024 * 1024)) : 0} MB
                                </TableCell>
                            </TableRow>
                            <TableRow>
                                <TableCell>Threads</TableCell>
                                <TableCell>{systemPerformance.process?.threads || 0}</TableCell>
                            </TableRow>
                        </TableBody>
                    </Table>
                </Paper>
            </>
        );
    };

    const renderDatabase = () => {
        return (
            <>
                <Paper sx={{ p: 2 }}>
                    <Typography variant="h6" gutterBottom>
                        Thông tin chi tiết về Database
                    </Typography>
                    
                    {Array.isArray(databaseInfo) && databaseInfo.length > 0 ? (
                        databaseInfo.map((table) => (
                            <Accordion key={table.name || Math.random()}>
                                <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                    <Typography>
                                        <strong>{table.name || 'Unknown'}</strong> - {table.row_count || 0} bản ghi
                                    </Typography>
                                </AccordionSummary>
                                <AccordionDetails>
                                    <Typography variant="body2" gutterBottom>
                                        Cấu trúc bảng:
                                    </Typography>
                                    {Array.isArray(table.columns) && table.columns.length > 0 ? (
                                        <Table size="small">
                                            <TableHead>
                                                <TableRow>
                                                    <TableCell>Column</TableCell>
                                                    <TableCell>Type</TableCell>
                                                </TableRow>
                                            </TableHead>
                                            <TableBody>
                                                {table.columns.map((column, index) => (
                                                    <TableRow key={index}>
                                                        <TableCell>{column.name || '-'}</TableCell>
                                                        <TableCell>{column.type || '-'}</TableCell>
                                                    </TableRow>
                                                ))}
                                            </TableBody>
                                        </Table>
                                    ) : (
                                        <Typography>Không có thông tin về cột</Typography>
                                    )}
                                </AccordionDetails>
                            </Accordion>
                        ))
                    ) : (
                        <Box sx={{ p: 2, textAlign: 'center' }}>
                            <Typography>Không có thông tin về database</Typography>
                        </Box>
                    )}
                </Paper>
            </>
        );
    };

    const renderErrorAnalysis = () => {
        if (!errorAnalysis) {
            return (
                <Box display="flex" justifyContent="center" flexDirection="column" alignItems="center" minHeight="60vh">
                    <CircularProgress sx={{ mb: 2 }} />
                    <Typography>Đang tải dữ liệu phân tích lỗi...</Typography>
                </Box>
            );
        }

        return (
            <>
                <Paper sx={{ p: 2, mb: 3 }}>
                    <Typography variant="h6" gutterBottom>
                        Thống kê lỗi
                    </Typography>
                    <Grid container spacing={3}>
                        <Grid item xs={12} sm={6}>
                            <Card>
                                <CardContent>
                                    <Typography color="textSecondary" gutterBottom>
                                        Tổng số lỗi
                                    </Typography>
                                    <Typography variant="h5">
                                        {errorAnalysis.total_errors || 0}
                                    </Typography>
                                </CardContent>
                            </Card>
                        </Grid>
                        <Grid item xs={12} sm={6}>
                            <Card>
                                <CardContent>
                                    <Typography color="textSecondary" gutterBottom>
                                        Nguồn lỗi
                                    </Typography>
                                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                                        {errorAnalysis.by_source && Object.entries(errorAnalysis.by_source).length > 0 ? (
                                            Object.entries(errorAnalysis.by_source).map(([source, count]) => (
                                                <Chip 
                                                    key={source} 
                                                    icon={<ErrorIcon />} 
                                                    label={`${source}: ${count}`} 
                                                    color="error" 
                                                />
                                            ))
                                        ) : (
                                            <Typography>Không có thông tin về nguồn lỗi</Typography>
                                        )}
                                    </Box>
                                </CardContent>
                            </Card>
                        </Grid>
                    </Grid>
                </Paper>

                {errorAnalysis.errors_by_source && Object.entries(errorAnalysis.errors_by_source).length > 0 ? (
                    Object.entries(errorAnalysis.errors_by_source).map(([source, errors]) => (
                        <Paper key={source} sx={{ p: 2, mb: 3 }}>
                            <Typography variant="h6" gutterBottom>
                                Lỗi từ nguồn: {source}
                            </Typography>
                            {Array.isArray(errors) && errors.length > 0 ? (
                                <Table>
                                    <TableHead>
                                        <TableRow>
                                            <TableCell>ID</TableCell>
                                            <TableCell>Thời gian</TableCell>
                                            <TableCell>Message</TableCell>
                                            <TableCell>Chi tiết</TableCell>
                                        </TableRow>
                                    </TableHead>
                                    <TableBody>
                                        {errors.map((error) => (
                                            <TableRow key={error.id || Math.random()}>
                                                <TableCell>{error.id || '-'}</TableCell>
                                                <TableCell>
                                                    {error.timestamp ? new Date(error.timestamp).toLocaleString() : '-'}
                                                </TableCell>
                                                <TableCell>{error.message || '-'}</TableCell>
                                                <TableCell>
                                                    {error.details && Object.keys(error.details).length > 0 ? (
                                                        <Accordion>
                                                            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                                                <Typography>Chi tiết</Typography>
                                                            </AccordionSummary>
                                                            <AccordionDetails>
                                                                <pre>{JSON.stringify(error.details, null, 2)}</pre>
                                                            </AccordionDetails>
                                                        </Accordion>
                                                    ) : (
                                                        '-'
                                                    )}
                                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
                            ) : (
                                <Typography align="center">Không có chi tiết lỗi nào</Typography>
                            )}
                        </Paper>
                    ))
                ) : (
                    <Paper sx={{ p: 2, mb: 3 }}>
                        <Typography align="center">Không có dữ liệu lỗi</Typography>
                    </Paper>
                )}
            </>
        );
    };

    return (
        <Box sx={{ p: 3 }}>
            <Typography variant="h4" gutterBottom>
                Bảng điều khiển Admin
            </Typography>

            <Paper sx={{ mb: 3 }}>
                <Tabs value={activeTab} onChange={handleTabChange} variant="scrollable" scrollButtons="auto">
                    <Tab label="Tổng quan" />
                    <Tab label="Logs" icon={<BugReportIcon />} iconPosition="start" />
                    <Tab label="Hiệu suất" icon={<MemoryIcon />} iconPosition="start" />
                    <Tab label="Database" icon={<StorageIcon />} iconPosition="start" />
                    <Tab label="Phân tích lỗi" icon={<ErrorIcon />} iconPosition="start" />
                </Tabs>
            </Paper>

            {loading && activeTab !== 0 ? (
                <Box display="flex" justifyContent="center" alignItems="center" minHeight="60vh">
                    <CircularProgress />
                </Box>
            ) : (
                renderTabs()
            )}
        </Box>
    );
};

export default Dashboard; 