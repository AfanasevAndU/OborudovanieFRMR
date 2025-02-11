const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let fastApiProcess;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            nodeIntegration: true,
        },
    });

    // Загрузите React-приложение
    mainWindow.loadURL('http://localhost:3000'); // Для разработки
    // Для продакшена: mainWindow.loadFile(path.join(__dirname, 'build/index.html'));

    // Откройте DevTools (опционально)
    mainWindow.webContents.openDevTools();

    mainWindow.on('closed', () => {
        mainWindow = null;
    });
}

function startFastApiServer() {
    const pythonPath = 'python3'; // Используйте python3 на macOS/Linux
    const serverPath = path.join(__dirname, '..', 'server', 'dist', 'app'); // Путь к app.py

    const fastApiProcess = spawn(pythonPath, ['-m', 'uvicorn', 'app:app', '--host', '0.0.0.0', '--port', '8000'], {
        shell: true,
        cwd: path.join(__dirname, '..', 'server'), // Установите рабочую директорию
    });

    fastApiProcess.stdout.on('data', (data) => {
        console.log(`[FastAPI] ${data.toString()}`);
    });

    fastApiProcess.stderr.on('data', (data) => {
        console.error(`[FastAPI Error] ${data.toString()}`);
    });

    fastApiProcess.on('close', (code) => {
        console.log(`[FastAPI] Process exited with code ${code}`);
    });
}

app.whenReady().then(() => {
    createWindow();
    startFastApiServer();

    app.on('activate', () => {
        if (BrowserWindow.getAllWindows().length === 0) {
            createWindow();
        }
    });
});

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('quit', () => {
    if (fastApiProcess) {
        fastApiProcess.kill(); // Остановить FastAPI при выходе
    }
});