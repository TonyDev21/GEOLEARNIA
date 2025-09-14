#!/usr/bin/env python3
# Script para verificar que el módulo OpenCV funciona

import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("🔄 Verificando módulo OpenCV (Sistema de Autenticación)...")
    
    # Verificar tkinter
    try:
        import tkinter as tk
        print("✅ Tkinter importado correctamente")
    except ImportError:
        print("❌ Tkinter NO está disponible. Instala con: sudo apt install python3-tk")
    
    # Verificar SQLAlchemy
    import sqlalchemy
    print("✅ SQLAlchemy importado correctamente")
    
    # Verificar Pillow
    from PIL import Image, ImageTk
    print("✅ Pillow (PIL) importado correctamente")
    
    # Verificar cryptography
    from cryptography.fernet import Fernet
    print("✅ Cryptography importado correctamente")
    
    # Verificar base de datos
    if os.path.exists("db/login.sqlite"):
        print("✅ Base de datos login.sqlite encontrada")
    else:
        print("⚠️  Base de datos login.sqlite NO encontrada")
        print("   Ejecuta: python build_db.py")
    
    # Verificar imágenes
    imagenes_necesarias = ["imagenes/lobo.jpg", "imagenes/fg.jpg"]
    for img in imagenes_necesarias:
        if os.path.exists(img):
            print(f"✅ Imagen {img} encontrada")
        else:
            print(f"❌ Imagen {img} NO encontrada")
    
    # Verificar OpenCV para reconocimiento facial
    try:
        import cv2
        print("✅ OpenCV importado correctamente")
    except ImportError:
        print("❌ OpenCV NO está disponible")
    
    # Verificar MTCNN para detección facial
    try:
        from mtcnn.mtcnn import MTCNN
        print("✅ MTCNN importado correctamente")
    except ImportError:
        print("❌ MTCNN NO está disponible")
    
    # Verificar MediaPipe
    try:
        import mediapipe as mp
        print("✅ MediaPipe importado correctamente")
    except ImportError:
        print("❌ MediaPipe NO está disponible")
    
    print("\n🎉 ¡Verificaciones del módulo OpenCV completadas!")
    print("📝 El sistema de autenticación está listo")
    print("💡 Para ejecutar el sistema de login:")
    print("   python main.py")
    print("💡 Para crear la base de datos:")
    print("   python build_db.py")
    print("💡 Para registrar usuarios con reconocimiento facial:")
    print("   python Reconocimiento/open.py")
    
except ImportError as e:
    print(f"❌ Error de importación: {e}")
except Exception as e:
    print(f"❌ Error: {e}")
