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
cap = cv2.VideoCapture(0)

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

# Función para generar frames con la predicción de figuras geométricas
def generar_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        else:
            predicted_class = predict_shape(frame,model)
            cv2.putText(frame, predicted_class, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

#Crear la app
app= Flask(__name__)

#Ruta principal
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generar_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

#Ejecutar
if __name__=='__main__':
    app.run(debug=True, port=5001)

#Ruta para vizualizar el modulo 1 en la web: http://127.0.0.1:5000/