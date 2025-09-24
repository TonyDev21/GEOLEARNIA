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
    """Realizar predicción con el modelo de IA mejorada"""
    global model
    
    if model is None:
        # Simulación mejorada sin modelo
        logger.info("Usando simulación (modelo no disponible)")
        gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        
        # Aplicar threshold para mejor detección de contornos
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(largest_contour)
            perimeter = cv2.arcLength(largest_contour, True)
            
            if perimeter > 0:
                # Calcular métricas para clasificación
                circularity = 4 * np.pi * area / (perimeter * perimeter)
                
                # Aproximar contorno a polígono
                epsilon = 0.02 * perimeter
                approx = cv2.approxPolyDP(largest_contour, epsilon, True)
                vertices = len(approx)
                
                logger.info(f"Análisis de forma: circularity={circularity:.3f}, vertices={vertices}")
                
                # Clasificación mejorada
                if circularity > 0.75:
                    return "circulo", min(0.95, 0.7 + circularity * 0.3)
                elif vertices == 3:
                    return "triangulo", min(0.90, 0.75 + (1-circularity) * 0.2)
                elif vertices == 4 or (0.4 < circularity < 0.75):
                    return "cuadrado", min(0.88, 0.70 + (1-abs(circularity-0.6)) * 0.3)
                else:
                    # Si no encaja claramente, usar heurísticas adicionales
                    if circularity > 0.6:
                        return "circulo", 0.65
                    elif circularity < 0.4:
                        return "triangulo", 0.60
                    else:
                        return "cuadrado", 0.62
        
        logger.info("No se pudo analizar la forma")
        return "desconocido", 0.0
    
    try:
        # Preprocesamiento mejorado para el modelo real
        roi_resized = cv2.resize(roi, (64, 64))
        
        # Normalización mejorada
        roi_normalized = roi_resized.astype('float32') / 255.0
        
        # Expandir dimensiones para el batch
        roi_batch = np.expand_dims(roi_normalized, axis=0)
        
        # Predicción con el modelo real
        predictions = model.predict(roi_batch, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        # Solo aceptar predicciones con confianza razonable
        if confidence < 0.3:
            logger.info(f"Confianza muy baja: {confidence:.3f}")
            return "desconocido", confidence
        
        shape_name = class_names[predicted_class]
        logger.info(f"Predicción: {shape_name} con confianza {confidence:.3f}")
        
        return shape_name, confidence
        
    except Exception as e:
        logger.error(f"Error en predicción con modelo: {e}")
        # Fallback a simulación si falla el modelo
        return predict_with_model(roi)  # Recursión controlada

def detect_object_in_frame(frame):
    """Detectar objeto en frame usando contornos mejorados"""
    try:
        # Convertir a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Mejores filtros para diferentes condiciones de iluminación
        # Ecualización del histograma para mejor contraste
        gray = cv2.equalizeHist(gray)
        
        # Blur gaussiano para reducir ruido
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)
        
        # Detectar bordes con parámetros más permisivos
        edges = cv2.Canny(blurred, 30, 80)
        
        # Dilatación para conectar bordes fragmentados
        kernel = np.ones((3,3), np.uint8)
        edges = cv2.dilate(edges, kernel, iterations=1)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            logger.info("No se encontraron contornos")
            return None, edges
        
        # Filtrar contornos por área y forma
        valid_contours = []
        for contour in contours:
            area = cv2.contourArea(contour)
            # Umbral más bajo para detectar objetos más pequeños
            if area > 300:  # Reducido de 1000 a 300
                # Verificar que el contorno tenga una forma razonable
                perimeter = cv2.arcLength(contour, True)
                if perimeter > 0:
                    circularity = 4 * np.pi * area / (perimeter * perimeter)
                    # Aceptar contornos con circularity entre 0.1 y 1.5 (más permisivo)
                    if 0.1 <= circularity <= 1.5:
                        valid_contours.append(contour)
        
        if not valid_contours:
            logger.info("No se encontraron contornos válidos")
            return None, edges
        
        # Seleccionar el contorno más grande de los válidos
        largest_contour = max(valid_contours, key=cv2.contourArea)
        area = cv2.contourArea(largest_contour)
        
        logger.info(f"Contorno detectado con área: {area}")
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
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        contour, edges = detect_object_in_frame(frame_rgb)
        
        if contour is None:
            return jsonify({
                'success': True,
                'detection': None,
                'message': 'Buscando figuras geométricas...'
            })
        
        # Extraer región de interés con padding
        x, y, w, h = cv2.boundingRect(contour)
        
        # Agregar padding para mejor análisis
        padding = 20
        x_pad = max(0, x - padding)
        y_pad = max(0, y - padding)
        w_pad = min(frame.shape[1] - x_pad, w + 2*padding)
        h_pad = min(frame.shape[0] - y_pad, h + 2*padding)
        
        roi = frame[y_pad:y_pad+h_pad, x_pad:x_pad+w_pad]
        
        if roi.size == 0 or roi.shape[0] < 10 or roi.shape[1] < 10:
            return jsonify({
                'success': True,
                'detection': None,
                'message': 'Región detectada muy pequeña'
            })
        
        # Predicción
        shape, confidence = predict_with_model(roi)
        
        # Solo devolver detecciones con confianza razonable
        if confidence < 0.4:
            return jsonify({
                'success': True,
                'detection': None,
                'message': f'Confianza baja ({confidence:.2f}) - Acerca más el objeto'
            })
        
        logger.info(f"Detección exitosa: {shape} ({confidence:.3f})")
        
        return jsonify({
            'success': True,
            'detection': {
                'shape': shape,
                'confidence': confidence,
                'bbox': [int(x_pad), int(y_pad), int(w_pad), int(h_pad)]
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