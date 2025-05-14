import React, { useState, useEffect, useRef } from 'react';
import { 
  Container, Typography, Box, Button, Paper, 
  Grid, FormControl, InputLabel, Select, MenuItem,
  CircularProgress, Alert, IconButton, Slider, Card,
  CardContent, Tabs, Tab, Divider, Chip, List, ListItem,
  ListItemText, ListItemIcon, ListItemSecondaryAction, Tooltip
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import AudioFileIcon from '@mui/icons-material/AudioFile';
import PlayCircleOutlineIcon from '@mui/icons-material/PlayCircleOutline';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import StopIcon from '@mui/icons-material/Stop';
import InfoIcon from '@mui/icons-material/Info';
import HistoryIcon from '@mui/icons-material/History';
import DownloadIcon from '@mui/icons-material/Download';
import CompareIcon from '@mui/icons-material/Compare';
import PersonIcon from '@mui/icons-material/Person';
import TextsmsIcon from '@mui/icons-material/Textsms';
import { VoiceAPI } from '../../services/api';
import TextToSpeechTab from './TextToSpeechTab';

// Component hiển thị thông tin chi tiết giọng nói
const VoiceDetailCard = ({ voicePath }) => {
  const [voiceDetails, setVoiceDetails] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchDetails = async () => {
      if (!voicePath) return;
      
      setLoading(true);
      try {
        const response = await VoiceAPI.getVoiceDetails(voicePath);
        setVoiceDetails(response.data);
        setError('');
      } catch (err) {
        console.error('Lỗi khi lấy thông tin giọng nói:', err);
        setError('Không thể lấy thông tin giọng nói');
      } finally {
        setLoading(false);
      }
    };

    fetchDetails();
  }, [voicePath]);

  if (loading) return <CircularProgress size={20} />;
  if (error) return <Typography color="error">{error}</Typography>;
  if (!voiceDetails) return null;

  return (
    <Card variant="outlined" sx={{ mt: 2, mb: 2 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Thông tin giọng nói
        </Typography>
        <Grid container spacing={1}>
          <Grid item xs={6}>
            <Typography variant="body2">Tên file: {voiceDetails.filename}</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="body2">Độ dài: {voiceDetails.duration}s</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="body2">Sample rate: {voiceDetails.sample_rate}Hz</Typography>
          </Grid>
          <Grid item xs={6}>
            <Typography variant="body2">Kích thước: {voiceDetails.file_size_mb}MB</Typography>
          </Grid>
          {voiceDetails.voice_type && (
            <>
              <Grid item xs={6}>
                <Typography variant="body2">Loại giọng: {voiceDetails.voice_type}</Typography>
              </Grid>
              <Grid item xs={6}>
                <Typography variant="body2">Âm vực: {voiceDetails.voice_range}</Typography>
              </Grid>
              <Grid item xs={12}>
                <Tooltip title="Độ cao của giọng (Hz)">
                  <Typography variant="body2">
                    Độ cao trung bình: {voiceDetails.average_pitch}Hz
                  </Typography>
                </Tooltip>
              </Grid>
            </>
          )}
        </Grid>
      </CardContent>
    </Card>
  );
};

// Component hiển thị lịch sử chuyển đổi
const ConversionHistory = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const response = await VoiceAPI.getConversionHistory();
      setHistory(response.data);
      setError('');
    } catch (err) {
      console.error('Lỗi khi lấy lịch sử chuyển đổi:', err);
      setError('Không thể lấy lịch sử chuyển đổi');
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

  if (loading) return <CircularProgress />;
  if (error) return <Typography color="error">{error}</Typography>;
  if (history.length === 0) return <Typography>Chưa có lịch sử chuyển đổi</Typography>;

  return (
    <List>
      {history.map((item, index) => (
        <React.Fragment key={index}>
          <ListItem>
            <ListItemIcon>
              <AudioFileIcon />
            </ListItemIcon>
            <ListItemText 
              primary={`${item.source_file} → ${item.target_voice.split('/').pop()}`}
              secondary={`${formatDate(item.timestamp)} - Tau: ${item.tau}`}
            />
            <ListItemSecondaryAction>
              <IconButton edge="end" onClick={() => VoiceAPI.downloadResult(item.result_url)}>
                <DownloadIcon />
              </IconButton>
              <IconButton edge="end" onClick={() => VoiceAPI.playAudioFile(item.result_url)}>
                <VolumeUpIcon />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
          {index < history.length - 1 && <Divider />}
        </React.Fragment>
      ))}
    </List>
  );
};

const UserDashboard = () => {
  // State variables
  const [audioFile, setAudioFile] = useState(null);
  const [audioPreviewUrl, setAudioPreviewUrl] = useState(null);
  const [availableVoices, setAvailableVoices] = useState([]);
  const [selectedVoice, setSelectedVoice] = useState('');
  const [tauValue, setTauValue] = useState(0.4);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [isModelLoading, setIsModelLoading] = useState(true);
  const [currentTab, setCurrentTab] = useState(0);
  const [showVoiceDetails, setShowVoiceDetails] = useState(false);
  const [processingProgress, setProcessingProgress] = useState(0);
  const [processingStatus, setProcessingStatus] = useState('');
  const [playbackSpeed, setPlaybackSpeed] = useState(1.0);
  const [audioProgress, setAudioProgress] = useState(0);
  const [audioDuration, setAudioDuration] = useState(0);
  
  // Trạng thái phát âm thanh
  const [isSourcePlaying, setIsSourcePlaying] = useState(false);
  const [isTargetPlaying, setIsTargetPlaying] = useState(false);
  const [isResultPlaying, setIsResultPlaying] = useState(false);
  
  // Tham chiếu đến các đối tượng Audio
  const sourceAudioRef = useRef(null);
  const targetAudioRef = useRef(null);
  const resultAudioRef = useRef(null);

  // Tải danh sách giọng nói từ backend
  useEffect(() => {
    const fetchVoices = async () => {
      try {
        const response = await VoiceAPI.getModels();
        if (response.data.openvoice && response.data.openvoice.length > 0) {
          setAvailableVoices(response.data.openvoice);
          setSelectedVoice(response.data.openvoice[0]);
          setIsModelLoading(false);
        } else {
          setError('Không tìm thấy mẫu giọng nói nào');
        }
      } catch (err) {
        console.error('Lỗi khi tải danh sách giọng nói:', err);
        setError('Không thể kết nối với máy chủ. Vui lòng thử lại sau.');
      }
    };

    fetchVoices();
  }, []);

  // Xử lý khi người dùng chọn file
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.type.includes('audio') || file.name.match(/\.(wav|mp3|flac)$/)) {
        // Nếu đang phát âm thanh, dừng trước khi thay đổi file
        if (sourceAudioRef.current) {
          sourceAudioRef.current.pause();
          sourceAudioRef.current = null;
          setIsSourcePlaying(false);
        }
        
        // Giải phóng URL cũ nếu có
        if (audioPreviewUrl) {
          URL.revokeObjectURL(audioPreviewUrl);
        }
        
        setAudioFile(file);
        setError('');
        
        // Tạo URL cho file audio để nghe thử
        const fileUrl = URL.createObjectURL(file);
        setAudioPreviewUrl(fileUrl);
        
        console.log(`Đã tạo URL mới cho file: ${file.name}, URL: ${fileUrl}`);
      } else {
        setError('Vui lòng chọn file âm thanh hợp lệ (WAV, MP3, FLAC)');
        setAudioFile(null);
        setAudioPreviewUrl(null);
      }
    }
  };

  // Xử lý khi người dùng thay đổi lựa chọn giọng nói
  const handleVoiceChange = (event) => {
    setSelectedVoice(event.target.value);
  };

  // Xử lý khi người dùng thay đổi giá trị tau
  const handleTauChange = (event, newValue) => {
    setTauValue(newValue);
  };

  // Xử lý khi người dùng gửi yêu cầu chuyển đổi
  const handleConvert = async () => {
    if (!audioFile) {
      setError('Vui lòng chọn file âm thanh');
      return;
    }

    if (!selectedVoice) {
      setError('Vui lòng chọn giọng nói mục tiêu');
      return;
    }

    setIsLoading(true);
    setResult(null);
    setError('');
    setProcessingProgress(0);
    setProcessingStatus('Đang chuẩn bị xử lý...');

    // Tạo form data để gửi lên server
    const formData = new FormData();
    formData.append('audio', audioFile);
    formData.append('model_type', 'openvoice');
    formData.append('target_voice', selectedVoice);
    formData.append('tau', tauValue);

    // Giả lập tiến trình xử lý
    let progressInterval = setInterval(() => {
      setProcessingProgress((prev) => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return prev;
        }
        
        const increment = Math.random() * 10;
        const newValue = Math.min(prev + increment, 90);
        
        // Cập nhật trạng thái dựa trên tiến trình
        if (newValue < 20) {
          setProcessingStatus('Đang tải file âm thanh...');
        } else if (newValue < 40) {
          setProcessingStatus('Đang phân tích đặc trưng âm thanh nguồn...');
        } else if (newValue < 60) {
          setProcessingStatus('Đang phân tích đặc trưng giọng nói đích...');
        } else if (newValue < 80) {
          setProcessingStatus('Đang chuyển đổi giọng nói...');
        } else {
          setProcessingStatus('Đang xử lý kết quả...');
        }
        
        return newValue;
      });
    }, 1000);

    try {
      const response = await VoiceAPI.convertVoice(formData);

      if (response.data.success) {
        // Đặt tiến trình về 100% khi hoàn thành
        clearInterval(progressInterval);
        setProcessingProgress(100);
        setProcessingStatus('Hoàn thành!');
        
        setResult(response.data);
      } else {
        clearInterval(progressInterval);
        setError(response.data.error || 'Có lỗi xảy ra khi xử lý yêu cầu');
      }
    } catch (err) {
      clearInterval(progressInterval);
      console.error('Lỗi khi gửi yêu cầu chuyển đổi:', err);
      setError(err.response?.data?.error || 'Không thể kết nối với máy chủ');
    } finally {
      setIsLoading(false);
    }
  };

  // Xử lý khi người dùng tải xuống kết quả
  const handleDownload = () => {
    if (result && result.result_url) {
      VoiceAPI.downloadResult(result.result_url);
    }
  };

  // Xử lý khi người dùng chuyển tab
  const handleTabChange = (event, newValue) => {
    setCurrentTab(newValue);
  };

  // Xử lý nghe thử file nguồn
  const handlePlaySourceAudio = () => {
    // Dừng các audio khác nếu đang phát
    if (targetAudioRef.current) {
      targetAudioRef.current.pause();
      setIsTargetPlaying(false);
    }
    if (resultAudioRef.current) {
      resultAudioRef.current.pause();
      setIsResultPlaying(false);
    }

    if (isSourcePlaying && sourceAudioRef.current) {
      // Nếu đang phát, dừng lại
      sourceAudioRef.current.pause();
      setIsSourcePlaying(false);
    } else if (audioPreviewUrl) {
      // Luôn tạo đối tượng Audio mới với URL hiện tại để đảm bảo phát đúng file
      if (sourceAudioRef.current) {
        sourceAudioRef.current.pause();
        sourceAudioRef.current = null;
      }
      
      console.log(`Phát audio từ URL: ${audioPreviewUrl}`);
      sourceAudioRef.current = new Audio(audioPreviewUrl);
      
      // Xử lý sự kiện khi phát xong
      sourceAudioRef.current.onended = () => {
        setIsSourcePlaying(false);
      };
      
      // Thêm xử lý lỗi
      sourceAudioRef.current.onerror = (error) => {
        console.error('Lỗi khi phát audio:', error);
        setIsSourcePlaying(false);
        setError('Không thể phát file âm thanh này, vui lòng thử file khác');
      };
      
      sourceAudioRef.current.play()
        .then(() => {
          setIsSourcePlaying(true);
        })
        .catch(error => {
          console.error('Lỗi khi phát audio:', error);
          setIsSourcePlaying(false);
          setError('Không thể phát file âm thanh này, vui lòng thử file khác');
        });
    }
  };

  // Xử lý nghe thử giọng nói đích
  const handlePlayTargetVoice = () => {
    // Dừng các audio khác nếu đang phát
    if (sourceAudioRef.current) {
      sourceAudioRef.current.pause();
      setIsSourcePlaying(false);
    }
    if (resultAudioRef.current) {
      resultAudioRef.current.pause();
      setIsResultPlaying(false);
    }

    if (isTargetPlaying && targetAudioRef.current) {
      // Nếu đang phát, dừng lại
      targetAudioRef.current.pause();

      targetAudioRef.current = null; // Reset tham chiếu khi dừng phát
      setIsTargetPlaying(false);
    } else if (selectedVoice) {
      // Nếu chưa phát, bắt đầu phát
      const encodedPath = encodeURIComponent(selectedVoice);
      const audioUrl = `/api/play-audio?path=${encodedPath}`;
      
      // Tạo mới đối tượng Audio mỗi lần phát để tránh cache
      targetAudioRef.current = new Audio(audioUrl);
      targetAudioRef.current.onended = () => {
        targetAudioRef.current = null; // Reset tham chiếu khi phát xong
        setIsTargetPlaying(false);
      };
      
      // Thêm sự kiện xử lý lỗi
      targetAudioRef.current.onerror = (error) => {
        console.error('Lỗi khi phát audio:', error);
        targetAudioRef.current = null;
        setIsTargetPlaying(false);
        setError('Không thể phát file audio, vui lòng thử lại sau.');
      };
      
      targetAudioRef.current.play().catch(error => {
        console.error('Lỗi khi phát audio:', error);
        targetAudioRef.current = null;
        setIsTargetPlaying(false);
        setError('Không thể phát file audio, vui lòng thử lại sau.');
      });
      
      setIsTargetPlaying(true);
    }
  };

  // Reset audio khi result thay đổi
  useEffect(() => {
    if (result) {
      // Dừng phát nếu đang phát
      if (resultAudioRef.current) {
        resultAudioRef.current.pause();
        resultAudioRef.current = null;
      }
      setIsResultPlaying(false);
      setAudioProgress(0);
      setAudioDuration(0);
      console.log("Có kết quả mới, đã reset player");
    }
  }, [result]);

  // Xử lý phát âm thanh kết quả
  const handlePlayResultAudio = () => {
    // Dừng các audio khác nếu đang phát
    if (sourceAudioRef.current) {
      sourceAudioRef.current.pause();
      setIsSourcePlaying(false);
    }
    if (targetAudioRef.current) {
      targetAudioRef.current.pause();
      setIsTargetPlaying(false);
    }

    if (isResultPlaying && resultAudioRef.current) {
      // Nếu đang phát, dừng lại
      resultAudioRef.current.pause();
      resultAudioRef.current = null;
      setIsResultPlaying(false);
    } else if (result && result.result_url) {
      // Luôn tạo mới đối tượng Audio để đảm bảo phát đúng file
      if (resultAudioRef.current) {
        resultAudioRef.current.pause();
        resultAudioRef.current = null;
      }
      
      // Thêm timestamp vào URL để tránh cache
      const audioUrl = `${result.result_url}${result.result_url.includes('?') ? '&' : '?'}t=${Date.now()}`;
      console.log(`Phát kết quả từ URL: ${audioUrl}`);
      
      resultAudioRef.current = new Audio(audioUrl);
      resultAudioRef.current.playbackRate = playbackSpeed;
      
      // Lắng nghe sự kiện metadata để lấy thời lượng audio
      resultAudioRef.current.onloadedmetadata = () => {
        setAudioDuration(resultAudioRef.current.duration);
      };
      
      // Lắng nghe sự kiện timeupdate để cập nhật tiến trình
      resultAudioRef.current.ontimeupdate = () => {
        // Thêm kiểm tra null để tránh lỗi
        if (resultAudioRef.current) {
          setAudioProgress(resultAudioRef.current.currentTime);
        }
      };
      
      // Xử lý sự kiện khi phát xong
      resultAudioRef.current.onended = () => {
        setAudioProgress(0);
        // Gỡ bỏ event listeners trước khi set null
        if (resultAudioRef.current) {
          resultAudioRef.current.ontimeupdate = null;
          resultAudioRef.current.onended = null;
          resultAudioRef.current.onerror = null;
          resultAudioRef.current = null;
        }
        setIsResultPlaying(false);
      };
      
      // Thêm xử lý lỗi
      resultAudioRef.current.onerror = (error) => {
        console.error('Lỗi khi phát audio kết quả:', error);
        // Gỡ bỏ event listeners trước khi set null
        if (resultAudioRef.current) {
          resultAudioRef.current.ontimeupdate = null;
          resultAudioRef.current.onended = null;
          resultAudioRef.current.onerror = null;
          resultAudioRef.current = null;
        }
        setIsResultPlaying(false);
        setError('Không thể phát file kết quả, vui lòng thử lại sau.');
      };
      
      resultAudioRef.current.play()
        .then(() => {
          setIsResultPlaying(true);
        })
        .catch(error => {
          console.error('Lỗi khi phát audio kết quả:', error);
          // Gỡ bỏ event listeners trước khi set null
          if (resultAudioRef.current) {
            resultAudioRef.current.ontimeupdate = null;
            resultAudioRef.current.onended = null;
            resultAudioRef.current.onerror = null;
            resultAudioRef.current = null;
          }
          setIsResultPlaying(false);
          setError('Không thể phát file kết quả, vui lòng thử lại sau.');
        });
    }
  };

  // Xử lý khi người dùng tua audio
  const handleAudioSeek = (event, newValue) => {
    setAudioProgress(newValue);
    if (resultAudioRef.current) {
      resultAudioRef.current.currentTime = newValue;
    }
  };

  // Xử lý thay đổi tốc độ phát
  const handleSpeedChange = (event, newValue) => {
    setPlaybackSpeed(newValue);
    // Áp dụng tốc độ mới nếu đang phát
    if (resultAudioRef.current && isResultPlaying) {
      resultAudioRef.current.playbackRate = newValue;
    }
  };

  // Giải phóng tài nguyên khi component unmount
  useEffect(() => {
    return () => {
      // Giải phóng các URL đã tạo để tránh rò rỉ bộ nhớ
      if (audioPreviewUrl) {
        URL.revokeObjectURL(audioPreviewUrl);
      }
      
      // Dừng và giải phóng các đối tượng Audio
      if (sourceAudioRef.current) {
        sourceAudioRef.current.pause();
        sourceAudioRef.current = null;
      }
      if (targetAudioRef.current) {
        targetAudioRef.current.pause();
        targetAudioRef.current = null;
      }
      if (resultAudioRef.current) {
        resultAudioRef.current.pause();
        resultAudioRef.current = null;
      }
    };
  }, [audioPreviewUrl]);

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom sx={{ mb: 3 }}>
        Chuyển đổi giọng nói
      </Typography>
      
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs 
          value={currentTab} 
          onChange={handleTabChange}
          aria-label="voice conversion tabs"
        >
          <Tab label="Chuyển đổi giọng nói" icon={<CompareIcon />} iconPosition="start" />
          <Tab label="Text-to-Speech" icon={<TextsmsIcon />} iconPosition="start" />
          <Tab label="Lịch sử" icon={<HistoryIcon />} iconPosition="start" />
        </Tabs>
      </Box>
      
      {/* Tab chuyển đổi giọng nói */}
      {currentTab === 0 && (
        <Box>
          <Paper elevation={3} sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Tải lên file âm thanh của bạn
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12}>
                <Box sx={{ display: 'flex', justifyContent: 'center', p: 3, border: '2px dashed grey', borderRadius: 2 }}>
                  <input
                    accept="audio/*"
                    style={{ display: 'none' }}
                    id="contained-button-file"
                    type="file"
                    onChange={handleFileChange}
                    disabled={isLoading}
                  />
                  <label htmlFor="contained-button-file">
                    <Button 
                      variant="contained" 
                      component="span"
                      startIcon={<CloudUploadIcon />}
                      disabled={isLoading}
                    >
                      Chọn file âm thanh
                    </Button>
                  </label>
                </Box>
                {audioFile && (
                  <Box sx={{ mt: 2 }}>
                    <Typography variant="body1">
                      File đã chọn: {audioFile.name}
                    </Typography>
                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                      <IconButton 
                        color="primary" 
                        onClick={handlePlaySourceAudio}
                        disabled={isLoading}
                        aria-label={isSourcePlaying ? 'Dừng phát' : 'Phát audio'}
                      >
                        {isSourcePlaying ? <StopIcon /> : <PlayCircleOutlineIcon />}
                      </IconButton>
                      <Typography variant="body2">
                        {isSourcePlaying ? 'Đang phát...' : 'Nghe thử'}
                      </Typography>
                    </Box>
                  </Box>
                )}
              </Grid>
              
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel id="voice-select-label">Giọng nói mục tiêu</InputLabel>
                  <Select
                    labelId="voice-select-label"
                    id="voice-select"
                    value={selectedVoice}
                    label="Giọng nói mục tiêu"
                    onChange={handleVoiceChange}
                    disabled={isLoading || availableVoices.length === 0}
                  >
                    {availableVoices.map((voice) => (
                      <MenuItem key={voice} value={voice}>
                        {voice.split('/').pop()} {/* Hiển thị tên file không có đường dẫn */}
                      </MenuItem>
                    ))}
                  </Select>
                </FormControl>
                {selectedVoice && (
                  <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                    <IconButton 
                      color="primary" 
                      onClick={handlePlayTargetVoice}
                      disabled={isLoading}
                      aria-label={isTargetPlaying ? 'Dừng phát' : 'Nghe giọng mục tiêu'}
                    >
                      {isTargetPlaying ? <StopIcon /> : <VolumeUpIcon />}
                    </IconButton>
                    <Typography variant="body2">
                      {isTargetPlaying ? 'Đang phát...' : 'Nghe thử giọng mục tiêu'}
                    </Typography>
                    <IconButton 
                      color="info" 
                      onClick={() => setShowVoiceDetails(!showVoiceDetails)}
                      aria-label="Xem thông tin chi tiết"
                      sx={{ ml: 'auto' }}
                    >
                      <InfoIcon />
                    </IconButton>
                  </Box>
                )}
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Typography id="tau-slider" gutterBottom>
                  Tau (độ giống giọng mục tiêu): {tauValue}
                </Typography>
                <Slider
                  aria-labelledby="tau-slider"
                  value={tauValue}
                  onChange={handleTauChange}
                  min={0.1}
                  max={1.0}
                  step={0.05}
                  marks={[
                    { value: 0.1, label: '0.1' },
                    { value: 0.4, label: '0.4' },
                    { value: 0.7, label: '0.7' },
                    { value: 1.0, label: '1.0' },
                  ]}
                  disabled={isLoading}
                />
                <Typography variant="body2" color="textSecondary">
                  Giá trị thấp: giữ nhiều đặc điểm từ giọng gốc. Giá trị cao: giống hơn với giọng mục tiêu.
                </Typography>
              </Grid>
              
              <Grid item xs={12}>
                <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                  <Button
                    variant="contained"
                    color="primary"
                    onClick={handleConvert}
                    disabled={isLoading || !audioFile || !selectedVoice}
                  >
                    {isLoading ? (
                      <>
                        <CircularProgress size={24} sx={{ mr: 1 }} />
                        Đang xử lý...
                      </>
                    ) : (
                      'Chuyển đổi giọng nói'
                    )}
                  </Button>
                </Box>
              </Grid>
            </Grid>
            
            {error && (
              <Alert severity="error" sx={{ mt: 2 }}>
                {error}
              </Alert>
            )}
            
            {isLoading && (
              <Box sx={{ mt: 2, textAlign: 'center' }}>
                <CircularProgress variant="determinate" value={processingProgress} />
                <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
                  {processingStatus || 'Đang xử lý...'}
                </Typography>
              </Box>
            )}
            
            {showVoiceDetails && selectedVoice && (
              <VoiceDetailCard voicePath={selectedVoice} />
            )}
          </Paper>
          
          {result && (
            <Paper elevation={3} sx={{ p: 3 }}>
              <Typography variant="h6" gutterBottom>
                Kết quả chuyển đổi
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                <IconButton 
                  color="primary" 
                  onClick={handlePlayResultAudio}
                  aria-label={isResultPlaying ? 'Dừng phát' : 'Phát kết quả'}
                >
                  {isResultPlaying ? <StopIcon /> : <PlayCircleOutlineIcon />}
                </IconButton>
                <Typography variant="body2" sx={{ ml: 1, minWidth: '70px' }}>
                  {audioDuration > 0 
                    ? `${Math.floor(audioProgress / 60)}:${Math.floor(audioProgress % 60).toString().padStart(2, '0')} / ${Math.floor(audioDuration / 60)}:${Math.floor(audioDuration % 60).toString().padStart(2, '0')}`
                    : isResultPlaying ? 'Đang phát...' : 'Nghe kết quả'}
                </Typography>
                
                <Box sx={{ flex: 1, mx: 2 }}>
                  <Slider
                    size="small"
                    value={audioProgress}
                    max={audioDuration || 100}
                    onChange={handleAudioSeek}
                    aria-label="Vị trí audio"
                    disabled={!isResultPlaying && audioProgress === 0}
                  />
                </Box>
                
                <Button
                  variant="outlined"
                  size="small"
                  startIcon={<DownloadIcon />}
                  onClick={handleDownload}
                >
                  Tải xuống
                </Button>
              </Box>
              
              {/* Điều chỉnh tốc độ phát */}
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Typography id="speed-slider" sx={{ width: '120px' }}>
                  Tốc độ phát: {playbackSpeed.toFixed(1)}x
                </Typography>
                <Slider
                  aria-labelledby="speed-slider"
                  value={playbackSpeed}
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
                  sx={{ ml: 2, width: 'calc(100% - 150px)' }}
                />
              </Box>
              
              <Divider sx={{ my: 2 }} />
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="body2">
                    <strong>File nguồn:</strong> {audioFile?.name}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body2">
                    <strong>Giọng mục tiêu:</strong> {selectedVoice.split('/').pop()}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body2">
                    <strong>Tau:</strong> {tauValue}
                  </Typography>
                </Grid>
                <Grid item xs={12} md={6}>
                  <Typography variant="body2">
                    <strong>Ngày tạo:</strong> {new Date().toLocaleString('vi-VN')}
                  </Typography>
                </Grid>
              </Grid>
            </Paper>
          )}
        </Box>
      )}
      
      {/* Tab Text-to-Speech */}
      {currentTab === 1 && <TextToSpeechTab />}
      
      {/* Tab lịch sử */}
      {currentTab === 2 && (
        <Paper elevation={3} sx={{ p: 3 }}>
          <Typography variant="h6" gutterBottom>
            Lịch sử chuyển đổi giọng nói
          </Typography>
          <ConversionHistory />
        </Paper>
      )}
      
    </Container>
  );
};

export default UserDashboard; 