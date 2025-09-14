# Changelog

Todos los cambios notables en este proyecto serán documentados aquí.

El formato está basado en [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
y este proyecto adhiere a [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-09-13

### ✨ Agregado
- Sistema completo de autenticación biométrica
- Clasificación de figuras geométricas con CNN
- Aplicación web Flask con streaming de video
- Aplicación de escritorio con Tkinter
- Base de datos SQLite con encriptación
- Reconocimiento facial con MTCNN
- Detección de contornos clásica con OpenCV
- Scripts de instalación automatizada
- Documentación completa para GitHub
- Sistema de verificación de componentes

### 🛠️ Componentes Principales
- **OpenCV Module**: Sistema de login y reconocimiento facial
- **Proyecto_SI Module**: IA para clasificación de figuras geométricas
- **Web Interface**: Flask app con video streaming
- **Desktop App**: Interfaz Tkinter para clasificación
- **Database**: SQLite con SQLAlchemy ORM
- **Security**: Encriptación Fernet para contraseñas

### 🔧 Técnico
- Python 3.12+ compatible
- TensorFlow 2.20.0 para deep learning
- OpenCV 4.8.1.78 para computer vision
- Flask 2.3.3 para aplicación web
- SQLAlchemy 2.0.23 para base de datos
- Modelo CNN entrenado para 3 clases (círculo, cuadrado, triángulo)

### 📚 Documentación
- README completo con instrucciones de instalación
- Guía de contribución (CONTRIBUTING.md)
- Documentación técnica detallada
- Scripts de verificación automatizada
- Troubleshooting guide

### 🐛 Correcciones
- Error crítico `franem` → `frame` en reconocimiento facial
- Compatibilidad de puertos Flask (5000 → 5001)
- Comentarios mal formateados en código Python
- Dependencias actualizadas a versiones estables

### 📦 Distribución
- Requirements.txt completo y actualizado
- Script setup.py para instalación automatizada
- Script run.py para ejecución sencilla
- .gitignore configurado para el proyecto
- Licencia MIT incluida

### 🔮 Futuras Mejoras Planeadas
- Soporte para más figuras geométricas
- API REST para integración externa
- Dashboard de administración
- Deployment con Docker
- Tests unitarios completos
- CI/CD pipeline

---

## Tipos de Cambios
- `✨ Agregado` para nuevas funcionalidades
- `🔄 Cambiado` para cambios en funcionalidades existentes  
- `🗑️ Obsoleto` para funcionalidades que se eliminarán pronto
- `🐛 Corregido` para corrección de bugs
- `🔒 Seguridad` en caso de vulnerabilidades
