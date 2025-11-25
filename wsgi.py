# Importar la aplicación Flask
import sys
import os

# Agregar el directorio del proyecto al path
project_home = '/home/TU_USUARIO/chatbot-animo'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Importar la aplicación
from app import app as application
