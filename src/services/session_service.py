from datetime import datetime
from sqlalchemy.orm import Session as DBSession
from db.models.session import Session as TimerSession
from db.models.action import Action
from sqlalchemy import select
from sqlalchemy import update
    
def create_action(timer_session: TimerSession, type: str, engine):
    with DBSession(engine) as db_session:
        action_entity = Action(
            type=type,
            created_at=datetime.now(),
            session=timer_session
        )
        db_session.add(action_entity)
        db_session.commit()
        return action_entity

def create_session(engine):
    with DBSession(engine) as db_session:
        session_entity = TimerSession(
            is_active=True,
            started_at=datetime.now(),
        )
        db_session.add(session_entity)
        db_session.commit()
        return session_entity

def get_last_session(engine):
    with DBSession(engine) as db_session:
        stmt = select(TimerSession).order_by(TimerSession.started_at.desc()).limit(1)
        last_session = db_session.scalars(stmt).first()
        print(last_session)
        print(last_session.session_id)
        return last_session

def complete_session(timer_session: TimerSession, engine):
    print(timer_session)
    print(timer_session.id)
    finished_at = datetime.now()

    with DBSession(engine) as db_session:
        stmt = (
            update(TimerSession)
            .where(TimerSession.session_id == timer_session.session_id)
            .values(
                is_active=False,
                finished_at=finished_at,
                seconds_duration=int((finished_at - timer_session.started_at).total_seconds())
            )
        )

        db_session.execute(stmt)
        db_session.commit()

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
