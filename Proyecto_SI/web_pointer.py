#!/usr/bin/env python3
"""
GEOLEARNIA - Sistema de Reconocimiento con PUNTERO CENTRAL
Versión optimizada con zona de análisis específica en el centro
"""

import cv2
import numpy as np
from flask import Flask, render_template_string, render_template, Response
import tensorflow as tf
from tensorflow import keras
import logging
import os

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Variables globales
model = None
camera = None
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
        return False

def initialize_camera():
    """Inicializar la cámara"""
    global camera
    try:
        camera = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        camera.set(cv2.CAP_PROP_FPS, 30)
        
        if not camera.isOpened():
            logger.error("❌ No se puede abrir la cámara")
            return False
        
        logger.info("✅ Cámara inicializada")
        return True
    except Exception as e:
        logger.error(f"❌ Error inicializando cámara: {e}")
        return False

def get_full_frame_info(frame):
    """Obtener información del frame completo para análisis"""
    h, w = frame.shape[:2]
    center_x, center_y = w // 2, h // 2
    
    # Ya no hay área específica - usar todo el frame
    # Sin texto adicional - solo análisis de la imagen completa
    
    return center_x, center_y, min(h, w)  # Usar toda la imagen

def get_full_frame_region(frame):
    """Usar todo el frame para análisis - sin restricciones de área"""
    h, w = frame.shape[:2]
    
    # Devolver todo el frame como región de interés
    return frame, (0, 0, w, h)

def detect_object_in_full_frame(frame):
    """Detectar objeto en todo el frame usando contornos"""
    if frame.size == 0:
        return None, None
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicar desenfoque para suavizar
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detección de bordes
    edges = cv2.Canny(blurred, 50, 150)
    
    # Encontrar contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return None, None
    
    # Obtener el contorno más grande
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Filtrar contornos muy pequeños (área mínima para detección)
    if cv2.contourArea(largest_contour) < 1000:
        return None, None
    
    return largest_contour, edges

def predict_shape(roi):
    """Predecir la forma usando el modelo de TensorFlow"""
    global model
    
    if model is None or roi.size == 0:
        return "desconocido", 0.0
    
    try:
        # Redimensionar para el modelo (200x200 como el original)
        resized = cv2.resize(roi, (200, 200))
        
        # Normalizar (como en el modelo original)
        normalized = resized.astype(np.float32) / 255.0
        
        # Expandir dimensiones para el modelo
        input_array = np.expand_dims(normalized, axis=0)
        
        # Predicción
        predictions = model.predict(input_array, verbose=0)
        
        # Obtener clase y confianza
        predicted_class_idx = np.argmax(predictions[0])
        confidence = np.max(predictions[0]) * 100
        
        # Verificar que el índice está en rango
        if predicted_class_idx < len(class_names):
            shape_name = class_names[predicted_class_idx]
        else:
            shape_name = "desconocido"
        
        return shape_name, confidence
    
    except Exception as e:
        logger.error(f"Error en predicción: {e}")
        return "error", 0.0

def process_frame(frame):
    """Procesar frame con detección en todo el área"""
    # Obtener información del frame completo y agregar texto discreto
    center_x, center_y, frame_size = get_full_frame_info(frame)
    
    # Usar todo el frame como región de interés
    roi, (x1, y1, x2, y2) = get_full_frame_region(frame)
    
    # Detectar objeto en todo el frame
    contour, edges = detect_object_in_full_frame(frame)
    
    prediction_text = ""
    
    if contour is not None:
        # El contorno ya está en coordenadas globales (todo el frame)
        contour_global = contour
        
        # Dibujar contorno del objeto detectado
        cv2.drawContours(frame, [contour_global], -1, (0, 255, 0), 3)
        
        # Calcular centro del objeto
        M = cv2.moments(contour)
        if M["m00"] != 0:
            obj_center_x = int(M["m10"] / M["m00"])
            obj_center_y = int(M["m01"] / M["m00"])
            
            # Marcar centro del objeto
            cv2.circle(frame, (obj_center_x, obj_center_y), 8, (0, 0, 255), -1)
            
            # Rectángulo alrededor del objeto
            x, y, w, h = cv2.boundingRect(contour_global)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Predecir forma usando todo el frame
        shape_name, confidence = predict_shape(frame)
        
        # Siempre mostrar la predicción si es válida
        if shape_name != "error" and shape_name != "desconocido":
            prediction_text = f"{shape_name.upper()}: {confidence:.1f}%"
            
            # Mostrar predicción en la parte inferior del frame
            h, w = frame.shape[:2]
            text_size = cv2.getTextSize(prediction_text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
            text_x = (w - text_size[0]) // 2  # Centrar horizontalmente
            text_y = h - 30  # Posición en la parte inferior (30px desde abajo)
            
            # Fondo para el texto
            cv2.rectangle(frame, (text_x - 15, text_y - 40), (text_x + text_size[0] + 15, text_y + 10), (0, 0, 0), -1)
            
            # Color según la confianza
            if confidence > 70:
                text_color = (0, 255, 0)  # Verde para alta confianza
            elif confidence > 40:
                text_color = (0, 255, 255)  # Amarillo para confianza media
            else:
                text_color = (255, 255, 255)  # Blanco para baja confianza
            
            # Texto de predicción
            cv2.putText(frame, prediction_text, (text_x, text_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.2, text_color, 3)
    else:
        # Sin objeto detectado - mensaje discreto en la parte inferior
        h, w = frame.shape[:2]
        message = "Muestra una figura geometrica"
        text_size = cv2.getTextSize(message, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)[0]
        text_x = (w - text_size[0]) // 2  # Centrar horizontalmente
        text_y = h - 25  # Posición en la parte inferior
        
        # Fondo sutil para el mensaje
        cv2.rectangle(frame, (text_x - 10, text_y - 30), (text_x + text_size[0] + 10, text_y + 5), (50, 50, 50), -1)
        cv2.putText(frame, message, (text_x, text_y), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (200, 200, 200), 2)
    
    return frame

def generate_frames():
    """Generador de frames para streaming"""
    global camera
    
    if camera is None:
        logger.error("❌ Cámara no inicializada")
        return
    
    frame_count = 0
    
    while True:
        try:
            success, frame = camera.read()
            if not success:
                logger.error("❌ Error leyendo frame")
                break
            
            frame_count += 1
            
            # Voltear horizontalmente para efecto espejo
            frame = cv2.flip(frame, 1)
            
            # Procesar frame con detección central
            processed_frame = process_frame(frame)
            
            # Codificar frame
            ret, buffer = cv2.imencode('.jpg', processed_frame, 
                                     [cv2.IMWRITE_JPEG_QUALITY, 85])
            
            if not ret:
                continue
            
            # Estadísticas cada 100 frames
            if frame_count % 100 == 0:
                frame_sum = np.sum(processed_frame)
                logger.info(f"📹 Frame {frame_count} OK - Sum: {frame_sum}")
            
            # Convertir a bytes para streaming
            frame_bytes = buffer.tobytes()
            
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        
        except Exception as e:
            logger.error(f"❌ Error en generate_frames: {e}")
            break

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html')

@app.route('/video')
def video():
    """Ruta para el feed de video (compatibilidad con template)"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed')
def video_feed():
    """Ruta para el feed de video"""
    return Response(generate_frames(),
                   mimetype='multipart/x-mixed-replace; boundary=frame')

def cleanup():
    """Limpiar recursos"""
    global camera
    if camera is not None:
        camera.release()
        logger.info("✅ Cámara liberada")

if __name__ == '__main__':
    try:
        logger.info("🎯 Iniciando GEOLEARNIA - Puntero Central")
        
        # Cargar modelo
        if not load_model():
            logger.error("❌ No se pudo cargar el modelo")
            exit(1)
        
        # Inicializar cámara
        if not initialize_camera():
            logger.error("❌ No se pudo inicializar la cámara")
            exit(1)
        
        logger.info("🌐 Iniciando servidor en http://127.0.0.1:5002")
        logger.info("🎯 Coloca objetos en el puntero central para detectarlos")
        
        # Ejecutar aplicación
        import os
        port = int(os.environ.get('PORT', 5002))
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
        
    except KeyboardInterrupt:
        logger.info("🛑 Deteniendo servidor...")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
    finally:
        cleanup()