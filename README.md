# 🎯 GEOLEARNIA

[![Python 3.13+](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20.0-orange.svg)](https://tensorflow.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.12.0-green.svg)](https://opencv.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-lightgrey.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Sistema Educativo de Inteligencia Artificial** para reconocimiento de figuras geométricas en tiempo real con sistema de puntero central optimizado.

## 🚀 Inicio Rápido

```bash
# 1. Clonar repositorio
git clone https://github.com/TonyDev21/GEOLEARNIA.git
cd GEOLEARNIA

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar aplicación principal
cd Proyecto_SI
python run_pointer.py
```

**¡Listo!** 🎉 Abre tu navegador en `http://127.0.0.1:5002`

## ✨ Características Principales

### 🎯 Sistema de Puntero Central
- **Detección Precisa**: Área específica de análisis en el centro de la pantalla
- **Cruz de Referencia**: Guía visual amarilla para posicionamiento
- **Rectángulo de Detección**: Zona delimitada de 250x250 píxeles
- **Contorno Verde**: Visualización del objeto detectado
- **Punto Central**: Indicador rojo del centro del objeto

### 🔺 Reconocimiento de Figuras IA
- **Modelo CNN**: Red neuronal convolucional entrenada
- **3 Figuras**: Círculos, cuadrados/rectángulos y triángulos
- **Tiempo Real**: Streaming de video con Flask
- **Alta Precisión**: Detección optimizada solo en zona central
- **Confianza**: Porcentaje de certeza en cada predicción

### 🔐 Sistema de Autenticación (Módulo Adicional)
- **Login Biométrico**: Reconocimiento facial con OpenCV
- **Login Tradicional**: Usuario y contraseña
- **Base de Datos**: SQLite con encriptación

## 📱 Uso de la Aplicación

### 🎯 Aplicación Principal - Puntero Central
```bash
cd Proyecto_SI
python run_pointer.py
```
- Abre: `http://127.0.0.1:5002`
- **Instrucciones**:
  1. 📍 Coloca el objeto en la cruz amarilla central
  2. 📦 Asegúrate de que esté dentro del rectángulo azul
  3. ⏳ Espera la detección automática
  4. ✅ Ve el resultado con porcentaje de confianza

### 🖥️ Aplicación de Escritorio (OpenCV)
```bash
cd OpenCV
python main.py
```

### 🔐 Sistema de Autenticación
```bash
cd OpenCV
python build_db.py  # Crear base de datos
python main.py      # Iniciar aplicación con login
```

## 🛠️ Requisitos del Sistema

### 📋 Prerequisitos
- **Python**: 3.13 o superior
- **Cámara web**: Para captura de video
- **Sistema Operativo**: Windows, macOS, Linux

### 📦 Dependencias Principales
| Librería | Versión | Propósito |
|----------|---------|-----------|
| TensorFlow | 2.20.0 | Modelo de IA |
| OpenCV | 4.12.0 | Procesamiento de video |
| Flask | 3.1.2 | Servidor web |
| NumPy | Latest | Operaciones numéricas |

## 🏗️ Estructura del Proyecto

```
GEOLEARNIA/
├── 📁 Proyecto_SI/              # 🎯 Aplicación Principal
│   ├── web_pointer.py           # Servidor Flask con puntero central
│   ├── run_pointer.py           # Script de ejecución
│   ├── FigurasGeometricas.h5    # Modelo CNN entrenado
│   ├── templates/               # Templates HTML
│   │   └── pointer.html         # Interfaz principal
│   └── static/css/              # Estilos CSS
│       └── styles.css           # Estilos de la aplicación
├── 📁 OpenCV/                   # 🔐 Sistema de Autenticación
│   ├── main.py                  # Aplicación principal con login
│   ├── build_db.py              # Creador de base de datos
│   └── forms/                   # Formularios GUI
└── 📄 requirements.txt          # Dependencias
```

## 🎯 Objetos Detectables

| Figura | Ejemplos | Consejos |
|--------|----------|----------|
| 🔴 **Círculo** | Monedas, tapas, discos | Usar objetos con borde definido |
| 🟦 **Cuadrado** | Libros, cajas, tarjetas | Colocar en posición plana |
| 🔺 **Triángulo** | Reglas, objetos triangulares | Asegurar visibilidad completa |

## 📖 Guías Adicionales

- 🛠️ **[Troubleshooting](TROUBLESHOOTING.md)** - Solución de problemas
- 🤝 **[Contribuir](CONTRIBUTING.md)** - Guía para desarrolladores
- 📝 **[Changelog](CHANGELOG.md)** - Historial de versiones
- 📚 **[Documentación Técnica](README_GITHUB.md)** - Detalles avanzados

## 🔄 Contribuir y Actualizar

### 📥 Para Desarrolladores
```bash
# 1. Fork del repositorio
git clone https://github.com/TU_USUARIO/GEOLEARNIA.git

# 2. Crear rama de desarrollo
git checkout -b feature/nueva-funcionalidad

# 3. Realizar cambios y commit
git add .
git commit -m "Descripción de cambios"

# 4. Push y crear Pull Request
git push origin feature/nueva-funcionalidad
```

### 🔄 Actualizar Repositorio
```bash
# Desde tu fork local
git remote add upstream https://github.com/TonyDev21/GEOLEARNIA.git
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
```

## 🆘 Solución de Problemas Comunes

### ❌ Error de Cámara
```bash
# Verificar cámara disponible
python -c "import cv2; print('Cámara OK' if cv2.VideoCapture(0).read()[0] else 'Sin cámara')"
```

### ❌ Error de Modelo
```bash
# Verificar modelo TensorFlow
cd Proyecto_SI
python -c "import tensorflow as tf; print('Modelo OK' if tf.keras.models.load_model('FigurasGeometricas.h5') else 'Error modelo')"
```

### ❌ Error de Puerto
- Si el puerto 5002 está ocupado, cambiar en `web_pointer.py` línea final
- Alternativamente usar: `python run_pointer.py --port 5003`

## 📞 Soporte

- 🐛 **Issues**: [GitHub Issues](https://github.com/TonyDev21/GEOLEARNIA/issues)
- 📧 **Contacto**: Crear issue en GitHub
- 📚 **Documentación**: Ver archivos en `/docs`

## 📄 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

---

**Desarrollado con ❤️ para la educación y el aprendizaje de IA**