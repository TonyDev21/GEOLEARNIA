# 🎯 GEOLEARNIA v3.0

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.17.0-orange.svg)](https://tensorflow.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.10.0-green.svg)](https://opencv.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **🎓 Aplicación Web de IA** para reconocimiento automático de figuras geométricas con **guías visuales en tiempo real**. Funciona en PC, móviles y tablets.

## 🚀 Instalación y Ejecución

### 📥 Descargar
```bash
git clone https://github.com/TonyDev21/GEOLEARNIA.git
cd GEOLEARNIA
```

### 🛠️ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### ▶️ Ejecutar
```bash
python app.py
```

**🌐 Abrir en navegador:** `http://127.0.0.1:5000`

### 🌍 Versión Online
**URL:** https://geolearnia-production.up.railway.app

---

## ✨ Características

- **📱 Reconocimiento Automático:** IA detecta formas cada 1.5 segundos
- **👀 Guías Visuales:** Contornos verdes y etiquetas en tiempo real  
- **🎯 Formas Soportadas:** Círculos, cuadrados y triángulos
- **📲 Multi-dispositivo:** PC, móviles, tablets
- **🎨 Interfaz Limpia:** Solo botón iniciar/detener cámara

## 📋 Requisitos
- **Python 3.9+** 
- **Cámara web** (PC/móvil)
- **Navegador moderno**

## 🏗️ Estructura del Proyecto
```
GEOLEARNIA/
├── app.py                       # Servidor principal
├── Proyecto_SI/
│   ├── web_api.py              # API Flask  
│   ├── FigurasGeometricas.h5   # Modelo IA entrenado
│   ├── templates/
│   │   └── index.html          # Interfaz principal
│   ├── static/
│   │   ├── css/geolearnia.css  # Estilos
│   │   └── js/geolearnia.js    # Funcionalidad
│   └── dataset/                # Datos de entrenamiento
└── requirements.txt            # Dependencias
```

## 📄 Licencia
MIT License - Consulta [LICENSE](LICENSE) para más detalles.

---
**Creado con ❤️ por [TonyDev21](https://github.com/TonyDev21)**