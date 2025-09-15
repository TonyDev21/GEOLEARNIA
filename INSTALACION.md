# 📘 Guía de Instalación y Uso - GEOLEARNIA

## 🛠️ Instalación Paso a Paso

### 1️⃣ Prerrequisitos
- **Python 3.13+** instalado en tu sistema
- **Git** para clonar el repositorio
- **Cámara web** funcional
- **Conexión a internet** para descargar dependencias

### 2️⃣ Clonar el Repositorio
```bash
git clone https://github.com/TonyDev21/GEOLEARNIA.git
cd GEOLEARNIA
```

### 3️⃣ Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 4️⃣ Ejecutar la Aplicación
```bash
cd Proyecto_SI
python run_pointer.py
```

### 5️⃣ Acceder a la Aplicación
Abre tu navegador y ve a: `http://127.0.0.1:5002`

## 🎯 Cómo Usar GEOLEARNIA

### Interfaz Principal
1. **Cruz Amarilla**: Indica el centro de detección
2. **Rectángulo Azul**: Área de análisis (250x250px)
3. **Video en Tiempo Real**: Stream de tu cámara
4. **Resultados**: Aparecen automáticamente cuando detecta un objeto

### Pasos para Detectar Figuras
1. 📹 **Iniciar**: La cámara se activa automáticamente
2. 🎯 **Posicionar**: Coloca tu objeto en la cruz amarilla
3. 📦 **Ajustar**: Asegúrate de que esté dentro del rectángulo
4. ⏳ **Esperar**: La detección es automática
5. ✅ **Ver Resultado**: Aparece el nombre y porcentaje de confianza

### Objetos Recomendados
- **Círculos**: Monedas, tapas redondas, discos
- **Cuadrados**: Libros, cajas, tarjetas
- **Triángulos**: Reglas triangulares, objetos con forma triangular

## 🔧 Solución de Problemas Rápidos

### 🚫 "No se puede acceder a la cámara"
```bash
# Verificar que la cámara funcione
python -c "import cv2; cap = cv2.VideoCapture(0); print('OK' if cap.read()[0] else 'Error')"
```

### 🚫 "Error de módulo no encontrado"
```bash
# Reinstalar dependencias
pip install -r requirements.txt --force-reinstall
```

### 🚫 "Puerto 5002 ocupado"
- Cerrar otras aplicaciones que usen ese puerto
- O cambiar el puerto en `web_pointer.py` línea 321

### 🚫 "Modelo no encontrado"
Verificar que existe: `Proyecto_SI/FigurasGeometricas.h5`

## 📱 Funciones Adicionales

### Aplicación de Escritorio
```bash
cd Proyecto_SI
python Video2.py
```

## 🔄 Para Desarrolladores

### Estructura de Archivos Principales
- `Proyecto_SI/web_pointer.py` - Aplicación principal Flask
- `Proyecto_SI/run_pointer.py` - Script de ejecución
- `Proyecto_SI/templates/pointer.html` - Interfaz web
- `Proyecto_SI/static/css/styles.css` - Estilos

### Hacer Contribuciones
1. Fork del repositorio
2. Crear rama: `git checkout -b mi-mejora`
3. Commit: `git commit -m "Descripción"`
4. Push: `git push origin mi-mejora`
5. Crear Pull Request

## ✅ Verificación de Instalación

Ejecuta estos comandos para verificar que todo funciona:

```bash
# 1. Verificar Python
python --version

# 2. Verificar dependencias principales
python -c "import cv2, tensorflow, flask; print('✅ Todas las dependencias OK')"

# 3. Verificar cámara
python -c "import cv2; print('✅ Cámara OK' if cv2.VideoCapture(0).read()[0] else '❌ Error cámara')"

# 4. Verificar modelo
cd Proyecto_SI
python -c "import tensorflow as tf; tf.keras.models.load_model('FigurasGeometricas.h5'); print('✅ Modelo OK')"
```

Si todos muestran ✅, ¡estás listo para usar GEOLEARNIA!

## 📞 Obtener Ayuda

- 🐛 **Reportar Problemas**: [GitHub Issues](https://github.com/TonyDev21/GEOLEARNIA/issues)
- 📚 **Documentación**: Ver `README.md` principal
- 🛠️ **Troubleshooting**: Ver `TROUBLESHOOTING.md`

---
*¡Disfruta aprendiendo con GEOLEARNIA! 🎓*