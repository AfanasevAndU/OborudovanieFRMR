import React, { useState } from 'react';
import { Box, Typography, FormControl, InputLabel, Select, MenuItem, Button, LinearProgress } from '@mui/material';
import { useDropzone } from 'react-dropzone';

const FileUploader = () => {
  const [headerOption, setHeaderOption] = useState('Первая строка');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFile = async (file) => {
    if (!file) return;
    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);
    formData.append('header_option', headerOption);

    try {
      const response = await fetch('http://localhost:8000/analyze', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || 'Ошибка анализа файла.');
      }

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'И11_оборудование.xlsx';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    handleFile(file);
  };

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        handleFile(acceptedFiles[0]);
      }
    },
    accept: '.xlsx',
    multiple: false,
  });

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h6" gutterBottom>
        Выберите файл для анализа
      </Typography>

      <FormControl fullWidth sx={{ mb: 2 }}>
        <InputLabel id="header-option-label">Строка заголовков</InputLabel>
        <Select
          labelId="header-option-label"
          value={headerOption}
          onChange={(e) => setHeaderOption(e.target.value)}
          label="Строка заголовков"
        >
          <MenuItem value="Первая строка">Первая строка</MenuItem>
          <MenuItem value="Шестая строка">Шестая строка</MenuItem>
        </Select>
      </FormControl>

      {/* Область drag & drop */}
      <Box
        {...getRootProps()}
        sx={{
          border: '2px dashed #ccc',
          borderRadius: '4px',
          padding: '20px',
          textAlign: 'center',
          cursor: 'pointer',
          mb: 2,
        }}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <Typography>Отпустите файл для загрузки</Typography>
        ) : (
          <Typography>Перетащите файл</Typography>
        )}
      </Box>

      <Button
        variant="contained"
        component="label"
        fullWidth
        disabled={loading}
        sx={{ mb: 2 }}
      >
        Загрузить файл
        <input type="file" accept=".xlsx" hidden onChange={handleFileUpload} />
      </Button>

      {loading && <LinearProgress />}
      {error && (
        <Typography variant="body1" color="error" sx={{ mt: 2 }}>
          Ошибка: {error}
        </Typography>
      )}
    </Box>
  );
};

export default FileUploader;
