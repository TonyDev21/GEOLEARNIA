#!/usr/bin/env python3
"""
GEOLEARNIA Setup Script
======================

Script de instalación automatizada para el proyecto GEOLEARNIA.
Configura el entorno virtual, instala dependencias y verifica la instalación.

Uso:
    python setup.py
    
Autor: GEOLEARNIA Team
"""

import os
import sys
import subprocess
import platform
import venv
from pathlib import Path

class Colors:
    """Colores para output en terminal"""
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
    print_colored(f"\n{'='*60}", Colors.HEADER)
    print_colored(f" {message}", Colors.HEADER)
    print_colored(f"{'='*60}", Colors.HEADER)

def run_command(command, description="", check=True):
    """Ejecutar comando del sistema"""
    if description:
        print_colored(f"🔄 {description}...", Colors.OKCYAN)
    
    try:
        result = subprocess.run(command, shell=True, check=check, 
                              capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print_colored(f"❌ Error: {e}", Colors.FAIL)
        if e.stderr:
            print_colored(f"Error details: {e.stderr}", Colors.FAIL)
        return False

def check_python_version():
    """Verificar versión de Python"""
    print_header("VERIFICANDO PYTHON")
    
    version = sys.version_info
    print_colored(f"✅ Python {version.major}.{version.minor}.{version.micro} detectado")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print_colored("❌ Se requiere Python 3.8 o superior", Colors.FAIL)
        return False
    
    if version.minor < 12:
        print_colored("⚠️  Se recomienda Python 3.12+", Colors.WARNING)
    
    return True

def detect_os():
    """Detectar sistema operativo"""
    os_name = platform.system().lower()
    print_colored(f"🖥️  Sistema operativo: {platform.system()} {platform.release()}")
    return os_name

def install_system_dependencies():
    """Instalar dependencias del sistema"""
    print_header("INSTALANDO DEPENDENCIAS DEL SISTEMA")
    
    os_name = detect_os()
    
    if os_name == "linux":
        # Detectar distribución Linux
        try:
            with open('/etc/os-release', 'r') as f:
                os_info = f.read().lower()
            
            if 'ubuntu' in os_info or 'debian' in os_info:
                print_colored("📦 Instalando dependencias para Ubuntu/Debian...")
                commands = [
                    "sudo apt update",
                    "sudo apt install -y python3-tk python3-dev python3-pip",
                    "sudo apt install -y libopencv-dev"
                ]
            elif 'fedora' in os_info or 'centos' in os_info or 'rhel' in os_info:
                print_colored("📦 Instalando dependencias para Fedora/CentOS/RHEL...")
                commands = [
                    "sudo dnf install -y tkinter python3-devel python3-pip",
                    "sudo dnf install -y opencv opencv-python"
                ]
            else:
                print_colored("⚠️  Distribución Linux no reconocida. Instala manualmente:", Colors.WARNING)
                print_colored("   - python3-tk (o tkinter)", Colors.WARNING)
                print_colored("   - python3-dev", Colors.WARNING)
                return True
            
            for cmd in commands:
                if not run_command(cmd, f"Ejecutando: {cmd}", check=False):
                    print_colored(f"⚠️  Fallo al ejecutar: {cmd}", Colors.WARNING)
                    print_colored("   Puede que necesites ejecutar manualmente", Colors.WARNING)
        
        except FileNotFoundError:
            print_colored("⚠️  No se pudo detectar la distribución Linux", Colors.WARNING)
    
    elif os_name == "darwin":  # macOS
        print_colored("🍎 Verificando Homebrew para macOS...")
        if run_command("brew --version", check=False):
            run_command("brew install python-tk opencv", "Instalando dependencias con Homebrew")
        else:
            print_colored("⚠️  Homebrew no encontrado. Instala desde: https://brew.sh", Colors.WARNING)
    
    elif os_name == "windows":
        print_colored("🪟 Windows detectado - las dependencias se instalarán con pip", Colors.OKBLUE)
    
    else:
        print_colored(f"⚠️  Sistema operativo {os_name} no reconocido", Colors.WARNING)
    
    return True

def create_virtual_environment():
    """Crear entorno virtual"""
    print_header("CONFIGURANDO ENTORNO VIRTUAL")
    
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print_colored("📁 Entorno virtual ya existe")
        response = input("¿Deseas recrearlo? (y/N): ").lower().strip()
        if response == 'y':
            print_colored("🗑️  Eliminando entorno virtual existente...")
            import shutil
            shutil.rmtree(venv_path)
        else:
            print_colored("✅ Usando entorno virtual existente")
            return True
    
    print_colored("🏗️  Creando entorno virtual...")
    venv.create(venv_path, with_pip=True)
    print_colored("✅ Entorno virtual creado exitosamente")
    
    return True

def get_pip_command():
    """Obtener comando pip para el entorno virtual"""
    if platform.system().lower() == "windows":
        return ".venv/Scripts/pip"
    else:
        return ".venv/bin/pip"

def install_python_dependencies():
    """Instalar dependencias Python"""
    print_header("INSTALANDO DEPENDENCIAS PYTHON")
    
    pip_cmd = get_pip_command()
    
    # Actualizar pip
    if not run_command(f"{pip_cmd} install --upgrade pip", "Actualizando pip"):
        return False
    
    # Instalar requirements
    if not run_command(f"{pip_cmd} install -r requirements.txt", "Instalando dependencias desde requirements.txt"):
        print_colored("❌ Error instalando dependencias", Colors.FAIL)
        return False
    
    print_colored("✅ Dependencias Python instaladas exitosamente")
    return True

def setup_database():
    """Configurar base de datos"""
    print_header("CONFIGURANDO BASE DE DATOS")
    
    python_cmd = ".venv/bin/python" if platform.system().lower() != "windows" else ".venv/Scripts/python"
    
    os.chdir("OpenCV")
    success = run_command(f"../{python_cmd} build_db.py", "Creando base de datos SQLite")
    os.chdir("..")
    
    if success:
        print_colored("✅ Base de datos configurada exitosamente")
    else:
        print_colored("❌ Error configurando base de datos", Colors.FAIL)
    
    return success

def verify_installation():
    """Verificar instalación"""
    print_header("VERIFICANDO INSTALACIÓN")
    
    python_cmd = ".venv/bin/python" if platform.system().lower() != "windows" else ".venv/Scripts/python"
    
    # Verificar módulo OpenCV
    print_colored("🔍 Verificando módulo OpenCV...")
    os.chdir("OpenCV")
    opencv_ok = run_command(f"../{python_cmd} verificar_opencv.py", check=False)
    os.chdir("..")
    
    # Verificar módulo Proyecto_SI
    print_colored("🔍 Verificando módulo Proyecto_SI...")
    os.chdir("Proyecto_SI")
    proyecto_ok = run_command(f"../{python_cmd} verificar_proyecto.py", check=False)
    os.chdir("..")
    
    if opencv_ok and proyecto_ok:
        print_colored("✅ Instalación verificada exitosamente", Colors.OKGREEN)
        return True
    else:
        print_colored("⚠️  Algunos componentes presentan advertencias", Colors.WARNING)
        return False

def show_usage_instructions():
    """Mostrar instrucciones de uso"""
    print_header("¡INSTALACIÓN COMPLETADA!")
    
    python_cmd = ".venv/bin/python" if platform.system().lower() != "windows" else ".venv\\Scripts\\python"
    activate_cmd = "source .venv/bin/activate" if platform.system().lower() != "windows" else ".venv\\Scripts\\activate"
    
    print_colored("🎉 GEOLEARNIA está listo para usar!", Colors.OKGREEN)
    print()
    print_colored("📋 COMANDOS PRINCIPALES:", Colors.OKBLUE)
    print_colored(f"   Activar entorno: {activate_cmd}")
    print()
    print_colored("🌐 APLICACIÓN WEB (Recomendado):", Colors.OKBLUE)
    print_colored(f"   cd Proyecto_SI")
    print_colored(f"   {python_cmd} web.py")
    print_colored("   Abrir: http://127.0.0.1:5001")
    print()
    print_colored("🔐 SISTEMA DE AUTENTICACIÓN:", Colors.OKBLUE)
    print_colored(f"   cd OpenCV")
    print_colored(f"   {python_cmd} main.py")
    print()
    print_colored("🖥️  APLICACIÓN DE ESCRITORIO:", Colors.OKBLUE)
    print_colored(f"   cd Proyecto_SI")
    print_colored(f"   {python_cmd} Video2.py")
    print()
    print_colored("📖 Ver README_GITHUB.md para documentación completa", Colors.OKCYAN)

def main():
    """Función principal"""
    print_colored("🎓 GEOLEARNIA Setup Script", Colors.HEADER)
    print_colored("Configurando proyecto educativo de IA...", Colors.HEADER)
    
    try:
        # Verificaciones iniciales
        if not check_python_version():
            sys.exit(1)
        
        # Instalación paso a paso
        steps = [
            ("Sistema", install_system_dependencies),
            ("Entorno Virtual", create_virtual_environment),
            ("Dependencias Python", install_python_dependencies),
            ("Base de Datos", setup_database),
            ("Verificación", verify_installation)
        ]
        
        for step_name, step_func in steps:
            try:
                if not step_func():
                    print_colored(f"❌ Fallo en paso: {step_name}", Colors.FAIL)
                    response = input("¿Continuar con la instalación? (y/N): ").lower().strip()
                    if response != 'y':
                        print_colored("❌ Instalación cancelada", Colors.FAIL)
                        sys.exit(1)
            except KeyboardInterrupt:
                print_colored("\n❌ Instalación cancelada por el usuario", Colors.FAIL)
                sys.exit(1)
            except Exception as e:
                print_colored(f"❌ Error inesperado en {step_name}: {e}", Colors.FAIL)
                response = input("¿Continuar con la instalación? (y/N): ").lower().strip()
                if response != 'y':
                    sys.exit(1)
        
        # Mostrar instrucciones finales
        show_usage_instructions()
        
    except KeyboardInterrupt:
        print_colored("\n❌ Instalación cancelada", Colors.FAIL)
        sys.exit(1)
    except Exception as e:
        print_colored(f"❌ Error crítico: {e}", Colors.FAIL)
        sys.exit(1)

if __name__ == "__main__":
    main()
