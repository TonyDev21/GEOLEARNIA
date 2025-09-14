# 🎓 GEOLEARNIA - Sistema Educativo de IA

[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.20.0-orange.svg)](https://tensorflow.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8.1-green.svg)](https://opencv.org/)
[![Flask](https://img.shields.io/badge/Flask-2.3.3-lightgrey.svg)](https://flask.palletsprojects.com/)

## 📋 Descripción

**GEOLEARNIA** es un sistema educativo de inteligencia artificial que combina:

- 🔐 **Sistema de Autenticación Biométrica**: Login tradicional y reconocimiento facial
- 🔺 **Clasificación de Figuras Geométricas**: Reconocimiento en tiempo real usando CNN

## 🏗️ Arquitectura del Proyecto

```
GEOLEARNIA/
├── 📁 OpenCV/                    # Módulo de Autenticación
│   ├── 📁 forms/                 # Interfaces gráficas
│   ├── 📁 persistence/           # Modelos y repositorios
│   ├── 📁 Reconocimiento/        # Sistema facial
│   ├── 📁 util/                  # Utilidades
│   ├── 📁 db/                    # Base de datos SQLite
│   └── main.py                   # Punto de entrada
│
├── 📁 Proyecto_SI/               # Módulo de IA
│   ├── 📁 dataset/               # Imágenes de entrenamiento
│   ├── 📁 templates/             # Templates HTML
│   ├── 📁 static/                # CSS y recursos
│   ├── 📁 Audios/                # Feedback de audio
│   ├── web.py                    # Aplicación Flask
│   ├── Video2.py                 # App de escritorio
│   ├── IA.py                     # Detección clásica
│   ├── ModeloConvolucional.py    # Entrenamiento CNN
│   └── FigurasGeometricas.h5     # Modelo entrenado
│
├── requirements.txt              # Dependencias
├── setup.py                      # Script de instalación
└── README.md                     # Esta documentación
```

## 🚀 Instalación Rápida

### Prerrequisitos

- **Python 3.12+** instalado
- **Cámara web** (para funciones de video)
- **Ubuntu/Linux** (recomendado) o Windows con WSL

### 🔧 Instalación Automática

```bash
# 1. Clonar el repositorio
git clone https://github.com/tu-usuario/geolearnia.git
cd geolearnia

# 2. Ejecutar script de instalación
chmod +x setup.py
python setup.py

# 3. ¡Listo! Ejecutar aplicación
python run.py
```

### 🛠️ Instalación Manual

#### Paso 1: Preparar el entorno

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/geolearnia.git
cd geolearnia

# Crear entorno virtual
python3 -m venv .venv

# Activar entorno virtual
# En Linux/Mac:
source .venv/bin/activate
# En Windows:
.venv\Scripts\activate
```

#### Paso 2: Instalar dependencias del sistema

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install -y python3-tk python3-dev python3-pip
sudo apt install -y libopencv-dev python3-opencv
```

**CentOS/RHEL/Fedora:**
```bash
sudo dnf install -y tkinter python3-devel python3-pip
sudo dnf install -y opencv opencv-python
```

**macOS:**
```bash
brew install python-tk opencv
```

**Windows:**
```bash
# Instalar desde Microsoft Store: Python 3.12
# No requiere dependencias adicionales
```

#### Paso 3: Instalar dependencias Python

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias
pip install -r requirements.txt
```

#### Paso 4: Configurar base de datos

```bash
cd OpenCV
python build_db.py
cd ..
```

#### Paso 5: Verificar instalación

```bash
# Verificar módulo de IA
cd Proyecto_SI
python verificar_proyecto.py

# Verificar módulo de autenticación
cd ../OpenCV
python verificar_opencv.py
```

## 🎮 Uso del Sistema

### 🌐 Aplicación Web (Recomendado)

```bash
cd Proyecto_SI
python web.py
```

Abrir navegador en: **http://127.0.0.1:5001**

- Muestra video en tiempo real
- Clasifica figuras geométricas automáticamente
- Interfaz web responsive

### 🖥️ Aplicación de Escritorio

```bash
cd Proyecto_SI
python Video2.py
```

- Interfaz Tkinter nativa
- Botones de control
- Predicción en tiempo real

### 🔐 Sistema de Autenticación

```bash
cd OpenCV
python main.py
```

**Funciones disponibles:**
- Login tradicional (usuario/contraseña)
- Login facial biométrico
- Registro de nuevos usuarios
- Encriptación de contraseñas

### 🔍 Reconocimiento Facial Avanzado

```bash
cd OpenCV/Reconocimiento
python open.py
```

- Registro facial con MTCNN
- Comparación biométrica ORB
- Malla facial MediaPipe

## 📊 Especificaciones Técnicas

### 🧠 Modelo de IA

- **Arquitectura**: CNN (Convolutional Neural Network)
- **Capas**: 4 Conv2D + MaxPooling + Dense
- **Clases**: Círculo, Cuadrado, Triángulo
- **Tamaño entrada**: 200x200x3
- **Precisión**: ~95% en dataset de prueba

### 🛡️ Seguridad

- **Encriptación**: Fernet (cryptography)
- **Base de datos**: SQLite con ORM SQLAlchemy
- **Autenticación**: Doble factor (tradicional + biométrico)

### 🎥 Procesamiento de Video

- **OpenCV**: 4.8.1.78
- **Resolución**: Adaptable (recomendado 640x480)
- **FPS**: ~30fps en hardware moderno
- **Formatos**: Cámara web, archivos de video

## 🔧 Configuración Avanzada

### Variables de Entorno

Crear archivo `.env`:

```env
# Configuración de base de datos
DATABASE_URL=sqlite:///db/login.sqlite

# Configuración de cámara
CAMERA_INDEX=0
VIDEO_WIDTH=640
VIDEO_HEIGHT=480

# Configuración Flask
FLASK_PORT=5001
FLASK_DEBUG=True

# Clave de encriptación (generar nueva en producción)
ENCRYPTION_KEY=FINEHtwMUOxgvyYM9fOvpXcQHYDDZKb3-NkPWTrZN5g=
```

### Configuración de Cámara

Si tienes problemas con la cámara, edita los archivos:

```python
# En web.py, Video2.py, IA.py
cap = cv2.VideoCapture(0)  # Cambiar 0 por 1, 2, etc.
```

### Entrenamiento Personalizado

Para entrenar con tu propio dataset:

```bash
cd Proyecto_SI

# 1. Organizar imágenes en:
# dataset/
#   ├── circulo/
#   ├── cuadrado/
#   └── triangulo/

# 2. Entrenar modelo
python ModeloConvolucional.py

# 3. El nuevo modelo se guardará como FigurasGeometricas1.h5
# Renombrar a FigurasGeometricas.h5
```

## 🐛 Solución de Problemas

### Problemas Comunes

#### ❌ "No module named 'tkinter'"
**Solución:**
```bash
sudo apt install python3-tk  # Ubuntu/Debian
sudo dnf install tkinter      # Fedora/CentOS
```

#### ❌ "Can't open camera by index"
**Solución:**
```bash
# Verificar cámaras disponibles
ls /dev/video*

# Cambiar índice en el código
cap = cv2.VideoCapture(1)  # Probar 0, 1, 2...
```

#### ❌ "Port 5000 is in use"
**Solución:**
```bash
# Matar proceso en puerto 5000
sudo lsof -ti:5000 | xargs sudo kill -9

# O usar puerto diferente (ya configurado en 5001)
```

#### ❌ "TensorFlow errors"
**Solución:**
```bash
# Reinstalar TensorFlow
pip uninstall tensorflow
pip install tensorflow==2.20.0

# Para CPU solamente:
pip install tensorflow-cpu
```

#### ❌ "CUDA errors" (Opcional)
**Información:** Los errores CUDA son normales si no tienes GPU NVIDIA. El sistema funcionará con CPU.

### Logs y Debugging

```bash
# Habilitar logs detallados
export TF_CPP_MIN_LOG_LEVEL=0

# Verificar instalación
python -c "import tensorflow as tf; print(tf.__version__)"
python -c "import cv2; print(cv2.__version__)"
```

## 🧪 Testing

```bash
# Ejecutar tests del módulo IA
cd Proyecto_SI
python verificar_proyecto.py

# Ejecutar tests del módulo OpenCV
cd OpenCV
python verificar_opencv.py

# Test de cámara
python -c "import cv2; cap=cv2.VideoCapture(0); print('Camera OK' if cap.read()[0] else 'Camera Error')"
```

## 📈 Performance

### Requisitos Mínimos

- **CPU**: 2 núcleos, 2.0 GHz
- **RAM**: 4 GB
- **Almacenamiento**: 2 GB libres
- **Cámara**: 640x480 mínimo

### Requisitos Recomendados

- **CPU**: 4 núcleos, 3.0 GHz
- **RAM**: 8 GB
- **GPU**: NVIDIA GTX 1050+ (opcional)
- **Cámara**: 1080p

### Optimización

```python
# Para mejorar performance en web.py
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = False
```

## 🤝 Contribuir

### Estructura de Commits

```
feat: nueva funcionalidad
fix: corrección de bugs
docs: documentación
style: formato de código
refactor: refactorización
test: tests
chore: mantenimiento
```

### Pull Requests

1. Fork del repositorio
2. Crear rama feature: `git checkout -b feature/nueva-funcionalidad`
3. Commit cambios: `git commit -m 'feat: agregar nueva funcionalidad'`
4. Push a la rama: `git push origin feature/nueva-funcionalidad`
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para detalles.

## 👥 Autores

- **Desarrollador Original** - *Trabajo inicial*
- **Mantenimiento** - *GitHub Copilot & Tony*

## 🙏 Agradecimientos

- TensorFlow team por el framework de ML
- OpenCV community por las herramientas de CV
- Flask team por el framework web
- SQLAlchemy por el ORM

## 📞 Soporte

- 📧 **Email**: soporte@geolearnia.com
- 🐛 **Issues**: [GitHub Issues](https://github.com/tu-usuario/geolearnia/issues)
- 📖 **Wiki**: [Documentación completa](https://github.com/tu-usuario/geolearnia/wiki)

---

⭐ **¡No olvides dar una estrella al proyecto si te fue útil!** ⭐
