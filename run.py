#!/usr/bin/env python3
"""
GEOLEARNIA Runner Script
========================

Script principal para ejecutar las diferentes aplicaciones del proyecto GEOLEARNIA.

Uso:
    python run.py                    # Menú interactivo
    python run.py --web             # Aplicación web
    python run.py --desktop         # Aplicación de escritorio
    python run.py --auth            # Sistema de autenticación
    python run.py --facial          # Reconocimiento facial
    
Autor: GEOLEARNIA Team
"""

import os
import sys
import argparse
import subprocess
import platform
from pathlib import Path

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_colored(message, color=Colors.OKGREEN):
    """Imprimir mensaje con color"""
    print(f"{color}{message}{Colors.ENDC}")

def print_header(message):
    """Imprimir encabezado"""
    print_colored(f"\n{'='*50}", Colors.HEADER)
    print_colored(f" {message}", Colors.HEADER)
    print_colored(f"{'='*50}", Colors.HEADER)

def get_python_command():
    """Obtener comando Python del entorno virtual"""
    if platform.system().lower() == "windows":
        return Path(".venv/Scripts/python")
    else:
        return Path(".venv/bin/python")

def check_environment():
    """Verificar que el entorno esté configurado"""
    python_cmd = get_python_command()
    
    if not python_cmd.exists():
        print_colored("❌ Entorno virtual no encontrado", Colors.FAIL)
        print_colored("   Ejecuta primero: python setup.py", Colors.WARNING)
        return False
    
    # Verificar dependencias básicas
    try:
        result = subprocess.run([str(python_cmd), "-c", "import tensorflow, cv2, flask"],
                              capture_output=True, text=True)
        if result.returncode != 0:
            print_colored("❌ Dependencias no instaladas correctamente", Colors.FAIL)
            print_colored("   Ejecuta: python setup.py", Colors.WARNING)
            return False
    except Exception:
        print_colored("❌ Error verificando dependencias", Colors.FAIL)
        return False
    
    return True

def run_web_app():
    """Ejecutar aplicación web"""
    print_header("INICIANDO APLICACIÓN WEB")
    print_colored("🌐 Iniciando servidor Flask...")
    print_colored("📱 La aplicación estará disponible en: http://127.0.0.1:5001")
    print_colored("⏹️  Presiona Ctrl+C para detener")
    
    python_cmd = get_python_command()
    os.chdir("Proyecto_SI")
    
    try:
        subprocess.run([str(python_cmd), "web.py"])
    except KeyboardInterrupt:
        print_colored("\n🛑 Aplicación web detenida", Colors.WARNING)
    finally:
        os.chdir("..")

def run_desktop_app():
    """Ejecutar aplicación de escritorio"""
    print_header("INICIANDO APLICACIÓN DE ESCRITORIO")
    print_colored("🖥️  Iniciando interfaz Tkinter...")
    print_colored("⏹️  Cierra la ventana para terminar")
    
    python_cmd = get_python_command()
    os.chdir("Proyecto_SI")
    
    try:
        subprocess.run([str(python_cmd), "Video2.py"])
    except KeyboardInterrupt:
        print_colored("\n🛑 Aplicación de escritorio detenida", Colors.WARNING)
    finally:
        os.chdir("..")

def run_auth_system():
    """Ejecutar sistema de autenticación"""
    print_header("INICIANDO SISTEMA DE AUTENTICACIÓN")
    print_colored("🔐 Iniciando sistema de login...")
    print_colored("⏹️  Cierra la ventana para terminar")
    
    python_cmd = get_python_command()
    os.chdir("OpenCV")
    
    try:
        subprocess.run([str(python_cmd), "main.py"])
    except KeyboardInterrupt:
        print_colored("\n🛑 Sistema de autenticación detenido", Colors.WARNING)
    finally:
        os.chdir("..")

def run_facial_recognition():
    """Ejecutar reconocimiento facial"""
    print_header("INICIANDO RECONOCIMIENTO FACIAL")
    print_colored("👤 Iniciando sistema de reconocimiento facial...")
    print_colored("📷 Asegúrate de tener una cámara conectada")
    print_colored("⏹️  Presiona ESC en la ventana de video para terminar")
    
    python_cmd = get_python_command()
    os.chdir("OpenCV/Reconocimiento")
    
    try:
        subprocess.run([str(python_cmd), "open.py"])
    except KeyboardInterrupt:
        print_colored("\n🛑 Reconocimiento facial detenido", Colors.WARNING)
    finally:
        os.chdir("../..")

def run_basic_detection():
    """Ejecutar detección básica sin IA"""
    print_header("INICIANDO DETECCIÓN BÁSICA")
    print_colored("🔍 Iniciando detección por contornos...")
    print_colored("📷 Asegúrate de tener una cámara conectada")
    print_colored("⏹️  Presiona ESC en la ventana de video para terminar")
    
    python_cmd = get_python_command()
    os.chdir("Proyecto_SI")
    
    try:
        subprocess.run([str(python_cmd), "IA.py"])
    except KeyboardInterrupt:
        print_colored("\n🛑 Detección básica detenida", Colors.WARNING)
    finally:
        os.chdir("..")

def show_interactive_menu():
    """Mostrar menú interactivo"""
    while True:
        print_header("🎓 GEOLEARNIA - MENÚ PRINCIPAL")
        print_colored("Selecciona una opción:", Colors.OKBLUE)
        print()
        print_colored("1. 🌐 Aplicación Web (Recomendado)", Colors.OKCYAN)
        print_colored("2. 🖥️  Aplicación de Escritorio", Colors.OKCYAN)
        print_colored("3. 🔐 Sistema de Autenticación", Colors.OKCYAN)
        print_colored("4. 👤 Reconocimiento Facial", Colors.OKCYAN)
        print_colored("5. 🔍 Detección Básica (sin IA)", Colors.OKCYAN)
        print_colored("6. ❌ Salir", Colors.WARNING)
        print()
        
        try:
            choice = input("Ingresa tu opción (1-6): ").strip()
            
            if choice == "1":
                run_web_app()
            elif choice == "2":
                run_desktop_app()
            elif choice == "3":
                run_auth_system()
            elif choice == "4":
                run_facial_recognition()
            elif choice == "5":
                run_basic_detection()
            elif choice == "6":
                print_colored("👋 ¡Hasta luego!", Colors.OKGREEN)
                break
            else:
                print_colored("❌ Opción inválida. Intenta de nuevo.", Colors.FAIL)
                
        except KeyboardInterrupt:
            print_colored("\n👋 ¡Hasta luego!", Colors.OKGREEN)
            break
        except Exception as e:
            print_colored(f"❌ Error: {e}", Colors.FAIL)

def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="GEOLEARNIA Runner - Ejecutar aplicaciones del proyecto")
    parser.add_argument("--web", action="store_true", help="Ejecutar aplicación web")
    parser.add_argument("--desktop", action="store_true", help="Ejecutar aplicación de escritorio")
    parser.add_argument("--auth", action="store_true", help="Ejecutar sistema de autenticación")
    parser.add_argument("--facial", action="store_true", help="Ejecutar reconocimiento facial")
    parser.add_argument("--basic", action="store_true", help="Ejecutar detección básica")
    
    args = parser.parse_args()
    
    # Verificar entorno
    if not check_environment():
        sys.exit(1)
    
    # Ejecutar según argumentos
    if args.web:
        run_web_app()
    elif args.desktop:
        run_desktop_app()
    elif args.auth:
        run_auth_system()
    elif args.facial:
        run_facial_recognition()
    elif args.basic:
        run_basic_detection()
    else:
        # Menú interactivo si no hay argumentos
        show_interactive_menu()

if __name__ == "__main__":
    main()
