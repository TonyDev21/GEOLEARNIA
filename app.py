#!/usr/bin/env python3
"""
GEOLEARNIA v3.0 - Punto de entrada principal para Railway
Reconocimiento Visual Automático con IA
"""

import os
import sys
import logging

# Configurar logging para Railway
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

logger.info("🚀 Iniciando GEOLEARNIA v3.0...")

# Agregar el directorio Proyecto_SI al path
project_dir = os.path.join(os.path.dirname(__file__), 'Proyecto_SI')
sys.path.insert(0, project_dir)

logger.info(f"📁 Directorio del proyecto: {project_dir}")

# Cambiar al directorio Proyecto_SI para que encuentre los archivos
os.chdir(project_dir)

logger.info(f"📂 Directorio actual: {os.getcwd()}")
logger.info(f"📄 Archivos disponibles: {os.listdir('.')}")

try:
    # Importar la aplicación Flask
    from web_api import app
    logger.info("✅ Aplicación Flask importada correctamente")
    
    # Configurar puerto para Railway
    port = int(os.environ.get('PORT', 5000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    logger.info(f"🌐 Iniciando servidor en {host}:{port}")
    
    if __name__ == '__main__':
        app.run(host=host, port=port, debug=False, threaded=True)
    
except Exception as e:
    logger.error(f"❌ Error al inicializar: {e}")
    raise