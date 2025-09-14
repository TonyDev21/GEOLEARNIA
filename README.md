# 🎓 GEOLEARNIA

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20.0-orange.svg)](https://tensorflow.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-green.svg)](https://opencv.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-lightgrey.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Sistema Educativo de Inteligencia Artificial** que combina autenticación biométrica y clasificación de figuras geométricas en tiempo real.

## � Inicio Rápido

```bash
# 1. Clonar repositorio
git clone https://github.com/tu-usuario/geolearnia.git
cd geolearnia

# 2. Instalación automática
python setup.py

# 3. Ejecutar aplicación
python run.py
```

**¡Eso es todo!** 🎉

## ✨ Características

### 🔐 Sistema de Autenticación
- **Login Biométrico**: Reconocimiento facial con MTCNN
- **Login Tradicional**: Usuario y contraseña encriptada
- **Registro Dual**: Modalidad facial y tradicional
- **Seguridad**: Encriptación Fernet + SQLite

### 🔺 Clasificación de Figuras IA
- **Reconocimiento CNN**: Círculos, cuadrados y triángulos
- **Tiempo Real**: Video streaming con Flask
- **Múltiples Interfaces**: Web, escritorio y detección clásica
- **Modelo Entrenado**: 95% precisión en dataset de prueba

## � Uso Rápido

### 🌐 Aplicación Web (Recomendado)
```bash
python run.py --web
# Abrir: http://127.0.0.1:5001
```

### 🖥️ Aplicación de Escritorio
```bash
python run.py --desktop
```

### 🔐 Sistema de Autenticación
```bash
python run.py --auth
```

## 📖 Documentación Completa

- 📚 **[Guía Técnica Detallada](README_GITHUB.md)** - Instalación completa y uso avanzado
- 🛠️ **[Troubleshooting](TROUBLESHOOTING.md)** - Solución de problemas comunes
- 🤝 **[Contribuir](CONTRIBUTING.md)** - Guía para desarrolladores
- � **[Changelog](CHANGELOG.md)** - Historial de cambios

## 🛠️ Tecnologías Principales

| Componente | Tecnología | Versión |
|-----------|------------|---------|
| **IA/ML** | TensorFlow | 2.20.0 |
| **Computer Vision** | OpenCV | 4.8.1 |
| **Web Framework** | Flask | 2.3.3 |
| **Database** | SQLite + SQLAlchemy | 2.0.23 |

**Ver [documentación técnica completa](README_GITHUB.md) para más detalles**
