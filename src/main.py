from dotenv import load_dotenv
from db.init_database import initialize_database
from services.llm_client import call_llm_with_sdk, call_llm_with_http
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializar BD 
initialize_database()

#Prueba
call_llm_with_sdk()
call_llm_with_http()

