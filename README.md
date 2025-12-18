# 🎯 GEOLEARNIA v3.0

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.17.0-orange.svg)](https://tensorflow.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.10.0-green.svg)](https://opencv.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.2-lightgrey.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **🎓 Sistema Inteligente de Reconocimiento Geométrico** | Aplicación web de visión por computadora con IA para detección automática de figuras geométricas en tiempo real. Reconoce círculos, cuadrados y triángulos con guías visuales instantáneas.

---

## 📑 Tabla de Contenidos

- [Características](#-características-principales)
- [Tecnologías](#-stack-tecnológico)
- [Arquitectura](#-arquitectura-del-sistema)
- [Módulos](#-módulos-del-proyecto)
- [Instalación](#-instalación-rápida)
- [Uso](#-uso)
- [Estructura](#-estructura-del-proyecto)
- [API](#-api-rest)
- [Licencia](#-licencia)

---

## ✨ Características Principales

### 🤖 Inteligencia Artificial
- **Red Neuronal Convolucional (CNN)** pre-entrenada con TensorFlow/Keras
- **Modelo ligero** de 64x64 píxeles con arquitectura optimizada
- **Clasificación en tiempo real** con confianza ajustable (>40%)
- **Fallback inteligente** con algoritmos geométricos si el modelo falla

### 👁️ Visión por Computadora
- **Detección de contornos** con OpenCV mejorada
- **Procesamiento adaptativo** según iluminación (ecualización de histograma)
- **Filtros anti-ruido** con Gaussian Blur y Canny Edge Detection
- **Reconocimiento instantáneo** cada 100ms sin lag

### 🎨 Interfaz de Usuario
- **Diseño responsive** para PC, tablets y móviles
- **Guías visuales en tiempo real** con overlays en canvas
- **Punto de escaneo animado** cuando busca figuras
- **Marcos de detección** con colores distintivos por forma
- **Indicadores de confianza** en porcentaje

### 📱 Multi-dispositivo
- Compatible con **cámaras web** de escritorio
- Soporte para **cámaras traseras** de móviles/tablets
- **Adaptación automática** de resolución (ideal: 640x480)
- **Sin instalación** - funciona en el navegador

---

## 🛠️ Tecnologías Usadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **Python** | 3.11 | Lenguaje de programación principal |
| **Flask** | 3.1.2 | Framework web minimalista y ligero |
| **TensorFlow** | 2.17.0 | Framework de Deep Learning (CPU optimizado) |
| **Keras** | 3.12.0 | API de alto nivel para redes neuronales |
| **OpenCV** | 4.10.0 | Procesamiento de imágenes y visión por computadora |
| **NumPy** | 1.26.x | Operaciones matriciales y arrays optimizados |
| **Pillow** | 10.0.1 | Manipulación y procesamiento de imágenes |
| **Gunicorn** | 23.0.0 | Servidor WSGI para producción |
| **HTML5** | - | Estructura de la interfaz web |
| **CSS3** | - | Diseño responsive y estilos visuales |
| **JavaScript** | ES6 | Lógica del cliente y gestión de cámara |

### Arquitectura del Modelo de IA
```
Red Neuronal Convolucional (CNN)
├── Input: 64x64x3 RGB
├── Arquitectura: 3 capas Conv2D + MaxPooling + Dense
├── Activación: ReLU + Softmax
├── Optimizador: Adam
├── Clases: [círculo, cuadrado, triángulo]
└── Formato: HDF5 (FigurasGeometricas.h5)
└── Parámetros: 683,715 (entrenables)
```

### ⚠️ Sin Base de Datos
> **Nota:** Este sistema NO utiliza bases de datos. El modelo está pre-entrenado y el procesamiento es 100% en memoria y tiempo real.

---

## 🏛️ Arquitectura del Sistema

### Patrón Cliente-Servidor

```
┌─────────────────────────────────────────────────────────────┐
│                        NAVEGADOR                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  FRONTEND (Cliente)                                  │  │
│  │  ┌────────────┐  ┌──────────────┐  ┌─────────────┐ │  │
│  │  │ HTML/CSS   │  │  JavaScript  │  │   Canvas    │ │  │
│  │  │ (UI/UX)    │  │ (Lógica)     │  │  (Overlay)  │ │  │
│  │  └────────────┘  └──────────────┘  └─────────────┘ │  │
│  │         │                │                  │        │  │
│  │         └────────────────┴──────────────────┘        │  │
│  │                         │                            │  │
│  │                    MediaDevices                      │  │
│  │                    (WebCamera)                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                             │                               │
│                    HTTP POST (Base64)                       │
│                             │                               │
└─────────────────────────────┼───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   SERVIDOR FLASK                            │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  BACKEND (Servidor)                                  │  │
│  │  ┌────────────┐  ┌──────────────┐  ┌─────────────┐ │  │
│  │  │   Flask    │  │   OpenCV     │  │ TensorFlow  │ │  │
│  │  │  (REST)    │  │ (Detección)  │  │  (Modelo)   │ │  │
│  │  └────────────┘  └──────────────┘  └─────────────┘ │  │
│  │         │                │                  │        │  │
│  │         └────────────────┴──────────────────┘        │  │
│  │                         │                            │  │
│  │              FigurasGeometricas.h5                   │  │
│  │              (Modelo Pre-entrenado)                  │  │
│  └──────────────────────────────────────────────────────┘  │
│                             │                               │
│                    JSON Response                            │
│                 {shape, confidence, bbox}                   │
│                             │                               │
└─────────────────────────────┼───────────────────────────────┘
                              │
                              ▼
                     Renderizado Visual
```

### Flujo de Datos

1. **Captura** → Usuario inicia cámara en el navegador
2. **Stream** → Video se muestra en elemento `<video>`
3. **Análisis Loop** → Cada 100ms captura frame en canvas
4. **Codificación** → Frame → Base64 string
5. **Envío** → POST a `/api/analyze` con imagen
6. **Procesamiento Backend:**
   - Decodifica Base64 → OpenCV Mat
   - Detecta contornos con Canny + filtros
   - Extrae ROI (Region of Interest) con padding
   - Predice con modelo TensorFlow
   - Retorna {shape, confidence, bbox}
7. **Renderizado** → Frontend dibuja overlay con resultado
8. **Repetición** → Ciclo continuo hasta detener cámara

---

## 📦 Módulos del Proyecto

El sistema está dividido en **3 módulos principales**:

### **1️⃣ Módulo de Backend - API REST** (`app.py`)

**Responsabilidades:**
- Servidor Flask con rutas HTTP
- Carga del modelo de IA al inicio
- Procesamiento de imágenes con OpenCV
- Predicción con TensorFlow
- Gestión de errores y logging

**Funcionalidades clave:**

| Función | Descripción |
|---------|-------------|
| `load_model()` | Carga FigurasGeometricas.h5 en memoria global |
| `base64_to_image()` | Convierte string Base64 a matriz OpenCV |
| `detect_object_in_frame()` | Encuentra contornos válidos en frame |
| `predict_with_model()` | Clasifica ROI con CNN y retorna shape + confianza |

**Endpoints REST:**

| Ruta | Método | Descripción |
|------|--------|-------------|
| `/` | GET | Sirve interfaz HTML principal |
| `/health` | GET | Health check para monitoreo |
| `/api/status` | GET | Estado del sistema y modelo |
| `/api/analyze` | POST | Análisis de frame (Base64 → JSON) |

**Documentación:** Ver [docs/MODULO_BACKEND.md](docs/MODULO_BACKEND.md) para detalles técnicos completos.

---

### **2️⃣ Módulo de Frontend - Interfaz Web** (`Proyecto_SI/`)

#### **A) Vista (Templates)** → `templates/index.html`

**Componentes HTML:**
- `<video>` → Stream de cámara en tiempo real
- `<canvas id="canvas">` → Captura frames (oculto)
- `<canvas id="overlay">` → Overlays visuales
- Botones de control (Iniciar/Detener)
- Panel de resultados con forma + confianza

#### **B) Controlador (JavaScript)** → `static/js/geolearnia.js`

**Clase `GeoLearnia`:**

```javascript
class GeoLearnia {
    // Gestión de cámara
    async startCamera()      // Solicita permisos MediaDevices
    stopCamera()             // Libera recursos de stream
    
    // Análisis en tiempo real
    startAutoAnalysis()      // Inicia loop cada 100ms
    async analyzeFrame()     // Captura + envía + renderiza
    
    // Detección cliente-side (fallback)
    detectShapeDirectly()    // Algoritmos geométricos en JS
    detectEdges()            // Edge detection en canvas
    findContoursInArea()     // Búsqueda de contornos
    
    // Renderizado visual
    drawSimpleFrame()        // Marco de detección
    drawScanningPoint()      // Punto animado de escaneo
    updateStatus()           // Actualiza mensajes UI
}
```

**Ciclo de vida:**
1. Constructor → Inicializa elementos DOM
2. `checkAPIStatus()` → Verifica backend disponible
3. Usuario click → `startCamera()` → Solicita permisos
4. Stream activo → `startAutoAnalysis()` → Loop infinito
5. Cada 100ms → `analyzeFrame()` → Fetch + dibujar
6. Usuario stop → `stopCamera()` → Limpia recursos

**Documentación:** Ver [docs/MODULO_FRONTEND.md](docs/MODULO_FRONTEND.md) para detalles técnicos completos.

---

### **3️⃣ Módulo de Inteligencia Artificial** (`Proyecto_SI/FigurasGeometricas.h5`)

**Modelo CNN Pre-entrenado**

**Arquitectura:**
```python
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d (Conv2D)              (None, 62, 62, 32)        896       
max_pooling2d (MaxPooling2D) (None, 31, 31, 32)        0         
conv2d_1 (Conv2D)            (None, 29, 29, 64)        18496     
max_pooling2d_1 (MaxPooling) (None, 14, 14, 64)        0         
conv2d_2 (Conv2D)            (None, 12, 12, 128)       73856     
max_pooling2d_2 (MaxPooling) (None, 6, 6, 128)         0         
flatten (Flatten)            (None, 4608)              0         
dense (Dense)                (None, 128)               590080    
dropout (Dropout)            (None, 128)               0         
dense_1 (Dense)              (None, 3)                 387       
=================================================================
Total params: 683,715
Trainable params: 683,715
```

**Datos de Entrenamiento:**
- **Dataset:** `Proyecto_SI/dataset/`
  - `circulo/` → Imágenes de objetos circulares
  - `cuadrado/` → Imágenes de objetos cuadrados
  - `triangulo/` → Imágenes de objetos triangulares
- **Formato:** Imágenes 64x64 RGB
- **Augmentation:** Rotación, zoom, flip horizontal

**Preprocesamiento:**
```python
1. Resize → 64x64 píxeles
2. Normalización → valores [0, 1]
3. Batch dimension → (1, 64, 64, 3)
4. Predicción → Softmax output [circulo, cuadrado, triangulo]
```

**Documentación:** Ver [docs/MODULO_IA.md](docs/MODULO_IA.md) para detalles técnicos completos.

---

## 🚀 Instalación Rápida

### Requisitos Previos
- **Python 3.11** instalado ([Descargar](https://www.python.org/downloads/))
- **pip** actualizado: `python -m pip install --upgrade pip`
- **Cámara web** funcional
- **Navegador moderno** (Chrome, Firefox, Edge, Safari)

### Pasos

1️⃣ **Clonar repositorio**
```bash
git clone https://github.com/TonyDev21/GEOLEARNIA.git
cd GEOLEARNIA
```

2️⃣ **Crear entorno virtual** (recomendado)
```bash
python -m venv .venv
```

**Activar:**
- Windows: `.venv\Scripts\activate`
- Linux/Mac: `source .venv/bin/activate`

3️⃣ **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4️⃣ **Ejecutar aplicación**
```bash
python app.py
```

5️⃣ **Abrir en navegador**
```
http://127.0.0.1:5000
```

---

## 💡 Uso

### Instrucciones Paso a Paso

1. **Iniciar Cámara**
   - Click en botón "📷 Iniciar Cámara"
   - Permitir acceso cuando el navegador solicite permisos

2. **Posicionar Objeto**
   - Coloca un objeto geométrico frente a la cámara
   - Objetos válidos:
     - 🔴 **Círculos:** Monedas, tapas, botones, CD
     - 🟦 **Cuadrados:** Libros, tarjetas, papeles, cajas
     - 🔺 **Triángulos:** Reglas triangulares, señales cortadas

3. **Reconocimiento Automático**
   - El sistema analiza automáticamente cada 100ms
   - Verás un **punto de escaneo** mientras busca
   - Al detectar: **marco verde** + etiqueta con nombre y confianza

4. **Consejos para Mejor Detección**
   - ✅ Buena iluminación (natural o artificial)
   - ✅ Fondo contrastante (evitar mismo color que objeto)
   - ✅ Objeto centrado y visible completamente
   - ✅ Distancia media (30-60 cm de la cámara)
   - ❌ Evitar reflejos o sombras fuertes

5. **Detener**
   - Click en "⏹️ Detener Cámara" cuando termines

---

## 📂 Estructura del Proyecto

```
GEOLEARNIA/
│
├── 📄 app.py                          # Servidor Flask principal (390 líneas)
├── 📄 run_app.py                      # Script alternativo de ejecución
├── 📄 requirements.txt                # Dependencias Python
├── 📄 README.md                       # Esta documentación
├── 📄 LICENSE                         # Licencia MIT
├── 📄 GEOLEARNIA.spec                 # Config PyInstaller (para .exe)
│
├── 📁 Proyecto_SI/                    # Módulo principal del sistema
│   │
│   ├── 🧠 FigurasGeometricas.h5       # Modelo CNN pre-entrenado (2.6 MB)
│   │
│   ├── 📁 templates/
│   │   └── 📄 index.html              # Interfaz HTML principal (60 líneas)
│   │
│   ├── 📁 static/
│   │   ├── 📁 css/
│   │   │   └── 📄 geolearnia.css      # Estilos responsive (~400 líneas)
│   │   └── 📁 js/
│   │       └── 📄 geolearnia.js       # Lógica cliente (~980 líneas)
│   │
│   ├── 📁 dataset/                    # Datos de entrenamiento
│   │   ├── 📁 circulo/                # Imágenes de círculos
│   │   ├── 📁 cuadrado/               # Imágenes de cuadrados
│   │   └── 📁 triangulo/              # Imágenes de triángulos
│   │
│   └── 📁 Audios/                     # Recursos de audio (opcional)
│
├── 📁 docs/                           # Documentación técnica de módulos
│   ├── 📄 MODULO_BACKEND.md           # Detalles del módulo Backend
│   ├── 📄 MODULO_FRONTEND.md          # Detalles del módulo Frontend
│   └── 📄 MODULO_IA.md                # Detalles del módulo de IA
│
├── 📁 .venv/                          # Entorno virtual Python (ignorado)
├── 📁 build/                          # Archivos de build PyInstaller
├── 📁 dist/                           # Ejecutable compilado (si se genera)
│
└── 📄 .gitignore                      # Archivos ignorados por Git
```

### Descripción de Archivos Clave

| Archivo | Líneas | Descripción |
|---------|--------|-------------|
| `app.py` | 390 | Backend Flask con API REST, procesamiento OpenCV y predicción IA |
| `index.html` | 60 | Estructura HTML con canvas para video y overlays |
| `geolearnia.js` | 980 | Clase JavaScript con gestión de cámara y análisis en tiempo real |
| `geolearnia.css` | 400 | Diseño responsive con animaciones y temas |
| `FigurasGeometricas.h5` | - | Red neuronal convolucional entrenada (683K parámetros) |

---

## 🔌 API REST

### Endpoints Disponibles

#### 1. **GET /** - Página Principal
**Descripción:** Sirve la interfaz web HTML  
**Respuesta:** HTML completo de la aplicación

---

#### 2. **GET /health** - Health Check
**Descripción:** Verifica estado del sistema  
**Respuesta:**
```json
{
  "status": "OK",
  "version": "3.0",
  "directories": {
    "base_dir": true,
    "project_si": true,
    "templates": true,
    "static": true
  },
  "model_loaded": true
}
```

---

#### 3. **GET /api/status** - Estado del Sistema
**Descripción:** Información del servidor y modelo  
**Respuesta:**
```json
{
  "status": "online",
  "model_loaded": true,
  "version": "3.0 - Reconocimiento Visual Automático",
  "directory": "/app",
  "files": ["app.py", "Proyecto_SI", "requirements.txt"]
}
```

---

#### 4. **POST /api/analyze** - Analizar Frame
**Descripción:** Procesa imagen y retorna detección de forma geométrica

**Request:**
```json
{
  "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEAYABgAAD..."
}
```

**Response (Detección exitosa):**
```json
{
  "success": true,
  "detection": {
    "shape": "circulo",
    "confidence": 0.87,
    "bbox": [150, 120, 200, 180]
  }
}
```

**Response (Sin detección):**
```json
{
  "success": true,
  "detection": null,
  "message": "Buscando figuras geométricas..."
}
```

**Response (Error):**
```json
{
  "success": false,
  "error": "No se proporcionó imagen"
}
```

**Parámetros del bbox:**
- `[x, y, width, height]` → Coordenadas del rectángulo delimitador

---

## 🧪 Testing y Validación

### Casos de Prueba

| Escenario | Objeto | Resultado Esperado |
|-----------|--------|-------------------|
| Luz natural | Moneda | ✅ circulo (85-95%) |
| Luz artificial | Libro cuadrado | ✅ cuadrado (80-90%) |
| Fondo blanco | Regla triangular | ✅ triangulo (75-88%) |
| Poca luz | Cualquier objeto | ⚠️ Confianza < 60% |
| Objeto parcial | Medio círculo | ❌ Sin detección |
| Múltiples objetos | 2 círculos | ✅ Detecta el mayor |

---

## 🚢 Deployment

### Producción con Gunicorn

```bash
gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 60 app:app
```

### Variables de Entorno

```bash
PORT=5000          # Puerto del servidor
HOST=0.0.0.0       # Host (0.0.0.0 para exponer públicamente)
```

---

## 🤝 Contribuir

¿Quieres mejorar GEOLEARNIA? ¡Las contribuciones son bienvenidas!

1. Fork del proyecto
2. Crea tu rama: `git checkout -b feature/nueva-caracteristica`
3. Commit: `git commit -m 'Añadir nueva característica'`
4. Push: `git push origin feature/nueva-caracteristica`
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**.  
Consulta el archivo [LICENSE](LICENSE) para más detalles.

---

## 👨‍💻 Autor

**TonyDev21**  
- GitHub: [@TonyDev21](https://github.com/TonyDev21)
- Proyecto: Sistema Inteligente de Reconocimiento Geométrico

---

## 📞 Soporte

¿Problemas o preguntas?
- 🐛 **Issues:** [GitHub Issues](https://github.com/TonyDev21/GEOLEARNIA/issues)
- 📧 **Email:** Contacta al autor

---

⭐ **Si te gusta este proyecto, dale una estrella en GitHub!**

**Creado con ❤️ y Python** | © 2025 GEOLEARNIA
