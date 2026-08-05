from dotenv import load_dotenv
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
initialize_database()

#Prueba
#print(call_llm_with_sdk("hola como estas?"))
#call_llm_with_http()

#Funcionalidad
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL, echo=True)

from datetime import datetime
from sqlalchemy.orm import Session
from db.models.action import Action

with Session(engine) as session:
    
    session_registry = Session(
        is_active=True,
        started_at=datetime.now(),
        created_at=datetime.now()
    )
    
    play = Action(
        type="play",
        created_at=datetime.now(),
        session=session_registry
    )
    
    pause = Action(
        type="pause",
        created_at=datetime.now(),
        session=session_registry
    )
    
    stop = Action(
        type="stop",
        created_at=datetime.now(),
        session=session_registry
    )
    
    session.add_all([play, pause, stop])
    session.commit()

