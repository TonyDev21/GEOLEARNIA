#!/usr/bin/env python3
"""
GEOLEARNIA - Backend API Profesional
Arquitectura moderna: Cliente captura cámara → Servidor procesa IA
"""

import cv2
import numpy as np
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
from tensorflow import keras
import logging
import os
import base64
import io
from PIL import Image

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar Flask con paths absolutos
template_dir = os.path.abspath('templates')
static_dir = os.path.abspath('static')

app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)

logger.info(f"📁 Template dir: {template_dir}")
logger.info(f"📁 Static dir: {static_dir}")
logger.info(f"📄 Templates disponibles: {os.listdir(template_dir) if os.path.exists(template_dir) else 'No existe'}")

# Variables globales
model = None
class_names = ['circulo', 'cuadrado', 'triangulo']

def load_model():
    """Cargar el modelo de TensorFlow"""
    global model
    try:
        model_path = 'FigurasGeometricas.h5'
        if not os.path.exists(model_path):
            logger.error(f"❌ Modelo no encontrado: {model_path}")
            return False
        
        model = keras.models.load_model(model_path)
        logger.info(f"✅ Modelo cargado: {model_path}")
        return True
    except Exception as e:
        logger.error(f"❌ Error cargando modelo: {e}")
        model = None
        return False

def detect_object_in_frame(frame):
    """Detectar objeto en frame usando contornos"""
    if frame.size == 0:
        return None, None
    
    try:
        # Convertir a escala de grises
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Aplicar desenfoque para reducir ruido
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Detección de bordes
        edges = cv2.Canny(blurred, 50, 150)
        
        # Encontrar contornos
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return None, edges
        
        # Encontrar el contorno más grande
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Filtrar contornos muy pequeños
        if cv2.contourArea(largest_contour) < 1000:
            return None, edges
        
        return largest_contour, edges
    except Exception as e:
        logger.error(f"Error en detección: {e}")
        return None, None

def predict_with_model(roi):
    """Realizar predicción con el modelo de IA"""
    global model
    
    if model is None:
        logger.warning("Modelo no disponible - predicción simulada")
        # Simulación básica basada en área y forma
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
        # Redimensionar para el modelo
        roi_resized = cv2.resize(roi, (64, 64))
        roi_normalized = roi_resized.astype('float32') / 255.0
        roi_batch = np.expand_dims(roi_normalized, axis=0)
        
        # Predicción
        predictions = model.predict(roi_batch, verbose=0)
        predicted_class = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class])
        
        return class_names[predicted_class], confidence
    except Exception as e:
        logger.error(f"Error en predicción: {e}")
        return "error", 0.0

def base64_to_image(base64_string):
    """Convertir base64 a imagen OpenCV"""
    try:
        # Remover prefijo si existe
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
        
        # Decodificar base64
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        
        # Convertir PIL a OpenCV
        opencv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        return opencv_image
    except Exception as e:
        logger.error(f"Error convirtiendo base64 a imagen: {e}")
        return None

def image_to_base64(image):
    """Convertir imagen OpenCV a base64"""
    try:
        _, buffer = cv2.imencode('.jpg', image)
        image_base64 = base64.b64encode(buffer).decode('utf-8')
        return f"data:image/jpeg;base64,{image_base64}"
    except Exception as e:
        logger.error(f"Error convirtiendo imagen a base64: {e}")
        return None

@app.route('/')
def index():
    """Página principal"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error sirviendo index.html: {e}")
        return f"<h1>GEOLEARNIA v3.0</h1><p>Error: {e}</p><p>Template path issue</p>", 500

@app.route('/api/analyze', methods=['POST'])
def analyze_frame():
    """API para analizar un frame de video"""
    try:
        data = request.get_json()
        
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'error': 'No se recibió imagen'
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
                'message': 'No se detectó ninguna forma geométrica'
            })
        
        # Extraer región de interés
        x, y, w, h = cv2.boundingRect(contour)
        roi = frame[y:y+h, x:x+w]
        
        # Realizar predicción
        predicted_shape, confidence = predict_with_model(roi)
        
        # Dibujar resultado en el frame
        result_frame = frame.copy()
        cv2.drawContours(result_frame, [contour], -1, (0, 255, 0), 3)
        cv2.rectangle(result_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Agregar texto con predicción
        cv2.putText(result_frame, f"{predicted_shape.upper()}", 
                   (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
        cv2.putText(result_frame, f"Confianza: {confidence:.2f}", 
                   (x, y+h+25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Convertir resultado a base64
        result_image_b64 = image_to_base64(result_frame)
        
        return jsonify({
            'success': True,
            'detection': {
                'shape': predicted_shape,
                'confidence': confidence,
                'bbox': {'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h)}
            },
            'result_image': result_image_b64,
            'message': f'Detectado: {predicted_shape} (confianza: {confidence:.2f})'
        })
        
    except Exception as e:
        logger.error(f"Error en análisis: {e}")
        return jsonify({
            'success': False,
            'error': f'Error interno: {str(e)}'
        })

@app.route('/api/status')
def api_status():
    """Estado de la API"""
    return jsonify({
        'status': 'online',
        'model_loaded': model is not None,
        'version': '3.0 - Reconocimiento Visual Automático'
    })

@app.route('/health')
def health_check():
    """Health check para Railway"""
    return "OK", 200

def cleanup():
    """Limpiar recursos"""
    pass

# Inicialización global para Railway/Gunicorn
logger.info("� Inicializando GEOLEARNIA para Railway...")
model_loaded = load_model()
if model_loaded:
    logger.info("✅ Modelo preocargado correctamente")
else:
    logger.warning("⚠️ Modelo no disponible - funcionando en modo simulado")

if __name__ == '__main__':
    logger.info("🚀 Iniciando GEOLEARNIA v3.0 - Reconocimiento Visual Automático")
    
    # Configurar puerto
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"🌐 Servidor iniciando en {host}:{port}")
    
    try:
        app.run(host=host, port=port, debug=False, threaded=True)
    finally:
        cleanup()