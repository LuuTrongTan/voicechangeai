import React from 'react';
import { Box, Container, Typography, Link } from '@mui/material';

const Footer = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: (theme) => theme.palette.grey[100]
      }}
    >
      <Container maxWidth="lg">
        <Typography variant="body2" color="text.secondary" align="center">
          © {new Date().getFullYear()} Voice Changer System - Ứng dụng chuyển đổi giọng nói với OpenVoice
        </Typography>
        <Typography variant="body2" color="text.secondary" align="center" sx={{ mt: 1 }}>
          <Link href="https://github.com/myshell-ai/OpenVoice" target="_blank" rel="noopener" color="inherit">
            Powered by OpenVoice
          </Link>
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer; 