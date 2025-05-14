import React, { useState, useEffect, useRef } from 'react';
import {
  Typography, Box, Button, Paper, 
  Grid, FormControl, InputLabel, Select, MenuItem,
  CircularProgress, Alert, IconButton, Slider,
  TextField, Divider, Chip, Tooltip
} from '@mui/material';
import PlayCircleOutlineIcon from '@mui/icons-material/PlayCircleOutline';
import StopIcon from '@mui/icons-material/Stop';
import DownloadIcon from '@mui/icons-material/Download';
import InfoIcon from '@mui/icons-material/Info';
import { VoiceAPI } from '../../services/api';
import TtsHistory from './TtsHistory';

const TextToSpeechTab = () => {
  // State variables
  const [text, setText] = useState('');
  const [availableSpeakers, setAvailableSpeakers] = useState([]);
  const [selectedSpeaker, setSelectedSpeaker] = useState('');
  const [language, setLanguage] = useState('english');
  const [speed, setSpeed] = useState(1.0);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [isPlaying, setIsPlaying] = useState(false);
  const [showHistory, setShowHistory] = useState(false);
  const [showInfo, setShowInfo] = useState(false);
  
  // Tham chiếu đến đối tượng Audio
  const audioRef = useRef(null);

  // Tải danh sách speakers từ backend
  useEffect(() => {
    const fetchSpeakers = async () => {
      try {
        const response = await VoiceAPI.getTtsSpeakers();
        if (response.data.speakers && response.data.speakers.length > 0) {
          setAvailableSpeakers(response.data.speakers);
          setSelectedSpeaker(response.data.speakers[0]);
        } else {
          setError('Không tìm thấy speakers nào');
          setShowInfo(true);
        }
      } catch (err) {
        console.error('Lỗi khi tải danh sách speakers:', err);
        setError('Không thể kết nối với máy chủ. Vui lòng thử lại sau.');
        setShowInfo(true);
      }
    };

    fetchSpeakers();
  }, []);

  // Xử lý khi người dùng thay đổi text
  const handleTextChange = (event) => {
    setText(event.target.value);
  };

  // Xử lý khi người dùng thay đổi speaker
  const handleSpeakerChange = (event) => {
    setSelectedSpeaker(event.target.value);
    
    // Tự động chọn ngôn ngữ dựa trên speaker
    const speaker = event.target.value;
    if (speaker.startsWith('en-')) {
      setLanguage('english');
    } else if (speaker === 'zh') {
      setLanguage('chinese');
    } else if (speaker === 'fr') {
      setLanguage('french');
    } else if (speaker === 'es') {
      setLanguage('spanish');
    } else if (speaker === 'jp') {
      setLanguage('japanese');
    } else if (speaker === 'kr') {
      setLanguage('korean');
    }
  };

  // Xử lý khi người dùng thay đổi ngôn ngữ
  const handleLanguageChange = (event) => {
    setLanguage(event.target.value);
  };

  // Xử lý khi người dùng thay đổi tốc độ
  const handleSpeedChange = (event, newValue) => {
    setSpeed(newValue);
  };

  // Xử lý khi người dùng gửi yêu cầu tạo giọng nói
  const handleGenerateTts = async () => {
    if (!text) {
      setError('Vui lòng nhập văn bản');
      return;
    }

    if (!selectedSpeaker) {
      setError('Vui lòng chọn speaker');
      return;
    }

    setIsLoading(true);
    setResult(null);
    setError('');

    try {
      const response = await VoiceAPI.generateTts({
        text,
        speaker: selectedSpeaker,
        language,
        speed
      });

      if (response.data.success) {
        setResult(response.data);
        setError('');
      } else {
        setError(response.data.error || 'Lỗi không xác định');
        if (response.data.error && response.data.error.includes('MeloTTS')) {
          setShowInfo(true);
        }
      }
    } catch (err) {
      console.error('Lỗi khi tạo giọng nói:', err);
      setError(err.response?.data?.error || 'Không thể kết nối với máy chủ');
      if (err.response?.data?.error && err.response.data.error.includes('MeloTTS')) {
        setShowInfo(true);
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Xử lý phát audio
  const handlePlayAudio = () => {
    if (!result) return;

    if (isPlaying) {
      audioRef.current.pause();
      audioRef.current.currentTime = 0;
      setIsPlaying(false);
    } else {
      // Luôn tạo đối tượng Audio mới với URL hiện tại
      audioRef.current = new Audio(result.result_url);
      audioRef.current.onended = () => setIsPlaying(false);
      
      // Cập nhật tốc độ phát nếu cần
      audioRef.current.playbackRate = speed;

      audioRef.current.play()
        .then(() => setIsPlaying(true))
        .catch(err => {
          console.error('Lỗi khi phát audio:', err);
          setError('Không thể phát audio');
        });
    }
  };

  // Cập nhật audioRef khi result thay đổi
  useEffect(() => {
    // Dọn dẹp audio trước đó nếu có
    if (audioRef.current) {
      audioRef.current.pause();
      audioRef.current = null;
    }
  }, [result]);

  // Xử lý tải xuống kết quả
  const handleDownload = () => {
    if (result && result.result_url) {
      VoiceAPI.downloadResult(result.result_url);
    }
  };

  // Cleanup khi component unmount
  useEffect(() => {
    return () => {
      if (audioRef.current) {
        audioRef.current.pause();
        audioRef.current = null;
      }
    };
  }, []);

  const toggleHistory = () => {
    setShowHistory(!showHistory);
  };
  
  const toggleInfo = () => {
    setShowInfo(!showInfo);
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

  return (
    <Box>
      <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6">
            Chuyển văn bản thành giọng nói
          </Typography>
          <Tooltip title="Xem thông tin về tính năng TTS">
            <IconButton onClick={toggleInfo}>
              <InfoIcon />
            </IconButton>
          </Tooltip>
        </Box>
        
        {showInfo && (
          <Alert severity="info" sx={{ mb: 3 }}>
            <Typography variant="body2" gutterBottom>
              Tính năng này sử dụng MeloTTS và OpenVoice để tạo giọng nói từ văn bản:
            </Typography>
            <ul style={{ margin: '8px 0', paddingLeft: '20px' }}>
              <li>Hỗ trợ nhiều ngôn ngữ: Anh, Trung, Pháp, Tây Ban Nha, Nhật, Hàn</li>
              <li>Mỗi language code (en-us, zh, v.v.) tương ứng với một accent khác nhau</li>
              <li>Lần đầu sử dụng, hệ thống sẽ tự động cài đặt MeloTTS (mất khoảng 1-2 phút), vui lòng đợi và thử lại</li>
              <li>Chọn speaker phù hợp với ngôn ngữ của văn bản để có kết quả tốt nhất</li>
            </ul>
          </Alert>
        )}
        
        <Grid container spacing={3}>
          <Grid item xs={12}>
            <TextField
              label="Văn bản cần chuyển thành giọng nói"
              multiline
              rows={4}
              fullWidth
              value={text}
              onChange={handleTextChange}
              variant="outlined"
              placeholder="Nhập văn bản ở đây..."
            />
          </Grid>
          
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel id="speaker-select-label">Speaker</InputLabel>
              <Select
                labelId="speaker-select-label"
                id="speaker-select"
                value={selectedSpeaker}
                label="Speaker"
                onChange={handleSpeakerChange}
                disabled={isLoading || availableSpeakers.length === 0}
              >
                {availableSpeakers.map((speaker) => (
                  <MenuItem key={speaker} value={speaker}>
                    {getSpeakerDisplayName(speaker)}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <FormControl fullWidth>
              <InputLabel id="language-select-label">Ngôn ngữ</InputLabel>
              <Select
                labelId="language-select-label"
                id="language-select"
                value={language}
                label="Ngôn ngữ"
                onChange={handleLanguageChange}
                disabled={isLoading}
              >
                <MenuItem value="english">{getLanguageDisplayName('english')}</MenuItem>
                <MenuItem value="chinese">{getLanguageDisplayName('chinese')}</MenuItem>
                <MenuItem value="french">{getLanguageDisplayName('french')}</MenuItem>
                <MenuItem value="spanish">{getLanguageDisplayName('spanish')}</MenuItem>
                <MenuItem value="japanese">{getLanguageDisplayName('japanese')}</MenuItem>
                <MenuItem value="korean">{getLanguageDisplayName('korean')}</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          
          <Grid item xs={12}>
            <Typography id="speed-slider" gutterBottom>
              Tốc độ: {speed.toFixed(1)}x
            </Typography>
            <Slider
              aria-labelledby="speed-slider"
              value={speed}
              onChange={handleSpeedChange}
              min={0.5}
              max={2.0}
              step={0.1}
              marks={[
                { value: 0.5, label: '0.5x' },
                { value: 1.0, label: '1.0x' },
                { value: 1.5, label: '1.5x' },
                { value: 2.0, label: '2.0x' },
              ]}
              disabled={isLoading}
            />
          </Grid>
          
          <Grid item xs={12}>
            <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
              <Button
                variant="contained"
                color="primary"
                onClick={handleGenerateTts}
                disabled={isLoading || !text}
                sx={{ mr: 2 }}
              >
                {isLoading ? (
                  <>
                    <CircularProgress size={24} sx={{ mr: 1 }} />
                    Đang xử lý...
                  </>
                ) : (
                  'Tạo giọng nói'
                )}
              </Button>
              
              <Button
                variant="outlined"
                onClick={toggleHistory}
              >
                {showHistory ? 'Ẩn lịch sử' : 'Hiện lịch sử'}
              </Button>
            </Box>
          </Grid>
        </Grid>
        
        {error && (
          <Alert severity="error" sx={{ mt: 2 }}>
            {error}
          </Alert>
        )}
        
        {result && (
          <Box sx={{ mt: 3, p: 2, bgcolor: 'background.paper', borderRadius: 1 }}>
            <Typography variant="subtitle1" gutterBottom>
              Kết quả
            </Typography>
            <Divider sx={{ mb: 2 }} />
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <IconButton 
                color="primary" 
                onClick={handlePlayAudio}
                aria-label={isPlaying ? 'Dừng phát' : 'Phát audio'}
              >
                {isPlaying ? <StopIcon /> : <PlayCircleOutlineIcon />}
              </IconButton>
              <Typography variant="body1" sx={{ flex: 1, ml: 1 }}>
                {isPlaying ? 'Đang phát...' : 'Sẵn sàng phát'}
              </Typography>
              <IconButton 
                color="primary" 
                onClick={handleDownload}
                aria-label="Tải xuống"
              >
                <DownloadIcon />
              </IconButton>
            </Box>
            <Box sx={{ mt: 1 }}>
              <Chip label={`Speaker: ${getSpeakerDisplayName(result.speaker)}`} sx={{ mr: 1 }} />
              <Chip label={`Ngôn ngữ: ${getLanguageDisplayName(result.language)}`} sx={{ mr: 1 }} />
              <Chip label={`Tốc độ: ${result.speed}x`} />
            </Box>
          </Box>
        )}
      </Paper>
      
      {showHistory && (
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Lịch sử chuyển đổi
          </Typography>
          <TtsHistory />
        </Paper>
      )}
    </Box>
  );
};

export default TextToSpeechTab; 