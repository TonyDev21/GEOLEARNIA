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

def draw_detection_area(frame):
    """Dibujar área de detección simple y limpia"""
    h, w = frame.shape[:2]
    center_x, center_y = w // 2, h // 2
    
    # Área de análisis - rectángulo más grande y visible
    analysis_size = 250
    top_left = (center_x - analysis_size//2, center_y - analysis_size//2)
    bottom_right = (center_x + analysis_size//2, center_y + analysis_size//2)
    
    # Rectángulo principal - línea más gruesa
    cv2.rectangle(frame, top_left, bottom_right, (0, 255, 255), 3)
    
    # Texto instructivo arriba del rectángulo
    cv2.putText(frame, "COLOCA EL OBJETO AQUI", (center_x - 130, center_y - 140), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
    
    return center_x, center_y, analysis_size

def extract_center_region(frame, center_x, center_y, size):
    """Extraer región central para análisis"""
    h, w = frame.shape[:2]
    
    # Calcular límites de la región central
    half_size = size // 2
    x1 = max(0, center_x - half_size)
    y1 = max(0, center_y - half_size)
    x2 = min(w, center_x + half_size)
    y2 = min(h, center_y + half_size)
    
    # Extraer región
    roi = frame[y1:y2, x1:x2]
    return roi, (x1, y1, x2, y2)

def detect_object_in_center(roi):
    """Detectar objeto en la región central usando contornos"""
    if roi.size == 0:
        return None, None
    
    # Convertir a escala de grises
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
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
    
    # Filtrar contornos muy pequeños (ajustado para área más grande)
    if cv2.contourArea(largest_contour) < 800:
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
    """Procesar frame con detección en zona central"""
    # Dibujar área de detección y obtener coordenadas
    center_x, center_y, analysis_size = draw_detection_area(frame)
    
    # Extraer región central
    roi, (x1, y1, x2, y2) = extract_center_region(frame, center_x, center_y, analysis_size)
    
    # Detectar objeto en la región central
    contour, edges = detect_object_in_center(roi)
    
    prediction_text = ""
    
    if contour is not None:
        # Ajustar contorno a coordenadas globales
        contour_global = contour + np.array([x1, y1])
        
        # Dibujar contorno del objeto detectado
        cv2.drawContours(frame, [contour_global], -1, (0, 255, 0), 2)
        
        # Calcular centro del objeto
        M = cv2.moments(contour)
        if M["m00"] != 0:
            obj_center_x = int(M["m10"] / M["m00"]) + x1
            obj_center_y = int(M["m01"] / M["m00"]) + y1
            
            # Marcar centro del objeto
            cv2.circle(frame, (obj_center_x, obj_center_y), 5, (0, 0, 255), -1)
            
            # Rectángulo alrededor del objeto
            x, y, w, h = cv2.boundingRect(contour_global)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        
        # Predecir forma
        shape_name, confidence = predict_shape(roi)
        
        # Siempre mostrar la predicción si es válida
        if shape_name != "error" and shape_name != "desconocido":
            prediction_text = f"{shape_name.upper()}: {confidence:.1f}%"
            
            # Mostrar predicción con fondo para mejor visibilidad
            text_size = cv2.getTextSize(prediction_text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 2)[0]
            text_x = center_x - text_size[0] // 2
            text_y = center_y + 160
            
            # Fondo para el texto
            cv2.rectangle(frame, (text_x - 10, text_y - 35), (text_x + text_size[0] + 10, text_y + 5), (0, 0, 0), -1)
            
            # Color según la confianza
            if confidence > 30:
                text_color = (0, 255, 0)  # Verde para alta confianza
            else:
                text_color = (0, 255, 255)  # Amarillo para baja confianza
            
            # Texto de predicción
            cv2.putText(frame, prediction_text, (text_x, text_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 1.0, text_color, 2)
        else:
            # Error en predicción
            cv2.putText(frame, "ERROR EN PREDICCION", (center_x - 100, center_y + 160), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    else:
        # Sin objeto detectado
        cv2.putText(frame, "Coloca un objeto en el area", (center_x - 120, center_y + 160), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (128, 128, 128), 2)
    
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
    return render_template('pointer.html')

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
        app.run(host='127.0.0.1', port=5002, debug=False, threaded=True)
        
    except KeyboardInterrupt:
        logger.info("🛑 Deteniendo servidor...")
    except Exception as e:
        logger.error(f"❌ Error: {e}")
    finally:
        cleanup()