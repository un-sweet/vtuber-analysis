import React, { useState } from 'react';
import { Box, Card, CardContent, Typography, CircularProgress, Grid } from '@mui/material';
import niji_freq from '../img/niji_freq.png';
import nijisanji_worldcloud from '../img/nijisanji_worldcloud.png';
import time_freq from '../img/Rplot02.png';

function Page1() {
  const [isHovered1, setIsHovered1] = useState(false);
  const [isHovered2, setIsHovered2] = useState(false);
  const [isHovered3, setIsHovered3] = useState(false);


  // Replace with your actual data and image paths
  const numberData = [
    { title: 'How Many Articles?', value: 2122, color: '#6729E5' },
    { title: 'Average Comments', value:  214, color: '#e56729' },
    { title: 'Average Like', value: 135, color: '#29e567' },
  ];

  const handleMouseEnter1 = () => {
    setIsHovered1(true);
  };

  const handleMouseLeave1 = () => {
    setIsHovered1(false);
  };

  const handleMouseEnter2 = () => {
    setIsHovered2(true);
  };

  const handleMouseLeave2 = () => {
    setIsHovered2(false);
  };

  const handleMouseEnter3 = () => {
    setIsHovered3(true);
  };

  const handleMouseLeave3 = () => {
    setIsHovered3(false);
  };

  const darkOverlayStyle = {
    position: 'absolute',
    top: 0,
    left: 0,
    right: 0,
    bottom: 0,
    backgroundColor: 'rgba(0, 0, 0, 0.5)',
    zIndex: 1,
    transition: 'opacity 0.3s ease',
  };

  return (
    <Box sx={{ flexGrow: 1, color: 'text.primary', bgcolor: 'background.default', p: 3 }}>
      <Grid container spacing={2}>
        {/* Number data with progress bars */}
        {numberData.map((data, index) => (
          <Grid item xs={12} sm={4} key={index}>
            <Card sx={{ textAlign: 'center', bgcolor: 'background.paper' }}>
              <CardContent>
              <Typography variant="h5" gutterBottom sx={{ marginBottom: 2 }}>
                  {data.title}
                </Typography>
                <Box position="relative" display="inline-flex">
                  <CircularProgress
                    variant="determinate"
                    value={100}
                    size={100}
                    thickness={4}
                    sx={{
                        color: data.color,
                        animation: 'kirakira 1s infinite alternate',
                        '@keyframes kirakira': {
                        '0%': { filter: 'hue-rotate(0deg)' },
                        '100%': { filter: 'hue-rotate(360deg)' },
                        },
                    }}
                    />
                  <Box
                    top={0}
                    left={0}
                    bottom={0}
                    right={0}
                    position="absolute"
                    display="flex"
                    alignItems="center"
                    justifyContent="center"
                  >
                    <Typography variant="h5" component="div" color="text.primary">
                      {`${data.value}`}
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}

        <Grid item xs={12} sm={6}>
          <Card sx={{ height: '70%', bgcolor: 'background.paper', display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
            <CardContent style={{ position: 'relative', height: '100%', textAlign: 'center' }}>
              <div
                onMouseEnter={handleMouseEnter1}
                onMouseLeave={handleMouseLeave1}
                style={{ position: 'relative', width: '100%', height: '90%', display: 'flex', justifyContent: 'center', alignItems: 'center' }}
              >
                <img src={nijisanji_worldcloud} alt="Data 1" style={{ maxWidth: '100%', maxHeight: '100%', display: 'block', margin: 'auto' }} />
                <div style={{ ...darkOverlayStyle, opacity: isHovered1 ? 0 : 1 }}></div>
              </div>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={6}>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <Card sx={{ height: '100%', bgcolor: 'background.paper', position: 'relative' }}>
                <CardContent style={{ position: 'relative' }}>
                  <div
                    onMouseEnter={handleMouseEnter2}
                    onMouseLeave={handleMouseLeave2}
                    style={{ position: 'relative', width: '100%', height: '100%' }}
                  >
                    <img src={niji_freq} alt="Data 2" style={{ width: '100%', height: 'auto' }} />
                    <div style={{ ...darkOverlayStyle, opacity: isHovered2 ? 0 : 1 }}></div>
                  </div>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12}>
              <Card sx={{ height: '100%', bgcolor: 'background.paper' }}>
                <CardContent style={{ position: 'relative' }}>
                  <div
                    onMouseEnter={handleMouseEnter3}
                    onMouseLeave={handleMouseLeave3}
                    style={{ position: 'relative', width: '100%', height: '100%' }}
                  >
                    <img src={time_freq} alt="Data 3" style={{ width: '100%', height: 'auto' }} />
                    <div style={{ ...darkOverlayStyle, opacity: isHovered3 ? 0 : 1 }}></div>
                  </div>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Page1;