import React from 'react';
import { Container, Typography, Box, Button } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import ErrorOutlineIcon from '@mui/icons-material/ErrorOutline';

const NotFound = () => {
  return (
    <Container maxWidth="sm">
      <Box
        sx={{
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          minHeight: '60vh',
          textAlign: 'center'
        }}
      >
        <ErrorOutlineIcon sx={{ fontSize: 100, color: 'primary.main', mb: 2 }} />
        <Typography variant="h4" gutterBottom>
          Không tìm thấy trang
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Trang bạn đang tìm kiếm không tồn tại hoặc đã bị di chuyển.
        </Typography>
        <Button
          variant="contained"
          component={RouterLink}
          to="/"
          sx={{ mt: 3 }}
        >
          Trở về trang chủ
        </Button>
      </Box>
    </Container>
  );
};

export default NotFound; 