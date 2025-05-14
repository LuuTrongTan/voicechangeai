import React, { useState, useEffect } from 'react';
import {
    Box,
    Grid,
    Paper,
    Typography,
    Button,
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableRow,
    CircularProgress,
    TextField,
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions
} from '@mui/material';
import { aiEngineerService } from '../../services/api';

const Dashboard = () => {
    const [models, setModels] = useState([]);
    const [trainings, setTrainings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [openUpload, setOpenUpload] = useState(false);
    const [uploadData, setUploadData] = useState({
        file: null,
        name: '',
        type: 'openvoice',
        description: ''
    });

    useEffect(() => {
        fetchData();
        // Polling cho trạng thái training
        const interval = setInterval(fetchData, 30000);
        return () => clearInterval(interval);
    }, []);

    const fetchData = async () => {
        try {
            const [modelsData, trainingsData] = await Promise.all([
                aiEngineerService.getModels(),
                aiEngineerService.getTrainings()
            ]);
            setModels(modelsData);
            setTrainings(trainingsData);
        } catch (error) {
            console.error('Lỗi khi tải dữ liệu:', error);
        } finally {
            setLoading(false);
        }
    };

    const handleUpload = async () => {
        try {
            await aiEngineerService.uploadModel(
                uploadData.file,
                uploadData.type,
                uploadData.name,
                uploadData.description
            );
            setOpenUpload(false);
            fetchData();
        } catch (error) {
            console.error('Lỗi khi upload model:', error);
        }
    };

    const handleStartTraining = async (modelName, modelType) => {
        try {
            await aiEngineerService.startTraining(modelName, modelType);
            fetchData();
        } catch (error) {
            console.error('Lỗi khi bắt đầu training:', error);
        }
    };

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
                AI Engineer Dashboard
            </Typography>

            {/* Upload Model Dialog */}
            <Dialog open={openUpload} onClose={() => setOpenUpload(false)}>
                <DialogTitle>Upload Model Mới</DialogTitle>
                <DialogContent>
                    <TextField
                        margin="dense"
                        label="Tên model"
                        fullWidth
                        value={uploadData.name}
                        onChange={(e) => setUploadData({ ...uploadData, name: e.target.value })}
                    />
                    <TextField
                        margin="dense"
                        label="Loại model"
                        fullWidth
                        select
                        SelectProps={{ native: true }}
                        value={uploadData.type}
                        onChange={(e) => setUploadData({ ...uploadData, type: e.target.value })}
                    >
                        <option value="openvoice">OpenVoice</option>
                        <option value="rvc">RVC</option>
                    </TextField>
                    <TextField
                        margin="dense"
                        label="Mô tả"
                        fullWidth
                        multiline
                        rows={4}
                        value={uploadData.description}
                        onChange={(e) => setUploadData({ ...uploadData, description: e.target.value })}
                    />
                    <input
                        type="file"
                        onChange={(e) => setUploadData({ ...uploadData, file: e.target.files[0] })}
                        style={{ marginTop: '1rem' }}
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={() => setOpenUpload(false)}>Hủy</Button>
                    <Button onClick={handleUpload} color="primary">
                        Upload
                    </Button>
                </DialogActions>
            </Dialog>

            {/* Models List */}
            <Paper sx={{ mb: 3, p: 2 }}>
                <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
                    <Typography variant="h6">
                        Danh sách Models
                    </Typography>
                    <Button
                        variant="contained"
                        color="primary"
                        onClick={() => setOpenUpload(true)}
                    >
                        Upload Model
                    </Button>
                </Box>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Tên</TableCell>
                            <TableCell>Loại</TableCell>
                            <TableCell>Trạng thái</TableCell>
                            <TableCell>Ngày tạo</TableCell>
                            <TableCell>Actions</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {models.map((model) => (
                            <TableRow key={model.id}>
                                <TableCell>{model.name}</TableCell>
                                <TableCell>{model.type}</TableCell>
                                <TableCell>{model.is_active ? 'Active' : 'Inactive'}</TableCell>
                                <TableCell>
                                    {new Date(model.created_at).toLocaleDateString()}
                                </TableCell>
                                <TableCell>
                                    <Button
                                        size="small"
                                        onClick={() => handleStartTraining(model.name, model.type)}
                                    >
                                        Train
                                    </Button>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Paper>

            {/* Training Status */}
            <Paper sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                    Trạng thái Training
                </Typography>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Model</TableCell>
                            <TableCell>Loại</TableCell>
                            <TableCell>Trạng thái</TableCell>
                            <TableCell>Bắt đầu</TableCell>
                            <TableCell>Hoàn thành</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {trainings.map((training) => (
                            <TableRow key={training.id}>
                                <TableCell>{training.model_name}</TableCell>
                                <TableCell>{training.model_type}</TableCell>
                                <TableCell>{training.status}</TableCell>
                                <TableCell>
                                    {new Date(training.started_at).toLocaleString()}
                                </TableCell>
                                <TableCell>
                                    {training.completed_at
                                        ? new Date(training.completed_at).toLocaleString()
                                        : '-'}
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </Paper>
        </Box>
    );
};

export default Dashboard; 