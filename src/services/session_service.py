from datetime import datetime
from sqlalchemy.orm import Session as DBSession
from db.models.session import Session as TimerSession
from db.models.action import Action
from sqlalchemy import select
    
def create_action(timer_session: TimerSession, type: str, engine):
    session = DBSession(engine)
    action_entity = Action(
        type=type,
        created_at=datetime.now(),
        session=timer_session
    )
    session.add(action_entity)
    session.commit()
    return action_entity

def create_session(engine):
    session = DBSession(engine)
    session_entity = TimerSession(
        is_active=True,
        started_at=datetime.now(),
    )
    session.add(session_entity)
    session.commit()
    return session_entity

def get_last_session(engine):
    session = DBSession(engine)
    stmt = select(TimerSession).order_by(TimerSession.started_at.desc()).limit(1)
    return session.scalars(stmt).first()

def complete_session(timer_session: TimerSession, engine):
    #Actualizar la session pasada como parámetro en la BD, seteando is_active a False y finish_at a la fecha actual
    session = DBSession(engine)
    timer_session.is_active = False
    timer_session.finished_at = datetime.now()
    timer_session.seconds_duration = (timer_session.finished_at - timer_session.started_at).total_seconds()
    session.commit()

def process_action(type: str, engine):
    last_session = get_last_session(engine)
    
    if(type) == "play":
        if(last_session is None or not last_session.is_active):
            session = create_session(engine)
            create_action(session, type, engine)
        else: # Cuando se reanuda luego de una pausa
            create_action(last_session, type, engine)

    elif(type) == "pause":
        create_action(last_session, type, engine)

    elif(type) == "stop":
        create_action(last_session, type, engine)
        complete_session(last_session, engine)
