#!/usr/bin/env python3
"""
Script para ejecutar GEOLEARNIA con Sistema de Puntero Central
Versión optimizada para detección precisa en zona específica
"""

import os
import sys
import subprocess

def main():
    """Función principal para iniciar el servidor con puntero central"""
    
    print("🎯 Iniciando GEOLEARNIA con SISTEMA DE PUNTERO CENTRAL...")
    
    # Obtener directorio actual
    current_dir = os.getcwd()
    print(f"📁 Directorio: {current_dir}")
    
    # Verificar entorno virtual
    venv_path = os.path.join(current_dir, '.venv')
    if os.path.exists(venv_path):
        venv_python = os.path.join(venv_path, 'Scripts', 'python.exe')
        print(f"🐍 Python: {venv_python}")
    else:
        venv_python = 'python'
        print("⚠️  Usando Python del sistema")
    
    # Ruta del archivo de la aplicación
    app_path = os.path.join(current_dir, 'Proyecto_SI', 'web_pointer.py')
    print(f"📄 Aplicación: {app_path}")
    
    # Verificar que existe el archivo
    if not os.path.exists(app_path):
        print(f"❌ Error: No se encuentra {app_path}")
        return
    
    # Cambiar al directorio del proyecto
    project_dir = os.path.join(current_dir, 'Proyecto_SI')
    print(f"📂 Cambiando a: {project_dir}")
    os.chdir(project_dir)
    
    print("🎯 Iniciando servidor con puntero central...")
    print("🔍 Funciones incluidas:")
    print("   • Puntero fijo en el centro")
    print("   • Zona de análisis específica")
    print("   • Cruz amarilla de referencia")
    print("   • Rectángulo de área de detección")
    print("   • Detección solo cuando el objeto está centrado")
    print("   • Contorno verde alrededor del objeto")
    print("   • Punto rojo en el centro del objeto")
    print("   • Predicción con porcentaje de confianza")
    print()
    print("🌐 Ejecutando en http://127.0.0.1:5002")
    print("🎯 INSTRUCCIONES:")
    print("   1. Coloca el objeto en la cruz amarilla central")
    print("   2. Ajusta hasta que quede dentro del rectángulo azul")
    print("   3. La detección será más precisa y no detectará el fondo")
    print()
    
    # Ejecutar la aplicación
    try:
        subprocess.run([venv_python, 'web_pointer.py'])
    except KeyboardInterrupt:
        print("\n🛑 Servidor detenido por el usuario")
    except Exception as e:
        print(f"❌ Error ejecutando aplicación: {e}")

if __name__ == "__main__":
    main()