from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.orm import Session as DBSession

from db.models.action import Action
from db.models.session import Session as TimerSession


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
        return db_session.scalars(stmt).first()


def create_action(timer_session: TimerSession, type: str, engine):
    with DBSession(engine) as db_session:
        session_ref = db_session.merge(timer_session)
        db_session.add(
            Action(
                type=type,
                created_at=datetime.now(),
                session=session_ref,
            )
        )
        db_session.commit()


def complete_session(timer_session: TimerSession, engine):
    finished_at = datetime.now()

    with DBSession(engine) as db_session:
        session_to_complete = db_session.merge(timer_session)
        stmt = (
            update(TimerSession)
            .where(TimerSession.session_id == session_to_complete.session_id)
            .values(
                is_active=False,
                finish_at=finished_at,
                seconds_duration=int(
                    (finished_at - session_to_complete.started_at).total_seconds()
                ),
            )
        )
        db_session.execute(stmt)
        db_session.commit()


def process_action(type: str, engine):
    last_session = get_last_session(engine)

    if type == "play":
        if last_session is None or not last_session.is_active:
            session = create_session(engine)
        else:
            session = last_session
        create_action(session, type, engine)

    elif type == "pause":
        create_action(last_session, type, engine)

    elif type == "stop":
        create_action(last_session, type, engine)
        complete_session(last_session, engine)
