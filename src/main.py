import time

from dotenv import load_dotenv
from sqlalchemy import create_engine
from db.init_database import initialize_database
from services.llm_service import call_llm_with_sdk, call_llm_with_http
from pathlib import Path

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

#Variables Generales
DB_PATH = Path(__file__).resolve().parent / "db/app.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

print(DATABASE_URL)

# Inicializar BD

if(DB_PATH.exists()):
    print("Database already exists. Skipping initialization.")
else:
    print("Database does not exist. Initializing...")
    initialize_database()

engine = create_engine(DATABASE_URL, echo=True)

#Logic
from services.session_service import process_action
process_action("play", engine)
process_action("pause", engine)
time.sleep(2)
process_action("play", engine)
time.sleep(1)
process_action("stop", engine)