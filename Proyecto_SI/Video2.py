from tkinter import Tk, Label, Button, PhotoImage #Botones y textos de la interfaz(diseño)
import cv2 #Manejo de la camara
import numpy as np #Operaciones numericas
import tensorflow as tf #Cargar el modelo
from PIL import Image, ImageTk #Manipular imagenes


# Lista de clases
clases = ['Circulo', 'Cuadrado', 'Triangulo']

# Cargar el modelo preentrenado
model = tf.keras.models.load_model("FigurasGeometricas.h5")

# Inicializar la cámara, el argumento 1 indica la camra que se usara
camara = cv2.VideoCapture(0)


# Función para realizar la predicción
def predict_shapes(frame, model):
    
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

# Función para mostrar el video en tiempo real con la predicción
def mostrar_video():
    ret, frame = camara.read()
    if ret:
        # Hacer la predicción
        predicted_class = predict_shapes(frame, model)
        
        # Dibujar el nombre de la figura en el fotograma
        cv2.putText(frame, predicted_class, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        
        # Mostrar el fotograma en la interfaz
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        imgtk = ImageTk.PhotoImage(image=img)
        lblVideo.imgtk = imgtk # type: ignore
        lblVideo.config(image=imgtk)
        
        # Llamar a la función mostrar_video() después de 10 ms
        lblVideo.after(10, mostrar_video)
        
def iniciar_prediccion():
    # Seleccionamos la cámara
    camara.open
    mostrar_video()
    print("Inicio")

# Función para detener la predicción y cerrar la ventana
def detener_prediccion():
    # Abrir la camara
    camara.release()
    # Cerrar la ventana
    pantalla.destroy()

# Inicializar la ventana Tkinter/ ventana principal de la interfaz
pantalla = Tk()
pantalla.title("Predicción de Figuras Geométricas")
pantalla.geometry("1280x720") #dimension de la pantalla

# Fondo de la pantalla
imagenFondo = PhotoImage(file="fon.png")
background = Label(image=imagenFondo, text="Fondo")
background.place(x = 0, y = 0, relwidth=1, relheight=1)

#Boton para iniciar la prediccion
imagenInicio = PhotoImage(file="start.png")
inicio=Button(pantalla, text="Iniciar", image=imagenInicio, height="90", width="160", command=iniciar_prediccion)
inicio.place(x = 100, y = 250)

# Botón para detener la predicción
imagenFinalizar = PhotoImage(file="finish.png")
detener_button = Button(pantalla, text="Detener Predicción",image=imagenFinalizar, command=detener_prediccion)
detener_button.place(x = 100, y = 450)
# Etiqueta en la interfaz para mostrar el video
lblVideo = Label(pantalla)
lblVideo.place(x = 320, y = 50)
pantalla.mainloop()




