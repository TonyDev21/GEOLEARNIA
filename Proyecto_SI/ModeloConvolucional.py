import matplotlib.pyplot as plt
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator

#Configurar el ordenador de datos
datos = ImageDataGenerator(
    validation_split=0.2, #El 20% de nuestros datos van a ser utilizados para pruebas
    rescale=1./255 #Normalizamos los datos con valores entre 0 y 1
)

# Generadores para sets de entrenamiento y pruebas
datos_para_entrenamiento = datos.flow_from_directory(
    "dataset",
    target_size=(200, 200), #Modificar el tamaño de las imagenes en pixeles
    batch_size=32,
    shuffle=True,
    subset='training'
)
datos_para_prueba = datos.flow_from_directory(
    'dataset',
    target_size=(200, 200), #Modificar el tamaño de las imagenes en pixeles
    batch_size=32,
    shuffle=True,
    subset='validation'
)



# Definir el modelo
modelo = tf.keras.Sequential([
     # Parte convoluciona
    tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(200, 200, 3)), # Identifica características
    tf.keras.layers.MaxPooling2D(2, 2), # Convertir las características en valores numéricos
    
    tf.keras.layers.Conv2D(64, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),

    tf.keras.layers.Conv2D(128, (3, 3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2, 2),

     # Parte de clasificación
    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(128, activation='relu'), # Aplana las 2 dimensiones
    tf.keras.layers.Dense(3, activation='softmax')
])

# Compilar el modelo
modelo.compile(
    optimizer='adam',
    loss='categorical_crossentropy',
    metrics=['accuracy']
)

# Entrenar el modelo
EPOCAS = 3
historical = modelo.fit(
    datos_para_entrenamiento,
    epochs=EPOCAS,
    batch_size=32,
    validation_data=datos_para_prueba
)

#Código para graficar
acc = historical.history['accuracy']
val_acc = historical.history['val_accuracy']
loss = historical.history['loss']
val_loss = historical.history['val_loss']
rango_epocas = range(EPOCAS)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(rango_epocas, acc, label='Precisión Entrenamiento')
plt.plot(rango_epocas, val_acc, label='Precisión Pruebas')
plt.legend(loc='lower right')
plt.title('Precisión de entrenamiento y pruebas')

plt.subplot(1, 2, 2)
plt.plot(rango_epocas, loss, label='Pérdida de entrenamiento')
plt.plot(rango_epocas, val_loss, label='Pérdida de pruebas')
plt.legend(loc='upper right')
plt.title('Pérdida de entrenamiento y pruebas')
plt.show()

#Exportar modelo
modelo.save('FigurasGeometricas1.h5')


