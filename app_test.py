#!/usr/bin/env python3
"""
GEOLEARNIA - Versión de prueba local (sin TensorFlow)
"""

import cv2
import numpy as np
from flask import Flask, render_template_string, Response
import logging
import os

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Variables globales
camera = None
class_names = ['circulo', 'cuadrado', 'triangulo']

def initialize_camera():
    """Inicializar la cámara"""
    global camera
    try:
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        camera.set(cv2.CAP_PROP_FPS, 30)
        
        if not camera.isOpened():
            logger.error("❌ No se pudo abrir la cámara")
            return False
        
        logger.info("✅ Cámara inicializada correctamente")
        return True
    except Exception as e:
        logger.error(f"❌ Error inicializando cámara: {e}")
        return False

def detect_object_in_full_frame(frame):
    """Simulación de detección (sin modelo real)"""
    # Simulamos una detección aleatoria para testing
    import random
    shapes = ['circulo', 'cuadrado', 'triangulo']
    confidence = random.uniform(0.7, 0.95)
    detected_shape = random.choice(shapes)
    
    return detected_shape, confidence

def process_frame():
    """Procesar frame y generar respuesta"""
    try:
        if not camera or not camera.isOpened():
            logger.error("❌ Cámara no disponible")
            return None
        
        success, frame = camera.read()
        if not success:
            logger.error("❌ Error capturando frame")
            return None
        
        # Voltear horizontalmente para efecto espejo
        frame = cv2.flip(frame, 1)
        
        # Detectar objeto (simulado)
        detected_shape, confidence = detect_object_in_full_frame(frame)
        
        # Mostrar predicción en la imagen
        cv2.putText(frame, f"Forma: {detected_shape}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f"Confianza: {confidence:.2f}", (10, 70), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        return frame
    except Exception as e:
        logger.error(f"❌ Error procesando frame: {e}")
        return None

def generate_frames():
    """Generar frames para streaming"""
    while True:
        frame = process_frame()
        if frame is None:
            continue
            
        ret, buffer = cv2.imencode('.jpg', frame)
        if not ret:
            continue
            
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    """Página principal"""
    html_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>GEOLEARNIA - Prueba Local</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body { 
                margin: 0; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                font-family: Arial, sans-serif;
                color: white;
                text-align: center;
            }
            .header {
                padding: 20px;
                background: rgba(0,0,0,0.5);
            }
            .video-container {
                width: 100%;
                max-width: 640px;
                margin: 0 auto;
                padding: 20px;
            }
            .video-stream {
                width: 100%;
                height: auto;
                border-radius: 15px;
                box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            }
            .info {
                margin-top: 20px;
                padding: 15px;
                background: rgba(255,255,255,0.1);
                border-radius: 10px;
                backdrop-filter: blur(10px);
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎯 GEOLEARNIA - Prueba Local</h1>
            <p>Versión de prueba sin modelo TensorFlow</p>
        </div>
        <div class="video-container">
            <img src="{{ url_for('video_feed') }}" class="video-stream">
            <div class="info">
                <p>✅ Aplicación funcionando correctamente</p>
                <p>📸 Cámara activa</p>
                <p>🔄 Detección simulada</p>
            </div>
        </div>
    </body>
    </html>
    """
    return render_template_string(html_template)

@app.route('/video_feed')
def video_feed():
    """Endpoint para el stream de video"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    logger.info("🚀 Iniciando GEOLEARNIA - Versión de prueba")
    
    # Inicializar cámara
    if not initialize_camera():
        logger.error("❌ No se pudo inicializar la cámara")
    
    # Ejecutar aplicación
    port = int(os.environ.get('PORT', 5002))
    logger.info(f"🌐 Aplicación disponible en: http://localhost:{port}")
    app.run(host='0.0.0.0', port=port, debug=True)