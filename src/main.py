from dotenv import load_dotenv
from db.init_database import initialize_database
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializar BD 
initialize_database()

