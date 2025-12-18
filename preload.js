const { contextBridge } = require('electron');

// Exponer APIs seguras al renderer process si es necesario
contextBridge.exposeInMainWorld('electron', {
  version: process.versions.electron,
  platform: process.platform
});
