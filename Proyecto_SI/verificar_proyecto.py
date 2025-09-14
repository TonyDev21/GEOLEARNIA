#!/usr/bin/env python3
# Script para verificar que la aplicación web Flask funciona

import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("🔄 Verificando importaciones...")
    
    # Verificar Flask
    from flask import Flask
    print("✅ Flask importado correctamente")
    
    # Verificar OpenCV
    import cv2
    print("✅ OpenCV importado correctamente")
    
    # Verificar TensorFlow
    import tensorflow as tf
    print("✅ TensorFlow importado correctamente")
    
    # Verificar numpy
    import numpy as np
    print("✅ NumPy importado correctamente")
    
    # Verificar que el modelo existe
    if os.path.exists("FigurasGeometricas.h5"):
        print("✅ Modelo FigurasGeometricas.h5 encontrado")
        
        # Intentar cargar el modelo
        model = tf.keras.models.load_model("FigurasGeometricas.h5")
        print("✅ Modelo cargado exitosamente")
        
        # Verificar las clases
        clases = ['Circulo', 'Cuadrado', 'Triangulo']
        print(f"✅ Clases configuradas: {clases}")
        
    else:
        print("❌ Modelo FigurasGeometricas.h5 NO encontrado")
    
    # Verificar que existe la carpeta de templates
    if os.path.exists("templates"):
        print("✅ Carpeta templates encontrada")
    else:
        print("❌ Carpeta templates NO encontrada")
    
    # Verificar que existe la carpeta static
    if os.path.exists("static"):
        print("✅ Carpeta static encontrada")
    else:
        print("❌ Carpeta static NO encontrada")
    
    print("\n🎉 ¡Todas las verificaciones pasaron exitosamente!")
    print("📝 La aplicación web está lista para ejecutarse")
    print("💡 Para ejecutar la aplicación web:")
    print("   python web.py")
    print("💡 Para ejecutar la aplicación de escritorio:")
    print("   python Video2.py")
    print("💡 Para ejecutar detección básica sin IA:")
    print("   python IA.py")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
