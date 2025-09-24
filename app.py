#!/usr/bin/env python3
"""
GEOLEARNIA v3.0 - Aplicación Completa
Reconocimiento Visual Automático con IA
"""

import os
import sys
import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow import keras
import logging
import base64
import io
from PIL import Image

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("🚀 Iniciando GEOLEARNIA v3.0...")

# Obtener directorio base del proyecto
base_dir = os.path.dirname(os.path.abspath(__file__))
project_si_dir = os.path.join(base_dir, 'Proyecto_SI')
logger.info(f"📂 Directorio base: {base_dir}")
logger.info(f"📂 Directorio Proyecto_SI: {project_si_dir}")

# Configurar Flask con rutas absolutas
template_dir = os.path.join(base_dir, 'Proyecto_SI', 'templates')
static_dir = os.path.join(base_dir, 'Proyecto_SI', 'static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

logger.info(f"📁 Template dir: {template_dir}")
logger.info(f"📁 Static dir: {static_dir}")

# Variables globales
model = None
class_names = ['circulo', 'cuadrado', 'triangulo']

def load_model():
    """Cargar el modelo de TensorFlow"""
    global model
    try:
        model_path = os.path.join(base_dir, 'Proyecto_SI', 'FigurasGeometricas.h5')
        if os.path.exists(model_path):
            model = keras.models.load_model(model_path)
            logger.info(f"✅ Modelo cargado: {model_path}")
            return True
        else:
            logger.warning(f"⚠️ Modelo no encontrado: {model_path}")
            return False
    except Exception as e:
        logger.error(f"❌ Error cargando modelo: {e}")
        model = None
        return False

def base64_to_image(base64_string):
    """Convertir base64 a imagen OpenCV"""
    try:
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        return opencv_image
    except Exception as e:
        logger.error(f"Error convirtiendo base64 a imagen: {e}")
        return None

def predict_with_model(roi):
    """Realizar predicción con el modelo de IA"""
    global model
    
    if model is None:
        # Simulación básica
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        contours, _ = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            
            if perimeter > 0:
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                if circularity > 0.7:
                    return "circulo", 0.85
                elif circularity < 0.5:
                    return "triangulo", 0.80
                else:
                    return "cuadrado", 0.82
        
        return "desconocido", 0.0
    
    try:
        roi_resized = cv2.resize(roi, (64, 64))
        roi_normalized = roi_resized.astype('float32') / 255.0
        roi_batch = np.expand_dims(roi_normalized, axis=0)
        
        predictions = model.predict(roi_batch, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        return class_names[predicted_class], confidence
    except Exception as e:
        logger.error(f"Error en predicción: {e}")
        return "error", 0.0

def detect_object_in_frame(frame):
    """Detectar objeto en frame usando contornos"""
    try:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blurred, 50, 150)
        
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None, edges
        
        largest_contour = max(contours, key=cv2.contourArea)
        
        if cv2.contourArea(largest_contour) < 1000:
            return None, edges
        
        return largest_contour, edges
    except Exception as e:
        logger.error(f"Error en detección: {e}")
        return None, None

@app.route('/')
def index():
    """Página principal con diagnóstico mejorado"""
    try:
        logger.info("Intentando cargar index.html...")
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error sirviendo index.html: {e}")
        
        # Diagnóstico completo
        diagnostics = {
            "error": str(e),
            "base_dir": base_dir,
            "project_si_dir": project_si_dir,
            "template_dir": template_dir,
            "static_dir": static_dir,
            "template_exists": os.path.exists(os.path.join(template_dir, 'index.html')),
            "css_exists": os.path.exists(os.path.join(static_dir, 'css', 'geolearnia.css')),
            "current_dir": os.getcwd(),
            "files_in_current": os.listdir('.') if os.path.exists('.') else [],
            "files_in_base": os.listdir(base_dir) if os.path.exists(base_dir) else []
        }
        
        html_response = f"""
        <h1>🎓 GEOLEARNIA v3.0 - Diagnóstico</h1>
        <h2>Error:</h2>
        <pre>{diagnostics['error']}</pre>
        <h2>Diagnóstico:</h2>
        <pre>{str(diagnostics)}</pre>
        """
        
        return html_response, 500

@app.route('/health')
def health_check():
    """Health check para Railway con diagnóstico"""
    try:
        status = {
            "status": "OK",
            "version": "3.0",
            "timestamp": str(os.getpid()),
            "directories": {
                "base_dir": os.path.exists(base_dir),
                "project_si": os.path.exists(project_si_dir),
                "templates": os.path.exists(template_dir),
                "static": os.path.exists(static_dir)
            },
            "model_loaded": model is not None
        }
        logger.info(f"Health check: {status}")
        return jsonify(status), 200
    except Exception as e:
        logger.error(f"Health check error: {e}")
        return jsonify({"status": "ERROR", "error": str(e)}), 500

@app.route('/api/status')
def api_status():
    """Estado de la API"""
    return jsonify({
        'status': 'online',
        'model_loaded': model is not None,
        'version': '3.0 - Reconocimiento Visual Automático',
        'directory': os.getcwd(),
        'files': os.listdir('.')
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_frame():
    """API para analizar un frame de video"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'No se proporcionó imagen'
            })
        
        # Convertir base64 a imagen
        frame = base64_to_image(data['image'])
        
        if frame is None:
            return jsonify({
                'success': False,
                'error': 'Error procesando imagen'
            })
        
        # Detectar objeto
        contour, edges = detect_object_in_frame(frame)
        
        if contour is None:
            return jsonify({
                'success': True,
                'detection': None,
                'message': 'No se detectó ningún objeto'
            })
        
        # Extraer región de interés
        x, y, w, h = cv2.boundingRect(contour)
        roi = frame[y:y+h, x:x+w]
        
        if roi.size == 0:
            return jsonify({
                'success': True,
                'detection': None,
                'message': 'ROI vacía'
            })
        
        # Predicción
        shape, confidence = predict_with_model(roi)
        
        return jsonify({
            'success': True,
            'detection': {
                'shape': shape,
                'confidence': confidence,
                'bbox': [int(x), int(y), int(w), int(h)]
            }
        })
        
    except Exception as e:
        logger.error(f"Error en análisis: {e}")
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        })

# Inicialización
logger.info("🔧 Inicializando modelo...")
model_loaded = load_model()
if model_loaded:
    logger.info("✅ Modelo cargado correctamente")
else:
    logger.warning("⚠️ Funcionando sin modelo - predicciones simuladas")

if __name__ == '__main__':
    # Configurar puerto
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"🌐 Servidor iniciando en {host}:{port}")
    logger.info(f"📂 Variables de entorno PORT: {os.environ.get('PORT')}")
    logger.info(f"📂 Variables de entorno RAILWAY_*: {[k for k in os.environ.keys() if k.startswith('RAILWAY')]}")
    logger.info(f"📂 Directorio actual: {os.getcwd()}")
    logger.info(f"📂 Archivos en raíz: {os.listdir('.')}")
    
    if os.path.exists('Proyecto_SI'):
        logger.info(f"📂 Archivos en Proyecto_SI: {os.listdir('Proyecto_SI')}")
        if os.path.exists('Proyecto_SI/templates'):
            logger.info(f"📂 Templates disponibles: {os.listdir('Proyecto_SI/templates')}")
        if os.path.exists('Proyecto_SI/static'):
            logger.info(f"📂 Static disponible: {os.listdir('Proyecto_SI/static')}")
    
    try:
        logger.info("🚀 Iniciando Flask app...")
        app.run(host=host, port=port, debug=False, threaded=True)
    except Exception as e:
        logger.error(f"💥 Error iniciando servidor: {e}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        raise