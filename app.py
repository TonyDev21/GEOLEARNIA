#!/usr/bin/env python3
"""
GEOLEARNIA v2.0 - Punto de entrada principal para despliegue
Arquitectura Web Moderna: Cliente → JavaScript → API REST → IA
"""

import os
import sys

# Agregar el directorio Proyecto_SI al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Proyecto_SI'))

# Cambiar al directorio Proyecto_SI
os.chdir(os.path.join(os.path.dirname(__file__), 'Proyecto_SI'))

# Importar y ejecutar la nueva API moderna
from web_api import app

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5002))
    host = os.environ.get('HOST', '0.0.0.0')
    print(f"🚀 Iniciando GEOLEARNIA v2.0 en {host}:{port}")
    print("🎯 Arquitectura Web Moderna - Cámara del Usuario")
    app.run(host=host, port=port, debug=False, threaded=True)