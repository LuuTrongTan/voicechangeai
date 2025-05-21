import React from 'react';
import { Link } from 'react-router-dom';
import { AppBar, Toolbar, Button, Box } from '@mui/material';

const Navbar = () => {
  return (
    <AppBar position="static">
      <Toolbar>
        <Box sx={{ flexGrow: 1, display: 'flex', gap: 2 }}>
          <Button color="inherit" component={Link} to="/dashboard">
            OpenVoice
          </Button>
          <Button color="inherit" component={Link} to="/rvc">
            RVC
          </Button>
          <Button color="inherit" component={Link} to="/viettts">
            VietTTS
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar; 