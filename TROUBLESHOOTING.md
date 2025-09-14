# 🛠️ Guía de Solución de Problemas - GEOLEARNIA

Esta guía te ayudará a resolver los problemas más comunes al instalar y ejecutar GEOLEARNIA.

## 📋 Índice

- [Problemas de Instalación](#problemas-de-instalación)
- [Problemas de Cámara](#problemas-de-cámara)
- [Problemas de TensorFlow](#problemas-de-tensorflow)
- [Problemas de Interfaz Gráfica](#problemas-de-interfaz-gráfica)
- [Problemas de Base de Datos](#problemas-de-base-de-datos)
- [Problemas de Red](#problemas-de-red)
- [Problemas de Performance](#problemas-de-performance)

---

## 🔧 Problemas de Instalación

### ❌ "No module named 'tkinter'"

**Síntoma:**
```
ModuleNotFoundError: No module named 'tkinter'
```

**Solución:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3-tk

# Fedora/CentOS/RHEL
sudo dnf install tkinter

# macOS
brew install python-tk

# Windows
# Tkinter viene incluido con Python desde python.org
```

### ❌ "Permission denied" durante instalación

**Síntoma:**
```
PermissionError: [Errno 13] Permission denied
```

**Soluciones:**
```bash
# Opción 1: Usar entorno virtual (recomendado)
python3 -m venv .venv
source .venv/bin/activate

# Opción 2: Instalar para usuario
pip install --user -r requirements.txt

# Opción 3: Cambiar permisos (solo Linux/Mac)
sudo chown -R $USER:$USER .
```

### ❌ "pip command not found"

**Solución:**
```bash
# Ubuntu/Debian
sudo apt install python3-pip

# Fedora/CentOS
sudo dnf install python3-pip

# macOS
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

### ❌ Versión de Python incompatible

**Síntoma:**
```
ERROR: This package requires Python >=3.8
```

**Solución:**
```bash
# Verificar versión
python3 --version

# Instalar Python actualizado (Ubuntu)
sudo apt update
sudo apt install python3.12

# Usar pyenv para múltiples versiones
curl https://pyenv.run | bash
pyenv install 3.12.0
pyenv global 3.12.0
```

---

## 📷 Problemas de Cámara

### ❌ "Can't open camera by index"

**Síntoma:**
```
[ WARN:0@1.572] global cap_v4l.cpp:982 open VIDEOIO(V4L2:/dev/video0): can't open camera by index
```

**Diagnóstico:**
```bash
# Verificar cámaras disponibles
ls /dev/video*

# Listar dispositivos USB
lsusb | grep -i camera

# Verificar permisos
ls -l /dev/video*
```

**Soluciones:**
```python
# 1. Cambiar índice de cámara en el código
cap = cv2.VideoCapture(0)  # Probar con 1, 2, etc.

# 2. Especificar backend
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Linux
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Windows
```

```bash
# 3. Agregar usuario al grupo video (Linux)
sudo usermod -a -G video $USER
# Reiniciar sesión después

# 4. Instalar drivers de cámara
sudo apt install v4l-utils
v4l2-ctl --list-devices
```

### ❌ Cámara en uso por otra aplicación

**Solución:**
```bash
# Encontrar procesos usando la cámara
sudo lsof /dev/video0

# Terminar procesos
sudo pkill -f "proceso_camara"

# Reiniciar servicios de cámara
sudo systemctl restart uvcvideo
```

### ❌ Calidad de video pobre

**Solución:**
```python
# Configurar resolución y FPS
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

# Ajustar configuraciones de cámara
cap.set(cv2.CAP_PROP_BRIGHTNESS, 0.5)
cap.set(cv2.CAP_PROP_CONTRAST, 0.5)
```

---

## 🧠 Problemas de TensorFlow

### ❌ "No module named 'tensorflow'"

**Solución:**
```bash
# Reinstalar TensorFlow
pip uninstall tensorflow
pip install tensorflow==2.20.0

# Para problemas de compatibilidad
pip install tensorflow-cpu
```

### ❌ CUDA Errors (Opcional)

**Síntoma:**
```
CUDA error: Failed call to cuInit: UNKNOWN ERROR (303)
```

**Información:** Estos errores son normales si no tienes GPU NVIDIA. El sistema funcionará con CPU.

**Para usar GPU (opcional):**
```bash
# Verificar GPU NVIDIA
nvidia-smi

# Instalar CUDA toolkit
# Seguir guía oficial de NVIDIA
```

### ❌ "Allocation exceeds memory"

**Síntoma:**
```
Allocation of 26214400 exceeds 10% of free system memory
```

**Soluciones:**
```python
# Configurar memoria GPU (si tienes GPU)
import tensorflow as tf
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    tf.config.experimental.set_memory_growth(gpus[0], True)

# Reducir batch size en entrenamiento
# En ModeloConvolucional.py
batch_size=16  # Reducir de 32
```

### ❌ Modelo no carga correctamente

**Síntoma:**
```
OSError: Unable to open file (file signature not found)
```

**Soluciones:**
```bash
# Verificar que el modelo existe
ls -la Proyecto_SI/FigurasGeometricas.h5

# Re-entrenar modelo si está corrupto
cd Proyecto_SI
python ModeloConvolucional.py

# Verificar espacio en disco
df -h
```

---

## 🖥️ Problemas de Interfaz Gráfica

### ❌ "no display name and no $DISPLAY environment variable"

**Síntoma:**
```
_tkinter.TclError: no display name and no $DISPLAY environment variable
```

**Soluciones:**
```bash
# Para SSH con X11 forwarding
ssh -X usuario@servidor

# Para WSL2 en Windows
export DISPLAY=$(cat /etc/resolv.conf | grep nameserver | awk '{print $2}'):0

# Usar VNC o X11 server
sudo apt install xvfb
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
```

### ❌ Ventanas no aparecen correctamente

**Soluciones:**
```bash
# Instalar herramientas adicionales
sudo apt install python3-tk-dev

# Verificar gestor de ventanas
echo $XDG_CURRENT_DESKTOP

# Usar modo virtual si no hay pantalla
python -c "import matplotlib; matplotlib.use('Agg')"
```

---

## 💾 Problemas de Base de Datos

### ❌ "no such table: auth_user"

**Solución:**
```bash
cd OpenCV
python build_db.py
```

### ❌ "database is locked"

**Soluciones:**
```bash
# Verificar procesos usando la BD
sudo lsof db/login.sqlite

# Eliminar locks
rm -f db/login.sqlite-wal db/login.sqlite-shm

# Recrear base de datos
rm db/login.sqlite
python build_db.py
```

### ❌ Problemas de encriptación

**Síntoma:**
```
cryptography.fernet.InvalidToken
```

**Solución:**
```python
# Verificar clave de encriptación en util/enoding_decoding.py
# Regenerar clave si es necesario
from cryptography.fernet import Fernet
key = Fernet.generate_key()
print(key.decode())
```

---

## 🌐 Problemas de Red

### ❌ "Port 5000 is in use"

**Solución:**
```bash
# Encontrar proceso usando el puerto
sudo lsof -ti:5000

# Terminar proceso
sudo kill -9 $(sudo lsof -ti:5000)

# O usar puerto diferente (ya configurado en 5001)
```

### ❌ "Connection refused"

**Soluciones:**
```bash
# Verificar que Flask está ejecutando
ps aux | grep python

# Verificar firewall
sudo ufw status
sudo ufw allow 5001

# Acceder desde localhost solamente
# http://127.0.0.1:5001 (no usar IP externa)
```

---

## ⚡ Problemas de Performance

### ❌ Video muy lento (bajo FPS)

**Soluciones:**
```python
# Reducir resolución
resized_frame = cv2.resize(frame, (200, 200))

# Procesar cada N frames
frame_count = 0
if frame_count % 3 == 0:  # Procesar cada 3er frame
    # hacer predicción
frame_count += 1

# Usar threading
import threading
```

### ❌ Consumo alto de memoria

**Soluciones:**
```python
# Liberar memoria
import gc
gc.collect()

# Usar context managers
with tf.device('/CPU:0'):
    # operaciones

# Cerrar ventanas OpenCV
cv2.destroyAllWindows()
```

### ❌ CPU al 100%

**Soluciones:**
```python
# Agregar delays
import time
time.sleep(0.01)  # 10ms delay

# Optimizar loops
if cv2.waitKey(1) & 0xFF == ord('q'):
    break
```

---

## 🔍 Comandos de Diagnóstico

### Verificación General
```bash
# Verificar Python y pip
python3 --version
pip --version

# Verificar dependencias principales
python3 -c "import cv2; print(f'OpenCV: {cv2.__version__}')"
python3 -c "import tensorflow as tf; print(f'TensorFlow: {tf.__version__}')"

# Verificar hardware
lscpu
free -h
df -h
```

### Logs Detallados
```bash
# Habilitar logs de TensorFlow
export TF_CPP_MIN_LOG_LEVEL=0

# Ejecutar con debug
python3 -u script.py 2>&1 | tee debug.log
```

### Verificar Instalación
```bash
# Usar scripts de verificación
cd Proyecto_SI && python3 verificar_proyecto.py
cd OpenCV && python3 verificar_opencv.py
```

---

## 🆘 Si Nada Funciona

1. **Reinstalación limpia:**
   ```bash
   rm -rf .venv
   python3 setup.py
   ```

2. **Verificar dependencias del sistema:**
   ```bash
   sudo apt update && sudo apt upgrade
   ```

3. **Usar Docker (alternativa):**
   ```bash
   # TODO: Agregar Dockerfile en futuras versiones
   ```

4. **Contactar soporte:**
   - GitHub Issues: [Reportar problema](https://github.com/tu-usuario/geolearnia/issues)
   - Email: soporte@geolearnia.com
   - Incluir logs completos y pasos para reproducir

---

## 📱 Contacto y Soporte

- 🐛 **Bugs**: [GitHub Issues](https://github.com/tu-usuario/geolearnia/issues)
- 💬 **Discusión**: [GitHub Discussions](https://github.com/tu-usuario/geolearnia/discussions)
- 📧 **Email**: dev@geolearnia.com
- 📚 **Wiki**: [Documentación Completa](https://github.com/tu-usuario/geolearnia/wiki)
