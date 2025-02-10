import React from 'react';
import { Container, Typography } from '@mui/material';
import FileUploader from './components/FileUploader';

function App() {
  return (
    <Container maxWidth="sm" sx={{ mt: 4, textAlign: 'center' }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Анализ медицинского оборудования
      </Typography>
      <FileUploader />
    </Container>
  );
}

export default App;