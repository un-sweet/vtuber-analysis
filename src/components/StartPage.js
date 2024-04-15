import React from 'react';
import { Card, CardContent, Typography, Box, CardHeader, useTheme } from '@mui/material';
import { styled, keyframes } from '@mui/system';

// Define keyframes for animation
const pulse = keyframes`
  0% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
  100% {
    transform: scale(1);
  }
`;

// Create a styled Card component with animation
const AnimatedCard = styled(Card)(({ theme }) => ({
  width: '45%',
  height: '68%',
  maxWidth: '100%',
  maxHeight: '100%',
  overflow: 'auto',
  backgroundColor: theme.palette.background.paper,
  borderRadius: '15px',
  borderColor: 'gray', // Change border color to purple
  borderWidth: '4px', // Make border wider
  borderStyle: 'solid',
  animation: `${pulse} 2s infinite`,
  '&:hover': {
    animationPlayState: 'paused', // Pause animation on hover
  },
}));

function StartPage() {
  const theme = useTheme();

  return (
    <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'start', height: '100vh', p: 3, backgroundColor: theme.palette.background.default }}>
      <AnimatedCard elevation={3}>
        <CardHeader
          title="Welcome to the PTT VTuber Analysis"
          // subheader="This is a description of the dashboard."
          titleTypographyProps={{ align: 'center' }}
       
        />
        <CardContent>
  {/* <Typography variant="h5" component="h2" gutterBottom align="center">
    PTT VTuber Analysis
  </Typography> */}
  <Typography color="textSecondary" align="left">
    This analysis focuses on the comments below each post. We will categorize the posts into three groups:
    </Typography>
    <ul>
    <li>Hololive</li>
    <li>Nijisanji</li>
    <li>Others</li>
  </ul>
  <Typography color="textSecondary" align="left">
     The data will be observed:
  </Typography>

  {/* The list of observations */}
  <ul>
    <li>Total number of posts.</li>
    <li>Average number of comments per posts.</li>
    <li>Average number of likes per post.</li>
    <li>Wordcloud of comments.</li>
    <li>Frequency of post appearances on the board.</li>
  </ul>
</CardContent>

      </AnimatedCard>
    </Box>
  );
}

export default StartPage;