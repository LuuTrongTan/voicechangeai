import axios from 'axios';

// Cấu hình Axios
const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  timeout: 300000, // 5 phút timeout cho các tác vụ xử lý dài
  headers: {
    'Content-Type': 'application/json'
  }
});

// Thêm interceptor để xử lý lỗi
API.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

// API Functions
export const VoiceAPI = {
  // Lấy danh sách các mô hình và giọng nói
  getModels: () => API.get('/api/models'),
  
  // Chuyển đổi giọng nói
  convertVoice: (formData) => {
    return API.post('/api/convert', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },

  // Kiểm tra trạng thái máy chủ
  checkHealth: () => API.get('/api/health'),
  
  // Download file kết quả
  downloadResult: (resultUrl) => {
    // Đảm bảo dùng URL đầy đủ của backend
    const fullUrl = resultUrl.startsWith('http') ? 
      resultUrl : 
      `${API.defaults.baseURL}${resultUrl}`;
    window.open(fullUrl, '_blank');
    return true;
  },
  
  // Phát file âm thanh
  playAudioFile: (audioPath) => {
    // Nếu đường dẫn là URL đầy đủ
    if (audioPath.startsWith('http')) {
      window.open(audioPath, '_blank');
      return true;
    }
    
    // Nếu là đường dẫn tương đối hoặc đường dẫn máy chủ
    const encodedPath = encodeURIComponent(audioPath);
    // Sử dụng URL đầy đủ của backend thay vì đường dẫn tương đối
    window.open(`${API.defaults.baseURL}/api/play-audio?path=${encodedPath}`, '_blank');
    return true;
  },
  
  // Lấy thông tin chi tiết về file giọng nói
  getVoiceDetails: (audioPath) => {
    const encodedPath = encodeURIComponent(audioPath);
    return API.get(`/api/voice-details?path=${encodedPath}`);
  },
  
  // Lấy lịch sử chuyển đổi
  getConversionHistory: (modelType = 'openvoice') => API.get(`/api/conversion-history?model_type=${modelType}`),
  
  // Lấy lịch sử tách giọng nói UVR
  getUvrHistory: () => API.get('/api/uvr-history'),
  
  // Theo dõi tiến trình xử lý (polling)
  getProgress: (jobId) => API.get(`/api/progress/${jobId}`),
  
  // So sánh nhiều giọng nói
  compareVoices: (formData) => {
    return API.post('/api/compare', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  
  // Text-to-Speech APIs
  // Lấy danh sách speakers TTS
  getTtsSpeakers: () => API.get('/api/tts/speakers'),
  
  // Tạo âm thanh từ văn bản
  generateTts: (data) => API.post('/api/tts/generate', data),
  
  // Lấy lịch sử TTS
  getTtsHistory: () => API.get('/api/tts-history'),
  
  // RVC APIs
  rvc: {
    // Lấy danh sách mô hình RVC
    getModels: () => API.get('/api/rvc/models'),
    
    // Lấy chi tiết về một mô hình
    getModelInfo: (modelName) => API.get(`/api/rvc/model-info?model=${modelName}`),
    
    // Chuyển đổi giọng nói đơn lẻ
    convertSingle: (formData) => {
      return API.post('/api/rvc/convert', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    },
    
    // Chuyển đổi hàng loạt
    convertBatch: (data) => API.post('/api/rvc/convert-batch', data),
    
    // Tách giọng nói khỏi âm nhạc (UVR5)
    separateVocals: (audioFile, modelName) => {
      const formData = new FormData();
      formData.append('audio', audioFile);
      formData.append('model', modelName);
      
      return API.post('/api/rvc/separate-vocals', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    },
    
    // Lấy lịch sử chuyển đổi giọng nói RVC
    getConversionHistory: () => API.get('/api/conversion-history?model_type=rvc'),
    
    // Lấy lịch sử tách giọng nói UVR
    getUvrHistory: () => API.get('/api/uvr-history'),
    
    // Trích xuất đường cong F0
    extractF0: (audioFile, f0Method = 'rmvpe') => {
      const formData = new FormData();
      formData.append('audio', audioFile);
      formData.append('f0_method', f0Method);
      
      return API.post('/api/rvc/extract-f0', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    },
    
    // Huấn luyện model
    trainModel: (data) => API.post('/api/rvc/train', data),
    
    // Tiền xử lý dataset
    preprocessDataset: (data) => API.post('/api/rvc/preprocess', data),
    
    // Trích xuất đặc trưng
    extractFeatures: (data) => API.post('/api/rvc/extract-features', data),
    
    // Xây dựng index feature
    buildIndex: (expDir) => API.post('/api/rvc/build-index', { exp_dir: expDir }),
    
    // Fusion (kết hợp) hai mô hình
    fusionModels: (modelA, modelB, alpha, targetName) => {
      return API.post('/api/rvc/fusion', {
        model_a: modelA,
        model_b: modelB,
        alpha,
        target_name: targetName
      });
    },
    
    // Trích xuất mô hình nhỏ từ checkpoint
    extractSmallModel: (ckptPath, saveName, sr, ifF0, info) => {
      return API.post('/api/rvc/extract-small-model', {
        ckpt_path: ckptPath,
        save_name: saveName,
        sr,
        if_f0: ifF0,
        info
      });
    },
    
    // Thay đổi thông tin mô hình
    changeModelInfo: (modelPath, info, saveName) => {
      return API.post('/api/rvc/change-info', {
        model_path: modelPath,
        info,
        save_name: saveName
      });
    },
    
    // Hiển thị thông tin mô hình
    showModelInfo: (modelPath) => {
      return API.get(`/api/rvc/show-info?model_path=${encodeURIComponent(modelPath)}`);
    },
    
    // Lấy trạng thái huấn luyện
    getTrainingStatus: (expDir) => {
      return API.get(`/api/rvc/training-status?exp_dir=${encodeURIComponent(expDir)}`);
    },
    
    // Xuất mô hình sang ONNX
    exportOnnx: (modelPath, outputPath) => {
      return API.post('/api/rvc/export-onnx', {
        model_path: modelPath,
        output_path: outputPath
      });
    }
  }
};

export const adminService = {
  // Lấy thống kê tổng quan
  getStats: () => API.get('/api/admin/stats').then(response => response.data),
  
  // Lấy danh sách người dùng
  getUsers: () => API.get('/api/admin/users').then(response => response.data),
  
  // Lấy logs hệ thống
  getLogs: (filters = {}) => {
    const { level, source, start_date, end_date, limit } = filters;
    let url = '/api/admin/logs?';
    
    if (level) url += `level=${level}&`;
    if (source) url += `source=${source}&`;
    if (start_date) url += `start_date=${start_date}&`;
    if (end_date) url += `end_date=${end_date}&`;
    if (limit) url += `limit=${limit}&`;
    
    return API.get(url).then(response => {
      // Kiểm tra và xử lý dữ liệu an toàn
      if (!response.data) {
        console.warn('Không có dữ liệu logs từ API');
        return [];
      }
      
      // Trả về mảng nếu response.data là mảng
      if (Array.isArray(response.data)) {
        return response.data;
      } 
      // Trả về mảng logs nếu response.data.logs là mảng
      else if (response.data && Array.isArray(response.data.logs)) {
        return response.data.logs;
      } 
      // Trường hợp có lỗi, trả về mảng rỗng
      else {
        console.error('Dữ liệu logs không phải là mảng:', response.data);
        return [];
      }
    }).catch(error => {
      console.error('Lỗi khi lấy logs:', error);
      return [];
    });
  },
  
  // Lấy thông tin hiệu suất hệ thống (APM)
  getSystemPerformance: () => API.get('/api/admin/system-performance').then(response => response.data),
  
  // Lấy thông tin database
  getDatabaseInfo: () => API.get('/api/admin/database-info').then(response => response.data),
  
  // Phân tích lỗi
  analyzeErrors: () => API.get('/api/admin/error-analysis').then(response => response.data),
  
  // Lấy nội dung file log trực tiếp
  getLogFile: (type = 'app', lines = 100) => {
    return API.get(`/api/admin/log-file?type=${type}&lines=${lines}`).then(response => {
      // Đảm bảo trả về mảng
      if (response.data && Array.isArray(response.data.log_content)) {
        return { log_content: response.data.log_content };
      } else if (response.data && typeof response.data.log_content === 'string') {
        return { log_content: response.data.log_content.split('\n') };
      } else {
        console.error('Dữ liệu log_content không hợp lệ:', response.data);
        return { log_content: [] };
      }
    }).catch(error => {
      console.error('Lỗi khi lấy log file:', error);
      return { log_content: [] };
    });
  }
};

export const aiEngineerService = {
  // Lấy danh sách models
  getModels: () => API.get('/api/ai-engineer/models'),
  
  // Lấy danh sách trainings
  getTrainings: () => API.get('/api/ai-engineer/trainings'),
  
  // Upload model mới
  uploadModel: (file, type, name, description) => {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);
    formData.append('name', name);
    formData.append('description', description);
    
    return API.post('/api/ai-engineer/models/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    });
  },
  
  // Bắt đầu training model
  startTraining: (modelName, modelType) => API.post('/api/ai-engineer/training/start', {
    model_name: modelName,
    model_type: modelType
  })
};

export default API; 