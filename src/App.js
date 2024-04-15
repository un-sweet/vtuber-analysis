import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import StartPage from './components/StartPage';
import Page1 from './components/Page1';
import Page2 from './components/Page2';
import Page3 from './components/Page3';
import { AppBar, Toolbar, Typography, CssBaseline, ThemeProvider, createTheme, Drawer, List, ListItem, ListItemText } from '@mui/material';

const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

const drawerWidth = 240;

function App() {
  return (
    <ThemeProvider theme={darkTheme}>
      <Router>
        <CssBaseline />
        <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
          <Toolbar>
            <Typography variant="h6" noWrap component="div" style={{ width: '100%', whiteSpace: 'nowrap', overflow: 'hidden', color: 'white', textShadow: '0 0 5px #7B22D7, 0 0 10px #7B22D7, 0 0 15px #7B22D7, 0 0 20px #7B22D7' }}>
              <marquee behavior="scroll" direction="left">🌟✨💫 Welcome to PTT VTuber Analysis world💫✨🌟  Here is the magic Data world 💫✨🌟 </marquee>
            </Typography>
          </Toolbar>
        </AppBar>
        <Drawer
          variant="permanent"
          sx={{
            width: drawerWidth,
            '& .MuiDrawer-paper': { width: drawerWidth, boxSizing: 'border-box' },
          }}
        >
          <Toolbar />
          <List>
            <CustomListItem to="/" primary="Welcome" />
            <CustomListItem to="/data1" primary="Hololive" />
            <CustomListItem to="/data2" primary="Nijisanji" />
            <CustomListItem to="/data3" primary="Others" />
          </List>
        </Drawer>
        <main style={{ marginLeft: drawerWidth, padding: '20px', marginTop: '64px' }}>
          <Routes>
            <Route path="/" element={<StartPage />} />
            <Route path="/data1" element={<Page1 />} />
            <Route path="/data2" element={<Page2 />} />
            <Route path="/data3" element={<Page3 />} />
          </Routes>
        </main>
      </Router>
    </ThemeProvider>
  );
}

function CustomListItem({ to, primary, color = '#7B22D7' }) {
  const location = useLocation();
  const isActive = location.pathname === to;

  return (
    <ListItem component="a" href={to} sx={{ color, backgroundColor: isActive ? '#362E38' : 'initial', '&:hover': { backgroundColor: 'gray', color: 'rgba(255, 255, 255, 1)' } }}>
      <ListItemText primary={primary} />
    </ListItem>
  );
}

export default App;