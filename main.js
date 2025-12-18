const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { spawn } = require('child_process');

let mainWindow;
let flaskProcess;
const FLASK_PORT = 5000;

function findPythonCommand() {
  const fs = require('fs');
  
  // 1. Buscar Python embebido en la app empaquetada
  const embeddedPython = path.join(process.resourcesPath, 'app.asar.unpacked', 'python-embed', 'python.exe');
  if (fs.existsSync(embeddedPython)) {
    console.log('✅ Usando Python embebido:', embeddedPython);
    return embeddedPython;
  }
  
  // 2. Buscar Python embebido en desarrollo
  const devEmbeddedPython = path.join(__dirname, 'python-embed', 'python.exe');
  if (fs.existsSync(devEmbeddedPython)) {
    console.log('✅ Usando Python embebido (dev):', devEmbeddedPython);
    return devEmbeddedPython;
  }
  
  // 3. Buscar el ejecutable de Python en el entorno virtual
  const venvPath = path.join(__dirname, '.venv', 'Scripts', 'python.exe');
  if (fs.existsSync(venvPath)) {
    console.log('✅ Usando Python del venv:', venvPath);
    return venvPath;
  }
  
  // 4. Fallback a Python global
  console.log('⚠️ Usando Python del sistema');
  return process.platform === 'win32' ? 'python' : 'python3';
}

function startFlaskServer() {
  return new Promise((resolve, reject) => {
    const fs = require('fs');
    const pythonCmd = findPythonCommand();
    
    // Buscar app.py en app.asar.unpacked primero
    let appPath = path.join(process.resourcesPath, 'app.asar.unpacked', 'app.py');
    if (!fs.existsSync(appPath)) {
      // Si no existe, buscar en __dirname (desarrollo)
      appPath = path.join(__dirname, 'app.py');
    }
    
    // Obtener el directorio de trabajo (donde están los archivos de Proyecto_SI)
    let workDir = path.dirname(appPath);
    
    console.log('🚀 Iniciando servidor Flask...');
    console.log('Python:', pythonCmd);
    console.log('App:', appPath);
    console.log('Work Dir:', workDir);
    
    flaskProcess = spawn(pythonCmd, [appPath], {
      cwd: workDir,
      env: { ...process.env, PORT: FLASK_PORT.toString() }
    });

    flaskProcess.stdout.on('data', (data) => {
      console.log(`Flask: ${data}`);
      if (data.toString().includes('Running on')) {
        resolve();
      }
    });

    flaskProcess.stderr.on('data', (data) => {
      console.error(`Flask Error: ${data}`);
    });

    flaskProcess.on('error', (error) => {
      console.error('Error iniciando Flask:', error);
      reject(error);
    });

    flaskProcess.on('close', (code) => {
      console.log(`Servidor Flask cerrado con código ${code}`);
    });

    // Esperar a que Flask esté realmente listo
    const http = require('http');
    let attempts = 0;
    const maxAttempts = 60; // 60 segundos máximo
    
    const checkFlask = setInterval(() => {
      attempts++;
      http.get(`http://127.0.0.1:${FLASK_PORT}`, (res) => {
        if (res.statusCode === 200) {
          console.log('✅ Flask está listo!');
          clearInterval(checkFlask);
          resolve();
        }
      }).on('error', () => {
        if (attempts >= maxAttempts) {
          console.log('⏱️ Timeout esperando Flask, continuando de todas formas...');
          clearInterval(checkFlask);
          resolve();
        } else {
          console.log(`⏳ Esperando Flask... (${attempts}/${maxAttempts})`);
        }
      });
    }, 1000);
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    minWidth: 800,
    minHeight: 600,
    icon: path.join(__dirname, 'Proyecto_SI', 'static', 'icon.png'),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    },
    autoHideMenuBar: true,
    backgroundColor: '#667eea'
  });

  // Cargar página de carga mientras Flask inicia
  const loadingPage = path.join(__dirname, 'loading.html');
  mainWindow.loadFile(loadingPage);

  // Abrir DevTools en desarrollo
  if (process.env.NODE_ENV === 'development') {
    mainWindow.webContents.openDevTools();
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // Manejar links externos
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    require('electron').shell.openExternal(url);
    return { action: 'deny' };
  });
}

app.whenReady().then(async () => {
  try {
    await startFlaskServer();
    createWindow();
  } catch (error) {
    console.error('Error al iniciar la aplicación:', error);
    app.quit();
  }

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

app.on('before-quit', () => {
  if (flaskProcess) {
    console.log('🛑 Deteniendo servidor Flask...');
    flaskProcess.kill();
  }
});

// Manejar cierre inesperado
process.on('SIGINT', () => {
  if (flaskProcess) {
    flaskProcess.kill();
  }
  app.quit();
});

process.on('SIGTERM', () => {
  if (flaskProcess) {
    flaskProcess.kill();
  }
  app.quit();
});
