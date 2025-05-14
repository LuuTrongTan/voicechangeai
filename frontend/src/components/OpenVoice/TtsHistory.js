import React, { useState, useEffect } from 'react';
import {
  List, ListItem, ListItemIcon, ListItemText, ListItemSecondaryAction,
  IconButton, Divider, CircularProgress, Typography, Box, Alert
} from '@mui/material';
import TextsmsIcon from '@mui/icons-material/Textsms';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import DownloadIcon from '@mui/icons-material/Download';
import { VoiceAPI } from '../../services/api';

const TtsHistory = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const response = await VoiceAPI.getTtsHistory();
      setHistory(response.data);
      setError('');
    } catch (err) {
      console.error('Lỗi khi lấy lịch sử TTS:', err);
      setError('Không thể lấy lịch sử TTS');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const formatDate = (timestamp) => {
    return new Date(timestamp * 1000).toLocaleString('vi-VN');
  };

  // Truncate long text for display
  const truncateText = (text, maxLength = 50) => {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };
  
  // Ánh xạ tên ngôn ngữ để hiển thị
  const getLanguageDisplayName = (code) => {
    const languageMap = {
      'english': 'Tiếng Anh',
      'chinese': 'Tiếng Trung',
      'french': 'Tiếng Pháp',
      'spanish': 'Tiếng Tây Ban Nha',
      'japanese': 'Tiếng Nhật',
      'korean': 'Tiếng Hàn'
    };
    return languageMap[code] || code;
  };
  
  // Ánh xạ tên speaker để hiển thị dễ đọc
  const getSpeakerDisplayName = (speakerCode) => {
    const speakerMap = {
      'en-us': 'Tiếng Anh - Mỹ',
      'en-br': 'Tiếng Anh - Anh',
      'en-au': 'Tiếng Anh - Úc',
      'en-india': 'Tiếng Anh - Ấn Độ',
      'en-default': 'Tiếng Anh - Mặc định',
      'en-newest': 'Tiếng Anh - Mới nhất',
      'zh': 'Tiếng Trung',
      'jp': 'Tiếng Nhật',
      'kr': 'Tiếng Hàn',
      'fr': 'Tiếng Pháp',
      'es': 'Tiếng Tây Ban Nha'
    };
    return speakerMap[speakerCode] || speakerCode;
  };

  if (loading) return <Box sx={{ textAlign: 'center', py: 3 }}><CircularProgress /></Box>;
  
  if (error) return (
    <Alert severity="error" sx={{ mt: 2 }}>
      {error}
    </Alert>
  );
  
  if (history.length === 0) return (
    <Box sx={{ py: 2 }}>
      <Typography align="center" color="textSecondary">
        Chưa có lịch sử chuyển đổi TTS
      </Typography>
    </Box>
  );

  return (
    <List>
      {history.map((item, index) => (
        <React.Fragment key={index}>
          <ListItem>
            <ListItemIcon>
              <TextsmsIcon />
            </ListItemIcon>
            <ListItemText 
              primary={truncateText(item.text)}
              secondary={
                <React.Fragment>
                  <span>{formatDate(item.timestamp)}</span>
                  <br />
                  <span>Speaker: {getSpeakerDisplayName(item.speaker)}, Ngôn ngữ: {getLanguageDisplayName(item.language)}, Tốc độ: {item.speed}x</span>
                </React.Fragment>
              }
            />
            <ListItemSecondaryAction>
              <IconButton
                edge="end"
                onClick={() => VoiceAPI.playAudioFile(item.result_url)}
                title="Phát audio"
              >
                <VolumeUpIcon />
              </IconButton>
              <IconButton
                edge="end"
                onClick={() => VoiceAPI.downloadResult(item.result_url)}
                title="Tải xuống"
              >
                <DownloadIcon />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
          {index < history.length - 1 && <Divider />}
        </React.Fragment>
      ))}
    </List>
  );
};

export default TtsHistory; 