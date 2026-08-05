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

#PRUEBA ---------------------------------------------
#print(call_llm_with_sdk("hola como estas?"))
#call_llm_with_http()

#Crear en BD
from sqlalchemy import create_engine
engine = create_engine(DATABASE_URL, echo=True)

from datetime import datetime
from sqlalchemy.orm import Session as DBSession
from db.models.session import Session as TimerSession
from db.models.action import Action

with DBSession(engine) as db_session:

    session_registry = TimerSession(
        is_active=True,
        started_at=datetime.now(),
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
    
    db_session.add_all([play, pause, stop])
    db_session.commit()


#Seleccionar en BD - SIMPLE
from sqlalchemy import select

session = DBSession(engine)

stmt = select(Action)

for action in session.scalars(stmt):
    print(action.type)
    

#Seleccionar en BD - JOIN
    
stmt = (
    select(TimerSession)
    .join(TimerSession.actions)
)

for session in session.scalars(stmt):
    print(session)
    
    
#-------------------------------------------

#Logic
from services.session_service import process_action
process_action("play")
process_action("pause")
process_action("play")
process_action("stop")