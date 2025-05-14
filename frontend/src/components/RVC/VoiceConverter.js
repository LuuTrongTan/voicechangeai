import React from 'react';
import { 
  Container, Typography, Box, Paper
} from '@mui/material';
import RVCTab from './RVCTab';

/**
 * Component VoiceConverter: Hiển thị giao diện chuyển đổi giọng nói RVC
 * Hiện đang hỗ trợ:
 * - RVC (Retrieval-based Voice Conversion)
 */
const VoiceConverter = () => {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom align="center">
        Chuyển đổi giọng nói
      </Typography>
      
      <Typography variant="subtitle1" align="center" color="textSecondary" sx={{ mb: 4 }}>
        Sử dụng AI để chuyển đổi giọng nói của bạn sang giọng nói khác
      </Typography>
      
      <Paper sx={{ mb: 4 }}>
        <Box sx={{ p: 0 }}>
          <RVCTab />
        </Box>
      </Paper>
      
      <Typography variant="body2" color="textSecondary" sx={{ mt: 2, textAlign: 'center' }}>
        Chú ý: Tất cả các chuyển đổi được xử lý trên máy chủ và có thể mất một khoảng thời gian tùy thuộc vào độ dài của audio.
      </Typography>
    </Container>
  );
};

export default VoiceConverter; 