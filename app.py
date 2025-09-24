#!/usr/bin/env python3
"""
GEOLEARNIA - Punto de entrada principal para despliegue
"""

import os
import sys

# Agregar el directorio Proyecto_SI al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'Proyecto_SI'))

# Cambiar al directorio Proyecto_SI
os.chdir(os.path.join(os.path.dirname(__file__), 'Proyecto_SI'))

# Importar y ejecutar la aplicación
from web_pointer import app

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5002))
    print(f"🎯 Iniciando GEOLEARNIA en puerto {port}")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)