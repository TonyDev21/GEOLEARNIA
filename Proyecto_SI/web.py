#importar librerias
from flask import Flask, render_template, Response
import cv2
import numpy as np
import tensorflow as tf

# Cargar el modelo preentrenado de figuras geométricas
model = tf.keras.models.load_model("FigurasGeometricas.h5")

# Lista de clases
clases = ['Circulo', 'Cuadrado', 'Triangulo']

#Realizar videocaptura
cap = None
# Variables globales
cap = None
camera_error = None

try:
    print("🔍 Intentando acceder a la cámara...")
    
    # Probar diferentes backends y configuraciones
    backends = [
        (cv2.CAP_DSHOW, "DirectShow"),
        (cv2.CAP_MSMF, "Media Foundation"),
        (cv2.CAP_ANY, "Auto-detect")
    ]
    
    for backend_id, backend_name in backends:
        try:
            print(f"   Probando backend: {backend_name}")
            test_cap = cv2.VideoCapture(0, backend_id)
            
            if test_cap.isOpened():
                # Configurar propiedades
                test_cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                test_cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
                test_cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
                
                # Intentar leer un frame
                ret, test_frame = test_cap.read()
                
                if ret and test_frame is not None:
                    print(f"✅ Cámara inicializada correctamente con {backend_name}")
                    print(f"   Resolución: {test_frame.shape}")
                    cap = test_cap
                    break
                else:
                    print(f"⚠️  {backend_name}: Cámara abierta pero sin frames")
                    test_cap.release()
            else:
                print(f"❌ {backend_name}: No se pudo abrir la cámara")
                test_cap.release()
                
        except Exception as e:
            print(f"❌ Error con {backend_name}: {e}")
            if 'test_cap' in locals():
                test_cap.release()
    
    if cap is None:
        camera_error = "No se pudo inicializar la cámara con ningún backend"
        print(f"⚠️  {camera_error}")
        print("   La aplicación funcionará sin video en tiempo real")
        
except Exception as e:
    camera_error = f"Error general al acceder a la cámara: {e}"
    print(f"❌ {camera_error}")
    print("   La aplicación funcionará sin video en tiempo real")

# Función para realizar la predicción con el modelo
def predict_shape(frame, model):
    # Redimensionar el fotograma al tamaño esperado por el modelo
    resized_frame = cv2.resize(frame, (200, 200)) 
    # Normalizar el fotograma
    normalized_frame = resized_frame / 255.0 
    # Hacer la predicción
    predictions = model.predict(np.expand_dims(normalized_frame, axis=0))
    # Obtener el índice de la clase con mayor probabilidad
    predicted_class_idx = np.argmax(predictions[0]) 
    # Obtener el nombre de la clase predicha
    predicted_class = clases[predicted_class_idx]
    
    return predicted_class

# Función para realizar la predicción con detección visual
def predict_shape_with_detection(frame, model):
    # Crear una copia del frame para dibujar
    display_frame = frame.copy()
    
    # Convertir a escala de grises para detección de contornos
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Aplicar desenfoque para reducir ruido
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Detectar bordes
    edges = cv2.Canny(blurred, 50, 150)
    
    # Encontrar contornos
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Realizar predicción con el modelo
    resized_frame = cv2.resize(frame, (200, 200))
    normalized_frame = resized_frame / 255.0
    predictions = model.predict(np.expand_dims(normalized_frame, axis=0))
    predicted_class_idx = np.argmax(predictions[0])
    predicted_class = clases[predicted_class_idx]
    confidence = predictions[0][predicted_class_idx] * 100
    
    # Encontrar el contorno más grande (probablemente la figura principal)
    if contours:
        # Filtrar contornos por área mínima
        min_area = 500
        valid_contours = [c for c in contours if cv2.contourArea(c) > min_area]
        
        if valid_contours:
            # Obtener el contorno más grande
            largest_contour = max(valid_contours, key=cv2.contourArea)
            
            # Dibujar el contorno
            cv2.drawContours(display_frame, [largest_contour], -1, (0, 255, 0), 3)
            
            # Obtener el rectángulo delimitador
            x, y, w, h = cv2.boundingRect(largest_contour)
            
            # Dibujar rectángulo delimitador
            cv2.rectangle(display_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            # Calcular centro del contorno
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                # Dibujar punto central
                cv2.circle(display_frame, (cx, cy), 8, (0, 0, 255), -1)
                
                # Dibujar flecha apuntando al centro
                cv2.arrowedLine(display_frame, (cx - 50, cy - 50), (cx - 10, cy - 10), (0, 255, 255), 3)
                
                # Mostrar texto con la predicción cerca del objeto
                label_text = f"{predicted_class} ({confidence:.1f}%)"
                text_x = max(x, 10)
                text_y = max(y - 10, 30)
                
                # Fondo para el texto
                (text_width, text_height), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.8, 2)
                cv2.rectangle(display_frame, (text_x - 5, text_y - text_height - 5), 
                            (text_x + text_width + 5, text_y + 5), (0, 0, 0), -1)
                
                # Texto de predicción
                cv2.putText(display_frame, label_text, (text_x, text_y), 
                          cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    # Mostrar información general en la esquina superior
    info_text = f"Detectando: {predicted_class}"
    cv2.putText(display_frame, info_text, (10, 30), 
              cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    
    # Mostrar instrucciones
    cv2.putText(display_frame, "Coloca una figura geometrica frente a la camara", (10, display_frame.shape[0] - 15), 
              cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    return predicted_class, display_frame

# Función SIMPLE para generar frames sin detección compleja
def generar_frames():
    global cap
    
    print("🎥 generar_frames() SIMPLE llamada")
    print(f"📷 Estado de cap: {cap}")
    
    if cap is None or not cap.isOpened():
        # Sin cámara - imagen de error simple
        print("❌ Cámara no disponible - enviando imagen de error")
        error_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        cv2.putText(error_frame, "CAMARA NO DISPONIBLE", (120, 200), 
                   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(error_frame, "Verifica la conexion", (150, 250), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        
        success, buffer = cv2.imencode('.jpg', error_frame)
        if success:
            frame_bytes = buffer.tobytes()
            while True:
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                import time
                time.sleep(1)
    else:
        # Con cámara - stream simple sin detección compleja
        print("✅ Iniciando stream SIMPLE")
        frame_count = 0
        
        while True:
            try:
                ret, frame = cap.read()
                
                if not ret:
                    print(f"❌ Error leyendo frame {frame_count + 1}")
                    break
                
                frame_count += 1
                
                # Log cada 30 frames
                if frame_count == 1 or frame_count % 30 == 0:
                    print(f"📹 Frame {frame_count} - Sum: {np.sum(frame)}")
                
                # Verificar que el frame no esté completamente negro
                if np.sum(frame) == 0:
                    print(f"⚠️  Frame {frame_count} está completamente negro")
                    continue
                
                # Hacer predicción SIMPLE
                try:
                    resized_frame = cv2.resize(frame, (200, 200))
                    normalized_frame = resized_frame / 255.0
                    predictions = model.predict(np.expand_dims(normalized_frame, axis=0))
                    predicted_class_idx = np.argmax(predictions[0])
                    predicted_class = clases[predicted_class_idx]
                    confidence = predictions[0][predicted_class_idx] * 100
                    
                    # Agregar SOLO texto simple
                    cv2.putText(frame, f"Figura: {predicted_class} ({confidence:.1f}%)", 
                              (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                    
                    cv2.putText(frame, "Coloca una figura frente a la camara", 
                              (10, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
                    
                except Exception as e:
                    print(f"⚠️  Error en predicción: {e}")
                    cv2.putText(frame, "Detectando...", (10, 30), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 0), 2)
                
                # Codificar como JPEG con buena calidad
                success, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
                
                if not success:
                    print(f"❌ Error codificando frame {frame_count}")
                    continue
                
                frame_bytes = buffer.tobytes()
                
                # Log del primer frame
                if frame_count == 1:
                    print(f"✅ Primer frame OK - {len(frame_bytes)} bytes")
                
                # Enviar frame
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                
            except Exception as e:
                print(f"❌ Error en loop: {e}")
                break
        
        # Crear imagen de placeholder
        img = Image.new('RGB', (640, 480), color=(60, 60, 60))
        draw = ImageDraw.Draw(img)
        
        # Texto informativo
        text_lines = [
            "CÁMARA NO DISPONIBLE",
            "",
            "Por favor verifica:",
            "• Que la cámara esté conectada",
            "• Permisos de cámara habilitados",
            "• Ninguna otra app use la cámara"
        ]
        
        y_position = 150
        for line in text_lines:
            draw.text((50, y_position), line, fill=(255, 255, 255))
            y_position += 30
        
        # Convertir a bytes
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG')
        frame_bytes = img_buffer.getvalue()
        
        while True:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            import time
            time.sleep(1)  # Actualizar cada segundo
    else:
        # Con cámara - funcionamiento normal
        print("✅ Iniciando stream de video con cámara")
        print(f"📹 Verificando cámara antes del loop...")
        
        # Test de lectura inicial
        test_ret, test_frame = cap.read()
        if not test_ret:
            print("❌ PROBLEMA: No se puede leer de la cámara en el primer intento")
            print("🔄 Intentando reinicializar la cámara...")
            cap.release()
            import time
            time.sleep(0.5)
            cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            test_ret, test_frame = cap.read()
            
        if test_ret:
            print(f"✅ Cámara OK - Frame size: {test_frame.shape}")
        else:
            print("❌ CRÍTICO: Cámara no responde después de reinicialización")
            
        frame_count = 0
        
        while True:
            try:
                ret, frame = cap.read()
                if not ret:
                    print(f"❌ No se pudo leer frame de la cámara (intento {frame_count + 1})")
                    # Intentar reconectarse
                    if frame_count == 0:
                        print("🔄 Intentando reconectar cámara...")
                        cap.release()
                        import time
                        time.sleep(1)
                        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
                        continue
                    else:
                        print("❌ Cámara perdida durante streaming")
                        break
                
                frame_count += 1
                if frame_count == 1:
                    print(f"🎉 ¡PRIMER FRAME LEÍDO EXITOSAMENTE! Size: {frame.shape}")
                if frame_count % 30 == 0:  # Log cada 30 frames (~1 segundo)
                    print(f"📹 Frame {frame_count} procesado exitosamente")
                
                # Realizar predicción y detección visual
                try:
                    predicted_class, detection_frame = predict_shape_with_detection(frame, model)
                    frame = detection_frame  # Usar el frame con la detección visual
                    
                except Exception as e:
                    print(f"❌ Error en predicción: {e}")
                    cv2.putText(frame, "Error en prediccion", 
                              (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
                # Codificar frame como JPEG
                try:
                    success, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                    if not success:
                        print("❌ Error al codificar frame como JPEG")
                        continue
                        
                    frame_bytes = buffer.tobytes()
                    if frame_count == 1:
                        print(f"✅ Frame codificado - Tamaño: {len(frame_bytes)} bytes")

                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
                           
                except Exception as e:
                    print(f"❌ Error al codificar/enviar frame: {e}")
                    continue
                       
            except Exception as e:
                print(f"❌ Error en el loop de video: {e}")
                import traceback
                traceback.print_exc()
                break

#Crear la app
app = Flask(__name__)

#Ruta principal
@app.route('/')
def index():
    print("🌐 Acceso a página principal")
    return render_template('index.html')

@app.route('/test')
def test():
    print("🧪 Acceso a página de test simple")
    return render_template('test_simple.html')

@app.route('/video')
def video():
    print("📹 Solicitando stream de video")
    print(f"📷 Estado de cámara en /video: cap={cap}, isOpened={cap.isOpened() if cap else 'N/A'}")
    try:
        response = Response(generar_frames(), 
                       mimetype='multipart/x-mixed-replace; boundary=frame')
        print("✅ Response de video creada exitosamente")
        return response
    except Exception as e:
        print(f"❌ Error en ruta de video: {e}")
        import traceback
        traceback.print_exc()
        return f"Error en stream de video: {e}", 500

#Ejecutar
if __name__=='__main__':
    print("🎓 GEOLEARNIA - Aplicación Web")
    print("================================")
    print("🌐 Servidor Flask iniciando...")
    print(f"📱 URL: http://127.0.0.1:5001")
    if cap and cap.isOpened():
        print("📷 Estado de cámara: ✅ Disponible")
    else:
        print("📷 Estado de cámara: ⚠️  No disponible")
        if camera_error:
            print(f"   Error: {camera_error}")
    print("🤖 TensorFlow cargado exitosamente")
    print("================================")
    app.run(debug=True, port=5001, host='127.0.0.1')

#Ruta para vizualizar el modulo 1 en la web: http://127.0.0.1:5000/