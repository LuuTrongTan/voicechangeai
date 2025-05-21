import React, { useState, useEffect, useRef } from 'react';
import { 
  Typography, Box, Button, Paper, 
  Grid, FormControl, InputLabel, Select, MenuItem,
  CircularProgress, Alert, IconButton, Slider, Card,
  CardContent, TextField, Divider, Tabs, Tab,
  FormControlLabel, Radio, RadioGroup, Switch,
  List, ListItem, ListItemIcon, ListItemText, ListItemSecondaryAction
} from '@mui/material';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import AudioFileIcon from '@mui/icons-material/AudioFile';
import PlayCircleOutlineIcon from '@mui/icons-material/PlayCircleOutline';
import VolumeUpIcon from '@mui/icons-material/VolumeUp';
import StopIcon from '@mui/icons-material/Stop';
import DownloadIcon from '@mui/icons-material/Download';
import TuneIcon from '@mui/icons-material/Tune';
import MusicNoteIcon from '@mui/icons-material/MusicNote';
import SettingsVoiceIcon from '@mui/icons-material/SettingsVoice';
import BuildIcon from '@mui/icons-material/Build';
import DeviceHubIcon from '@mui/icons-material/DeviceHub';
import FolderZipIcon from '@mui/icons-material/FolderZip';
import FolderIcon from '@mui/icons-material/Folder';
import SaveIcon from '@mui/icons-material/Save';
import HistoryIcon from '@mui/icons-material/History';
import MicOffIcon from '@mui/icons-material/MicOff';
import { VoiceAPI } from '../../services/api';

// TabPanel component để hiển thị nội dung tab
function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`rvc-tabpanel-${index}`}
      aria-labelledby={`rvc-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 2 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

// Component hiển thị lịch sử chuyển đổi RVC
const RVCConversionHistory = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const response = await VoiceAPI.rvc.getConversionHistory();
      setHistory(response.data);
      setError('');
    } catch (err) {
      console.error('Lỗi khi lấy lịch sử chuyển đổi RVC:', err);
      setError('Không thể lấy lịch sử chuyển đổi RVC');
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
  if (history.length === 0) return <Typography>Chưa có lịch sử chuyển đổi RVC</Typography>;

  return (
    <List>
      {history.map((item, index) => (
        <React.Fragment key={index}>
          <ListItem>
            <ListItemIcon>
              <AudioFileIcon />
            </ListItemIcon>
            <ListItemText 
              primary={`${item.source_file} → ${typeof item.target_voice === 'string' ? item.target_voice.split('/').pop() : item.target_voice}`}
              secondary={
                <Box>
                  <Typography variant="body2" color="textSecondary">
                    {formatDate(item.timestamp)}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    F0 Key: {item.params?.f0up_key || 0}, 
                    Index Rate: {item.params?.index_rate || 0.5},
                    Protect: {item.params?.protect || 0.33}
                  </Typography>
                </Box>
              }
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

// Component hiển thị lịch sử tách giọng UVR
const UVRHistory = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchHistory = async () => {
    setLoading(true);
    try {
      const response = await VoiceAPI.rvc.getUvrHistory();
      setHistory(response.data);
      setError('');
    } catch (err) {
      console.error('Lỗi khi lấy lịch sử tách giọng UVR:', err);
      setError('Không thể lấy lịch sử tách giọng UVR');
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
  if (history.length === 0) return <Typography>Chưa có lịch sử tách giọng UVR</Typography>;

  return (
    <List>
      {history.map((item, index) => (
        <React.Fragment key={index}>
          <ListItem>
            <ListItemIcon>
              <MicOffIcon />
            </ListItemIcon>
            <ListItemText 
              primary={`${item.source_file} - ${item.model_name}`}
              secondary={formatDate(item.timestamp)}
            />
            <ListItemSecondaryAction>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Typography variant="body2" sx={{ mr: 1 }}>Vocals:</Typography>
                <IconButton edge="end" onClick={() => VoiceAPI.downloadResult(item.vocals_url)}>
                  <DownloadIcon />
                </IconButton>
                <IconButton edge="end" onClick={() => VoiceAPI.playAudioFile(item.vocals_url)}>
                  <VolumeUpIcon />
                </IconButton>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <Typography variant="body2" sx={{ mr: 1 }}>Instrumental:</Typography>
                <IconButton edge="end" onClick={() => VoiceAPI.downloadResult(item.instrumental_url)}>
                  <DownloadIcon />
                </IconButton>
                <IconButton edge="end" onClick={() => VoiceAPI.playAudioFile(item.instrumental_url)}>
                  <VolumeUpIcon />
                </IconButton>
              </Box>
            </ListItemSecondaryAction>
          </ListItem>
          {index < history.length - 1 && <Divider />}
        </React.Fragment>
      ))}
    </List>
  );
};

// Mapping tên mô hình UVR sang tiếng Việt thân thiện
const uvrModelDisplayName = (model) => {
  if (model.startsWith('HP5_only_main_vocal')) return 'HP5 (Tách giọng hát chính, nhạc nền phức tạp) (' + model + ')';
  if (model.startsWith('HP5')) return 'HP5 (Tách nhiều loại, nhạc nền phức tạp) (' + model + ')';
  if (model.startsWith('HP3')) return 'HP3 (Tách tất cả giọng nói, nhạc nền đơn giản) (' + model + ')';
  if (model.startsWith('HP2_all_vocals')) return 'HP2 (Tách tất cả giọng nói, tốt cho nhạc nền đơn giản) (' + model + ')';
  if (model.startsWith('HP2-')) return 'HP2 (Tách giọng người/không phải người, nhạc nền đơn giản) (' + model + ')';
  if (model.startsWith('VR-DeEchoNormal')) return 'DeEcho Bình thường (Khử vang nhẹ) (' + model + ')';
  if (model.startsWith('VR-DeEchoAggressive')) return 'DeEcho Mạnh (Khử vang mạnh) (' + model + ')';
  if (model.startsWith('HP5_only_main_vocal')) return 'HP5 (Tách giọng chính) (' + model + ')';
  if (model.startsWith('HP5')) return 'HP5 (Tách nhiều loại) (' + model + ')';
  if (model.startsWith('HP3')) return 'HP3 (Tách tất cả giọng nói) (' + model + ')';
  if (model.startsWith('HP2')) return 'HP2 (Tách tất cả giọng nói) (' + model + ')';
  if (model.startsWith('VR-DeEchoNormal')) return 'DeEcho Bình thường (' + model + ')';
  if (model.startsWith('VR-DeEchoAggressive')) return 'DeEcho Mạnh (' + model + ')';
  if (model.startsWith('VR-DeEchoDeReverb')) return 'DeEcho + Khử vang (' + model + ')';
  return model;
};

const RVCTab = () => {
  // State cho tab navigation - theo infer-web.py
  const [activeTab, setActiveTab] = useState(0);
  // State mới cho tab lịch sử
  const [historyTab, setHistoryTab] = useState(0);

  // State cho mô hình
  const [availableVoices, setAvailableVoices] = useState([]);
  const [selectedVoice, setSelectedVoice] = useState('');
  const [isModelLoading, setIsModelLoading] = useState(true);
  
  // State cho file index feature
  const [indexPaths, setIndexPaths] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState('');
  const [indexInputPath, setIndexInputPath] = useState('');
  
  // State cho chuyển đổi giọng nói (đơn lẻ)
  const [audioFile, setAudioFile] = useState(null);
  const [audioPreviewUrl, setAudioPreviewUrl] = useState(null);
  const [isSourcePlaying, setIsSourcePlaying] = useState(false);
  const [isResultPlaying, setIsResultPlaying] = useState(false);
  const [f0Method, setF0Method] = useState('rmvpe');
  const [f0UpKey, setF0UpKey] = useState(0);
  const [indexRate, setIndexRate] = useState(0.75);
  const [protectValue, setProtectValue] = useState(0.33);
  const [resampleRate, setResampleRate] = useState(0);
  const [rmsRate, setRmsRate] = useState(0.25);
  const [filterRadius, setFilterRadius] = useState(3);
  const [isConverting, setIsConverting] = useState(false);
  const [result, setResult] = useState(null);
  
  // State cho batch processing
  const [batchInputDir, setBatchInputDir] = useState('');
  const [batchOutputDir, setBatchOutputDir] = useState('opt');
  const [batchFormats, setBatchFormats] = useState('wav');
  const [isBatchProcessing, setIsBatchProcessing] = useState(false);
  const [batchResult, setBatchResult] = useState(null);
  
  // State cho UVR (tách vocals)
  const [uvrModels, setUvrModels] = useState([]);
  const [selectedUvrModel, setSelectedUvrModel] = useState('');
  const [uvrFile, setUvrFile] = useState(null);
  const [vocalOutputDir, setVocalOutputDir] = useState('opt');
  const [instrumentalOutputDir, setInstrumentalOutputDir] = useState('opt');
  const [isUvrProcessing, setIsUvrProcessing] = useState(false);
  const [uvrResult, setUvrResult] = useState(null);
  
  // State cho training
  const [experimentName, setExperimentName] = useState('');
  const [trainsetDir, setTrainsetDir] = useState('');
  const [targetSR, setTargetSR] = useState('40k');
  const [ifF0, setIfF0] = useState(true);
  const [speakerId, setSpeakerId] = useState(0);
  const [batchSize, setBatchSize] = useState(4);
  const [totalEpochs, setTotalEpochs] = useState(20);
  const [saveEpochs, setSaveEpochs] = useState(5);
  const [pretrained, setPretrained] = useState(true);
  const [pretrainedG, setPretrainedG] = useState('');
  const [pretrainedD, setPretrainedD] = useState('');
  const [gpuIds, setGpuIds] = useState('0');
  const [isTraining, setIsTraining] = useState(false);
  
  // State cho hiển thị lỗi
  const [error, setError] = useState('');
  
  // Refs cho audio players
  const sourceAudioRef = useRef(null);
  const resultAudioRef = useRef(null);
  const vocalsAudioRef = useRef(null);
  const instrumentalAudioRef = useRef(null);
  const uvrSourceAudioRef = useRef(null); // Thêm ref cho file UVR source

  // Thêm state để quản lý việc phát âm thanh và vị trí phát
  const [audioProgress, setAudioProgress] = useState(0);
  const [audioDuration, setAudioDuration] = useState(0);
  const [vocalsProgress, setVocalsProgress] = useState(0);
  const [vocalsDuration, setVocalsDuration] = useState(0);
  const [instrumentalProgress, setInstrumentalProgress] = useState(0);
  const [instrumentalDuration, setInstrumentalDuration] = useState(0);
  const [uvrSourceProgress, setUvrSourceProgress] = useState(0); // Thêm state cho progress
  const [uvrSourceDuration, setUvrSourceDuration] = useState(0); // Thêm state cho duration
  
  // Thêm state để quản lý việc phát vocals và instrumental
  const [isVocalsPlaying, setIsVocalsPlaying] = useState(false);
  const [isInstrumentalPlaying, setIsInstrumentalPlaying] = useState(false);
  const [isUvrSourcePlaying, setIsUvrSourcePlaying] = useState(false); // Thêm state cho phát UVR source
  
  // Tải danh sách model và index paths khi component mount
  useEffect(() => {
    const loadModelsAndIndices = async () => {
      try {
        // Tải danh sách model RVC
        const response = await VoiceAPI.rvc.getModels();
        if (response.data && response.data.models) {
          const voices = response.data.models;
          if (voices.length > 0) {
            setAvailableVoices(voices);
            setSelectedVoice(voices[0]);
          } else {
            setError('Không tìm thấy mô hình RVC nào.');
          }
        }
        // Tải danh sách index files
        if (response.data && response.data.indices) {
          const indices = response.data.indices;
          setIndexPaths(indices);
          if (indices.length > 0) {
            setSelectedIndex(indices[0]);
          }
        }
        // Tải danh sách model UVR5 từ API riêng biệt
        const uvrResponse = await fetch('http://localhost:5000/api/uvr/models');
        const uvrData = await uvrResponse.json();
        if (uvrData && uvrData.success && uvrData.models) {
          setUvrModels(uvrData.models);
          if (uvrData.models.length > 0) {
            setSelectedUvrModel(uvrData.models[0]);
          }
        }
      } catch (err) {
        console.error('Lỗi khi tải danh sách mô hình:', err);
        setError('Không thể kết nối với máy chủ. Vui lòng thử lại sau.');
      } finally {
        setIsModelLoading(false);
      }
    };
    loadModelsAndIndices();
  }, []);

  // Xử lý khi người dùng chọn file
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.type.includes('audio') || file.name.match(/\.(wav|mp3|flac|ogg)$/)) {
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
        
        // Reset kết quả khi chọn file mới
        setResult(null);
      } else {
        setError('Vui lòng chọn file âm thanh hợp lệ (WAV, MP3, FLAC, OGG)');
        setAudioFile(null);
        setAudioPreviewUrl(null);
      }
    }
  };

  // Xử lý khi người dùng chọn UVR file
  const handleUvrFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      if (file.type.includes('audio') || file.name.match(/\.(wav|mp3|flac|ogg)$/)) {
        // Dừng phát âm thanh nếu đang phát
        if (uvrSourceAudioRef.current) {
          uvrSourceAudioRef.current.pause();
          uvrSourceAudioRef.current = null;
          setIsUvrSourcePlaying(false);
        }
        
        setUvrFile(file);
        setUvrResult(null);
        setError('');
      } else {
        setError('Vui lòng chọn file âm thanh hợp lệ (WAV, MP3, FLAC, OGG)');
        setUvrFile(null);
      }
    }
  };

  // Xử lý khi người dùng chọn giọng nói
  const handleVoiceChange = (event) => {
    setSelectedVoice(event.target.value);
  };

  // Xử lý khi người dùng chọn index
  const handleIndexChange = (event) => {
    setSelectedIndex(event.target.value);
  };

  // Xử lý phát/dừng âm thanh gốc
  const handlePlaySourceAudio = () => {
    if (isSourcePlaying) {
      // Nếu đang phát thì dừng lại
      if (sourceAudioRef.current) {
        sourceAudioRef.current.pause();
        setIsSourcePlaying(false);
      }
    } else {
      // Nếu chưa phát thì tạo và phát
      const audio = new Audio(audioPreviewUrl);
      audio.onended = () => {
        setIsSourcePlaying(false);
        sourceAudioRef.current = null;
      };
      
      sourceAudioRef.current = audio;
      audio.play()
        .then(() => setIsSourcePlaying(true))
        .catch(error => {
          console.error('Lỗi khi phát âm thanh:', error);
          setError('Không thể phát âm thanh. Vui lòng thử lại.');
          setIsSourcePlaying(false);
        });
    }
  };

  // Xử lý phát/dừng âm thanh kết quả với thanh tua
  const handlePlayResultAudio = () => {
    if (!result || !result.result_url) {
      setError('Không có kết quả để phát');
      return;
    }
    
    if (isResultPlaying) {
      // Nếu đang phát thì dừng lại
      if (resultAudioRef.current) {
        resultAudioRef.current.pause();
        setIsResultPlaying(false);
      }
    } else {
      // Nếu chưa phát thì tạo và phát
      // Thêm domain của backend nếu URL là tương đối
      let audioUrl = result.result_url;
      if (audioUrl.startsWith('/')) {
        audioUrl = `http://localhost:5000${audioUrl}`;
      }
      
      // Thêm timestamp vào URL để tránh cache
      audioUrl = `${audioUrl}${audioUrl.includes('?') ? '&' : '?'}t=${Date.now()}`;
      
      const audio = new Audio(audioUrl);
      
      // Lắng nghe sự kiện metadata để lấy thời lượng audio
      audio.onloadedmetadata = () => {
        setAudioDuration(audio.duration);
      };
      
      // Lắng nghe sự kiện timeupdate để cập nhật tiến trình
      audio.ontimeupdate = () => {
        setAudioProgress(audio.currentTime);
      };
      
      // Xử lý sự kiện khi phát xong
      audio.onended = () => {
        setAudioProgress(0);
        setIsResultPlaying(false);
        resultAudioRef.current = null;
      };
      
      resultAudioRef.current = audio;
      audio.play()
        .then(() => setIsResultPlaying(true))
        .catch(error => {
          console.error('Lỗi khi phát âm thanh kết quả:', error);
          setError('Không thể phát âm thanh kết quả. Vui lòng thử lại.');
          setIsResultPlaying(false);
        });
    }
  };

  // Xử lý tải xuống kết quả
  const handleDownload = (url) => {
    if (url) {
      // Thêm domain của backend nếu URL là tương đối
      let downloadUrl = url;
      if (downloadUrl.startsWith('/')) {
        downloadUrl = `http://localhost:5000${downloadUrl}`;
      }
      
      // Debug log
      console.log("DEBUG - URL download hoàn chỉnh:", downloadUrl);
      
      // Kiểm tra URL bằng cách tạo yêu cầu fetch trước
      fetch(downloadUrl, { method: 'HEAD' })
        .then(response => {
          if (response.ok) {
            // Nếu URL tồn tại, tiến hành tải xuống
            VoiceAPI.downloadResult(downloadUrl);
          } else {
            // Nếu URL không tồn tại, thử thay đổi URL
            if (downloadUrl.includes('vocals_')) {
              const altUrl = downloadUrl.replace('vocals_', 'vocal_');
              console.log("DEBUG - Thử URL download thay thế cho vocals:", altUrl);
              VoiceAPI.downloadResult(altUrl);
            } 
            else if (downloadUrl.includes('instrumental_')) {
              const altUrl = downloadUrl.replace('instrumental_', 'instrument_');
              console.log("DEBUG - Thử URL download thay thế cho instrumental:", altUrl);
              VoiceAPI.downloadResult(altUrl);
            }
            else {
              setError('Không thể tải xuống file. URL không tồn tại.');
            }
          }
        })
        .catch(error => {
          console.error('Lỗi kiểm tra URL download:', error);
          setError('Lỗi kiểm tra URL download. Vui lòng thử lại.');
        });
    } else {
      setError('Không có kết quả để tải xuống');
    }
  };

  // Xử lý khi người dùng nhấn nút chuyển đổi
  const handleConvert = async () => {
    if (!audioFile) {
      setError('Vui lòng chọn file âm thanh');
      return;
    }
    
    if (!selectedVoice) {
      setError('Vui lòng chọn giọng nói đích');
      return;
    }
    
    setIsConverting(true);
    setError('');
    setResult(null);
    
    try {
      // Tạo FormData để gửi lên server
      const formData = new FormData();
      formData.append('audio', audioFile);
      formData.append('model_type', 'rvc');
      formData.append('target_voice', selectedVoice);
      
      // Thêm các tham số
      formData.append('f0_method', f0Method);
      formData.append('f0up_key', f0UpKey.toString());
      formData.append('index_rate', indexRate.toString());
      formData.append('protect', protectValue.toString());
      formData.append('filter_radius', filterRadius.toString());
      formData.append('resample_sr', resampleRate.toString());
      formData.append('rms_mix_rate', rmsRate.toString());
      
      // Thêm index path nếu có
      if (indexInputPath) {
        formData.append('file_index1', indexInputPath);
      } else if (selectedIndex) {
        formData.append('file_index2', selectedIndex);
      }
      
      // Gửi request lên server
      const response = await VoiceAPI.convertVoice(formData);
      
      if (response.data.success) {
        setResult(response.data);
        console.log('Đã nhận kết quả:', response.data);
    } else {
        setError(`Chuyển đổi thất bại: ${response.data.error || 'Lỗi không xác định'}`);
    }
    } catch (err) {
      console.error('Lỗi khi chuyển đổi giọng nói:', err);
      if (err.response && err.response.data && err.response.data.error) {
        setError(`Lỗi: ${err.response.data.error}`);
      } else {
        setError('Lỗi kết nối đến máy chủ. Vui lòng thử lại sau.');
      }
    } finally {
      setIsConverting(false);
    }
  };
  
  // Xử lý khi người dùng nhấn nút xử lý hàng loạt (batch)
  const handleBatchConvert = async () => {
    if (!batchInputDir) {
      setError('Vui lòng nhập đường dẫn thư mục đầu vào');
      return;
    }
    
    if (!selectedVoice) {
      setError('Vui lòng chọn giọng nói đích');
      return;
    }
    
    setIsBatchProcessing(true);
    setError('');
    setBatchResult(null);
    
    try {
      // Tạo dữ liệu để gửi lên server
      const data = {
        input_dir: batchInputDir,
        output_dir: batchOutputDir,
        model_type: 'rvc',
        target_voice: selectedVoice,
        f0_method: f0Method,
        f0up_key: f0UpKey,
        index_rate: indexRate,
        protect: protectValue,
        filter_radius: filterRadius,
        resample_sr: resampleRate,
        rms_mix_rate: rmsRate,
        format: batchFormats
      };
      
      // Thêm index path nếu có
      if (indexInputPath) {
        data.file_index1 = indexInputPath;
      } else if (selectedIndex) {
        data.file_index2 = selectedIndex;
      }
      
      // Gửi request lên server
      const response = await VoiceAPI.rvc.convertBatch(data);
      
      if (response.data.success) {
        setBatchResult(response.data);
        console.log('Đã nhận kết quả xử lý hàng loạt:', response.data);
      } else {
        setError(`Xử lý hàng loạt thất bại: ${response.data.error || 'Lỗi không xác định'}`);
      }
    } catch (err) {
      console.error('Lỗi khi xử lý hàng loạt:', err);
      if (err.response && err.response.data && err.response.data.error) {
        setError(`Lỗi: ${err.response.data.error}`);
      } else {
        setError('Lỗi kết nối đến máy chủ. Vui lòng thử lại sau.');
      }
    } finally {
      setIsBatchProcessing(false);
    }
  };
  
  // Xử lý khi người dùng nhấn nút tách vocals (UVR)
  const handleSeparateVocals = async () => {
    if (!uvrFile) {
      setError('Vui lòng chọn file âm thanh');
      return;
    }
    
    if (!selectedUvrModel) {
      setError('Vui lòng chọn mô hình UVR');
      return;
    }
    
    setIsUvrProcessing(true);
    setError('');
    setUvrResult(null);
    
    try {
      // Tạo FormData để gửi lên server
      const formData = new FormData();
      formData.append('audio', uvrFile);
      formData.append('model', selectedUvrModel);
      formData.append('vocal_output', 'opt');
      formData.append('instrumental_output', 'opt');
      
      // Gửi request lên server
      const response = await VoiceAPI.rvc.separateVocals(uvrFile, selectedUvrModel);
      
      if (response.data.success) {
        setUvrResult(response.data);
        console.log('Đã nhận kết quả tách vocals:', response.data);
      } else {
        setError(`Tách vocals thất bại: ${response.data.error || 'Lỗi không xác định'}`);
      }
    } catch (err) {
      console.error('Lỗi khi tách vocals:', err);
      if (err.response && err.response.data && err.response.data.error) {
        setError(`Lỗi: ${err.response.data.error}`);
      } else {
        setError('Lỗi kết nối đến máy chủ. Vui lòng thử lại sau.');
      }
    } finally {
      setIsUvrProcessing(false);
    }
  };

  // Phát file âm thanh vocals với khả năng pause và thanh tua
  const handlePlayVocals = () => {
    if (!uvrResult || !uvrResult.vocals_url) {
      setError('Không có file vocals để phát');
      return;
    }

    // Dừng phát instrumental nếu đang phát
    if (instrumentalAudioRef.current) {
      instrumentalAudioRef.current.pause();
      setIsInstrumentalPlaying(false);
    }
    
    if (isVocalsPlaying) {
      // Nếu đang phát thì dừng lại
      if (vocalsAudioRef.current) {
        vocalsAudioRef.current.pause();
        setIsVocalsPlaying(false);
      }
    } else {
      // Nếu chưa phát thì tạo và phát
      // Thêm domain của backend nếu URL là tương đối
      let audioUrl = uvrResult.vocals_url;
      if (audioUrl.startsWith('/')) {
        audioUrl = `http://localhost:5000${audioUrl}`;
      }
      
      // Thêm timestamp vào URL để tránh cache
      audioUrl = `${audioUrl}${audioUrl.includes('?') ? '&' : '?'}t=${Date.now()}`;
      
      const audio = new Audio(audioUrl);
      
      // Lắng nghe sự kiện metadata để lấy thời lượng audio
      audio.onloadedmetadata = () => {
        setVocalsDuration(audio.duration);
      };
      
      // Lắng nghe sự kiện timeupdate để cập nhật tiến trình
      audio.ontimeupdate = () => {
        setVocalsProgress(audio.currentTime);
      };
      
      // Xử lý sự kiện khi phát xong
      audio.onended = () => {
        setVocalsProgress(0);
        setIsVocalsPlaying(false);
        vocalsAudioRef.current = null;
      };
      
      vocalsAudioRef.current = audio;
      audio.play()
        .then(() => setIsVocalsPlaying(true))
        .catch(error => {
          console.error('Lỗi khi phát file vocals:', error);
          setError('Không thể phát file vocals. Vui lòng thử lại.');
          setIsVocalsPlaying(false);
        });
    }
  };

  // Phát file âm thanh instrumental với khả năng pause và thanh tua
  const handlePlayInstrumental = () => {
    if (!uvrResult || !uvrResult.instrumental_url) {
      setError('Không có file instrumental để phát');
      return;
    }

    // Dừng phát vocals nếu đang phát
    if (vocalsAudioRef.current) {
      vocalsAudioRef.current.pause();
      setIsVocalsPlaying(false);
    }
    
    if (isInstrumentalPlaying) {
      // Nếu đang phát thì dừng lại
      if (instrumentalAudioRef.current) {
        instrumentalAudioRef.current.pause();
        setIsInstrumentalPlaying(false);
      }
    } else {
      // Nếu chưa phát thì tạo và phát
      // Thêm domain của backend nếu URL là tương đối
      let audioUrl = uvrResult.instrumental_url;
      if (audioUrl.startsWith('/')) {
        audioUrl = `http://localhost:5000${audioUrl}`;
      }
      
      // Thêm timestamp vào URL để tránh cache
      audioUrl = `${audioUrl}${audioUrl.includes('?') ? '&' : '?'}t=${Date.now()}`;
      
      const audio = new Audio(audioUrl);
      
      // Lắng nghe sự kiện metadata để lấy thời lượng audio
      audio.onloadedmetadata = () => {
        setInstrumentalDuration(audio.duration);
      };
      
      // Lắng nghe sự kiện timeupdate để cập nhật tiến trình
      audio.ontimeupdate = () => {
        setInstrumentalProgress(audio.currentTime);
      };
      
      // Xử lý sự kiện khi phát xong
      audio.onended = () => {
        setInstrumentalProgress(0);
        setIsInstrumentalPlaying(false);
        instrumentalAudioRef.current = null;
      };
      
      instrumentalAudioRef.current = audio;
      audio.play()
        .then(() => setIsInstrumentalPlaying(true))
        .catch(error => {
          console.error('Lỗi khi phát file instrumental:', error);
          setError('Không thể phát file instrumental. Vui lòng thử lại.');
          setIsInstrumentalPlaying(false);
        });
    }
  };

  // Xử lý khi người dùng tua audio kết quả
  const handleAudioSeek = (event, newValue) => {
    setAudioProgress(newValue);
    if (resultAudioRef.current) {
      resultAudioRef.current.currentTime = newValue;
    }
  };
  
  // Xử lý khi người dùng tua audio vocals
  const handleVocalsSeek = (event, newValue) => {
    setVocalsProgress(newValue);
    if (vocalsAudioRef.current) {
      vocalsAudioRef.current.currentTime = newValue;
    }
  };
  
  // Xử lý khi người dùng tua audio instrumental
  const handleInstrumentalSeek = (event, newValue) => {
    setInstrumentalProgress(newValue);
    if (instrumentalAudioRef.current) {
      instrumentalAudioRef.current.currentTime = newValue;
    }
  };

  // Xử lý khi người dùng nhấn nút train model
  const handleTrainModel = async () => {
    if (!experimentName) {
      setError('Vui lòng nhập tên thí nghiệm');
      return;
    }
    
    if (!trainsetDir) {
      setError('Vui lòng nhập đường dẫn thư mục dữ liệu huấn luyện');
      return;
    }
    
    setIsTraining(true);
    setError('');
    
    try {
      // Tạo dữ liệu để gửi lên server
      const data = {
        exp_name: experimentName,
        trainset_dir: trainsetDir,
        sr: targetSR,
        if_f0: ifF0,
        speaker_id: speakerId,
        save_epoch: saveEpochs,
        total_epoch: totalEpochs,
        batch_size: batchSize,
        gpus: gpuIds
      };
      
      // Thêm pretrained models nếu có
      if (pretrained) {
        data.pretrained_G = pretrainedG;
        data.pretrained_D = pretrainedD;
      }
      
      // Gửi request lên server
      const response = await VoiceAPI.rvc.trainModel(data);
      
      if (response.data.success) {
        setError('');
        alert('Quá trình huấn luyện đã bắt đầu. Bạn có thể theo dõi tiến trình trong log.');
      } else {
        setError(`Huấn luyện thất bại: ${response.data.error || 'Lỗi không xác định'}`);
      }
    } catch (err) {
      console.error('Lỗi khi huấn luyện model:', err);
      if (err.response && err.response.data && err.response.data.error) {
        setError(`Lỗi: ${err.response.data.error}`);
      } else {
        setError('Lỗi kết nối đến máy chủ. Vui lòng thử lại sau.');
      }
    } finally {
      setIsTraining(false);
    }
  };

  // Xử lý chuyển đổi tab
  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };
  
  // Xử lý chuyển đổi tab lịch sử
  const handleHistoryTabChange = (event, newValue) => {
    setHistoryTab(newValue);
  };

  // Thêm hàm xử lý phát/dừng audio source UVR
  const handlePlayUvrSourceAudio = () => {
    if (!uvrFile) {
      setError('Không có file âm thanh để phát');
      return;
    }
    
    if (isUvrSourcePlaying) {
      // Nếu đang phát thì dừng lại
      if (uvrSourceAudioRef.current) {
        uvrSourceAudioRef.current.pause();
        setIsUvrSourcePlaying(false);
      }
    } else {
      // Nếu chưa phát thì tạo và phát
      const fileUrl = URL.createObjectURL(uvrFile);
      const audio = new Audio(fileUrl);
      
      // Lắng nghe sự kiện metadata để lấy thời lượng audio
      audio.onloadedmetadata = () => {
        setUvrSourceDuration(audio.duration);
      };
      
      // Lắng nghe sự kiện timeupdate để cập nhật tiến trình
      audio.ontimeupdate = () => {
        setUvrSourceProgress(audio.currentTime);
      };
      
      // Xử lý sự kiện khi phát xong
      audio.onended = () => {
        setUvrSourceProgress(0);
        setIsUvrSourcePlaying(false);
        uvrSourceAudioRef.current = null;
        URL.revokeObjectURL(fileUrl);
      };
      
      uvrSourceAudioRef.current = audio;
      audio.play()
        .then(() => setIsUvrSourcePlaying(true))
        .catch(error => {
          console.error('Lỗi khi phát âm thanh nguồn UVR:', error);
          setError('Không thể phát âm thanh. Vui lòng thử lại.');
          setIsUvrSourcePlaying(false);
          URL.revokeObjectURL(fileUrl);
        });
    }
  };
  
  // Thêm hàm xử lý khi người dùng tua audio UVR source
  const handleUvrSourceSeek = (event, newValue) => {
    setUvrSourceProgress(newValue);
    if (uvrSourceAudioRef.current) {
      uvrSourceAudioRef.current.currentTime = newValue;
    }
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={activeTab} onChange={handleTabChange} aria-label="RVC tabs">
          <Tab icon={<AudioFileIcon />} label="Chuyển đổi" id="rvc-tab-0" aria-controls="rvc-tabpanel-0" />
          <Tab icon={<FolderZipIcon />} label="Batch" id="rvc-tab-1" aria-controls="rvc-tabpanel-1" />
          <Tab icon={<MicOffIcon />} label="Tách giọng" id="rvc-tab-2" aria-controls="rvc-tabpanel-2" />
          <Tab icon={<BuildIcon />} label="Huấn luyện" id="rvc-tab-3" aria-controls="rvc-tabpanel-3" />
          <Tab icon={<DeviceHubIcon />} label="Tools" id="rvc-tab-4" aria-controls="rvc-tabpanel-4" />
          <Tab icon={<HistoryIcon />} label="Lịch sử" id="rvc-tab-5" aria-controls="rvc-tabpanel-5" />
        </Tabs>
      </Box>
      
      {/* Tab Chuyển đổi đơn lẻ */}
      <TabPanel value={activeTab} index={0}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
                Chọn file và mô hình
          </Typography>
          
              <Grid container spacing={2} sx={{ mb: 3 }}>
                <Grid item xs={12}>
              <Button
                variant="outlined"
                component="label"
                startIcon={<CloudUploadIcon />}
                fullWidth
                sx={{ height: '56px' }}
              >
                Chọn file âm thanh
                <input
                  type="file"
                  accept="audio/*"
                  hidden
                  onChange={handleFileChange}
                />
              </Button>
            </Grid>
                <Grid item xs={12}>
              <Paper variant="outlined" sx={{ p: 1, display: 'flex', alignItems: 'center', height: '56px' }}>
                {audioFile ? (
                  <>
                    <AudioFileIcon color="primary" sx={{ mx: 1 }} />
                    <Typography variant="body2" sx={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                      {audioFile.name}
                    </Typography>
                    <IconButton 
                      onClick={handlePlaySourceAudio}
                      disabled={!audioPreviewUrl}
                      color="primary"
                    >
                      {isSourcePlaying ? <StopIcon /> : <PlayCircleOutlineIcon />}
                    </IconButton>
                  </>
                ) : (
                  <Typography variant="body2" color="textSecondary" sx={{ mx: 1 }}>
                    Chưa chọn file nào
                  </Typography>
                )}
              </Paper>
            </Grid>
          </Grid>
          
          <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Mô hình giọng nói</InputLabel>
            <Select
              value={selectedVoice}
              onChange={handleVoiceChange}
                  disabled={isModelLoading}
                  label="Mô hình giọng nói"
            >
                  {isModelLoading ? (
                <MenuItem value="">Đang tải...</MenuItem>
              ) : (
                availableVoices.map((voice) => (
                  <MenuItem key={voice} value={voice}>
                    {voice}
                  </MenuItem>
                ))
              )}
            </Select>
          </FormControl>

              <Typography variant="subtitle1" gutterBottom sx={{ mt: 3 }}>
                Nguồn index
              </Typography>
              
              <TextField
                fullWidth
                label="Đường dẫn index tùy chỉnh"
                variant="outlined"
                value={indexInputPath}
                onChange={(e) => setIndexInputPath(e.target.value)}
                placeholder="Để trống để sử dụng index tự động"
                margin="normal"
                size="small"
              />
              
              <FormControl fullWidth sx={{ mt: 1 }}>
                <InputLabel>Index tự động</InputLabel>
                <Select
                  value={selectedIndex}
                  onChange={handleIndexChange}
                  disabled={isModelLoading || indexInputPath !== ''}
                  label="Index tự động"
                  size="small"
                >
                  {indexPaths.map((path) => (
                    <MenuItem key={path} value={path}>
                      {path.split('/').pop()}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Cài đặt chuyển đổi
              </Typography>
          
          {/* Điều chỉnh Pitch (f0up_key) */}
          <Typography gutterBottom>
                Điều chỉnh độ cao (F0 Up Key)
          </Typography>
          <Grid container spacing={2} alignItems="center">
            <Grid item xs>
              <Slider
                value={f0UpKey}
                onChange={(e, newValue) => setF0UpKey(newValue)}
                min={-12}
                max={12}
                step={1}
                marks
                valueLabelDisplay="auto"
              />
            </Grid>
                <Grid item xs={2}>
                  <Typography variant="body2" align="center">
                {f0UpKey > 0 ? `+${f0UpKey}` : f0UpKey}
              </Typography>
            </Grid>
          </Grid>
          
              {/* F0 Method */}
              <FormControl fullWidth sx={{ mt: 3, mb: 2 }}>
                <InputLabel>Phương pháp F0</InputLabel>
                <Select
                  value={f0Method}
                  onChange={(e) => setF0Method(e.target.value)}
                  label="Phương pháp F0"
              size="small"
            >
                  <MenuItem value="pm">PM (Nhanh)</MenuItem>
                  <MenuItem value="harvest">Harvest (Chất lượng cao)</MenuItem>
                  <MenuItem value="crepe">Crepe (GPU)</MenuItem>
                  <MenuItem value="rmvpe">RMVPE (Tốt nhất)</MenuItem>
                </Select>
              </FormControl>
                
                {/* Index Rate */}
                <Typography variant="body2" gutterBottom>
                  Tỷ lệ áp dụng index (Index Rate)
                </Typography>
                <Grid container spacing={2} alignItems="center">
                  <Grid item xs>
                    <Slider
                      value={indexRate}
                      onChange={(e, newValue) => setIndexRate(newValue)}
                      min={0}
                      max={1}
                      step={0.01}
                      valueLabelDisplay="auto"
                    />
                  </Grid>
                <Grid item xs={2}>
                  <Typography variant="body2" align="center">
                      {indexRate.toFixed(2)}
                    </Typography>
                  </Grid>
                </Grid>
                
                {/* Protect */}
              <Typography variant="body2" gutterBottom sx={{ mt: 2 }}>
                Bảo vệ phụ âm (Protect)
                </Typography>
                <Grid container spacing={2} alignItems="center">
                  <Grid item xs>
                    <Slider
                      value={protectValue}
                      onChange={(e, newValue) => setProtectValue(newValue)}
                      min={0}
                      max={0.5}
                      step={0.01}
                      valueLabelDisplay="auto"
                    />
                  </Grid>
                <Grid item xs={2}>
                  <Typography variant="body2" align="center">
                      {protectValue.toFixed(2)}
                    </Typography>
                  </Grid>
                </Grid>
                
                {/* RMS Mix Rate */}
              <Typography variant="body2" gutterBottom sx={{ mt: 2 }}>
                  Tỷ lệ trộn RMS
                </Typography>
                <Grid container spacing={2} alignItems="center">
                  <Grid item xs>
                    <Slider
                      value={rmsRate}
                      onChange={(e, newValue) => setRmsRate(newValue)}
                      min={0}
                      max={1}
                      step={0.01}
                      valueLabelDisplay="auto"
                    />
                  </Grid>
                <Grid item xs={2}>
                  <Typography variant="body2" align="center">
                      {rmsRate.toFixed(2)}
                    </Typography>
                  </Grid>
                </Grid>
              
              {/* Filter Radius */}
              <Typography variant="body2" gutterBottom sx={{ mt: 2 }}>
                Bán kính lọc (Filter Radius)
              </Typography>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs>
                  <Slider
                    value={filterRadius}
                    onChange={(e, newValue) => setFilterRadius(newValue)}
                    min={0}
                    max={7}
                    step={1}
                    marks
                    valueLabelDisplay="auto"
                  />
                </Grid>
                <Grid item xs={2}>
                  <Typography variant="body2" align="center">
                    {filterRadius}
                  </Typography>
                </Grid>
              </Grid>
              
              {/* Resample SR */}
              <Typography variant="body2" gutterBottom sx={{ mt: 2 }}>
                Tái lấy mẫu SR (0 = không tái lấy mẫu)
              </Typography>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs>
                  <Slider
                    value={resampleRate}
                    onChange={(e, newValue) => setResampleRate(newValue)}
                    min={0}
                    max={48000}
                    step={100}
                    valueLabelDisplay="auto"
                  />
                </Grid>
                <Grid item xs={2}>
                  <Typography variant="body2" align="center">
                    {resampleRate}
                  </Typography>
                </Grid>
              </Grid>
          
          {/* Nút chuyển đổi */}
          <Button
            variant="contained"
            fullWidth
                sx={{ mt: 3 }}
            onClick={handleConvert}
                disabled={isConverting || !audioFile || !selectedVoice}
          >
                {isConverting ? (
              <>
                <CircularProgress size={24} sx={{ mr: 1 }} color="inherit" />
                Đang xử lý...
              </>
            ) : (
              'Chuyển đổi giọng nói'
            )}
          </Button>
            </Paper>
          </Grid>
        </Grid>
          
          {/* Kết quả */}
          {result && (
          <Paper elevation={2} sx={{ p: 2, mt: 3 }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
              <Typography variant="h6">
                Kết quả chuyển đổi
                </Typography>
                
                <Box>
                  <IconButton color="primary" onClick={handlePlayResultAudio}>
                    {isResultPlaying ? <StopIcon /> : <VolumeUpIcon />}
                  </IconButton>
                  
                  <IconButton color="primary" onClick={() => handleDownload(result.result_url)}>
                    <DownloadIcon />
                  </IconButton>
                </Box>
              </Box>
              
            {/* Thêm thanh tua cho audio kết quả */}
            {audioDuration > 0 && (
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Typography variant="body2" sx={{ minWidth: '70px' }}>
                  {Math.floor(audioProgress / 60)}:{Math.floor(audioProgress % 60).toString().padStart(2, '0')} / 
                  {Math.floor(audioDuration / 60)}:{Math.floor(audioDuration % 60).toString().padStart(2, '0')}
                </Typography>
                <Box sx={{ flex: 1, mx: 2 }}>
                  <Slider
                    size="small"
                    value={audioProgress}
                    max={audioDuration || 100}
                    onChange={handleAudioSeek}
                    aria-label="Vị trí audio"
                  />
                </Box>
              </Box>
            )}
            
            <Divider sx={{ mb: 2 }} />
            
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography variant="body2">
                  <strong>Mô hình:</strong> {result.target_voice}
                </Typography>
                <Typography variant="body2">
                  <strong>Phương pháp F0:</strong> {f0Method}
                </Typography>
                <Typography variant="body2">
                  <strong>Điều chỉnh pitch:</strong> {f0UpKey > 0 ? `+${f0UpKey}` : f0UpKey}
                </Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                    <Typography variant="body2">
                      <strong>Index Rate:</strong> {indexRate.toFixed(2)}
                    </Typography>
                    <Typography variant="body2">
                      <strong>Protect:</strong> {protectValue.toFixed(2)}
                    </Typography>
                    <Typography variant="body2">
                      <strong>RMS Mix Rate:</strong> {rmsRate.toFixed(2)}
                    </Typography>
              </Grid>
            </Grid>
          </Paper>
                )}
      </TabPanel>

      {/* Tab Batch processing */}
      <TabPanel value={activeTab} index={1}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Thư mục đầu vào/đầu ra
              </Typography>
              
              <TextField
                fullWidth
                label="Thư mục đầu vào"
                variant="outlined"
                value={batchInputDir}
                onChange={(e) => setBatchInputDir(e.target.value)}
                placeholder="Ví dụ: C:\\Users\\Desktop\\input_vocal_dir"
                margin="normal"
              />
              
              <TextField
                fullWidth
                label="Thư mục đầu ra"
                variant="outlined"
                value={batchOutputDir}
                onChange={(e) => setBatchOutputDir(e.target.value)}
                placeholder="Ví dụ: opt"
                margin="normal"
              />
              
              <FormControl fullWidth sx={{ mt: 2 }}>
                <InputLabel>Định dạng xuất</InputLabel>
                <Select
                  value={batchFormats}
                  onChange={(e) => setBatchFormats(e.target.value)}
                  label="Định dạng xuất"
                >
                  <MenuItem value="wav">WAV</MenuItem>
                  <MenuItem value="mp3">MP3</MenuItem>
                  <MenuItem value="flac">FLAC</MenuItem>
                  <MenuItem value="m4a">M4A</MenuItem>
                </Select>
              </FormControl>
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Cài đặt chuyển đổi
              </Typography>
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Mô hình giọng nói</InputLabel>
                <Select
                  value={selectedVoice}
                  onChange={handleVoiceChange}
                  disabled={isModelLoading}
                  label="Mô hình giọng nói"
                >
                  {isModelLoading ? (
                    <MenuItem value="">Đang tải...</MenuItem>
                  ) : (
                    availableVoices.map((voice) => (
                      <MenuItem key={voice} value={voice}>
                        {voice}
                      </MenuItem>
                    ))
                  )}
                </Select>
              </FormControl>
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Phương pháp F0</InputLabel>
                <Select
                  value={f0Method}
                  onChange={(e) => setF0Method(e.target.value)}
                  label="Phương pháp F0"
                >
                  <MenuItem value="pm">PM (Nhanh)</MenuItem>
                  <MenuItem value="harvest">Harvest (Chất lượng cao)</MenuItem>
                  <MenuItem value="crepe">Crepe (GPU)</MenuItem>
                  <MenuItem value="rmvpe">RMVPE (Tốt nhất)</MenuItem>
                </Select>
              </FormControl>
              
              {/* Điều chỉnh Pitch (f0up_key) */}
              <Typography gutterBottom>
                Điều chỉnh độ cao (F0 Up Key)
              </Typography>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs>
                  <Slider
                    value={f0UpKey}
                    onChange={(e, newValue) => setF0UpKey(newValue)}
                    min={-12}
                    max={12}
                    step={1}
                    marks
                    valueLabelDisplay="auto"
                  />
                </Grid>
                <Grid item xs={2}>
                  <Typography variant="body2" align="center">
                    {f0UpKey > 0 ? `+${f0UpKey}` : f0UpKey}
                  </Typography>
                </Grid>
              </Grid>
              
              {/* Index selection */}
              <Typography variant="subtitle1" gutterBottom sx={{ mt: 3 }}>
                Nguồn index
              </Typography>
              
              <TextField
                fullWidth
                label="Đường dẫn index tùy chỉnh"
                variant="outlined"
                value={indexInputPath}
                onChange={(e) => setIndexInputPath(e.target.value)}
                placeholder="Để trống để sử dụng index tự động"
                margin="normal"
                size="small"
              />
              
              <FormControl fullWidth sx={{ mt: 1 }}>
                <InputLabel>Index tự động</InputLabel>
                <Select
                  value={selectedIndex}
                  onChange={handleIndexChange}
                  disabled={isModelLoading || indexInputPath !== ''}
                  label="Index tự động"
                  size="small"
                >
                  {indexPaths.map((path) => (
                    <MenuItem key={path} value={path}>
                      {path.split('/').pop()}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
              
              {/* Index Rate */}
              <Typography variant="body2" gutterBottom sx={{ mt: 2 }}>
                Tỷ lệ áp dụng index
              </Typography>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs>
                  <Slider
                    value={indexRate}
                    onChange={(e, newValue) => setIndexRate(newValue)}
                    min={0}
                    max={1}
                    step={0.01}
                    valueLabelDisplay="auto"
                  />
                </Grid>
                <Grid item xs={2}>
                  <Typography variant="body2" align="center">
                    {indexRate.toFixed(2)}
                  </Typography>
                </Grid>
              </Grid>
              
              {/* Protect */}
              <Typography variant="body2" gutterBottom sx={{ mt: 2 }}>
                Bảo vệ phụ âm
              </Typography>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs>
                  <Slider
                    value={protectValue}
                    onChange={(e, newValue) => setProtectValue(newValue)}
                    min={0}
                    max={0.5}
                    step={0.01}
                    valueLabelDisplay="auto"
                  />
                </Grid>
                <Grid item xs={2}>
                  <Typography variant="body2" align="center">
                    {protectValue.toFixed(2)}
                  </Typography>
                </Grid>
              </Grid>
              
              {/* Nút xử lý hàng loạt */}
              <Button
                variant="contained"
                fullWidth
                sx={{ mt: 3 }}
                onClick={handleBatchConvert}
                disabled={isBatchProcessing || !batchInputDir || !selectedVoice}
              >
                {isBatchProcessing ? (
                  <>
                    <CircularProgress size={24} sx={{ mr: 1 }} color="inherit" />
                    Đang xử lý...
                  </>
                ) : (
                  'Xử lý hàng loạt'
                )}
              </Button>
            </Paper>
          </Grid>
        </Grid>
        
        {/* Kết quả xử lý hàng loạt */}
        {batchResult && (
          <Paper elevation={2} sx={{ p: 2, mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Kết quả xử lý hàng loạt
            </Typography>
            
            <Box sx={{ mt: 2 }}>
              <Typography variant="body1">
                Đã xử lý {batchResult.processed_files} file.
              </Typography>
              <Typography variant="body1">
                Thư mục đầu ra: {batchResult.output_dir}
              </Typography>
              </Box>
            
            {batchResult.files && batchResult.files.length > 0 && (
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle1" gutterBottom>
                  Danh sách file đã xử lý:
                </Typography>
                <ul>
                  {batchResult.files.slice(0, 10).map((file, index) => (
                    <li key={index}>{file}</li>
                  ))}
                  {batchResult.files.length > 10 && (
                    <li>...và {batchResult.files.length - 10} file khác</li>
                  )}
                </ul>
              </Box>
            )}
            </Paper>
          )}
        </TabPanel>
        
      {/* Tab Tách giọng */}
      <TabPanel value={activeTab} index={2}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Tách giọng nói và nhạc nền (UVR5)
              </Typography>
              
              <Grid container spacing={2} sx={{ mt: 1, mb: 2 }}>
                <Grid item xs={12}>
                  <Button
                    variant="outlined"
                    component="label"
                    startIcon={<CloudUploadIcon />}
                    fullWidth
                    sx={{ height: '56px' }}
                  >
                    Chọn file âm thanh
                    <input
                      type="file"
                      accept="audio/*"
                      hidden
                      onChange={handleUvrFileChange}
                    />
                  </Button>
                </Grid>
                <Grid item xs={12}>
                  <Paper variant="outlined" sx={{ p: 1, display: 'flex', alignItems: 'center', height: '56px' }}>
                    {uvrFile ? (
                      <>
                        <AudioFileIcon color="primary" sx={{ mx: 1 }} />
                        <Typography variant="body2" sx={{ flex: 1, overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                          {uvrFile.name}
                        </Typography>
                        <IconButton 
                          onClick={handlePlayUvrSourceAudio}
                          color="primary"
                        >
                          {isUvrSourcePlaying ? <StopIcon /> : <PlayCircleOutlineIcon />}
                        </IconButton>
                      </>
                    ) : (
                      <Typography variant="body2" color="textSecondary" sx={{ mx: 1 }}>
                        Chưa chọn file nào
                      </Typography>
                    )}
                  </Paper>
                </Grid>
              </Grid>
              
              {/* Thêm thanh tua cho file âm thanh UVR nguồn */}
              {uvrSourceDuration > 0 && (
                <Box sx={{ display: 'flex', alignItems: 'center', mt: 1, mb: 2, px: 1 }}>
                  <Typography variant="body2" sx={{ minWidth: '70px' }}>
                    {Math.floor(uvrSourceProgress / 60)}:{Math.floor(uvrSourceProgress % 60).toString().padStart(2, '0')} / 
                    {Math.floor(uvrSourceDuration / 60)}:{Math.floor(uvrSourceDuration % 60).toString().padStart(2, '0')}
                  </Typography>
                  <Box sx={{ flex: 1, mx: 2 }}>
                    <Slider
                      size="small"
                      value={uvrSourceProgress}
                      max={uvrSourceDuration || 100}
                      onChange={handleUvrSourceSeek}
                      aria-label="Vị trí file nguồn"
                    />
                  </Box>
                </Box>
              )}
              
              <FormControl fullWidth sx={{ mb: 2 }}>
                <InputLabel>Mô hình UVR</InputLabel>
                <Select
                  value={selectedUvrModel}
                  onChange={(e) => setSelectedUvrModel(e.target.value)}
                  label="Mô hình UVR"
                >
                  {uvrModels.length > 0 ? (
                    uvrModels.map((model) => (
                      <MenuItem key={model} value={model}>
                        {uvrModelDisplayName(model)}
                      </MenuItem>
                    ))
                  ) : (
                    <MenuItem value="">
                      <em>Không có mô hình UVR5 nào</em>
                    </MenuItem>
                  )}
                </Select>
              </FormControl>
              
              <Button
                variant="contained"
                fullWidth
                sx={{ mt: 3 }}
                onClick={handleSeparateVocals}
                disabled={isUvrProcessing || !uvrFile || !selectedUvrModel}
              >
                {isUvrProcessing ? (
                  <>
                    <CircularProgress size={24} sx={{ mr: 1 }} color="inherit" />
                    Đang xử lý...
                  </>
                ) : (
                  'Tách giọng nói'
                )}
              </Button>
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={6}>
            {/* Kết quả UVR */}
            {uvrResult ? (
              <Paper elevation={2} sx={{ p: 2 }}>
                <Typography variant="h6" gutterBottom>
                  Kết quả tách giọng nói
                </Typography>
                
                {uvrResult.vocals_url && (
                  <Box sx={{ mt: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', p: 1, bgcolor: 'background.paper', borderRadius: 1 }}>
                      <Typography>
                        <strong>Giọng nói (Vocals)</strong>
                      </Typography>
                      
                      <Box>
                        <IconButton color="primary" onClick={handlePlayVocals} sx={{ mr: 1 }}>
                          {isVocalsPlaying ? <StopIcon /> : <PlayCircleOutlineIcon />}
                        </IconButton>
                        <IconButton color="primary" onClick={() => handleDownload(uvrResult.vocals_url)}>
                          <DownloadIcon />
                        </IconButton>
                      </Box>
                    </Box>
                    
                    {/* Thanh tua cho vocals */}
                    {vocalsDuration > 0 && (
                      <Box sx={{ display: 'flex', alignItems: 'center', mt: 1, mb: 2, px: 1 }}>
                        <Typography variant="body2" sx={{ minWidth: '70px' }}>
                          {Math.floor(vocalsProgress / 60)}:{Math.floor(vocalsProgress % 60).toString().padStart(2, '0')} / 
                          {Math.floor(vocalsDuration / 60)}:{Math.floor(vocalsDuration % 60).toString().padStart(2, '0')}
                        </Typography>
                        <Box sx={{ flex: 1, mx: 2 }}>
                          <Slider
                            size="small"
                            value={vocalsProgress}
                            max={vocalsDuration || 100}
                            onChange={handleVocalsSeek}
                            aria-label="Vị trí vocals"
                          />
                        </Box>
                      </Box>
                    )}
                  </Box>
                )}
                
                {uvrResult.instrumental_url && (
                  <Box sx={{ mt: 2 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', p: 1, bgcolor: 'background.paper', borderRadius: 1 }}>
                      <Typography>
                        <strong>Nhạc nền (Instrumental)</strong>
                      </Typography>
                      
                      <Box>
                        <IconButton color="primary" onClick={handlePlayInstrumental} sx={{ mr: 1 }}>
                          {isInstrumentalPlaying ? <StopIcon /> : <PlayCircleOutlineIcon />}
                        </IconButton>
                        <IconButton color="primary" onClick={() => handleDownload(uvrResult.instrumental_url)}>
                          <DownloadIcon />
                        </IconButton>
                      </Box>
                    </Box>
                    
                    {/* Thanh tua cho instrumental */}
                    {instrumentalDuration > 0 && (
                      <Box sx={{ display: 'flex', alignItems: 'center', mt: 1, mb: 2, px: 1 }}>
                        <Typography variant="body2" sx={{ minWidth: '70px' }}>
                          {Math.floor(instrumentalProgress / 60)}:{Math.floor(instrumentalProgress % 60).toString().padStart(2, '0')} / 
                          {Math.floor(instrumentalDuration / 60)}:{Math.floor(instrumentalDuration % 60).toString().padStart(2, '0')}
                        </Typography>
                        <Box sx={{ flex: 1, mx: 2 }}>
                          <Slider
                            size="small"
                            value={instrumentalProgress}
                            max={instrumentalDuration || 100}
                            onChange={handleInstrumentalSeek}
                            aria-label="Vị trí instrumental"
                          />
                        </Box>
                      </Box>
                    )}
                  </Box>
                )}
              </Paper>
            ) : (
              <Paper elevation={2} sx={{ p: 2, height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'center', alignItems: 'center' }}>
                <Typography variant="body1" color="textSecondary" align="center">
                  Chọn file âm thanh và mô hình UVR để tách giọng nói và nhạc nền
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <Alert severity="info" sx={{ mb: 2 }}>
                    <Typography variant="body2">
                      <strong>Mẹo:</strong> Các mô hình UVR khác nhau sẽ cho kết quả khác nhau. Mô hình HP5 tốt cho giọng nói chính, HP2/HP3 tốt cho giọng nói không có hòa âm. Vậy nên bạn có thể sử dụng 1 file audio và dùng nhiều model để tách được nhạc và lời mong muốn
                    </Typography>
                  </Alert>
                </Box>
              </Paper>
            )}
          </Grid>
        </Grid>
        </TabPanel>
        
      {/* Tab Huấn luyện */}
      <TabPanel value={activeTab} index={3}>
        <Paper elevation={2} sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
            Huấn luyện mô hình RVC mới
          </Typography>
          
          <Alert severity="info" sx={{ mb: 3 }}>
            Huấn luyện mô hình mới cần nhiều tài nguyên GPU và thời gian. Đảm bảo bạn có đủ không gian đĩa và card đồ họa phù hợp.
          </Alert>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" gutterBottom>
                Cấu hình thí nghiệm
              </Typography>
              
              <TextField
                fullWidth
                label="Tên thí nghiệm"
                variant="outlined"
                value={experimentName}
                onChange={(e) => setExperimentName(e.target.value)}
                placeholder="Ví dụ: mi-test"
                margin="normal"
                required
              />
              
              <TextField
                fullWidth
                label="Thư mục dữ liệu huấn luyện"
                variant="outlined"
                value={trainsetDir}
                onChange={(e) => setTrainsetDir(e.target.value)}
                placeholder="Ví dụ: E:\\audio_data\\source"
                margin="normal"
                required
              />
              
              <Grid container spacing={2} sx={{ mt: 1 }}>
                <Grid item xs={6}>
                  <FormControl fullWidth>
                    <InputLabel>Tần số lấy mẫu (SR)</InputLabel>
                    <Select
                      value={targetSR}
                      onChange={(e) => setTargetSR(e.target.value)}
                      label="Tần số lấy mẫu (SR)"
                    >
                      <MenuItem value="32k">32kHz</MenuItem>
                      <MenuItem value="40k">40kHz</MenuItem>
                      <MenuItem value="48k">48kHz</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                
                <Grid item xs={6}>
                  <FormControl fullWidth>
                    <InputLabel>Speaker ID</InputLabel>
                    <Select
                      value={speakerId}
                      onChange={(e) => setSpeakerId(e.target.value)}
                      label="Speaker ID"
                    >
                      {[0, 1, 2, 3, 4].map((id) => (
                        <MenuItem key={id} value={id}>{id}</MenuItem>
                      ))}
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>
              
              <FormControlLabel
                control={
                  <Switch 
                    checked={ifF0} 
                    onChange={(e) => setIfF0(e.target.checked)}
                />
                }
                label="Sử dụng F0 (cần thiết cho hát)"
                sx={{ mt: 2 }}
              />
            </Grid>
            
            <Grid item xs={12} md={6}>
              <Typography variant="subtitle1" gutterBottom>
                Cài đặt huấn luyện
                    </Typography>
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Batch Size"
                    type="number"
                    variant="outlined"
                    value={batchSize}
                    onChange={(e) => setBatchSize(parseInt(e.target.value))}
                    margin="normal"
                    InputProps={{ inputProps: { min: 1, max: 32 } }}
                  />
                </Grid>
                
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="GPU IDs"
                    variant="outlined"
                    value={gpuIds}
                    onChange={(e) => setGpuIds(e.target.value)}
                    placeholder="Ví dụ: 0-1-2"
                    margin="normal"
                  />
                </Grid>
              </Grid>
              
              <Grid container spacing={2}>
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Tổng số epoch"
                    type="number"
                    variant="outlined"
                    value={totalEpochs}
                    onChange={(e) => setTotalEpochs(parseInt(e.target.value))}
                    margin="normal"
                    InputProps={{ inputProps: { min: 2, max: 1000 } }}
                  />
                </Grid>
                
                <Grid item xs={6}>
                  <TextField
                    fullWidth
                    label="Lưu mỗi (epoch)"
                    type="number"
                    variant="outlined"
                    value={saveEpochs}
                    onChange={(e) => setSaveEpochs(parseInt(e.target.value))}
                    margin="normal"
                    InputProps={{ inputProps: { min: 1, max: 100 } }}
                  />
                </Grid>
              </Grid>
              
              <FormControlLabel
                control={
                  <Switch 
                    checked={pretrained} 
                    onChange={(e) => setPretrained(e.target.checked)}
                  />
                }
                label="Sử dụng mô hình pretrained"
                sx={{ mt: 2 }}
              />
              
              {pretrained && (
                <>
                  <TextField
                    fullWidth
                    label="Đường dẫn pretrained G"
                    variant="outlined"
                    value={pretrainedG}
                    onChange={(e) => setPretrainedG(e.target.value)}
                    placeholder="Ví dụ: assets/pretrained_v2/f0G40k.pth"
                    margin="normal"
                    size="small"
                  />
                  
                  <TextField
                    fullWidth
                    label="Đường dẫn pretrained D"
                    variant="outlined"
                    value={pretrainedD}
                    onChange={(e) => setPretrainedD(e.target.value)}
                    placeholder="Ví dụ: assets/pretrained_v2/f0D40k.pth"
                    margin="normal"
                    size="small"
                  />
                </>
              )}
            </Grid>
          </Grid>
          
          <Divider sx={{ my: 3 }} />
          
          <Grid container spacing={2}>
            <Grid item xs={4}>
              <Button
                variant="contained"
                fullWidth
                startIcon={<BuildIcon />}
                onClick={() => {/* Xử lý dữ liệu */}}
                disabled={isTraining || !experimentName || !trainsetDir}
              >
                Xử lý dữ liệu
              </Button>
            </Grid>
          
            <Grid item xs={4}>
          <Button
            variant="contained"
            fullWidth
                startIcon={<TuneIcon />}
                onClick={() => {/* Trích xuất đặc trưng */}}
                disabled={isTraining || !experimentName || !trainsetDir}
              >
                Trích xuất đặc trưng
              </Button>
            </Grid>
            
            <Grid item xs={4}>
              <Button
                variant="contained"
                fullWidth
                color="primary"
                startIcon={<PlayCircleOutlineIcon />}
                onClick={handleTrainModel}
                disabled={isTraining || !experimentName || !trainsetDir}
          >
                {isTraining ? (
              <>
                <CircularProgress size={24} sx={{ mr: 1 }} color="inherit" />
                    Đang huấn luyện...
              </>
            ) : (
                  'Huấn luyện mô hình'
            )}
          </Button>
            </Grid>
          </Grid>
            </Paper>
        </TabPanel>
        
      {/* Tab Tools */}
      <TabPanel value={activeTab} index={4}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2 }}>
          <Typography variant="h6" gutterBottom>
                Fusion mô hình
          </Typography>
          
          <Alert severity="info" sx={{ mb: 2 }}>
                Kết hợp hai mô hình RVC để tạo ra mô hình với giọng nói kết hợp.
          </Alert>
          
              <Grid container spacing={2}>
            <Grid item xs={12} md={6}>
                  <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>Mô hình A</InputLabel>
                    <Select
                      value={selectedVoice} // Sử dụng shared state cho demo
                      onChange={handleVoiceChange}
                      label="Mô hình A"
                    >
                      {availableVoices.map((voice) => (
                        <MenuItem key={voice} value={voice}>
                          {voice}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
            </Grid>
                
            <Grid item xs={12} md={6}>
                  <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel>Mô hình B</InputLabel>
                    <Select
                      // value và onChange handler thực tế sẽ khác
                      value=""
                      label="Mô hình B"
                    >
                      {availableVoices.map((voice) => (
                        <MenuItem key={voice} value={voice}>
                          {voice}
                        </MenuItem>
                      ))}
                    </Select>
                  </FormControl>
            </Grid>
          </Grid>
          
              <Typography gutterBottom>
                Tỷ lệ kết hợp (Alpha A)
              </Typography>
              <Grid container spacing={2} alignItems="center">
                <Grid item xs>
                  <Slider
                    defaultValue={0.5}
                    min={0}
                    max={1}
                    step={0.01}
                    valueLabelDisplay="auto"
                  />
                </Grid>
                <Grid item xs={2}>
                  <Typography variant="body2" align="center">
                    0.50
                  </Typography>
                </Grid>
              </Grid>
              
              <TextField
                fullWidth
                label="Tên mô hình mới"
                variant="outlined"
                placeholder="Nhập tên cho mô hình mới"
                margin="normal"
              />
              
          <Button
            variant="contained"
            fullWidth
                startIcon={<DeviceHubIcon />}
            sx={{ mt: 2 }}
              >
                Kết hợp mô hình
          </Button>
            </Paper>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Paper elevation={2} sx={{ p: 2 }}>
              <Typography variant="h6" gutterBottom>
                Trích xuất mô hình nhỏ (weights)
              </Typography>
              
              <Alert severity="info" sx={{ mb: 2 }}>
                Trích xuất mô hình nhỏ từ checkpoint đã huấn luyện để sử dụng trong inference.
                </Alert>
                
              <TextField
                fullWidth
                label="Đường dẫn checkpoint"
                variant="outlined"
                placeholder="Ví dụ: logs/mi-test/G_32000.pth"
                margin="normal"
              />
              
              <TextField
                fullWidth
                label="Tên mô hình mới"
                variant="outlined"
                placeholder="Tên file lưu"
                margin="normal"
              />
              
              <Grid container spacing={2} sx={{ mt: 1 }}>
                <Grid item xs={6}>
                  <FormControl fullWidth>
                    <InputLabel>Tần số lấy mẫu (SR)</InputLabel>
                    <Select
                      value={targetSR}
                      onChange={(e) => setTargetSR(e.target.value)}
                      label="Tần số lấy mẫu (SR)"
                    >
                      <MenuItem value="32k">32kHz</MenuItem>
                      <MenuItem value="40k">40kHz</MenuItem>
                      <MenuItem value="48k">48kHz</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
                
                <Grid item xs={6}>
                  <FormControlLabel
                    control={
                      <Switch 
                        checked={ifF0} 
                        onChange={(e) => setIfF0(e.target.checked)}
                      />
                    }
                    label="Sử dụng F0"
                  />
                </Grid>
              </Grid>
              
              <TextField
                fullWidth
                label="Thông tin mô hình"
                variant="outlined"
                multiline
                rows={4}
                placeholder="Nhập thông tin về mô hình"
                margin="normal"
              />
              
              <Button
                variant="contained"
                fullWidth
                startIcon={<SaveIcon />}
                sx={{ mt: 2 }}
              >
                Trích xuất mô hình
              </Button>
            </Paper>
          </Grid>
        </Grid>
        </TabPanel>
        
      {/* Tab Lịch sử */}
      <TabPanel value={activeTab} index={5}>
        <Box>
          <Typography variant="h6" gutterBottom>
            Lịch sử chuyển đổi RVC và tách giọng nói UVR
          </Typography>
          
          <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
            <Tabs value={historyTab} onChange={handleHistoryTabChange}>
              <Tab label="Lịch sử chuyển đổi RVC" />
              <Tab label="Lịch sử tách giọng UVR" />
            </Tabs>
          </Box>
          
          <Box sx={{ mt: 2 }}>
            {historyTab === 0 && (
              <Paper elevation={2} sx={{ p: 2 }}>
                <RVCConversionHistory />
              </Paper>
            )}
            
            {historyTab === 1 && (
              <Paper elevation={2} sx={{ p: 2 }}>
                <UVRHistory />
              </Paper>
            )}
          </Box>
        </Box>
      </TabPanel>
    </Box>
  );
};

export default RVCTab; 